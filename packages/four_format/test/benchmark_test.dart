import 'dart:typed_data';

import 'package:four_format/four_format.dart';
import 'package:test/test.dart';

/// Pure-Dart decrypt throughput (the fallback path; Android video uses javax.crypto in FourChunkReader.kt).
void main() {
  test('benchmark: pure-Dart chunk decrypt throughput', () async {
    final mk = await FourKeys.devMasterKey();
    final data = Uint8List(8 << 20);
    final enc = await FourWriter.encryptBytes(data, meta: FourMeta(title: 'b', subject: 's', grade: 9, type: FourType.video, mime: 'video/mp4'), masterKey: mk, batch: FourBatch.create('b'));
    final r = await FourReader.open(BytesSource(enc), (_) async => mk);
    await r.readChunk(0);
    final sw = Stopwatch()..start();
    for (var i = 0; i < r.preamble.chunkCount; i++) {
      await r.readChunk(i);
    }
    final mbs = 8 / (sw.elapsedMicroseconds / 1e6);
    // ignore: avoid_print
    print('FOUR_BENCH pure-Dart AES-GCM decrypt: ${mbs.toStringAsFixed(1)} MB/s');
    // seek cost: one random chunk
    final s2 = Stopwatch()..start();
    await r.readRange(5 << 20, 1000);
    // ignore: avoid_print
    print('FOUR_BENCH one seek (1 chunk): ${s2.elapsedMilliseconds} ms');
    expect(mbs, greaterThan(0));
  });
}
