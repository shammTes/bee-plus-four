import 'package:flutter/material.dart';

import '../../core/theme/four_theme.dart';

/// Colorful card-style illustrated lesson (used when PDF pack is missing).
class IllustratedCardsPage extends StatefulWidget {
  const IllustratedCardsPage({
    super.key,
    required this.title,
    required this.subtitle,
    required this.slides,
  });

  final String title;
  final String subtitle;
  final List<Map<String, dynamic>> slides;

  @override
  State<IllustratedCardsPage> createState() => _IllustratedCardsPageState();
}

class _IllustratedCardsPageState extends State<IllustratedCardsPage> {
  final _ctrl = PageController();
  int page = 0;

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final slides = widget.slides;
    return Scaffold(
      backgroundColor: FourTheme.surface,
      appBar: AppBar(
        title: Text(widget.title,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
            child: Row(
              children: [
                Expanded(
                  child: Text(widget.subtitle,
                      style: const TextStyle(color: FourTheme.muted)),
                ),
                Text('${page + 1}/${slides.length}',
                    style: const TextStyle(fontWeight: FontWeight.w800)),
              ],
            ),
          ),
          Expanded(
            child: PageView.builder(
              controller: _ctrl,
              itemCount: slides.length,
              onPageChanged: (i) => setState(() => page = i),
              itemBuilder: (context, i) {
                final s = slides[i];
                final accent = Color(
                  int.parse((s['accent'] as String? ?? '#0D9488')
                      .replaceFirst('#', '0xFF')),
                );
                return Padding(
                  padding: const EdgeInsets.all(16),
                  child: Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          accent.withOpacity(0.15),
                          Colors.white,
                          const Color(0xFFFDF4FF),
                        ],
                      ),
                      borderRadius: BorderRadius.circular(24),
                      border: Border.all(color: accent.withOpacity(0.4), width: 1.5),
                      boxShadow: [
                        BoxShadow(
                          color: accent.withOpacity(0.12),
                          blurRadius: 20,
                          offset: const Offset(0, 10),
                        ),
                      ],
                    ),
                    padding: const EdgeInsets.all(22),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: accent,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text('Card ${s['n'] ?? i + 1}',
                              style: const TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w900)),
                        ),
                        const SizedBox(height: 16),
                        Text('${s['heading']}',
                            style: const TextStyle(
                                fontSize: 22,
                                fontWeight: FontWeight.w900,
                                height: 1.25)),
                        const SizedBox(height: 14),
                        Expanded(
                          child: SingleChildScrollView(
                            child: Text('${s['body']}',
                                style: const TextStyle(
                                    fontSize: 16.5,
                                    height: 1.5,
                                    fontWeight: FontWeight.w600)),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: page == 0
                          ? null
                          : () => _ctrl.previousPage(
                              duration: const Duration(milliseconds: 250),
                              curve: Curves.easeOut),
                      child: const Text('Back'),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: FilledButton(
                      onPressed: page >= slides.length - 1
                          ? () => Navigator.pop(context)
                          : () => _ctrl.nextPage(
                              duration: const Duration(milliseconds: 250),
                              curve: Curves.easeOut),
                      child: Text(
                          page >= slides.length - 1 ? 'Done' : 'Next'),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
