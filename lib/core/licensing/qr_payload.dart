import 'dart:convert';
import 'package:crypto/crypto.dart';

/// Offline signed payloads shared by 4 (student), Bee Seller, and Master (Shamm).
///
/// Formats (pipe-separated):
/// - Student unlock:  BEE1|HIGHSCHOOL|{deviceId}|{nonce}|{sig}
/// - Wholesale auth:  BEE1|WHOLESALE:{quota}|{sellerDeviceId}|{nonce}|{sig}
/// - Sub-seller auth: BEE1|SELLER:{quota}|{sellerDeviceId}|{nonce}|{sig}
class QrPayload {
  static const version = 'BEE1';
  static const _signingKey = String.fromEnvironment(
    'BEE_HMAC_KEY',
    defaultValue: 'BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE',
  );

  final String packageCode;
  final String deviceId;
  final String nonce;
  final String signature;

  const QrPayload({
    required this.packageCode,
    required this.deviceId,
    required this.nonce,
    required this.signature,
  });

  String get canonical => '$version|$packageCode|$deviceId|$nonce';

  static QrPayload issue({
    required String packageCode,
    required String deviceId,
    required String nonce,
  }) {
    final body = '$version|$packageCode|$deviceId|$nonce';
    return QrPayload(
      packageCode: packageCode,
      deviceId: deviceId,
      nonce: nonce,
      signature: _hmac(body),
    );
  }

  static QrPayload issueWholesale({
    required String sellerDeviceId,
    required int quota,
    required String nonce,
  }) {
    final code = 'WHOLESALE:${quota.clamp(1, 100000)}';
    final body = '$version|$code|$sellerDeviceId|$nonce';
    return QrPayload(
      packageCode: code,
      deviceId: sellerDeviceId,
      nonce: nonce,
      signature: _hmac(body),
    );
  }

  static QrPayload issueSeller({
    required String sellerDeviceId,
    required int quota,
    required String nonce,
  }) {
    final code = 'SELLER:${quota.clamp(1, 100000)}';
    final body = '$version|$code|$sellerDeviceId|$nonce';
    return QrPayload(
      packageCode: code,
      deviceId: sellerDeviceId,
      nonce: nonce,
      signature: _hmac(body),
    );
  }

  String encode() => '$canonical|$signature';

  static QrPayload? tryParse(String raw) {
    final parts = raw.trim().split('|');
    if (parts.length != 5 || parts[0] != version) return null;
    return QrPayload(
      packageCode: parts[1],
      deviceId: parts[2],
      nonce: parts[3],
      signature: parts[4],
    );
  }

  bool get isSignatureValid =>
      _constantTimeEquals(_hmac(canonical), signature);

  bool matchesDevice(String currentDeviceId) =>
      deviceId.isNotEmpty && deviceId == currentDeviceId;

  bool get isWholesale => packageCode.toUpperCase().startsWith('WHOLESALE');
  bool get isSellerGrant => packageCode.toUpperCase().startsWith('SELLER:');
  bool get isStudentUnlock =>
      packageCode.toUpperCase() == 'HIGHSCHOOL' ||
      packageCode.toUpperCase() == 'JUNIOR';

  int? get quota {
    final p = packageCode.split(':');
    if (p.length != 2) return null;
    return int.tryParse(p[1]);
  }

  static String _hmac(String body) =>
      Hmac(sha256, utf8.encode(_signingKey)).convert(utf8.encode(body)).toString();

  static bool _constantTimeEquals(String a, String b) {
    if (a.length != b.length) return false;
    var r = 0;
    for (var i = 0; i < a.length; i++) {
      r |= a.codeUnitAt(i) ^ b.codeUnitAt(i);
    }
    return r == 0;
  }
}

enum UnlockPackage { junior, highschool }

extension UnlockPackageX on UnlockPackage {
  String get code => switch (this) {
        UnlockPackage.junior => 'JUNIOR',
        UnlockPackage.highschool => 'HIGHSCHOOL',
      };

  static UnlockPackage? fromCode(String c) {
    switch (c.toUpperCase()) {
      case 'JUNIOR':
        return UnlockPackage.junior;
      case 'HIGHSCHOOL':
        return UnlockPackage.highschool;
      default:
        return null;
    }
  }
}
