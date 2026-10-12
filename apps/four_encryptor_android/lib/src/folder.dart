// "Encrypt folder": walk a picked folder, encrypt every PDF / video with the same code path as single files
// (Job.meta() + encryptStream), mirror the subfolders into the output folder. No Flutter imports: unit-tested on a PC.
import 'dart:async';
import 'dart:typed_data';

import 'package:four_format/four_format.dart';

import 'core.dart';

/// One file found in the picked folder. [dir] is the subfolder path relative to the picked folder ('' = top).
class FolderEntry {
  FolderEntry({required this.uri, required this.name, required this.size, required this.mime, this.dir = ''});
  final String uri, name, mime, dir;
  final int size;
  String get path => dir.isEmpty ? name : '$dir/$name';
}

/// Extensions written by this app (and by the Mac / CLI tools).
const fourExtensions = ['.4pdf', '.4vid', '.4reel', '.4web'];

bool isEncryptedName(String name) {
  final l = name.toLowerCase();
  return fourExtensions.any(l.endsWith);
}

/// Why a file is skipped in folder mode, or null if it will be encrypted.
/// Web pages (.zip) are skipped: they need a licence and a start page, so add them one by one.
String? folderSkipReason(FolderEntry e) {
  if (isEncryptedName(e.name)) return 'already encrypted';
  if (e.name.startsWith('.')) return 'hidden file';
  final mime = e.mime.isEmpty ? guessMime(e.name) : e.mime;
  final t = detectType(e.name, mime);
  if (t == null) return 'not a PDF or video';
  if (t == FourType.web) return 'web page: add it with "Add files"';
  return null;
}

/// Same job single-file mode builds after picking + probing (title from file name, auto reel for portrait video).
Job folderJob(FolderEntry e, {Map<Object?, Object?> probe = const {}}) {
  final mime = e.mime.isEmpty ? guessMime(e.name) : e.mime;
  final portrait = probe['portrait'] == true;
  final j = Job(uri: e.uri, name: e.name, size: e.size, mime: mime, type: detectType(e.name, mime, portrait: portrait)!)
    ..title = titleFromName(e.name)
    ..portrait = portrait
    ..durationMs = (probe['durationMs'] as num?)?.toInt()
    ..pages = (probe['pages'] as num?)?.toInt();
  final t = probe['thumb'];
  if (t is Uint8List) j.thumb = t;
  return j;
}

String titleFromName(String name) {
  final i = name.lastIndexOf('.');
  return (i > 0 ? name.substring(0, i) : name).replaceAll(RegExp(r'[_-]+'), ' ').trim();
}

/// Output document writer (SafSink on the phone, memory in tests).
abstract class FolderSink {
  Future<void> add(List<int> b);
  Future<void> close({required bool ok});
  String get name;
}

class FolderResult {
  int done = 0, skipped = 0, failed = 0;
  bool cancelled = false;
  final failures = <String>[]; // "path: reason"
  final skips = <String>[];
}

class FolderProgress {
  FolderProgress(this.index, this.total, this.current, this.fileProgress);
  final int index, total; // 1-based file number of [total] files to encrypt
  final String current;
  final double fileProgress;
}

/// Encrypts [entries] one at a time (only one file open at once; input streamed chunk by chunk, so memory stays
/// flat even for 2 GB videos). Already-encrypted / unsupported files are counted as skipped.
Future<FolderResult> encryptFolder({
  required List<FolderEntry> entries,
  required Future<FourSource> Function(FolderEntry e) open,
  required Future<FolderSink> Function(String dir, String fileName) create,
  required List<int> masterKey,
  required FourBatch batch,
  Future<Map<Object?, Object?>> Function(FolderEntry e)? probe,
  void Function(FolderProgress p)? onProgress,
  void Function(String line)? log,
  bool Function()? cancelled,
}) async {
  final res = FolderResult();
  final todo = <FolderEntry>[];
  for (final e in entries) {
    final why = folderSkipReason(e);
    if (why == null) {
      todo.add(e);
    } else {
      res.skipped++;
      res.skips.add('${e.path}: $why');
    }
  }
  for (var i = 0; i < todo.length; i++) {
    if (cancelled?.call() == true) {
      res.cancelled = true;
      break;
    }
    final e = todo[i];
    onProgress?.call(FolderProgress(i + 1, todo.length, e.path, 0));
    FourSource? src;
    FolderSink? out;
    var ok = false;
    try {
      Map<Object?, Object?> p = const {};
      if (probe != null) {
        try {
          p = await probe(e);
        } catch (err) {
          log?.call('probe ${e.path} failed (not fatal): $err');
        }
      }
      final j = folderJob(e, probe: p);
      src = await open(e);
      out = await create(e.dir, j.outFileName);
      var last = DateTime.now();
      await encryptStream(
        input: _CancelSource(src, cancelled),
        add: out.add,
        meta: j.meta(),
        masterKey: masterKey,
        batch: batch,
        thumb: j.thumb,
        onProgress: (d, t) {
          final now = DateTime.now();
          if (now.difference(last).inMilliseconds < 150 && d < t) return;
          last = now;
          onProgress?.call(FolderProgress(i + 1, todo.length, e.path, t == 0 ? 1 : d / t));
        },
      );
      ok = true;
      await out.close(ok: true);
      res.done++;
      log?.call('folder: ${e.path} → ${out.name}');
    } on _Cancelled {
      res.cancelled = true;
    } catch (err) {
      res.failed++;
      res.failures.add('${e.path}: $err');
      log?.call('folder: FAILED ${e.path}: $err');
    } finally {
      if (out != null && !ok) {
        try {
          await out.close(ok: false); // deletes the half-written file
        } catch (_) {}
      }
      try {
        await src?.close();
      } catch (_) {}
    }
    if (res.cancelled) break;
  }
  return res;
}

class _Cancelled implements Exception {}

/// Stops a big video mid-way when Cancel is tapped (checked before every chunk).
class _CancelSource extends FourSource {
  _CancelSource(this.inner, this.cancelled);
  final FourSource inner;
  final bool Function()? cancelled;
  @override
  int get length => inner.length;
  @override
  Future<Uint8List> read(int offset, int len) {
    if (cancelled?.call() == true) throw _Cancelled();
    return inner.read(offset, len);
  }
}
