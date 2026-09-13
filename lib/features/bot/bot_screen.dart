import 'package:flutter/material.dart';

import '../../core/bot/offline_bot.dart';
import '../../core/content/content_repository.dart';
import '../../core/models/content_models.dart';
import '../../core/theme/four_theme.dart';

class BotScreen extends StatefulWidget {
  const BotScreen({super.key, this.initialGrade = 'G10'});
  final String initialGrade;

  @override
  State<BotScreen> createState() => _BotScreenState();
}

class _BotScreenState extends State<BotScreen> {
  final _bot = OfflineBot();
  final _ctrl = TextEditingController();
  final _scroll = ScrollController();
  final _messages = <_Msg>[];
  bool busy = false;

  String grade = 'G10';
  String subject = 'MATH';
  int? unit;
  /// quiz | notes | matric
  String mode = 'quiz';
  List<UnitNote> units = [];

  static const grades = ['G9', 'G10', 'G11', 'G12'];
  static const subjects = [
    'MATH', 'PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'ENGLISH',
    'GEOGRAPHY', 'HISTORY', 'AGRICULTURE', 'BUSINESS_ECONOMICS',
  ];

  @override
  void initState() {
    super.initState();
    grade = widget.initialGrade;
    _bot.grade = grade;
    _bot.subject = subject;
    _loadUnits();
    _messages.add(_Msg(
      false,
      'Coach offline.\n\n'
      '• Pick grade · subject · unit\n'
      '• Modes: Quiz · Notes · Matric\n'
      '• Start when ready',
    ));
  }

  Future<void> _loadUnits() async {
    final list =
        await ContentRepository.instance.notesFor(grade, subject);
    if (!mounted) return;
    setState(() {
      units = list;
      unit = list.isEmpty ? null : list.first.unitNumber;
    });
  }

  Future<void> _send(String text) async {
    final t = text.trim();
    if (t.isEmpty || busy) return;
    setState(() {
      busy = true;
      _messages.add(_Msg(true, t));
      _ctrl.clear();
    });
    _bot.grade = grade;
    _bot.subject = subject;
    try {
      BotReply reply;
      final low = t.toLowerCase();
      if (mode == 'matric' || low.contains('matric')) {
        reply = await _bot.handle('start quiz');
        // Prefer matric pool via repo if available — fall back to quiz
        final matric = await ContentRepository.instance.matricForSubject(subject);
        if (matric.isNotEmpty) {
          final q = matric.first;
          reply = BotReply(
            'Matric mode · $subject\n\n${q.prompt}\n\nReply A/B/C/D',
            // reuse practice-shaped flow via handle letters
          );
        }
      } else if (mode == 'notes' || low == 'notes' || low.contains('show notes')) {
        reply = await _bot.notesBrief();
      } else {
        reply = await _bot.handle(t);
      }
      if (!mounted) return;
      setState(() {
        _messages.add(_Msg(false, reply.text,
            question: reply.question, quick: reply.quick));
        busy = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _messages.add(_Msg(false, 'Coach error: $e'));
        busy = false;
      });
    }
    await Future<void>.delayed(const Duration(milliseconds: 40));
    if (_scroll.hasClients) {
      _scroll.animateTo(_scroll.position.maxScrollExtent,
          duration: const Duration(milliseconds: 250), curve: Curves.easeOut);
    }
  }

  Widget _chip(String label, bool selected, VoidCallback onTap) {
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
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 12),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF7C3AED), Color(0xFF6D28D9)],
            ),
            borderRadius: BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Coach',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              Text(
                unit == null
                    ? '$grade · $subject'
                    : '$grade · $subject · Unit $unit',
                style: const TextStyle(color: Color(0xFFE9D5FF), fontSize: 13),
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: grades
                      .map((g) => _chip(g, g == grade, () async {
                            setState(() => grade = g);
                            _bot.grade = g;
                            await _loadUnits();
                          }))
                      .toList(),
                ),
              ),
              const SizedBox(height: 6),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: subjects.map((s) {
                    final label = s == 'BUSINESS_ECONOMICS'
                        ? 'Business'
                        : s[0] + s.substring(1).toLowerCase();
                    return _chip(label, s == subject, () async {
                      setState(() => subject = s);
                      _bot.subject = s;
                      await _loadUnits();
                    });
                  }).toList(),
                ),
              ),
              if (units.isNotEmpty) ...[
                const SizedBox(height: 6),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: units
                        .map((u) => _chip(
                              'U${u.unitNumber}',
                              unit == u.unitNumber,
                              () => setState(() => unit = u.unitNumber),
                            ))
                        .toList(),
                  ),
                ),
              ],
              const SizedBox(height: 8),
              Row(
                children: [
                  _chip('Quiz', mode == 'quiz', () => setState(() => mode = 'quiz')),
                  _chip('Notes', mode == 'notes', () => setState(() => mode = 'notes')),
                  _chip('Matric', mode == 'matric',
                      () => setState(() => mode = 'matric')),
                  const Spacer(),
                  FilledButton(
                    style: FilledButton.styleFrom(
                      backgroundColor: const Color(0xFFFBBF24),
                      foregroundColor: const Color(0xFF0F172A),
                    ),
                    onPressed: busy
                        ? null
                        : () => _send(mode == 'notes'
                            ? 'notes'
                            : mode == 'matric'
                                ? 'matric'
                                : 'start quiz'),
                    child: Text(
                      mode == 'notes'
                          ? 'Show notes'
                          : mode == 'matric'
                              ? 'Matric Q'
                              : 'Start',
                      style: const TextStyle(fontWeight: FontWeight.w900),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        Expanded(
          child: ListView.builder(
            controller: _scroll,
            padding: const EdgeInsets.all(12),
            itemCount: _messages.length,
            itemBuilder: (context, i) {
              final m = _messages[i];
              return Align(
                alignment:
                    m.mine ? Alignment.centerRight : Alignment.centerLeft,
                child: Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.all(12),
                  constraints: BoxConstraints(
                      maxWidth: MediaQuery.sizeOf(context).width * 0.88),
                  decoration: BoxDecoration(
                    color: m.mine ? const Color(0xFFDDD6FE) : Colors.white,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: const Color(0xFFE2E8F0)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(m.text,
                          style: const TextStyle(
                              color: Color(0xFF0F172A), height: 1.35)),
                      if (m.question != null) ...[
                        const SizedBox(height: 10),
                        ...List.generate(m.question!.options.length, (oi) {
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 6),
                            child: OutlinedButton(
                              onPressed: busy
                                  ? null
                                  : () => _send(
                                      String.fromCharCode(65 + oi)),
                              child: Align(
                                alignment: Alignment.centerLeft,
                                child: Text(
                                  '${String.fromCharCode(65 + oi)}. ${m.question!.options[oi]}',
                                  style: const TextStyle(
                                      color: Color(0xFF0F172A),
                                      fontWeight: FontWeight.w600),
                                ),
                              ),
                            ),
                          );
                        }),
                      ],
                      if (m.quick != null && m.quick!.isNotEmpty) ...[
                        const SizedBox(height: 8),
                        Wrap(
                          spacing: 6,
                          children: m.quick!
                              .map((q) => ActionChip(
                                    label: Text(q.label,
                                        style: const TextStyle(
                                            color: Color(0xFF0F172A),
                                            fontWeight: FontWeight.w800,
                                            fontSize: 12)),
                                    backgroundColor: Colors.white,
                                    onPressed: busy
                                        ? null
                                        : () => _send(q.label),
                                  ))
                              .toList(),
                        ),
                      ],
                    ],
                  ),
                ),
              );
            },
          ),
        ),
        SafeArea(
          top: false,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(12, 0, 12, 10),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _ctrl,
                    decoration: const InputDecoration(
                      hintText: 'start quiz · notes · matric · A/B/C/D',
                      border: OutlineInputBorder(),
                      isDense: true,
                    ),
                    onSubmitted: _send,
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  onPressed: busy ? null : () => _send(_ctrl.text),
                  icon: const Icon(Icons.send),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}

class _Msg {
  _Msg(this.mine, this.text, {this.question, this.quick});
  final bool mine;
  final String text;
  final PracticeQuestion? question;
  final List<QuickAction>? quick;
}
