import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/theme/four_theme.dart';

/// Adaptive unit practice — student picks grade · subject · unit.
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
    final all = await ContentRepository.instance.questions();
    var filtered = all
        .where((q) =>
            q.grade == widget.grade &&
            q.subject == widget.subject &&
            (q.unitNumber == unit || q.unitNumber == 0))
        .toList();
    if (filtered.isEmpty) {
      filtered = all
          .where((q) =>
              q.grade == widget.grade && q.subject == widget.subject)
          .toList();
    }
    if (filtered.isEmpty) {
      filtered =
          all.where((q) => q.subject == widget.subject).toList();
    }
    // Adaptive order: interleave weaker emphasis — shuffle but prefer unseen
    filtered.shuffle();
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
    final mastery = unit == null
        ? 0.0
        : MasteryStore.instance
            .mastery(widget.grade, widget.subject, unit!);
    final level = unit == null
        ? '—'
        : MasteryStore.instance
            .levelLabel(widget.grade, widget.subject, unit!);

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 12),
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
              const Text('Exam prep · topic mastery',
                  style:
                      TextStyle(color: Color(0xFFE9D5FF), fontSize: 13)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) => _chip(g, g == widget.grade, () {
                            widget.onGrade(g);
                          }))
                      .toList(),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects.map((s) {
                    final label = s == 'BUSINESS_ECONOMICS'
                        ? 'Business'
                        : s[0] + s.substring(1).toLowerCase();
                    return _chip(label, s == widget.subject, () {
                      widget.onSubject(s);
                    });
                  }).toList(),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: units.isEmpty
                      ? [
                          _chip('All units', true, () {}),
                        ]
                      : units
                          .map((u) => _chip(
                                'U${u.unitNumber}',
                                unit == u.unitNumber,
                                () async {
                                  setState(() => unit = u.unitNumber);
                                  await _loadPool();
                                },
                              ))
                          .toList(),
                ),
              ),
              if (unit != null) ...[
                const SizedBox(height: 10),
                Row(
                  children: [
                    Expanded(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: LinearProgressIndicator(
                          value: mastery,
                          minHeight: 8,
                          backgroundColor: Colors.white24,
                          color: const Color(0xFFFBBF24),
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    Text(level,
                        style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.w800)),
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  sessionTotal == 0
                      ? 'Answer to build mastery for this unit'
                      : 'Session $sessionCorrect / $sessionTotal correct',
                  style: const TextStyle(
                      color: Color(0xFFE9D5FF), fontSize: 12),
                ),
              ],
            ],
          ),
        ),
        Expanded(child: _buildBody()),
      ],
    );
  }

  Widget _buildBody() {
    if (current == null) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Text(
            'No questions for this filter yet.\nTry another unit or subject.',
            textAlign: TextAlign.center,
            style: TextStyle(color: FourTheme.muted),
          ),
        ),
      );
    }
    final q = current!;
    final unitTitle = units
        .where((u) => u.unitNumber == unit)
        .map((u) => u.title)
        .cast<String?>()
        .firstWhere((_) => true, orElse: () => null);

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (unitTitle != null)
          Text(unitTitle,
              style: const TextStyle(
                  fontWeight: FontWeight.w800,
                  fontSize: 15,
                  color: FourTheme.ink)),
        const SizedBox(height: 8),
        Text(q.prompt,
            style: const TextStyle(
                fontSize: 16, height: 1.4, fontWeight: FontWeight.w600)),
        const SizedBox(height: 16),
        ...List.generate(q.options.length, (i) {
          final isSel = selected == i;
          final isCorrect = revealed && i == q.correctIndex;
          final isWrong = revealed && isSel && i != q.correctIndex;
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
                    border: Border.all(color: border, width: 1.5),
                  ),
                  child: Row(
                    children: [
                      CircleAvatar(
                        radius: 14,
                        backgroundColor: border.withOpacity(0.2),
                        child: Text(String.fromCharCode(65 + i),
                            style: TextStyle(
                                fontWeight: FontWeight.w900,
                                fontSize: 12,
                                color: FourTheme.ink)),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(q.options[i],
                            style: const TextStyle(
                                fontWeight: FontWeight.w600,
                                color: FourTheme.ink)),
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
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFFF8FAFC),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: const Color(0xFFE2E8F0)),
            ),
            child: Text(
              q.explanation.isEmpty
                  ? 'Correct option: ${String.fromCharCode(65 + q.correctIndex)}'
                  : q.explanation,
              style: const TextStyle(height: 1.4),
            ),
          ),
          const SizedBox(height: 12),
          FilledButton(
            onPressed: () => _next(record: true),
            child: const Text('Next question'),
          ),
        ],
      ],
    );
  }
}
