#!/usr/bin/env python3
"""Cut clips from a long recording on word timings.

For each clip in the spec: pull an audio window around the rough in and out
points, run whisper.cpp with token offsets, find the start and end phrases,
cut the source at the word boundaries, and write word-grouped SRT subtitles
plus a manifest the branding step reads.

usage: precise-cuts.py clips.json

Spec (JSON):
{
  "source": "recording.mp4",           # the long recording
  "work":   "work",                    # scratch dir; WAV, probes and clips go here
  "model":  "work/models/ggml-small.en.bin",
  "fixes":  [["GP context", "GMP context"]],   # ASR corrections applied to subtitles
  "clips": [
    {"id": "m1-trust", "speaker": "Speaker name", "role": "Role, Company",
     "title": "Clip title for the title card.",
     "rough_start": "0:39:10", "rough_end": "0:40:40",
     "start_phrase": "but before we jump in", "end_phrase": "defined use",
     "hold_for_consent": false}
  ]
}
Needs: ffmpeg, ffprobe, whisper-cli (whisper.cpp) on PATH, and a ggml model file.
"""
import json, os, re, subprocess, sys

def secs(v):
    if isinstance(v, (int, float)): return float(v)
    p = [float(x) for x in str(v).split(":")]
    while len(p) < 3: p.insert(0, 0.0)
    return p[0]*3600 + p[1]*60 + p[2]

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower()).split()
def run(cmd, **kw): return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)

def ts(x):
    ms = int(round((x % 1)*1000)); x = int(x)
    return f"{x//3600:02d}:{(x%3600)//60:02d}:{x%60:02d},{ms:03d}"

def words_in_window(wav, model, t0, t1, probe_dir, tag):
    """Transcribe [t0, t1] of the WAV and return [[start_abs, end_abs, word], ...]."""
    seg = os.path.join(probe_dir, f"{tag}.wav")
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1-t0:.3f}", "-i", wav, "-c", "copy", seg])
    run(["whisper-cli", "-m", model, "-f", seg, "-l", "en", "-t", "8", "-ojf", "-of", os.path.join(probe_dir, tag), "-nt"])
    j = json.load(open(os.path.join(probe_dir, f"{tag}.json")))
    words = []
    for s in j["transcription"]:
        for tok in s.get("tokens", []):
            txt = tok["text"]
            # skip whisper control tokens such as <|endoftext|> and [_BEG_]; they
            # otherwise end up burned into the subtitles
            if txt.startswith("[_") or re.match(r"^\s*<\|.*\|>\s*$", txt) or not txt.strip(): continue
            txt = re.sub(r"<\|[^|]*\|>", "", txt)
            a = t0 + tok["offsets"]["from"]/1000; b = t0 + tok["offsets"]["to"]/1000
            if txt.startswith(" ") or not words: words.append([a, b, txt.strip()])
            else: words[-1][1] = b; words[-1][2] += txt   # sub-word piece
    return words

def find(words, phrase, prefer="first"):
    """Exact token match. If the ASR phrased it slightly differently, retry with
    the phrase shortened from the front (for a start) or the back (for an end)."""
    ph = norm(phrase)
    while len(ph) >= 2:
        n = len(ph)
        hits = [i for i in range(len(words)-n+1)
                if [w for k in range(n) for w in norm(words[i+k][2])] == ph]
        if hits:
            return (hits[0] if prefer == "first" else hits[-1]), n
        ph = ph[1:] if prefer == "first" else ph[:-1]
    raise LookupError(f"phrase not found: {phrase!r}")

def main(spec_path):
    spec = json.load(open(spec_path))
    src, W, model = spec["source"], spec.get("work", "work"), spec["model"]
    fixes = [tuple(x) for x in spec.get("fixes", [])]
    probe, C = os.path.join(W, "probe"), os.path.join(W, "clips")
    os.makedirs(probe, exist_ok=True); os.makedirs(C, exist_ok=True)
    wav = spec.get("wav") or os.path.join(W, "source-16k.wav")
    if not os.path.exists(wav):
        print("extracting 16 kHz mono audio ...")
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav])
    def fix(s):
        for a, b in fixes: s = s.replace(a, b)
        return s
    manifest = []
    for c in spec["clips"]:
        cid, r0, r1 = c["id"], secs(c["rough_start"]), secs(c["rough_end"])
        words = words_in_window(wav, model, r0-12, r1+12, probe, cid)
        try:
            i0, _ = find(words, c["start_phrase"])
        except LookupError as e:
            print(f"  {cid}: start phrase missing, using rough start ({e})")
            i0 = next(i for i, w in enumerate(words) if w[0] >= r0 - 0.5)
        try:
            i1, n1 = find(words, c["end_phrase"], "last"); j1 = i1 + n1 - 1
        except LookupError as e:
            print(f"  {cid}: end phrase missing, using rough end ({e})")
            j1 = max(i for i, w in enumerate(words) if w[1] <= r1 + 0.5)
        # run the end out to the close of the sentence (at most 8 more words), so a
        # clip never stops mid-thought when the end phrase sits before the full stop
        k = j1
        while k < len(words)-1 and k-j1 < 8 and not re.search(r"[.?!]$", words[k][2]): k += 1
        if re.search(r"[.?!]$", words[k][2]): j1 = k
        start, end = words[i0][0] - 0.20, words[j1][1] + 0.30
        out = os.path.join(C, f"{cid}.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", src, "-t", f"{end-start:.3f}",
             "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
        # subtitles: cues of <= 12 words or <= 5 s, and break on sentence ends
        cues, cur = [], []
        for w in words[i0:j1+1]:
            cur.append(w)
            if len(cur) >= 12 or (cur[-1][1]-cur[0][0]) >= 5.0 or (re.search(r"[.?!]$", w[2]) and len(cur) >= 5):
                cues.append(cur); cur = []
        if cur: cues.append(cur)
        lines = []
        for n, cue in enumerate(cues, 1):
            a = max(0, cue[0][0]-start)
            b = (cues[n][0][0]-start-0.05) if n < len(cues) else (cue[-1][1]-start+0.2)
            lines.append(f"{n}\n{ts(a)} --> {ts(max(b, a+0.6))}\n{fix(' '.join(x[2] for x in cue))}\n")
        srt = os.path.join(C, f"{cid}.srt")
        open(srt, "w").write("\n".join(lines))
        text = fix(" ".join(x[2] for x in words[i0:j1+1]))
        manifest.append({**{k: c[k] for k in ("id", "speaker", "role", "title")},
                         "source_start": round(start, 2), "source_end": round(end, 2),
                         "duration_s": round(end-start, 1), "hold_for_consent": bool(c.get("hold_for_consent")),
                         "file": os.path.abspath(out), "srt": os.path.abspath(srt), "transcript": text})
        print(f"{cid}: {end-start:.1f}s ({start:.1f}-{end:.1f}) cues={len(cues)} hold={c.get('hold_for_consent', False)}")
        print("   starts:", text[:70], "...  ends:", text[-60:])
    json.dump(manifest, open(os.path.join(C, "manifest.json"), "w"), indent=1)
    print("manifest written:", os.path.join(C, "manifest.json"))

if __name__ == "__main__":
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    main(sys.argv[1])
