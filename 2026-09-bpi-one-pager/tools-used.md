# Tools used

Everything ran inside Claude Code. No MCP data sources were needed: the copy already existed, and the work was design, rendering, and measurement.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| Claude Artifacts, Design System type | Artifact | Held design system v2: color tokens in two themes, type scale, spacing, radii, and a guideline page that lists each removed v1 pattern | The page regenerates some of its own files when opened. Read the files back before you republish. |
| Claude Artifacts, Design canvas type | Artifact | Held the one-pager as two fixed-size artboards (one per side), then two more at bleed size on a separate canvas page | "All artboards (.pdf)" exports every artboard on a canvas page, so the print-shop set needs its own page. The canvas stored a downsized screenshot. Upload the full-resolution file. |
| Headless Chrome over the DevTools protocol | Local | HTML to PDF for Letter and A4, and a report of each sheet's rendered height | `--print-to-pdf` hangs on this Mac. Drive `Page.printToPDF` over a WebSocket. Script in [`tools/print-kit/`](tools/print-kit/). |
| Swift + PDFKit | Local | Rendered each PDF page to PNG and dumped its text, to count pages and check that nothing moved to a third page | No poppler on this machine. Twenty lines of Swift do the job. |
| `sips` (macOS) | Local | Read pixel sizes to compute effective dpi; cropped the screenshot | `sips` silently ignores a crop when offset plus height equals the image height. Use a smaller height or a temp file. |
| Python 3 | Local | Built the bleed artboards from the originals: new size, +0.125in on outer padding, solid line colors, the new image | Keep the originals. The office-print version and the print-shop version are different files. |
| Skills | Skill | `pdf` for the print pass. The design-system work followed the design type's own `print.md` reference: fixed pages, 1pt = 4/3px, and no grey lighter than #767676. | |
