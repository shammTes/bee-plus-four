import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';
import 'html_note_page.dart';

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
  Future<List<UnitNote>> _notes() async {
    final fromRepo = await ContentRepository.instance
        .notesFor(widget.grade, widget.subject);
    if (fromRepo.isNotEmpty &&
        fromRepo.any((n) => n.htmlAsset.isNotEmpty || n.unitNumber > 0)) {
      final hasUnits = fromRepo.any((n) => n.unitNumber > 0);
      if (hasUnits) {
        return fromRepo.where((n) => n.unitNumber > 0).toList();
      }
      return fromRepo;
    }
    try {
      final raw = await rootBundle
          .loadString('assets/content/interactive_notes/index.json');
      final decoded = jsonDecode(raw);
      final list = (decoded is Map ? decoded['notes'] : decoded) as List? ?? [];
      final g = widget.grade.toUpperCase();
      final s = widget.subject.toUpperCase();
      final notes = <UnitNote>[];
      for (final e in list) {
        if (e is! Map) continue;
        final m = Map<String, dynamic>.from(e);
        if ('${m['grade']}'.toUpperCase() != g) continue;
        if ('${m['subject']}'.toUpperCase() != s) continue;
        notes.add(UnitNote.fromJson(m));
      }
      final units = notes.where((n) => n.unitNumber > 0).toList()
        ..sort((a, b) => a.unitNumber.compareTo(b.unitNumber));
      return units.isNotEmpty ? units : notes;
    } catch (_) {
      return fromRepo;
    }
  }

  Widget _chip(String label, bool sel, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          decoration: BoxDecoration(
            color: sel ? FourTheme.coral : FourTheme.surface,
            borderRadius: BorderRadius.circular(999),
            boxShadow: sel ? FourTheme.clay(small: true) : null,
            border: Border.all(color: sel ? FourTheme.coral : FourTheme.line),
          ),
          child: Text(
            label,
            style: TextStyle(
              color: sel ? Colors.white : FourTheme.ink,
              fontWeight: FontWeight.w800,
              fontSize: 13,
            ),
          ),
        ),
      ),
    );
  }

  Future<void> _openNote(BuildContext context, UnitNote n) async {
    final path = n.htmlAsset.isNotEmpty
        ? n.htmlAsset
        : await HtmlNotesIndex.assetFor(n.grade, n.subject, n.unitNumber);
    if (!context.mounted) return;
    if (path == null || path.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Interactive HTML for this subject is not in the APK yet.'),
        ),
      );
      return;
    }
    final anchor = n.anchor.isNotEmpty
        ? n.anchor
        : (n.unitNumber > 0 ? 'u${n.unitNumber}' : '');
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => HtmlNotePage(
          title: n.title,
          assetPath: path,
          subtitle: '${n.grade} · ${n.subject}',
          anchor: anchor,
        ),
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
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 16),
          decoration: BoxDecoration(
            color: FourTheme.surface,
            borderRadius: const BorderRadius.only(
              bottomLeft: Radius.circular(28),
              bottomRight: Radius.circular(28),
            ),
            boxShadow: FourTheme.clay(small: true),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Notes',
                  style: TextStyle(
                      color: FourTheme.ink,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              const SizedBox(height: 4),
              const Text(
                'Tap a unit to open that section',
                style: TextStyle(
                    color: FourTheme.ink2, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) => _chip(g, widget.grade == g, () => widget.onGrade(g)))
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
            future: _notes(),
            builder: (context, snap) {
              if (snap.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              final notes = snap.data ?? [];
              if (notes.isEmpty) {
                final missingEnglish = widget.subject == 'ENGLISH';
                return Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(
                      missingEnglish
                          ? 'Grade ${widget.grade.replaceAll('G', '')} English interactive notes are not in this drop yet.'
                          : widget.grade == 'G9'
                              ? 'No Grade 9 pack for this subject yet.'
                              : 'Interactive notes for ${widget.grade} ${CurriculumStreams.label(widget.subject)} are not listed yet.',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: FourTheme.muted),
                    ),
                  ),
                );
              }
              return ListView.separated(
                padding: const EdgeInsets.all(16),
                itemCount: notes.length,
                separatorBuilder: (_, __) => const SizedBox(height: 10),
                itemBuilder: (context, i) {
                  final n = notes[i];
                  final tone = FourTheme.subjectTile(n.subject);
                  final deep = FourTheme.subjectDeep(n.subject);
                  return Container(
                    decoration: BoxDecoration(
                      color: FourTheme.surface,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: FourTheme.clay(small: true),
                    ),
                    child: ListTile(
                      contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 8),
                      leading: CircleAvatar(
                        backgroundColor: tone,
                        child: Text(
                          n.unitNumber == 0 ? 'All' : '${n.unitNumber}',
                          style: TextStyle(
                              color: deep, fontWeight: FontWeight.w900),
                        ),
                      ),
                      title: Text(n.title,
                          style: const TextStyle(fontWeight: FontWeight.w800)),
                      subtitle: const Text('Opens at this unit'),
                      trailing: Icon(Icons.chevron_right, color: deep),
                      onTap: () => _openNote(context, n),
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
