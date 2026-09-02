import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/theme/four_theme.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({
    super.key,
    required this.grade,
    required this.onGrade,
    required this.onOpenNotes,
    required this.onOpenPractice,
    required this.onOpenBot,
    required this.onOpenExams,
  });

  final String grade;
  final ValueChanged<String> onGrade;
  final VoidCallback onOpenNotes;
  final VoidCallback onOpenPractice;
  final VoidCallback onOpenBot;
  final VoidCallback onOpenExams;

  static const grades = ['G9', 'G10', 'G11'];

  @override
  Widget build(BuildContext context) {
    final repo = ContentRepository.instance;

    return FutureBuilder(
      future: Future.wait([
        repo.notes(),
        repo.questions(),
        repo.matricBundle(),
        repo.allSlides(),
      ]),
      builder: (context, snap) {
        final noteCount = snap.hasData ? (snap.data![0] as List).length : '—';
        final qCount = snap.hasData ? (snap.data![1] as List).length : '—';
        final matricCount =
            snap.hasData ? (snap.data![2] as dynamic).questions.length : '—';
        final slideDecks =
            snap.hasData ? (snap.data![3] as Map).length : '—';

        return CustomScrollView(
          slivers: [
            SliverToBoxAdapter(
              child: Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [Color(0xFF0D9488), Color(0xFF0F766E)],
                  ),
                  borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(28),
                    bottomRight: Radius.circular(28),
                  ),
                ),
                padding: EdgeInsets.fromLTRB(
                  20,
                  MediaQuery.paddingOf(context).top + 16,
                  20,
                  28,
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 44,
                          height: 44,
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: const Icon(Icons.school_rounded, color: Colors.white),
                        ),
                        const SizedBox(width: 12),
                        const Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                '4 · BEE PLUS',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 22,
                                  fontWeight: FontWeight.w800,
                                ),
                              ),
                              Text(
                                'Highschool · Offline study',
                                style: TextStyle(color: Color(0xFFCCFBF1), fontSize: 13),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    const Text('Choose your grade',
                        style: TextStyle(color: Colors.white70, fontSize: 12)),
                    const SizedBox(height: 8),
                    Row(
                      children: grades.map((g) {
                        final selected = g == grade;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(g),
                            selected: selected,
                            onSelected: (_) => onGrade(g),
                            selectedColor: Colors.white,
                            labelStyle: TextStyle(
                              color: selected ? FourTheme.primaryDark : Colors.white,
                              fontWeight: FontWeight.w700,
                            ),
                            backgroundColor: Colors.white.withOpacity(0.15),
                            side: BorderSide.none,
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            ),
            const SliverToBoxAdapter(child: SizedBox(height: 16)),
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              sliver: SliverGrid(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  mainAxisSpacing: 10,
                  crossAxisSpacing: 10,
                  childAspectRatio: 1.55,
                ),
                delegate: SliverChildListDelegate([
                  _StatTile('$noteCount', 'Unit notes', Icons.menu_book_rounded),
                  _StatTile('$qCount', 'Practice Qs', Icons.quiz_rounded),
                  _StatTile('$matricCount', 'Matric items', Icons.assignment_rounded),
                  _StatTile('$slideDecks', 'Illustrations', Icons.slideshow_rounded),
                ]),
              ),
            ),
            const SliverToBoxAdapter(
              child: Padding(
                padding: EdgeInsets.fromLTRB(20, 24, 20, 10),
                child: Text(
                  'Continue studying',
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: FontWeight.w800,
                    color: FourTheme.ink,
                  ),
                ),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              sliver: SliverList.list(
                children: [
                  _ActionCard(
                    title: 'Notes & illustrated',
                    subtitle: 'Unit summaries · swipeable decks',
                    icon: Icons.auto_stories_rounded,
                    color: const Color(0xFF0D9488),
                    onTap: onOpenNotes,
                  ),
                  _ActionCard(
                    title: 'Practice MCQs',
                    subtitle: 'Explanations · similar questions',
                    icon: Icons.quiz_rounded,
                    color: const Color(0xFF2563EB),
                    onTap: onOpenPractice,
                  ),
                  _ActionCard(
                    title: 'Study coach',
                    subtitle: 'Offline hints · controlled Q&A',
                    icon: Icons.smart_toy_rounded,
                    color: const Color(0xFF7C3AED),
                    onTap: onOpenBot,
                  ),
                  _ActionCard(
                    title: 'Matric & model exams',
                    subtitle: 'Catalogue · step-by-step solutions',
                    icon: Icons.assignment_rounded,
                    color: const Color(0xFFD97706),
                    onTap: onOpenExams,
                  ),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ],
        );
      },
    );
  }
}

class _StatTile extends StatelessWidget {
  const _StatTile(this.value, this.label, this.icon);
  final String value;
  final String label;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Icon(icon, size: 20, color: FourTheme.primary),
            const Spacer(),
            Text(value,
                style: const TextStyle(
                    fontSize: 22, fontWeight: FontWeight.w800, color: FourTheme.ink)),
            Text(label, style: const TextStyle(fontSize: 12, color: FourTheme.muted)),
          ],
        ),
      ),
    );
  }
}

class _ActionCard extends StatelessWidget {
  const _ActionCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.onTap,
  });

  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(18),
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              border: Border.all(color: color.withOpacity(0.12)),
            ),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Icon(icon, color: color),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(title,
                          style: const TextStyle(
                              fontWeight: FontWeight.w700,
                              fontSize: 15,
                              color: FourTheme.ink)),
                      const SizedBox(height: 2),
                      Text(subtitle,
                          style: const TextStyle(fontSize: 12, color: FourTheme.muted)),
                    ],
                  ),
                ),
                Icon(Icons.chevron_right_rounded, color: color.withOpacity(0.5)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
