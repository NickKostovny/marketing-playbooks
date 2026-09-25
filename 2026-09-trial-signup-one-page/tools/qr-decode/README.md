# qr-decode

Before you change or retire a URL, find out which printed pieces point at it. Banners, one-pagers and booth signs cannot be recalled. This script reads every QR code in the images you give it and prints what each one encodes.

```bash
swift qr-decode.swift banner.png one-pager-page-2.png
```

Output, one line per file:

```
banner.png: https://example.com/trial?utm_source=booth&utm_medium=banner
one-pager-page-2.png: https://example.com/trial
```

- macOS only. It uses Core Image's built-in QR detector, so there is nothing to install.
- Works on PNG and JPEG exports, and on screenshots of a PDF page. For a multi-page PDF, export the page with the code as an image first.
- "no QR code found" usually means the code is too small in the image. Export at a higher resolution.

On this rebuild it confirmed that the booth banner and the one-pager both pointed at the page-one URL, which became the whole flow, so no printed piece broke.
