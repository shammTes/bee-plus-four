// Real-disk self-test of "Encrypt folder": nested source tree on disk -> "<name>_encrypted" mirror with the same
// subfolder names, each file decrypting back to the original; one unreadable file fails without aborting the run.
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:four_encryptor/src/core.dart';
import 'package:four_encryptor/src/folder.dart';
import 'package:four_encryptor/src/master_key.dart';
import 'package:four_format/four_format.dart';

class _FileSink implements FolderSink {
  _FileSink(this.file) : _s = file.openWrite();
  final File file;
  final IOSink _s;
  @override
  String get name => file.uri.pathSegments.last;
  @override
  Future<void> add(List<int> b) async => _s.add(b);
  @override
  Future<void> close({required bool ok}) async {
    await _s.close();
    if (!ok && file.existsSync()) file.deleteSync();
  }
}

void main() {
  test('nested folder on disk -> mirrored encrypted folder, round-trips, per-file errors reported', () async {
    final tmp = Directory.systemTemp.createTempSync('fourfolder');
    final src = Directory('${tmp.path}/Grade 9 Biology')..createSync();
    final files = <String, List<int>>{
      'intro.pdf': List.generate(70000, (i) => i * 7 & 0xff),
      'Unit 1/cells.pdf': List.generate(1234, (i) => i & 0xff),
      'Unit 1/Lesson A/video.mp4': List.generate(900000, (i) => i * 3 & 0xff),
      'Unit 2/deep/deeper/notes.pdf': List.generate(10, (i) => i),
      'Unit 2/broken.pdf': [1, 2, 3],
    };
    files.forEach((p, b) => (File('${src.path}/$p')..createSync(recursive: true)).writeAsBytesSync(b));
    final entries = [
      for (final f in src.listSync(recursive: true).whereType<File>())
        () {
          final rel = f.path.substring(src.path.length + 1);
          final i = rel.lastIndexOf('/');
          return FolderEntry(uri: f.path, name: rel.substring(i + 1), size: f.lengthSync(), mime: '', dir: i < 0 ? '' : rel.substring(0, i));
        }(),
    ];
    final out = Directory('${tmp.path}/Grade 9 Biology_encrypted');
    final mk = await MasterKey.load(KeyTarget.four);
    final res = await encryptFolder(
      entries: entries,
      open: (e) async {
        if (e.name == 'broken.pdf') throw const FileSystemException('cannot read');
        return BytesSource(Uint8List.fromList(File(e.uri).readAsBytesSync()));
      },
      create: (dir, name) async => _FileSink(File('${out.path}/${dir.isEmpty ? '' : '$dir/'}$name')..parent.createSync(recursive: true)),
      masterKey: mk,
      batch: FourBatch.create(newBatchId()),
    );
    expect(res.done, 4);
    expect(res.failed, 1);
    expect(res.failures.single, startsWith('Unit 2/broken.pdf'));
    final got = out.listSync(recursive: true).whereType<File>().map((f) => f.path.substring(out.path.length + 1)).toSet();
    expect(got, {'intro.4pdf', 'Unit 1/cells.4pdf', 'Unit 1/Lesson A/video.4vid', 'Unit 2/deep/deeper/notes.4pdf'});
    Future<List<int>?> resolver(int v) async => v == 1 ? mk : null;
    for (final p in files.keys.where((p) => !p.contains('broken'))) {
      final enc = File('${out.path}/${p.replaceAll('.pdf', '.4pdf').replaceAll('.mp4', '.4vid')}').readAsBytesSync();
      expect(enc.length, greaterThan(files[p]!.length));
      final r = await FourReader.open(BytesSource(enc), resolver, verify: true);
      expect(await r.readAll(), files[p]);
    }
    // ignore: avoid_print
    print('SELFTEST tree:\n${got.join('\n')}');
    tmp.deleteSync(recursive: true);
  });
}
