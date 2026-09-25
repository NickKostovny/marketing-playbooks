# Print preflight for a handout on good stock

Run this before you send a PDF to a print shop. Every item is a failure I have seen, and none of them show on screen.

## Ask the printer first

- [ ] Finished size, and whether they want bleed (usually 0.125in, which is 12px at 96px/in).
- [ ] Stock: coated (gloss or silk) or uncoated. Uncoated absorbs ink, so it fills in fine light-on-dark type and softens hairlines.
- [ ] File format and color: PDF, RGB or CMYK, and whether they want crop marks.

## Page geometry

- [ ] If any color touches an edge, the file is the finished size plus bleed on every side. Letter with bleed is 8.75 × 11.25in (840 × 1080px).
- [ ] All content moves in by the bleed amount, so after trim it sits where you designed it.
- [ ] Text and logos stay at least 0.25in inside the trim line. I use about 0.58in.
- [ ] Keep a separate office-print version at the exact page size with no bleed. Home and office printers cannot print to the edge.

## Images

- [ ] Every raster is 300 dpi or more at its placed size. Effective dpi = pixel width ÷ placed width in inches. A 380px-wide slot is 3.96in, so it needs about 1190px.
- [ ] Use the original file, not the copy your design tool stored. Tools often downsize on upload.
- [ ] Logos are vector (SVG or PDF), not PNG.

## Lines and tints

- [ ] Hairlines are 1px or more, and they are solid colors, not transparent ink. `rgba(ink, 0.1)` on white becomes a solid hex of the same color.
- [ ] No page-wide tint under 5%. On premium stock it looks like dirty paper, and flat light tints can band on a digital press. Let the stock be the ground.
- [ ] One tint band per page, at most.

## Type

- [ ] Body 12pt (16px) or larger. Captions 9pt (12px) or larger.
- [ ] No grey text lighter than #767676 on white.
- [ ] Light text on a dark flood: 11pt (15px) or larger, regular weight or heavier, and not pale grey. Small reversed type fills in on uncoated stock.
- [ ] No links styled as links. Paper cannot click. Write the URL as bold text, or use a QR code with its own UTM source.
- [ ] The font license covers embedding in a distributed PDF. A web-font license often does not.

## Ink

- [ ] Large dark floods: ask for one paper proof on the real stock before the full run.
- [ ] The page still reads in grayscale.

## Verify by measuring

- [ ] The page count is correct in the exported PDF (not in the preview).
- [ ] Render each page to PNG and look at it at 100%.
- [ ] Extract the text, and check that nothing moved to an extra page.
