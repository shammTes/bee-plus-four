import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';
import 'matric_practice_screen.dart';

/// Native Warsay Prep / ExamPrep clay home — same layout as the preview.
class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  ExamCatalog? catalog;
  MatricBundle? bank;
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

  List<ExamPaper> get _allPapers {
    final out = <ExamPaper>[];
    out.addAll(catalog?.matriculation ?? const []);
    out.addAll(catalog?.model ?? const []);
    if (out.isEmpty && bank != null) {
      final keys = <String>{};
      for (final q in bank!.questions) {
        final k = '${q.subject}|${q.year}|${q.examType}';
        if (!keys.add(k)) continue;
        out.add(ExamPaper(
          id: k,
          type: q.examType == 'model' ? 'model' : 'matriculation',
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
    }
    return out;
  }

  List<String> get _subjects {
    final s = _allPapers.map((p) => p.mappedSubject).where((e) => e.isNotEmpty).toSet().toList()
      ..sort();
    return s;
  }

  String _pretty(String s) => s.replaceAll('_', ' ');

  String _greet() {
    final h = DateTime.now().hour;
    if (h < 12) return 'Good morning';
    if (h < 17) return 'Good afternoon';
    return 'Good evening';
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    if (loading) {
      return const ColoredBox(
        color: FourTheme.bg,
        child: Center(child: CircularProgressIndicator()),
      );
    }
    return ColoredBox(
      color: FourTheme.bg,
      child: subject == null ? _home(top) : _subject(top),
    );
  }

  Widget _home(double top) {
    final qn = bank?.questions.length ?? 0;
    final papers = _allPapers;
    final years = papers.map((p) => p.year).where((y) => y > 0).toSet().toList()..sort((a, b) => b.compareTo(a));
    return ListView(
      padding: EdgeInsets.fromLTRB(16, top + 12, 16, 28),
      children: [
        const Text('Warsay Prep',
            style: TextStyle(
                fontSize: 26, fontWeight: FontWeight.w900, color: FourTheme.ink)),
        const Text('Grade 12 · Sawa matric practice',
            style: TextStyle(
                fontSize: 14, fontWeight: FontWeight.w700, color: FourTheme.ink2)),
        const SizedBox(height: 8),
        Text('${_greet()} — pick a subject and start.',
            style: const TextStyle(color: FourTheme.ink2, fontWeight: FontWeight.w600)),
        const SizedBox(height: 16),
        Container(
          decoration: BoxDecoration(
            gradient: FourTheme.ctaGradient,
            borderRadius: BorderRadius.circular(999),
            boxShadow: FourTheme.clay(small: true),
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              borderRadius: BorderRadius.circular(999),
              onTap: () {
                if (_subjects.isNotEmpty) setState(() => subject = _subjects.first);
              },
              child: const Padding(
                padding: EdgeInsets.symmetric(horizontal: 22, vertical: 16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.play_arrow_rounded, color: Colors.white),
                    SizedBox(width: 8),
                    Text('Continue studying',
                        style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.w900,
                            fontSize: 16)),
                  ],
                ),
              ),
            ),
          ),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            _stat(FourTheme.sageTile, FourTheme.sageDeep, '$qn', 'Questions'),
            const SizedBox(width: 10),
            _stat(FourTheme.peachTile, FourTheme.peachDeep, '${papers.length}', 'Papers'),
            const SizedBox(width: 10),
            _stat(FourTheme.butterTile, FourTheme.butterDeep, '${years.length}', 'Years'),
            const SizedBox(width: 10),
            _stat(FourTheme.blueTile, FourTheme.blueDeep, '${_subjects.length}', 'Subjects'),
          ],
        ),
        const SizedBox(height: 22),
        const Text('Subjects',
            style: TextStyle(
                fontSize: 18, fontWeight: FontWeight.w900, color: FourTheme.ink)),
        const SizedBox(height: 12),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          childAspectRatio: 1.35,
          children: _subjects.map(_subjectTile).toList(),
        ),
      ],
    );
  }

  Widget _stat(Color tile, Color deep, String n, String label) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 8),
        decoration: BoxDecoration(
          color: tile,
          borderRadius: BorderRadius.circular(22),
          boxShadow: FourTheme.clay(small: true),
        ),
        child: Column(
          children: [
            Text(n,
                style: TextStyle(
                    fontSize: 18, fontWeight: FontWeight.w900, color: deep)),
            Text(label,
                style: TextStyle(
                    fontSize: 11, fontWeight: FontWeight.w800, color: deep)),
          ],
        ),
      ),
    );
  }

  Widget _subjectTile(String s) {
    final n = _allPapers.where((p) => p.mappedSubject == s).length;
    final tile = FourTheme.subjectTile(s);
    final deep = FourTheme.subjectDeep(s);
    return Material(
      color: tile,
      borderRadius: BorderRadius.circular(24),
      child: InkWell(
        borderRadius: BorderRadius.circular(24),
        onTap: () => setState(() {
          subject = s;
          yearFilter = null;
        }),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.auto_stories_rounded, color: deep),
              const Spacer(),
              Text(_pretty(s),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                      fontWeight: FontWeight.w900, fontSize: 15, color: deep)),
              Text('$n papers',
                  style: TextStyle(
                      fontWeight: FontWeight.w700, fontSize: 12, color: deep.withValues(alpha: 0.8))),
            ],
          ),
        ),
      ),
    );
  }

  Widget _subject(double top) {
    final papers = _allPapers.where((p) => p.mappedSubject == subject).toList()
      ..sort((a, b) => b.year.compareTo(a.year));
    final years = papers.map((p) => p.year).where((y) => y > 0).toSet().toList()..sort((a, b) => b.compareTo(a));
    final shown = yearFilter == null
        ? papers
        : papers.where((p) => p.year == yearFilter).toList();
    final deep = FourTheme.subjectDeep(subject!);
    return Column(
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(8, top + 6, 16, 8),
          child: Row(
            children: [
              IconButton(
                onPressed: () => setState(() => subject = null),
                icon: const Icon(Icons.arrow_back_rounded),
                color: FourTheme.ink,
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(_pretty(subject!),
                        style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w900,
                            color: deep)),
                    Text('${papers.length} papers',
                        style: const TextStyle(
                            color: FourTheme.ink2, fontWeight: FontWeight.w700)),
                  ],
                ),
              ),
            ],
          ),
        ),
        SizedBox(
          height: 42,
          child: ListView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            children: [
              _yearChip('All', yearFilter == null, () => setState(() => yearFilter = null)),
              ...years.map((y) => _yearChip(
                    '$y',
                    yearFilter == y,
                    () => setState(() => yearFilter = y),
                  )),
            ],
          ),
        ),
        const SizedBox(height: 8),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
            itemCount: shown.length,
            itemBuilder: (_, i) => _paper(shown[i]),
          ),
        ),
      ],
    );
  }

  Widget _yearChip(String label, bool on, VoidCallback tap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: GestureDetector(
        onTap: tap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: on ? FourTheme.coral : FourTheme.surface,
            borderRadius: BorderRadius.circular(999),
            boxShadow: on ? FourTheme.clay(small: true) : null,
          ),
          child: Text(label,
              style: TextStyle(
                  fontWeight: FontWeight.w800,
                  color: on ? Colors.white : FourTheme.ink)),
        ),
      ),
    );
  }

  Widget _paper(ExamPaper p) {
    final tile = FourTheme.subjectTile(p.mappedSubject);
    final deep = FourTheme.subjectDeep(p.mappedSubject);
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: FourTheme.surface,
        borderRadius: BorderRadius.circular(22),
        child: InkWell(
          borderRadius: BorderRadius.circular(22),
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute(
              builder: (_) => MatricPracticeScreen(
                subjectFilter: p.mappedSubject,
                yearFilter: p.year,
                title: p.shortTitle,
              ),
            ),
          ),
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(22),
              boxShadow: FourTheme.clay(small: true),
              border: Border.all(color: FourTheme.line),
            ),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  alignment: Alignment.center,
                  decoration: BoxDecoration(
                    color: tile,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Text('${p.year}',
                      style: TextStyle(
                          fontWeight: FontWeight.w900, color: deep, fontSize: 13)),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(p.shortTitle,
                          style: const TextStyle(
                              fontWeight: FontWeight.w900, color: FourTheme.ink)),
                      Text(
                        p.questionCount > 0
                            ? '${p.questionCount} questions'
                            : (p.type == 'model' ? 'Model paper' : 'Matric paper'),
                        style: const TextStyle(
                            color: FourTheme.ink2, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
                const Icon(Icons.play_circle_fill_rounded, color: FourTheme.coral),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
