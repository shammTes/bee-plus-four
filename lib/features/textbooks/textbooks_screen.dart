import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/theme/four_theme.dart';
import '../notes/illustrated_pdf_page.dart';

/// Offline textbook library — grade · subject · open PDF.
class TextbooksScreen extends StatefulWidget {
  const TextbooksScreen({super.key, this.initialGrade});

  final String? initialGrade;

  @override
  State<TextbooksScreen> createState() => _TextbooksScreenState();
}

class _TextbooksScreenState extends State<TextbooksScreen> {
  List<_Book> books = [];
  String? gradeFilter;
  String? subjectFilter;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    gradeFilter = widget.initialGrade;
    _load();
  }

  Future<void> _load() async {
    try {
      final raw = await rootBundle
          .loadString('assets/content/textbooks_catalog.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final list = <_Book>[];
      for (final e in (map['books'] as List? ?? const [])) {
        final m = Map<String, dynamic>.from(e as Map);
        final path = '${m['pdf_asset'] ?? ''}';
        if (path.isEmpty) continue;
        list.add(_Book(
          id: '${m['id']}',
          grade: '${m['grade']}',
          subject: '${m['subject']}',
          title: '${m['title']}',
          pdfAsset: path,
          coverAsset: '${m['cover_asset'] ?? ''}',
        ));
      }
      list.sort((a, b) {
        final g = a.grade.compareTo(b.grade);
        if (g != 0) return g;
        return a.subject.compareTo(b.subject);
      });
      if (!mounted) return;
      setState(() {
        books = list;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        loading = false;
        books = [];
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final grades = books.map((b) => b.grade).toSet().toList()..sort();
    final subjects = books
        .where((b) => gradeFilter == null || b.grade == gradeFilter)
        .map((b) => b.subject)
        .toSet()
        .toList()
      ..sort();
    final filtered = books.where((b) {
      if (gradeFilter != null && b.grade != gradeFilter) return false;
      if (subjectFilter != null && b.subject != subjectFilter) return false;
      return true;
    }).toList();

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF0F766E), Color(0xFF0E7490)],
            ),
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Expanded(
                    child: Text('Textbooks',
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 22,
                            fontWeight: FontWeight.w900)),
                  ),
                  IconButton(
                    onPressed: () => Navigator.of(context).maybePop(),
                    icon: const Icon(Icons.close, color: Colors.white),
                  ),
                ],
              ),
              Text(
                loading
                    ? 'Loading…'
                    : '${filtered.length} of ${books.length} books · offline PDF',
                style: const TextStyle(color: Color(0xFFCCFBF1), fontSize: 13),
              ),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _chip('All grades', gradeFilter == null, () {
                      setState(() {
                        gradeFilter = null;
                        subjectFilter = null;
                      });
                    }),
                    ...grades.map((g) => _chip(g, gradeFilter == g, () {
                          setState(() {
                            gradeFilter = g;
                            subjectFilter = null;
                          });
                        })),
                  ],
                ),
              ),
              if (subjects.isNotEmpty) ...[
                const SizedBox(height: 6),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _chip('All subjects', subjectFilter == null,
                          () => setState(() => subjectFilter = null)),
                      ...subjects.map((s) => _chip(
                            s.replaceAll('_', ' '),
                            subjectFilter == s,
                            () => setState(() => subjectFilter = s),
                          )),
                    ],
                  ),
                ),
              ],
            ],
          ),
        ),
        if (loading)
          const Expanded(child: Center(child: CircularProgressIndicator()))
        else if (filtered.isEmpty)
          const Expanded(
            child: Center(
              child: Text(
                'No textbooks in this filter.\nRebuild APK after CI embeds the pack.',
                textAlign: TextAlign.center,
                style: TextStyle(color: FourTheme.muted),
              ),
            ),
          )
        else
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: filtered.length,
              itemBuilder: (ctx, i) {
                final b = filtered[i];
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: b.coverAsset.isNotEmpty
                        ? ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.asset(
                              b.coverAsset,
                              width: 44,
                              height: 56,
                              fit: BoxFit.cover,
                              errorBuilder: (_, __, ___) => const Icon(
                                  Icons.menu_book,
                                  color: FourTheme.primaryDark),
                            ),
                          )
                        : const Icon(Icons.menu_book,
                            color: FourTheme.primaryDark),
                    title: Text(b.title,
                        style: const TextStyle(fontWeight: FontWeight.w800)),
                    subtitle: Text('${b.grade} · ${b.subject.replaceAll('_', ' ')}'),
                    trailing: const Icon(Icons.picture_as_pdf,
                        color: Color(0xFFEA580C)),
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => IllustratedPdfPage(
                          title: b.title,
                          subtitle: '${b.grade} · textbook',
                          assetPath: b.pdfAsset,
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
      ],
    );
  }

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
      ),
    );
  }
}

class _Book {
  _Book({
    required this.id,
    required this.grade,
    required this.subject,
    required this.title,
    required this.pdfAsset,
    required this.coverAsset,
  });
  final String id;
  final String grade;
  final String subject;
  final String title;
  final String pdfAsset;
  final String coverAsset;
}
