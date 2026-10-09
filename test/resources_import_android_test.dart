// End-to-end import check under Android-like crypto: cryptography_flutter sends HMAC to javax.crypto, which
// throws "IllegalArgumentException: Empty key" for a zero-length key. A file written exactly like
// 4 Encryptor 1.0.1 (FourWriter.write, 256 KiB chunks, thumbnail, video meta) must import in 4:
// magic/id from the head, peek, gate master key, footer verify, full decrypt, sealed index.
import 'dart:io';

import 'package:cryptography/cryptography.dart';
import 'package:cryptography/dart.dart';
import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:four_format/four_format.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:high/resources/gate.dart';
import 'package:high/resources/library.dart';
import 'package:shared_preferences/shared_preferences.dart';

class _StrictHmac extends Hmac {
  _StrictHmac(this.hashAlgorithm) : super.constructor();
  @override
  final HashAlgorithm hashAlgorithm;
  @override
  Future<Mac> calculateMac(List<int> bytes, {required SecretKey secretKey, List<int> nonce = const [], List<int> aad = const []}) async {
    final k = await secretKey.extractBytes();
    if (k.isEmpty) throw PlatformException(code: 'CAUGHT_ERROR', message: 'Unexpected error java.lang.IllegalArgumentException: Empty key');
    return DartHmac(hashAlgorithm).calculateMac(bytes, secretKey: SecretKey(k));
  }

  @override
  DartHmac toSync() => DartHmac(hashAlgorithm);
}

class _AndroidLike extends DartCryptography {
  @override
  Hmac hmac(HashAlgorithm hashAlgorithm) => _StrictHmac(hashAlgorithm);
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late Cryptography saved;
  setUp(() {
    saved = Cryptography.instance;
    Cryptography.instance = _AndroidLike();
  });
  tearDown(() => Cryptography.instance = saved);

  Future<ResourceGate> gate({bool unlocked = true}) async {
    SharedPreferences.setMockInitialValues({'four_device_id_v1': 'ABC234DEF567', if (unlocked) 'four_highschool_unlocked': true});
    FlutterSecureStorage.setMockInitialValues({});
    final u = UnlockStore();
    await u.init();
    return ResourceGate.install(u);
  }

  /// Same call and meta shape as 4 Encryptor 1.0.1 (encryptStream → FourWriter.write), streamed to a file.
  Future<(File, Uint8List)> encryptorFile({List<int>? mk, int size = 700000}) async {
    final plain = Uint8List.fromList(List.generate(size, (i) => i * 37 & 0xff));
    final f = File('${(await Directory.systemTemp.createTemp('4imp')).path}/clip.4vid');
    final sink = f.openWrite();
    await FourWriter.write(
      input: BytesSource(plain),
      add: (b) => sink.add(b),
      meta: FourMeta(title: 'clip', subject: '', grade: 0, unit: '', type: FourType.video, mime: 'video/mp4', durationMs: 12000),
      masterKey: mk ?? await FourKeys.devMasterKey(),
      batch: FourBatch.create('android-20261009T070000'),
      thumbnail: List.filled(900, 9),
    );
    await sink.close();
    return (f, plain);
  }

  test('old code path really fails on Android (empty HKDF salt → Empty key)', () async {
    expect(() => Hkdf(hmac: Hmac.sha256(), outputLength: 32).deriveKey(secretKey: SecretKey(List.filled(32, 1)), nonce: const []), throwsA(isA<PlatformException>()));
  });

  test('encryptor 1.0.1 file imports in 4 (legacy + strong unlock), footer verified, bytes identical', () async {
    final (f, plain) = await encryptorFile();
    final head = await f.openRead(0, 64).first;
    expect(FourFormat.hasMagic(head), isTrue);
    final id = head.sublist(8, 24).map((b) => b.toRadixString(16).padLeft(2, '0')).join();
    for (final strong in [false, true]) {
      final g = await gate();
      if (strong) await g.recordFreshUnlock('ABC234DEF567', 'n1');
      final src = await FileSource.open(f.path);
      try {
        expect((await FourReader.peek(src)).fileIdHex, id);
        final r = await FourReader.open(src, g.masterKey, verify: true);
        expect(r.meta.type, FourType.video);
        expect(r.thumbnail!.length, 900);
        expect(await r.readAll(), plain);
      } finally {
        await src.close();
      }
      // sealed local index (device key = HKDF with a non-empty salt) still works
      final dk = await g.deviceKey();
      final box = await FourKeys.aes.encrypt([1, 2, 3], secretKey: SecretKey(dk!), nonce: FourKeys.random(12));
      expect(await FourKeys.aes.decrypt(box, secretKey: SecretKey(dk)), [1, 2, 3]);
    }
  });

  test('device key unchanged by the fix (old indexes stay readable)', () async {
    final g = await gate();
    final dk = await g.deviceKey();
    Cryptography.instance = DartCryptography.defaultInstance; // the pre-fix pure-Dart Hkdf
    final mk = await FourKeys.devMasterKey();
    final old = await Hkdf(hmac: Hmac.sha256(), outputLength: 32).deriveKey(secretKey: SecretKey(mk), info: 'x4RES-device-v1'.substring(1).codeUnits, nonce: 'legacy|ABC234DEF567'.codeUnits);
    expect(dk, await old.extractBytes());
  });

  test('failure reasons are plain', () async {
    final (f, _) = await encryptorFile(mk: List.filled(32, 5)); // other FOUR_MK
    final g = await gate();
    Future<String> reason(FourSource s, ResourceGate gg) async {
      try {
        await FourReader.open(s, gg.masterKey, verify: true);
        return 'opened';
      } catch (e) {
        return explainImportError(e);
      }
    }

    final bytes = await f.readAsBytes();
    expect(await reason(BytesSource(bytes), g), contains('different key'));
    expect(await reason(BytesSource(Uint8List.sublistView(bytes, 0, bytes.length - 100)), g), contains('damaged'));
    expect(await reason(BytesSource(bytes), await gate(unlocked: false)), contains('not unlocked'));
    expect(explainImportError(PlatformException(code: 'import', message: 'IOException: ENOSPC')), contains('storage'));
    expect(explainImportError(const FourFormatException('unsupported version 2')), contains('update 4'));
  });
}
