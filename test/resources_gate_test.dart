import 'dart:typed_data';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:four_format/four_format.dart';
import 'package:high/licensing/qr_payload.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:high/resources/gate.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  Future<(UnlockStore, ResourceGate)> setup({bool unlocked = false, Map<String, String> secure = const {}}) async {
    SharedPreferences.setMockInitialValues({'four_device_id_v1': 'ABC234DEF567', if (unlocked) 'four_highschool_unlocked': true});
    FlutterSecureStorage.setMockInitialValues(Map.of(secure));
    final u = UnlockStore();
    await u.init();
    return (u, ResourceGate.install(u));
  }

  test('locked phone gets no master key', () async {
    final (_, g) = await setup();
    expect(await g.mode(), GateMode.locked);
    expect(await g.masterKey(1), isNull);
    expect(await g.deviceKey(), isNull);
  });

  test('old unlock (no proof) falls back to legacy MK-only', () async {
    final (_, g) = await setup(unlocked: true);
    expect(await g.mode(), GateMode.legacy);
    expect(await g.masterKey(1), await FourKeys.devMasterKey());
    expect(await g.masterKey(2), isNull);
  });

  test('fresh unlock stores a proof → strong mode with a different device key', () async {
    final (u, g) = await setup(unlocked: true);
    final legacyKey = await g.deviceKey();
    await g.recordFreshUnlock(await u.deviceId(), 'nonce1');
    expect(await g.mode(), GateMode.strong);
    final strongKey = await g.deviceKey();
    expect(strongKey, isNot(legacyKey));
    expect(await g.masterKey(1), isNotNull);
  });

  test('forged or foreign proof is ignored', () async {
    final (_, g) = await setup(unlocked: true, secure: {'four_res_unlock_v1': '{"d":"ABC234DEF567","n":"x","s":"deadbeef"}'});
    expect(await g.mode(), GateMode.legacy);
    final other = QrPayload.resourceSecret('OTHERPHONE22', 'x');
    final (_, g2) = await setup(unlocked: true, secure: {'four_res_unlock_v1': '{"d":"OTHERPHONE22","n":"x","s":"$other"}'});
    expect(await g2.mode(), GateMode.legacy);
  });

  test('resource opens only through the gate', () async {
    final mk = await FourKeys.devMasterKey();
    final enc = await FourWriter.encryptBytes(
      Uint8List.fromList(List.filled(5000, 7)),
      meta: FourMeta(title: 't', subject: 'biology', grade: 11, type: FourType.pdf, mime: 'application/pdf'),
      masterKey: mk,
      batch: FourBatch.create('b'),
    );
    final (_, locked) = await setup();
    expect(() => FourReader.open(BytesSource(enc), locked.masterKey), throwsA(isA<FourKeyException>()));
    final (_, open) = await setup(unlocked: true);
    final r = await FourReader.open(BytesSource(enc), open.masterKey, verify: true);
    expect((await r.readAll()).length, 5000);
  });

  test('applyPayload with a valid code records the proof (strong)', () async {
    final (u, g) = await setup();
    final r = await u.applyPayload('BEE1|HIGHSCHOOL|ABC234DEF567|0123456789ab|e55e3d2def0a3eb4d977598de639f0d48c02645f37c4226bcb84d0d24b9793d4');
    expect(r.isOk, isTrue, reason: r.error);
    expect(await g.mode(), GateMode.strong);
  });
}
