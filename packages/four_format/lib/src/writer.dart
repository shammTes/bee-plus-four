import 'dart:async';
import 'dart:io';
import 'dart:typed_data';

import 'package:cryptography/cryptography.dart';

import 'format.dart';
import 'keys.dart';
import 'meta.dart';
import 'source.dart';

/// A batch: one batch key shared by many files, wrapped under the master key.
class FourBatch {
  FourBatch({required this.id, required this.key, this.mkVersion = 1});
  factory FourBatch.create(String id, {int mkVersion = 1}) => FourBatch(id: id, key: FourKeys.random(32), mkVersion: mkVersion);
  final String id;
  final Uint8List key;
  final int mkVersion;
}

abstract final class FourWriter {
  /// Encrypts [input] into [add] (called with each output piece, in order). Streams; never holds the whole file.
  static Future<FourPreamble> write({
    required FourSource input,
    required FutureOr<void> Function(List<int>) add,
    required FourMeta meta,
    required List<int> masterKey,
    required FourBatch batch,
    List<int>? thumbnail,
    int chunkSize = FourFormat.defaultChunk,
    void Function(int done, int total)? onProgress,
  }) async {
    if (chunkSize <= 0 || chunkSize > FourFormat.maxChunk) throw ArgumentError('chunkSize');
    FourKeys.need32(masterKey, 'master key');
    FourKeys.need32(batch.key, 'batch key');
    final aes = FourKeys.aes;
    final fileId = FourKeys.random(FourFormat.idLen);
    final ck = FourKeys.random(32);
    final wbk = await FourKeys.wrap(masterKey, batch.key, FourKeys.batchAad(batch.id));
    final wck = await FourKeys.wrap(batch.key, ck, fileId);
    final ckKey = SecretKey(ck);
    final size = input.length;
    final count = FourPreamble.chunksFor(size, chunkSize);
    final headerPlain = meta.encode();
    final hasThumb = thumbnail != null && thumbnail.isNotEmpty;
    final pre = FourPreamble(
      flags: hasThumb ? FourFormat.flagThumb : 0,
      mkVersion: batch.mkVersion,
      fileId: fileId,
      batchId: batch.id,
      wrappedBatchKey: wbk,
      wrappedContentKey: wck,
      noncePrefix: FourKeys.random(FourFormat.prefixLen),
      chunkSize: chunkSize,
      chunkCount: count,
      plainSize: size,
      headerLen: headerPlain.length + FourFormat.nonceLen + FourFormat.tagLen,
      thumbLen: hasThumb ? thumbnail.length + FourFormat.nonceLen + FourFormat.tagLen : 0,
    );
    final preBytes = pre.encode();
    await add(preBytes);
    final h = await aes.encrypt(headerPlain, secretKey: ckKey, nonce: FourKeys.random(12), aad: [...preBytes, 0x48]);
    await add(h.concatenation());
    if (hasThumb) {
      final t = await aes.encrypt(thumbnail, secretKey: ckKey, nonce: FourKeys.random(12), aad: [...preBytes, 0x54]);
      await add(t.concatenation());
    }
    final mac = await FourKeys.hmac.newMacSink(secretKey: SecretKey(await FourKeys.footerKey(ck)));
    mac.add(preBytes);
    for (var i = 0; i < count; i++) {
      final off = i * chunkSize;
      final len = pre.plainLenOf(i);
      final plain = await input.read(off, len);
      final box = await aes.encrypt(plain, secretKey: ckKey, nonce: pre.chunkNonce(i), aad: pre.chunkAad(i));
      await add(box.cipherText);
      await add(box.mac.bytes);
      mac.add(box.mac.bytes);
      onProgress?.call(off + len, size);
    }
    mac.close();
    await add(FourFormat.footerMagic);
    await add((await mac.mac()).bytes);
    return pre;
  }

  /// In-memory helper (tests, small files).
  static Future<Uint8List> encryptBytes(Uint8List data, {required FourMeta meta, required List<int> masterKey, required FourBatch batch, List<int>? thumbnail, int chunkSize = FourFormat.defaultChunk}) async {
    final out = BytesBuilder(copy: false);
    await write(input: BytesSource(data), add: out.add, meta: meta, masterKey: masterKey, batch: batch, thumbnail: thumbnail, chunkSize: chunkSize);
    return out.toBytes();
  }

  /// File → file, streaming. Writes to `<out>.part` then renames.
  static Future<FourPreamble> encryptFile(String inPath, String outPath, {required FourMeta meta, required List<int> masterKey, required FourBatch batch, List<int>? thumbnail, int chunkSize = FourFormat.defaultChunk, void Function(int, int)? onProgress}) async {
    final src = await FileSource.open(inPath);
    final tmp = File('$outPath.part');
    final raf = await tmp.open(mode: FileMode.write);
    try {
      final pre = await write(input: src, add: (b) => raf.writeFrom(b), meta: meta, masterKey: masterKey, batch: batch, thumbnail: thumbnail, chunkSize: chunkSize, onProgress: onProgress);
      await raf.close();
      await tmp.rename(outPath);
      return pre;
    } catch (_) {
      await raf.close();
      if (await tmp.exists()) await tmp.delete();
      rethrow;
    } finally {
      await src.close();
    }
  }
}
