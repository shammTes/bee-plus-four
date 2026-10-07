import 'dart:typed_data';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/resources/native_video.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  const ch = MethodChannel('com.warsay.high/video');
  final calls = <MethodCall>[];

  setUp(() {
    calls.clear();
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(ch, (c) async {
      calls.add(c);
      return switch (c.method) {
        'create' => {'id': 7},
        'state' => {'pos': 61000, 'dur': 3723000, 'playing': true, 'buffering': false, 'w': 1280, 'h': 720},
        _ => null,
      };
    });
  });

  test('open passes path + key, then zeroes the Dart copy of the key', () async {
    final key = Uint8List.fromList(List.filled(32, 9));
    final v = await NativeVideo.open('/data/x.4res', key);
    expect(v.id, 7);
    expect((calls.single.arguments as Map)['path'], '/data/x.4res');
    expect(key.every((b) => b == 0), isTrue);
  });

  test('controls and state', () async {
    final v = await NativeVideo.open('/p', Uint8List(32));
    await v.seek(10000);
    await v.speed(1.5);
    final s = await v.state();
    expect(s!.pos, 61000);
    expect(s.w / s.h, closeTo(16 / 9, .01));
    expect(calls.map((c) => c.method), ['create', 'seek', 'speed', 'state']);
    expect(fmtMs(s.dur), '1:02:03');
    expect(fmtMs(61000), '1:01');
  });
}
