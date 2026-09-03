import 'package:flutter/material.dart';

import '../../core/theme/four_theme.dart';

/// Placeholder offline notes viewer (PDF binaries embed next).
class IllustratedPdfPage extends StatelessWidget {
  const IllustratedPdfPage({
    super.key,
    required this.title,
    required this.assetPath,
    this.subtitle = '',
  });

  final String title;
  final String assetPath;
  final String subtitle;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: FourTheme.surface,
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
            if (subtitle.isNotEmpty)
              Text(subtitle,
                  style: const TextStyle(fontSize: 11, color: FourTheme.muted)),
          ],
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: FourTheme.glassPanel(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.picture_as_pdf,
                    size: 48, color: FourTheme.primaryDark),
                const SizedBox(height: 12),
                Text(title,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                        fontWeight: FontWeight.w800, fontSize: 16)),
                const SizedBox(height: 8),
                Text(
                  assetPath.isEmpty
                      ? 'PDF not linked yet.'
                      : 'Ready for embed:\n$assetPath\n\nAdd compressed PDF under assets/content/illustrated_pdf/ and rebuild.',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: FourTheme.muted, height: 1.4),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
