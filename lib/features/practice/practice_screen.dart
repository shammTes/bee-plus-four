import 'package:flutter/material.dart';
import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';

class PracticeScreen extends StatelessWidget {
  const PracticeScreen({super.key, required this.grade, required this.subject, required this.onGrade, required this.onSubject});
  final String grade, subject;
  final ValueChanged<String> onGrade, onSubject;
  static const subjects = ['MATH','SCIENCE','ENGLISH','PHYSICS','CHEMISTRY','BIOLOGY'];

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.fromLTRB(16,12,16,0), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Practice', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
        const Text('MCQs with explanations'),
        const SizedBox(height: 10),
        SingleChildScrollView(scrollDirection: Axis.horizontal, child: Row(children:
          ['G9','G10','G11','G12'].map((g) => Padding(padding: const EdgeInsets.only(right: 8),
            child: ChoiceChip(label: Text(g), selected: grade == g, onSelected: (_) => onGrade(g)))).toList())),
        const SizedBox(height: 8),
        SingleChildScrollView(scrollDirection: Axis.horizontal, child: Row(children:
          subjects.map((s) => Padding(padding: const EdgeInsets.only(right: 8),
            child: ChoiceChip(label: Text(s), selected: subject == s, onSelected: (_) => onSubject(s)))).toList())),
      ])),
      Expanded(child: FutureBuilder<List<PracticeQuestion>>(
        future: ContentRepository.instance.questionsFor(grade, subject),
        builder: (context, snap) {
          final list = snap.data ?? [];
          if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (list.isEmpty) return const Center(child: Text('No questions yet.'));
          return ListView.separated(
            padding: const EdgeInsets.all(16), itemCount: list.length,
            separatorBuilder: (_, __) => const SizedBox(height: 8),
            itemBuilder: (context, i) {
              final q = list[i];
              return Card(child: ListTile(
                leading: const CircleAvatar(child: Icon(Icons.quiz, size: 18)),
                title: Text(q.prompt, maxLines: 2, overflow: TextOverflow.ellipsis),
                subtitle: Text('${q.subject} · ${q.grade}'),
                onTap: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => _Detail(q: q))),
              ));
            },
          );
        },
      )),
    ]);
  }
}

class _Detail extends StatefulWidget {
  const _Detail({required this.q});
  final PracticeQuestion q;
  @override
  State<_Detail> createState() => _DetailState();
}
class _DetailState extends State<_Detail> {
  int? selected; bool revealed = false;
  @override
  Widget build(BuildContext context) {
    final q = widget.q;
    return Scaffold(
      appBar: AppBar(title: const Text('Practice')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        Text(q.prompt, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
        const SizedBox(height: 16),
        ...List.generate(q.options.length, (i) {
          Color? bg;
          if (revealed) {
            if (i == q.correctIndex) bg = Colors.green.withValues(alpha: 0.2);
            else if (selected == i) bg = Colors.red.withValues(alpha: 0.2);
          }
          return Card(color: bg, child: ListTile(title: Text(q.options[i]), onTap: revealed ? null : () => setState(() => selected = i)));
        }),
        FilledButton(onPressed: selected == null || revealed ? null : () => setState(() => revealed = true), child: const Text('Check')),
        if (revealed) Padding(padding: const EdgeInsets.only(top: 12), child: Text(q.explanation)),
      ]),
    );
  }
}
