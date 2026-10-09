import 'dart:convert';
import 'dart:typed_data';

import 'package:cryptography/cryptography.dart';
import 'package:four_format/four_format.dart';

/// Which app the encrypted files are for. Each app has its own key domain, so a file made for 4 does not open in
/// Bee Plus and vice versa:
///   4        → `--dart-define=FOUR_MK=<base64 32 bytes>` (same as 4's lib/resources/gate.dart), else 4's DEV key
///   Bee Plus → `--dart-define=BEE_MK=<base64 32 bytes>` (same as Bee Plus' lib/junior/resources/gate.dart), else
///              the Bee Plus DEV key (SHA-256 of 'BEE-RES-DEV-MASTER-KEY-v1-CHANGE-IN-RELEASE')
/// Container format, chunking and file extensions are identical; only the master key differs.
enum KeyTarget {
  four('4', 'FOUR_MK', String.fromEnvironment('FOUR_MK')),
  bee('Bee Plus', 'BEE_MK', String.fromEnvironment('BEE_MK'));

  const KeyTarget(this.label, this.defineName, this.define);
  final String label, defineName, define;

  bool get isDev => define.isEmpty;

  /// Notes subjects of the target app (subject + grade + unit put a file on the matching notes unit page).
  List<String> get subjects => switch (this) {
    four => const ['', 'agriculture', 'biology', 'business_economics', 'chemistry', 'civics', 'english', 'geography', 'history', 'ict', 'mathematics', 'physics', 'tigrinya', 'general'],
    bee => const ['', 'science', 'mathematics', 'english', 'social_studies', 'citizenship', 'ict', 'life_skills', 'tigrinya', 'general'],
  };

  List<int> get grades => switch (this) {
    four => const [0, 9, 10, 11, 12],
    bee => const [0, 6, 7, 8],
  };
}

class MasterKey {
  /// Current target (switch in the app bar). Default 4, so existing workflows are unchanged.
  static KeyTarget target = KeyTarget.four;
  static bool get isDev => target.isDev;

  static final _mk = <KeyTarget, Uint8List>{};

  /// Public development master key of the Bee Plus domain (must match Bee Plus' ResourceGate.devMasterKey).
  static Future<Uint8List> beeDevMasterKey() async {
    final h = await Sha256().hash(utf8.encode('BEE-RES-DEV-MASTER-KEY-v1-CHANGE-IN-RELEASE'));
    return Uint8List.fromList(h.bytes);
  }

  static Future<Uint8List> load([KeyTarget? t]) async {
    final tt = t ?? target;
    final have = _mk[tt];
    if (have != null) return have;
    if (tt.define.isNotEmpty) {
      final k = base64.decode(tt.define.trim());
      if (k.length != 32) throw FourFormatException('${tt.defineName} must be 32 bytes (base64)');
      return _mk[tt] = Uint8List.fromList(k);
    }
    return _mk[tt] = tt == KeyTarget.bee ? await beeDevMasterKey() : await FourKeys.devMasterKey();
  }

  /// Short fingerprint so the user can check both apps carry the same key (never shows the key).
  static Future<String> fingerprint([KeyTarget? t]) async {
    final h = await Sha256().hash([...utf8.encode('4RES-MK-FP|'), ...await load(t)]);
    return h.bytes.take(4).map((b) => b.toRadixString(16).padLeft(2, '0')).join();
  }
}
