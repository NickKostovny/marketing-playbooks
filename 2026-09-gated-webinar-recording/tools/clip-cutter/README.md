# clip-cutter

Cut share-ready clips from a long recording on word timings, then brand them for LinkedIn.

Two scripts and a runner:

| File | Does |
| --- | --- |
| `precise-cuts.py` | Reads `clips.json`. For each clip, transcribes a window around the rough in and out points with whisper.cpp, finds the start and end phrases in the word offsets, extends the end to the close of the sentence, cuts the source there, writes word-grouped SRT subtitles and a `manifest.json`. |
| `brand-clip.py` | Frames one cut in a 1080 by 1080 square: soft canvas, rounded 16:9 card with a shadow, logo or wordmark, speaker line, burned-in subtitles from the SRT, a title card in, an end card out. Speech normalised to -14 LUFS, stereo. |
| `render-all.sh` | Runs both over every clip in the spec and writes a contact sheet per clip. |

## Requirements

- Python 3.9 or later, Pillow (`pip install pillow`).
- ffmpeg and ffprobe on PATH. Text is rendered with Pillow and composited as PNG overlays, so an ffmpeg built without `drawtext` or the `subtitles` filter works.
- whisper.cpp (`whisper-cli`) and a ggml model. `brew install whisper-cpp` on macOS. Model: `ggml-small.en.bin` from the whisper.cpp model repository into `work/models/`. Small is enough for word timings; the fixes list handles domain terms.
- A font. The script looks for Helvetica Neue (macOS), DejaVu Sans, Liberation Sans, then Arial. Pass `--font` for anything else. The published clips used Helvetica Neue; a single `.ttf` is used for every weight, so headlines lose their bold on Linux unless you point `--font` at a bold face.

## Run

```bash
./render-all.sh clips.json out/ --brand "Company" --footer "From the September webinar" \
  --cta-url "example.com/page" --end-line "1 h 34 min." --end-line "Work email required."
```

Add `--logo logo.png --logo-light logo-light.png` for a real logo (PNG with alpha; the light one goes on the dark end card). Without them the brand name is set as a wordmark. The logo files are not in this repo.

`clips.json` format is in the docstring at the top of `precise-cuts.py`. Times can be `H:MM:SS` or seconds.

## Palette

Inlined at the top of `brand-clip.py` as RGB tuples. Swap for your own.

## Known limits

- Phrase matching is exact on normalised tokens, with a fallback that shortens the phrase from the front (start) or the back (end). If neither finds it, the tool falls back to the rough time and says so. Read the "starts:" and "ends:" lines it prints.
- Subtitle cues are at most 12 words or 5 seconds, three lines on the card. Very fast speech can still overflow; the contact sheet shows it.
- The end card always shows the CTA URL as plain text. Set `--cta-url ""` to drop it.
- Everything is re-encoded once at CRF 20. Good enough for LinkedIn's own transcode; not an archival master.

Sample cards produced by this version, with placeholder speaker text, are in `../../assets/`.
