import 'package:flutter/material.dart';
import '../../core/content/content_repository.dart';
import '../bot/bot_screen.dart';
import '../exams/exams_screen.dart';
import '../home/home_screen.dart';
import '../notes/notes_screen.dart';
import '../practice/practice_screen.dart';
import '../tools/tools_screen.dart';
import '../unlock/unlock_screen.dart';

class AppShell extends StatefulWidget {
  const AppShell({super.key});
  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int index = 0;
  String grade = 'G10';
  String subject = 'MATH';
  bool ready = false;

  @override
  void initState() {
    super.initState();
    ContentRepository.instance.preload().then((_) { if (mounted) setState(() => ready = true); });
  }

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomeScreen(grade: grade, onGrade: (g) => setState(() => grade = g),
        onOpenNotes: () => setState(() => index = 1),
        onOpenPractice: () => setState(() => index = 2),
        onOpenBot: () => setState(() => index = 3),
        onOpenExams: () => setState(() => index = 4)),
      NotesScreen(grade: grade, subject: subject, onGrade: (g) => setState(() => grade = g), onSubject: (s) => setState(() => subject = s)),
      PracticeScreen(grade: grade, subject: subject, onGrade: (g) => setState(() => grade = g), onSubject: (s) => setState(() => subject = s)),
      const BotScreen(),
      const ExamsScreen(),
      const ToolsScreen(),
    ];
    return Scaffold(
      appBar: AppBar(
        title: const Row(children: [
          CircleAvatar(backgroundColor: Color(0xFFCCFBF1), child: Icon(Icons.school, color: Color(0xFF0D9488), size: 20)),
          SizedBox(width: 10),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('4', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            Text('Highschool · offline coach', style: TextStyle(fontSize: 11)),
          ]),
        ]),
        actions: [
          IconButton(icon: const Icon(Icons.lock_open), onPressed: () {
            Navigator.of(context).push(MaterialPageRoute(builder: (_) => const UnlockScreen()));
          }),
        ],
      ),
      body: ready ? IndexedStack(index: index, children: pages) : const Center(child: CircularProgressIndicator()),
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (i) => setState(() => index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.menu_book_outlined), selectedIcon: Icon(Icons.menu_book), label: 'Notes'),
          NavigationDestination(icon: Icon(Icons.quiz_outlined), selectedIcon: Icon(Icons.quiz), label: 'Practice'),
          NavigationDestination(icon: Icon(Icons.smart_toy_outlined), selectedIcon: Icon(Icons.smart_toy), label: 'Coach'),
          NavigationDestination(icon: Icon(Icons.assignment_outlined), selectedIcon: Icon(Icons.assignment), label: 'Exams'),
          NavigationDestination(icon: Icon(Icons.build_outlined), selectedIcon: Icon(Icons.build), label: 'Tools'),
        ],
      ),
    );
  }
}
