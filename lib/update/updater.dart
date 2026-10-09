// App updates for 4, from a FILE only — never over Wi-Fi / mobile data. A newer 4 APK arrives by SHAREit,
// Bluetooth, Nearby Share or cable; 4 finds it by itself (start / resume, in the resources folder and an optional
// "update folder"), or the user picks it once with "Find update file". Each candidate must be 4 (same package), a
// higher versionCode and signed with the same certificate; then the system installer opens (one tap — Android never
// allows a silent install for sideloaded apps). Same applicationId + same signing key ⇒ Android keeps all app data.
import 'dart:async';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocalApk {
  const LocalApk(this.path, this.versionCode, this.versionName, {this.from = ''});
  final String path, versionName;
  final int versionCode;

  /// where it was found ("your resources folder", "the file you picked", …), for the card
  final String from;
}

class Updater extends ChangeNotifier {
  Updater._();
  static final instance = Updater._();

  static const _ch = MethodChannel('com.warsay.high/update');
  static const _resCh = MethodChannel('com.warsay.high/resources');

  /// same key as ResourceLibrary's chosen folder (lib/resources/library.dart)
  static const resFolderKey = 'four_res_folder_v1';
  static const updateFolderKey = 'four_update_folder_v1';
  static const _skipKey = 'four_update_skip_v1', _noteKey = 'four_update_note_v1';

  /// start/resume scans closer together than this are skipped (cheap on low-end phones)
  static const debounce = Duration(seconds: 45);

  Map<Object?, Object?> info = const {};
  LocalApk? local;
  bool scanning = false, sharing = false;

  /// last notable outcome of a scan / pick (e.g. "found 4 1.2 but signed with a different key"), or null
  String? message;
  String? updateFolder;
  DateTime? lastScan;
  bool _pendingInstall = false;
  Future<bool>? _scan;

  /// tests only
  @visibleForTesting
  Directory? dirOverride;
  @visibleForTesting
  DateTime Function() now = DateTime.now;

  int get currentCode => (info['versionCode'] as num?)?.toInt() ?? 0;
  String get currentName => info['versionName'] as String? ?? '?';
  String? get cert => info['cert'] as String?;
  bool get hasUpdate => local != null;

  @visibleForTesting
  void resetForTest() {
    info = const {};
    local = null;
    message = null;
    updateFolder = null;
    lastScan = null;
    scanning = false;
    _pendingInstall = false;
    _scan = null;
  }

  Future<void> _info() async {
    try {
      info = await _ch.invokeMethod<Map<Object?, Object?>>('info') ?? const {};
    } catch (_) {
      info = const {};
    }
  }

  Future<Directory> _dir() async {
    if (dirOverride != null) return dirOverride!;
    final d = Directory('${(await getTemporaryDirectory()).path}/updates'); // = cacheDir/updates (FileProvider path)
    if (!await d.exists()) await d.create(recursive: true);
    return d;
  }

  /// App start / resume (unlocked phones). Debounced; all file work runs on Android's background thread.
  Future<bool> autoScan({bool force = false}) async {
    if (_scan != null) return _scan!;
    final t = now();
    if (!force && lastScan != null && t.difference(lastScan!) < debounce) return local != null;
    lastScan = t;
    _scan = _autoScan().whenComplete(() => _scan = null);
    return _scan!;
  }

  Future<bool> _autoScan() async {
    await _info();
    if (info.isEmpty) return false;
    final prefs = await SharedPreferences.getInstance();
    updateFolder = prefs.getString(updateFolderKey);
    // came back from "Install unknown apps → allow": continue the install the user asked for
    if (_pendingInstall && info['canInstall'] == true && local != null) {
      _pendingInstall = false;
      unawaited(install());
    }
    // the installed version caught up (update done), or Android cleared the cache: forget the candidate
    if (local != null && (local!.versionCode <= currentCode || !File(local!.path).existsSync())) local = null;
    message ??= prefs.getString(_noteKey);
    await _cleanup();
    final trees = <String>[];
    for (final k in [resFolderKey, updateFolderKey]) {
      final u = prefs.getString(k);
      if (u != null && !trees.contains(u) && await _hasFolder(u)) trees.add(u);
    }
    if (trees.isEmpty) {
      notifyListeners();
      return local != null;
    }
    return _scanTrees(trees);
  }

  Future<bool> _hasFolder(String uri) async {
    try {
      return await _resCh.invokeMethod<bool>('hasFolder', {'uri': uri}) ?? false;
    } catch (_) {
      return false;
    }
  }

  /// Resources → Refresh also looks for an update in the chosen folder (kept for lib/resources/library.dart).
  Future<bool> scanFolder(String treeUri) async {
    if (info.isEmpty) await _info();
    if (info.isEmpty) return false;
    return _scanTrees([treeUri]);
  }

  /// Lists APKs (manifest-only check on the Android side), then copies + fully verifies the newest candidate.
  /// Files already judged "not a newer 4" are remembered by uri|size|modified and not opened again.
  Future<bool> _scanTrees(List<String> trees) async {
    scanning = true;
    notifyListeners();
    try {
      final prefs = await SharedPreferences.getInstance();
      final skip = prefs.getStringList(_skipKey) ?? <String>[];
      final above = local != null && local!.versionCode > currentCode ? local!.versionCode : currentCode;
      final list = await _ch.invokeListMethod<Map<Object?, Object?>>('findApks', {'trees': trees, 'package': info['package'], 'above': above, 'skip': skip}) ?? const [];
      final newSkip = {...skip};
      final cands = <Map<Object?, Object?>>[];
      for (final f in list) {
        if (f['other'] == true) {
          newSkip.add('${f['key']}');
        } else {
          cands.add(f);
        }
      }
      cands.sort((a, b) => (b['versionCode'] as num).compareTo(a['versionCode'] as num));
      for (final f in cands) {
        final uri = '${f['uri']}', uf = updateFolder;
        final from = uf != null && uri.startsWith(uf) ? 'your update folder' : 'your resources folder';
        final r = await _takeFrom(uri, from: from, code: (f['versionCode'] as num).toInt(), size: (f['size'] as num?)?.toInt() ?? -1);
        if (r == null) break; // found
        newSkip.add('${f['key']}'); // wrong key / damaged: do not copy it again on every start
      }
      // keep the list small: newest 200 entries
      final keep = newSkip.toList();
      await prefs.setStringList(_skipKey, keep.length > 200 ? keep.sublist(keep.length - 200) : keep);
    } catch (e) {
      debugPrint('update scan: $e');
    } finally {
      scanning = false;
      notifyListeners();
    }
    return local != null;
  }

  /// Copies a content uri into cacheDir/updates and verifies it. Returns null when it became [local], else why not.
  /// A copy of the same version and size left from an earlier start is re-checked instead of copied again.
  Future<String?> _takeFrom(String uri, {required String from, int? code, int size = -1}) async {
    final dir = await _dir();
    if (code != null && size > 0) {
      final have = File('${dir.path}/four-$code.apk');
      if (have.existsSync() && have.lengthSync() == size) return _accept(have, from: from);
    }
    final tmp = File('${dir.path}/incoming.apk');
    try {
      await _resCh.invokeMethod<int>('importFile', {'uri': uri, 'dest': tmp.path});
      return await _accept(tmp, from: from);
    } catch (e) {
      debugPrint('update copy $uri: $e');
      if (tmp.existsSync()) tmp.deleteSync();
      return 'Could not read that file.';
    }
  }

  /// Verifies [f]; on success renames it to four-<code>.apk and makes it [local].
  Future<String?> _accept(File f, {required String from}) async {
    final a = await _ch.invokeMethod<Map<Object?, Object?>>('inspectApk', {'path': f.path});
    final err = verdict(a, info);
    if (err != null) {
      if (a != null && a['package'] == info['package'] && err.contains('different key')) {
        message = 'Found 4 ${a['versionName']}, but it is signed with a different key, so it cannot update this 4.';
        unawaited(SharedPreferences.getInstance().then((p) => p.setString(_noteKey, message!)));
      }
      if (f.existsSync()) f.deleteSync();
      return err;
    }
    final code = (a!['versionCode'] as num).toInt();
    final dest = '${f.parent.path}/four-$code.apk';
    if (f.path != dest) await f.rename(dest);
    local = LocalApk(dest, code, '${a['versionName']}', from: from);
    message = null;
    unawaited(SharedPreferences.getInstance().then((p) => p.remove(_noteKey)));
    return null;
  }

  /// The gate every update file passes. Null = install it; else the reason shown to the user.
  static String? verdict(Map<Object?, Object?>? apk, Map<Object?, Object?> installed) {
    if (apk == null) return 'Not a valid APK.';
    if (apk['package'] != installed['package']) return 'This APK is not 4.';
    final code = (apk['versionCode'] as num?)?.toInt() ?? 0;
    if (code <= ((installed['versionCode'] as num?)?.toInt() ?? 0)) return 'This APK is not newer than the installed 4.';
    final c = apk['cert'] as String?;
    if (c == null || installed['cert'] == null || c != installed['cert']) return 'This APK is signed with a different key; installing it would fail.';
    return null;
  }

  /// One tap "Find update file": SAF file picker (starts in Download). Returns a message for a toast.
  Future<String> pickFile() async {
    if (info.isEmpty) await _info();
    final uri = await _ch.invokeMethod<String>('pickApk');
    if (uri == null) return '';
    scanning = true;
    notifyListeners();
    final err = await _takeFrom(uri, from: 'the file you picked');
    scanning = false;
    notifyListeners();
    return err ?? 'Found 4 ${local!.versionName} — tap Install.';
  }

  /// Optional folder 4 watches for update files (e.g. SHAREit/apps). SAF tree, persisted read permission.
  Future<bool> pickUpdateFolder() async {
    final uri = await _resCh.invokeMethod<String>('pickFolder');
    if (uri == null) return false;
    // pickFolder on the resources channel only stores the permission; keep our own pref
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(updateFolderKey, uri);
    updateFolder = uri;
    notifyListeners();
    return autoScan(force: true);
  }

  Future<void> forgetUpdateFolder() async {
    (await SharedPreferences.getInstance()).remove(updateFolderKey);
    updateFolder = null;
    notifyListeners();
  }

  Future<String> install([String? path]) async {
    final p = path ?? local?.path;
    if (p == null) return 'none';
    final r = await _ch.invokeMethod<String>('install', {'path': p}) ?? 'started';
    if (r == 'permission') {
      _pendingInstall = true;
      message = 'Allow "Install unknown apps" for 4, then come back — the install continues.';
      lastScan = null; // the resume after Settings must not be debounced
    }
    notifyListeners();
    return r;
  }

  /// "Send 4 to a friend": the installed APK through the share sheet (SHAREit, Bluetooth, Nearby Share…).
  Future<String> shareSelf() async {
    if (sharing) return '';
    sharing = true;
    notifyListeners();
    try {
      final r = await _ch.invokeMethod<Map<Object?, Object?>>('shareSelf') ?? const {};
      final splits = (r['splits'] as num?)?.toInt() ?? 0;
      return splits > 0 ? 'This 4 was installed in ${splits + 1} parts; friends need all files and a split-APK installer. A universal APK from the build is easier.' : '';
    } catch (e) {
      debugPrint('share 4: $e');
      return 'Could not prepare 4 for sharing.';
    } finally {
      sharing = false;
      notifyListeners();
    }
  }

  /// Old copies: finished updates (four-<code>.apk not newer than the installed 4), half copies, PR #40 leftovers.
  Future<void> _cleanup() async {
    try {
      final dir = await _dir();
      for (final f in dir.listSync().whereType<File>()) {
        final m = RegExp(r'four-(\d+)\.apk$').firstMatch(f.path);
        if (m == null || int.parse(m.group(1)!) <= currentCode) f.deleteSync();
      }
    } catch (_) {}
  }
}
