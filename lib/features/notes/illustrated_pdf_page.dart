import 'package:flutter/material.dart';
import 'package:pdfrx/pdfrx.dart';

import '../../core/theme/four_theme.dart';

/// Offline PDF viewer for textbooks and illustrated notes.
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
    final path = assetPath.startsWith('assets/')
        ? assetPath
        : 'assets/content/$assetPath';

    return Scaffold(
      backgroundColor: FourTheme.surface,
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                    fontSize: 16, fontWeight: FontWeight.w800)),
            if (subtitle.isNotEmpty)
              Text(subtitle,
                  style: const TextStyle(fontSize: 11, color: FourTheme.muted)),
          ],
        ),
      ),
      body: path.isEmpty
          ? const Center(child: Text('No PDF path'))
          : PdfViewer.asset(
              path,
              params: const PdfViewerParams(
                margin: 8,
              ),
            ),
    );
  }
}
