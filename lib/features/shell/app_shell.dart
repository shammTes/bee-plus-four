import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

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
  String grade = 'G12';
  String subject = 'MATH';
  bool ready = false;

  @override
  void initState() {
    super.initState();
    ContentRepository.instance.preload().then((_) {
      if (mounted) setState(() => ready = true);
    });
  }

  Future<bool> _onWillPop() async {
    final leave = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Leave BEE PLUS 4?'),
        content: const Text('Do you want to stay or close the app?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Stay'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Leave'),
          ),
        ],
      ),
    );
    if (leave == true) {
      await SystemNavigator.pop();
      return true;
    }
    return false;
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
        onOpenTools: () => setState(() => index = 5),
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

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        await _onWillPop();
      },
      child: Scaffold(
        body: ready
            ? AnimatedSwitcher(
                duration: const Duration(milliseconds: 220),
                child: KeyedSubtree(
                  key: ValueKey('$index-$grade-$subject'),
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
          height: 68,
          labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.home_outlined, size: 28),
              selectedIcon: Icon(Icons.home_rounded, size: 28),
              label: 'Home',
            ),
            NavigationDestination(
              icon: Icon(Icons.auto_stories_outlined, size: 28),
              selectedIcon: Icon(Icons.auto_stories, size: 28),
              label: 'Notes',
            ),
            NavigationDestination(
              icon: Icon(Icons.quiz_outlined, size: 28),
              selectedIcon: Icon(Icons.quiz, size: 28),
              label: 'Practice',
            ),
            NavigationDestination(
              icon: Icon(Icons.smart_toy_outlined, size: 28),
              selectedIcon: Icon(Icons.smart_toy, size: 28),
              label: 'Coach',
            ),
            NavigationDestination(
              icon: Icon(Icons.assignment_outlined, size: 28),
              selectedIcon: Icon(Icons.assignment, size: 28),
              label: 'Exams',
            ),
          ],
        ),
      ),
    );
  }
}
