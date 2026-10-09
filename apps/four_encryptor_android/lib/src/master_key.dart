import 'dart:convert';
import 'dart:typed_data';

import 'package:cryptography/cryptography.dart';
import 'package:four_format/four_format.dart';

/// Same source as the 4 app (lib/resources/gate.dart): `--dart-define=FOUR_MK=<base64 32 bytes>`,
/// otherwise the public DEV key from four_format. Build both apps with the same FOUR_MK.
class MasterKey {
  static const _define = String.fromEnvironment('FOUR_MK');
  static bool get isDev => _define.isEmpty;

  static Uint8List? _mk;
  static Future<Uint8List> load() async {
    if (_mk != null) return _mk!;
    if (_define.isNotEmpty) {
      final k = base64.decode(_define.trim());
      if (k.length != 32) throw const FourFormatException('FOUR_MK must be 32 bytes (base64)');
      return _mk = Uint8List.fromList(k);
    }
    return _mk = await FourKeys.devMasterKey();
  }

  /// Short fingerprint so the user can check both apps carry the same key (never shows the key).
  static Future<String> fingerprint() async {
    final h = await Sha256().hash([...utf8.encode('4RES-MK-FP|'), ...await load()]);
    return h.bytes.take(4).map((b) => b.toRadixString(16).padLeft(2, '0')).join();
  }
}
