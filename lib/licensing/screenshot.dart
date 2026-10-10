// Screenshot / screen-recording block (Android FLAG_SECURE) for the Notes and Matric sections and the
// encrypted resource viewers.
//
// Several features want the flag at the same time (a notes page with a video resource on top, a reels
// page opened from a PDF...). Each one *acquires* the flag under its own owner name and *releases* it
// when it leaves the screen. The native flag is only turned on when the first holder arrives and only
// cleared when the last holder leaves, so one feature can never clear the flag another still needs.
//
// The native side is `setSecure(on)` on the existing `com.warsay.high/resources` channel
// (ResourcesChannel.kt). MainActivity.onResume re-applies the last state; [ScreenshotGuard] also re-sends
// it when the app comes back to the foreground (the unlock camera clears the flag while it is open).
import 'package:flutter/foundation.dart' show visibleForTesting;
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

typedef SecureSink = Future<void> Function(bool on);

/// Reference-counted secure flag. Pure Dart: the platform call is injected so it can be unit tested.
class SecureFlag {
  SecureFlag(this._sink);
  final SecureSink _sink;
  final Map<String, int> _holds = {};
  bool _on = false;

  /// true while at least one holder has the flag
  bool get isOn => _on;
  int get count => _holds.values.fold(0, (a, b) => a + b);
  int holds(String owner) => _holds[owner] ?? 0;

  void acquire(String owner) {
    _holds[owner] = holds(owner) + 1;
    _apply();
  }

  /// A release without a matching acquire is ignored (it can never clear someone else's hold).
  void release(String owner) {
    final n = holds(owner);
    if (n <= 0) return;
    if (n == 1) {
      _holds.remove(owner);
    } else {
      _holds[owner] = n - 1;
    }
    _apply();
  }

  /// drop every hold of [owner] (e.g. the whole app shell is being disposed)
  void releaseAll(String owner) {
    if (_holds.remove(owner) != null) _apply();
  }

  /// re-send the current state to the platform (app resumed)
  Future<void> reapply() => _sink(_on);

  void _apply() {
    final want = count > 0;
    if (want == _on) return;
    _on = want;
    _sink(want);
  }
}

abstract final class ScreenshotGuard {
  static const _ch = MethodChannel('com.warsay.high/resources');

  static Future<void> _platform(bool on) async {
    try {
      await _ch.invokeMethod<void>('setSecure', {'on': on});
    } catch (_) {}
  }

  static SecureFlag flag = SecureFlag(_platform);

  /// fresh flag with no holders (tests)
  @visibleForTesting
  static void reset() => flag = SecureFlag(_platform);
  static _Lifecycle? _life;

  static void _ensureLifecycle() {
    if (_life != null) return;
    try {
      _life = _Lifecycle();
      WidgetsBinding.instance.addObserver(_life!);
    } catch (_) {
      _life = null; // no binding (pure Dart tests)
    }
  }

  static void acquire(String owner) {
    _ensureLifecycle();
    flag.acquire(owner);
  }

  static void release(String owner) => flag.release(owner);
  static void releaseAll(String owner) => flag.releaseAll(owner);
  static bool get isOn => flag.isOn;
}

class _Lifecycle with WidgetsBindingObserver {
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) ScreenshotGuard.flag.reapply();
  }
}
