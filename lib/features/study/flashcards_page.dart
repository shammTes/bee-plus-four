import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/theme/four_theme.dart';

/// Flip-style flashcards from unit notes key terms + key ideas.
class FlashcardsPage extends StatefulWidget {
  const FlashcardsPage({
    super.key,
    this.grade = 'G10',
    this.subject = 'MATH',
  });

  final String grade;
  final String subject;

  @override
  State<FlashcardsPage> createState() => _FlashcardsPageState();
}

class _FlashcardsPageState extends State<FlashcardsPage> {
  late String grade;
  late String subject;
  List<Map<String, dynamic>> cards = [];
  int index = 0;
  bool showBack = false;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    grade = widget.grade;
    subject = widget.subject;
    _load();
  }

  Future<void> _load() async {
    setState(() => loading = true);
    final all = await ContentRepository.instance.flashcardsFor(grade, subject);
    if (!mounted) return;
    setState(() {
      cards = all;
      index = 0;
      showBack = false;
      loading = false;
    });
  }

  void _next() {
    if (cards.isEmpty) return;
    setState(() {
      index = (index + 1) % cards.length;
      showBack = false;
    });
  }

  void _prev() {
    if (cards.isEmpty) return;
    setState(() {
      index = (index - 1 + cards.length) % cards.length;
      showBack = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final subjects =
        CurriculumStreams.subjectsFor(grade, stream: CurriculumStreams.science);
    final card = cards.isEmpty ? null : cards[index];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Flashcards',
            style: TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 8, 12, 0),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: ['G9', 'G10', 'G11', 'G12'].map((g) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ChoiceChip(
                      label: Text(g),
                      selected: g == grade,
                      onSelected: (_) {
                        setState(() => grade = g);
                        _load();
                      },
                      selectedColor: const Color(0xFFFBBF24),
                      backgroundColor: Colors.white,
                      labelStyle: const TextStyle(
                        color: Color(0xFF0F172A),
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 6, 12, 8),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: subjects.map((s) {
                  return Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: ChoiceChip(
                      label: Text(CurriculumStreams.label(s)),
                      selected: s == subject,
                      onSelected: (_) {
                        setState(() => subject = s);
                        _load();
                      },
                      selectedColor: const Color(0xFFA5F3FC),
                      backgroundColor: Colors.white,
                      labelStyle: const TextStyle(
                        color: Color(0xFF0F172A),
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                  );
                }).toList(),
              ),
            ),
          ),
          Expanded(
            child: loading
                ? const Center(child: CircularProgressIndicator())
                : card == null
                    ? const Center(
                        child: Text('No flashcards for this selection yet.',
                            style: TextStyle(color: FourTheme.muted)))
                    : Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          children: [
                            Text(
                              '${index + 1} / ${cards.length}',
                              style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                  color: FourTheme.muted),
                            ),
                            const SizedBox(height: 12),
                            Expanded(
                              child: GestureDetector(
                                onTap: () =>
                                    setState(() => showBack = !showBack),
                                child: AnimatedContainer(
                                  duration: const Duration(milliseconds: 200),
                                  width: double.infinity,
                                  padding: const EdgeInsets.all(24),
                                  decoration: BoxDecoration(
                                    gradient: LinearGradient(
                                      colors: showBack
                                          ? [
                                              const Color(0xFF0D9488),
                                              const Color(0xFF0F766E)
                                            ]
                                          : [
                                              const Color(0xFF7C3AED),
                                              const Color(0xFF6D28D9)
                                            ],
                                    ),
                                    borderRadius: BorderRadius.circular(24),
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black.withOpacity(0.15),
                                        blurRadius: 16,
                                        offset: const Offset(0, 8),
                                      ),
                                    ],
                                  ),
                                  child: Center(
                                    child: Text(
                                      showBack
                                          ? '${card['back'] ?? ''}'
                                          : '${card['front'] ?? ''}',
                                      textAlign: TextAlign.center,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontSize: 20,
                                        fontWeight: FontWeight.w800,
                                        height: 1.35,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text('Tap card to flip',
                                style: TextStyle(color: FourTheme.muted)),
                            const SizedBox(height: 12),
                            Row(
                              children: [
                                Expanded(
                                  child: OutlinedButton(
                                    onPressed: _prev,
                                    child: const Text('Previous'),
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Expanded(
                                  child: FilledButton(
                                    onPressed: _next,
                                    child: const Text('Next'),
                                  ),
                                ),
                              ],
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
