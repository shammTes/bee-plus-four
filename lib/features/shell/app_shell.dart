import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/l10n/app_strings.dart';
import '../../core/settings/app_settings.dart';
import '../../core/theme/four_theme.dart';
import '../bot/bot_screen.dart';
import '../exams/exams_screen.dart';
import '../home/home_screen.dart';
import '../labs/virtual_lab_screen.dart';
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
    ContentRepository.instance.preload().whenComplete(() {
      if (mounted) setState(() => ready = true);
    });
    AppSettings.instance.addListener(_onSettings);
  }

  void _onSettings() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    AppSettings.instance.removeListener(_onSettings);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      HomeScreen(
        grade: grade,
        onGrade: (g) => setState(() => grade = g),
        onOpenNotes: () => setState(() => index = 1),
        onOpenPractice: () => setState(() => index = 2),
        onOpenBot: () => setState(() => index = 3),
        onOpenExams: () => setState(() => index = 4),
        onOpenLabs: () => setState(() => index = 5),
        onOpenTools: () => setState(() => index = 6),
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
      BotScreen(initialGrade: grade),
      const ExamsScreen(),
      const VirtualLabScreen(),
      ToolsScreen(grade: grade, subject: subject),
      const UnlockScreen(),
    ];

    final navIndex = index <= 4 ? index : 0;

    return Scaffold(
      body: ready
          ? AnimatedSwitcher(
              duration: const Duration(milliseconds: 220),
              child: KeyedSubtree(
                key: ValueKey('$index-$grade-$subject-${AppSettings.instance.tigrinya}'),
                child: pages[index.clamp(0, pages.length - 1)],
              ),
            )
          : Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const CircularProgressIndicator(),
                  const SizedBox(height: 16),
                  Text(AppStrings.loading,
                      style: const TextStyle(color: FourTheme.muted)),
                ],
              ),
            ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: navIndex,
        onDestinationSelected: (i) => setState(() => index = i),
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home_rounded),
            label: AppStrings.home,
          ),
          NavigationDestination(
            icon: const Icon(Icons.auto_stories_outlined),
            selectedIcon: const Icon(Icons.auto_stories),
            label: AppStrings.notes,
          ),
          NavigationDestination(
            icon: const Icon(Icons.quiz_outlined),
            selectedIcon: const Icon(Icons.quiz),
            label: AppStrings.practice,
          ),
          NavigationDestination(
            icon: const Icon(Icons.smart_toy_outlined),
            selectedIcon: const Icon(Icons.smart_toy),
            label: AppStrings.coach,
          ),
          NavigationDestination(
            icon: const Icon(Icons.assignment_outlined),
            selectedIcon: const Icon(Icons.assignment),
            label: AppStrings.exams,
          ),
        ],
      ),
    );
  }
}
