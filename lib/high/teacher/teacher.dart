// Teacher tools: pick questions (Matric + Exercise bank) -> show codes on the board. Student side: enter a class code
// -> homework sheet with ONLY the questions (text, figures, tables, options) — no answers, explanations or checking.
import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../exam/cards.dart' show Fig, TableView, Tag, tablesOf, texOpts, texStem;
import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/art.dart' show Ic;
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../widgets/rich.dart';
import 'presenter.dart';

// ---------------------------------------------------------------- teacher: browse + tick
String _src = 'matric', _subj = 'all', _grade = 'all', _unit = 'all', _q = '';
bool _onlySel = false;

String _qGrade(Question q) {
  final g = q.textbookRef?['grade'];
  if (g is num) return g.toInt().toString();
  if (g is String && RegExp(r'^\d{1,2}$').hasMatch(g)) return g;
  final m = RegExp(r'(?:Grade\s+|exercise_[a-z_]+_)(\d{1,2})\b').firstMatch('${q.exam.year} ${q.exam.id}');
  return m?.group(1) ?? '';
}

String _qUnit(Question q) {
  final u = str(q.textbookRef?['unit']);
  if (u.isNotEmpty) return u;
  final raw = str(q.j['unit']);
  if (raw.isEmpty) return 'Unmapped';
  if (raw.startsWith('general')) return 'General';
  final m = RegExp(r'-u(\d+)$').firstMatch(raw);
  return m != null ? 'Unit ${m.group(1)}' : raw;
}

int _unitRank(String u) {
  if (u == 'Unmapped') return 1000;
  if (u == 'General') return 999;
  return int.tryParse(RegExp(r'Unit\s+(\d+)').firstMatch(u)?.group(1) ?? '') ?? 500;
}

void _setSrc(String v) {
  _src = v;
  _unit = 'all';
}

void _setSubj(String v) {
  _subj = v;
  _unit = 'all';
}

void _setGrade(String v) {
  _grade = v;
  _unit = 'all';
}

class TeacherPage extends StatefulWidget with NoNav {
  const TeacherPage({super.key});
  @override
  State<TeacherPage> createState() => _TeacherPageState();
}

class _TeacherPageState extends State<TeacherPage> {
  late final _c = TextEditingController(text: _q);
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  List<Question> _pool(HighState s) => _src == 'matric'
      ? [for (final e in s.repo.exams) ...e.questions]
      : [for (final e in s.repo.exerciseExams.values.toList()..sort((a, b) => '${a.year}${a.subject}'.compareTo('${b.year}${b.subject}'))) ...e.questions];

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, cd = s.repo.codes;
    final pool = _pool(s);
    final subjects = {for (final q in pool) q.exam.subject}.toList()..sort();
    if (_subj != 'all' && !subjects.contains(_subj)) {
      _subj = 'all';
      _unit = 'all';
    }
    final afterSubj = [for (final q in pool) if (_subj == 'all' || q.exam.subject == _subj) q];
    final grades = {
      for (final q in afterSubj) _qGrade(q),
    }.where((g) => g == '9' || g == '10' || g == '11' || g == '12').toList()
      ..sort();
    if (_grade != 'all' && !grades.contains(_grade)) {
      _grade = 'all';
      _unit = 'all';
    }
    final afterGrade = [for (final q in afterSubj) if (_grade == 'all' || _qGrade(q) == _grade) q];
    final units = {for (final q in afterGrade) _qUnit(q)}.toList()
      ..sort((a, b) {
        final c = _unitRank(a) - _unitRank(b);
        return c != 0 ? c : a.compareTo(b);
      });
    if (_unit != 'all' && !units.contains(_unit)) _unit = 'all';
    final words = _q.toLowerCase().split(RegExp(r'\s+')).where((w) => w.isNotEmpty).toList();
    final list = pool.where((q) {
      if (_onlySel && !s.basket.contains(q.id)) return false;
      if (_subj != 'all' && q.exam.subject != _subj) return false;
      if (_grade != 'all' && _qGrade(q) != _grade) return false;
      if (_unit != 'all' && _qUnit(q) != _unit) return false;
      if (words.isEmpty) return true;
      final code = cd?.codeOf(q.id)?.toLowerCase() ?? '';
      final hay = '${q.stem} ${q.exam.name} ${q.exam.year} ${_qGrade(q)} ${_qUnit(q)} ${(q.options ?? const {}).values.join(' ')}'.toLowerCase();
      return words.every((w) => w == code || hay.contains(w));
    }).toList();
    list.sort((a, b) {
      final ua = _qUnit(a), ub = _qUnit(b);
      final c = _unitRank(ua) - _unitRank(ub);
      if (c != 0) return c;
      final d = ua.compareTo(ub);
      if (d != 0) return d;
      final y = a.exam.year.compareTo(b.exam.year);
      if (y != 0) return y;
      return a.number.compareTo(b.number);
    });
    final rows = <Object>[];
    String? lastUnit;
    for (final q in list) {
      final u = _qUnit(q);
      if (u != lastUnit) {
        rows.add(u);
        lastUnit = u;
      }
      rows.add(q);
    }
    final n = s.basket.length;
    return PageShell(
      top: TopBar(title: 'Teacher', sub: 'Pick by subject, grade and unit', onBack: HighNav.of(context).back, tab: false),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 6, 16, 0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 10,
              children: [
                Seg(
                  current: _src,
                  items: [
                    (id: 'matric', label: 'Matric', icon: 'trophy', count: null, tone: 'sage', enabled: true),
                    (id: 'exercise', label: 'Exercise', icon: 'pen', count: null, tone: 'sage', enabled: true),
                  ],
                  onPick: (v) => setState(() => _setSrc(v)),
                ),
                Field(controller: _c, placeholder: 'Search text or a code…', search: true, onChanged: (v) => setState(() => _q = v)),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  clipBehavior: Clip.none,
                  child: Row(
                    spacing: 8,
                    children: [
                      ChipX('Selected', small: true, icon: 'check', count: n, on: _onlySel, onTap: () => setState(() => _onlySel = !_onlySel)),
                      ChipX('All subjects', small: true, on: _subj == 'all', onTap: () => setState(() => _setSubj('all'))),
                      for (final sj in subjects) ChipX(sj, small: true, tone: look(sj).tone, on: _subj == sj, onTap: () => setState(() => _setSubj(sj))),
                    ],
                  ),
                ),
                if (grades.isNotEmpty)
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    clipBehavior: Clip.none,
                    child: Row(
                      spacing: 8,
                      children: [
                        ChipX('All grades', small: true, on: _grade == 'all', onTap: () => setState(() => _setGrade('all'))),
                        for (final g in grades) ChipX('Grade $g', small: true, on: _grade == g, onTap: () => setState(() => _setGrade(g))),
                      ],
                    ),
                  ),
                if (units.isNotEmpty)
                  SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    clipBehavior: Clip.none,
                    child: Row(
                      spacing: 8,
                      children: [
                        ChipX('All units', small: true, on: _unit == 'all', onTap: () => setState(() => _unit = 'all')),
                        for (final u in units)
                          ChipX(u, small: true, on: _unit == u, onTap: () => setState(() => _unit = u)),
                      ],
                    ),
                  ),
                Text('${thousands(list.length)} question${list.length == 1 ? '' : 's'}', style: ts(12.5, w800, p.ink3)),
              ],
            ),
          ),
          Expanded(
            child: ScrollConfiguration(
              behavior: const NoGlow(),
              child: ListView.builder(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 150),
                itemCount: rows.length,
                itemBuilder: (c, i) {
                  final row = rows[i];
                  if (row is String) {
                    final nIn = list.where((q) => _qUnit(q) == row).length;
                    return Padding(
                      padding: EdgeInsets.fromLTRB(2, i == 0 ? 4 : 14, 2, 8),
                      child: Text(nIn == 0 ? row : '$row · $nIn', style: ts(12.5, w800, p.ink3)),
                    );
                  }
                  final q = row as Question;
                  return _PickRow(q: q, code: cd?.codeOf(q.id) ?? '?', on: s.basket.contains(q.id));
                },
              ),
            ),
          ),
          Container(
            padding: EdgeInsets.fromLTRB(16, 10, 16, 16 + MediaQuery.paddingOf(context).bottom),
            decoration: k.d.raised(p.surface, radius: 26),
            child: Row(
              spacing: 10,
              children: [
                Expanded(child: Text(n == 0 ? 'Tick questions to build a set' : '$n selected', style: ts(15, w900, p.ink))),
                if (n > 0) Btn('Clear', kind: BtnKind.soft, onTap: s.clearBasket),
                if (n > 0) CBtn('play', label: 'Present on TV', onTap: () => HighNav.of(context).push(PresenterPage(slides: [for (final (i, id) in cd!.canonical(s.basket).indexed) QuestionSlide(s.repo.byId[id]!, n: i + 1)]))),
                Btn('Show on board', icon: 'play', enabled: n > 0, onTap: () => HighNav.of(context).push(BoardPage(ids: List.of(s.basket)))),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _PickRow extends StatelessWidget {
  const _PickRow({required this.q, required this.code, required this.on});
  final Question q;
  final String code;
  final bool on;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, lk = look(q.exam.subject);
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Press(
        onTap: () => k.s.toggleBasket(q.id),
        selected: on,
        deco: k.d.raised(on ? k.tone('sage').tile : p.surface, radius: 18),
        pressedDeco: k.d.optPressed(),
        dy: 3,
        padding: const EdgeInsets.all(12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          spacing: 12,
          children: [
            Knob(tone: on ? 'sage' : lk.tone, size: 36, child: on ? Ic('check', size: 18, color: k.tone('sage').deep) : Text('', style: ts(10, w900, p.ink))),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    spacing: 6,
                    children: [
                      Text(code, style: ts(14, w900, k.tone(lk.tone).deep, spacing: 1.2)),
                      Flexible(child: Text('${q.exam.name} · ${yearShort(q.exam.year)} · ${q.label}', maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(12, w700, p.ink3))),
                    ],
                  ),
                  Padding(padding: const EdgeInsets.only(top: 3), child: RichTx((q.isMatch ? q.matchPrompt : q.stem).replaceAll(RegExp(r'<[^>]+>'), ''), maxLines: 2, style: ts(13.5, w700, p.ink, height: 1.4))),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------- board (big codes)
class BoardPage extends StatelessWidget with NoNav {
  const BoardPage({super.key, required this.ids});
  final List<String> ids;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, cd = k.s.repo.codes!;
    final list = cd.canonical(ids), set = cd.setCode(list);
    final w = MediaQuery.sizeOf(context).width, big = (w / 9).clamp(38.0, 140.0), small = (w / 22).clamp(20.0, 64.0);
    return PageShell(
      top: TopBar(
        title: 'Board',
        sub: '${list.length} questions · students tap "Enter class code"',
        onBack: HighNav.of(context).back,
        tab: false,
        actions: [CBtn('play', label: 'Present on TV', onTap: () => HighNav.of(context).push(PresenterPage(slides: [for (final (i, id) in list.indexed) QuestionSlide(k.s.repo.byId[id]!, n: i + 1)])))],
      ),
      body: ScreenList(
        children: [
          Panel(
            tone: 'sage',
            padding: const EdgeInsets.fromLTRB(18, 18, 18, 22),
            child: Column(
              children: [
                Text('CLASS CODE', style: ts(small * .6, w900, p.ink2, spacing: 2)),
                FittedBox(fit: BoxFit.scaleDown, child: Text(set, style: ts(big, w900, p.ink, spacing: big * .08, height: 1.2))),
                Text('or type the question codes below', style: ts(small * .55, w700, p.ink2)),
              ],
            ),
          ),
          Panel(
            padding: const EdgeInsets.all(18),
            child: Wrap(
              spacing: small * 1.2,
              runSpacing: small * .5,
              children: [
                for (final (i, id) in list.indexed)
                  Text.rich(
                    TextSpan(children: [
                      TextSpan(text: '${i + 1}. ', style: ts(small * .7, w800, p.ink3)),
                      TextSpan(text: cd.codeOf(id), style: ts(small, w900, p.ink, spacing: small * .08)),
                    ]),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------- student: enter a class code
class EnterCodePage extends StatefulWidget {
  const EnterCodePage({super.key});
  @override
  State<EnterCodePage> createState() => _EnterCodePageState();
}

class _EnterCodePageState extends State<EnterCodePage> {
  final _c = TextEditingController();
  String? _err;
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  void _open() {
    final s = HighScope.read(context), cd = s.repo.codes;
    if (cd == null) return;
    final r = cd.parse(_c.text);
    if (r.ids.isEmpty || r.bad.isNotEmpty) {
      setState(() => _err = r.bad.isNotEmpty ? 'Unknown code${r.bad.length > 1 ? 's' : ''}: ${r.bad.join(', ')}. Check the letters (codes never use O, 0, I or 1).' : 'Type the class code from the board.');
      return;
    }
    setState(() => _err = null);
    final code = QCodesX.label(cd.setCode(r.ids), r.ids.length);
    s.saveHomework(code, r.ids);
    HighNav.of(context).open('hw:$code', () => HomeworkPage(ids: r.ids, code: code));
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    return PageShell(
      top: TopBar(title: 'Class code', sub: 'Homework from your teacher', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Panel(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 12,
              children: [
                Text('Type the class code (or the question codes) from the board', style: ts(15, w900, p.ink)),
                Field(fieldKey: const ValueKey('classCode'), controller: _c, placeholder: 'e.g. 7KQ2MX', onSubmitted: (_) => _open()),
                if (_err != null) Text(_err!, style: ts(13, w800, p.peach.deep)),
                Btn('Open homework', icon: 'book', block: true, onTap: _open),
              ],
            ),
          ),
          if (s.homework.isNotEmpty) ...[
            SectionLabel('Recent homework', n: s.homework.length, icon: 'cal'),
            for (final h in s.homework)
              Panel(
                padding: const EdgeInsets.all(14),
                onTap: () {
                  final ids = [for (final x in h['ids'] as List) if (s.repo.byId.containsKey(x)) x as String];
                  HighNav.of(context).open('hw:${h['code']}', () => HomeworkPage(ids: ids, code: h['code'] as String));
                },
                child: Row(
                  spacing: 12,
                  children: [
                    const Badge('blue', 'book', s: 38),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(h['code'] as String, style: ts(16, w900, p.ink, spacing: 1)),
                          Text('${(h['ids'] as List).length} questions · ${ago((h['t'] as num).toInt())}', style: ts(12.5, w700, p.ink3)),
                        ],
                      ),
                    ),
                    Ic('right', size: 20, color: p.ink3),
                  ],
                ),
              ),
          ],
        ],
      ),
    );
  }
}

abstract final class QCodesX {
  static String label(String setCode, int n) => setCode;
}

// ---------------------------------------------------------------- homework sheet (questions only)
class HomeworkPage extends StatelessWidget {
  const HomeworkPage({super.key, required this.ids, required this.code});
  final List<String> ids;
  final String code;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, cd = s.repo.codes;
    final qs = [for (final id in ids) ?s.repo.byId[id]];
    final shownPassages = <String>{};
    return PageShell(
      top: TopBar(title: 'Homework', sub: '$code · ${qs.length} questions', onBack: HighNav.of(context).back, tab: false),
      body: ScreenList(
        children: [
          Panel(
            tone: 'blue',
            padding: const EdgeInsets.all(16),
            child: Row(
              spacing: 12,
              children: [
                const Badge('blue', 'pen', s: 44),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Homework $code', style: ts(18, w900, p.ink)),
                      Text('Write your answers in your exercise book, numbered 1–${qs.length}.', style: ts(13, w700, p.ink2)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          for (final (i, q) in qs.indexed) ...[
            if (q.passageId != null && q.exam.passages[q.passageId] != null && shownPassages.add(q.passageId!))
              Panel(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  spacing: 8,
                  children: [
                    Text(str(q.exam.passages[q.passageId]!['title']).isEmpty ? 'Read the passage' : str(q.exam.passages[q.passageId]!['title']), style: ts(15, w900, p.ink)),
                    RichTx(str(q.exam.passages[q.passageId]!['text']), style: ts(14, w600, p.ink, height: 1.55)),
                  ],
                ),
              ),
            _HwQuestion(n: i + 1, q: q, code: cd?.codeOf(q.id) ?? ''),
          ],
        ],
      ),
    );
  }
}

class _HwQuestion extends StatelessWidget {
  const _HwQuestion({required this.n, required this.q, required this.code});
  final int n;
  final Question q;
  final String code;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, lk = look(q.exam.subject);
    final tx = texOpts(q);
    final opts = q.isMatch ? q.matchList!.choices : (q.options ?? const <String, String>{});
    return Panel(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Row(
            spacing: 10,
            children: [
              Text('Question $n', style: ts(19, w900, k.tone(lk.tone).deep)),
              const Spacer(),
              Tag(code, tone: lk.tone),
            ],
          ),
          Padding(padding: const EdgeInsets.only(top: 2, bottom: 10), child: Text('${q.exam.subject} · ${q.exam.isExercise ? q.exam.year : '${q.exam.short} ${yearShort(q.exam.year)}'}', style: ts(12, w700, p.ink3))),
          if (q.isMatch && q.matchList!.instructions.isNotEmpty) Padding(padding: const EdgeInsets.only(bottom: 6), child: RichTx(q.matchList!.instructions, style: ts(13, w700, p.ink2))),
          RichTx(q.isMatch ? q.matchPrompt : texStem(q), tex: q.stemTex != null, style: ts(15.5, w700, p.ink, height: 1.5)),
          for (final t in tablesOf(q.j['stem_tables'])) Padding(padding: const EdgeInsets.only(top: 10), child: TableView(t)),
          if (q.image != null) Padding(padding: const EdgeInsets.only(top: 10), child: Fig(path: q.image!, alt: q.imageAlt, exam: q.exam)),
          if (opts.isNotEmpty) ...[
            if (q.isMatch) Padding(padding: const EdgeInsets.only(top: 10), child: Text('Choose from:', style: ts(12.5, w800, p.ink3))),
            for (final e in opts.entries)
              Container(
                margin: const EdgeInsets.only(top: 8),
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                decoration: k.d.raisedSoft(p.surface2, radius: 14),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  spacing: 10,
                  children: [
                    Text(e.key, style: ts(14.5, w900, p.ink2)),
                    Expanded(child: RichTx(tx?[e.key] ?? e.value, tex: tx?[e.key] != null, style: ts(14.5, w700, p.ink, height: 1.4))),
                  ],
                ),
              ),
          ],
          for (final sp in q.subparts)
            Padding(
              padding: const EdgeInsets.only(top: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  RichTx('${str(sp['label'])}. ${str(sp['question'])}${sp['marks'] != null ? ' (${sp['marks']} pt)' : ''}', style: ts(14, w800, p.ink, height: 1.45)),
                  if (sp['image'] != null) Fig(path: str(sp['image']), alt: sp['image_alt'] as String?, exam: q.exam),
                ],
              ),
            ),
          if (!q.isScored && q.subparts.isEmpty && q.marks != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text('(${q.marks} pt)', style: ts(12.5, w800, p.ink3))),
        ],
      ),
    );
  }
}

/// "Enter class code" card (Home / Exercise tab)
class ClassCodeCard extends StatelessWidget implements Spaced {
  const ClassCodeCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    return Panel(
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.all(14),
      onTap: () => HighNav.of(context).open('classcode', () => const EnterCodePage()),
      child: Row(
        spacing: 12,
        children: [
          const Badge('blue', 'book', s: 42),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Enter class code', style: ts(15, w900, p.ink)),
                Text(s.homework.isEmpty ? 'Homework from your teacher' : 'Last: ${s.homework.first['code']}', style: ts(12.5, w700, p.ink2)),
              ],
            ),
          ),
          Ic('right', size: 20, color: p.ink3),
        ],
      ),
    );
  }
}

/// Home card shown in teacher mode
class TeacherCard extends StatelessWidget implements Spaced {
  const TeacherCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s;
    if (!s.teacher) return const SizedBox.shrink();
    return Panel(
      tone: 'lilac',
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.all(14),
      onTap: () => HighNav.of(context).open('teacher', () => const TeacherPage()),
      child: Row(
        spacing: 12,
        children: [
          const Badge('lilac', 'grid', s: 42),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Teacher: build a class set', style: ts(15, w900, p.ink)),
                Text(s.basket.isEmpty ? 'Pick questions, show codes on the board' : '${s.basket.length} selected', style: ts(12.5, w700, p.ink2)),
              ],
            ),
          ),
          Ic('right', size: 20, color: p.ink3),
        ],
      ),
    );
  }
}
