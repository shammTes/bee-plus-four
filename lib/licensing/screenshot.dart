// Screenshot block for notes, exercise, and matric only.
import 'package:flutter/services.dart';

class ScreenshotGuard {
  static const _channel = MethodChannel('com.warsay.high/secure');
  static bool _on = false;

  static Future<void> set(bool on) async {
    if (on == _on) return;
    _on = on;
    try {
      await _channel.invokeMethod<void>('set', on);
    } catch (_) {
      _on = !on;
    }
  }
}
