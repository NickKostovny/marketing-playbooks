import Foundation
import PDFKit
import AppKit
let args = CommandLine.arguments
let url = URL(fileURLWithPath: args[1]); let outDir = args[2]; let scale = CGFloat(Double(args[3]) ?? 2.0)
guard let doc = PDFDocument(url: url) else { print("cannot open"); exit(1) }
print("pages:", doc.pageCount)
for i in 0..<doc.pageCount {
  guard let page = doc.page(at: i) else { continue }
  let box = page.bounds(for: .mediaBox)
  print("page \(i+1) size pt: \(box.width) x \(box.height)")
  let w = Int(box.width * scale), h = Int(box.height * scale)
  let img = NSImage(size: NSSize(width: w, height: h))
  img.lockFocus()
  NSColor.white.setFill(); NSRect(x: 0, y: 0, width: w, height: h).fill()
  let ctx = NSGraphicsContext.current!.cgContext
  ctx.saveGState(); ctx.scaleBy(x: scale, y: scale)
  page.draw(with: .mediaBox, to: ctx)
  ctx.restoreGState()
  img.unlockFocus()
  if let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff), let png = rep.representation(using: .png, properties: [:]) {
    try? png.write(to: URL(fileURLWithPath: "\(outDir)/page-\(i+1).png"))
  }
  let text = page.string ?? ""
  try? text.write(toFile: "\(outDir)/page-\(i+1).txt", atomically: true, encoding: .utf8)
  print("--- page \(i+1) text (\(text.count) chars) ---"); print(text)
}
