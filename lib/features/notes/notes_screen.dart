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
import 'illustrated_cards_page.dart';

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
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) => _chip(
                            g,
                            widget.grade == g,
                            () => widget.onGrade(g),
                          ))
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
                            s,
                            widget.subject == s,
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
              if (snap.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              final notes = snap.data ?? [];
              if (notes.isEmpty) {
                return const Center(
                  child: Text('No notes for this grade/subject yet.',
                      style: TextStyle(color: FourTheme.muted)),
                );
              }
              return ListView.separated(
                padding: const EdgeInsets.all(16),
                itemCount: notes.length,
                separatorBuilder: (_, __) => const SizedBox(height: 8),
                itemBuilder: (context, i) {
                  final n = notes[i];
                  return Card(
                    child: ListTile(
                      leading: CircleAvatar(
                        backgroundColor: FourTheme.primarySoft,
                        child: Text('U${n.unitNumber}',
                            style: const TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w900,
                                color: FourTheme.primaryDark)),
                      ),
                      title: Text(n.title,
                          style: const TextStyle(fontWeight: FontWeight.w800)),
                      subtitle: Text(
                        (n.summary.isEmpty
                                ? 'Open unit notes, illustrated, practice'
                                : n.summary)
                            .length >
                            100
                            ? '${n.summary.substring(0, 100)}…'
                            : (n.summary.isEmpty
                                ? 'Open unit notes, illustrated, practice'
                                : n.summary),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => _UnitHub(note: n),
                        ),
                      ),
                    ),
                  );
                },
              );
            },
          ),
        ),
      ],
    );
  }
}

class _UnitHub extends StatelessWidget {
  const _UnitHub({required this.note});
  final UnitNote note;

  Future<List<Map<String, dynamic>>> _illustrated() async {
    final out = <Map<String, dynamic>>[];
    try {
      final raw = await rootBundle.loadString(
          'assets/content/illustrated_catalog_${note.grade.toLowerCase()}.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final all = (map['decks'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map))
          .where((d) => d['subject'] == note.subject)
          .toList();
      out.addAll(all.where((d) =>
          (d['unit_number'] as num?)?.toInt() == note.unitNumber));
    } catch (_) {}
    try {
      final raw = await rootBundle.loadString(
          'assets/content/illustrated_cards_${note.grade.toLowerCase()}.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final all = (map['decks'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map))
          .where((d) => d['subject'] == note.subject)
          .toList();
      out.addAll(all.where((d) =>
          (d['unit_number'] as num?)?.toInt() == note.unitNumber));
    } catch (_) {}
    return out;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Unit ${note.unitNumber} · ${note.title}',
            maxLines: 1, overflow: TextOverflow.ellipsis),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (note.summary.isNotEmpty) ...[
            Text(note.summary,
                style: const TextStyle(fontSize: 15, height: 1.4)),
            const SizedBox(height: 12),
          ],
          if (note.keyTerms.isNotEmpty) ...[
            const Text('Key terms',
                style: TextStyle(fontWeight: FontWeight.w900)),
            const SizedBox(height: 6),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: note.keyTerms
                  .map((t) => Chip(label: Text(t)))
                  .toList(),
            ),
            const SizedBox(height: 12),
          ],
          FilledButton.icon(
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => UnitPracticePage(
                  grade: note.grade,
                  subject: note.subject,
                  unitNumber: note.unitNumber,
                  title: note.title,
                ),
              ),
            ),
            icon: const Icon(Icons.quiz),
            label: const Text('Practice this unit'),
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
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
            icon: const Icon(Icons.school),
            label: const Text('Related matric questions'),
          ),
          const SizedBox(height: 16),
          const Text('Illustrated for this unit',
              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
          FutureBuilder<List<Map<String, dynamic>>>(
            future: _illustrated(),
            builder: (context, snap) {
              final decks = snap.data ?? [];
              if (decks.isEmpty) {
                return const Padding(
                  padding: EdgeInsets.only(top: 8),
                  child: Text('No illustrated deck for this unit yet.',
                      style: TextStyle(color: FourTheme.muted)),
                );
              }
              return Column(
                children: decks.map((d) {
                  final path = '${d['pdf_asset'] ?? ''}';
                  return Card(
                    child: ListTile(
                      leading: const Icon(Icons.slideshow, color: Color(0xFF7C3AED)),
                      title: Text('${d['title']}',
                          style: const TextStyle(fontWeight: FontWeight.w800)),
                      subtitle: Text(
                        d['type'] == 'illustrated_cards'
                            ? 'Colorful cards · tap to open'
                            : 'Illustrated pack',
                      ),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () {
                        final isCards = d['type'] == 'illustrated_cards' ||
                            (d['slides'] is List &&
                                (d['slides'] as List).isNotEmpty);
                        if (isCards) {
                          final slides = ((d['slides'] as List?) ?? const [])
                              .map((e) =>
                                  Map<String, dynamic>.from(e as Map))
                              .toList();
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => IllustratedCardsPage(
                                title: '${d['title']}',
                                subtitle:
                                    '${note.grade} · ${note.subject}',
                                slides: slides,
                              ),
                            ),
                          );
                          return;
                        }
                        if (path.isEmpty) return;
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => IllustratedPdfPage(
                              title: '${d['title']}',
                              subtitle:
                                  '${note.grade} · ${note.subject}',
                              assetPath: path,
                            ),
                          ),
                        );
                      },
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
