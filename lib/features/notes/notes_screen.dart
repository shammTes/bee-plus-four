import 'package:flutter/material.dart';
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
  Widget _chip(String label, bool sel, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ChoiceChip(
        label: Text(label),
        selected: sel,
        onSelected: (_) => onTap(),
        selectedColor: FourTheme.butterMid,
        backgroundColor: FourTheme.surface,
        labelStyle: TextStyle(
          color: FourTheme.ink,
          fontWeight: FontWeight.w800,
          fontSize: 13,
        ),
        side: BorderSide(color: sel ? FourTheme.butterDeep : FourTheme.line),
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
              Text(
                widget.grade == 'G9'
                    ? 'Grade 9 units — tap a unit to open that section'
                    : 'Tap a unit to open that section',
                style: const TextStyle(
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
            future: ContentRepository.instance
                .notesFor(widget.grade, widget.subject),
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
                          ? 'Grade ${widget.grade.replaceAll('G', '')} English interactive notes are not in this drop yet. Grammar pack comes next.'
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
