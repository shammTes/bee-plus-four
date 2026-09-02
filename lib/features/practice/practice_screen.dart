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

  List<PracticeQuestion> items = const [];
  int index = 0;
  int? selected;
  bool revealed = false;
  int correct = 0;
  int answered = 0;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void didUpdateWidget(covariant PracticeScreen old) {
    super.didUpdateWidget(old);
    if (old.grade != widget.grade || old.subject != widget.subject) {
      _load();
    }
  }

  Future<void> _load() async {
    setState(() {
      loading = true;
      index = 0;
      selected = null;
      revealed = false;
      correct = 0;
      answered = 0;
    });
    final list = await ContentRepository.instance.questionsFor(
      widget.grade,
      widget.subject,
    );
    if (!mounted) return;
    setState(() {
      items = list;
      loading = false;
    });
  }

  void _pick(int i) {
    if (revealed) return;
    setState(() {
      selected = i;
      revealed = true;
      answered++;
      if (i == items[index].correctIndex) correct++;
    });
  }

  void _next() {
    if (index >= items.length - 1) return;
    setState(() {
      index++;
      selected = null;
      revealed = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final total = items.length;
    final progress = total == 0 ? 0.0 : (index + (revealed ? 1 : 0)) / total;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF2563EB), Color(0xFF1D4ED8)],
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
              const SizedBox(height: 4),
              Text(
                answered == 0
                    ? 'MCQs with explanations'
                    : 'Score $correct / $answered',
                style: const TextStyle(color: Color(0xFFDBEAFE), fontSize: 13),
              ),
              const SizedBox(height: 12),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11'].map((g) {
                    final sel = g == widget.grade;
                    return Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: ChoiceChip(
                        label: Text(g),
                        selected: sel,
                        onSelected: (_) => widget.onGrade(g),
                        selectedColor: Colors.white,
                        labelStyle: TextStyle(
                          color: sel ? const Color(0xFF1D4ED8) : Colors.white,
                          fontWeight: FontWeight.w700,
                          fontSize: 12,
                        ),
                        backgroundColor: Colors.white.withOpacity(0.15),
                        side: BorderSide.none,
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
                        selectedColor: Colors.white,
                        labelStyle: TextStyle(
                          color: sel ? const Color(0xFF1D4ED8) : Colors.white,
                          fontWeight: FontWeight.w600,
                          fontSize: 11,
                        ),
                        backgroundColor: Colors.white.withOpacity(0.12),
                        side: BorderSide.none,
                        visualDensity: VisualDensity.compact,
                      ),
                    );
                  }).toList(),
                ),
              ),
              if (total > 0) ...[
                const SizedBox(height: 12),
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: LinearProgressIndicator(
                    value: progress.clamp(0.0, 1.0),
                    minHeight: 6,
                    backgroundColor: Colors.white24,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Question ${index + 1} of $total',
                  style: const TextStyle(color: Colors.white70, fontSize: 11),
                ),
              ],
            ],
          ),
        ),
        if (loading)
          const Expanded(child: Center(child: CircularProgressIndicator()))
        else if (items.isEmpty)
          const Expanded(
            child: Center(
              child: Padding(
                padding: EdgeInsets.all(24),
                child: Text(
                  'No practice questions for this grade/subject yet.',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: FourTheme.muted),
                ),
              ),
            ),
          )
        else
          Expanded(child: _buildQuestion(items[index])),
      ],
    );
  }

  Widget _buildQuestion(PracticeQuestion q) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              q.prompt,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
                height: 1.35,
                color: FourTheme.ink,
              ),
            ),
          ),
        ),
        const SizedBox(height: 12),
        ...List.generate(q.options.length, (i) {
          final isSel = selected == i;
          final isCorrect = i == q.correctIndex;
          Color? bg;
          Color border = const Color(0xFFE2E8F0);
          if (revealed) {
            if (isCorrect) {
              bg = const Color(0xFFD1FAE5);
              border = const Color(0xFF10B981);
            } else if (isSel && !isCorrect) {
              bg = const Color(0xFFFEE2E2);
              border = const Color(0xFFEF4444);
            }
          } else if (isSel) {
            bg = FourTheme.primarySoft;
            border = FourTheme.primary;
          }
          return Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Material(
              color: bg ?? Colors.white,
              borderRadius: BorderRadius.circular(14),
              child: InkWell(
                onTap: () => _pick(i),
                borderRadius: BorderRadius.circular(14),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: border, width: 1.4),
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 14,
                        backgroundColor: revealed && isCorrect
                            ? const Color(0xFF10B981)
                            : (revealed && isSel
                                ? const Color(0xFFEF4444)
                                : FourTheme.primarySoft),
                        child: Text(
                          String.fromCharCode(65 + i),
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w800,
                            color: revealed && (isCorrect || isSel)
                                ? Colors.white
                                : FourTheme.primaryDark,
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(child: Text(q.options[i])),
                      if (revealed && isCorrect)
                        const Icon(Icons.check_circle, color: Color(0xFF10B981), size: 20),
                      if (revealed && isSel && !isCorrect)
                        const Icon(Icons.cancel, color: Color(0xFFEF4444), size: 20),
                    ],
                  ),
                ),
              ),
            ),
          );
        }),
        if (revealed) ...[
          const SizedBox(height: 8),
          Card(
            color: const Color(0xFFF8FAFC),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        selected == q.correctIndex
                            ? Icons.celebration_outlined
                            : Icons.lightbulb_outline,
                        color: selected == q.correctIndex
                            ? const Color(0xFF10B981)
                            : FourTheme.accent,
                        size: 20,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        selected == q.correctIndex ? 'Correct' : 'Explanation',
                        style: const TextStyle(fontWeight: FontWeight.w800),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(
                    q.explanation.isEmpty ? 'No explanation in pack.' : q.explanation,
                    style: const TextStyle(height: 1.4, color: FourTheme.ink),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: OutlinedButton(
                  onPressed: index > 0
                      ? () => setState(() {
                            index--;
                            selected = null;
                            revealed = false;
                          })
                      : null,
                  child: const Text('Previous'),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FilledButton(
                  onPressed: index < items.length - 1 ? _next : null,
                  child: Text(index < items.length - 1 ? 'Next' : 'Done'),
                ),
              ),
            ],
          ),
        ],
        const SizedBox(height: 24),
      ],
    );
  }
}
