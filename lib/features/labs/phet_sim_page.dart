import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// Offline PhET HTML5 simulation loaded from Flutter assets.
class PhetSimPage extends StatefulWidget {
  const PhetSimPage({
    super.key,
    required this.title,
    required this.assetPath,
  });

  final String title;
  /// e.g. assets/content/phet/ohms-law_all.html
  final String assetPath;

  @override
  State<PhetSimPage> createState() => _PhetSimPageState();
}

class _PhetSimPageState extends State<PhetSimPage> {
  late final WebViewController _controller;
  var _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF0B1220))
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (_) {
            if (mounted) {
              setState(() {
                _loading = true;
                _error = null;
              });
            }
          },
          onPageFinished: (_) {
            if (mounted) setState(() => _loading = false);
          },
          onWebResourceError: (e) {
            if (mounted) {
              setState(() {
                _loading = false;
                _error = e.description;
              });
            }
          },
        ),
      );
    _loadAsset();
  }

  Future<void> _loadAsset() async {
    try {
      // Single-file PhET builds are self-contained HTML.
      await _controller.loadFlutterAsset(widget.assetPath);
    } catch (e) {
      if (mounted) {
        setState(() {
          _loading = false;
          _error = 'Could not load offline sim.\n$e';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title,
            style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
        actions: [
          IconButton(
            tooltip: 'Reload',
            onPressed: _loadAsset,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: Stack(
        children: [
          if (_error != null)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.error_outline, size: 48),
                    const SizedBox(height: 12),
                    Text(
                      _error!,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: _loadAsset,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              ),
            )
          else
            WebViewWidget(controller: _controller),
          if (_loading)
            const Center(child: CircularProgressIndicator()),
        ],
      ),
    );
  }
}
