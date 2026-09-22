import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';

class MatricPracticeScreen extends StatefulWidget {
  const MatricPracticeScreen({
    super.key,
    this.subjectFilter,
    this.yearFilter,
    this.grade,
    this.unitNumber,
    this.title,
  });

  final String? subjectFilter;
  final int? yearFilter;
  final String? grade;
  final int? unitNumber;
  final String? title;

  @override
  State<MatricPracticeScreen> createState() => _MatricPracticeScreenState();
}

class _MatricPracticeScreenState extends State<MatricPracticeScreen> {
  List<MatricQuestion> items = const [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final b = await ContentRepository.instance.matricBundle();
      var list = b.questions;
      if (widget.subjectFilter != null && widget.subjectFilter != 'ALL') {
        final s = widget.subjectFilter!.toUpperCase();
        list = list.where((q) => q.subject == s).toList();
      }
      if (widget.yearFilter != null) {
        list = list.where((q) => q.year == widget.yearFilter).toList();
      }
      if (widget.unitNumber != null) {
        final unitHit = list
            .where((q) =>
                q.unitLinks.any((u) => u.unitNumber == widget.unitNumber))
            .toList();
        // Prefer unit-linked, but fall back to full subject list if too thin
        if (unitHit.length >= 3) {
          list = unitHit;
        }
      }
      // Deduplicate by prompt (keep first with year > 0 preferred)
      final seen = <String>{};
      final dedup = <MatricQuestion>[];
      final sorted = [...list]..sort((a, b) {
          final y = b.year.compareTo(a.year);
          if (y != 0) return y;
          return a.number.compareTo(b.number);
        });
      for (final q in sorted) {
        final key = q.prompt.trim().toLowerCase();
        if (key.isEmpty || seen.contains(key)) continue;
        seen.add(key);
        dedup.add(q);
      }
      dedup.sort((a, b) {
        final y = b.year.compareTo(a.year);
        if (y != 0) return y;
        return a.number.compareTo(b.number);
      });
      if (mounted) {
        setState(() {
          items = dedup;
          loading = false;
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          items = const [];
          loading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final title = widget.title ??
        (widget.subjectFilter != null && widget.yearFilter != null
            ? '${widget.subjectFilter!.replaceAll('_', ' ')} ${widget.yearFilter}'
            : widget.subjectFilter != null
                ? widget.subjectFilter!.replaceAll('_', ' ')
                : 'Matriculation');
    return Scaffold(
      appBar: AppBar(
        title: Text(title,
            style: const TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : items.isEmpty
              ? const Center(
                  child: Padding(
                    padding: EdgeInsets.all(24),
                    child: Text(
                      'No interactive questions for this paper yet.\n'
                      'More years are being parsed into the bank.',
                      textAlign: TextAlign.center,
                    ),
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(12),
                  itemCount: items.length,
                  itemBuilder: (context, i) {
                    final q = items[i];
                    final yearLabel =
                        q.year > 0 ? 'Matric ${q.year}' : 'Matric';
                    return Card(
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: FourTheme.primarySoft,
                          child: Text(
                            'Q${q.number == 0 ? i + 1 : q.number}',
                            style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w800,
                              color: FourTheme.primaryDark,
                            ),
                          ),
                        ),
                        title: Text(
                          q.prompt,
                          maxLines: 3,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontWeight: FontWeight.w600),
                        ),
                        subtitle: Text(
                          '$yearLabel · ${q.subject.replaceAll('_', ' ')}'
                          '${q.section.isNotEmpty ? ' · ${q.section}' : ''}',
                          style: const TextStyle(
                            fontWeight: FontWeight.w700,
                            color: Color(0xFF0D9488),
                          ),
                        ),
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => _QuestionDetail(q: q),
                          ),
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}

class _QuestionDetail extends StatelessWidget {
  const _QuestionDetail({required this.q});
  final MatricQuestion q;

  @override
  Widget build(BuildContext context) {
    final yearLabel = q.year > 0 ? 'Matric ${q.year}' : 'Matric';
    return Scaffold(
      appBar: AppBar(
        title: Text('$yearLabel · ${q.subject} · Q${q.number}'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: const Color(0xFFCCFBF1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              '$yearLabel · ${q.subject.replaceAll('_', ' ')}'
              '${q.section.isNotEmpty ? ' · ${q.section}' : ''}',
              style: const TextStyle(
                fontWeight: FontWeight.w900,
                color: Color(0xFF0F766E),
              ),
            ),
          ),
          const SizedBox(height: 12),
          Text(q.prompt,
              style:
                  const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          ...List.generate(q.options.length, (i) {
            final selected = i == q.correctIndex;
            return Card(
              color: selected ? const Color(0xFFCCFBF1) : null,
              child: ListTile(
                leading: Text(String.fromCharCode(65 + i),
                    style: const TextStyle(fontWeight: FontWeight.w900)),
                title: Text(q.options[i]),
              ),
            );
          }),
          if (q.explanationSteps.isNotEmpty ||
              q.correctAnswerText.isNotEmpty) ...[
            const SizedBox(height: 16),
            const Text('Explanation',
                style: TextStyle(fontWeight: FontWeight.w900)),
            const SizedBox(height: 8),
            Text(q.explanationJoined.isEmpty
                ? q.correctAnswerText
                : q.explanationJoined),
          ],
          if (q.similarQuestions.isNotEmpty) ...[
            const SizedBox(height: 16),
            const Text('Similar questions',
                style: TextStyle(fontWeight: FontWeight.w900)),
            ...q.similarQuestions.map((s) {
              final letter = s.correctIndex >= 0 && s.correctIndex < 26
                  ? String.fromCharCode(65 + s.correctIndex)
                  : '?';
              final ans = (s.correctIndex >= 0 &&
                      s.correctIndex < s.options.length)
                  ? s.options[s.correctIndex]
                  : '';
              return Card(
                margin: const EdgeInsets.only(top: 8),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(s.prompt,
                          style:
                              const TextStyle(fontWeight: FontWeight.w700)),
                      const SizedBox(height: 8),
                      ...List.generate(s.options.length, (i) {
                        final sel = i == s.correctIndex;
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: Text(
                            '${String.fromCharCode(65 + i)}. ${s.options[i]}',
                            style: TextStyle(
                              fontWeight:
                                  sel ? FontWeight.w900 : FontWeight.w500,
                              color: sel
                                  ? const Color(0xFF0D9488)
                                  : const Color(0xFF0F172A),
                            ),
                          ),
                        );
                      }),
                      const SizedBox(height: 6),
                      Text('Answer: ($letter) $ans',
                          style: const TextStyle(
                              fontWeight: FontWeight.w900,
                              color: Color(0xFF0D9488))),
                      if (s.explanation.isNotEmpty) ...[
                        const SizedBox(height: 4),
                        Text('Explanation: ${s.explanation}',
                            style: const TextStyle(height: 1.35)),
                      ],
                    ],
                  ),
                ),
              );
            }),
          ],
          if (q.unitLinks.isNotEmpty) ...[
            const SizedBox(height: 16),
            const Text('Linked units',
                style: TextStyle(fontWeight: FontWeight.w900)),
            ...q.unitLinks.map((u) => Text(
                '• ${u.grade} ${u.subject} Unit ${u.unitNumber} ${u.unitTitleHint}')),
          ],
        ],
      ),
    );
  }
}
