import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';
import 'matric_practice_screen.dart';

/// Matriculation + Model papers. Catalog + live bank, clay UI.
class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  ExamCatalog? catalog;
  MatricBundle? bank;
  String? subjectFilter;
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

  List<ExamPaper> _merged(String type) {
    final fromCat = type == 'model'
        ? (catalog?.model ?? const <ExamPaper>[])
        : (catalog?.matriculation ?? const <ExamPaper>[]);
    final byKey = <String, ExamPaper>{};
    for (final p in fromCat) {
      byKey['${p.mappedSubject}|${p.year}|${p.type}'] = p;
    }
    final qs = bank?.questions ?? const <MatricQuestion>[];
    final counts = <String, int>{};
    for (final q in qs) {
      final t = (q.examType == 'model') ? 'model' : 'matriculation';
      if (t != type) continue;
      final k = '${q.subject}|${q.year}|$t';
      counts[k] = (counts[k] ?? 0) + 1;
    }
    for (final e in counts.entries) {
      final parts = e.key.split('|');
      final subject = parts[0];
      final year = int.tryParse(parts[1]) ?? 0;
      final existing = byKey[e.key];
      if (existing == null) {
        byKey[e.key] = ExamPaper(
          id: '${subject.toLowerCase()}-$year-$type',
          type: type,
          subject: subject,
          year: year,
          title: '$subject $year',
          driveFileId: '',
          source: 'bank',
          interactive: true,
          mappedSubject: subject,
          questionCount: e.value,
        );
      } else if (existing.questionCount < e.value) {
        byKey[e.key] = ExamPaper(
          id: existing.id,
          type: existing.type,
          subject: existing.subject,
          year: existing.year,
          title: existing.title,
          driveFileId: existing.driveFileId,
          source: existing.source,
          interactive: existing.interactive,
          mappedSubject: existing.mappedSubject,
          questionCount: e.value,
        );
      }
    }
    final list = byKey.values.toList()
      ..sort((a, b) {
        final y = b.year.compareTo(a.year);
        if (y != 0) return y;
        return a.mappedSubject.compareTo(b.mappedSubject);
      });
    return list;
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final matric = _merged('matriculation');
    final model = _merged('model');
    final subjects = <String>{
      ...matric.map((p) => p.mappedSubject),
      ...model.map((p) => p.mappedSubject),
    }.where((s) => s.isNotEmpty).toList()
      ..sort();
    final years = <int>{
      ...matric.map((p) => p.year),
      ...model.map((p) => p.year),
    }.where((y) => y > 0).toList()
      ..sort((a, b) => b.compareTo(a));

    List<ExamPaper> filter(List<ExamPaper> list) {
      var out = list;
      if (subjectFilter != null) {
        out = out.where((p) => p.mappedSubject == subjectFilter).toList();
      }
      if (yearFilter != null) {
        out = out.where((p) => p.year == yearFilter).toList();
      }
      return out;
    }

    return ColoredBox(
      color: FourTheme.bg,
      child: Column(
        children: [
          Container(
            width: double.infinity,
            padding: EdgeInsets.fromLTRB(16, top + 10, 16, 16),
            decoration: BoxDecoration(
              color: FourTheme.surface,
              borderRadius: const BorderRadius.only(
                bottomLeft: Radius.circular(28),
                bottomRight: Radius.circular(28),
              ),
              boxShadow: FourTheme.clay(small: true),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Exams',
                    style: TextStyle(
                        color: FourTheme.ink,
                        fontSize: 22,
                        fontWeight: FontWeight.w900)),
                Text(
                  loading
                      ? 'Loading…'
                      : '${bank?.questions.length ?? 0} questions · ${matric.length} matric · ${model.length} model',
                  style: const TextStyle(color: FourTheme.ink2, fontSize: 13),
                ),
                const SizedBox(height: 10),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _chip('All subjects', subjectFilter == null,
                          () => setState(() => subjectFilter = null)),
                      ...subjects.map((s) => _chip(
                            s.replaceAll('_', ' '),
                            subjectFilter == s,
                            () => setState(() => subjectFilter = s),
                          )),
                    ],
                  ),
                ),
                const SizedBox(height: 8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _chip('All years', yearFilter == null,
                          () => setState(() => yearFilter = null)),
                      ...years.map((y) => _chip(
                            '$y',
                            yearFilter == y,
                            () => setState(() => yearFilter = y),
                          )),
                    ],
                  ),
                ),
              ],
            ),
          ),
          if (loading)
            const Expanded(child: Center(child: CircularProgressIndicator()))
          else
            Expanded(
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  const Text('Matriculation',
                      style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w900,
                          color: FourTheme.ink)),
                  const SizedBox(height: 4),
                  Text(
                    years.isEmpty
                        ? 'No papers in this build yet.'
                        : 'Years ${years.join(', ')}',
                    style: const TextStyle(color: FourTheme.muted, fontSize: 12),
                  ),
                  const SizedBox(height: 10),
                  if (filter(matric).isEmpty)
                    const Text('No matric papers for this filter.',
                        style: TextStyle(color: FourTheme.muted))
                  else
                    ...filter(matric).map((p) => _PaperTile(paper: p)),
                  const SizedBox(height: 20),
                  const Text('Model exams',
                      style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w900,
                          color: FourTheme.ink)),
                  const SizedBox(height: 10),
                  if (filter(model).isEmpty)
                    const Text('No model papers for this filter.',
                        style: TextStyle(color: FourTheme.muted))
                  else
                    ...filter(model).map((p) => _PaperTile(paper: p)),
                  const SizedBox(height: 24),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _chip(String label, bool sel, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: sel ? FourTheme.coral : FourTheme.surface2,
            borderRadius: BorderRadius.circular(999),
          ),
          child: Text(
            label,
            style: TextStyle(
              color: sel ? Colors.white : FourTheme.ink,
              fontWeight: FontWeight.w800,
              fontSize: 12,
            ),
          ),
        ),
      ),
    );
  }
}

class _PaperTile extends StatelessWidget {
  const _PaperTile({required this.paper});
  final ExamPaper paper;

  @override
  Widget build(BuildContext context) {
    final tile = FourTheme.subjectTile(paper.mappedSubject);
    final deep = FourTheme.subjectDeep(paper.mappedSubject);
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
                subjectFilter: paper.mappedSubject,
                yearFilter: paper.year,
                title: paper.shortTitle,
              ),
            ),
          ),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(22),
              boxShadow: FourTheme.clay(small: true),
              border: Border.all(color: FourTheme.line),
            ),
            padding: const EdgeInsets.all(14),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: tile,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Icon(
                    paper.type == 'model'
                        ? Icons.folder_special_rounded
                        : Icons.assignment_rounded,
                    color: deep,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        paper.shortTitle,
                        style: const TextStyle(
                          fontWeight: FontWeight.w900,
                          color: FourTheme.ink,
                        ),
                      ),
                      Text(
                        paper.questionCount > 0
                            ? '${paper.questionCount} questions · ${paper.year}'
                            : 'Paper · ${paper.year}',
                        style: const TextStyle(
                          color: FourTheme.ink2,
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                        ),
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
