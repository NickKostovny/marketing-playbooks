# Design canvas to print-shop PDF, with bleed

This recipe is for a Claude Design canvas (or any HTML page) laid out as one fixed-size artboard per printed side. It adds bleed and fixes the problems you can only see on paper. The originals stay as they are.

## 1. Read before you change

- Read the canvas index and each artboard's full source.
- List every image the artboards use and check the pixel size of each: `sips -g pixelWidth -g pixelHeight <file>`. Compute the effective dpi at placed size. If one is under 300, find the original file and upload it.

## 2. Make the bleed copies

For each artboard, write a new file (for example `Front-Print`) with these changes:

| Change | From | To (Letter) |
| --- | --- | --- |
| Root size and `$preview` | 816 × 1056 | 840 × 1080 |
| Outer padding (top, sides, bottom of the last band) | n | n + 12px |
| Page ground | light grey tint | `#ffffff` |
| Transparent lines, e.g. `rgba(28,54,60,0.1)` | alpha | the solid hex it composites to on white, e.g. `#d6dbdc` |
| Light text on dark, 14px | pale grey | 15px, slightly lighter |
| Links | underlined `<a>` | bold `<span>` |
| Screenshot | stored copy | full-resolution upload |

Background bands already run edge to edge, so they extend into the bleed without further changes.

To compute the solid color: `c = alpha * ink + (1 - alpha) * 255`, per channel.

## 3. Put them on their own canvas page

"Export all artboards" exports every artboard on one canvas page. Put the bleed artboards on a page named something like "Print shop (bleed)", and the originals on "Office print". Each page then exports its own complete PDF.

## 4. Send it

Tell the printer: "Trim to 8.5 × 11in. 0.125in bleed is included." Ask for one paper proof if there is a large dark area, and confirm your font license covers an embedded PDF.
