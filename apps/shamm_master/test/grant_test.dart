import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:shamm_master/grant.dart';
import 'package:shamm_master/store.dart';

const userId = 'BEE-ABC2C246C30520515';
const fourVector =
    'BEE1|WHOLESALE:FOUR:50|BEE-ABC2C246C30520515|aaaaaaaaaaaa|e42ec317bc30a5df439c74065383c5a82ae5e40be26b6a99cc79acc1e464d9b2';
const winnerVector =
    'BEE1|WHOLESALE:WINNER:50|BEE-ABC2C246C30520515|aaaaaaaaaaaa|cf547112fb6a4efca935603455ef6553573c3d1eef6a4ac7a5d9897310807415';
const oldUserCode = 'BEE1|WHOLESALE:50|BEE-ABC2C246C30520515|472037270a5d|498eab3fa40f3a3444cb983334a4b6329a3d8f24360bacf5d2ba63d453ce2844';

void main() {
  test('same signatures as the first Shamm Master (Bee Seller test vectors)', () {
    expect(MasterGrant.issueOld(sellerId: userId, credit: 50, nonce: '472037270a5d'), oldUserCode);
    expect(MasterGrant.issue(sellerId: userId, credit: 50, app: SellerApp.four, nonce: 'aaaaaaaaaaaa'), fourVector);
    expect(MasterGrant.issue(sellerId: userId, credit: 50, app: SellerApp.winner, nonce: 'aaaaaaaaaaaa'), winnerVector);
  });

  test('bad input refused, nonce random', () {
    expect(() => MasterGrant.issue(sellerId: userId, credit: 0, app: SellerApp.four), throwsRangeError);
    expect(() => MasterGrant.issue(sellerId: userId, credit: 100001, app: SellerApp.four), throwsRangeError);
    expect(() => MasterGrant.issue(sellerId: 'a|b', credit: 1, app: SellerApp.four), throwsArgumentError);
    expect(MasterGrant.newNonce(), matches(RegExp(r'^[0-9a-f]{12}$')));
    expect(MasterGrant.newNonce(), isNot(MasterGrant.newNonce()));
    expect(MasterGrant.findSellerId('Seller ID: bee-abc2c246c30520515'), userId);
    expect(MasterGrant.findSellerId('BEE-W0123456789ABCDEF'), 'BEE-W0123456789ABCDEF');
    expect(MasterGrant.findSellerId('hello'), isNull);
  });

  test('check: real, old, damaged and wrong codes', () {
    final c = MasterGrant.check(winnerVector);
    expect(c.ok, isTrue);
    expect(c.app, SellerApp.winner);
    expect(c.credit, 50);
    expect(c.sellerId, userId);
    final o = MasterGrant.check('  "$oldUserCode"\n');
    expect(o.ok, isTrue);
    expect(o.app, SellerApp.four);
    expect(o.kind, contains('old'));
    expect(MasterGrant.check(fourVector.replaceAll('|', '%7C')).ok, isTrue);
    expect(MasterGrant.check(fourVector.replaceFirst(':50|', ':500|')).ok, isFalse);
    expect(MasterGrant.check(fourVector.substring(0, fourVector.length - 3)).ok, isFalse);
    expect(MasterGrant.check(userId).problem, contains('Seller ID'));
    expect(MasterGrant.check('hello').ok, isFalse);
    expect(MasterGrant.check('BEE1|WHOLESALE:FOUR:5|x').problem, contains('not complete'));
  });

  test('CSV export quotes commas and quotes', () {
    final s = Store.forTest();
    s.history.add(
      Issued(at: DateTime(2026, 10, 15, 9, 5), sellerId: userId, app: SellerApp.four, credit: 50, code: fourVector, name: 'Abel, "Asmara"'),
    );
    final csv = s.csv();
    expect(csv.split('\r\n').first, 'date,seller_id,seller_name,app,credit,code');
    expect(csv, contains('2026-10-15 09:05,$userId,"Abel, ""Asmara""",Four,50,$fourVector'));
  });

  // Codes for the Bee Seller 1.2.0 compatibility check (tool/bee_seller_compat.sh feeds them to Bee Seller's own
  // parser: core-licensing SellerCreditManager.redeemWith + app-bee-seller ScanParse.topUpCode).
  test('write compatibility vectors', () {
    final ids = [userId, 'BEE-A0123456789ABCDEF', 'BEE-WFEDCBA9876543210'];
    final b = StringBuffer();
    var k = 0;
    for (final id in ids) {
      for (final app in SellerApp.values) {
        for (final n in [1, 10, 50, 500, 100000]) {
          final code = MasterGrant.issue(sellerId: id, credit: n, app: app);
          expect(MasterGrant.check(code).ok, isTrue);
          b.writeln([id, app.code, n, code].join('\t'));
          k++;
        }
      }
    }
    b.writeln([userId, 'FOUR', 50, fourVector].join('\t'));
    b.writeln([userId, 'WINNER', 50, winnerVector].join('\t'));
    final f = File('build/compat_vectors.tsv')..createSync(recursive: true);
    f.writeAsStringSync(b.toString());
    expect(k, 30);
  });
}
