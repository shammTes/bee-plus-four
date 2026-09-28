import 'package:flutter/material.dart';

import '../../core/theme/four_theme.dart';
import 'matric_practice_screen.dart';

/// Native 4 exams home. Warsay Prep is the floating window, not this tab.
class ExamsScreen extends StatelessWidget {
  const ExamsScreen({super.key, this.onOpenWarsay});

  final VoidCallback? onOpenWarsay;

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return Column(
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
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Exams',
                  style: TextStyle(
                      color: FourTheme.ink,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              SizedBox(height: 4),
              Text(
                '4 papers stay here. Warsay Prep floats on top.',
                style: TextStyle(
                    color: FourTheme.ink2, fontWeight: FontWeight.w600),
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _Tile(
                icon: Icons.assignment_rounded,
                title: 'Matriculation bank',
                subtitle: 'Native 4 questions, years, answers',
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => const MatricPracticeScreen(),
                  ),
                ),
              ),
              const SizedBox(height: 10),
              _Tile(
                icon: Icons.auto_awesome,
                title: 'Open Warsay Prep',
                subtitle: 'Small floating window — 4 nav stays',
                tone: FourTheme.coral,
                onTap: onOpenWarsay,
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _Tile extends StatelessWidget {
  const _Tile({
    required this.icon,
    required this.title,
    required this.subtitle,
    this.onTap,
    this.tone = FourTheme.ok,
  });
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback? onTap;
  final Color tone;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: FourTheme.surface,
      elevation: 0,
      borderRadius: BorderRadius.circular(24),
      shadowColor: FourTheme.tint.withValues(alpha: 0.3),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(24),
        child: Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),
            boxShadow: FourTheme.clay(small: true),
          ),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: tone.withValues(alpha: 0.25),
                child: Icon(icon, color: FourTheme.ink),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title,
                        style: const TextStyle(
                            fontWeight: FontWeight.w900, fontSize: 16)),
                    Text(subtitle,
                        style: const TextStyle(
                            color: FourTheme.ink2, fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
              const Icon(Icons.chevron_right, color: FourTheme.muted),
            ],
          ),
        ),
      ),
    );
  }
}
