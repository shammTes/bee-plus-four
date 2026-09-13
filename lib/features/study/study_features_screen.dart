import 'dart:async';

import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/l10n/app_strings.dart';
import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/progress/study_log.dart';
import '../../core/theme/four_theme.dart';

/// Hub for Daily 10, weakness, flashcards, Pomodoro, progress calendar.
class StudyFeaturesScreen extends StatelessWidget {
  const StudyFeaturesScreen({
    super.key,
    required this.grade,
    required this.subject,
  });

  final String grade;
  final String subject;

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return ListView(
      padding: EdgeInsets.fromLTRB(16, top + 12, 16, 24),
      children: [
        Text(AppStrings.tools,
            style: const TextStyle(
                fontSize: 22, fontWeight: FontWeight.w900)),
        const SizedBox(height: 12),
        _tile(
          context,
          Icons.bolt,
          AppStrings.daily10,
          AppStrings.daily10Sub,
          const Color(0xFFF59E0B),
          () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) =>
                  Daily10Screen(grade: grade, subject: subject),
            ),
          ),
        ),
        _tile(
          context,
          Icons.warning_amber_rounded,
          AppStrings.weakness,
          AppStrings.weaknessSub,
          const Color(0xFFEF4444),
          () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) =>
                  WeaknessScreen(grade: grade, subject: subject),
            ),
          ),
        ),
        _tile(
          context,
          Icons.style,
          AppStrings.flashcards,
          AppStrings.flashcardsSub,
          FourTheme.violet,
          () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) =>
                  FlashcardsScreen(grade: grade, subject: subject),
            ),
          ),
        ),
        _tile(
          context,
          Icons.timer,
          AppStrings.studyTimer,
          AppStrings.studyTimerSub,
          FourTheme.primaryDark,
          () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const PomodoroScreen()),
          ),
        ),
        _tile(
          context,
          Icons.calendar_month,
          AppStrings.progress,
          AppStrings.progressSub,
          const Color(0xFF0EA5E9),
          () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const ProgressScreen()),
          ),
        ),
        _tile(
          context,
          Icons.hourglass_bottom,
          AppStrings.timedMock,
          AppStrings.timedMockSub,
          const Color(0xFFEA580C),
          () => Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) =>
                  TimedMockScreen(grade: grade, subject: subject),
            ),
          ),
        ),
      ],
    );
  }

  Widget _tile(
    BuildContext context,
    IconData icon,
    String title,
    String sub,
    Color color,
    VoidCallback onTap,
  ) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.15),
          child: Icon(icon, color: color),
        ),
        title: Text(title,
            style: const TextStyle(fontWeight: FontWeight.w800)),
        subtitle: Text(sub),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}

class Daily10Screen extends StatefulWidget {
  const Daily10Screen({super.key, required this.grade, required this.subject});
  final String grade;
  final String subject;

  @override
  State<Daily10Screen> createState() => _Daily10ScreenState();
}

class _Daily10ScreenState extends State<Daily10Screen> {
  List<PracticeQuestion> qs = [];
  int i = 0;
  int? sel;
  bool revealed = false;
  int correct = 0;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final all = await ContentRepository.instance.questions();
    var pool = all
        .where((q) =>
            q.grade == widget.grade && q.subject == widget.subject)
        .toList();
    if (pool.length < 10) {
      pool = all.where((q) => q.subject == widget.subject).toList();
    }
    pool.shuffle();
    setState(() => qs = pool.take(10).toList());
  }

  @override
  Widget build(BuildContext context) {
    if (qs.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(AppStrings.daily10)),
        body: const Center(child: CircularProgressIndicator()),
      );
    }
    if (i >= qs.length) {
      StudyLog.instance.markStudied(minutes: 15);
      return Scaffold(
        appBar: AppBar(title: Text(AppStrings.daily10)),
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('$correct / ${qs.length}',
                  style: const TextStyle(
                      fontSize: 40, fontWeight: FontWeight.w900)),
              Text(AppStrings.mastery),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: () => Navigator.pop(context),
                child: Text(AppStrings.gotIt),
              ),
            ],
          ),
        ),
      );
    }
    final q = qs[i];
    return Scaffold(
      appBar: AppBar(
        title: Text('${AppStrings.daily10} · ${i + 1}/10'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(q.prompt,
              style: const TextStyle(
                  fontSize: 16, fontWeight: FontWeight.w700)),
          const SizedBox(height: 16),
          ...List.generate(q.options.length, (oi) {
            final ok = revealed && oi == q.correctIndex;
            final bad = revealed && sel == oi && oi != q.correctIndex;
            return Card(
              color: ok
                  ? const Color(0xFFECFDF5)
                  : bad
                      ? const Color(0xFFFEF2F2)
                      : null,
              child: ListTile(
                title: Text(
                    '${String.fromCharCode(65 + oi)}. ${q.options[oi]}'),
                onTap: revealed
                    ? null
                    : () => setState(() => sel = oi),
                selected: sel == oi,
              ),
            );
          }),
          const SizedBox(height: 12),
          if (!revealed)
            FilledButton(
              onPressed: sel == null
                  ? null
                  : () {
                      setState(() {
                        revealed = true;
                        if (sel == q.correctIndex) correct++;
                      });
                      MasteryStore.instance.record(
                        widget.grade,
                        widget.subject,
                        q.unitNumber == 0 ? 1 : q.unitNumber,
                        correct: sel == q.correctIndex,
                      );
                    },
              child: Text(AppStrings.checkAnswer),
            )
          else ...[
            if (q.explanation.isNotEmpty)
              Text(q.explanation,
                  style: const TextStyle(height: 1.4)),
            const SizedBox(height: 8),
            FilledButton(
              onPressed: () => setState(() {
                i++;
                sel = null;
                revealed = false;
              }),
              child: Text(AppStrings.nextQuestion),
            ),
          ],
        ],
      ),
    );
  }
}

class WeaknessScreen extends StatelessWidget {
  const WeaknessScreen({super.key, required this.grade, required this.subject});
  final String grade;
  final String subject;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<UnitNote>>(
      future: ContentRepository.instance.notesFor(grade, subject),
      builder: (context, snap) {
        final notes = snap.data ?? [];
        final units = notes.map((n) => n.unitNumber).toSet().toList()..sort();
        final weak = MasteryStore.instance
            .weakUnits(grade: grade, subject: subject, units: units);
        return Scaffold(
          appBar: AppBar(title: Text(AppStrings.weakness)),
          body: weak.isEmpty
              ? Center(child: Text(AppStrings.loading))
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: weak.length,
                  itemBuilder: (context, i) {
                    final w = weak[i];
                    final u = w['unit'] as int;
                    final title = notes
                        .where((n) => n.unitNumber == u)
                        .map((n) => n.title)
                        .cast<String?>()
                        .firstWhere((_) => true, orElse: () => null);
                    final m = w['mastery'] as double;
                    return Card(
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: m < 0.4
                              ? const Color(0xFFFEE2E2)
                              : const Color(0xFFFEF3C7),
                          child: Text('U$u',
                              style: const TextStyle(
                                  fontWeight: FontWeight.w900,
                                  fontSize: 12)),
                        ),
                        title: Text(title ?? 'Unit $u',
                            maxLines: 2,
                            style: const TextStyle(
                                fontWeight: FontWeight.w700)),
                        subtitle: Text(
                            '${w['label']} · ${(m * 100).round()}%'),
                        trailing: Text(
                          '${(w['stats'] as Map)['correct']}/${(w['stats'] as Map)['seen']}',
                        ),
                      ),
                    );
                  },
                ),
        );
      },
    );
  }
}

class FlashcardsScreen extends StatefulWidget {
  const FlashcardsScreen(
      {super.key, required this.grade, required this.subject});
  final String grade;
  final String subject;

  @override
  State<FlashcardsScreen> createState() => _FlashcardsScreenState();
}

class _FlashcardsScreenState extends State<FlashcardsScreen> {
  List<UnitNote> notes = [];
  int i = 0;
  bool back = false;

  @override
  void initState() {
    super.initState();
    ContentRepository.instance.notesFor(widget.grade, widget.subject).then((n) {
      if (mounted) setState(() => notes = n);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(AppStrings.flashcards)),
      body: notes.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : GestureDetector(
              onTap: () => setState(() => back = !back),
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  children: [
                    Text('${i + 1} / ${notes.length}'),
                    const Spacer(),
                    Container(
                      width: double.infinity,
                      height: 280,
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: back
                              ? [const Color(0xFF0D9488), const Color(0xFF115E59)]
                              : [const Color(0xFF7C3AED), const Color(0xFF5B21B6)],
                        ),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Center(
                        child: Text(
                          back
                              ? (notes[i].summary.isEmpty
                                  ? notes[i].title
                                  : notes[i].summary)
                              : 'U${notes[i].unitNumber}\n${notes[i].title}',
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 18,
                            fontWeight: FontWeight.w800,
                            height: 1.35,
                          ),
                        ),
                      ),
                    ),
                    const Spacer(),
                    Row(
                      children: [
                        Expanded(
                          child: OutlinedButton(
                            onPressed: i == 0
                                ? null
                                : () => setState(() {
                                      i--;
                                      back = false;
                                    }),
                            child: const Text('←'),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: FilledButton(
                            onPressed: i >= notes.length - 1
                                ? null
                                : () => setState(() {
                                      i++;
                                      back = false;
                                    }),
                            child: Text(AppStrings.next),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
    );
  }
}

class PomodoroScreen extends StatefulWidget {
  const PomodoroScreen({super.key});

  @override
  State<PomodoroScreen> createState() => _PomodoroScreenState();
}

class _PomodoroScreenState extends State<PomodoroScreen> {
  static const focusSecs = 25 * 60;
  static const breakSecs = 5 * 60;
  int remaining = focusSecs;
  bool focusing = true;
  bool running = false;
  Timer? t;

  void _tick() {
    if (remaining <= 1) {
      if (focusing) {
        StudyLog.instance.markStudied(minutes: 25);
      }
      setState(() {
        focusing = !focusing;
        remaining = focusing ? focusSecs : breakSecs;
        running = false;
      });
      t?.cancel();
      return;
    }
    setState(() => remaining--);
  }

  void _toggle() {
    if (running) {
      t?.cancel();
      setState(() => running = false);
    } else {
      t = Timer.periodic(const Duration(seconds: 1), (_) => _tick());
      setState(() => running = true);
    }
  }

  @override
  void dispose() {
    t?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final m = (remaining ~/ 60).toString().padLeft(2, '0');
    final s = (remaining % 60).toString().padLeft(2, '0');
    return Scaffold(
      appBar: AppBar(title: Text(AppStrings.studyTimer)),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(focusing ? 'Focus' : 'Break',
                style: const TextStyle(
                    fontSize: 18, fontWeight: FontWeight.w800)),
            const SizedBox(height: 12),
            Text('$m:$s',
                style: const TextStyle(
                    fontSize: 64, fontWeight: FontWeight.w900)),
            const SizedBox(height: 20),
            FilledButton(
              onPressed: _toggle,
              child: Text(running ? 'Pause' : AppStrings.start),
            ),
          ],
        ),
      ),
    );
  }
}

class ProgressScreen extends StatelessWidget {
  const ProgressScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final days = StudyLog.instance.lastWeeks();
    final streak = StudyLog.instance.currentStreak();
    return Scaffold(
      appBar: AppBar(title: Text(AppStrings.progress)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Streak: $streak',
                style: const TextStyle(
                    fontSize: 22, fontWeight: FontWeight.w900)),
            const SizedBox(height: 16),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: days.map((e) {
                final intensity = e.minutes == 0
                    ? 0.08
                    : (e.minutes.clamp(1, 60) / 60);
                return Container(
                  width: 36,
                  height: 36,
                  decoration: BoxDecoration(
                    color: Color.lerp(
                      const Color(0xFFE2E8F0),
                      const Color(0xFF0D9488),
                      intensity,
                    ),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  alignment: Alignment.center,
                  child: Text('${e.day.day}',
                      style: const TextStyle(
                          fontSize: 10, fontWeight: FontWeight.w700)),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}

class TimedMockScreen extends StatefulWidget {
  const TimedMockScreen(
      {super.key, required this.grade, required this.subject});
  final String grade;
  final String subject;

  @override
  State<TimedMockScreen> createState() => _TimedMockScreenState();
}

class _TimedMockScreenState extends State<TimedMockScreen> {
  List<PracticeQuestion> qs = [];
  int i = 0;
  int? sel;
  int remaining = 90 * 60; // 90 min
  Timer? t;
  int correct = 0;
  bool done = false;

  @override
  void initState() {
    super.initState();
    _load();
    t = Timer.periodic(const Duration(seconds: 1), (_) {
      if (remaining <= 1) {
        setState(() => done = true);
        t?.cancel();
        return;
      }
      setState(() => remaining--);
    });
  }

  Future<void> _load() async {
    final all = await ContentRepository.instance.questions();
    var pool = all
        .where((q) =>
            q.grade == widget.grade && q.subject == widget.subject)
        .toList();
    if (pool.isEmpty) pool = all.where((q) => q.subject == widget.subject).toList();
    pool.shuffle();
    setState(() => qs = pool.take(40).toList());
  }

  @override
  void dispose() {
    t?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final mm = (remaining ~/ 60).toString().padLeft(2, '0');
    final ss = (remaining % 60).toString().padLeft(2, '0');
    if (done || (qs.isNotEmpty && i >= qs.length)) {
      StudyLog.instance.markStudied(minutes: 30);
      return Scaffold(
        appBar: AppBar(title: Text(AppStrings.timedMock)),
        body: Center(
          child: Text('$correct / ${qs.length}',
              style: const TextStyle(
                  fontSize: 40, fontWeight: FontWeight.w900)),
        ),
      );
    }
    if (qs.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(AppStrings.timedMock)),
        body: const Center(child: CircularProgressIndicator()),
      );
    }
    final q = qs[i];
    return Scaffold(
      appBar: AppBar(
        title: Text('$mm:$ss · ${i + 1}/${qs.length}'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(q.prompt,
              style: const TextStyle(
                  fontWeight: FontWeight.w700, fontSize: 16)),
          const SizedBox(height: 12),
          ...List.generate(q.options.length, (oi) {
            return Card(
              child: ListTile(
                title: Text(
                    '${String.fromCharCode(65 + oi)}. ${q.options[oi]}'),
                selected: sel == oi,
                onTap: () => setState(() => sel = oi),
              ),
            );
          }),
          FilledButton(
            onPressed: sel == null
                ? null
                : () {
                    if (sel == q.correctIndex) correct++;
                    setState(() {
                      i++;
                      sel = null;
                    });
                  },
            child: Text(AppStrings.nextQuestion),
          ),
        ],
      ),
    );
  }
}
