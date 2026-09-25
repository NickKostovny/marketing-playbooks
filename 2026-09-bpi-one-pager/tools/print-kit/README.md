# print-kit

Two small tools that turn an HTML handout into PDFs and check the result by measurement. They exist because headless Chrome's `--print-to-pdf` hangs on my Mac and there is no poppler.

## print-cdp.mjs

Starts headless Chrome with a debugging port. It opens the page over the DevTools protocol, waits for fonts, and reports the rendered height of every `.sheet` element. It then writes three PDFs: Letter with backgrounds off, Letter with backgrounds on, and A4 with backgrounds off.

```bash
node print-cdp.mjs "$PWD/one-pager.html" "$PWD/out/v1"
```

Needs Node 22 or later (it uses the global `WebSocket`) and Google Chrome at the default macOS path. Edit `CH` for other systems. The viewport is 816px wide (Letter at 96px/in). The `.sheet` selector and the 0.5in margins match my page. Change them to match yours.

## pdfdump.swift

Renders each page of a PDF to PNG and writes each page's text to a file. It also prints the page count and page sizes.

```bash
swiftc pdfdump.swift -o pdfdump
./pdfdump out/v1-letter-nobg.pdf out 2
```

The last argument is the render scale (2 = 144 dpi). macOS only (PDFKit).

## The gates I use

- Each sheet 960px or less at a 720px content width (Letter minus 0.5in margins, with room to spare).
- Exactly the intended page count on both Letter and A4.
- The text dump of the last page ends with the last line you expect.
