// Folder names → grade / subject / chapter, and folder mode writes them into the file header.
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:four_encryptor/src/core.dart';
import 'package:four_encryptor/src/folder.dart';
import 'package:four_encryptor/src/master_key.dart';
import 'package:four_encryptor/src/res_path.dart';
import 'package:four_format/four_format.dart';

class _Sink implements FolderSink {
  _Sink(this.name);
  @override
  final String name;
  final out = BytesBuilder(copy: true);
  @override
  Future<void> add(List<int> b) async => out.add(b);
  @override
  Future<void> close({required bool ok}) async {}
}

void main() {
  test('parseResPath', () {
    var r = parseResPath('Winner handouts_encrypted/Grade 8/Science/Chapter 01 - Living things');
    expect([r.grade, r.subject, r.unit, r.chapter], [8, 'science', '1', 'Chapter 01 - Living things']);
    expect(r.folder, 'Winner handouts/Grade 8/Science/Chapter 01 - Living things');
    r = parseResPath('Grade 7_encrypted/Maths/Unit 3 Fractions');
    expect([r.grade, r.subject, r.unit], [7, 'mathematics', '3']);
    r = parseResPath('Social Studies/Grade 6/2. Maps');
    expect([r.grade, r.subject, r.unit], [6, 'social_studies', '2']);
    r = parseResPath('random/stuff');
    expect([r.grade, r.subject, r.unit], [0, '', '']);
  });

  test('folder mode stores grade, subject, unit and folder in the header (Winner)', () async {
    final mk = await MasterKey.load(KeyTarget.bee);
    final data = Uint8List.fromList(List.generate(5000, (i) => i & 0xff));
    final e = FolderEntry(uri: 'x', name: 'Cells.pdf', size: data.length, mime: '', dir: 'Science/Chapter 02 - Cells');
    final sinks = <_Sink>[];
    await encryptFolder(
      entries: [e],
      open: (_) async => BytesSource(data),
      create: (dir, name) async => (sinks..add(_Sink(name))).last,
      masterKey: mk,
      batch: FourBatch.create(newBatchId()),
      root: 'Grade 8',
      grades: KeyTarget.bee.grades,
      subjects: KeyTarget.bee.subjects,
    );
    final r = await FourReader.open(BytesSource(sinks.single.out.toBytes()), (v) async => mk);
    expect(r.meta.grade, 8);
    expect(r.meta.subject, 'science');
    expect(r.meta.unit, '2');
    expect(r.meta.folder, 'Grade 8/Science/Chapter 02 - Cells');
  });

  test('second run skips files already in the output folder', () {
    final done = doneKeys([
      FolderEntry(uri: 'o1', name: 'clip.4reel', size: 10, mime: '', dir: 'Grade 9/Unit 1'),
      FolderEntry(uri: 'o2', name: 'empty.4vid', size: 0, mime: '', dir: 'Grade 9/Unit 1'),
    ]);
    expect(folderSkipReason(FolderEntry(uri: 'a', name: 'clip.mp4', size: 9, mime: '', dir: 'Grade 9/Unit 1'), done: done), isNotNull);
    expect(folderSkipReason(FolderEntry(uri: 'b', name: 'empty.mp4', size: 9, mime: '', dir: 'Grade 9/Unit 1'), done: done), isNull);
    expect(folderSkipReason(FolderEntry(uri: 'c', name: 'clip.mp4', size: 9, mime: '', dir: 'Grade 9/Unit 2'), done: done), isNull);
  });
}
