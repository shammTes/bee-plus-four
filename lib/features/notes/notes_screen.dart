import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/progress/mastery_store.dart';
import '../../core/theme/four_theme.dart';
import '../exams/matric_practice_screen.dart';
import 'illustrated_pdf_page.dart';

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

  String _subjLabel(String s) => s == 'BUSINESS_ECONOMICS'
      ? 'Business'
      : s[0] + s.substring(1).toLowerCase();

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
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
              const Text('Textbook units · cards · practice links',
                  style:
                      TextStyle(color: Color(0xFFCCFBF1), fontSize: 13)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) => _chip(g, g == widget.grade, () => widget.onGrade(g)))
                      .toList(),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects
                      .map((s) => _chip(
                            _subjLabel(s),
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
              var list = snap.data!;
              if (list.isEmpty) {
                return FutureBuilder<List<UnitNote>>(
                  future: ContentRepository.instance.notes().then(
                        (all) => all
                            .where((n) => n.grade == widget.grade)
                            .toList(),
                      ),
                  builder: (context, s2) {
                    final all = s2.data ?? [];
                    if (all.isEmpty) {
                      return const Center(
                          child: Text('No unit notes for this filter.',
                              style: TextStyle(color: FourTheme.muted)));
                    }
                    return _unitGrid(all);
                  },
                );
              }
              return _unitGrid(list);
            },
          ),
        ),
      ],
    );
  }

  Widget _unitGrid(List<UnitNote> list) {
    list = [...list]..sort((a, b) => a.unitNumber.compareTo(b.unitNumber));
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: list.length + 1,
      itemBuilder: (context, i) {
        if (i == 0) {
          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Text(
              '${widget.grade} · ${_subjLabel(widget.subject)} · ${list.length} units',
              style: const TextStyle(
                  fontWeight: FontWeight.w800, color: FourTheme.muted),
            ),
          );
        }
        final n = list[i - 1];
        final level = MasteryStore.instance
            .levelLabel(n.grade, n.subject, n.unitNumber);
        final colors = [
          const Color(0xFF0D9488),
          const Color(0xFF7C3AED),
          const Color(0xFF0284C7),
          const Color(0xFFEA580C),
          const Color(0xFFDB2777),
        ];
        final c = colors[n.unitNumber % colors.length];
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
                MaterialPageRoute(builder: (_) => _UnitHub(note: n)),
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
                        gradient: LinearGradient(
                          colors: [c, c.withOpacity(0.8)],
                        ),
                        borderRadius: const BorderRadius.vertical(
                            top: Radius.circular(20)),
                      ),
                      child: Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 10, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            child: Text('Unit ${n.unitNumber}',
                                style: const TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.w900)),
                          ),
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
                          Text(n.title,
                              style: const TextStyle(
                                  fontWeight: FontWeight.w900,
                                  fontSize: 16,
                                  height: 1.25)),
                          const SizedBox(height: 8),
                          Text(
                            n.summary.isEmpty
                                ? 'Open for notes · illustrated · practice'
                                : n.summary,
                            maxLines: 3,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(
                                color: FourTheme.muted, height: 1.35),
                          ),
                          const SizedBox(height: 12),
                          Row(
                            children: const [
                              _MiniTag(Icons.menu_book, 'Notes'),
                              SizedBox(width: 6),
                              _MiniTag(Icons.slideshow, 'Illustrated'),
                              SizedBox(width: 6),
                              _MiniTag(Icons.quiz, 'Practice'),
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
      },
    );
  }
}

class _MiniTag extends StatelessWidget {
  const _MiniTag(this.icon, this.label);
  final IconData icon;
  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: const Color(0xFFF1F5F9),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 12, color: FourTheme.ink),
          const SizedBox(width: 4),
          Text(label,
              style: const TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.w800,
                  color: FourTheme.ink)),
        ],
      ),
    );
  }
}

/// Hub for one textbook unit: Notes · Illustrated · Practice · Matric.
class _UnitHub extends StatelessWidget {
  const _UnitHub({required this.note});
  final UnitNote note;

  Future<List<Map<String, dynamic>>> _illustrated() async {
    try {
      final raw = await rootBundle.loadString(
          'assets/content/illustrated_catalog_${note.grade.toLowerCase()}.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final decks = (map['decks'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map))
          .where((d) =>
              d['subject'] == note.subject &&
              ((d['unit_number'] as num?)?.toInt() == note.unitNumber ||
                  '${d['title']}'.toLowerCase().contains(note.title
                      .toLowerCase()
                      .split(' ')
                      .take(2)
                      .join(' '))))
          .toList();
      if (decks.isEmpty) {
        return (map['decks'] as List? ?? [])
            .map((e) => Map<String, dynamic>.from(e as Map))
            .where((d) => d['subject'] == note.subject)
            .take(5)
            .toList();
      }
      return decks;
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
          const SizedBox(height: 16),
          // Engaging summary card
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
          const Text('Study this unit',
              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
          const SizedBox(height: 10),
          FutureBuilder<List<Map<String, dynamic>>>(
            future: _illustrated(),
            builder: (context, snap) {
              final decks = snap.data ?? [];
              return Column(
                children: [
                  if (decks.isNotEmpty)
                    ...decks.map((d) {
                      final path = '${d['pdf_asset'] ?? ''}';
                      return Card(
                        child: ListTile(
                          leading: const Icon(Icons.slideshow,
                              color: FourTheme.primaryDark),
                          title: Text('${d['title']}',
                              maxLines: 2,
                              style: const TextStyle(
                                  fontWeight: FontWeight.w700)),
                          subtitle: const Text('Illustrated PDF'),
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
                    }),
                  Card(
                    child: ListTile(
                      leading: const Icon(Icons.quiz,
                          color: FourTheme.violet),
                      title: const Text('Practice this unit',
                          style: TextStyle(fontWeight: FontWeight.w800)),
                      subtitle:
                          const Text('Adaptive questions · mastery tracking'),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text(
                                'Open Practice tab and select this unit (U#).'),
                          ),
                        );
                      },
                    ),
                  ),
                  Card(
                    child: ListTile(
                      leading: const Icon(Icons.assignment,
                          color: Color(0xFFEA580C)),
                      title: const Text('Matric for this unit',
                          style: TextStyle(fontWeight: FontWeight.w800)),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () => Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => MatricPracticeScreen(
                            subjectFilter: note.subject,
                            grade: note.grade,
                            unitNumber: note.unitNumber,
                            title: 'Matric · ${note.title}',
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              );
            },
          ),
        ],
      ),
    );
  }
}
