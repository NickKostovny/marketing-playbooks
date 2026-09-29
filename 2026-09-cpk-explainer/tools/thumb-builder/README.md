# Thumb builder (Cpk card)

Generates a 1600 by 1000 blog-card image from a few lines of Python: one process distribution between two dashed specification limits, the nearer gap in the accent color, three headline lines. Renders through headless Chrome so the type is real text, and writes a 400 by 250 proof so you judge it at the size the grid shows.

```bash
./render.sh            # needs python3 with Pillow, and Chrome (set CHROME= to another path)
```

Edit the `CONFIG` block at the top of `build.py`: headline lines, colors, and the curve geometry. Drop `.woff2` files into `fonts/` and name them in `FONT_FILES` to use a brand typeface; without them it falls back to the system sans-serif, which is what this public copy does.

It is the same frame as the [OPC UA card builder](../../../2026-09-opc-ua-explainer/tools/thumb-builder/), so two explainers in the same grid read as a series.

## Why it looks the way it does

- **The picture is a correct Cpk.** The mean sits at 1110 px between limits at 470 and 1450 px, with a standard deviation of 104 px. That gives Cpu 1.09 and Cpl 2.05, so the upper side sets Cpk, and the upper gap gets the accent. `build.py` prints both values and puts the accent on whichever side is nearer, so an edit cannot make the picture wrong.
- **No labels on the limits.** "LSL" and "USL" at a legible size in the full image become unreadable on a 326 px card. Dashed lines read as limits without them.
- **16:10, white ground.** The card is `aspect-ratio: 16/10` with `object-fit: cover`, and the card behind the image is tinted. Same reasons as the OPC UA card.
- **One accent.** The far gap is the same gray as the curve. Two accent colors would say two things matter.

## Output of the original run

`../../assets/thumbnail.png` is the shipped card, rendered from this geometry with the company typeface.
