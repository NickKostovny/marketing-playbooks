#!/usr/bin/env python3
"""Blog-card thumbnail builder: one stirred-tank bioreactor, three live signal traces,
three headline lines. Writes thumb.html; render.sh turns it into a PNG.

Public version of the builder used for "What is OPC UA, and how do bioreactors use it?".
The original used a licensed typeface. This one loads any .woff2 files you drop into
fonts/ and otherwise falls back to the system sans-serif.

Why these choices:
  1600x1000 is 16:10, the card's exact aspect ratio, so object-fit: cover crops nothing.
  White ground, because the card behind it is tinted; a tinted image dissolves into it.
  No small labels: at the card's ~326 px width, 30 px mono text turns to grey mush.
  Every trace starts exactly on its lane, or the fan-out from the port shows a visible step.

Edit the CONFIG block. Everything else is geometry.
"""
import math
import pathlib

# ---------------------------------------------------------------- CONFIG
W, H = 1600, 1000
HEADLINE = [
    ("pH, DO, temperature, agitation.", "ink"),
    ("Live from the controller.",       "ink"),
    ("OPC UA, explained.",              "dim"),
]
BG        = "#FFFFFF"   # image ground
FILL      = "#E4E8DC"   # vessel fill
STROKE    = "#4A5D61"   # vessel stroke and dim type
INK       = "#1C363C"   # headline type
ACCENTS   = ["#4E7A90", "#B88A29", "#62734F"]   # one per trace
FONT_FILES = {  # optional: drop .woff2 files in fonts/ and name them here
    400: "fonts/regular.woff2",
    500: "fonts/medium.woff2",
}
# ------------------------------------------------------------------------


def reactor(cx, base_y, w):
    """Stirred-tank glyph. Proportions measured off a product video frame:
    body h/w 1.055, straight wall 0.925w, dished bottom 0.13w,
    impellers at 0.40w and 0.655w, sparger bar 0.315w at 0.925w."""
    sw   = w * 0.018
    wall = w * 0.925
    dish = w * 0.130
    top  = base_y - dish - wall
    x0, x1 = cx - w / 2, cx + w / 2
    foot = w * 0.105
    sh   = dish * 0.58
    body = (f"M{x0:.1f},{top:.1f} H{x1:.1f} V{top+wall:.1f} "
            f"Q{x1:.1f},{top+wall+sh:.1f} {cx+foot:.1f},{base_y:.1f} H{cx-foot:.1f} "
            f"Q{x0:.1f},{top+wall+sh:.1f} {x0:.1f},{top+wall:.1f} Z")

    def impeller(y):
        half, cap = w * 0.26, w * 0.040
        return (f'<path d="M{cx-half:.1f},{y:.1f} H{cx+half:.1f}"/>'
                f'<path d="M{cx-half:.1f},{y-cap:.1f} V{y+cap:.1f}"/>'
                f'<path d="M{cx+half:.1f},{y-cap:.1f} V{y+cap:.1f}"/>')

    shaft_top = top - w * 0.105
    bar_w, bar_h = w * 0.15, w * 0.032
    port_y = top + w * 0.185
    port_x = x1 + w * 0.215
    ticks = "".join(f'<path d="M{cx+dx*w:.1f},{top+wall-w*0.020-dy*w:.1f} v{dy*w:.1f}"/>'
                    for dx, dy in ((-0.075, 0.032), (0.0, 0.050), (0.075, 0.028)))
    svg = f'''<g fill="none" stroke="{STROKE}" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round">
    <path d="{body}" fill="{FILL}"/>
    <path d="M{cx:.1f},{shaft_top:.1f} V{top+wall*0.76:.1f}"/>
    <rect x="{cx-bar_w:.1f}" y="{shaft_top-bar_h/2:.1f}" width="{bar_w*2:.1f}" height="{bar_h:.1f}" rx="{bar_h/2:.1f}" fill="{STROKE}" stroke="none"/>
    {impeller(top + w * 0.400)}
    {impeller(top + w * 0.655)}
    <path d="M{x1:.1f},{port_y:.1f} H{port_x:.1f}"/>
    <path d="M{port_x:.1f},{port_y-w*0.048:.1f} V{port_y+w*0.048:.1f}"/>
    {ticks}
    <path d="M{cx-w*0.157:.1f},{top+wall-w*0.020:.1f} H{cx+w*0.157:.1f}"/>
  </g>'''
    return svg, (port_x, port_y)


def trace(kind, lane_y, x0, x1, n=160):
    """Three signal shapes. Each evaluates to lane_y at t=0 so the fan-out joins cleanly."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        if kind == "ring":        # overshoot, ring, settle (a pH controller)
            y = lane_y - 46 * (1 - math.exp(-14 * t)) * math.cos(11 * t) * math.exp(-2.6 * t) - 18 * t
        elif kind == "dip":       # dip and recover (DO after a feed)
            y = lane_y + 52 * math.exp(-((t - 0.34) / 0.12) ** 2) - 8 * t
        else:                     # ramp to setpoint and hold (temperature)
            y = lane_y - 48 * (1 - math.exp(-5.5 * t)) + 5 * math.sin(16 * t) * math.exp(-3 * t)
        pts.append((x, y))
    return " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), pts[-1]


def font_css():
    here = pathlib.Path(__file__).parent
    faces = []
    for weight, rel in FONT_FILES.items():
        if (here / rel).exists():
            faces.append(f'@font-face {{ font-family:"Card"; src:url("{rel}") format("woff2"); font-weight:{weight}; }}')
    family = '"Card", ' if faces else ""
    return "\n".join(faces), f'{family}-apple-system, "Helvetica Neue", Arial, sans-serif'


def build():
    CX, BASE_Y, VW = 420, 850, 300
    vessel, (px, py) = reactor(CX, BASE_Y, VW)
    lanes = [("ring", 590), ("dip", 690), ("ramp", 832)]   # keep lanes far enough apart that no trace crosses another
    x_start, x_end = 780, 1524
    paths = []
    for (kind, lane_y), color in zip(lanes, ACCENTS):
        d, (ex, ey) = trace(kind, lane_y, x_start, x_end)
        fan = f"M{px:.1f},{py:.1f} C{px+70:.1f},{py:.1f} {x_start-70:.1f},{lane_y:.1f} {x_start:.1f},{lane_y:.1f}"
        paths.append(f'<path d="{fan} L{d}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="12" fill="{color}"/>')
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
{vessel}
{chr(10).join(paths)}
</svg>
'''


if __name__ == "__main__":
    out = pathlib.Path(__file__).parent / "thumb.html"
    out.write_text(build())
    print("wrote", out)
