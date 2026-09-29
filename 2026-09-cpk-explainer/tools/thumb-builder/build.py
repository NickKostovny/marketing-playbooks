#!/usr/bin/env python3
"""Blog-card thumbnail builder: one process distribution between two dashed specification
limits, three headline lines. Writes thumb.html; render.sh turns it into a PNG.

Public version of the builder used for "What is Cpk, and how do biologics teams use it?".
Same frame as the OPC UA card builder. The original used a licensed typeface. This one loads
any .woff2 files you drop into fonts/ and otherwise falls back to the system sans-serif.

Why these choices:
  1600x1000 is 16:10, the card's exact aspect ratio, so object-fit: cover crops nothing.
  White ground, because the card behind it is tinted; a tinted image dissolves into it.
  No small labels: at the card's ~326 px width, "LSL" and "USL" turn to grey mush.
  The mean sits off center toward the upper limit. The nearer gap is the one that sets Cpk,
  so it gets the only accent color; the far gap stays quiet.
  The geometry is a real Cpk: (USL - MEAN) / 3SD = 1.09 and (MEAN - LSL) / 3SD = 2.05.
  If you move the curve, keep the picture honest: the accent goes on the smaller side.

Edit the CONFIG block. Everything else is geometry.
"""
import math
import pathlib

# ---------------------------------------------------------------- CONFIG
W, H = 1600, 1000
HEADLINE = [
    ("Spread, centering, and the nearer limit.", "ink"),
    ("How much room the process has.",           "ink"),
    ("Cpk, explained.",                          "dim"),
]
BG      = "#FFFFFF"   # image ground
FILL    = "#E4E8DC"   # area under the curve
STROKE  = "#4A5D61"   # curve, baseline, mean line, far-gap arrow, dim type
INK     = "#1C363C"   # headline type and specification limits
ACCENT  = "#B88A29"   # the nearer gap, the one that sets Cpk
FONT_FILES = {  # optional: drop .woff2 files in fonts/ and name them here
    400: "fonts/regular.woff2",
}

# Geometry in px. Cpu = (USL - MEAN) / (3 * SD) = 1.09; Cpl = (MEAN - LSL) / (3 * SD) = 2.05.
LSL, USL, MEAN, SD = 470, 1450, 1110, 104
BASE, PEAK = 812, 436
# ------------------------------------------------------------------------


def curve():
    """Normal curve from mean - 4.2 SD to mean + 4.2 SD."""
    pts = []
    x0, x1 = MEAN - 4.2 * SD, MEAN + 4.2 * SD
    for i in range(241):
        x = x0 + (x1 - x0) * i / 240
        y = BASE - (BASE - PEAK) * math.exp(-0.5 * ((x - MEAN) / SD) ** 2)
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return d, x0, x1


def arrow(xa, xb, y, color, sw):
    """Double-headed arrow from xa to xb."""
    h = sw * 3.2
    return (f'<path d="M{xa + h:.1f},{y} H{xb - h:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="M{xa:.1f},{y} l{h:.1f},{-h * 0.7:.1f} v{h * 1.4:.1f} Z" fill="{color}"/>'
            f'<path d="M{xb:.1f},{y} l{-h:.1f},{-h * 0.7:.1f} v{h * 1.4:.1f} Z" fill="{color}"/>')


def font_css():
    here = pathlib.Path(__file__).parent
    faces = []
    for weight, rel in FONT_FILES.items():
        if (here / rel).exists():
            faces.append(f'@font-face {{ font-family:"Card"; src:url("{rel}") format("woff2"); font-weight:{weight}; }}')
    family = '"Card", ' if faces else ""
    return "\n".join(faces), f'{family}-apple-system, "Helvetica Neue", Arial, sans-serif'


def build():
    d, x0, x1 = curve()
    limits = "".join(f'<path d="M{x},{PEAK - 56} V{BASE}" stroke="{INK}" stroke-width="6" stroke-dasharray="20 16" stroke-linecap="round"/>'
                     for x in (LSL, USL))
    # The nearer limit gets the accent. With the default geometry that is the upper one.
    near_upper = (USL - MEAN) <= (MEAN - LSL)
    lower_color, lower_w = (STROKE, 5) if near_upper else (ACCENT, 8)
    upper_color, upper_w = (ACCENT, 8) if near_upper else (STROKE, 5)
    faces, family = font_css()
    headline = "\n".join(
        f'  <text class="h{" dim" if tone == "dim" else ""}" x="76" y="{156 + 76 * i}">{line}</text>'
        for i, (line, tone) in enumerate(HEADLINE))
    return f'''<!doctype html>
<meta charset="utf-8">
<style>
  {faces}
  * {{ margin:0; padding:0; }}
  html,body {{ width:{W}px; height:{H}px; background:{BG}; overflow:hidden; }}
  svg {{ display:block; }}
  .h     {{ font-family:{family}; font-weight:400; font-size:62px; letter-spacing:-0.022em; fill:{INK}; }}
  .h.dim {{ fill:{STROKE}; }}
</style>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="{BG}"/>
{headline}
  <path d="{d} L{x1:.1f},{BASE} L{x0:.1f},{BASE} Z" fill="{FILL}"/>
  <path d="{d}" fill="none" stroke="{STROKE}" stroke-width="7" stroke-linejoin="round"/>
  <path d="M{LSL - 70},{BASE} H{USL + 70}" stroke="{STROKE}" stroke-width="5" stroke-linecap="round"/>
  <path d="M{MEAN},{PEAK} V{BASE}" stroke="{STROKE}" stroke-width="5"/>
  {limits}
  {arrow(LSL + 6, MEAN - 6, 890, lower_color, lower_w)}
  {arrow(MEAN + 6, USL - 6, 890, upper_color, upper_w)}
</svg>
'''


if __name__ == "__main__":
    out = pathlib.Path(__file__).parent / "thumb.html"
    out.write_text(build())
    print("wrote", out)
    print(f"Cpu = {(USL - MEAN) / (3 * SD):.2f}, Cpl = {(MEAN - LSL) / (3 * SD):.2f}")
