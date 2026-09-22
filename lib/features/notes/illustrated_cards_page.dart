import 'package:flutter/material.dart';

/// Neon / study-poster style illustrated lesson cards.
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

  Color _accent(Map<String, dynamic> s) {
    final raw = (s['accent'] as String? ?? '#22D3EE').replaceFirst('#', '');
    try {
      return Color(int.parse('FF$raw', radix: 16));
    } catch (_) {
      return const Color(0xFF22D3EE);
    }
  }

  bool _isFormula(String text) {
    final t = text.trim();
    if (t.length > 48) return false;
    return t.contains('=') ||
        t.contains('→') ||
        t.contains('∝') ||
        RegExp(r'\b(F|V|I|P|KE|PE|pH|sin|cos|log)\b').hasMatch(t);
  }

  @override
  Widget build(BuildContext context) {
    final slides = widget.slides;
    return Scaffold(
      backgroundColor: const Color(0xFF0B1020),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0B1020),
        foregroundColor: Colors.white,
        elevation: 0,
        title: Text(
          widget.title,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontWeight: FontWeight.w900, letterSpacing: 0.3),
        ),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    widget.subtitle,
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.55),
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: const Color(0xFF22D3EE).withOpacity(0.15),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(
                        color: const Color(0xFF22D3EE).withOpacity(0.4)),
                  ),
                  child: Text(
                    '${page + 1} / ${slides.length}',
                    style: const TextStyle(
                      color: Color(0xFF22D3EE),
                      fontWeight: FontWeight.w900,
                      fontSize: 12,
                    ),
                  ),
                ),
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
                final accent = _accent(s);
                final heading = '${s['heading'] ?? s['title'] ?? 'Key idea'}';
                final body = '${s['body'] ?? s['text'] ?? ''}';
                final formula = _isFormula(body) || _isFormula(heading);
                return Padding(
                  padding: const EdgeInsets.fromLTRB(14, 4, 14, 12),
                  child: Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          const Color(0xFF121A2F),
                          Color.lerp(const Color(0xFF121A2F), accent, 0.12)!,
                          const Color(0xFF0B1020),
                        ],
                      ),
                      borderRadius: BorderRadius.circular(28),
                      border: Border.all(
                          color: accent.withOpacity(0.55), width: 1.6),
                      boxShadow: [
                        BoxShadow(
                          color: accent.withOpacity(0.22),
                          blurRadius: 28,
                          offset: const Offset(0, 12),
                        ),
                      ],
                    ),
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: accent.withOpacity(0.18),
                            borderRadius: BorderRadius.circular(999),
                            border: Border.all(color: accent.withOpacity(0.7)),
                            boxShadow: [
                              BoxShadow(
                                color: accent.withOpacity(0.35),
                                blurRadius: 12,
                              ),
                            ],
                          ),
                          child: Text(
                            heading.toUpperCase(),
                            style: TextStyle(
                              color: accent,
                              fontWeight: FontWeight.w900,
                              fontSize: 12,
                              letterSpacing: 1.1,
                            ),
                          ),
                        ),
                        const SizedBox(height: 18),
                        if (formula) ...[
                          Container(
                            width: double.infinity,
                            padding: const EdgeInsets.symmetric(
                                horizontal: 16, vertical: 14),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.35),
                              borderRadius: BorderRadius.circular(16),
                              border: Border.all(
                                  color: accent.withOpacity(0.5), width: 1.2),
                            ),
                            child: Text(
                              body.isEmpty ? heading : body,
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: accent,
                                fontWeight: FontWeight.w900,
                                fontSize: 22,
                                height: 1.25,
                                letterSpacing: 0.4,
                              ),
                            ),
                          ),
                          const SizedBox(height: 16),
                        ],
                        Expanded(
                          child: SingleChildScrollView(
                            child: Text(
                              formula && body.isNotEmpty && body != heading
                                  ? body
                                  : (body.isEmpty ? heading : body),
                              style: TextStyle(
                                color: Colors.white.withOpacity(0.92),
                                fontSize: formula ? 15 : 17,
                                height: 1.45,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: List.generate(slides.length, (di) {
                            final on = di == page;
                            return AnimatedContainer(
                              duration: const Duration(milliseconds: 200),
                              margin: const EdgeInsets.symmetric(horizontal: 3),
                              width: on ? 18 : 7,
                              height: 7,
                              decoration: BoxDecoration(
                                color: on
                                    ? accent
                                    : Colors.white.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(99),
                              ),
                            );
                          }),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          SafeArea(
            top: false,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
              child: Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: page == 0
                          ? null
                          : () => _ctrl.previousPage(
                                duration: const Duration(milliseconds: 280),
                                curve: Curves.easeOut,
                              ),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: Colors.white,
                        side: BorderSide(
                            color: Colors.white.withOpacity(0.25)),
                        padding: const EdgeInsets.symmetric(vertical: 14),
                      ),
                      icon: const Icon(Icons.chevron_left),
                      label: const Text('Back'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: FilledButton.icon(
                      onPressed: page >= slides.length - 1
                          ? () => Navigator.of(context).maybePop()
                          : () => _ctrl.nextPage(
                                duration: const Duration(milliseconds: 280),
                                curve: Curves.easeOut,
                              ),
                      style: FilledButton.styleFrom(
                        backgroundColor: const Color(0xFF22D3EE),
                        foregroundColor: const Color(0xFF0B1020),
                        padding: const EdgeInsets.symmetric(vertical: 14),
                      ),
                      icon: Icon(page >= slides.length - 1
                          ? Icons.check
                          : Icons.chevron_right),
                      label: Text(
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
