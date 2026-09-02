import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/theme/four_theme.dart';
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
    ContentRepository.instance.preload().then((_) {
      if (mounted) setState(() => ready = true);
    });
  }

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomeScreen(
        grade: grade,
        onGrade: (g) => setState(() => grade = g),
        onOpenNotes: () => setState(() => index = 1),
        onOpenPractice: () => setState(() => index = 2),
        onOpenBot: () => setState(() => index = 3),
        onOpenExams: () => setState(() => index = 4),
      ),
      NotesScreen(
        grade: grade,
        subject: subject,
        onGrade: (g) => setState(() => grade = g),
        onSubject: (s) => setState(() => subject = s),
      ),
      PracticeScreen(
        grade: grade,
        subject: subject,
        onGrade: (g) => setState(() => grade = g),
        onSubject: (s) => setState(() => subject = s),
      ),
      const BotScreen(),
      const ExamsScreen(),
      const ToolsScreen(),
      const UnlockScreen(),
    ];

    return Scaffold(
      body: ready
          ? AnimatedSwitcher(
              duration: const Duration(milliseconds: 220),
              child: KeyedSubtree(
                key: ValueKey(index),
                child: pages[index.clamp(0, pages.length - 1)],
              ),
            )
          : const Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Loading study content…',
                      style: TextStyle(color: FourTheme.muted)),
                ],
              ),
            ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: index > 4 ? 0 : index,
        onDestinationSelected: (i) => setState(() => index = i),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home_rounded),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.auto_stories_outlined),
            selectedIcon: Icon(Icons.auto_stories),
            label: 'Notes',
          ),
          NavigationDestination(
            icon: Icon(Icons.quiz_outlined),
            selectedIcon: Icon(Icons.quiz),
            label: 'Practice',
          ),
          NavigationDestination(
            icon: Icon(Icons.smart_toy_outlined),
            selectedIcon: Icon(Icons.smart_toy),
            label: 'Coach',
          ),
          NavigationDestination(
            icon: Icon(Icons.assignment_outlined),
            selectedIcon: Icon(Icons.assignment),
            label: 'Exams',
          ),
        ],
      ),
    );
  }
}
