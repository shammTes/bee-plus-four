import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/models/content_models.dart';
import '../../core/models/exam_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/progress/study_log.dart';
import '../../core/theme/four_theme.dart';

enum PracticeSource { mixed, matricOnly }

/// Multi grade / subject / unit practice with mixed or matric-only sources.
class MultiPracticePage extends StatefulWidget {
  const MultiPracticePage({super.key, this.initialGrade = 'G11'});

  final String initialGrade;

  @override
  State<MultiPracticePage> createState() => _MultiPracticePageState();
}

class _MultiPracticePageState extends State<MultiPracticePage> {
  final Set<String> grades = {};
  final Set<String> subjects = {};
  final Set<String> unitKeys = {}; // "G11|MATH|2"
  PracticeSource source = PracticeSource.mixed;
  List<UnitNote> allNotes = [];
  List<PracticeQuestion> pool = [];
  PracticeQuestion? current;
  int? selected;
  bool revealed = false;
  bool loading = true;
  bool session = false;
  int sessionCorrect = 0;
  int sessionTotal = 0;

  @override
  void initState() {
    super.initState();
    grades.add(widget.initialGrade);
    subjects.add('MATH');
    _loadNotes();
  }

  Future<void> _loadNotes() async {
    final notes = await ContentRepository.instance.notes();
    if (!mounted) return;
    setState(() {
      allNotes = notes;
      loading = false;
    });
  }

  List<UnitNote> get visibleUnits {
    return allNotes
        .where((n) =>
            (grades.isEmpty || grades.contains(n.grade)) &&
            (subjects.isEmpty || subjects.contains(n.subject)))
        .toList()
      ..sort((a, b) {
        final g = a.grade.compareTo(b.grade);
        if (g != 0) return g;
        final s = a.subject.compareTo(b.subject);
        if (s != 0) return s;
        return a.unitNumber.compareTo(b.unitNumber);
      });
  }

  String _uk(UnitNote n) => '${n.grade}|${n.subject}|${n.unitNumber}';

  Future<void> _start() async {
    setState(() {
      loading = true;
      session = true;
    });
    final byId = <String, PracticeQuestion>{};
    final repo = ContentRepository.instance;

    final targets = unitKeys.isEmpty
        ? visibleUnits.map(_uk).toSet()
        : unitKeys;

    if (source == PracticeSource.mixed) {
      for (final key in targets) {
        final parts = key.split('|');
        if (parts.length != 3) continue;
        final g = parts[0];
        final s = parts[1];
        final u = int.tryParse(parts[2]) ?? 1;
        final qs = await repo.questionsForUnit(
            grade: g, subject: s, unitNumber: u);
        for (final q in qs) {
          byId[q.id] = q;
        }
      }
    }

    // Matric / model / school from bank for selected subjects (and units if set)
    final bank = await repo.matricBundle();
    for (final m in bank.questions) {
      if (subjects.isNotEmpty && !subjects.contains(m.subject)) continue;
      if (source == PracticeSource.matricOnly && m.examType != 'matriculation') {
        continue;
      }
      if (source == PracticeSource.mixed && m.examType == 'matriculation') {
        // already may be pulled via unit links; still allow subject-wide matric
      }
      if (unitKeys.isNotEmpty) {
        final ok = m.unitLinks.any((ul) {
          final k = '${ul.grade.isEmpty ? '' : ul.grade}|${m.subject}|${ul.unitNumber}';
          // match any grade if unit+subject in selection
          return unitKeys.any((sel) {
            final p = sel.split('|');
            return p.length == 3 &&
                p[1] == m.subject &&
                p[2] == '${ul.unitNumber}';
          }) || unitKeys.contains(k);
        });
        if (!ok && source == PracticeSource.matricOnly) {
          // matric-only without unit filter: allow all for subject
          if (unitKeys.isNotEmpty) {
            // still require subject match only when no unit overlap
            final hasSubjectUnit = unitKeys.any((sel) => sel.contains('|${m.subject}|'));
            if (!hasSubjectUnit) continue;
            if (!ok) continue;
          }
        } else if (!ok && source == PracticeSource.mixed) {
          continue;
        }
      }
      if (m.options.length < 3) continue;
      byId.putIfAbsent(
        m.id,
        () => PracticeQuestion(
          id: m.id,
          grade: m.unitLinks.isNotEmpty
              ? (m.unitLinks.first.grade.isEmpty
                  ? widget.initialGrade
                  : m.unitLinks.first.grade)
              : widget.initialGrade,
          subject: m.subject,
          unitNumber: m.unitLinks.isNotEmpty
              ? m.unitLinks.first.unitNumber
              : 0,
          prompt: m.prompt,
          options: m.options,
          correctIndex: m.correctIndex < 0 ? 0 : m.correctIndex,
          explanation: m.explanationJoined.isEmpty
              ? (m.correctIndex < 0
                  ? 'Answer key not verified yet.'
                  : '')
              : m.explanationJoined,
        ),
      );
    }

    // Matric-only: if still empty, all matric for subjects
    if (source == PracticeSource.matricOnly && byId.isEmpty) {
      for (final m in bank.questions) {
        if (m.examType != 'matriculation') continue;
        if (subjects.isNotEmpty && !subjects.contains(m.subject)) continue;
        if (m.options.length < 3) continue;
        byId[m.id] = PracticeQuestion(
          id: m.id,
          grade: widget.initialGrade,
          subject: m.subject,
          unitNumber: 0,
          prompt: m.prompt,
          options: m.options,
          correctIndex: m.correctIndex < 0 ? 0 : m.correctIndex,
          explanation: m.explanationJoined,
        );
      }
    }

    final list = byId.values.toList()..shuffle();
    if (!mounted) return;
    setState(() {
      pool = list;
      current = pool.isEmpty ? null : pool.first;
      selected = null;
      revealed = false;
      loading = false;
      sessionCorrect = 0;
      sessionTotal = 0;
    });
  }

  Future<void> _next({bool record = false}) async {
    if (record && current != null && selected != null) {
      final ok = selected == current!.correctIndex;
      await MasteryStore.instance.record(
        current!.grade,
        current!.subject,
        current!.unitNumber == 0 ? 1 : current!.unitNumber,
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
    final dark = Theme.of(context).brightness == Brightness.dark;

    if (session && !loading) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Multi practice',
              style: TextStyle(fontWeight: FontWeight.w800)),
          actions: [
            TextButton(
              onPressed: () => setState(() {
                session = false;
                current = null;
              }),
              child: const Text('Setup'),
            ),
          ],
        ),
        body: current == null
            ? const Center(child: Text('No questions for this selection.'))
            : ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  Text(
                    '${pool.length} questions · $sessionCorrect/$sessionTotal correct',
                    style: TextStyle(
                      color: dark ? FourTheme.darkMuted : FourTheme.muted,
                      fontWeight: FontWeight.w700,
                    ),
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
                    Color border = dark
                        ? FourTheme.darkBorder
                        : const Color(0xFFE2E8F0);
                    Color bg = dark ? FourTheme.darkCard : Colors.white;
                    if (isCorrect) {
                      border = const Color(0xFF10B981);
                      bg = dark
                          ? const Color(0xFF064E3B)
                          : const Color(0xFFECFDF5);
                    } else if (isWrong) {
                      border = const Color(0xFFEF4444);
                      bg = dark
                          ? const Color(0xFF7F1D1D)
                          : const Color(0xFFFEF2F2);
                    } else if (isSel) {
                      border = FourTheme.violet;
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
                              border: Border.all(color: border, width: 1.5),
                            ),
                            child: Text(
                              '${String.fromCharCode(65 + i)}. ${current!.options[i]}',
                              style:
                                  const TextStyle(fontWeight: FontWeight.w600),
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
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Multi practice',
            style: TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                const Text('Grades',
                    style: TextStyle(fontWeight: FontWeight.w900)),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 6,
                  children: ['G9', 'G10', 'G11', 'G12'].map((g) {
                    final sel = grades.contains(g);
                    return FilterChip(
                      label: Text(g),
                      selected: sel,
                      onSelected: (v) => setState(() {
                        if (v) {
                          grades.add(g);
                        } else {
                          grades.remove(g);
                        }
                      }),
                    );
                  }).toList(),
                ),
                const SizedBox(height: 16),
                const Text('Subjects',
                    style: TextStyle(fontWeight: FontWeight.w900)),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: CurriculumStreams.juniorCore.map((s) {
                    final sel = subjects.contains(s);
                    return FilterChip(
                      label: Text(CurriculumStreams.label(s)),
                      selected: sel,
                      onSelected: (v) => setState(() {
                        if (v) {
                          subjects.add(s);
                        } else {
                          subjects.remove(s);
                        }
                      }),
                    );
                  }).toList()
                    ..addAll(['AGRICULTURE'].map((s) {
                      final sel = subjects.contains(s);
                      return FilterChip(
                        label: Text(CurriculumStreams.label(s)),
                        selected: sel,
                        onSelected: (v) => setState(() {
                          if (v) {
                            subjects.add(s);
                          } else {
                            subjects.remove(s);
                          }
                        }),
                      );
                    })),
                ),
                const SizedBox(height: 16),
                const Text('Units (optional — leave empty for all)',
                    style: TextStyle(fontWeight: FontWeight.w900)),
                const SizedBox(height: 8),
                ...visibleUnits.take(40).map((n) {
                  final k = _uk(n);
                  final sel = unitKeys.contains(k);
                  return CheckboxListTile(
                    dense: true,
                    value: sel,
                    title: Text(
                      '${n.grade} · ${CurriculumStreams.label(n.subject)} · U${n.unitNumber}',
                      style: const TextStyle(
                          fontWeight: FontWeight.w700, fontSize: 13),
                    ),
                    subtitle: Text(n.title,
                        maxLines: 1, overflow: TextOverflow.ellipsis),
                    onChanged: (v) => setState(() {
                      if (v == true) {
                        unitKeys.add(k);
                      } else {
                        unitKeys.remove(k);
                      }
                    }),
                  );
                }),
                const SizedBox(height: 12),
                const Text('Question source',
                    style: TextStyle(fontWeight: FontWeight.w900)),
                const SizedBox(height: 8),
                SegmentedButton<PracticeSource>(
                  segments: const [
                    ButtonSegment(
                      value: PracticeSource.mixed,
                      label: Text('Mixed'),
                    ),
                    ButtonSegment(
                      value: PracticeSource.matricOnly,
                      label: Text('Matric only'),
                    ),
                  ],
                  selected: {source},
                  onSelectionChanged: (s) =>
                      setState(() => source = s.first),
                ),
                const SizedBox(height: 8),
                Text(
                  source == PracticeSource.matricOnly
                      ? 'Only matriculation exam questions for selected subjects.'
                      : 'Curriculum + school + model + matric linked to selected units.',
                  style: TextStyle(
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                    fontSize: 12,
                  ),
                ),
                const SizedBox(height: 20),
                FilledButton.icon(
                  onPressed: subjects.isEmpty
                      ? null
                      : () => _start(),
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Start practice'),
                ),
              ],
            ),
    );
  }
}
