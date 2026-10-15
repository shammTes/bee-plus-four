import 'package:flutter/services.dart';

/// Android side: live QR scanner (ML Kit, copied from Four) and the share sheet.
class Native {
  static const _ch = MethodChannel('com.shamm.master/native');

  /// Text of the scanned QR, or null (cancelled). Throws [PlatformException]-free: errors come back as a message.
  static Future<({String? text, String? error})> scan({required String title, required String hint}) async {
    try {
      final r = await _ch.invokeMapMethod<String, Object?>('scan', {'title': title, 'hint': hint});
      if (r == null) return (text: null, error: null);
      if (r['status'] == 'ok') return (text: r['payload'] as String?, error: null);
      if (r['status'] == 'error') {
        final code = r['code'];
        return (text: null, error: code == 'permission_denied' ? 'Allow the camera to scan.' : '${r['message'] ?? code}');
      }
      return (text: null, error: null);
    } on MissingPluginException {
      return (text: null, error: 'The scanner works on Android phones only.');
    } on PlatformException catch (e) {
      return (text: null, error: e.message);
    }
  }

  static Future<bool> shareText(String text, {String title = 'Share code'}) async {
    try {
      await _ch.invokeMethod('shareText', {'text': text, 'title': title});
      return true;
    } catch (_) {
      return false;
    }
  }

  static Future<bool> shareFile(String name, String content, {String mime = 'text/csv', String title = 'Export'}) async {
    try {
      await _ch.invokeMethod('shareFile', {'name': name, 'content': content, 'mime': mime, 'title': title});
      return true;
    } catch (_) {
      return false;
    }
  }
}
