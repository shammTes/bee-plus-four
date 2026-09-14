import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';
import 'matric_practice_screen.dart';

/// Matriculation + Model full papers.
/// School exam items live in unit Practice (linked by unit).
class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  ExamCatalog? catalog;
  MatricBundle? bank;
  String? subjectFilter;
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

    List<ExamPaper> filter(List<ExamPaper> list) {
      if (subjectFilter == null) return list;
      return list.where((p) => p.mappedSubject == subjectFilter).toList();
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
                    : '${bank?.questions.length ?? 0} in bank · ${matric.length} matric · ${model.length} model',
                style: const TextStyle(color: Color(0xFFFED7AA), fontSize: 13),
              ),
              const SizedBox(height: 4),
              const Text(
                'School exam items are inside unit Practice',
                style: TextStyle(color: Color(0xFFFED7AA), fontSize: 11),
              ),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: ChoiceChip(
                        label: const Text('All'),
                        selected: subjectFilter == null,
                        onSelected: (_) =>
                            setState(() => subjectFilter = null),
                        selectedColor: const Color(0xFFFBBF24),
                        backgroundColor: Colors.white,
                        labelStyle: const TextStyle(
                          color: Color(0xFF0F172A),
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                    ...subjects.map((s) => Padding(
                          padding: const EdgeInsets.only(right: 6),
                          child: ChoiceChip(
                            label: Text(s.replaceAll('_', ' ')),
                            selected: subjectFilter == s,
                            onSelected: (_) =>
                                setState(() => subjectFilter = s),
                            selectedColor: const Color(0xFFFBBF24),
                            backgroundColor: Colors.white,
                            labelStyle: const TextStyle(
                              color: Color(0xFF0F172A),
                              fontWeight: FontWeight.w900,
                            ),
                          ),
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
                const SizedBox(height: 8),
                ...filter(matric).map((p) => _PaperTile(paper: p)),
                const SizedBox(height: 20),
                const Text('Model exams',
                    style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w900,
                        color: FourTheme.ink)),
                const SizedBox(height: 4),
                const Text('Subject + year · full paper practice',
                    style: TextStyle(color: FourTheme.muted, fontSize: 12)),
                const SizedBox(height: 8),
                if (filter(model).isEmpty)
                  const Text('No model papers in filter.',
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
              ? '${paper.questionCount} questions'
              : 'Interactive',
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
