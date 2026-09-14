# Thumb builder

Generates a 1600 by 1000 blog-card image from a few lines of Python: one bioreactor glyph, three live signal traces, three headline lines. Renders through headless Chrome so the type is real text, and writes a 400 by 250 proof so you judge it at the size the grid shows.

```bash
./render.sh            # needs python3 with Pillow, and Chrome (set CHROME= to another path)
```

Edit the `CONFIG` block at the top of `build.py`: headline lines, colors, trace accents. Drop `.woff2` files into `fonts/` and name them in `FONT_FILES` to use a brand typeface; without them it falls back to the system sans-serif, which is what this public copy does.

## Why it looks the way it does

- **16:10, not 1200 by 630.** The card is `aspect-ratio: 16/10` with `object-fit: cover`. A social-share sized image loses its left and right edges on the card.
- **White ground.** The card behind the image is tinted. A tinted image has no visible edge.
- **No small labels.** The card renders about 326 px wide. Two headline lines survive; a 30 px mono label does not.
- **Traces start on their lane.** Each signal function evaluates to the lane at t = 0. The first version did not, and the fan-out from the port showed a step.
- **Lanes far enough apart.** The dip and the ramp amplitudes are set so no trace crosses another.

## Output of the original run

`../../assets/thumbnail.png` is the shipped card, rendered from this geometry with the company typeface.
