import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';
import '../exams/matric_practice_screen.dart';

class NotesScreen extends StatefulWidget {
  const NotesScreen({
    super.key,
    required this.grade,
    required this.subject,
    required this.onGrade,
    required this.onSubject,
  });

  final String grade;
  final String subject;
  final ValueChanged<String> onGrade;
  final ValueChanged<String> onSubject;

  @override
  State<NotesScreen> createState() => _NotesScreenState();
}

class _NotesScreenState extends State<NotesScreen> {
  static const subjects = [
    'MATH', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'ENGLISH',
    'GEOGRAPHY', 'HISTORY', 'AGRICULTURE', 'BUSINESS_ECONOMICS',
  ];

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF0D9488), Color(0xFF0F766E)],
            ),
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Notes',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w800)),
              const SizedBox(height: 4),
              const Text('Unit notes · illustrated decks · matric links',
                  style: TextStyle(color: Color(0xFFCCFBF1), fontSize: 13)),
              const SizedBox(height: 12),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11'].map((g) {
                    final sel = g == widget.grade;
                    return Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: ChoiceChip(
                        label: Text(g),
                        selected: sel,
                        onSelected: (_) => widget.onGrade(g),
                        selectedColor: Colors.white,
                        labelStyle: TextStyle(
                          color: sel ? FourTheme.primaryDark : Colors.white,
                          fontWeight: FontWeight.w700,
                          fontSize: 12,
                        ),
                        backgroundColor: Colors.white.withOpacity(0.15),
                        side: BorderSide.none,
                        visualDensity: VisualDensity.compact,
                      ),
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects.map((s) {
                    final sel = s == widget.subject;
                    final label = s == 'BUSINESS_ECONOMICS'
                        ? 'Business'
                        : s[0] + s.substring(1).toLowerCase();
                    return Padding(
                      padding: const EdgeInsets.only(right: 6),
                      child: FilterChip(
                        label: Text(label),
                        selected: sel,
                        onSelected: (_) => widget.onSubject(s),
                        selectedColor: Colors.white,
                        labelStyle: TextStyle(
                          color: sel ? FourTheme.primaryDark : Colors.white,
                          fontWeight: FontWeight.w600,
                          fontSize: 11,
                        ),
                        backgroundColor: Colors.white.withOpacity(0.12),
                        side: BorderSide.none,
                        visualDensity: VisualDensity.compact,
                      ),
                    );
                  }).toList(),
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              const Text('Illustrated deck',
                  style: TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 15,
                      color: FourTheme.ink)),
              const SizedBox(height: 10),
              Material(
                borderRadius: BorderRadius.circular(18),
                child: InkWell(
                  borderRadius: BorderRadius.circular(18),
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => const IllustratedDeckPage(
                        deckId: 'g6-math-1',
                        title: 'Banuna Pizzeria',
                        subtitle: 'Quantities · equations · tables',
                      ),
                    ),
                  ),
                  child: Container(
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(18),
                      gradient: const LinearGradient(
                        colors: [Color(0xFF134E4A), Color(0xFF0D9488)],
                      ),
                    ),
                    padding: const EdgeInsets.all(16),
                    child: const Row(
                      children: [
                        Icon(Icons.auto_stories, color: Colors.white, size: 40),
                        SizedBox(width: 14),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Illustrated notes',
                                  style: TextStyle(
                                      color: Colors.white70, fontSize: 12)),
                              SizedBox(height: 4),
                              Text('Banuna Pizzeria',
                                  style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 17,
                                      fontWeight: FontWeight.w800)),
                              Text('12 slides · swipe to study',
                                  style: TextStyle(
                                      color: Colors.white70, fontSize: 12)),
                            ],
                          ),
                        ),
                        Icon(Icons.play_circle_fill,
                            color: Colors.white, size: 36),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Text(
                'Unit notes · ' + widget.grade + ' · ' + widget.subject,
                style: const TextStyle(
                    fontWeight: FontWeight.w800,
                    fontSize: 15,
                    color: FourTheme.ink),
              ),
              const SizedBox(height: 10),
              FutureBuilder<List<UnitNote>>(
                future: ContentRepository.instance
                    .notesFor(widget.grade, widget.subject),
                builder: (context, snap) {
                  if (snap.connectionState != ConnectionState.done) {
                    return const Padding(
                      padding: EdgeInsets.all(24),
                      child: Center(child: CircularProgressIndicator()),
                    );
                  }
                  final notes = snap.data ?? [];
                  if (notes.isEmpty) {
                    return const Card(
                      child: Padding(
                        padding: EdgeInsets.all(20),
                        child: Text(
                          'No unit notes for this filter yet.\nOpen the illustrated deck or switch grade/subject.',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: FourTheme.muted),
                        ),
                      ),
                    );
                  }
                  return Column(
                    children: notes.map((n) {
                      return Card(
                        margin: const EdgeInsets.only(bottom: 8),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: FourTheme.primarySoft,
                            child: Text('${n.unitNumber}',
                                style: const TextStyle(
                                    fontWeight: FontWeight.w800,
                                    color: FourTheme.primaryDark)),
                          ),
                          title: Text(n.title,
                              style:
                                  const TextStyle(fontWeight: FontWeight.w600)),
                          subtitle: Text(
                            n.summary.isEmpty
                                ? (n.subject + ' · ' + n.grade)
                                : n.summary,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                          trailing: const Icon(Icons.chevron_right),
                          onTap: () => Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => _NoteDetail(note: n),
                            ),
                          ),
                        ),
                      );
                    }).toList(),
                  );
                },
              ),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ],
    );
  }
}

class _NoteDetail extends StatelessWidget {
  const _NoteDetail({required this.note});
  final UnitNote note;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(note.title)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(note.grade + ' · ' + note.subject + ' · Unit ${note.unitNumber}',
              style: const TextStyle(color: FourTheme.muted)),
          const SizedBox(height: 12),
          Text(note.summary.isEmpty ? 'No summary text yet.' : note.summary,
              style: const TextStyle(height: 1.45, fontSize: 15)),
          const SizedBox(height: 20),
          FilledButton.icon(
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => MatricPracticeScreen(
                  subjectFilter: note.subject,
                  grade: note.grade,
                  unitNumber: note.unitNumber,
                  title: 'Matric · ' + note.title,
                ),
              ),
            ),
            icon: const Icon(Icons.assignment),
            label: const Text('Matric questions for this unit'),
          ),
        ],
      ),
    );
  }
}

class IllustratedDeckPage extends StatefulWidget {
  const IllustratedDeckPage({
    super.key,
    required this.deckId,
    required this.title,
    this.subtitle = '',
  });

  final String deckId;
  final String title;
  final String subtitle;

  @override
  State<IllustratedDeckPage> createState() => _IllustratedDeckPageState();
}

class _IllustratedDeckPageState extends State<IllustratedDeckPage> {
  final _page = PageController();
  int index = 0;

  @override
  void dispose() {
    _page.dispose();
    super.dispose();
  }

  String _slideAsset(int i) {
    final n = (i + 1).toString().padLeft(2, '0');
    return 'assets/content/illustrated/g6_math_ch1_webp/slide_$n.webp';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: FourTheme.ink,
      appBar: AppBar(
        backgroundColor: FourTheme.ink,
        foregroundColor: Colors.white,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.title,
                style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    color: Colors.white)),
            if (widget.subtitle.isNotEmpty)
              Text(widget.subtitle,
                  style: const TextStyle(fontSize: 11, color: Colors.white70)),
          ],
        ),
      ),
      body: FutureBuilder<List<IllustratedSlide>>(
        future: ContentRepository.instance.slidesFor(widget.deckId),
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) {
            return const Center(
                child: CircularProgressIndicator(color: FourTheme.accent));
          }
          final slides = snap.data ?? [];
          if (slides.isEmpty) {
            return const Center(
              child: Text('No slides in this deck yet',
                  style: TextStyle(color: Colors.white70)),
            );
          }
          return Column(
            children: [
              Expanded(
                child: PageView.builder(
                  controller: _page,
                  itemCount: slides.length,
                  onPageChanged: (i) => setState(() => index = i),
                  itemBuilder: (context, i) {
                    final s = slides[i];
                    return Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        children: [
                          Expanded(
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(16),
                              child: Image.asset(
                                _slideAsset(i),
                                fit: BoxFit.contain,
                                errorBuilder: (_, __, ___) => Container(
                                  color: Colors.white10,
                                  alignment: Alignment.center,
                                  child: const Icon(Icons.image_outlined,
                                      color: Colors.white54, size: 48),
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(height: 12),
                          Text(s.title,
                              style: const TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w800,
                                  fontSize: 16)),
                          const SizedBox(height: 8),
                          Text(s.body,
                              style: const TextStyle(
                                  color: Colors.white70, height: 1.4)),
                        ],
                      ),
                    );
                  },
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 24),
                child: Row(
                  children: [
                    Text('${index + 1} / ${slides.length}',
                        style: const TextStyle(color: Colors.white70)),
                    const SizedBox(width: 12),
                    Expanded(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(8),
                        child: LinearProgressIndicator(
                          value: (index + 1) / slides.length,
                          minHeight: 6,
                          backgroundColor: Colors.white24,
                          color: FourTheme.accent,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
