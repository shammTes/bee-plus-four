import 'dart:convert';
import 'dart:typed_data';

/// Byte layout constants (version 1). All integers big-endian.
abstract final class FourFormat {
  static const magic = [0x34, 0x52, 0x45, 0x53]; // "4RES"
  static const footerMagic = [0x34, 0x45, 0x4E, 0x44]; // "4END"
  static const version = 1;
  static const flagThumb = 1;
  static const nonceLen = 12, tagLen = 16, keyLen = 32, idLen = 16, prefixLen = 8;
  static const wrappedLen = nonceLen + keyLen + tagLen; // 60
  static const footerLen = 4 + 32;
  static const defaultChunk = 256 * 1024;
  static const maxChunk = 8 << 20;
  static const maxHeader = 1 << 20, maxThumb = 2 << 20;

  static bool hasMagic(List<int> b) => b.length >= 4 && b[0] == magic[0] && b[1] == magic[1] && b[2] == magic[2] && b[3] == magic[3];
}

class FourFormatException implements Exception {
  const FourFormatException(this.message);
  final String message;
  @override
  String toString() => 'FourFormatException: $message';
}

/// Wrong key / not unlocked / batch key missing.
class FourKeyException extends FourFormatException {
  const FourKeyException(super.message);
}

/// Bytes changed, reordered or cut short.
class FourIntegrityException extends FourFormatException {
  const FourIntegrityException(super.message);
}

/// The plaintext preamble. It is authenticated as AAD of the header, so any edit fails decryption.
class FourPreamble {
  FourPreamble({
    required this.flags,
    required this.mkVersion,
    required this.fileId,
    required this.batchId,
    required this.wrappedBatchKey,
    required this.wrappedContentKey,
    required this.noncePrefix,
    required this.chunkSize,
    required this.chunkCount,
    required this.plainSize,
    required this.headerLen,
    required this.thumbLen,
    this.version = FourFormat.version,
  });

  final int version, flags, mkVersion, chunkSize, chunkCount, plainSize, headerLen, thumbLen;
  final Uint8List fileId, wrappedBatchKey, wrappedContentKey, noncePrefix;
  final String batchId;

  String get fileIdHex => fileId.map((b) => b.toRadixString(16).padLeft(2, '0')).join();
  bool get hasThumb => flags & FourFormat.flagThumb != 0;

  int get encodedLength => 4 + 4 + FourFormat.idLen + 1 + utf8.encode(batchId).length + 2 * FourFormat.wrappedLen + FourFormat.prefixLen + 4 + 4 + 8 + 4 + 4;
  int get dataStart => encodedLength + headerLen + thumbLen;
  int get chunkStride => chunkSize + FourFormat.tagLen;
  int plainLenOf(int i) => i < chunkCount - 1 ? chunkSize : plainSize - chunkSize * (chunkCount - 1);
  int offsetOf(int i) => dataStart + i * chunkStride;
  int get footerStart => dataStart + plainSize + chunkCount * FourFormat.tagLen;
  int get totalLength => footerStart + FourFormat.footerLen;

  static int chunksFor(int plainSize, int chunkSize) => plainSize == 0 ? 1 : (plainSize + chunkSize - 1) ~/ chunkSize;

  Uint8List encode() {
    final bid = utf8.encode(batchId);
    if (bid.length > 64) throw const FourFormatException('batchId too long');
    final b = BytesBuilder(copy: false)
      ..add(FourFormat.magic)
      ..add([version, flags, mkVersion, 0])
      ..add(fileId)
      ..addByte(bid.length)
      ..add(bid)
      ..add(wrappedBatchKey)
      ..add(wrappedContentKey)
      ..add(noncePrefix);
    final t = ByteData(24)
      ..setUint32(0, chunkSize)
      ..setUint32(4, chunkCount)
      ..setUint64(8, plainSize)
      ..setUint32(16, headerLen)
      ..setUint32(20, thumbLen);
    b.add(t.buffer.asUint8List());
    return b.toBytes();
  }

  /// Parses from the first bytes of a file. Needs at most [maxLength] bytes.
  static const maxLength = 4 + 4 + 16 + 1 + 64 + 120 + 8 + 24;

  static FourPreamble decode(Uint8List b) {
    if (!FourFormat.hasMagic(b)) throw const FourFormatException('not a 4 resource (bad magic)');
    if (b.length < 26) throw const FourIntegrityException('file too short');
    final ver = b[4];
    if (ver != FourFormat.version) throw FourFormatException('unsupported version $ver');
    if (b[7] != 0) throw const FourIntegrityException('reserved byte set');
    var o = 8;
    final id = Uint8List.fromList(b.sublist(o, o += FourFormat.idLen));
    final bl = b[o++];
    if (b.length < o + bl + 2 * FourFormat.wrappedLen + FourFormat.prefixLen + 24) throw const FourIntegrityException('file too short');
    final bid = utf8.decode(b.sublist(o, o += bl), allowMalformed: true);
    final wbk = Uint8List.fromList(b.sublist(o, o += FourFormat.wrappedLen));
    final wck = Uint8List.fromList(b.sublist(o, o += FourFormat.wrappedLen));
    final np = Uint8List.fromList(b.sublist(o, o += FourFormat.prefixLen));
    final d = ByteData.sublistView(b, o, o + 24);
    final p = FourPreamble(
      version: ver,
      flags: b[5],
      mkVersion: b[6],
      fileId: id,
      batchId: bid,
      wrappedBatchKey: wbk,
      wrappedContentKey: wck,
      noncePrefix: np,
      chunkSize: d.getUint32(0),
      chunkCount: d.getUint32(4),
      plainSize: d.getUint64(8),
      headerLen: d.getUint32(16),
      thumbLen: d.getUint32(20),
    );
    if (p.chunkSize == 0 || p.chunkSize > FourFormat.maxChunk) throw const FourFormatException('bad chunk size');
    if (p.chunkCount != chunksFor(p.plainSize, p.chunkSize)) throw const FourIntegrityException('chunk count mismatch');
    if (p.headerLen > FourFormat.maxHeader || p.thumbLen > FourFormat.maxThumb) throw const FourFormatException('header too large');
    return p;
  }

  /// nonce for chunk i = prefix(8) || u32(i)
  Uint8List chunkNonce(int i) {
    final n = Uint8List(FourFormat.nonceLen)..setAll(0, noncePrefix);
    ByteData.sublistView(n).setUint32(8, i);
    return n;
  }

  /// AAD for chunk i = fileId || u32(i) || u8(isLast)
  Uint8List chunkAad(int i) {
    final a = Uint8List(FourFormat.idLen + 5)..setAll(0, fileId);
    ByteData.sublistView(a).setUint32(FourFormat.idLen, i);
    a[FourFormat.idLen + 4] = i == chunkCount - 1 ? 1 : 0;
    return a;
  }
}
