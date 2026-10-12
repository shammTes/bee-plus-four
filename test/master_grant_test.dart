import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/master/master_grant.dart';
import 'package:high/master_main.dart';

void main() {
  const userId = 'BEE-ABC2C246C30520515';

  test('old code (no app) from the user phone is unchanged', () {
    // Real code from the Shamm Master screenshot (2026-10-10); Bee Seller reads it as Four credit.
    expect(
      MasterGrant.issueOld(sellerId: userId, credit: 50, nonce: '472037270a5d'),
      'BEE1|WHOLESALE:50|BEE-ABC2C246C30520515|472037270a5d|498eab3fa40f3a3444cb983334a4b6329a3d8f24360bacf5d2ba63d453ce2844',
    );
  });

  test('new codes carry the app', () {
    final f = MasterGrant.issue(sellerId: userId, credit: 50, app: SellerApp.four, nonce: 'aaaaaaaaaaaa');
    final w = MasterGrant.issue(sellerId: userId, credit: 50, app: SellerApp.winner, nonce: 'aaaaaaaaaaaa');
    expect(f, startsWith('BEE1|WHOLESALE:FOUR:50|$userId|aaaaaaaaaaaa|'));
    expect(w, startsWith('BEE1|WHOLESALE:WINNER:50|$userId|aaaaaaaaaaaa|'));
    expect(f.split('|').last, hasLength(64));
    expect(f.split('|').last, isNot(w.split('|').last)); // the app is inside the signature
    expect(f, FOUR_VECTOR);
    expect(w, WINNER_VECTOR);
  });

  test('bad input refused, nonce random', () {
    expect(() => MasterGrant.issue(sellerId: userId, credit: 0, app: SellerApp.four), throwsRangeError);
    expect(() => MasterGrant.issue(sellerId: 'a|b', credit: 1, app: SellerApp.four), throwsArgumentError);
    expect(MasterGrant.newNonce(), matches(RegExp(r'^[0-9a-f]{12}$')));
    expect(MasterGrant.newNonce(), isNot(MasterGrant.newNonce()));
    expect(MasterGrant.findSellerId('Seller ID: bee-abc2c246c30520515'), userId);
  });

  testWidgets('issuer UI: pick Winner, make code', (t) async {
    t.view.physicalSize = const Size(1080, 2400);
    t.view.devicePixelRatio = 1;
    addTearDown(t.view.reset);
    await t.pumpWidget(const ShammMasterApp());
    expect(find.text('Four (Grade 9–12)'), findsWidgets);
    await t.tap(find.text('Winner').first);
    await t.pump();
    await t.enterText(find.byKey(const Key('sellerId')), userId);
    await t.enterText(find.byKey(const Key('credit')), '25');
    await t.ensureVisible(find.byKey(const Key('make')));
    await t.tap(find.byKey(const Key('make')));
    await t.pump();
    final code = (t.widget(find.byKey(const Key('code'))) as SelectableText).data!;
    expect(code, startsWith('BEE1|WHOLESALE:WINNER:25|$userId|'));
    expect(find.text('Code made: 25 Winner credit for $userId.'), findsOneWidget);
  });
}

// ignore: constant_identifier_names
const FOUR_VECTOR = 'BEE1|WHOLESALE:FOUR:50|BEE-ABC2C246C30520515|aaaaaaaaaaaa|e42ec317bc30a5df439c74065383c5a82ae5e40be26b6a99cc79acc1e464d9b2';
// ignore: constant_identifier_names
const WINNER_VECTOR = 'BEE1|WHOLESALE:WINNER:50|BEE-ABC2C246C30520515|aaaaaaaaaaaa|cf547112fb6a4efca935603455ef6553573c3d1eef6a4ac7a5d9897310807415';
