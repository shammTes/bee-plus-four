// In-app updates for 4. Online: a small JSON manifest (GitHub Releases "latest") → resumable APK download →
// SHA-256 + package + signing-certificate checks → system installer (one tap; Android never allows a silent
// install for sideloaded apps). Offline: a newer 4 APK shared via SHAREit/cable into the resources folder.
// Same applicationId + same signing key ⇒ Android keeps all app data (unlock, progress, imported resources).
import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

class UpdateManifest {
  const UpdateManifest({required this.versionCode, required this.versionName, required this.apk, required this.sha256, required this.size, this.cert, this.notes = ''});
  final int versionCode, size;
  final String versionName, apk, sha256, notes;
  final String? cert;

  /// [abis]: this phone's ABIs, best first. A manifest may list per-ABI APKs (`flutter build apk --split-per-abi`,
  /// ~3× smaller downloads) under "abis"; the universal "apk" is the fallback.
  factory UpdateManifest.fromJson(Map<String, Object?> j, [List<String> abis = const []]) {
    var pick = j;
    final per = (j['abis'] as Map?)?.cast<String, Object?>();
    if (per != null) {
      for (final a in abis) {
        if (per[a] is Map) {
          pick = (per[a] as Map).cast<String, Object?>();
          break;
        }
      }
    }
    return UpdateManifest(
      versionCode: (j['versionCode'] as num).toInt(),
      versionName: '${j['versionName']}',
      apk: pick['apk'] as String,
      sha256: (pick['sha256'] as String).toLowerCase(),
      size: (pick['size'] as num?)?.toInt() ?? 0,
    cert: (j['cert'] as String?)?.toLowerCase().replaceAll(':', ''),
      notes: j['notes'] as String? ?? '',
    );
  }
}

class LocalApk {
  const LocalApk(this.path, this.versionCode, this.versionName);
  final String path, versionName;
  final int versionCode;
}

enum UpdateStep { idle, checking, downloading, verifying, ready, failed }

class Updater extends ChangeNotifier {
  Updater._();
  static final instance = Updater._();

  static const manifestUrl = String.fromEnvironment('FOUR_UPDATE_URL', defaultValue: 'https://github.com/shammTes/bee-plus-four/releases/latest/download/four-update.json');
  static const _ch = MethodChannel('com.warsay.high/update');
  static const _lastKey = 'four_update_last_check', _wifiKey = 'four_update_wifi_only';
  static const _resCh = MethodChannel('com.warsay.high/resources');

  Map<Object?, Object?> info = const {};
  UpdateManifest? available;
  LocalApk? local;
  UpdateStep step = UpdateStep.idle;
  double progress = 0;
  String? message, readyPath;
  bool wifiOnly = true;

  /// tests only
  @visibleForTesting
  Directory? dirOverride;
  @visibleForTesting
  String? urlOverride;

  int get currentCode => (info['versionCode'] as num?)?.toInt() ?? 0;
  String get currentName => info['versionName'] as String? ?? '?';
  String? get cert => info['cert'] as String?;
  bool get hasUpdate => available != null || local != null;

  Future<void> _info() async {
    try {
      info = await _ch.invokeMethod<Map<Object?, Object?>>('info') ?? const {};
    } catch (_) {
      info = const {};
    }
  }

  /// Called once after start (unlocked phones). At most once a day; respects "Wi-Fi only".
  Future<void> autoCheck() async {
    final prefs = await SharedPreferences.getInstance();
    wifiOnly = prefs.getBool(_wifiKey) ?? true;
    await _info();
    if (info.isEmpty) return;
    final last = prefs.getInt(_lastKey) ?? 0;
    if (DateTime.now().millisecondsSinceEpoch - last < const Duration(hours: 20).inMilliseconds) return;
    final net = info['network'];
    if (net == 'none' || (wifiOnly && net != 'wifi')) return;
    await check();
  }

  Future<void> setWifiOnly(bool v) async {
    wifiOnly = v;
    (await SharedPreferences.getInstance()).setBool(_wifiKey, v);
    notifyListeners();
  }

  Future<UpdateManifest?> check() async {
    step = UpdateStep.checking;
    message = null;
    notifyListeners();
    try {
      if (info.isEmpty) await _info();
      final c = HttpClient()..connectionTimeout = const Duration(seconds: 12);
      final req = await c.getUrl(Uri.parse(urlOverride ?? manifestUrl));
      final res = await req.close().timeout(const Duration(seconds: 20));
      if (res.statusCode != 200) throw HttpException('manifest HTTP ${res.statusCode}');
      final m = UpdateManifest.fromJson((jsonDecode(await res.transform(utf8.decoder).join()) as Map).cast<String, Object?>(), [for (final a in (info['abis'] as List?) ?? const []) '$a']);
      c.close();
      (await SharedPreferences.getInstance()).setInt(_lastKey, DateTime.now().millisecondsSinceEpoch);
      available = m.versionCode > currentCode ? m : null;
      message = available == null ? '4 is up to date ($currentName)' : null;
      step = UpdateStep.idle;
    } catch (e) {
      step = UpdateStep.failed;
      message = 'Could not check for updates (offline?)';
      debugPrint('update check: $e');
    }
    notifyListeners();
    return available;
  }

  Future<Directory> _dir() async {
    if (dirOverride != null) return dirOverride!;
    final d = Directory('${(await getTemporaryDirectory()).path}/updates'); // = cacheDir/updates (FileProvider path)
    if (!await d.exists()) await d.create(recursive: true);
    return d;
  }

  /// Resumable download (HTTP Range on the .part file), then verify. Safe to call again after a drop.
  Future<void> download() async {
    final m = available;
    if (m == null || step == UpdateStep.downloading) return;
    step = UpdateStep.downloading;
    message = null;
    notifyListeners();
    final dir = await _dir();
    final part = File('${dir.path}/four-${m.versionCode}.apk.part');
    final done = File('${dir.path}/four-${m.versionCode}.apk');
    try {
      if (!await done.exists()) {
        var have = await part.exists() ? await part.length() : 0;
        final c = HttpClient()..connectionTimeout = const Duration(seconds: 15);
        final req = await c.getUrl(Uri.parse(m.apk));
        if (have > 0) req.headers.set(HttpHeaders.rangeHeader, 'bytes=$have-');
        final res = await req.close();
        if (res.statusCode == 200) {
          have = 0; // server ignored Range → start over
        } else if (res.statusCode != 206) {
          throw HttpException('download HTTP ${res.statusCode}');
        }
        final total = m.size > 0 ? m.size : (res.contentLength > 0 ? res.contentLength + have : 0);
        final sink = part.openWrite(mode: have > 0 ? FileMode.append : FileMode.write);
        var got = have, lastUi = 0;
        await for (final b in res) {
          sink.add(b);
          got += b.length;
          if (total > 0 && got - lastUi > 256 * 1024) {
            lastUi = got;
            progress = got / total;
            notifyListeners();
          }
        }
        await sink.close();
        c.close();
        await part.rename(done.path);
      }
      step = UpdateStep.verifying;
      notifyListeners();
      final err = await _verify(done.path, sha: m.sha256, versionCode: m.versionCode, manifestCert: m.cert);
      if (err != null) {
        await done.delete();
        throw StateError(err);
      }
      readyPath = done.path;
      step = UpdateStep.ready;
      progress = 1;
    } catch (e) {
      step = UpdateStep.failed;
      message = e is StateError ? e.message : 'Download stopped. Tap again to resume.';
      debugPrint('update download: $e');
    }
    notifyListeners();
  }

  /// Returns null when the APK is a newer 4 signed with this app's key, else a reason.
  Future<String?> _verify(String path, {String? sha, int? versionCode, String? manifestCert}) async {
    if (sha != null) {
      final d = await sha256.bind(File(path).openRead()).first;
      if (d.toString() != sha) return 'Download damaged (checksum mismatch). Try again.';
    }
    final a = await _ch.invokeMethod<Map<Object?, Object?>>('inspectApk', {'path': path});
    if (a == null) return 'Not a valid APK.';
    if (a['package'] != info['package']) return 'This APK is not 4.';
    final code = (a['versionCode'] as num).toInt();
    if (code <= currentCode) return 'This APK is not newer than the installed 4.';
    if (versionCode != null && code != versionCode) return 'APK version does not match the release.';
    final c = a['cert'] as String?;
    if (c == null || c != cert) return 'This APK is signed with a different key; installing it would fail.';
    if (manifestCert != null && manifestCert != c) return 'Signing key does not match the release.';
    return null;
  }

  Future<String> install([String? path]) async {
    final p = path ?? readyPath ?? local?.path;
    if (p == null) return 'none';
    final r = await _ch.invokeMethod<String>('install', {'path': p}) ?? 'started';
    if (r == 'permission') message = 'Allow "Install unknown apps" for 4, then tap Install again.';
    notifyListeners();
    return r;
  }

  /// Offline: look for a newer 4 APK in the resources folder (SHAREit / cable). Returns true when one was found.
  Future<bool> scanFolder(String treeUri) async {
    try {
      if (info.isEmpty) await _info();
      final list = await _resCh.invokeListMethod<Map<Object?, Object?>>('listApks', {'uri': treeUri}) ?? const [];
      final dir = await _dir();
      for (final f in list) {
        final tmp = '${dir.path}/shared-${f['size']}.apk';
        if (!File(tmp).existsSync() || File(tmp).lengthSync() != f['size']) {
          await _resCh.invokeMethod<int>('importFile', {'uri': f['uri'], 'dest': tmp});
        }
        final err = await _verify(tmp);
        if (err == null) {
          final a = await _ch.invokeMethod<Map<Object?, Object?>>('inspectApk', {'path': tmp});
          final code = (a!['versionCode'] as num).toInt();
          if (local == null || code > local!.versionCode) local = LocalApk(tmp, code, '${a['versionName']}');
        } else {
          debugPrint('shared apk ${f['name']}: $err');
          File(tmp).deleteSync();
        }
      }
    } catch (e) {
      debugPrint('apk scan: $e');
    }
    notifyListeners();
    return local != null;
  }
}
