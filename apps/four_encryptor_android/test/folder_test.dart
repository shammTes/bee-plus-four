// "Encrypt folder" must produce files that decrypt exactly like single-file mode (same writer, key, meta),
// keep subfolders, skip already-encrypted / unsupported files and stop on Cancel.
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:four_encryptor/src/core.dart';
import 'package:four_encryptor/src/folder.dart';
import 'package:four_encryptor/src/master_key.dart';
import 'package:four_format/four_format.dart';

class _MemSink implements FolderSink {
  _MemSink(this.name);
  @override
  final String name;
  final out = BytesBuilder(copy: true);
  bool? closedOk;
  @override
  Future<void> add(List<int> b) async => out.add(b);
  @override
  Future<void> close({required bool ok}) async => closedOk = ok;
}

Uint8List _data(int n, int seed) => Uint8List.fromList(List.generate(n, (i) => (i * 131 + seed) & 0xff));

void main() {
  for (final t in KeyTarget.values) {
    test('folder-encrypted file decrypts identically to single-file mode (${t.label})', () async {
      final mk = await MasterKey.load(t);
      final files = {
        'a.pdf': _data(300 * 1024 + 3, 1),
        'Unit 1/Cell_cycle.mp4': _data(1300 * 1024 + 7, 2),
        'Unit 1/deep/clip.mp4': _data(5000, 3),
        'Unit 1/old.4vid': _data(100, 4),
        'notes.txt': _data(10, 5),
        'page.zip': _data(10, 6),
      };
      FolderEntry entry(String p) {
        final i = p.lastIndexOf('/');
        return FolderEntry(uri: p, name: p.substring(i + 1), size: files[p]!.length, mime: '', dir: i < 0 ? '' : p.substring(0, i));
      }

      final probes = {'Unit 1/deep/clip.mp4': {'portrait': true, 'durationMs': 9000}};
      final sinks = <String, _MemSink>{};
      final res = await encryptFolder(
        entries: [for (final p in files.keys) entry(p)],
        open: (e) async => BytesSource(files[e.path]!),
        create: (dir, name) async => sinks[dir.isEmpty ? name : '$dir/$name'] = _MemSink(name),
        probe: (e) async => probes[e.path] ?? const {},
        masterKey: mk,
        batch: FourBatch.create(newBatchId()),
      );
      expect(res.done, 3);
      expect(res.skipped, 3);
      expect(res.failed, 0);
      expect(sinks.keys.toSet(), {'a.4pdf', 'Unit 1/Cell_cycle.4vid', 'Unit 1/deep/clip.4reel'});

      Future<List<int>?> resolver(int v) async => v == 1 ? mk : null;
      for (final p in ['a.pdf', 'Unit 1/Cell_cycle.mp4', 'Unit 1/deep/clip.mp4']) {
        final e = entry(p);
        final folderBytes = sinks.entries.firstWhere((s) => s.key.startsWith(e.dir) && s.value.name.startsWith(e.name.split('.').first)).value.out.toBytes();
        // single-file mode: same Job the Add files flow builds
        final j = folderJob(e, probe: probes[p] ?? const {});
        final single = BytesBuilder();
        await encryptStream(input: BytesSource(files[p]!), add: single.add, meta: j.meta(), masterKey: mk, batch: FourBatch.create(newBatchId()));
        final a = await FourReader.open(BytesSource(folderBytes), resolver, verify: true);
        final b = await FourReader.open(BytesSource(single.toBytes()), resolver, verify: true);
        expect(await a.readAll(), files[p]);
        expect(await a.readAll(), await b.readAll());
        expect(a.meta.toString(), b.meta.toString());
        expect(a.meta.type, b.meta.type);
        expect(a.meta.title, b.meta.title);
        expect(a.meta.mime, b.meta.mime);
        expect(a.meta.durationMs, b.meta.durationMs);
        expect(a.preamble.chunkSize, b.preamble.chunkSize);
      }
    });
  }

  test('cancel stops mid-way and drops the half-written file', () async {
    var reads = 0;
    final sinks = <_MemSink>[];
    final res = await encryptFolder(
      entries: [FolderEntry(uri: 'v', name: 'big.mp4', size: 2 * 1024 * 1024, mime: 'video/mp4'), FolderEntry(uri: 'w', name: 'next.pdf', size: 10, mime: '')],
      open: (e) async => _Counting(BytesSource(_data(e.size, 1)), () => reads++),
      create: (_, n) async => (sinks..add(_MemSink(n))).last,
      masterKey: await MasterKey.load(),
      batch: FourBatch.create(newBatchId()),
      cancelled: () => reads >= 2,
    );
    expect(res.cancelled, isTrue);
    expect(res.done, 0);
    expect(sinks.single.closedOk, isFalse);
  });
}

class _Counting extends FourSource {
  _Counting(this.inner, this.onRead);
  final FourSource inner;
  final void Function() onRead;
  @override
  int get length => inner.length;
  @override
  Future<Uint8List> read(int o, int l) {
    onRead();
    return inner.read(o, l);
  }
}
