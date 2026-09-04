import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';
import '../exams/matric_practice_screen.dart';
import 'illustrated_pdf_page.dart';

/// High-contrast chip used on gradient headers.
Widget _hcChip({
  required String label,
  required bool selected,
  required VoidCallback onTap,
}) {
  return Padding(
    padding: const EdgeInsets.only(right: 6),
    child: ChoiceChip(
      label: Text(label),
      selected: selected,
      onSelected: (_) => onTap(),
      selectedColor: const Color(0xFFFBBF24),
      backgroundColor: Colors.white,
      labelStyle: const TextStyle(
        color: Color(0xFF0F172A),
        fontWeight: FontWeight.w900,
        fontSize: 12,
      ),
      side: const BorderSide(color: Color(0xFFE2E8F0)),
      visualDensity: VisualDensity.compact,
    ),
  );
}

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

class _NotesScreenState extends State<NotesScreen>
    with SingleTickerProviderStateMixin {
  static const subjects = [
    'MATH',
    'PHYSICS',
    'CHEMISTRY',
    'BIOLOGY',
    'ENGLISH',
    'GEOGRAPHY',
    'HISTORY',
    'AGRICULTURE',
    'BUSINESS_ECONOMICS',
  ];

  late TabController _tabs;

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabs.dispose();
    super.dispose();
  }

  String _subjLabel(String s) => s == 'BUSINESS_ECONOMICS'
      ? 'Business'
      : s[0] + s.substring(1).toLowerCase();

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 8),
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
              const SizedBox(height: 2),
              const Text('Unit notes · illustrated · textbooks',
                  style: TextStyle(color: Color(0xFFCCFBF1), fontSize: 13)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) => _hcChip(
                            label: g,
                            selected: g == widget.grade,
                            onTap: () => widget.onGrade(g),
                          ))
                      .toList(),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects
                      .map((s) => _hcChip(
                            label: _subjLabel(s),
                            selected: s == widget.subject,
                            onTap: () => widget.onSubject(s),
                          ))
                      .toList(),
                ),
              ),
              const SizedBox(height: 8),
              TabBar(
                controller: _tabs,
                labelColor: Colors.white,
                unselectedLabelColor: Colors.white70,
                indicatorColor: const Color(0xFFFBBF24),
                labelStyle: const TextStyle(fontWeight: FontWeight.w800),
                tabs: const [
                  Tab(text: 'Unit notes'),
                  Tab(text: 'Illustrated'),
                  Tab(text: 'Textbooks'),
                ],
              ),
            ],
          ),
        ),
        Expanded(
          child: TabBarView(
            controller: _tabs,
            children: [
              _UnitNotesTab(grade: widget.grade, subject: widget.subject),
              _IllustratedTab(grade: widget.grade, subject: widget.subject),
              _TextbooksTab(grade: widget.grade, subject: widget.subject),
            ],
          ),
        ),
      ],
    );
  }
}

class _UnitNotesTab extends StatelessWidget {
  const _UnitNotesTab({required this.grade, required this.subject});
  final String grade;
  final String subject;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<UnitNote>>(
      future: ContentRepository.instance.notesFor(grade, subject),
      builder: (context, snap) {
        if (!snap.hasData) {
          return const Center(child: CircularProgressIndicator());
        }
        var list = snap.data!;
        if (list.isEmpty) {
          // fall back to all subjects for this grade
          return FutureBuilder<List<UnitNote>>(
            future: ContentRepository.instance.notes().then(
                  (all) => all.where((n) => n.grade == grade).toList(),
                ),
            builder: (context, s2) {
              final all = s2.data ?? [];
              if (all.isEmpty) {
                return const Center(
                    child: Text('No unit notes for this grade yet.',
                        style: TextStyle(color: FourTheme.muted)));
              }
              return _noteList(context, all);
            },
          );
        }
        return _noteList(context, list);
      },
    );
  }

  Widget _noteList(BuildContext context, List<UnitNote> list) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: list.length,
      itemBuilder: (context, i) {
        final n = list[i];
        return Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: FourTheme.primarySoft,
              child: Text('${n.unitNumber}',
                  style: const TextStyle(
                      fontWeight: FontWeight.w900,
                      color: FourTheme.primaryDark)),
            ),
            title: Text(n.title,
                style: const TextStyle(fontWeight: FontWeight.w700)),
            subtitle: Text(
              n.summary.isEmpty
                  ? '${n.subject} · ${n.grade}'
                  : n.summary,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => _NoteDetail(note: n)),
            ),
          ),
        );
      },
    );
  }
}

class _IllustratedTab extends StatelessWidget {
  const _IllustratedTab({required this.grade, required this.subject});
  final String grade;
  final String subject;

  Future<List<Map<String, dynamic>>> _load() async {
    // Prefer grade catalog, then HS master catalog
    final paths = [
      'assets/content/illustrated_catalog_${grade.toLowerCase()}.json',
      'assets/content/illustrated_catalog_hs.json',
    ];
    final all = <Map<String, dynamic>>[];
    for (final path in paths) {
      try {
        final raw = await rootBundle.loadString(path);
        final map = jsonDecode(raw) as Map<String, dynamic>;
        for (final d in (map['decks'] as List? ?? [])) {
          all.add(Map<String, dynamic>.from(d as Map));
        }
      } catch (_) {}
    }
    // de-dupe by title
    final seen = <String>{};
    final unique = <Map<String, dynamic>>[];
    for (final d in all) {
      final k = '${d['title']}|${d['pdf_asset']}';
      if (seen.add(k)) unique.add(d);
    }
    var filtered = unique
        .where((d) =>
            d['grade'] == grade &&
            (d['subject'] == subject || subject.isEmpty))
        .toList();
    if (filtered.isEmpty) {
      filtered = unique.where((d) => d['grade'] == grade).toList();
    }
    if (filtered.isEmpty) filtered = unique;
    return filtered;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: _load(),
      builder: (context, snap) {
        if (!snap.hasData) {
          return const Center(child: CircularProgressIndicator());
        }
        final list = snap.data!;
        if (list.isEmpty) {
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(24),
              child: Text(
                'No illustrated PDFs for this filter yet.\nTry another grade/subject or open Textbooks.',
                textAlign: TextAlign.center,
                style: TextStyle(color: FourTheme.muted),
              ),
            ),
          );
        }
        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: list.length,
          itemBuilder: (context, i) {
            final d = list[i];
            final path = '${d['pdf_asset'] ?? ''}';
            final hasPdf = path.isNotEmpty;
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: FourTheme.primarySoft,
                  child: Icon(
                    hasPdf ? Icons.slideshow : Icons.cloud_off,
                    color: FourTheme.primaryDark,
                  ),
                ),
                title: Text('${d['title']}',
                    maxLines: 2,
                    style: const TextStyle(fontWeight: FontWeight.w700)),
                subtitle: Text(
                    '${d['grade']} · ${d['subject']}${hasPdf ? ' · Offline PDF' : ''}'),
                trailing: const Icon(Icons.chevron_right),
                onTap: hasPdf
                    ? () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => IllustratedPdfPage(
                              title: '${d['title']}',
                              subtitle: '${d['grade']} · ${d['subject']}',
                              assetPath: path,
                            ),
                          ),
                        )
                    : null,
              ),
            );
          },
        );
      },
    );
  }
}

class _TextbooksTab extends StatelessWidget {
  const _TextbooksTab({required this.grade, required this.subject});
  final String grade;
  final String subject;

  Future<List<Map<String, dynamic>>> _load() async {
    try {
      final raw =
          await rootBundle.loadString('assets/content/textbooks_catalog.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final books = (map['books'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map))
          .toList();
      var filtered = books
          .where((b) => b['grade'] == grade && b['subject'] == subject)
          .toList();
      if (filtered.isEmpty) {
        filtered = books.where((b) => b['grade'] == grade).toList();
      }
      if (filtered.isEmpty) filtered = books;
      return filtered;
    } catch (_) {
      return [];
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: _load(),
      builder: (context, snap) {
        if (!snap.hasData) {
          return const Center(child: CircularProgressIndicator());
        }
        final list = snap.data!;
        if (list.isEmpty) {
          return const Center(
              child: Text('No textbooks embedded for this filter.',
                  style: TextStyle(color: FourTheme.muted)));
        }
        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: list.length,
          itemBuilder: (context, i) {
            final b = list[i];
            final path = '${b['pdf_asset'] ?? ''}';
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                leading: const CircleAvatar(
                  backgroundColor: Color(0xFFFFEDD5),
                  child: Icon(Icons.menu_book, color: Color(0xFFC2410C)),
                ),
                title: Text('${b['title']}',
                    style: const TextStyle(fontWeight: FontWeight.w700)),
                subtitle: Text('${b['grade']} · ${b['subject']} · Textbook PDF'),
                trailing: const Icon(Icons.picture_as_pdf),
                onTap: path.isEmpty
                    ? null
                    : () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => IllustratedPdfPage(
                              title: '${b['title']}',
                              subtitle: 'Textbook · ${b['grade']}',
                              assetPath: path,
                            ),
                          ),
                        ),
              ),
            );
          },
        );
      },
    );
  }
}

class _NoteDetail extends StatelessWidget {
  const _NoteDetail({required this.note});
  final UnitNote note;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(note.title, maxLines: 1)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('${note.grade} · ${note.subject} · Unit ${note.unitNumber}',
              style: const TextStyle(color: FourTheme.muted)),
          const SizedBox(height: 12),
          Text(
            note.summary.isEmpty ? 'No summary text yet.' : note.summary,
            style: const TextStyle(height: 1.45, fontSize: 15),
          ),
          if (note.keyTerms.isNotEmpty) ...[
            const SizedBox(height: 16),
            const Text('Key terms',
                style: TextStyle(fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: note.keyTerms
                  .map((t) => Chip(
                        label: Text(t,
                            style: const TextStyle(
                                color: Color(0xFF0F172A),
                                fontWeight: FontWeight.w600)),
                        backgroundColor: Colors.white,
                      ))
                  .toList(),
            ),
          ],
          const SizedBox(height: 20),
          FilledButton.icon(
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => MatricPracticeScreen(
                  subjectFilter: note.subject,
                  grade: note.grade,
                  unitNumber: note.unitNumber,
                  title: 'Matric · ${note.title}',
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
