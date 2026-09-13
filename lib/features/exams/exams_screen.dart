import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/exam_models.dart';
import '../../core/theme/four_theme.dart';
import 'matric_practice_screen.dart';

class ExamsScreen extends StatefulWidget {
  const ExamsScreen({super.key});

  @override
  State<ExamsScreen> createState() => _ExamsScreenState();
}

class _ExamsScreenState extends State<ExamsScreen> {
  ExamCatalog? catalog;
  MatricBundle? bank;
  bool loading = true;
  String subjectFilter = 'ALL';

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
    final list = catalog?.matriculation ?? const <ExamPaper>[];
    if (subjectFilter == 'ALL') return list;
    return list.where((p) => p.mappedSubject == subjectFilter).toList();
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final subjects = <String>{
      'ALL',
      ...?catalog?.matriculation.map((p) => p.mappedSubject),
    }.toList();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsets.fromLTRB(20, top + 12, 20, 16),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFFD97706), Color(0xFFB45309)],
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
                      fontWeight: FontWeight.w800)),
              const SizedBox(height: 4),
              Text(
                '${bank?.questions.length ?? 0} questions · subject + year',
                style: const TextStyle(color: Color(0xFFFFEDD5), fontSize: 13),
              ),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects.map((s) {
                    final label = s == 'ALL'
                        ? 'All'
                        : s.replaceAll('_', ' ');
                    final sel = s == subjectFilter;
                    return Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: ChoiceChip(
                        label: Text(label),
                        selected: sel,
                        onSelected: (_) =>
                            setState(() => subjectFilter = s),
                        selectedColor: const Color(0xFFFBBF24),
                        backgroundColor: Colors.white,
                        labelStyle: const TextStyle(
                          color: Color(0xFF0F172A),
                          fontWeight: FontWeight.w900,
                          fontSize: 12,
                        ),
                      ),
                    );
                  }).toList(),
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
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: FourTheme.ink)),
                const SizedBox(height: 4),
                const Text('Titles show Subject and Year only',
                    style: TextStyle(color: FourTheme.muted, fontSize: 12)),
                const SizedBox(height: 10),
                ...papers.map((p) => Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: FourTheme.primarySoft,
                          child: Text('${p.year % 100}',
                              style: const TextStyle(
                                  fontWeight: FontWeight.w800,
                                  color: FourTheme.primaryDark,
                                  fontSize: 12)),
                        ),
                        // ONLY subject + year
                        title: Text(
                          p.shortTitle,
                          style: const TextStyle(fontWeight: FontWeight.w800),
                        ),
                        subtitle: Text(
                          p.questionCount > 0
                              ? '${p.questionCount} questions'
                              : 'Interactive',
                        ),
                        trailing: const Icon(Icons.play_circle_outline,
                            color: FourTheme.primary),
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => MatricPracticeScreen(
                              subjectFilter: p.mappedSubject,
                              yearFilter: p.year,
                              title: p.shortTitle,
                            ),
                          ),
                        ),
                      ),
                    )),
                const SizedBox(height: 20),
                const Text('Model & school exams',
                    style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: FourTheme.ink)),
                const SizedBox(height: 4),
                const Text(
                  'Catalogue folders — interactive JSON continues to grow as papers are parsed',
                  style: TextStyle(color: FourTheme.muted, fontSize: 12),
                ),
                const SizedBox(height: 10),
                ...?catalog?.modelYears.map((y) => Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: Icon(
                          y.type == 'school'
                              ? Icons.school_outlined
                              : Icons.folder_special_outlined,
                          color: FourTheme.primary,
                        ),
                        title: Text(y.label,
                            style:
                                const TextStyle(fontWeight: FontWeight.w700)),
                        subtitle: Text(y.type == 'school'
                            ? 'School exam'
                            : 'Model exam year'),
                      ),
                    )),
                const SizedBox(height: 24),
              ],
            ),
          ),
      ],
    );
  }
}
