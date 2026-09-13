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
      // Prefer unit-linked questions when unit specified
      if (widget.unitNumber != null) {
        final unitHit = list
            .where((q) => q.unitLinks
                .any((u) => u.unitNumber == widget.unitNumber))
            .toList();
        if (unitHit.isNotEmpty) list = unitHit;
      }
      list.sort((a, b) => a.number.compareTo(b.number));
      if (mounted) {
        setState(() {
          items = list;
          loading = false;
        });
      }
    } catch (_) {
      if (mounted) setState(() {
        items = const [];
        loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    // Title is always Subject + Year when provided
    final title = widget.title ??
        (
          widget.subjectFilter != null && widget.yearFilter != null
              ? '${widget.subjectFilter!.replaceAll('_', ' ')} ${widget.yearFilter}'
              : 'Matric questions'
        );

    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : items.isEmpty
              ? const Center(
                  child: Padding(
                    padding: EdgeInsets.all(24),
                    child: Text(
                      'No interactive questions for this paper yet.\nMore years are being parsed into the bank.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: FourTheme.muted),
                    ),
                  ),
                )
              : ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: items.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 8),
                  itemBuilder: (context, i) {
                    final q = items[i];
                    return Card(
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: FourTheme.primarySoft,
                          child: Text('Q${q.number == 0 ? i + 1 : q.number}',
                              style: const TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.w800,
                                  color: FourTheme.primaryDark)),
                        ),
                        title: Text(q.prompt,
                            maxLines: 3,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(fontWeight: FontWeight.w600)),
                        subtitle: Text(q.displayTitle),
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
    return Scaffold(
      appBar: AppBar(title: Text('${q.displayTitle} · Q${q.number}')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
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
            const SizedBox(height: 20),
            const Text('Similar questions',
                style: TextStyle(fontWeight: FontWeight.w900)),
            const SizedBox(height: 8),
            ...q.similarQuestions.map((s) => Card(
                  child: ListTile(
                    title: Text(s.prompt, maxLines: 3),
                    subtitle: Text(s.topic),
                  ),
                )),
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
