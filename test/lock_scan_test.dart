import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:high/licensing/lock_screen.dart';
import 'package:high/licensing/unlock_store.dart';
import 'package:shared_preferences/shared_preferences.dart';

const _channel = MethodChannel('com.warsay.high/secure');

/// Fake native side of `com.warsay.high/secure`.
class _Native {
  final calls = <String>[];
  bool granted = true;
  Object? startupReport;
  Completer<Object?> scan = Completer<Object?>();
  Object? photo = const {'status': 'cancelled'};

  Future<Object?> handle(MethodCall c) async {
    calls.add(c.method);
    switch (c.method) {
      case 'hasCamera':
      case 'requestCamera':
        return granted;
      case 'takeStartupReport':
        return startupReport;
      case 'scanUnlock':
        return scan.future;
      case 'cancelScan':
        if (!scan.isCompleted) scan.complete({'status': 'error', 'code': 'not_opened'});
        return true;
      case 'capturePhotoAndScanQr':
        return photo;
      case 'getLog':
        return <String>['10:00:00 I native line'];
    }
    return null;
  }
}

Future<_Native> _pump(WidgetTester t, {Object? startupReport}) async {
  // A small phone: 360 x 740 dp.
  t.view.physicalSize = const Size(720, 1480);
  t.view.devicePixelRatio = 2;
  addTearDown(t.view.reset);
  SharedPreferences.setMockInitialValues({});
  final store = UnlockStore();
  await store.init();
  final n = _Native()..startupReport = startupReport;
  t.binding.defaultBinaryMessenger.setMockMethodCallHandler(_channel, n.handle);
  addTearDown(() => t.binding.defaultBinaryMessenger.setMockMethodCallHandler(_channel, null));
  await t.pumpWidget(
    WidgetsApp(color: const Color(0xFF000000), builder: (c, _) => LockScreen(unlock: store, onUnlocked: () {})),
  );
  await t.pump();
  return n;
}

bool _onScreen(WidgetTester t, Finder f) {
  final r = t.getRect(f);
  return r.top >= 0 && r.bottom <= 740;
}

Future<void> _settle(WidgetTester t) async {
  for (var i = 0; i < 12; i++) {
    await t.pump(const Duration(milliseconds: 100));
  }
}

/// Lock-screen scanning is Android-only; the platform override must be reset inside the body.
void _testAndroid(String name, Future<void> Function(WidgetTester t) body) {
  testWidgets(name, (t) async {
    debugDefaultTargetPlatformOverride = TargetPlatform.android;
    try {
      await body(t);
    } finally {
      debugDefaultTargetPlatformOverride = null;
    }
  });
}

void main() {

  test('error codes are short and readable', () {
    expect(scanErrorCode('not_opened'), 'E-NOT-OPENED');
    expect(scanErrorCode(null), 'E-UNKNOWN');
    expect(liveScannerBroken('launch'), isTrue);
    expect(liveScannerBroken('permission_denied'), isFalse);
  });

  _testAndroid('tapping Scan opens the live scanner and shows a status on screen', (t) async {
    final n = await _pump(t);
    await t.tap(find.text('Scan unlock code'));
    await _settle(t);
    expect(n.calls, containsAllInOrder(['hasCamera', 'scanUnlock']));
    final status = find.textContaining('Opening the scanner');
    expect(status, findsOneWidget);
    expect(_onScreen(t, status), isTrue, reason: 'status must be visible without scrolling');
    // Scanner screen comes up → app leaves the foreground → watchdog must not fire.
    for (final s in [AppLifecycleState.inactive, AppLifecycleState.hidden, AppLifecycleState.paused]) {
      t.binding.handleAppLifecycleStateChanged(s);
    }
    await t.pump(const Duration(seconds: 11));
    expect(n.calls, isNot(contains('cancelScan')));
    for (final s in [AppLifecycleState.hidden, AppLifecycleState.inactive, AppLifecycleState.resumed]) {
      t.binding.handleAppLifecycleStateChanged(s);
    }
    n.scan.complete({'status': 'cancelled', 'frames': 0});
    await _settle(t);
    expect(find.textContaining('Scan cancelled'), findsOneWidget);
  });

  _testAndroid('live scanner launch error falls back to photo scan with a code', (t) async {
    final n = await _pump(t);
    await t.tap(find.text('Scan unlock code'));
    await _settle(t);
    n.scan.complete({'status': 'error', 'code': 'launch', 'message': 'Scanner could not open: boom'});
    await _settle(t);
    expect(n.calls, contains('capturePhotoAndScanQr'));
    expect(find.textContaining('E-LAUNCH'), findsWidgets);
  });

  _testAndroid('scanner that never appears is reported and falls back (watchdog)', (t) async {
    final n = await _pump(t);
    await t.tap(find.text('Scan unlock code'));
    await _settle(t);
    await t.pump(const Duration(seconds: 11));
    await _settle(t);
    expect(n.calls, contains('cancelScan'));
    expect(n.calls, contains('capturePhotoAndScanQr'));
    expect(find.textContaining('E-NOT-OPENED'), findsWidgets);
  });

  _testAndroid('a crash in the last run is shown and Scan uses photo scan', (t) async {
    final n = await _pump(
      t,
      startupReport: {'code': 'crash', 'wasScanning': true, 'message': 'java.lang.IllegalStateException: x', 'detail': 'stack'},
    );
    await _settle(t);
    expect(find.textContaining('E-CRASH'), findsOneWidget);
    expect(_onScreen(t, find.textContaining('E-CRASH')), isTrue);
    await t.tap(find.text('Scan unlock code'));
    await _settle(t);
    expect(n.calls, contains('capturePhotoAndScanQr'));
    expect(n.calls, isNot(contains('scanUnlock')));
  });

  _testAndroid('long-press on Scan shows the scanner log', (t) async {
    await _pump(t);
    await t.longPress(find.text('Scan unlock code'));
    await _settle(t);
    expect(find.textContaining('native line'), findsOneWidget, reason: 'log scrolled into view');
  });

  _testAndroid('missing native channel is visible, not silent', (t) async {
    await _pump(t);
    t.binding.defaultBinaryMessenger.setMockMethodCallHandler(_channel, (c) async {
      if (c.method == 'hasCamera' || c.method == 'requestCamera') return true;
      throw MissingPluginException('No implementation found for method ${c.method}');
    });
    await t.tap(find.text('Scan unlock code'));
    await _settle(t);
    expect(find.textContaining('E-NO-CHANNEL'), findsOneWidget);
  });
}
