import 'dart:math' as math;
import 'dart:typed_data';

import 'package:cryptography/cryptography.dart';

import 'format.dart';
import 'keys.dart';
import 'meta.dart';
import 'source.dart';

/// Returns the master key for an mkVersion, or null if this device has none (= locked).
typedef MasterKeyResolver = Future<List<int>?> Function(int mkVersion);

/// Opens a resource. Chunks are decrypted on demand, so seeking costs one chunk.
class FourReader {
  FourReader._(this.source, this.preamble, this.meta, this.thumbnail, this._ck);

  final FourSource source;
  final FourPreamble preamble;
  final FourMeta meta;
  final Uint8List? thumbnail;
  final SecretKey _ck;

  int get length => preamble.plainSize;
  String get id => preamble.fileIdHex;

  /// Reads only the plaintext preamble (no key needed): detects 4 files and their batch.
  static Future<FourPreamble> peek(FourSource src) async {
    final head = await src.read(0, math.min(src.length, FourPreamble.maxLength));
    final p = FourPreamble.decode(head);
    if (src.length < p.totalLength) throw const FourIntegrityException('file is truncated');
    if (src.length > p.totalLength) throw const FourIntegrityException('file has trailing bytes');
    return p;
  }

  static Future<FourReader> open(FourSource src, MasterKeyResolver masterKey, {bool verify = false}) async {
    final p = await peek(src);
    final mk = await masterKey(p.mkVersion);
    if (mk == null) throw const FourKeyException('this phone has not unlocked 4');
    final bk = await FourKeys.unwrap(mk, p.wrappedBatchKey, FourKeys.batchAad(p.batchId));
    final ck = await FourKeys.unwrap(bk, p.wrappedContentKey, p.fileId);
    final pre = p.encode();
    final aes = FourKeys.aes;
    final key = SecretKey(ck);
    Future<Uint8List> blob(int off, int len, int tag) async {
      final raw = await src.read(off, len);
      try {
        final box = SecretBox.fromConcatenation(raw, nonceLength: 12, macLength: 16, copy: false);
        return Uint8List.fromList(await aes.decrypt(box, secretKey: key, aad: [...pre, tag]));
      } on SecretBoxAuthenticationError {
        throw const FourIntegrityException('header was modified');
      }
    }

    final meta = FourMeta.decode(await blob(pre.length, p.headerLen, 0x48));
    final thumb = p.hasThumb ? await blob(pre.length + p.headerLen, p.thumbLen, 0x54) : null;
    final r = FourReader._(src, p, meta, thumb, key);
    if (verify) await r.verifyFooter(ck);
    return r;
  }

  /// Checks the footer HMAC over every chunk tag (catches reordered/replaced chunks without decrypting).
  Future<void> verifyFooter([List<int>? ck]) async {
    final p = preamble;
    final mac = await Hmac.sha256().newMacSink(secretKey: SecretKey(await FourKeys.footerKey(ck ?? await _ck.extractBytes())));
    mac.add(p.encode());
    for (var i = 0; i < p.chunkCount; i++) {
      mac.add(await source.read(p.offsetOf(i) + p.plainLenOf(i), FourFormat.tagLen));
    }
    mac.close();
    final want = (await mac.mac()).bytes;
    final f = await source.read(p.footerStart, FourFormat.footerLen);
    if (f[0] != 0x34 || f[1] != 0x45 || f[2] != 0x4E || f[3] != 0x44) {
      throw const FourIntegrityException('footer missing');
    }
    var diff = 0;
    for (var i = 0; i < 32; i++) {
      diff |= want[i] ^ f[4 + i];
    }
    if (diff != 0) throw const FourIntegrityException('footer check failed');
  }

  Future<Uint8List> readChunk(int i) async {
    final p = preamble;
    if (i < 0 || i >= p.chunkCount) throw RangeError.index(i, null, 'chunk', null, p.chunkCount);
    final len = p.plainLenOf(i);
    final raw = await source.read(p.offsetOf(i), len + FourFormat.tagLen);
    try {
      final box = SecretBox(Uint8List.sublistView(raw, 0, len), nonce: p.chunkNonce(i), mac: Mac(Uint8List.sublistView(raw, len)));
      final out = await FourKeys.aes.decrypt(box, secretKey: _ck, aad: p.chunkAad(i));
      return out is Uint8List ? out : Uint8List.fromList(out);
    } on SecretBoxAuthenticationError {
      throw FourIntegrityException('chunk $i was modified');
    }
  }

  /// Plaintext bytes [start, start+len). Decrypts only the chunks it touches.
  Future<Uint8List> readRange(int start, int len) async {
    if (start < 0 || len < 0 || start + len > length) throw RangeError('range outside resource');
    final out = Uint8List(len);
    var pos = start, w = 0;
    final cs = preamble.chunkSize;
    while (w < len) {
      final ci = pos ~/ cs, inner = pos - ci * cs;
      final c = await readChunk(ci);
      final n = math.min(c.length - inner, len - w);
      out.setRange(w, w + n, c, inner);
      w += n;
      pos += n;
    }
    return out;
  }

  Future<Uint8List> readAll() => readRange(0, length);

  Future<void> close() => source.close();
}
