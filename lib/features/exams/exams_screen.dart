import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';
import 'matric_practice_screen.dart';

/// Matriculation + Model full papers with year chips.
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

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final matric = catalog?.matriculation ?? const <ExamPaper>[];
    final model = catalog?.model ?? const <ExamPaper>[];
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

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFFEA580C), Color(0xFFC2410C)],
            ),
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Exams',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              Text(
                loading
                    ? 'Loading…'
                    : '${bank?.questions.length ?? 0} questions · ${matric.length} matric papers · ${model.length} model',
                style: const TextStyle(color: Color(0xFFFED7AA), fontSize: 13),
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
              const SizedBox(height: 6),
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
                  'Years in bank: ${matric.map((p) => p.year).toSet().toList()..sort((a, b) => b.compareTo(a))}',
                  style: const TextStyle(color: FourTheme.muted, fontSize: 11),
                ),
                const SizedBox(height: 8),
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
                const SizedBox(height: 4),
                const Text('Subject + year · full paper',
                    style: TextStyle(color: FourTheme.muted, fontSize: 12)),
                const SizedBox(height: 8),
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
    );
  }

  Widget _chip(String label, bool sel, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 6),
      child: ChoiceChip(
        label: Text(label),
        selected: sel,
        onSelected: (_) => onTap(),
        selectedColor: const Color(0xFFFBBF24),
        backgroundColor: Colors.white,
        labelStyle: const TextStyle(
          color: Color(0xFF0F172A),
          fontWeight: FontWeight.w900,
          fontSize: 12,
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
    final color = paper.type == 'model'
        ? const Color(0xFF7C3AED)
        : FourTheme.primary;
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(
          paper.type == 'model' ? Icons.folder_special : Icons.assignment,
          color: color,
        ),
        title: Text(
          paper.shortTitle,
          style: const TextStyle(fontWeight: FontWeight.w800),
        ),
        subtitle: Text(
          paper.questionCount > 0
              ? '${paper.questionCount} questions · ${paper.year}'
              : 'Interactive · ${paper.year}',
        ),
        trailing: Icon(Icons.play_circle_outline, color: color),
        onTap: () => Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => MatricPracticeScreen(
              subjectFilter: paper.mappedSubject,
              yearFilter: paper.year,
              title: paper.shortTitle,
            ),
          ),
        ),
      ),
    );
  }
}
