import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/theme/four_theme.dart';
import '../exams/exams_screen.dart';
import '../exams/matric_practice_screen.dart';
import '../labs/virtual_lab_screen.dart';
import '../notes/notes_screen.dart';
import '../practice/practice_screen.dart';
import '../textbooks/textbooks_screen.dart';

/// Dedicated page for one grade: Notes · Textbooks · Practice · Matric · Labs.
class GradeHubPage extends StatefulWidget {
  const GradeHubPage({
    super.key,
    required this.grade,
    this.onGradeSelected,
  });

  final String grade;
  final ValueChanged<String>? onGradeSelected;

  @override
  State<GradeHubPage> createState() => _GradeHubPageState();
}

class _GradeHubPageState extends State<GradeHubPage> {
  late String subject;
  String stream = CurriculumStreams.science;

  @override
  void initState() {
    super.initState();
    final allowed =
        CurriculumStreams.subjectsFor(widget.grade, stream: stream);
    subject = allowed.contains('MATH') ? 'MATH' : allowed.first;
    widget.onGradeSelected?.call(widget.grade);
  }

  Color get _accent {
    switch (widget.grade) {
      case 'G9':
        return const Color(0xFF0D9488);
      case 'G10':
        return const Color(0xFF0284C7);
      case 'G11':
        return const Color(0xFF7C3AED);
      case 'G12':
        return const Color(0xFFEA580C);
      default:
        return FourTheme.primary;
    }
  }

  void _openNotes() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => Scaffold(
          body: NotesScreen(
            grade: widget.grade,
            subject: subject,
            stream: stream,
            onGrade: (_) {},
            onSubject: (s) => setState(() => subject = s),
            onStream: (st) => setState(() {
              stream = st;
              final allowed =
                  CurriculumStreams.subjectsFor(widget.grade, stream: st);
              if (!allowed.contains(subject)) subject = allowed.first;
            }),
          ),
        ),
      ),
    );
  }

  void _openTextbooks() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => Scaffold(
          body: TextbooksScreen(initialGrade: widget.grade),
        ),
      ),
    );
  }

  void _openPractice() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => Scaffold(
          body: PracticeScreen(
            grade: widget.grade,
            subject: subject,
            onGrade: (_) {},
            onSubject: (s) => setState(() => subject = s),
          ),
        ),
      ),
    );
  }

  void _openMatric() {
    // Matric is national — show all papers; subject list for this grade as shortcut.
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => Scaffold(
          appBar: AppBar(
            title: Text('${widget.grade} · Matriculation',
                style: const TextStyle(fontWeight: FontWeight.w800)),
          ),
          body: const ExamsScreen(),
        ),
      ),
    );
  }

  void _openMatricSubject(String sub) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => MatricPracticeScreen(
          subjectFilter: sub,
          title: '${CurriculumStreams.label(sub)} · Matric',
        ),
      ),
    );
  }

  void _openLabs() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => Scaffold(
          appBar: AppBar(
            title: const Text('Virtual labs',
                style: TextStyle(fontWeight: FontWeight.w800)),
          ),
          body: const VirtualLabScreen(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    final subjects =
        CurriculumStreams.subjectsFor(widget.grade, stream: stream);
    final showStream = widget.grade == 'G11' || widget.grade == 'G12';

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: dark
                ? const [Color(0xFF0B1220), Color(0xFF111827)]
                : [Color.lerp(_accent, Colors.white, 0.92)!, Colors.white],
          ),
        ),
        child: CustomScrollView(
          slivers: [
            SliverAppBar(
              expandedHeight: 120,
              pinned: true,
              backgroundColor: _accent,
              foregroundColor: Colors.white,
              flexibleSpace: FlexibleSpaceBar(
                title: Text(
                  widget.grade,
                  style: const TextStyle(
                      fontWeight: FontWeight.w900, color: Colors.white),
                ),
                background: Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [_accent, Color.lerp(_accent, Colors.black, 0.25)!],
                    ),
                  ),
                  padding: const EdgeInsets.fromLTRB(16, 0, 16, 48),
                  alignment: Alignment.bottomLeft,
                  child: const Text(
                    'Notes · textbooks · practice · matric · labs',
                    style: TextStyle(
                        color: Colors.white70,
                        fontWeight: FontWeight.w600,
                        fontSize: 13),
                  ),
                ),
              ),
            ),
            if (showStream)
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(16, 12, 16, 0),
                  child: Row(
                    children: [
                      ChoiceChip(
                        label: const Text('Science'),
                        selected: stream == CurriculumStreams.science,
                        onSelected: (_) => setState(() {
                          stream = CurriculumStreams.science;
                          final a = CurriculumStreams.subjectsFor(
                              widget.grade,
                              stream: stream);
                          if (!a.contains(subject)) subject = a.first;
                        }),
                        selectedColor: const Color(0xFFFBBF24),
                        labelStyle: const TextStyle(
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF0F172A)),
                      ),
                      const SizedBox(width: 8),
                      ChoiceChip(
                        label: const Text('Arts'),
                        selected: stream == CurriculumStreams.arts,
                        onSelected: (_) => setState(() {
                          stream = CurriculumStreams.arts;
                          final a = CurriculumStreams.subjectsFor(
                              widget.grade,
                              stream: stream);
                          if (!a.contains(subject)) subject = a.first;
                        }),
                        selectedColor: const Color(0xFFFBBF24),
                        labelStyle: const TextStyle(
                            fontWeight: FontWeight.w900,
                            color: Color(0xFF0F172A)),
                      ),
                    ],
                  ),
                ),
              ),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
              sliver: SliverToBoxAdapter(
                child: Text(
                  'Study tools',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 14,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                  ),
                ),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              sliver: SliverList(
                delegate: SliverChildListDelegate([
                  _HubCard(
                    title: 'Notes',
                    subtitle: 'Unit notes · illustrated slides',
                    icon: Icons.auto_stories_rounded,
                    color: const Color(0xFF0D9488),
                    onTap: _openNotes,
                  ),
                  _HubCard(
                    title: 'Textbooks',
                    subtitle: '${widget.grade} offline PDF books',
                    icon: Icons.menu_book_rounded,
                    color: const Color(0xFF0F766E),
                    onTap: _openTextbooks,
                  ),
                  _HubCard(
                    title: 'Practice',
                    subtitle: 'Unit questions · mastery',
                    icon: Icons.quiz_rounded,
                    color: const Color(0xFF7C3AED),
                    onTap: _openPractice,
                  ),
                  _HubCard(
                    title: 'Matriculation exams',
                    subtitle: 'All years · subject + year papers',
                    icon: Icons.assignment_rounded,
                    color: const Color(0xFF4F46E5),
                    onTap: _openMatric,
                  ),
                  _HubCard(
                    title: 'Virtual labs',
                    subtitle: 'PhET offline · Physics · Chem · Bio · Math',
                    icon: Icons.science_rounded,
                    color: const Color(0xFF0EA5E9),
                    onTap: _openLabs,
                  ),
                ]),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
              sliver: SliverToBoxAdapter(
                child: Text(
                  'Matric by subject',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 14,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                  ),
                ),
              ),
            ),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 32),
              sliver: SliverToBoxAdapter(
                child: FutureBuilder(
                  future: ContentRepository.instance.matricBundle(),
                  builder: (context, snap) {
                    final counts = <String, int>{};
                    if (snap.hasData) {
                      for (final q in (snap.data as dynamic).questions as List) {
                        final s = q.subject as String;
                        counts[s] = (counts[s] ?? 0) + 1;
                      }
                    }
                    return Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: subjects.map((s) {
                        final n = counts[s];
                        return ActionChip(
                          avatar: Icon(Icons.assignment_outlined,
                              size: 16, color: _accent),
                          label: Text(
                            n == null
                                ? CurriculumStreams.label(s)
                                : '${CurriculumStreams.label(s)} · $n',
                            style: const TextStyle(fontWeight: FontWeight.w800),
                          ),
                          onPressed: () => _openMatricSubject(s),
                          backgroundColor:
                              dark ? const Color(0xFF1E293B) : Colors.white,
                          side: BorderSide(
                            color: dark
                                ? Colors.white12
                                : const Color(0xFFE2E8F0),
                          ),
                        );
                      }).toList(),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _HubCard extends StatelessWidget {
  const _HubCard({
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
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: dark ? const Color(0xFF1E293B) : Colors.white,
        borderRadius: BorderRadius.circular(18),
        elevation: dark ? 0 : 1,
        child: InkWell(
          borderRadius: BorderRadius.circular(18),
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              border: Border.all(
                color: dark ? Colors.white10 : color.withOpacity(0.2),
              ),
            ),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.15),
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
                          style: TextStyle(
                            fontWeight: FontWeight.w900,
                            fontSize: 16,
                            color: dark ? Colors.white : FourTheme.ink,
                          )),
                      const SizedBox(height: 2),
                      Text(subtitle,
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color:
                                dark ? FourTheme.darkMuted : FourTheme.muted,
                          )),
                    ],
                  ),
                ),
                Icon(Icons.chevron_right,
                    color: dark ? Colors.white38 : FourTheme.muted),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
