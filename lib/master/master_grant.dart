// Shamm Master: top-up (wholesale) codes for Bee Seller, one app per code.
//
//   BEE1|WHOLESALE:FOUR:{n}|{sellerId}|{nonce12}|{hmac64}     Four credit   (High school, Grade 9–12)
//   BEE1|WHOLESALE:WINNER:{n}|{sellerId}|{nonce12}|{hmac64}   Winner credit (Junior, was Bee Plus)
//
// hmac64 = full HMAC-SHA256 (lowercase hex) of everything before the last '|', key BEE_HMAC_KEY (same default as the
// Shamm Master app built from the old lib/core/licensing/qr_payload.dart, so codes made with it keep working).
// Old codes BEE1|WHOLESALE:{n}|… (no app part) are still read by Bee Seller as Four credit (the only app sold before).
// Bee Seller (shammTes/bee-plus-ecosystem, Android 1.2.0 / Windows 3.2.0) reads this exact format.
import 'dart:convert';
import 'dart:math';

import 'package:crypto/crypto.dart';

/// The app whose credit a code adds.
enum SellerApp {
  four('FOUR', 'Four (Grade 9–12)'),
  winner('WINNER', 'Winner');

  const SellerApp(this.code, this.label);

  /// Word inside the code.
  final String code;

  /// Plain label for buttons.
  final String label;
}

class MasterGrant {
  static const version = 'BEE1';
  static const maxCredit = 100000;
  static const _key = String.fromEnvironment(
    'BEE_HMAC_KEY',
    defaultValue: 'BEE_PLUS_ERITREA_OFFLINE_HMAC_V1_CHANGE_IN_RELEASE',
  );

  /// Makes a signed top-up code for one seller and one app. [nonce] is random when not given.
  static String issue({
    required String sellerId,
    required int credit,
    required SellerApp app,
    String? nonce,
  }) {
    final id = sellerId.trim();
    if (id.isEmpty || id.contains('|')) throw ArgumentError('Seller ID');
    if (credit < 1 || credit > maxCredit) throw RangeError.range(credit, 1, maxCredit, 'credit');
    final n = nonce ?? newNonce();
    final body = '$version|WHOLESALE:${app.code}:$credit|$id|$n';
    return '$body|${hmacHex(body)}';
  }

  /// Old format without the app part (= Four). Kept only so tests can check the old vector.
  static String issueOld({required String sellerId, required int credit, required String nonce}) {
    final body = '$version|WHOLESALE:$credit|${sellerId.trim()}|$nonce';
    return '$body|${hmacHex(body)}';
  }

  static String hmacHex(String body) =>
      Hmac(sha256, utf8.encode(_key)).convert(utf8.encode(body)).toString();

  /// 12 hex characters, from a secure random source.
  static String newNonce() {
    final r = Random.secure();
    return List.generate(6, (_) => r.nextInt(256).toRadixString(16).padLeft(2, '0')).join();
  }

  /// Bee Seller IDs look like BEE-A + 16 hex (phone) or BEE-W + 16 hex (Windows). Finds one in pasted text.
  static String? findSellerId(String raw) =>
      RegExp(r'BEE-[AW][0-9A-F]{16}').firstMatch(raw.toUpperCase().replaceAll(' ', ''))?.group(0);
}
