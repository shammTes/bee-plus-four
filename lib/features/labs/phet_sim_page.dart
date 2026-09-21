import 'package:flutter/material.dart';

/// Offline lab placeholder (webview optional — avoids hard CI dependency).
/// When PhET HTML assets are embedded, this page can be upgraded to WebView.
class PhetSimPage extends StatelessWidget {
  const PhetSimPage({
    super.key,
    required this.title,
    required this.assetPath,
  });

  final String title;
  final String assetPath;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title,
            style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.science_outlined, size: 56),
              const SizedBox(height: 16),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 18),
              ),
              const SizedBox(height: 12),
              Text(
                'This offline lab pack is not embedded in this build yet.\n'
                'Asset: $assetPath\n\n'
                'Use Notes, Practice, and Matric while labs are prepared.',
                textAlign: TextAlign.center,
                style: const TextStyle(height: 1.4),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
