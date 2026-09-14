import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
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
  /// SCIENCE or ARTS — only matters for G11/G12
  String stream = CurriculumStreams.science;
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

  void _setGrade(String g) {
    setState(() {
      grade = g;
      final allowed = CurriculumStreams.subjectsFor(g, stream: stream);
      if (!allowed.contains(subject)) {
        subject = allowed.first;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      HomeScreen(
        grade: grade,
        onGrade: _setGrade,
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
        stream: stream,
        onGrade: _setGrade,
        onSubject: (s) => setState(() => subject = s),
        onStream: (st) => setState(() {
          stream = st;
          final allowed = CurriculumStreams.subjectsFor(grade, stream: st);
          if (!allowed.contains(subject)) subject = allowed.first;
        }),
      ),
      PracticeScreen(
        grade: grade,
        subject: subject,
        onGrade: _setGrade,
        onSubject: (s) => setState(() => subject = s),
      ),
      BotScreen(initialGrade: grade),
      const ExamsScreen(),
      const VirtualLabScreen(),
      ToolsScreen(grade: grade, subject: subject),
      const UnlockScreen(),
    ];

    final navIndex = index <= 4 ? index : 0;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) async {
        if (didPop) return;
        // Prefer leaving secondary pages (labs/tools/unlock) first
        if (index > 4) {
          setState(() => index = 0);
          return;
        }
        if (index != 0) {
          setState(() => index = 0);
          return;
        }
        // On home: confirm exit
        final leave = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            title: const Text('Leave 4?'),
            content: const Text('Close the app?'),
            actions: [
              TextButton(
                  onPressed: () => Navigator.pop(ctx, false),
                  child: const Text('Stay')),
              FilledButton(
                  onPressed: () => Navigator.pop(ctx, true),
                  child: const Text('Exit')),
            ],
          ),
        );
        if (leave == true && context.mounted) {
          // Allow system back to finish
          Navigator.of(context).maybePop();
        }
      },
      child: Scaffold(
        body: ready
            ? AnimatedSwitcher(
                duration: const Duration(milliseconds: 220),
                child: KeyedSubtree(
                  key: ValueKey(
                      '$index-$grade-$subject-$stream-${AppSettings.instance.tigrinya}'),
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
      ),
    );
  }
}
