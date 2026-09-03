import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';

class PracticeScreen extends StatefulWidget {
  const PracticeScreen({
    super.key,
    required this.grade,
    required this.subject,
    required this.onGrade,
    required this.onSubject,
  });

  final String grade;
  final String subject;
  final ValueChanged<String> onGrade;
  final ValueChanged<String> onSubject;

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  static const subjects = [
    'MATH', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'ENGLISH',
    'GEOGRAPHY', 'HISTORY', 'AGRICULTURE', 'BUSINESS_ECONOMICS',
  ];

  int index = 0;
  int? selected;
  bool revealed = false;
  List<PracticeQuestion> questions = const [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void didUpdateWidget(covariant PracticeScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.grade != widget.grade || oldWidget.subject != widget.subject) {
      _load();
    }
  }

  Future<void> _load() async {
    setState(() {
      loading = true;
      index = 0;
      selected = null;
      revealed = false;
    });
    final list = await ContentRepository.instance
        .questionsFor(widget.grade, widget.subject);
    if (!mounted) return;
    setState(() {
      questions = list;
      loading = false;
    });
  }

  void _next() {
    if (questions.isEmpty) return;
    setState(() {
      index = (index + 1) % questions.length;
      selected = null;
      revealed = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final q = questions.isEmpty ? null : questions[index.clamp(0, questions.length - 1)];

    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFFE0E7FF), Color(0xFFF8FAFC)],
        ),
      ),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF4F46E5), Color(0xFF6366F1)],
              ),
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(24),
                bottomRight: Radius.circular(24),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Practice',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                        fontWeight: FontWeight.w800)),
                const SizedBox(height: 2),
                const Text('MCQs · instant feedback',
                    style: TextStyle(color: Color(0xFFE0E7FF), fontSize: 13)),
                const SizedBox(height: 12),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: ['G9', 'G10', 'G11', 'G12'].map((g) {
                      final sel = g == widget.grade;
                      return Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: ChoiceChip(
                          label: Text(g),
                          selected: sel,
                          onSelected: (_) => widget.onGrade(g),
                          selectedColor: const Color(0xFFFBBF24),
                          labelStyle: const TextStyle(
                            color: Color(0xFF0F172A),
                            fontWeight: FontWeight.w900,
                            fontSize: 12,
                          ),
                          backgroundColor: Colors.white,
                          side: const BorderSide(color: Color(0xFFE2E8F0)),
                          visualDensity: VisualDensity.compact,
                        ),
                      );
                    }).toList(),
                  ),
                ),
                const SizedBox(height: 8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: subjects.map((s) {
                      final sel = s == widget.subject;
                      final label = s == 'BUSINESS_ECONOMICS'
                          ? 'Business'
                          : s[0] + s.substring(1).toLowerCase();
                      return Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: FilterChip(
                          label: Text(label),
                          selected: sel,
                          onSelected: (_) => widget.onSubject(s),
                          selectedColor: const Color(0xFFFBBF24),
                          labelStyle: const TextStyle(
                            color: Color(0xFF0F172A),
                            fontWeight: FontWeight.w900,
                            fontSize: 11,
                          ),
                          backgroundColor: Colors.white,
                          side: const BorderSide(color: Color(0xFFE2E8F0)),
                          visualDensity: VisualDensity.compact,
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ],
            ),
          ),
          if (loading)
            const Expanded(child: Center(child: CircularProgressIndicator()))
          else if (q == null)
            const Expanded(
              child: Center(
                child: Text('No questions for this filter yet.',
                    style: TextStyle(color: FourTheme.muted)),
              ),
            )
          else
            Expanded(
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  Text(
                    '${index + 1} / ${questions.length}',
                    style: const TextStyle(
                        color: FourTheme.muted, fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 10),
                  FourTheme.glassPanel(
                    child: Text(q.prompt,
                        style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                            height: 1.35)),
                  ),
                  const SizedBox(height: 12),
                  ...List.generate(q.options.length, (i) {
                    final isSel = selected == i;
                    final isCorrect = revealed && i == q.correctIndex;
                    final isWrong = revealed && isSel && i != q.correctIndex;
                    Color bg = Colors.white;
                    Color border = const Color(0xFFE2E8F0);
                    if (isCorrect) {
                      bg = const Color(0xFFD1FAE5);
                      border = const Color(0xFF059669);
                    } else if (isWrong) {
                      bg = const Color(0xFFFEE2E2);
                      border = const Color(0xFFDC2626);
                    } else if (isSel) {
                      bg = const Color(0xFFEEF2FF);
                      border = const Color(0xFF4F46E5);
                    }
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 8),
                      child: Material(
                        color: bg,
                        borderRadius: BorderRadius.circular(14),
                        child: InkWell(
                          borderRadius: BorderRadius.circular(14),
                          onTap: revealed
                              ? null
                              : () => setState(() {
                                    selected = i;
                                    revealed = true;
                                  }),
                          child: Container(
                            padding: const EdgeInsets.all(14),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(14),
                              border: Border.all(color: border),
                            ),
                            child: Text(
                              '${String.fromCharCode(65 + i)}. ${q.options[i]}',
                              style: const TextStyle(
                                fontWeight: FontWeight.w600,
                                color: Color(0xFF0F172A),
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }),
                  if (revealed) ...[
                    const SizedBox(height: 8),
                    FourTheme.glassPanel(
                      child: Text(
                        q.explanation.isEmpty
                            ? 'Answer: ${String.fromCharCode(65 + q.correctIndex)}'
                            : q.explanation,
                        style: const TextStyle(
                            height: 1.4, color: Color(0xFF0F172A)),
                      ),
                    ),
                    const SizedBox(height: 12),
                    FilledButton(
                      onPressed: _next,
                      child: const Text('Next question'),
                    ),
                  ],
                ],
              ),
            ),
        ],
      ),
    );
  }
}
