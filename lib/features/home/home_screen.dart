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
    this.onOpenTools,
  });

  final String grade;
  final ValueChanged<String> onGrade;
  final VoidCallback onOpenNotes;
  final VoidCallback onOpenPractice;
  final VoidCallback onOpenBot;
  final VoidCallback onOpenExams;
  final VoidCallback? onOpenTools;

  static const grades = ['G9', 'G10', 'G11', 'G12'];

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

        return Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [Color(0xFFE0F2FE), Color(0xFFF5F3FF), Color(0xFFF8FAFC)],
            ),
          ),
          child: CustomScrollView(
            slivers: [
              ConcurrentlyHomeHero(
                grade: grade,
                onGrade: onGrade,
                noteCount: '$noteCount',
                qCount: '$qCount',
                matricCount: '$matricCount',
                slideDecks: '$slideDecks',
                onOpenNotes: onOpenNotes,
                onOpenPractice: onOpenPractice,
                onOpenBot: onOpenBot,
                onOpenExams: onOpenExams,
                onOpenTools: onOpenTools,
              ),
            ],
          ),
        );
      },
    );
  }
}

// Inline hero+body kept as one widget tree without ConcurrentlyHomeHero - rewrite simple
class ConcurrentlyHomeHero extends StatelessWidget {
  const ConcurrentlyHomeHero({
    super.key,
    required this.grade,
    required this.onGrade,
    required this.noteCount,
    required this.qCount,
    required this.matricCount,
    required this.slideDecks,
    required this.onOpenNotes,
    required this.onOpenPractice,
    required this.onOpenBot,
    required this.onOpenExams,
    this.onOpenTools,
  });
  final String grade;
  final ValueChanged<String> onGrade;
  final String noteCount, qCount, matricCount, slideDecks;
  final VoidCallback onOpenNotes, onOpenPractice, onOpenBot, onOpenExams;
  final VoidCallback? onOpenTools;

  static const grades = ['G9', 'G10', 'G11', 'G12'];

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          width: double.infinity,
          decoration: const BoxDecoration(
            gradient: FourTheme.heroGradient,
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(28),
              bottomRight: Radius.circular(28),
            ),
          ),
          padding: EdgeInsets.fromLTRB(
            20,
            MediaQuery.paddingOf(context).top + 16,
            20,
            26,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: Colors.white54),
                    ),
                    child: const Icon(Icons.school_rounded,
                        color: Colors.white, size: 28),
                  ),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('BEE PLUS 4',
                            style: TextStyle(
                                color: Colors.white,
                                fontSize: 22,
                                fontWeight: FontWeight.w900)),
                        Text('Highschool · offline',
                            style: TextStyle(
                                color: Color(0xFFCCFBF1), fontSize: 13)),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 18),
              const Text('Your grade',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 12,
                      fontWeight: FontWeight.w700)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                children: grades.map((g) {
                  final selected = g == grade;
                  return ChoiceChip(
                    label: Text(g),
                    selected: selected,
                    onSelected: (_) => onGrade(g),
                    selectedColor: const Color(0xFFFBBF24),
                    labelStyle: const TextStyle(
                      color: Color(0xFF0F172A),
                      fontWeight: FontWeight.w900,
                      fontSize: 13,
                    ),
                    backgroundColor: Colors.white,
                    side: const BorderSide(color: Color(0xFFE2E8F0)),
                  );
                }).toList(),
              ),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
          child: GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 2,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 1.55,
            children: [
              _StatTile(noteCount, 'Notes', Icons.menu_book_rounded, FourTheme.primary),
              _StatTile(qCount, 'MCQs', Icons.quiz_rounded, FourTheme.violet),
              _StatTile(matricCount, 'Matric', Icons.assignment_rounded, FourTheme.accentDeep),
              _StatTile(slideDecks, 'Decks', Icons.slideshow_rounded, FourTheme.mint),
            ],
          ),
        ),
        const Padding(
          padding: EdgeInsets.fromLTRB(20, 22, 20, 10),
          child: Align(
            alignment: Alignment.centerLeft,
            child: Text('Study',
                style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                    color: FourTheme.ink)),
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Column(
            children: [
              _ActionCard(
                title: 'Notes',
                subtitle: 'Units · PDF packs',
                icon: Icons.auto_stories_rounded,
                color: const Color(0xFF0E7490),
                onTap: onOpenNotes,
              ),
              _ActionCard(
                title: 'Practice',
                subtitle: 'MCQs · feedback',
                icon: Icons.quiz_rounded,
                color: const Color(0xFF6366F1),
                onTap: onOpenPractice,
              ),
              _ActionCard(
                title: 'Coach',
                subtitle: 'Offline quiz bot',
                icon: Icons.smart_toy_rounded,
                color: const Color(0xFF8B5CF6),
                onTap: onOpenBot,
              ),
              _ActionCard(
                title: 'Exams',
                subtitle: 'Matric · model',
                icon: Icons.assignment_rounded,
                color: const Color(0xFFD97706),
                onTap: onOpenExams,
              ),
              if (onOpenTools != null)
                _ActionCard(
                  title: 'Tools',
                  subtitle: 'Labs · utilities',
                  icon: Icons.handyman_rounded,
                  color: const Color(0xFF059669),
                  onTap: onOpenTools!,
                ),
              const SizedBox(height: 28),
            ],
          ),
        ),
      ],
    );
  }
}

class _StatTile extends StatelessWidget {
  const _StatTile(this.value, this.label, this.icon, this.color);
  final String value;
  final String label;
  final IconData icon;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return FourTheme.glassPanel(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 22),
          const Spacer(),
          Text(value,
              style: const TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w900,
                  color: FourTheme.ink)),
          Text(label,
              style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  color: FourTheme.muted)),
        ],
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
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: onTap,
          child: Ink(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
              gradient: LinearGradient(
                colors: [color, color.withOpacity(0.82)],
              ),
              boxShadow: [
                BoxShadow(
                  color: color.withOpacity(0.28),
                  blurRadius: 14,
                  offset: const Offset(0, 6),
                ),
              ],
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 46,
                    height: 46,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Icon(icon, color: Colors.white, size: 26),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(title,
                            style: const TextStyle(
                                color: Colors.white,
                                fontSize: 17,
                                fontWeight: FontWeight.w900)),
                        Text(subtitle,
                            style: TextStyle(
                                color: Colors.white.withOpacity(0.88),
                                fontSize: 12,
                                fontWeight: FontWeight.w600)),
                      ],
                    ),
                  ),
                  const Icon(Icons.arrow_forward_ios_rounded,
                      color: Colors.white70, size: 16),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
