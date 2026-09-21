import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/theme/four_theme.dart';
import '../exams/matric_practice_screen.dart';
import '../practice/unit_practice_page.dart';
import 'illustrated_pdf_page.dart';

class NotesScreen extends StatefulWidget {
  const NotesScreen({
    super.key,
    required this.grade,
    required this.subject,
    required this.onGrade,
    required this.onSubject,
    this.stream = CurriculumStreams.science,
    this.onStream,
  });

  final String grade;
  final String subject;
  final String stream;
  final ValueChanged<String> onGrade;
  final ValueChanged<String> onSubject;
  final ValueChanged<String>? onStream;

  @override
  State<NotesScreen> createState() => _NotesScreenState();
}

class _NotesScreenState extends State<NotesScreen> {
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
        side: const BorderSide(color: Color(0xFFE2E8F0)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final subjects =
        CurriculumStreams.subjectsFor(widget.grade, stream: widget.stream);
    final showStream = widget.grade == 'G11' || widget.grade == 'G12';

    return Column(
      children: [
        Container(
          width: double.infinity,
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
                      fontWeight: FontWeight.w900)),
              const Text('Unit · Illustrated · Practice · Matric',
                  style: TextStyle(color: Color(0xFFCCFBF1), fontSize: 13)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) =>
                          _chip(g, g == widget.grade, () => widget.onGrade(g)))
                      .toList(),
                ),
              ),
              if (showStream) ...[
                const SizedBox(height: 6),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _chip(
                        'Science',
                        widget.stream == CurriculumStreams.science,
                        () => widget.onStream?.call(CurriculumStreams.science),
                      ),
                      _chip(
                        'Arts',
                        widget.stream == CurriculumStreams.arts,
                        () => widget.onStream?.call(CurriculumStreams.arts),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects
                      .map((s) => _chip(
                            CurriculumStreams.label(s),
                            s == widget.subject,
                            () => widget.onSubject(s),
                          ))
                      .toList(),
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: FutureBuilder<List<UnitNote>>(
            future: ContentRepository.instance
                .notesFor(widget.grade, widget.subject),
            builder: (context, snap) {
              if (!snap.hasData) {
                return const Center(child: CircularProgressIndicator());
              }
              final list = snap.data!;
              if (list.isEmpty) {
                return Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(
                      'No unit notes for ${widget.grade} · ${CurriculumStreams.label(widget.subject)} yet.',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: FourTheme.muted),
                    ),
                  ),
                );
              }
              final sorted = [...list]
                ..sort((a, b) => a.unitNumber.compareTo(b.unitNumber));
              return ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: sorted.length + 1,
                itemBuilder: (context, i) {
                  if (i == 0) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: Text(
                        '${widget.grade} · ${CurriculumStreams.label(widget.subject)} · ${sorted.length} units',
                        style: const TextStyle(
                            fontWeight: FontWeight.w800, color: FourTheme.muted),
                      ),
                    );
                  }
                  final n = sorted[i - 1];
                  return _UnitCard(note: n);
                },
              );
            },
          ),
        ),
      ],
    );
  }
}

class _UnitCard extends StatelessWidget {
  const _UnitCard({required this.note});
  final UnitNote note;

  @override
  Widget build(BuildContext context) {
    final level = MasteryStore.instance
        .levelLabel(note.grade, note.subject, note.unitNumber);
    final colors = [
      const Color(0xFF0D9488),
      const Color(0xFF7C3AED),
      const Color(0xFF0284C7),
      const Color(0xFFEA580C),
      const Color(0xFFDB2777),
    ];
    final c = colors[note.unitNumber % colors.length];

    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Material(
        color: Colors.white,
        elevation: 2,
        shadowColor: c.withOpacity(0.25),
        borderRadius: BorderRadius.circular(20),
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute(builder: (_) => UnitHubPage(note: note)),
          ),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: c.withOpacity(0.25)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Container(
                  padding: const EdgeInsets.fromLTRB(16, 14, 16, 12),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: [c, c.withOpacity(0.8)]),
                    borderRadius:
                        const BorderRadius.vertical(top: Radius.circular(20)),
                  ),
                  child: Row(
                    children: [
                      Text('Unit ${note.unitNumber}',
                          style: const TextStyle(
                              color: Colors.white, fontWeight: FontWeight.w900)),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(level,
                            style: TextStyle(
                                color: c,
                                fontWeight: FontWeight.w900,
                                fontSize: 11)),
                      ),
                    ],
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(note.title,
                          style: const TextStyle(
                              fontWeight: FontWeight.w900,
                              fontSize: 16,
                              height: 1.25)),
                      const SizedBox(height: 8),
                      Text(
                        note.summary.isEmpty
                            ? 'Open for notes · illustrated · practice'
                            : note.summary,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                            color: FourTheme.muted, height: 1.35),
                      ),
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          _ActionBtn(
                            icon: Icons.menu_book,
                            label: 'Notes',
                            onTap: () => Navigator.of(context).push(
                              MaterialPageRoute(
                                  builder: (_) => UnitHubPage(note: note)),
                            ),
                          ),
                          const SizedBox(width: 6),
                          _ActionBtn(
                            icon: Icons.slideshow,
                            label: 'Slides',
                            onTap: () => Navigator.of(context).push(
                              MaterialPageRoute(
                                  builder: (_) =>
                                      UnitHubPage(note: note, initialTab: 1)),
                            ),
                          ),
                          const SizedBox(width: 6),
                          _ActionBtn(
                            icon: Icons.quiz,
                            label: 'Practice',
                            onTap: () => Navigator.of(context).push(
                              MaterialPageRoute(
                                builder: (_) => UnitPracticePage(
                                  grade: note.grade,
                                  subject: note.subject,
                                  unitNumber: note.unitNumber,
                                  unitTitle: note.title,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _ActionBtn extends StatelessWidget {
  const _ActionBtn(
      {required this.icon, required this.label, required this.onTap});
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Material(
        color: const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(10),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(10),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Column(
              children: [
                Icon(icon, size: 18, color: FourTheme.ink),
                const SizedBox(height: 2),
                Text(label,
                    style: const TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.w800,
                        color: FourTheme.ink)),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class UnitHubPage extends StatelessWidget {
  const UnitHubPage({super.key, required this.note, this.initialTab = 0});
  final UnitNote note;
  final int initialTab;

  Future<List<Map<String, dynamic>>> _illustrated() async {
    try {
      final raw = await rootBundle.loadString(
          'assets/content/illustrated_catalog_${note.grade.toLowerCase()}.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final all = (map['decks'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map))
          .where((d) => d['subject'] == note.subject)
          .toList();
      // EXACT unit_number match only — no soft title matching
      final exact = all
          .where((d) =>
              (d['unit_number'] as num?)?.toInt() == note.unitNumber)
          .toList();
      return exact;
    } catch (_) {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: FourTheme.surface,
      appBar: AppBar(
        title: Text('Unit ${note.unitNumber}',
            style: const TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(note.title,
              style: const TextStyle(
                  fontSize: 22, fontWeight: FontWeight.w900, height: 1.25)),
          const SizedBox(height: 6),
          Text('${note.grade} · ${note.subject}',
              style: const TextStyle(color: FourTheme.muted)),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: FilledButton.icon(
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => UnitPracticePage(
                        grade: note.grade,
                        subject: note.subject,
                        unitNumber: note.unitNumber,
                        unitTitle: note.title,
                      ),
                    ),
                  ),
                  icon: const Icon(Icons.quiz),
                  label: const Text('Practice'),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => MatricPracticeScreen(
                        subjectFilter: note.subject,
                        grade: note.grade,
                        unitNumber: note.unitNumber,
                        title: '${note.subject} · Unit ${note.unitNumber}',
                      ),
                    ),
                  ),
                  icon: const Icon(Icons.assignment),
                  label: const Text('Matric'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [Color(0xFFECFDF5), Color(0xFFEFF6FF)],
              ),
              borderRadius: BorderRadius.circular(18),
              border: Border.all(color: const Color(0xFF99F6E4)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Row(
                  children: [
                    Icon(Icons.lightbulb, color: Color(0xFF0D9488)),
                    SizedBox(width: 8),
                    Text('Key idea',
                        style: TextStyle(fontWeight: FontWeight.w900)),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  note.summary.isEmpty
                      ? 'Open illustrated packs and practice for this unit.'
                      : note.summary,
                  style: const TextStyle(height: 1.45, fontSize: 15),
                ),
              ],
            ),
          ),
          if (note.keyTerms.isNotEmpty) ...[
            const SizedBox(height: 14),
            const Text('Key terms',
                style: TextStyle(fontWeight: FontWeight.w900)),
            const SizedBox(height: 8),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: note.keyTerms
                  .map((t) => Chip(
                        label: Text(t,
                            style: const TextStyle(
                                color: Color(0xFF0F172A),
                                fontWeight: FontWeight.w700)),
                        backgroundColor: Colors.white,
                      ))
                  .toList(),
            ),
          ],
          const SizedBox(height: 18),
          const Text('Illustrated for this unit',
              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
          const SizedBox(height: 8),
          FutureBuilder<List<Map<String, dynamic>>>(
            future: _illustrated(),
            builder: (context, snap) {
              final decks = snap.data ?? [];
              if (decks.isEmpty) {
                return const Text(
                  'No illustrated deck matched this unit yet (accuracy filter).',
                  style: TextStyle(color: FourTheme.muted),
                );
              }
              return Column(
                children: decks.map((d) {
                  final path = '${d['pdf_asset'] ?? ''}';
                  return Card(
                    child: ListTile(
                      leading: const Icon(Icons.slideshow,
                          color: FourTheme.primaryDark),
                      title: Text('${d['title']}',
                          maxLines: 2,
                          style: const TextStyle(fontWeight: FontWeight.w700)),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: path.isEmpty
                          ? null
                          : () => Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (_) => IllustratedPdfPage(
                                    title: '${d['title']}',
                                    subtitle:
                                        '${note.grade} · ${note.subject}',
                                    assetPath: path,
                                  ),
                                ),
                              ),
                    ),
                  );
                }).toList(),
              );
            },
          ),
        ],
      ),
    );
  }
}
