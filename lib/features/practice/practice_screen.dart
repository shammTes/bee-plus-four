import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/theme/four_theme.dart';

/// Adaptive unit practice — grade · subject · unit.
/// Pool = curriculum practice + school/model/matric items linked to that unit.
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
  int? unit;
  List<UnitNote> units = [];
  List<PracticeQuestion> pool = [];
  PracticeQuestion? current;
  int? selected;
  bool revealed = false;
  int sessionCorrect = 0;
  int sessionTotal = 0;

  @override
  void initState() {
    super.initState();
    _loadUnits();
  }

  @override
  void didUpdateWidget(covariant PracticeScreen old) {
    super.didUpdateWidget(old);
    if (old.grade != widget.grade || old.subject != widget.subject) {
      unit = null;
      current = null;
      _loadUnits();
    }
  }

  Future<void> _loadUnits() async {
    final notes =
        await ContentRepository.instance.notesFor(widget.grade, widget.subject);
    if (!mounted) return;
    setState(() {
      units = notes;
      if (units.isNotEmpty && unit == null) unit = units.first.unitNumber;
    });
    if (unit != null) await _loadPool();
  }

  Future<void> _loadPool() async {
    if (unit == null) return;
    final filtered = await ContentRepository.instance.questionsForUnit(
      grade: widget.grade,
      subject: widget.subject,
      unitNumber: unit!,
    );
    if (!mounted) return;
    setState(() {
      pool = filtered;
      current = pool.isEmpty ? null : pool.first;
      selected = null;
      revealed = false;
    });
  }

  Future<void> _next({bool record = false}) async {
    if (record && current != null && selected != null && unit != null) {
      final ok = selected == current!.correctIndex;
      await MasteryStore.instance.record(
        widget.grade,
        widget.subject,
        unit!,
        correct: ok,
      );
      sessionTotal++;
      if (ok) sessionCorrect++;
    }
    if (pool.isEmpty) return;
    final idx = current == null ? 0 : pool.indexOf(current!);
    final next = pool[(idx + 1) % pool.length];
    setState(() {
      current = next;
      selected = null;
      revealed = false;
    });
  }

  Widget _chip(String label, bool sel, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 6),
      child: ChoiceChip(
        label: Text(label),
        selected: sel,
        onSelected: (_) => onTap(),
        selectedColor: const Color(0xFFFBBF24),
        backgroundColor: Colors.white,
        labelStyle: const TextStyle(
          color: Color(0xFF0F172A),
          fontWeight: FontWeight.w900,
          fontSize: 12,
        ),
        side: const BorderSide(color: Color(0xFFE2E8F0)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final subjects = CurriculumStreams.subjectsFor(widget.grade);

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF7C3AED), Color(0xFF6D28D9)],
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
                      fontWeight: FontWeight.w900)),
              const Text('Unit mastery · includes school exam items',
                  style: TextStyle(color: Color(0xFFE9D5FF), fontSize: 13)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) =>
                          _chip(g, g == widget.grade, () => widget.onGrade(g)))
                      .toList(),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects
                      .map((s) => _chip(
                            CurriculumStreams.label(s),
                            s == widget.subject,
                            () => widget.onSubject(s),
                          ))
                      .toList(),
                ),
              ),
              if (units.isNotEmpty) ...[
                const SizedBox(height: 6),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: units.map((u) {
                      final sel = unit == u.unitNumber;
                      return _chip(
                        'U${u.unitNumber}',
                        sel,
                        () async {
                          setState(() => unit = u.unitNumber);
                          await _loadPool();
                        },
                      );
                    }).toList(),
                  ),
                ),
              ],
            ],
          ),
        ),
        Expanded(
          child: current == null
              ? Center(
                  child: Text(
                    units.isEmpty
                        ? 'No units for this subject yet'
                        : 'No questions for this unit yet',
                    style: const TextStyle(color: FourTheme.muted),
                  ),
                )
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    Text(
                      '${pool.length} questions · session $sessionCorrect/$sessionTotal',
                      style: const TextStyle(
                          color: FourTheme.muted,
                          fontWeight: FontWeight.w700),
                    ),
                    const SizedBox(height: 12),
                    Text(current!.prompt,
                        style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w700,
                            height: 1.4)),
                    const SizedBox(height: 14),
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
                              child: Text(
                                '${String.fromCharCode(65 + i)}. ${current!.options[i]}',
                                style: const TextStyle(
                                    fontWeight: FontWeight.w600),
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
                        Padding(
                          padding: const EdgeInsets.only(bottom: 12),
                          child: Text(current!.explanation,
                              style: const TextStyle(height: 1.4)),
                        ),
                      FilledButton(
                        onPressed: () => _next(record: true),
                        child: const Text('Next question'),
                      ),
                    ],
                  ],
                ),
        ),
      ],
    );
  }
}
