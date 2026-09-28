import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// Keeps one Warsay Prep WebView alive so the 13MB pack parses once.
class ExamPrepEngine {
  ExamPrepEngine._();
  static final ExamPrepEngine instance = ExamPrepEngine._();

  static const asset = 'assets/content/examprep_preview/index.html';

  WebViewController? controller;
  bool ready = false;
  String? error;
  final ValueNotifier<bool> loading = ValueNotifier(true);

  Future<void> preload() async {
    if (controller != null) return;
    try {
      final c = WebViewController();
      await c.setJavaScriptMode(JavaScriptMode.unrestricted);
      await c.setBackgroundColor(const Color(0xFFF7F0E5));
      await c.enableZoom(false);
      await c.setUserAgent('Mozilla/5.0 (Linux; Android 14) ExamPrepApp Four');
      c.setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (_) {
            ready = true;
            loading.value = false;
          },
          onWebResourceError: (e) {
            error = e.description;
            loading.value = false;
          },
        ),
      );
      await c.loadFlutterAsset(asset);
      controller = c;
    } catch (e) {
      error = '$e';
      loading.value = false;
    }
  }

  Future<bool> handleBack() async {
    final c = controller;
    if (c == null) return false;
    try {
      final raw = await c.runJavaScriptReturningResult(
        'window.appBack ? window.appBack() : false',
      );
      final s = '$raw'.toLowerCase();
      return s.contains('true');
    } catch (_) {
      return false;
    }
  }
}
