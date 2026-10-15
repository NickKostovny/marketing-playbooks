#!/usr/bin/env python3
"""
Turn light-on-dark logos into ink-on-transparent PNGs for a light page.

Input: one image with one or more light logos on a flat dark background
(the kind a partner pastes into a chat). Output: one PNG per logo, the
background removed, every logo pixel recoloured to INK, alpha from how far
each pixel is from the background colour.

usage: python3 recolour-logos.py in.png out-dir name-a name-b ...
The names are assigned left to right. Logos are split on the widest empty
column run in the middle of the image.
"""
import sys
from PIL import Image

INK = (0x1C, 0x36, 0x3C)

def main(src, out_dir, names):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()
    bg = px[0, 0]
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()
    cols = [0] * w
    for y in range(h):
        for x in range(w):
            d = max(abs(px[x, y][i] - bg[i]) for i in range(3))
            a = min(255, int(d * 255 / 150))
            if a > 20:
                cols[x] += 1
            op[x, y] = (*INK, a)
    # split on empty column runs
    runs, start = [], None
    for x in range(w):
        if cols[x] == 0 and start is None:
            start = x
        if cols[x] > 0 and start is not None:
            runs.append((start, x)); start = None
    gaps = sorted([r for r in runs if r[1] - r[0] > 20 and 50 < r[0] < w - 50], key=lambda r: r[0])
    bounds, left = [], 0
    for g in gaps[: len(names) - 1]:
        bounds.append((left, g[0])); left = g[1]
    bounds.append((left, w))
    for (x0, x1), name in zip(bounds, names):
        sub = out.crop((x0, 0, x1, h))
        sub = sub.crop(sub.getbbox())
        sub.save(f"{out_dir}/{name}.png")
        print(name, sub.size)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
