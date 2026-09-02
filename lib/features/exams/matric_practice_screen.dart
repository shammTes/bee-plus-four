import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';

class MatricPracticeScreen extends StatefulWidget {
  const MatricPracticeScreen({
    super.key,
    this.subjectFilter,
    this.grade,
    this.unitNumber,
    this.title,
  });

  final String? subjectFilter;
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
        list = list.where((q) => q.subject == widget.subjectFilter).toList();
      }
      if (mounted) setState(() { items = list; loading = false; });
    } catch (_) {
      if (mounted) setState(() { items = const []; loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.title ?? 'Matric questions')),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : items.isEmpty
              ? const Center(child: Text('No matric questions loaded yet.\nAdd assets/content/matric_*.json'))
              : ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: items.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 8),
                  itemBuilder: (context, i) {
                    final q = items[i];
                    return Card(
                      child: ListTile(
                        title: Text(q.prompt, maxLines: 3, overflow: TextOverflow.ellipsis),
                        subtitle: Text('${q.subject} · ${q.year} · Q${q.number}'),
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(builder: (_) => _QuestionDetail(q: q)),
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
      appBar: AppBar(title: Text('${q.subject} ${q.year} Q${q.number}')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(q.prompt, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
          const SizedBox(height: 12),
          ...List.generate(q.options.length, (i) {
            final selected = i == q.correctIndex;
            return Card(
              color: selected ? const Color(0xFFCCFBF1) : null,
              child: ListTile(
                leading: Text(String.fromCharCode(65 + i)),
                title: Text(q.options[i]),
              ),
            );
          }),
          if (q.explanationSteps.isNotEmpty) ...[
            const SizedBox(height: 16),
            const Text('Step-by-step', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...q.explanationSteps.map((s) => Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Text(s),
                )),
          ],
        ],
      ),
    );
  }
}
