import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/progress/study_log.dart';
import '../../core/theme/four_theme.dart';

/// Opens practice for ONE unit directly (from Notes unit hub).
class UnitPracticePage extends StatefulWidget {
  const UnitPracticePage({
    super.key,
    required this.grade,
    required this.subject,
    required this.unitNumber,
    required this.unitTitle,
  });

  final String grade;
  final String subject;
  final int unitNumber;
  final String unitTitle;

  @override
  State<UnitPracticePage> createState() => _UnitPracticePageState();
}

class _UnitPracticePageState extends State<UnitPracticePage> {
  List<PracticeQuestion> pool = [];
  PracticeQuestion? current;
  int? selected;
  bool revealed = false;
  int sessionCorrect = 0;
  int sessionTotal = 0;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final all = await ContentRepository.instance.questions();
    var filtered = all
        .where((q) =>
            q.grade == widget.grade &&
            q.subject == widget.subject &&
            (q.unitNumber == widget.unitNumber || q.unitNumber == 0))
        .toList();
    if (filtered.isEmpty) {
      filtered = all
          .where((q) =>
              q.grade == widget.grade && q.subject == widget.subject)
          .toList();
    }
    if (filtered.isEmpty) {
      filtered = all.where((q) => q.subject == widget.subject).toList();
    }
    filtered.shuffle();
    if (!mounted) return;
    setState(() {
      pool = filtered;
      current = pool.isEmpty ? null : pool.first;
      loading = false;
    });
  }

  Future<void> _next({bool record = false}) async {
    if (record && current != null && selected != null) {
      final ok = selected == current!.correctIndex;
      await MasteryStore.instance.record(
        widget.grade,
        widget.subject,
        widget.unitNumber,
        correct: ok,
      );
      sessionTotal++;
      if (ok) sessionCorrect++;
      await StudyLog.instance.markStudied(minutes: 1);
    }
    if (pool.isEmpty) return;
    final idx = current == null ? 0 : pool.indexOf(current!);
    setState(() {
      current = pool[(idx + 1) % pool.length];
      selected = null;
      revealed = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final mastery = MasteryStore.instance
        .mastery(widget.grade, widget.subject, widget.unitNumber);
    final level = MasteryStore.instance
        .levelLabel(widget.grade, widget.subject, widget.unitNumber);

    return Scaffold(
      appBar: AppBar(
        title: Text('U${widget.unitNumber} · Practice',
            style: const TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : current == null
              ? const Center(
                  child: Padding(
                    padding: EdgeInsets.all(24),
                    child: Text(
                      'No practice questions for this unit yet.\nTry Coach or Exams for related items.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: FourTheme.muted),
                    ),
                  ),
                )
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    Text(widget.unitTitle,
                        style: const TextStyle(
                            fontWeight: FontWeight.w800, fontSize: 15)),
                    const SizedBox(height: 6),
                    Text(
                        '${widget.grade} · ${widget.subject} · $level · session $sessionCorrect/$sessionTotal',
                        style: const TextStyle(
                            color: FourTheme.muted, fontSize: 12)),
                    const SizedBox(height: 8),
                    ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: LinearProgressIndicator(
                        value: mastery == 0 ? null : mastery,
                        minHeight: 6,
                        backgroundColor: const Color(0xFFE2E8F0),
                        color: FourTheme.violet,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Text(current!.prompt,
                        style: const TextStyle(
                            fontSize: 16,
                            height: 1.4,
                            fontWeight: FontWeight.w600)),
                    const SizedBox(height: 16),
                    ...List.generate(current!.options.length, (i) {
                      final isSel = selected == i;
                      final isCorrect =
                          revealed && i == current!.correctIndex;
                      final isWrong =
                          revealed && isSel && i != current!.correctIndex;
                      Color border = const Color(0xFFE2E8F0);
                      Color bg = Colors.white;
                      if (isCorrect) {
                        border = const Color(0xFF10B981);
                        bg = const Color(0xFFECFDF5);
                      } else if (isWrong) {
                        border = const Color(0xFFEF4444);
                        bg = const Color(0xFFFEF2F2);
                      } else if (isSel) {
                        border = FourTheme.violet;
                        bg = const Color(0xFFF5F3FF);
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
                                : () => setState(() => selected = i),
                            child: Container(
                              padding: const EdgeInsets.all(14),
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(14),
                                border:
                                    Border.all(color: border, width: 1.5),
                              ),
                              child: Row(
                                children: [
                                  CircleAvatar(
                                    radius: 14,
                                    backgroundColor:
                                        border.withOpacity(0.2),
                                    child: Text(
                                        String.fromCharCode(65 + i),
                                        style: const TextStyle(
                                            fontWeight: FontWeight.w900,
                                            fontSize: 12)),
                                  ),
                                  const SizedBox(width: 12),
                                  Expanded(
                                    child: Text(current!.options[i],
                                        style: const TextStyle(
                                            fontWeight: FontWeight.w600)),
                                  ),
                                ],
                              ),
                            ),
                          ),
                        ),
                      );
                    }),
                    const SizedBox(height: 12),
                    if (!revealed)
                      FilledButton(
                        onPressed: selected == null
                            ? null
                            : () => setState(() => revealed = true),
                        child: const Text('Check answer'),
                      )
                    else ...[
                      if (current!.explanation.isNotEmpty)
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: const Color(0xFFF8FAFC),
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: Text(current!.explanation,
                              style: const TextStyle(height: 1.4)),
                        ),
                      const SizedBox(height: 12),
                      FilledButton(
                        onPressed: () => _next(record: true),
                        child: const Text('Next question'),
                      ),
                    ],
                  ],
                ),
    );
  }
}
