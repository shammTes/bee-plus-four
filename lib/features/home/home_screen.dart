import 'package:flutter/material.dart';
import '../../core/content/content_repository.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.grade, required this.onGrade, required this.onOpenNotes, required this.onOpenPractice, required this.onOpenBot, required this.onOpenExams});
  final String grade;
  final ValueChanged<String> onGrade;
  final VoidCallback onOpenNotes, onOpenPractice, onOpenBot, onOpenExams;
  static const grades = ['G9', 'G10', 'G11', 'G12'];

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: Future.wait([ContentRepository.instance.notes(), ContentRepository.instance.questions()]),
      builder: (context, snap) {
        final notes = (snap.data?[0] as List?)?.length ?? 0;
        final qs = (snap.data?[1] as List?)?.length ?? 0;
        return ListView(children: [
          Container(
            width: double.infinity, padding: const EdgeInsets.fromLTRB(20, 20, 20, 24),
            decoration: const BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Color(0xFFCCFBF1), Color(0xFFF0FDFA)])),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Your learning dashboard', style: TextStyle(color: Color(0xFF0F766E), fontWeight: FontWeight.w600)),
              const SizedBox(height: 6),
              const Text('4', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Color(0xFF134E4A))),
              const Text('Highschool only · offline coach · no Junior', style: TextStyle(color: Color(0xFF0F766E))),
              const SizedBox(height: 16),
              Wrap(spacing: 8, children: grades.map((g) => ChoiceChip(
                label: Text(g), selected: grade == g, onSelected: (_) => onGrade(g),
                selectedColor: const Color(0xFF0D9488),
                labelStyle: TextStyle(color: grade == g ? Colors.white : null, fontWeight: FontWeight.w600),
              )).toList()),
            ]),
          ),
          Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Row(children: [
              _Stat('$notes', 'Notes'), const SizedBox(width: 10),
              _Stat('$qs', 'Practice'), const SizedBox(width: 10),
              const _Stat('Bot', 'Coach'),
            ]),
            const SizedBox(height: 20),
            const Text('Quick actions', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 10),
            _Action('Offline study coach', 'Controlled Q&A · hints · progress', Icons.smart_toy, onOpenBot),
            _Action('Notes', 'Highschool unit notes', Icons.menu_book, onOpenNotes),
            _Action('Practice', 'MCQs with explanations', Icons.quiz, onOpenPractice),
            _Action('Exams', 'Matriculation catalogue', Icons.assignment, onOpenExams),
          ])),
        ]);
      },
    );
  }
}

class _Stat extends StatelessWidget {
  const _Stat(this.value, this.label);
  final String value, label;
  @override
  Widget build(BuildContext context) => Expanded(child: Card(child: Padding(padding: const EdgeInsets.all(14), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
    Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF0D9488))),
    Text(label, style: const TextStyle(fontSize: 12)),
  ]))));
}

class _Action extends StatelessWidget {
  const _Action(this.title, this.subtitle, this.icon, this.onTap);
  final String title, subtitle; final IconData icon; final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    return Card(margin: const EdgeInsets.only(bottom: 10), child: ListTile(
      onTap: onTap,
      leading: CircleAvatar(backgroundColor: cs.primaryContainer, child: Icon(icon, color: cs.primary)),
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
      subtitle: Text(subtitle), trailing: const Icon(Icons.chevron_right),
    ));
  }
}
