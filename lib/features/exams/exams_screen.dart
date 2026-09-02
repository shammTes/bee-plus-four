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
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Exams',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w800)),
              SizedBox(height: 4),
              Text('Matric · model · school catalogue',
                  style: TextStyle(color: Color(0xFFFFEDD5), fontSize: 13)),
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
                const Text('Interactive matric bank',
                    style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: FourTheme.ink)),
                const SizedBox(height: 10),
                Card(
                  child: ListTile(
                    leading: const CircleAvatar(
                      backgroundColor: Color(0xFFFFEDD5),
                      child: Icon(Icons.bolt, color: Color(0xFFD97706)),
                    ),
                    title: Text(
                      '${bank?.questions.length ?? 0} verified questions',
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                    subtitle: const Text('Step-by-step · similar practice'),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => const MatricPracticeScreen(),
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 20),
                const Text('Matriculation papers',
                    style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: FourTheme.ink)),
                const SizedBox(height: 10),
                ...?catalog?.matriculation.map((p) => Card(
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
                        title: Text(p.title,
                            style: const TextStyle(fontWeight: FontWeight.w600)),
                        subtitle: Text('${p.subject} · ${p.source}'),
                        trailing: const Icon(Icons.play_circle_outline,
                            color: FourTheme.primary),
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => MatricPracticeScreen(
                              subjectFilter: p.mappedSubject,
                              title: p.title,
                            ),
                          ),
                        ),
                      ),
                    )),
                const SizedBox(height: 20),
                const Text('Years & folders',
                    style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: FourTheme.ink)),
                const SizedBox(height: 10),
                ...?catalog?.modelYears.map((y) => Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: const Icon(Icons.folder_special_outlined,
                            color: FourTheme.primary),
                        title: Text(y.label,
                            style: const TextStyle(fontWeight: FontWeight.w600)),
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
