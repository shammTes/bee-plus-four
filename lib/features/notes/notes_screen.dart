import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';
import 'illustrated_pdf_page.dart';
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
              const Text('Unit notes · illustrated PDFs · matric links',
                  style: TextStyle(color: Color(0xFFCCFBF1), fontSize: 13)),
              const SizedBox(height: 12),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12'].map((g) {
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
              const Text('Highschool illustrated packs',
                  style: TextStyle(
                      fontWeight: FontWeight.w800,
                      fontSize: 15,
                      color: FourTheme.ink)),
              const SizedBox(height: 8),
              FutureBuilder<String>(
                future: rootBundle.loadString(
                    'assets/content/illustrated_catalog_' +
                        widget.grade.toLowerCase() +
                        '.json'),
                builder: (context, snap) {
                  if (!snap.hasData) {
                    return const Text('Loading illustrated catalogue…',
                        style: TextStyle(color: FourTheme.muted));
                  }
                  try {
                    final map = jsonDecode(snap.data!) as Map<String, dynamic>;
                    final decks = (map['decks'] as List?) ?? [];
                    final filtered = decks.where((d) {
                      final m = d as Map<String, dynamic>;
                      return m['subject'] == widget.subject;
                    }).toList();
                    final list =
                        filtered.isNotEmpty ? filtered : decks.take(12).toList();
                    if (list.isEmpty) {
                      return const Text('No packs for this filter yet.',
                          style: TextStyle(color: FourTheme.muted));
                    }
                    return Column(
                      children: list.map((raw) {
                        final d = raw as Map<String, dynamic>;
                        final hasPdf = d['pdf_asset'] != null &&
                            '${d['pdf_asset']}'.isNotEmpty;
                        return Card(
                          margin: const EdgeInsets.only(bottom: 8),
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundColor: FourTheme.primarySoft,
                              child: Text('${d['unit_number'] ?? '•'}',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color: FourTheme.primaryDark,
                                      fontSize: 11)),
                            ),
                            title: Text('${d['title']}',
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(
                                    fontWeight: FontWeight.w600, fontSize: 13)),
                            subtitle: Text(hasPdf
                                ? '${d['grade']} · ${d['subject']} · Offline PDF'
                                : '${d['grade']} · ${d['subject']} · Export PDF to embed'),
                            trailing: Icon(
                              hasPdf
                                  ? Icons.picture_as_pdf
                                  : Icons.cloud_download_outlined,
                              color: FourTheme.primaryDark,
                            ),
                            onTap: () {
                              final path = d['pdf_asset']?.toString() ?? '';
                              if (path.isEmpty) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text(
                                      'PDF not embedded yet. Export PPT → compressed PDF, put under assets/content/illustrated_pdf/, set pdf_asset in catalog.',
                                    ),
                                  ),
                                );
                                return;
                              }
                              Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (_) => IllustratedPdfPage(
                                    title: '${d['title']}',
                                    subtitle:
                                        '${d['grade']} · ${d['subject']}',
                                    assetPath: path,
                                  ),
                                ),
                              );
                            },
                          ),
                        );
                      }).toList(),
                    );
                  } catch (_) {
                    return const Text(
                      'Catalogue file missing for this grade. Push illustrated_catalog_g9..g12.json',
                      style: TextStyle(color: FourTheme.muted),
                    );
                  }
                },
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
                          'No unit notes for this filter yet.\nOpen an illustrated PDF when embedded, or switch grade/subject.',
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
