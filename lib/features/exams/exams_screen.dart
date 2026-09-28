import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// The ExamPrep preview app, unchanged — same zip you uploaded.
class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  WebViewController? _controller;
  String? _error;
  bool _loading = true;

  static const _asset = 'assets/content/examprep_preview/index.html';

  @override
  void initState() {
    super.initState();
    _open();
  }

  Future<void> _open() async {
    try {
      final c = WebViewController();
      await c.setJavaScriptMode(JavaScriptMode.unrestricted);
      await c.setBackgroundColor(const Color(0xFFF7F0E5));
      await c.enableZoom(false);
      await c.setUserAgent(
        'Mozilla/5.0 (Linux; Android 13) ExamPrepApp Four',
      );
      c.setNavigationDelegate(
        NavigationDelegate(
          onPageFinished: (_) {
            if (mounted) setState(() => _loading = false);
          },
          onWebResourceError: (e) {
            if (mounted) {
              setState(() {
                _error = e.description;
                _loading = false;
              });
            }
          },
        ),
      );
      await c.loadFlutterAsset(_asset);
      if (!mounted) return;
      setState(() {
        _controller = c;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = '$e';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return ColoredBox(
        color: const Color(0xFFF7F0E5),
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Text(
              'ExamPrep failed to open.\n$_error',
              textAlign: TextAlign.center,
            ),
          ),
        ),
      );
    }
    return ColoredBox(
      color: const Color(0xFFF7F0E5),
      child: Stack(
        children: [
          if (_controller != null) WebViewWidget(controller: _controller!),
          if (_loading) const Center(child: CircularProgressIndicator()),
        ],
      ),
    );
  }
}
