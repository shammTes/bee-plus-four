import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

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

  void _setStream(String st) {
    setState(() {
      stream = st;
      final allowed = CurriculumStreams.subjectsFor(grade, stream: st);
      if (!allowed.contains(subject)) {
        subject = allowed.first;
      }
    });
  }

  void _setSubject(String s) {
    setState(() => subject = s);
  }

  @override
  Widget build(BuildContext context) {
    final pages = <Widget>[
      HomeScreen(
        grade: grade,
        stream: stream,
        onGrade: _setGrade,
        onStream: _setStream,
        onSubject: _setSubject,
        onOpenNotes: () => setState(() => index = 1),
        onOpenPractice: () => setState(() => index = 2),
        onOpenExams: () => setState(() => index = 3),
        onOpenBot: () => setState(() => index = 5),
      ),
      NotesScreen(
        grade: grade,
        subject: subject,
        stream: stream,
        onGrade: _setGrade,
        onSubject: _setSubject,
        onStream: _setStream,
      ),
      PracticeScreen(
        grade: grade,
        subject: subject,
        stream: stream,
        onGrade: _setGrade,
        onSubject: _setSubject,
        onStream: _setStream,
      ),
      ExamsScreen(
        grade: grade,
        subject: subject,
        onGrade: _setGrade,
        onSubject: _setSubject,
      ),
      ToolsScreen(grade: grade, subject: subject),
      BotScreen(initialGrade: grade),
      const UnlockScreen(),
    ];

    final navIndex = index <= 4 ? index : 0;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) async {
        if (didPop) return;
        if (index > 4) {
          setState(() => index = 0);
          return;
        }
        if (index != 0) {
          setState(() => index = 0);
          return;
        }
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
          SystemNavigator.pop();
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
            : const Center(child: CircularProgressIndicator()),
        bottomNavigationBar: NavigationBar(
          selectedIndex: navIndex,
          onDestinationSelected: (i) => setState(() => index = i),
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
            NavigationDestination(icon: Icon(Icons.menu_book_outlined), selectedIcon: Icon(Icons.menu_book), label: 'Notes'),
            NavigationDestination(icon: Icon(Icons.quiz_outlined), selectedIcon: Icon(Icons.quiz), label: 'Practice'),
            NavigationDestination(icon: Icon(Icons.assignment_outlined), selectedIcon: Icon(Icons.assignment), label: 'Exams'),
            NavigationDestination(icon: Icon(Icons.handyman_outlined), selectedIcon: Icon(Icons.handyman), label: 'Tools'),
          ],
        ),
        floatingActionButton: FloatingActionButton.extended(
          onPressed: () => setState(() => index = 5),
          icon: const Icon(Icons.smart_toy),
          label: const Text('Coach'),
        ),
      ),
    );
  }
}
