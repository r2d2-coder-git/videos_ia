// iPhone HDR (HLG) .MOV -> SDR BT.709 ProRes 422 HQ, using Apple's own tone mapping (AVFoundation).
// Usage: swift hdr2prores.swift in.MOV out.mov
import AVFoundation

let args = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let outURL = URL(fileURLWithPath: args[2])
try? FileManager.default.removeItem(at: outURL)

let track = asset.tracks(withMediaType: .video)[0]
let sdr: [String: Any] = [AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
                          AVVideoTransferFunctionKey: AVVideoTransferFunction_ITU_R_709_2,
                          AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2]
let reader = try AVAssetReader(asset: asset)
let out = AVAssetReaderTrackOutput(track: track, outputSettings: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_422YpCbCr10BiPlanarVideoRange,
    AVVideoColorPropertiesKey: sdr])
out.alwaysCopiesSampleData = false
reader.add(out)

let size = track.naturalSize
let writer = try AVAssetWriter(outputURL: outURL, fileType: .mov)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.proRes422HQ, AVVideoWidthKey: size.width, AVVideoHeightKey: size.height,
    AVVideoColorPropertiesKey: sdr])
input.transform = track.preferredTransform          // keep the portrait rotation
input.expectsMediaDataInRealTime = false
writer.add(input)

reader.startReading(); writer.startWriting(); writer.startSession(atSourceTime: .zero)
let q = DispatchQueue(label: "w"); let done = DispatchSemaphore(value: 0); var n = 0
input.requestMediaDataWhenReady(on: q) {
    while input.isReadyForMoreMediaData {
        if let sb = out.copyNextSampleBuffer() { input.append(sb); n += 1; if n % 600 == 0 { print("frames", n) } }
        else { input.markAsFinished(); writer.finishWriting { done.signal() }; return }
    }
}
done.wait()
print("status", writer.status.rawValue, writer.error?.localizedDescription ?? "ok", "frames", n)
