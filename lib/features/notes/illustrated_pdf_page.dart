import 'package:flutter/material.dart';

import '../../core/theme/four_theme.dart';

/// PDF viewer stub (pdfrx removed — incompatible with current Flutter/Dart on CI).
/// UI still opens; body explains offline pack status.
class IllustratedPdfPage extends StatelessWidget {
  const IllustratedPdfPage({
    super.key,
    required this.title,
    required this.assetPath,
    this.subtitle = '',
    this.initialPage,
  });

  final String title;
  final String assetPath;
  final String subtitle;
  final int? initialPage;

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
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.picture_as_pdf, size: 56, color: FourTheme.primary),
              const SizedBox(height: 16),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 18),
              ),
              const SizedBox(height: 12),
              Text(
                'PDF engine is temporarily offline in this build.\n'
                'Asset: $assetPath'
                '${initialPage != null ? '\nPage: $initialPage' : ''}\n\n'
                'Use text notes, practice, and matric questions for now.',
                textAlign: TextAlign.center,
                style: const TextStyle(height: 1.4, color: FourTheme.muted),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
