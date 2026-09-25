#!/usr/bin/env python3
"""Brand a talking-head clip for LinkedIn: 1080x1080, soft canvas, rounded 16:9
card with a shadow, logo or wordmark, speaker line, timed subtitles from an SRT,
a title card in and an end card out. Speech only, normalised to -14 LUFS.

Text is rendered with Pillow to PNG and composited with ffmpeg overlays, so the
script works on an ffmpeg built without drawtext or the subtitles filter.

usage: brand-clip.py <clip.mp4> <clip.srt> <out.mp4> --title "..." --speaker "..." --role "..."
                     [--logo logo.png] [--logo-light logo-light.png] [--brand "Company"]
                     [--footer "From the ... webinar"] [--cta-url "example.com/page"]
                     [--end-headline "Watch the full session."] [--end-line "..." --end-line "..."]
                     [--font /path/to/font.ttf|.ttc] [--intro 2.8] [--outro 3.4]
Needs: ffmpeg, ffprobe, Pillow.
"""
import argparse, os, re, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Palette, RGB. Swap for your own; these are the values the published clips used.
PALETTE = {
    "bg":       (242, 245, 238),   # canvas
    "brand":    (29, 54, 59),      # end-card ground
    "headline": (34, 52, 54),
    "body":     (85, 93, 90),
    "muted":    (115, 124, 121),
    "label":    (156, 162, 160),
    "border":   (229, 233, 232),
    "white":    (255, 255, 255),
    "on_brand": (183, 197, 200),   # secondary text on the end card
}
FONT_CANDIDATES = [
    "/System/Library/Fonts/HelveticaNeue.ttc",                       # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",               # Debian/Ubuntu
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
S, FPS = 1080, 30
ENC = ["-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart"]

def rgb(k): return PALETTE[k]

_font_path, _faces = None, {}
def font(style, size):
    """style: 'bold' | 'medium' | 'regular'. A .ttc exposes named faces; a single
    .ttf is used for every style (bold falls back to the same face)."""
    global _font_path
    if _font_path is None:
        _font_path = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
        if _font_path is None: raise SystemExit("no font found; pass --font")
        if _font_path.endswith(".ttc"):
            for i in range(0, 20):
                try: _faces[ImageFont.truetype(_font_path, 20, index=i).getname()[1].lower()] = i
                except Exception: break
    if _faces:
        want = {"bold": ["bold", "medium"], "medium": ["medium", "bold"], "regular": ["regular", "light"]}[style]
        for w in want:
            for name, idx in _faces.items():
                if name == w or name.replace(" ", "") == w:
                    return ImageFont.truetype(_font_path, size, index=idx)
        return ImageFont.truetype(_font_path, size, index=0)
    if style == "bold":
        for cand in [_font_path.replace("-Regular", "-Bold"), _font_path.replace(".ttf", "-Bold.ttf")]:
            if os.path.exists(cand): return ImageFont.truetype(cand, size)
    return ImageFont.truetype(_font_path, size)

def wrap(text, fnt, max_w, d):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_logo(img, logo_path, brand, x=40, y=44, h=26, color="brand"):
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        lw = round(logo.width * h / logo.height)
        img.alpha_composite(logo.resize((lw, h), Image.LANCZOS), (x, y))
    else:   # no logo file: set the brand name as a small wordmark
        ImageDraw.Draw(img).text((x, y - 2), brand, font=font("bold", 30), fill=rgb(color))

def card_geometry(margin=40, top=108):
    w = S - 2 * margin
    return margin, top, w, round(w * 9 / 16)

def base_frame(speaker_line, path, a):
    x, y, w, h = card_geometry()
    img = Image.new("RGBA", (S, S), rgb("bg") + (255,))
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x, y + 18, x + w, y + h + 18], radius=26, fill=rgb("brand") + (64,))
    img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(28)))
    draw_logo(img, a.logo, a.brand)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + w, y + h], radius=26, fill=rgb("white"), outline=rgb("border"), width=1)
    d.text((x, y + h + 26), speaker_line, font=font("regular", 26), fill=rgb("muted"))
    img.convert("RGB").save(path)
    return x, y, w, h

def rounded_mask(w, h, path, radius=26):
    m = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=(255, 255, 255, 255))
    m.save(path)

def subtitle_png(text, path, band_top=770, band_h=280):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font("medium", 40)
    lines = wrap(text, f, S - 2 * 72, d)[:3]
    lh = 52; y0 = band_top + (band_h - lh * len(lines)) / 2
    for i, ln in enumerate(lines):
        d.text(((S - d.textlength(ln, font=f)) / 2, y0 + i * lh), ln, font=f, fill=rgb("headline"))
    img.save(path)

def title_card(a, path):
    img = Image.new("RGBA", (S, S), rgb("bg") + (255,))
    draw_logo(img, a.logo, a.brand)
    d = ImageDraw.Draw(img)
    ft = font("bold", 60); y = 300
    for ln in wrap(a.title, ft, S - 2 * 80, d)[:4]:
        d.text((80, y), ln, font=ft, fill=rgb("headline")); y += 72
    fs = font("regular", 30)
    d.text((80, y + 28), a.speaker, font=fs, fill=rgb("body"))
    d.text((80, y + 68), a.role, font=fs, fill=rgb("muted"))
    if a.footer: d.text((80, S - 90), a.footer, font=font("regular", 24), fill=rgb("label"))
    img.convert("RGB").save(path)

def end_card(a, path):
    img = Image.new("RGBA", (S, S), rgb("brand") + (255,))
    if a.logo_light and os.path.exists(a.logo_light):
        logo = Image.open(a.logo_light).convert("RGBA"); lh = 44
        img.alpha_composite(logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS), (80, 300))
    else:
        ImageDraw.Draw(img).text((80, 300), a.brand, font=font("bold", 44), fill=rgb("bg"))
    d = ImageDraw.Draw(img)
    d.text((80, 420), a.end_headline, font=font("bold", 54), fill=rgb("bg"))
    y = 500
    for ln in a.end_line:
        d.text((80, y), ln, font=font("regular", 30), fill=rgb("on_brand")); y += 60
    if a.cta_url: d.text((80, max(y + 40, 660)), a.cta_url, font=font("medium", 36), fill=rgb("bg"))
    img.convert("RGB").save(path)

def parse_srt(path):
    cues = []
    for block in open(path).read().strip().split("\n\n"):
        L = block.split("\n")
        if len(L) < 3: continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+) --> (\d+):(\d+):(\d+),(\d+)", L[1])
        if not m: continue
        g = list(map(int, m.groups()))
        cues.append((g[0]*3600 + g[1]*60 + g[2] + g[3]/1000, g[4]*3600 + g[5]*60 + g[6] + g[7]/1000, " ".join(L[2:]).strip()))
    for i in range(len(cues) - 1):   # butt cues together so there is no blank gap
        a, b, t = cues[i]; cues[i] = (a, max(b, cues[i + 1][0] - 0.05), t)
    return cues

def run(cmd): subprocess.run(cmd, check=True)

def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip"); ap.add_argument("srt"); ap.add_argument("out")
    ap.add_argument("--title", required=True); ap.add_argument("--speaker", required=True); ap.add_argument("--role", required=True)
    ap.add_argument("--logo"); ap.add_argument("--logo-light"); ap.add_argument("--brand", default="Brand")
    ap.add_argument("--footer", default=""); ap.add_argument("--cta-url", default="")
    ap.add_argument("--end-headline", default="Watch the full session.")
    ap.add_argument("--end-line", action="append", default=[])
    ap.add_argument("--font"); ap.add_argument("--intro", type=float, default=2.8); ap.add_argument("--outro", type=float, default=3.4)
    a = ap.parse_args()
    if a.font: FONT_CANDIDATES.insert(0, a.font)
    work = tempfile.mkdtemp(prefix="brandclip-")
    bg, mask = os.path.join(work, "bg.png"), os.path.join(work, "mask.png")
    x, y, w, h = base_frame(f"{a.speaker} · {a.role}", bg, a)
    rounded_mask(w, h, mask)
    clip_dur = duration(a.clip)

    cues = parse_srt(a.srt)
    inputs = ["-loop", "1", "-i", bg, "-i", a.clip, "-i", mask]
    fc = (f"[1:v]fps={FPS},scale={w}:{h}:force_original_aspect_ratio=decrease,"
          f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=white,format=rgba[vv];"
          f"[2:v]alphaextract[m];[vv][m]alphamerge[rv];[0:v]fps={FPS},format=rgba[bg];"
          f"[bg][rv]overlay={x}:{y}:shortest=1[v0]")
    last = "v0"
    for i, (s, e, t) in enumerate(cues):
        p = os.path.join(work, f"sub{i:03d}.png"); subtitle_png(t, p)
        inputs += ["-loop", "1", "-i", p]
        fc += f";[{3+i}:v]format=rgba[s{i}];[{last}][s{i}]overlay=0:0:enable='between(t,{s:.3f},{e:.3f})'[v{i+1}]"
        last = f"v{i+1}"
    fc += f";[{last}]format=yuv420p,fade=t=in:st=0:d=0.25,fade=t=out:st={clip_dur-0.3:.3f}:d=0.3[vout];"
    fc += "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[aout]"
    body = os.path.join(work, "body.mp4")
    run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", fc, "-map", "[vout]", "-map", "[aout]",
         "-t", f"{clip_dur:.3f}"] + ENC + [body])

    tc, ec = os.path.join(work, "title.png"), os.path.join(work, "end.png")
    title_card(a, tc); end_card(a, ec)
    intro, outro = os.path.join(work, "intro.mp4"), os.path.join(work, "outro.mp4")
    for png, dur, outp, fo in [(tc, a.intro, intro, 0.3), (ec, a.outro, outro, 0.5)]:
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", png, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
             "-filter_complex", f"[0:v]fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.3,fade=t=out:st={dur-fo:.3f}:d={fo}[v]",
             "-map", "[v]", "-map", "1:a", "-t", f"{dur:.3f}"] + ENC + [outp])
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in [intro, body, outro]))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", a.out])
    print(f"wrote {a.out}  ({duration(a.out):.1f}s, body {clip_dur:.1f}s, {len(cues)} cues)")
    print(f"cards kept in {work} (title.png, end.png)")

if __name__ == "__main__":
    main()
