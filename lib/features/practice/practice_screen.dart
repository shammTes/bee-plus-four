import 'package:flutter/material.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';
import 'multi_practice_page.dart';
import 'practice_list_session.dart';

/// Pick grade · subject · unit — questions listed; tap opens that question.
class PracticeScreen extends StatefulWidget {
  const PracticeScreen({
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
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  int? unit;
  List<UnitNote> units = [];
  List<PracticeQuestion> pool = [];
  bool loading = false;

  @override
  void initState() {
    super.initState();
    _loadUnits();
  }

  @override
  void didUpdateWidget(covariant PracticeScreen old) {
    super.didUpdateWidget(old);
    if (old.grade != widget.grade || old.subject != widget.subject) {
      unit = null;
      pool = [];
      _loadUnits();
    }
  }

  Future<void> _loadUnits() async {
    final notes =
        await ContentRepository.instance.notesFor(widget.grade, widget.subject);
    if (!mounted) return;
    setState(() {
      units = notes;
      if (units.isNotEmpty && unit == null) unit = units.first.unitNumber;
    });
    if (unit != null) await _loadPool();
  }

  Future<void> _loadPool() async {
    if (unit == null) return;
    setState(() => loading = true);
    final filtered = await ContentRepository.instance.questionsForUnit(
      grade: widget.grade,
      subject: widget.subject,
      unitNumber: unit!,
    );
    if (!mounted) return;
    setState(() {
      pool = filtered;
      loading = false;
    });
  }

  void _openQuestion(int index) {
    if (pool.isEmpty) return;
    final title = units
            .where((u) => u.unitNumber == unit)
            .map((u) => 'U${u.unitNumber} · ${u.title}')
            .firstOrNull ??
        'U$unit Practice';
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => PracticeListSession(
          title: title,
          grade: widget.grade,
          subject: widget.subject,
          unitNumber: unit ?? 1,
          pool: List.of(pool),
          initialIndex: index,
        ),
      ),
    );
  }

  Widget _chip(String label, bool sel, VoidCallback onTap) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Padding(
      padding: const EdgeInsets.only(right: 6),
      child: ChoiceChip(
        label: Text(label),
        selected: sel,
        onSelected: (_) => onTap(),
        selectedColor: const Color(0xFFFBBF24),
        backgroundColor: dark ? const Color(0xFF1E293B) : Colors.white,
        labelStyle: TextStyle(
          color: dark ? Colors.white : const Color(0xFF0F172A),
          fontWeight: FontWeight.w900,
          fontSize: 12,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final dark = Theme.of(context).brightness == Brightness.dark;
    final subjects = CurriculumStreams.subjectsFor(widget.grade,
        stream: CurriculumStreams.science);
    final unitTitle = units
        .where((u) => u.unitNumber == unit)
        .map((u) => 'Unit ${u.unitNumber}: ${u.title}')
        .firstOrNull;

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 14),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF7C3AED), Color(0xFF5B21B6)],
            ),
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Practice',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              const Text('Tap any question to answer now',
                  style: TextStyle(color: Color(0xFFE9D5FF), fontSize: 13)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: ['G9', 'G10', 'G11', 'G12']
                      .map((g) => _chip(g, g == widget.grade, () {
                            widget.onGrade(g);
                          }))
                      .toList(),
                ),
              ),
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
              if (units.isNotEmpty) ...[
                const SizedBox(height: 6),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: units.map((u) {
                      final sel = u.unitNumber == unit;
                      return _chip('U${u.unitNumber}', sel, () async {
                        setState(() => unit = u.unitNumber);
                        await _loadPool();
                      });
                    }).toList(),
                  ),
                ),
              ],
            ],
          ),
        ),
        // Multi-unit practice — high visibility
        Padding(
          padding: const EdgeInsets.fromLTRB(12, 12, 12, 0),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              borderRadius: BorderRadius.circular(18),
              onTap: () => Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => MultiPracticePage(
                    initialGrade: widget.grade,
                  ),
                ),
              ),
              child: Ink(
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFFF59E0B), Color(0xFFEA580C)],
                  ),
                  borderRadius: BorderRadius.circular(18),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFFEA580C).withOpacity(0.35),
                      blurRadius: 12,
                      offset: const Offset(0, 6),
                    ),
                  ],
                ),
                child: const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  child: Row(
                    children: [
                      Icon(Icons.library_add_check_rounded,
                          color: Colors.white, size: 28),
                      SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Multi-unit practice',
                                style: TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.w900,
                                    fontSize: 16)),
                            Text('Mix units · matric or mixed · exam prep',
                                style: TextStyle(
                                    color: Color(0xFFFFEDD5), fontSize: 12)),
                          ],
                        ),
                      ),
                      Icon(Icons.arrow_forward_ios,
                          color: Colors.white, size: 16),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
        Expanded(
          child: loading
              ? const Center(child: CircularProgressIndicator())
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    if (unitTitle != null)
                      Text(unitTitle,
                          style: const TextStyle(
                              fontWeight: FontWeight.w900, fontSize: 16)),
                    const SizedBox(height: 6),
                    Text(
                      pool.isEmpty
                          ? 'No questions for this unit yet'
                          : '${pool.length} questions — tap to open',
                      style: TextStyle(
                          color:
                              dark ? FourTheme.darkMuted : FourTheme.muted,
                          fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 12),
                    if (pool.isNotEmpty)
                      ...List.generate(
                        pool.length,
                        (i) => Card(
                          margin: const EdgeInsets.only(bottom: 8),
                          elevation: 1,
                          child: ListTile(
                            contentPadding: const EdgeInsets.symmetric(
                                horizontal: 14, vertical: 6),
                            leading: CircleAvatar(
                              backgroundColor:
                                  FourTheme.primary.withOpacity(0.15),
                              child: Text('${i + 1}',
                                  style: const TextStyle(
                                      fontSize: 13,
                                      fontWeight: FontWeight.w900,
                                      color: FourTheme.primaryDark)),
                            ),
                            title: Text(
                              pool[i].prompt,
                              maxLines: 3,
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                  fontSize: 14, fontWeight: FontWeight.w700),
                            ),
                            subtitle: Text(
                              '${pool[i].options.length} choices · tap to answer',
                              style: const TextStyle(fontSize: 11),
                            ),
                            trailing: const Icon(Icons.play_circle_fill,
                                color: Color(0xFF7C3AED)),
                            onTap: () => _openQuestion(i),
                          ),
                        ),
                      ),
                  ],
                ),
        ),
      ],
    );
  }
}
