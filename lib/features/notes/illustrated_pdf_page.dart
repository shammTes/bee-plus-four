import 'package:flutter/material.dart';
import 'package:pdfrx/pdfrx.dart';

import '../../core/theme/four_theme.dart';

/// Offline illustrated-notes PDF viewer (assets or file path).
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
      body: PdfViewer.asset(
        assetPath,
        params: const PdfViewerParams(
          backgroundColor: Color(0xFFF1F5F9),
        ),
      ),
    );
  }
}
