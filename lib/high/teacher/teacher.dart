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
