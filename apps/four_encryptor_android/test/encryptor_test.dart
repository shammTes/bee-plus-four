// The encryptor's write path (core.dart → FourWriter, through the same buffered-sink pattern as SafSink)
// must produce files that 4's decrypt code (FourReader, used by lib/resources in the app) opens.
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:four_encryptor/src/core.dart';
import 'package:four_encryptor/src/master_key.dart';
import 'package:four_format/four_format.dart';

/// Mirrors SafSink: batches small pieces into big writes, then concatenates.
class _MemSink {
  final out = BytesBuilder(copy: false);
  final _buf = BytesBuilder(copy: true);
  int writes = 0;
  Future<void> add(List<int> b) async {
    _buf.add(b);
    if (_buf.length >= 512 * 1024) flush();
  }

  void flush() {
    if (_buf.isEmpty) return;
    out.add(_buf.takeBytes());
    writes++;
  }
}

/// Counts reads so we can prove the input is streamed chunk by chunk.
class _CountingSource extends FourSource {
  _CountingSource(this.inner);
  final FourSource inner;
  int maxRead = 0, reads = 0;
  @override
  int get length => inner.length;
  @override
  Future<Uint8List> read(int offset, int len) {
    reads++;
    if (len > maxRead) maxRead = len;
    return inner.read(offset, len);
  }
}

Future<Uint8List> _encrypt(Job j, FourSource src, {Uint8List? thumb}) async {
  final sink = _MemSink();
  await encryptStream(input: src, add: sink.add, meta: j.meta(), masterKey: await MasterKey.load(), batch: FourBatch.create(newBatchId()), thumb: thumb);
  sink.flush();
  return sink.out.toBytes();
}

Uint8List _data(int n) => Uint8List.fromList(List.generate(n, (i) => (i * 131 + 17) & 0xff));

void main() {
  // the app's resolver: MK only when unlocked, mkVersion 1 (lib/resources/gate.dart)
  Future<List<int>?> appResolver(int v) async => v == 1 ? await FourKeys.devMasterKey() : null;

  test('this build uses the DEV key (no FOUR_MK), same as the current 4 builds', () async {
    expect(MasterKey.isDev, isTrue);
    expect(await MasterKey.load(), await FourKeys.devMasterKey());
  });

  test('video round trip: 1.3 MB in 256 KiB chunks, streamed, opens with 4\'s reader', () async {
    final d = _data(1300 * 1024 + 7);
    final j = Job(uri: 'x', name: 'Cell_cycle.mp4', size: d.length, mime: 'video/mp4', type: FourType.video)
      ..title = 'Cell cycle'
      ..subject = 'biology'
      ..grade = 11
      ..unit = '2'
      ..durationMs = 61000;
    final src = _CountingSource(BytesSource(d));
    final enc = await _encrypt(j, src, thumb: Uint8List.fromList([0xff, 0xd8, 1, 2]));
    expect(src.maxRead, FourFormat.defaultChunk, reason: 'never reads more than one chunk');
    final r = await FourReader.open(BytesSource(enc), appResolver, verify: true);
    expect(r.preamble.chunkSize, 256 * 1024);
    expect(r.preamble.chunkCount, 6);
    expect(r.meta.type, FourType.video);
    expect(r.meta.title, 'Cell cycle');
    expect(r.meta.subject, 'biology');
    expect(r.meta.grade, 11);
    expect(r.meta.durationMs, 61000);
    expect(r.thumbnail, [0xff, 0xd8, 1, 2]);
    expect(await r.readAll(), d);
    expect(j.outFileName, 'Cell_cycle.4vid');
  });

  test('pdf / reel / web extensions + metadata incl. licence credit', () async {
    for (final (name, mime, type, ext) in [
      ('notes.pdf', 'application/pdf', FourType.pdf, '.4pdf'),
      ('clip.mp4', 'video/mp4', FourType.reel, '.4reel'),
      ('sim.zip', 'application/zip', FourType.web, '.4web'),
    ]) {
      final d = _data(5000);
      final j = Job(uri: 'x', name: name, size: d.length, mime: mime, type: type)
        ..thirdParty = true
        ..licence = FourLicence.ccBy
        ..author = 'OpenSciEd'
        ..source = 'LabXchange'
        ..sourceUrl = 'https://www.labxchange.org/library/items/lb:LabXchange:dad95647:lx_simulation:1'
        ..entry = type == FourType.web ? 'index.html' : '';
      expect(j.refusal, isNull);
      final r = await FourReader.open(BytesSource(await _encrypt(j, BytesSource(d))), appResolver, verify: true);
      expect(j.outFileName.endsWith(ext), isTrue);
      expect(r.meta.type, type);
      expect(r.meta.licence, 'CC-BY-4.0');
      expect(r.meta.creditLine, 'OpenSciEd · LabXchange · CC-BY-4.0');
      expect(r.meta.entry, type == FourType.web ? 'index.html' : '');
      expect(await r.readAll(), d);
    }
  });

  test('wrong key (other FOUR_MK) cannot open', () async {
    final j = Job(uri: 'x', name: 'a.pdf', size: 10, mime: 'application/pdf', type: FourType.pdf);
    final enc = await _encrypt(j, BytesSource(_data(10)));
    expect(() => FourReader.open(BytesSource(enc), (_) async => FourKeys.random(32)), throwsA(isA<FourKeyException>()));
  });

  test('header layout matches the Mac/CLI sample files (and the samples open with the same key)', () async {
    final dir = Directory('/workspace/samples');
    if (!dir.existsSync()) return markTestSkipped('samples not on this machine');
    final ours = FourPreamble.decode(await _encrypt(Job(uri: 'x', name: 'a.mp4', size: 0, mime: 'video/mp4', type: FourType.video), BytesSource(_data(300000))));
    for (final f in dir.listSync().whereType<File>().where((f) => RegExp(r'\.4(vid|reel|pdf)$').hasMatch(f.path))) {
      final src = await FileSource.open(f.path);
      try {
        final p = await FourReader.peek(src);
        expect(p.version, ours.version, reason: f.path);
        expect(p.mkVersion, ours.mkVersion);
        expect(p.chunkSize, ours.chunkSize);
        expect(p.encodedLength - utf8Len(p.batchId), ours.encodedLength - utf8Len(ours.batchId));
        final r = await FourReader.open(src, appResolver);
        expect(r.meta.type, isNot(FourType.web));
        expect((await r.readChunk(0)).length, p.plainLenOf(0));
      } finally {
        await src.close();
      }
    }
  });

  test('licence gate', () {
    expect(FourLicence.parse('CC BY 4.0'), FourLicence.ccBy);
    expect(FourLicence.parse('CC BY-SA 4.0'), FourLicence.ccBySa);
    expect(FourLicence.parse('https://creativecommons.org/licenses/by-nc-sa/4.0/'), FourLicence.ccByNcSa);
    expect(FourLicence.parse('CC BY-NC 4.0'), FourLicence.ccByNc);
    expect(FourLicence.parse('Public Domain'), FourLicence.pd);
    expect(FourLicence.parse('CC0'), FourLicence.cc0);
    expect(FourLicence.parse('All rights reserved'), FourLicence.arr);
    expect(FourLicence.parse('whatever'), FourLicence.unknown);
    expect(FourLicence.ccBy.refusal(), isNull);
    expect(FourLicence.ccBySa.refusal(), isNull);
    expect(FourLicence.cc0.refusal(), isNull);
    expect(FourLicence.pd.refusal(), isNull);
    expect(FourLicence.ccByNd.refusal(), isNull);
    expect(FourLicence.ccByNd.refusal(modified: true), contains('no changes'));
    expect(FourLicence.ccByNc.refusal(), contains('non-commercial'));
    expect(FourLicence.arr.refusal(), contains('All rights reserved'));
    expect(FourLicence.lx1.refusal(), contains('LabXchange Standard License'));
    expect(FourLicence.unknown.refusal(), contains('unknown'));
    final j = Job(uri: 'x', name: 'a.zip', size: 1, mime: 'application/zip', type: FourType.web)..thirdParty = true;
    expect(j.refusal, isNotNull, reason: 'third-party without a licence is refused');
    j.thirdParty = false;
    expect(j.refusal, isNull, reason: 'own content needs no licence');
  });

  test('type auto-detect and bundle entry', () {
    expect(detectType('a.pdf', ''), FourType.pdf);
    expect(detectType('a.mp4', 'video/mp4'), FourType.video);
    expect(detectType('a.mp4', 'video/mp4', portrait: true), FourType.reel);
    expect(detectType('a.zip', 'application/zip'), FourType.web);
    expect(detectType('a.txt', 'text/plain'), isNull);
    expect(bundleEntry(['index.html', 'a/index.html']), 'index.html');
    expect(bundleEntry(['site/a/index.html', 'site/index.html', 'x.png']), 'site/index.html');
    expect(bundleEntry(['__MACOSX/x.html', 'sim.html', 'img/a.png']), 'sim.html');
    expect(bundleEntry(['a.png']), isNull);
  });
}

int utf8Len(String s) => s.codeUnits.length;
