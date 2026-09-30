import 'dart:convert';

import 'package:crypto/crypto.dart';

/// Offline payload Bee Seller signs. Two layouts are accepted:
///
/// Flutter 4 / Junior (5 fields):
///   `BEE1|HIGHSCHOOL|<deviceId>|<nonce>|<hmac-sha256-hex>`
///
/// Kotlin Bee Seller (6 fields):
///   `BEE1|<deviceId>|<J|H|K|JH>|<nonce>|<timestamp>|<hmac12>`
class QrPayload {
  static const version = 'BEE1';
  static const _signingKey = String.fromEnvironment(
    'BEE_HMAC_KEY',
    defaultValue: 'BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE',
  );
  static const _sellerKey = 'BEE-PLUS-OFFLINE-SECRET-v1-ET-2026-SHAM';

  final String packageCode;
  final String deviceId;
  final String nonce;
  final String signature;
  final bool sellerLayout;

  const QrPayload({
    required this.packageCode,
    required this.deviceId,
    required this.nonce,
    required this.signature,
    this.sellerLayout = false,
  });

  String get canonical => '$version|$packageCode|$deviceId|$nonce';

  static QrPayload? tryParse(String raw) {
    var text = raw.trim();
    final i = text.indexOf('$version|');
    if (i > 0) text = text.substring(i);
    text = text.replaceAll(RegExp(r'\s+'), '');
    final parts = text.split('|');
    if (parts.isEmpty || parts[0] != version) return null;
    if (parts.length == 5) {
      return QrPayload(
        packageCode: parts[1],
        deviceId: parts[2],
        nonce: parts[3],
        signature: parts[4],
      );
    }
    if (parts.length == 6 && int.tryParse(parts[4]) != null) {
      return QrPayload(
        packageCode: parts[2],
        deviceId: parts[1],
        nonce: parts[3],
        signature: parts[5],
        sellerLayout: true,
      );
    }
    return null;
  }

  bool get isSignatureValid {
    if (sellerLayout) return false;
    return _constantTimeEquals(_hmac(_signingKey, canonical), signature);
  }

  /// Kotlin Seller signs `BEE1|device|pkg|nonce|timestamp` with a 12-byte HMAC.
  bool sellerSignatureValid(String raw) {
    if (!sellerLayout) return false;
    var text = raw.trim();
    final i = text.indexOf('$version|');
    if (i > 0) text = text.substring(i);
    text = text.replaceAll(RegExp(r'\s+'), '');
    final parts = text.split('|');
    if (parts.length != 6) return false;
    final body = '${parts[0]}|${parts[1]}|${parts[2]}|${parts[3]}|${parts[4]}';
    final expect = _hmac12(_sellerKey, body);
    return _constantTimeEquals(expect, parts[5].toLowerCase());
  }

  bool matchesDevice(String currentDeviceId) => deviceId.isNotEmpty && deviceId == currentDeviceId;

  bool get isHighschool {
    final p = packageCode.toUpperCase();
    return p == 'HIGHSCHOOL' || p.contains('H');
  }

  static String _hmac(String key, String body) {
    return Hmac(sha256, utf8.encode(key)).convert(utf8.encode(body)).toString();
  }

  static String _hmac12(String key, String body) {
    final bytes = Hmac(sha256, utf8.encode(key)).convert(utf8.encode(body)).bytes;
    final out = StringBuffer();
    for (var i = 0; i < 12 && i < bytes.length; i++) {
      out.write(bytes[i].toRadixString(16).padLeft(2, '0'));
    }
    return out.toString();
  }

  static bool _constantTimeEquals(String a, String b) {
    if (a.length != b.length) return false;
    var r = 0;
    for (var i = 0; i < a.length; i++) {
      r |= a.codeUnitAt(i) ^ b.codeUnitAt(i);
    }
    return r == 0;
  }
}
