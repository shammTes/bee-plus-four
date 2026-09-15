import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path_provider/path_provider.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// Offline PhET HTML5 simulation — never uses the network.
/// Copies the single-file sim from Flutter assets into app storage, then
/// loads via file:// so Android WebView works reliably offline.
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
          // Hard-block any outbound network request.
          onNavigationRequest: (req) {
            final u = req.url.toLowerCase();
            if (u.startsWith('file:') ||
                u.startsWith('about:') ||
                u.startsWith('data:') ||
                u.startsWith('blob:')) {
              return NavigationDecision.navigate;
            }
            // PhET must never phone home.
            return NavigationDecision.prevent;
          },
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
            // Ignore blocked external resource noise; only surface hard failures.
            if (e.isForMainFrame == true && mounted) {
              setState(() {
                _loading = false;
                _error = e.description;
              });
            }
          },
        ),
      );
    _loadOffline();
  }

  Future<void> _loadOffline() async {
    if (mounted) {
      setState(() {
        _loading = true;
        _error = null;
      });
    }
    try {
      // 1) Read bundled HTML from APK assets
      final data = await rootBundle.load(widget.assetPath);
      final bytes = data.buffer.asUint8List();
      if (bytes.length < 1000) {
        throw Exception(
          'Sim file too small or missing from APK.\n'
          'Rebuild after sharing the PhET Drive pack as Anyone with the link.',
        );
      }

      // 2) Write to app-private storage (reliable file:// load on Android)
      final dir = await getApplicationSupportDirectory();
      final phetDir = Directory('${dir.path}/phet');
      if (!await phetDir.exists()) {
        await phetDir.create(recursive: true);
      }
      final name = widget.assetPath.split('/').last;
      final file = File('${phetDir.path}/$name');
      // Skip rewrite if same size already present
      if (!await file.exists() || (await file.length()) != bytes.length) {
        await file.writeAsBytes(bytes, flush: true);
      }

      // 3) Load local file only — no internet
      await _controller.loadFile(file.path);
    } on FlutterError catch (e) {
      if (mounted) {
        setState(() {
          _loading = false;
          _error =
              'This simulation is not embedded in the APK yet.\n'
              'Asset: ${widget.assetPath}\n\n'
              'Share Drive file four_phet_offline.tgz as "Anyone with the link", '
              'then rebuild the APK from GitHub Actions.\n\n$e';
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _loading = false;
          _error = 'Offline load failed.\n$e';
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
          const Padding(
            padding: EdgeInsets.only(right: 4),
            child: Center(
              child: Text('OFFLINE',
                  style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w900,
                      color: Color(0xFF5EEAD4))),
            ),
          ),
          IconButton(
            tooltip: 'Reload offline',
            onPressed: _loadOffline,
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
                    const Icon(Icons.cloud_off, size: 48),
                    const SizedBox(height: 12),
                    Text(
                      _error!,
                      textAlign: TextAlign.center,
                      style: const TextStyle(height: 1.4),
                    ),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: _loadOffline,
                      child: const Text('Retry offline load'),
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
