import 'dart:io';
import 'dart:typed_data';

import 'package:four_format/four_format.dart';
import 'package:test/test.dart';

void main() {
  late List<int> mk;
  final batch = FourBatch.create('test-batch');
  Uint8List data(int n) => Uint8List.fromList(List.generate(n, (i) => (i * 31 + 7) & 0xff));
  FourMeta meta() => FourMeta(title: 'Cells', subject: 'biology', grade: 11, unit: '3', type: FourType.pdf, mime: 'application/pdf');
  Future<List<int>?> Function(int) res(List<int>? k) => (_) async => k;

  setUpAll(() async => mk = await FourKeys.devMasterKey());

  test('round trip with thumbnail, footer verified', () async {
    final d = data(10000);
    final enc = await FourWriter.encryptBytes(d, meta: meta(), masterKey: mk, batch: batch, thumbnail: [1, 2, 3], chunkSize: 1024);
    final r = await FourReader.open(BytesSource(enc), res(mk), verify: true);
    expect(r.meta.title, 'Cells');
    expect(r.meta.grade, 11);
    expect(r.thumbnail, [1, 2, 3]);
    expect(await r.readAll(), d);
    expect(r.preamble.chunkCount, 10);
    expect(enc.length, r.preamble.totalLength);
  });

  test('empty and exact-multiple sizes', () async {
    for (final n in [0, 1, 1024, 2048, 2049]) {
      final d = data(n);
      final enc = await FourWriter.encryptBytes(d, meta: meta(), masterKey: mk, batch: batch, chunkSize: 1024);
      final r = await FourReader.open(BytesSource(enc), res(mk), verify: true);
      expect(await r.readAll(), d, reason: 'n=$n');
    }
  });

  test('chunk seek decrypts only touched chunks', () async {
    final d = data(50000);
    final enc = await FourWriter.encryptBytes(d, meta: meta(), masterKey: mk, batch: batch, chunkSize: 4096);
    final counting = _Counting(BytesSource(enc));
    final r = await FourReader.open(counting, res(mk));
    counting.reads = 0;
    expect(await r.readRange(30000, 100), d.sublist(30000, 30100));
    expect(counting.reads, 1);
    expect(await r.readRange(4090, 10), d.sublist(4090, 4100)); // straddles two chunks
    expect(counting.reads, 3);
    expect(await r.readChunk(12), d.sublist(12 * 4096));
  });

  test('wrong master key / locked', () async {
    final enc = await FourWriter.encryptBytes(data(100), meta: meta(), masterKey: mk, batch: batch);
    expect(() => FourReader.open(BytesSource(enc), res(FourKeys.random(32))), throwsA(isA<FourKeyException>()));
    expect(() => FourReader.open(BytesSource(enc), res(null)), throwsA(isA<FourKeyException>()));
  });

  test('tampered chunk byte is detected', () async {
    final d = data(5000);
    final enc = await FourWriter.encryptBytes(d, meta: meta(), masterKey: mk, batch: batch, chunkSize: 1024);
    final r0 = await FourReader.open(BytesSource(enc), res(mk));
    final bad = Uint8List.fromList(enc)..[r0.preamble.offsetOf(2) + 5] ^= 1;
    final r = await FourReader.open(BytesSource(bad), res(mk));
    expect(await r.readChunk(1), d.sublist(1024, 2048));
    expect(() => r.readChunk(2), throwsA(isA<FourIntegrityException>()));
    // ciphertext edits are caught per chunk; tag edits are also caught by the footer
    await r.verifyFooter();
    final badTag = Uint8List.fromList(enc)..[r0.preamble.offsetOf(1) + 1024 + 3] ^= 1;
    final r2 = await FourReader.open(BytesSource(badTag), res(mk));
    expect(() => r2.verifyFooter(), throwsA(isA<FourIntegrityException>()));
  });

  test('tampered preamble / header is detected', () async {
    final enc = await FourWriter.encryptBytes(data(3000), meta: meta(), masterKey: mk, batch: batch, chunkSize: 1024);
    final r0 = await FourReader.open(BytesSource(enc), res(mk));
    // flip a flag bit (preamble is header AAD)
    final a = Uint8List.fromList(enc)..[6] ^= 2; // mkVersion
    expect(() => FourReader.open(BytesSource(a), res(mk)), throwsA(isA<FourIntegrityException>()));
    // flip a header byte
    final b = Uint8List.fromList(enc)..[r0.preamble.encodedLength + 20] ^= 1;
    expect(() => FourReader.open(BytesSource(b), res(mk)), throwsA(isA<FourIntegrityException>()));
  });

  test('swapped chunks are detected', () async {
    final enc = await FourWriter.encryptBytes(data(4096), meta: meta(), masterKey: mk, batch: batch, chunkSize: 1024);
    final p = (await FourReader.open(BytesSource(enc), res(mk))).preamble;
    final s = p.chunkStride;
    final sw = Uint8List.fromList(enc);
    sw.setRange(p.offsetOf(0), p.offsetOf(0) + s, enc, p.offsetOf(1));
    sw.setRange(p.offsetOf(1), p.offsetOf(1) + s, enc, p.offsetOf(0));
    final r = await FourReader.open(BytesSource(sw), res(mk));
    expect(() => r.readChunk(0), throwsA(isA<FourIntegrityException>()));
  });

  test('truncation and trailing bytes are rejected', () async {
    final enc = await FourWriter.encryptBytes(data(3000), meta: meta(), masterKey: mk, batch: batch, chunkSize: 1024);
    for (final cut in [1, 36, 500, enc.length - 30]) {
      expect(() => FourReader.peek(BytesSource(Uint8List.sublistView(enc, 0, enc.length - cut))), throwsA(isA<FourFormatException>()), reason: 'cut $cut');
    }
    expect(() => FourReader.peek(BytesSource(Uint8List.fromList([...enc, 0]))), throwsA(isA<FourIntegrityException>()));
  });

  test('not a 4 file', () async {
    expect(() => FourReader.peek(BytesSource(Uint8List.fromList('%PDF-1.7 hello'.codeUnits))), throwsA(isA<FourFormatException>()));
  });

  test('file round trip via encryptFile', () async {
    final dir = await Directory.systemTemp.createTemp('four');
    final d = data(300000);
    final inF = File('${dir.path}/a.pdf')..writeAsBytesSync(d);
    await FourWriter.encryptFile(inF.path, '${dir.path}/a.4pdf', meta: meta(), masterKey: mk, batch: batch);
    final src = await FileSource.open('${dir.path}/a.4pdf');
    final r = await FourReader.open(src, res(mk), verify: true);
    expect(await r.readRange(262140, 10), d.sublist(262140, 262150));
    expect(await r.readAll(), d);
    await r.close();
    await dir.delete(recursive: true);
  });
}

class _Counting extends FourSource {
  _Counting(this.inner);
  final FourSource inner;
  int reads = 0;
  @override
  int get length => inner.length;
  @override
  Future<Uint8List> read(int offset, int len) {
    reads++;
    return inner.read(offset, len);
  }
}
