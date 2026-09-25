// Print the URL (or text) inside every QR code image you pass in.
// usage: swift qr-decode.swift image1.png [image2.jpg ...]
// macOS only: uses Core Image's built-in QR detector, no installs.
import Foundation
import CoreImage

let paths = CommandLine.arguments.dropFirst()
if paths.isEmpty {
  print("usage: swift qr-decode.swift <image> [<image> ...]")
  exit(1)
}
let detector = CIDetector(ofType: CIDetectorTypeQRCode, context: nil,
                          options: [CIDetectorAccuracy: CIDetectorAccuracyHigh])!
for path in paths {
  guard let image = CIImage(contentsOf: URL(fileURLWithPath: path)) else {
    print("\(path): cannot read"); continue
  }
  let found = detector.features(in: image).compactMap { ($0 as? CIQRCodeFeature)?.messageString }
  print("\(path): \(found.isEmpty ? "no QR code found" : found.joined(separator: " | "))")
}
