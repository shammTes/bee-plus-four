import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';
import '../bot/bot_screen.dart';
import 'matric_practice_screen.dart';

/// Pixel-close native ExamPrep / Warsay Prep shell.
class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  ExamCatalog? catalog;
  MatricBundle? bank;
  String inner = 'home'; // home subjects review tutor
  String cat = 'matric';
  String? subject;
  int? yearFilter;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final c = await ContentRepository.instance.examCatalog();
    final b = await ContentRepository.instance.matricBundle();
    if (!mounted) return;
    setState(() {
      catalog = c;
      bank = b;
      loading = false;
    });
  }

  List<ExamPaper> get papers {
    final out = <ExamPaper>[
      ...catalog?.matriculation ?? const [],
      ...catalog?.model ?? const [],
    ];
    if (out.isNotEmpty) return out;
    final seen = <String>{};
    for (final q in bank?.questions ?? const <MatricQuestion>[]) {
      final t = q.examType == 'model' ? 'model' : 'matriculation';
      final k = '${q.subject}|${q.year}|$t';
      if (!seen.add(k)) continue;
      out.add(ExamPaper(
        id: k,
        type: t,
        subject: q.subject,
        year: q.year,
        title: '${q.subject} ${q.year}',
        driveFileId: '',
        source: 'bank',
        interactive: true,
        mappedSubject: q.subject,
        questionCount: 0,
      ));
    }
    return out;
  }

  List<ExamPaper> get catPapers =>
      papers.where((p) => cat == 'model' ? p.type == 'model' : p.type != 'model').toList();

  List<String> subjectsOf(List<ExamPaper> list) {
    final s = list.map((p) => p.mappedSubject).where((e) => e.isNotEmpty).toSet().toList()..sort();
    return s;
  }

  String pretty(String s) => s.replaceAll('_', ' ');

  String greet() {
    final h = DateTime.now().hour;
    if (h < 12) return 'Good Morning';
    if (h < 17) return 'Good Afternoon';
    return 'Good Evening';
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    if (loading) {
      return const ColoredBox(color: FourTheme.bg, child: Center(child: CircularProgressIndicator()));
    }
    return ColoredBox(
      color: FourTheme.bg,
      child: Column(
        children: [
          Expanded(child: _body(top)),
          _examNav(),
        ],
      ),
    );
  }

  Widget _body(double top) {
    if (inner == 'tutor') return const BotScreen();
    if (inner == 'review') return _review(top);
    if (inner == 'subjects') {
      return subject == null ? _subjects(top) : _subjectDetail(top);
    }
    return _home(top);
  }

  Widget _examNav() {
    Widget tab(String id, IconData icon, String label) {
      final on = inner == id || (id == 'home' && inner == 'home');
      return Expanded(
        child: InkWell(
          onTap: () => setState(() {
            inner = id;
            if (id != 'subjects') subject = null;
          }),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 10),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(icon, color: on ? FourTheme.sageDeep : FourTheme.ink3),
                const SizedBox(height: 2),
                Text(label,
                    style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w800,
                        color: on ? FourTheme.sageDeep : FourTheme.ink3)),
              ],
            ),
          ),
        ),
      );
    }

    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 0, 14, 8),
      child: Container(
        decoration: BoxDecoration(
          color: FourTheme.surface,
          borderRadius: BorderRadius.circular(26),
          boxShadow: FourTheme.clay(small: true),
        ),
        child: Row(
          children: [
            tab('home', Icons.home_rounded, 'Home'),
            tab('subjects', Icons.grid_view_rounded, 'Subjects'),
            tab('review', Icons.bookmark_rounded, 'Review'),
            tab('tutor', Icons.chat_bubble_rounded, 'Tutor'),
          ],
        ),
      ),
    );
  }

  Widget _home(double top) {
    final qn = bank?.questions.length ?? 0;
    final all = papers;
    final years = all.map((p) => p.year).where((y) => y > 0).toSet().length;
    final week = List<int>.filled(7, 0);
    return ListView(
      padding: EdgeInsets.fromLTRB(16, top + 10, 16, 20),
      children: [
        const Text('Warsay Prep',
            style: TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: FourTheme.ink)),
        const Text('Grade 12 · Sawa matric practice',
            style: TextStyle(fontWeight: FontWeight.w700, color: FourTheme.ink2)),
        const SizedBox(height: 6),
        Text('${greet()} — Student',
            style: const TextStyle(fontWeight: FontWeight.w800, color: FourTheme.ink)),
        const SizedBox(height: 14),
        _coralCta('Continue studying', () {
          setState(() {
            inner = 'subjects';
            subject = subjectsOf(catPapers).isEmpty ? null : subjectsOf(catPapers).first;
          });
        }),
        const SizedBox(height: 14),
        Row(children: [
          _stat(FourTheme.sageTile, FourTheme.sageDeep, '$qn', 'Answered'),
          const SizedBox(width: 8),
          _stat(FourTheme.peachTile, FourTheme.peachDeep, '0%', 'Accuracy'),
          const SizedBox(width: 8),
          _stat(FourTheme.butterTile, FourTheme.butterDeep, '0m', 'Study'),
          const SizedBox(width: 8),
          _stat(FourTheme.blueTile, FourTheme.blueDeep, '0', 'Streak'),
        ]),
        const SizedBox(height: 16),
        _card(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('This week',
                  style: TextStyle(fontWeight: FontWeight.w900, color: FourTheme.ink)),
              const SizedBox(height: 10),
              SizedBox(height: 88, child: _WeekBars(values: week)),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          child: Row(
            children: [
              SizedBox(width: 120, height: 120, child: CustomPaint(painter: _DonutPainter())),
              const SizedBox(width: 12),
              const Expanded(
                child: Text(
                  'Answer 5 questions to see which topics you practise most — and how you score in each.',
                  style: TextStyle(fontWeight: FontWeight.w700, color: FourTheme.ink2, height: 1.4),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),
        _card(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Daily quiz',
                  style: TextStyle(fontWeight: FontWeight.w900, color: FourTheme.ink)),
              const SizedBox(height: 6),
              const Text('10 mixed MCQs · instant feedback',
                  style: TextStyle(color: FourTheme.ink2, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),
              _coralCta('Quiz me', () {
                if (all.isEmpty) return;
                final p = all.first;
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (_) => MatricPracticeScreen(
                    subjectFilter: p.mappedSubject,
                    yearFilter: p.year,
                    title: 'Daily quiz',
                  ),
                ));
              }),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Text('Subjects · $years years in bank',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: FourTheme.ink)),
        const SizedBox(height: 10),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          childAspectRatio: 1.28,
          children: subjectsOf(papers).map(_subjectTile).toList(),
        ),
      ],
    );
  }

  Widget _subjects(double top) {
    final list = catPapers;
    final years = list.map((p) => p.year).where((y) => y > 0).toSet().toList()..sort((a, b) => b.compareTo(a));
    final shown = yearFilter == null ? list : list.where((p) => p.year == yearFilter).toList();
    final subs = subjectsOf(shown);
    return ListView(
      padding: EdgeInsets.fromLTRB(16, top + 10, 16, 20),
      children: [
        const Text('Subjects',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: FourTheme.ink)),
        Text('${papers.length} exams · ${catalog?.matriculation.length ?? 0} matriculation · ${catalog?.model.length ?? 0} model',
            style: const TextStyle(color: FourTheme.ink2, fontWeight: FontWeight.w700)),
        const SizedBox(height: 12),
        Row(children: [
          _seg('Matriculation', cat == 'matric', () => setState(() {
                cat = 'matric';
                yearFilter = null;
              })),
          const SizedBox(width: 8),
          _seg('Model', cat == 'model', () => setState(() {
                cat = 'model';
                yearFilter = null;
              })),
        ]),
        const SizedBox(height: 10),
        SizedBox(
          height: 40,
          child: ListView(
            scrollDirection: Axis.horizontal,
            children: [
              _chip('All years', yearFilter == null, () => setState(() => yearFilter = null)),
              ...years.map((y) => _chip('$y', yearFilter == y, () => setState(() => yearFilter = y))),
            ],
          ),
        ),
        const SizedBox(height: 12),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          childAspectRatio: 1.2,
          children: subs.map(_subjectTile).toList(),
        ),
      ],
    );
  }

  Widget _subjectDetail(double top) {
    final list = catPapers.where((p) => p.mappedSubject == subject).toList()
      ..sort((a, b) => b.year.compareTo(a.year));
    final years = list.map((p) => p.year).where((y) => y > 0).toSet().toList()..sort((a, b) => b.compareTo(a));
    final shown = yearFilter == null ? list : list.where((p) => p.year == yearFilter).toList();
    final deep = FourTheme.subjectDeep(subject!);
    return Column(
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(4, top + 4, 16, 6),
          child: Row(
            children: [
              IconButton(
                onPressed: () => setState(() => subject = null),
                icon: const Icon(Icons.arrow_back_rounded, color: FourTheme.ink),
              ),
              Expanded(
                child: Text(pretty(subject!),
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: deep)),
              ),
            ],
          ),
        ),
        SizedBox(
          height: 40,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            children: [
              _chip('All', yearFilter == null, () => setState(() => yearFilter = null)),
              ...years.map((y) => _chip('$y', yearFilter == y, () => setState(() => yearFilter = y))),
            ],
          ),
        ),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.fromLTRB(16, 10, 16, 16),
            itemCount: shown.length,
            itemBuilder: (_, i) {
              final p = shown[i];
              return Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: _card(
                  child: ListTile(
                    contentPadding: EdgeInsets.zero,
                    leading: CircleAvatar(
                      backgroundColor: FourTheme.subjectTile(p.mappedSubject),
                      child: Text('${p.year}',
                          style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w900,
                              color: FourTheme.subjectDeep(p.mappedSubject))),
                    ),
                    title: Text(p.shortTitle,
                        style: const TextStyle(fontWeight: FontWeight.w900)),
                    subtitle: Text(
                      p.questionCount > 0 ? '${p.questionCount} questions' : 'Practice · instant feedback',
                      style: const TextStyle(fontWeight: FontWeight.w600, color: FourTheme.ink2),
                    ),
                    trailing: const Icon(Icons.play_circle_fill_rounded, color: FourTheme.coral),
                    onTap: () => Navigator.of(context).push(MaterialPageRoute(
                      builder: (_) => MatricPracticeScreen(
                        subjectFilter: p.mappedSubject,
                        yearFilter: p.year,
                        title: p.shortTitle,
                      ),
                    )),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _review(double top) {
    return ListView(
      padding: EdgeInsets.fromLTRB(16, top + 16, 16, 20),
      children: [
        const Text('Review',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: FourTheme.ink)),
        const SizedBox(height: 14),
        _card(
          child: const Padding(
            padding: EdgeInsets.symmetric(vertical: 20),
            child: Column(
              children: [
                Icon(Icons.bookmark_outline_rounded, size: 36, color: FourTheme.butterDeep),
                SizedBox(height: 8),
                Text('Bookmarks and mistakes live here',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontWeight: FontWeight.w800, color: FourTheme.ink)),
                SizedBox(height: 4),
                Text('Answer questions in a paper to fill this shelf.',
                    textAlign: TextAlign.center,
                    style: TextStyle(color: FourTheme.ink2, fontWeight: FontWeight.w600)),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _subjectTile(String s) {
    final n = papers.where((p) => p.mappedSubject == s).length;
    final tile = FourTheme.subjectTile(s);
    final deep = FourTheme.subjectDeep(s);
    return Material(
      color: tile,
      borderRadius: BorderRadius.circular(24),
      child: InkWell(
        borderRadius: BorderRadius.circular(24),
        onTap: () => setState(() {
          inner = 'subjects';
          subject = s;
        }),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.auto_stories_rounded, color: deep),
              const Spacer(),
              Text(pretty(s),
                  maxLines: 2,
                  style: TextStyle(fontWeight: FontWeight.w900, color: deep)),
              Text('$n exams · Not started',
                  style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: deep)),
              const SizedBox(height: 6),
              ClipRRect(
                borderRadius: BorderRadius.circular(99),
                child: LinearProgressIndicator(
                  value: 0,
                  minHeight: 6,
                  backgroundColor: Colors.white.withValues(alpha: 0.5),
                  color: deep,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _stat(Color tile, Color deep, String n, String label) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 6),
        decoration: BoxDecoration(
          color: tile,
          borderRadius: BorderRadius.circular(22),
          boxShadow: FourTheme.clay(small: true),
        ),
        child: Column(
          children: [
            Text(n, style: TextStyle(fontWeight: FontWeight.w900, color: deep, fontSize: 16)),
            Text(label, style: TextStyle(fontWeight: FontWeight.w800, color: deep, fontSize: 10)),
          ],
        ),
      ),
    );
  }

  Widget _coralCta(String label, VoidCallback onTap) {
    return Container(
      decoration: BoxDecoration(
        gradient: FourTheme.ctaGradient,
        borderRadius: BorderRadius.circular(999),
        boxShadow: FourTheme.clay(small: true),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(999),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 14),
            child: Center(
              child: Text(label,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16)),
            ),
          ),
        ),
      ),
    );
  }

  Widget _seg(String label, bool on, VoidCallback tap) {
    return Expanded(
      child: GestureDetector(
        onTap: tap,
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: on ? FourTheme.coral : FourTheme.surface2,
            borderRadius: BorderRadius.circular(999),
          ),
          child: Text(label,
              textAlign: TextAlign.center,
              style: TextStyle(
                  fontWeight: FontWeight.w800, color: on ? Colors.white : FourTheme.ink)),
        ),
      ),
    );
  }

  Widget _chip(String label, bool on, VoidCallback tap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: GestureDetector(
        onTap: tap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: on ? FourTheme.coral : FourTheme.surface,
            borderRadius: BorderRadius.circular(999),
          ),
          child: Text(label,
              style: TextStyle(
                  fontWeight: FontWeight.w800, color: on ? Colors.white : FourTheme.ink)),
        ),
      ),
    );
  }

  Widget _card({required Widget child}) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: FourTheme.surface,
        borderRadius: BorderRadius.circular(24),
        boxShadow: FourTheme.clay(small: true),
        border: Border.all(color: FourTheme.line),
      ),
      child: child,
    );
  }
}

class _WeekBars extends StatelessWidget {
  const _WeekBars({required this.values});
  final List<int> values;
  @override
  Widget build(BuildContext context) {
    const days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: List.generate(7, (i) {
        return Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 3),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Container(
                  height: 10 + (values[i] * 8).clamp(0, 60).toDouble(),
                  decoration: BoxDecoration(
                    color: FourTheme.sageMid,
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                const SizedBox(height: 4),
                Text(days[i],
                    style: const TextStyle(
                        fontSize: 10, fontWeight: FontWeight.w800, color: FourTheme.ink3)),
              ],
            ),
          ),
        );
      }),
    );
  }
}

class _DonutPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final c = Offset(size.width / 2, size.height / 2);
    final r = math.min(size.width, size.height) / 2 - 10;
    final bg = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 18
      ..color = FourTheme.surface2;
    canvas.drawCircle(c, r, bg);
    final tones = [
      FourTheme.peachMid,
      FourTheme.butterMid,
      FourTheme.sageMid,
      FourTheme.blueMid,
      FourTheme.lilacMid,
    ];
    var start = -math.pi / 2;
    for (var i = 0; i < tones.length; i++) {
      final sweep = (math.pi * 2) / tones.length * 0.08;
      canvas.drawArc(
        Rect.fromCircle(center: c, radius: r),
        start,
        sweep,
        false,
        Paint()
          ..style = PaintingStyle.stroke
          ..strokeCap = StrokeCap.round
          ..strokeWidth = 18
          ..color = tones[i],
      );
      start += sweep + 0.02;
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
