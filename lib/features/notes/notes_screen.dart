import 'package:flutter/material.dart';
import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';

class NotesScreen extends StatelessWidget {
  const NotesScreen({super.key, required this.grade, required this.subject, required this.onGrade, required this.onSubject});
  final String grade, subject;
  final ValueChanged<String> onGrade, onSubject;
  static const subjects = ['MATH','SCIENCE','ENGLISH','PHYSICS','CHEMISTRY','BIOLOGY'];

  @override
  Widget build(BuildContext context) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      Padding(padding: const EdgeInsets.fromLTRB(16,12,16,0), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Notes', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
        const Text('Highschool units only'),
        const SizedBox(height: 10),
        SingleChildScrollView(scrollDirection: Axis.horizontal, child: Row(children:
          ['G9','G10','G11','G12'].map((g) => Padding(padding: const EdgeInsets.only(right: 8),
            child: ChoiceChip(label: Text(g), selected: grade == g, onSelected: (_) => onGrade(g)))).toList())),
        const SizedBox(height: 8),
        SingleChildScrollView(scrollDirection: Axis.horizontal, child: Row(children:
          subjects.map((s) => Padding(padding: const EdgeInsets.only(right: 8),
            child: ChoiceChip(label: Text(s), selected: subject == s, onSelected: (_) => onSubject(s)))).toList())),
      ])),
      Expanded(child: FutureBuilder<List<UnitNote>>(
        future: ContentRepository.instance.notesFor(grade, subject),
        builder: (context, snap) {
          final notes = snap.data ?? [];
          if (snap.connectionState != ConnectionState.done) return const Center(child: CircularProgressIndicator());
          if (notes.isEmpty) return const Center(child: Text('No notes yet. Upload JSON packs.'));
          return ListView.separated(
            padding: const EdgeInsets.all(16), itemCount: notes.length,
            separatorBuilder: (_, __) => const SizedBox(height: 8),
            itemBuilder: (context, i) {
              final n = notes[i];
              return Card(child: ListTile(
                leading: CircleAvatar(child: Text('${n.unitNumber}')),
                title: Text(n.title, style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text(n.summary, maxLines: 2, overflow: TextOverflow.ellipsis),
              ));
            },
          );
        },
      )),
    ]);
  }
}
