// Imported add-on resources: SAF folder → app-private storage → sealed local index.
import 'dart:convert';
import 'dart:io';

import 'package:cryptography/cryptography.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:four_format/four_format.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../update/updater.dart';
import '../licensing/screenshot.dart';
import 'gate.dart';

class ResEntry {
  ResEntry({required this.id, required this.path, required this.meta, this.thumb, required this.size});
  final String id, path;
  final FourMeta meta;
  final Uint8List? thumb;
  final int size;

  Map<String, Object?> toJson() => {'id': id, 'path': path, 'meta': meta.toJson(), 'size': size, if (thumb != null) 'thumb': base64.encode(thumb!)};
  factory ResEntry.fromJson(Map<String, Object?> j) => ResEntry(
    id: j['id'] as String,
    path: j['path'] as String,
    meta: FourMeta.fromJson((j['meta'] as Map).cast<String, Object?>()),
    size: (j['size'] as num).toInt(),
    thumb: j['thumb'] == null ? null : base64.decode(j['thumb'] as String),
  );

  /// `biology_11` style notes book id
  String get bookKey => '${meta.subject.toLowerCase().replaceAll(' ', '_')}_${meta.grade}';
}

class RefreshReport {
  const RefreshReport(this.added, this.skipped, this.failed, [this.error, this.problems = const []]);
  final int added, skipped, failed;
  final String? error;

  /// One line per file that could not be added: "name: plain reason".
  final List<String> problems;
}

/// Plain-language reason a resource file could not be added/opened, followed by the technical error.
String explainImportError(Object e) {
  final tech = e is PlatformException ? '${e.code}: ${e.message}' : '$e';
  final String why;
  if (e is FourKeyException && e.message.contains('not unlocked')) {
    why = '4 is not unlocked on this phone';
  } else if (e is FourKeyException && e.message == 'wrong key') {
    why = 'made with a different key: the encryptor and this 4 must both use the DEV key, or the same FOUR_MK';
  } else if (e is FourKeyException) {
    why = 'key problem';
  } else if (e is FourIntegrityException) {
    why = 'the file is damaged or was not copied completely (copy it again)';
  } else if (e is FourFormatException && e.message.startsWith('unsupported version')) {
    why = 'made by a newer encryptor; update 4';
  } else if (e is FourFormatException) {
    why = 'not a valid 4 resource file';
  } else if (e is PlatformException || e is FileSystemException) {
    why = 'could not copy it into 4 (storage full or the file is not readable)';
  } else if (e is SecretBoxAuthenticationError) {
    why = 'the file is damaged or made with a different key';
  } else {
    why = 'unexpected error';
  }
  return '$why [$tech]';
}

/// App-wide store. Lazy: nothing is read until the Resources page or a unit strip asks.
class ResourceLibrary extends ChangeNotifier {
  ResourceLibrary._();
  static final instance = ResourceLibrary._();

  static const _ch = MethodChannel('com.warsay.high/resources');
  static const _folderKey = 'four_res_folder_v1';

  List<ResEntry> entries = const [];
  GateMode mode = GateMode.locked;
  int lockedFiles = 0;
  bool loaded = false, busy = false;
  String? folder;
  Future<void>? _loading;

  ResourceGate get gate => ResourceGate.instance!;
  bool get available => ResourceGate.instance != null;

  Future<Directory> _dir() async {
    final d = Directory('${(await getApplicationSupportDirectory()).path}/resources');
    if (!await d.exists()) await d.create(recursive: true);
    return d;
  }

  Future<void> ensureLoaded() => loaded ? Future.value() : (_loading ??= _load());

  Future<void> reload() {
    gate.reset();
    _loading = _load();
    return _loading!;
  }

  Future<void> _load() async {
    if (!available) return;
    try {
      final prefs = await SharedPreferences.getInstance();
      folder = prefs.getString(_folderKey);
      mode = await gate.mode();
      final dir = await _dir();
      final files = dir.listSync().whereType<File>().where((f) => f.path.endsWith('.4res')).toList();
      if (mode == GateMode.locked) {
        entries = const [];
        lockedFiles = files.length;
      } else {
        lockedFiles = 0;
        entries = await _readIndex(dir) ?? await _rebuild(files);
        // drop entries whose file vanished; add files missing from the index
        final known = {for (final e in entries) e.path};
        final extra = files.where((f) => !known.contains(f.path)).toList();
        entries = [...entries.where((e) => File(e.path).existsSync()), ...await _rebuild(extra)];
        await _writeIndex(dir);
      }
    } catch (e) {
      debugPrint('resources load failed: $e');
    }
    loaded = true;
    notifyListeners();
  }

  Future<List<ResEntry>> _rebuild(List<File> files) async {
    final out = <ResEntry>[];
    for (final f in files) {
      final e = await _entryFor(f.path);
      if (e != null) out.add(e);
    }
    return out;
  }

  Future<ResEntry?> _entryFor(String path, {bool verify = false, bool rethrowErrors = false}) async {
    final src = await FileSource.open(path);
    try {
      final r = await FourReader.open(src, gate.masterKey, verify: verify);
      return ResEntry(id: r.id, path: path, meta: r.meta, thumb: r.thumbnail, size: r.length);
    } catch (e) {
      debugPrint('resource $path: $e');
      if (rethrowErrors) rethrow;
      return null;
    } finally {
      await src.close();
    }
  }

  // ---- sealed index (AES-GCM under the device key)
  Future<List<ResEntry>?> _readIndex(Directory dir) async {
    final f = File('${dir.path}/index.bin');
    if (!await f.exists()) return null;
    try {
      final key = await gate.deviceKey();
      if (key == null) return null;
      final box = SecretBox.fromConcatenation(await f.readAsBytes(), nonceLength: 12, macLength: 16);
      final plain = await FourKeys.aes.decrypt(box, secretKey: SecretKey(key));
      return [for (final j in jsonDecode(utf8.decode(plain)) as List) ResEntry.fromJson((j as Map).cast<String, Object?>())];
    } catch (_) {
      return null; // key changed (e.g. fresh unlock) → rebuilt from the files
    }
  }

  Future<void> _writeIndex(Directory dir) async {
    final key = await gate.deviceKey();
    if (key == null) return;
    final plain = utf8.encode(jsonEncode([for (final e in entries) e.toJson()]));
    final box = await FourKeys.aes.encrypt(plain, secretKey: SecretKey(key), nonce: FourKeys.random(12));
    final f = File('${dir.path}/index.bin.part');
    await f.writeAsBytes(box.concatenation(), flush: true);
    await f.rename('${dir.path}/index.bin');
  }

  // ---- folder + import
  Future<String?> pickFolder() async {
    final uri = await _ch.invokeMethod<String>('pickFolder');
    if (uri != null) {
      folder = uri;
      (await SharedPreferences.getInstance()).setString(_folderKey, uri);
      notifyListeners();
    }
    return uri;
  }

  Future<RefreshReport> refresh() async {
    if (busy) return const RefreshReport(0, 0, 0, 'Already refreshing');
    await ensureLoaded();
    var f = folder;
    if (f == null || !(await _ch.invokeMethod<bool>('hasFolder', {'uri': f}) ?? false)) {
      f = await pickFolder();
      if (f == null) return const RefreshReport(0, 0, 0, 'No folder chosen');
    }
    busy = true;
    notifyListeners();
    var added = 0, skipped = 0, failed = 0;
    final problems = <String>[];
    try {
      final dir = await _dir();
      final list = await _ch.invokeListMethod<Map<Object?, Object?>>('listFolder', {'uri': f}) ?? const [];
      final have = {for (final x in dir.listSync().whereType<File>()) x.uri.pathSegments.last.split('.').first};
      for (final item in list) {
        final head = item['head'] as Uint8List;
        if (!FourFormat.hasMagic(head) || head.length < 24) continue;
        final id = head.sublist(8, 24).map((b) => b.toRadixString(16).padLeft(2, '0')).join();
        if (have.contains(id)) {
          skipped++;
          continue;
        }
        final tmp = '${dir.path}/$id.part';
        try {
          await _ch.invokeMethod<int>('importFile', {'uri': item['uri'], 'dest': tmp});
          final src = await FileSource.open(tmp);
          try {
            final p = await FourReader.peek(src); // length/structure check
            if (p.fileIdHex != id) throw const FourFormatException('id mismatch');
          } finally {
            await src.close();
          }
          final dest = '${dir.path}/$id.4res';
          if (mode != GateMode.locked) {
            final e = (await _entryFor(tmp, verify: true, rethrowErrors: true))!;
            await File(tmp).rename(dest);
            entries = [...entries, ResEntry(id: e.id, path: dest, meta: e.meta, thumb: e.thumb, size: e.size)];
          } else {
            await File(tmp).rename(dest);
            lockedFiles++;
          }
          have.add(id);
          added++;
        } catch (e) {
          debugPrint('import ${item['name']}: $e');
          problems.add('${item['name']}: ${explainImportError(e)}');
          final t = File(tmp);
          if (await t.exists()) await t.delete();
          failed++;
        }
      }
      if (mode != GateMode.locked) await _writeIndex(dir);
      // offline update: a newer 4 APK shared into the same folder
      await Updater.instance.scanFolder(f);
    } on PlatformException catch (e) {
      return RefreshReport(added, skipped, failed, e.message, problems);
    } finally {
      busy = false;
      notifyListeners();
    }
    return RefreshReport(added, skipped, failed, null, problems);
  }

  Future<void> remove(ResEntry e) async {
    final f = File(e.path);
    if (await f.exists()) await f.delete();
    entries = entries.where((x) => x.id != e.id).toList();
    await _writeIndex(await _dir());
    notifyListeners();
  }

  /// Resources for a notes unit page (`bookId` like `biology_11`).
  List<ResEntry> forUnit(String bookId, int unitNumber, String unitId) => [
    for (final e in entries)
      if (e.bookKey == bookId && (e.meta.unit == '$unitNumber' || e.meta.unit == unitId)) e,
  ];

  /// Resource viewers (video / PDF / reels) hold the screenshot block while open. Reference counted with the
  /// Notes / Matric sections ([ScreenshotGuard]) so closing a video never clears the block a notes page needs.
  static Future<void> setSecure(bool on) async {
    on ? ScreenshotGuard.acquire('resources') : ScreenshotGuard.release('resources');
  }
}
