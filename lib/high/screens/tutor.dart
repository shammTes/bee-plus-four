// Tutor tab: Kokob, an offline BM25 tutor over the exam packs' textbook concepts and questions (web renderTutor/reply).
import 'dart:math' as math;

import 'package:flutter/widgets.dart';

import '../data/models.dart';
import '../data/repository.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';
import '../widgets/rich.dart';
import 'routes.dart';

const _sub = {'₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-'};
final _stop = 'a an the of to in on for and or is are was be by with what which how why when does do did can i me my you your it its this that as at from about explain tell define give please show help want know find calculate'.split(' ').toSet();
const _syn = {'ph': 'ph acidity', 'kmt': 'kinetic molecular theory', 'electrolysis': 'electrolysis electrode', 'mole': 'mole moles avogadro', 'redox': 'oxidation reduction redox', 'plastic': 'plastics polymer', 'soap': 'soap saponification', 'nuclear': 'nuclear radioactive', 'halflife': 'half-life half life', 'vsepr': 'vsepr shape geometry', 'shape': 'shape geometry vsepr molecular', 'geometry': 'geometry shape vsepr', 'water': 'water h2o', 'dna': 'dna gene', 'gdp': 'gdp national income', 'soil': 'soil erosion'};

String _stemW(String w) {
  if (w.length > 4 && w.endsWith('ies')) return '${w.substring(0, w.length - 3)}y';
  if (w.length > 4 && w.endsWith('es') && !w.endsWith('ses')) return w.substring(0, w.length - 2);
  if (w.length > 3 && w.endsWith('s') && !w.endsWith('ss')) return w.substring(0, w.length - 1);
  return w;
}

List<String> tokens(String s) => s
    .replaceAllMapped(RegExp('[₀-₉⁰-⁹⁺⁻¹²³]'), (m) => _sub[m[0]] ?? m[0]!)
    .toLowerCase()
    .replaceAll(RegExp('half[- ]life'), 'halflife')
    .split(RegExp('[^a-z0-9+]+'))
    .where((w) => w.isNotEmpty && !_stop.contains(w) && (w.length > 1 || RegExp(r'\d').hasMatch(w)))
    .map(_stemW)
    .toList();

class _Doc {
  _Doc(this.subject, this.concept, this.q, String text) {
    for (final w in tokens(text)) {
      tf[w] = (tf[w] ?? 0) + 1;
      len++;
    }
  }
  final String subject;
  final Concept? concept;
  final Question? q;
  final tf = <String, int>{};
  int len = 0;
}

class TutorIndex {
  TutorIndex(ExamRepo r) {
    for (final c in r.concepts) {
      final kw = strs(c.sub['keywords']).join(' ');
      docs.add(_Doc(c.subject, c, null, [c.sub['title'], c.sub['title'], c.sub['concept'], kw, kw, c.topic['title']].map(str).join(' ')));
    }
    for (final e in r.exams) {
      for (final q in e.questions) {
        final kw = q.keywords.join(' ');
        docs.add(_Doc(e.subject, null, q, [q.stem, q.stem, kw, kw, q.topics.join(' ').replaceAll('-', ' '), q.isMCQ ? q.options!.values.join(' ') : q.answer, q.steps.join(' ')].join(' ')));
      }
    }
    for (final d in docs) {
      avg += d.len;
      for (final w in d.tf.keys) {
        df[w] = (df[w] ?? 0) + 1;
      }
    }
    avg /= math.max(1, docs.length);
  }
  final docs = <_Doc>[];
  final df = <String, int>{};
  double avg = 0;
  static TutorIndex? _i;
  static TutorIndex of(ExamRepo r) => _i ??= TutorIndex(r);

  List<({_Doc d, double s, double cov})> bm25(List<String> qt) {
    const k1 = 1.4, b = .72;
    final n = docs.length;
    double idf(String w) => df[w] != null ? math.log(1 + (n - df[w]! + .5) / (df[w]! + .5)) : math.log(1 + n);
    final total = qt.fold<double>(0, (a, w) => a + idf(w));
    final out = <({_Doc d, double s, double cov})>[];
    for (final d in docs) {
      var s = 0.0, cov = 0.0;
      for (final w in qt) {
        final f = d.tf[w];
        if (f == null) continue;
        final i = idf(w);
        cov += i;
        s += i * f * (k1 + 1) / (f + k1 * (1 - b + b * d.len / avg));
      }
      if (s > 0) out.add((d: d, s: s, cov: cov / (total == 0 ? 1 : total)));
    }
    out.sort((a, b) => b.s.compareTo(a.s));
    return out;
  }
}

class _Msg {
  _Msg(this.me, this.text, {this.title, this.ref, this.qs = const [], this.refuse = false});
  final bool me, refuse;
  final String text;
  final String? title, ref;
  final List<Question> qs;
}

final _chat = <_Msg>[];

class TutorPage extends StatefulWidget {
  const TutorPage({super.key});
  @override
  State<TutorPage> createState() => _TutorPageState();
}

class _TutorPageState extends State<TutorPage> {
  final _c = TextEditingController();
  final _sc = ScrollController();

  _Msg _reply(ExamRepo r, String text) {
    final ix = TutorIndex.of(r);
    final raw = tokens(text).toSet();
    final qt = {for (final w in raw) ...(_syn[w] != null ? tokens(_syn[w]!) : [w])}.toList();
    final known = qt.where(ix.df.containsKey).length;
    final res = qt.isEmpty ? const <({_Doc d, double s, double cov})>[] : ix.bm25(qt);
    final bestCov = res.take(5).fold<double>(0, (a, x) => math.max(a, x.cov));
    if (qt.isEmpty || res.isEmpty || res.first.s < 2.2 || known / qt.length < .5 || bestCov < .6) {
      return _Msg(false, 'I only answer from the questions and textbook concepts stored on this device. Try another topic from your subjects.', title: "Sorry — that's outside your exam packs 🙏", refuse: true);
    }
    final top = res.first.s;
    final concept = res.where((x) => x.d.concept != null && x.s >= top * .45).firstOrNull?.d.concept;
    final qs = res.where((x) => x.d.q != null).take(4).where((x) => x.s >= top * .35).map((x) => x.d.q!).toList();
    String? ref;
    if (concept != null) {
      final refs = concept.sub['textbook_refs'];
      if (refs is List && refs.isNotEmpty && refs.first is Map) {
        final f = refs.first as Map;
        ref = 'Textbook: ${concept.subject} Grade ${f['grade']} · ${f['section']} · p.${f['page']}';
      }
    }
    return _Msg(false, concept != null ? str(concept.sub['concept']) : 'These exam questions match what you asked:', title: concept != null ? '📘 ${shortTitle(str(concept.sub['title']))}' : "Here's what I found", ref: ref, qs: qs);
  }

  void _ask(String t) {
    t = t.trim();
    if (t.isEmpty) return;
    final r = Kit.of(context).s.repo;
    setState(() {
      _chat.add(_Msg(true, t));
      _chat.add(_reply(r, t));
      _c.clear();
    });
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_sc.hasClients) _sc.jumpTo(_sc.position.maxScrollExtent);
    });
  }

  List<String> _sugg(ExamRepo r) {
    final out = <String>[];
    for (final c in r.concepts) {
      final st = shortTitle(str(c.sub['title']));
      if (st.length <= 24 && st.contains(' ')) out.add(st.toLowerCase());
    }
    final seen = <String>{};
    return out.where(seen.add).take(8).toList();
  }

  @override
  void dispose() {
    _c.dispose();
    _sc.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p, s = k.s, r = s.repo;
    Widget bot(Widget child, {bool refuse = false}) => Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        spacing: 8,
        children: [
          const Kokob(width: 38),
          Flexible(child: Container(padding: const EdgeInsets.all(14), decoration: k.d.msgBot(t: refuse ? k.tone('peach') : null), child: child)),
        ],
      ),
    );
    final msgs = <Widget>[
      bot(
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Selam ${s.name ?? 'Student'}! I'm Kokob, your offline tutor 👋", style: ts(15, w900, p.ink)),
            Padding(padding: const EdgeInsets.only(top: 4), child: Text('Ask me about any topic in your ${r.subjects.join(', ')} exam packs. I explain the concept, point you to the textbook and quiz you on real exam questions.', style: ts(13.5, w700, p.ink2, height: 1.45))),
          ],
        ),
      ),
      for (final m in _chat)
        m.me
            ? Align(
                alignment: Alignment.centerRight,
                child: Container(margin: const EdgeInsets.symmetric(vertical: 6), padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10), decoration: k.d.msgMe(), child: Text(m.text, style: ts(14, w800, p.onCoral))),
              )
            : bot(
                refuse: m.refuse,
                Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  spacing: 6,
                  children: [
                    if (m.title != null) Text(m.title!, style: ts(15, w900, p.ink)),
                    RichTx(m.text, style: ts(13.5, w700, p.ink2, height: 1.45)),
                    if (m.ref != null) Text(m.ref!, style: ts(12, w800, p.ink3)),
                    for (final q in m.qs)
                      Press(
                        onTap: () => HighNav.of(context).push(PracticePage(examId: q.exam.id, focus: q.id)),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                          decoration: k.d.raised(p.surface2, radius: 12),
                          child: RichTx('${q.exam.name} ${yearShort(q.exam.year)} · ${q.label}: ${q.stem}', maxLines: 2, style: ts(12.5, w700, p.ink)),
                        ),
                      ),
                    if (m.qs.any((q) => q.isScored))
                      Btn('Quiz me on this (${m.qs.where((q) => q.isScored).length})', icon: 'play', onTap: () => HighNav.of(context).push(QuizPage(ids: [for (final q in m.qs) if (q.isScored) q.id], title: 'Quiz', sub: 'From your tutor chat'))),
                  ],
                ),
              ),
    ];
    return PageShell(
      top: const TopBar(title: 'Tutor', sub: 'Offline · answers only from your exam packs'),
      body: Column(
        children: [
          Expanded(
            child: ScrollConfiguration(
              behavior: const NoGlow(),
              child: ListView(controller: _sc, padding: const EdgeInsets.fromLTRB(16, 4, 16, 12), children: msgs),
            ),
          ),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 8),
            child: Row(spacing: 8, children: [for (final t in _sugg(r)) ChipX(t, small: true, icon: 'sparkle', onTap: () => _ask(t))]),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(16, 0, 16, kScreenBottom - 20 + MediaQuery.paddingOf(context).bottom),
            child: Row(
              spacing: 8,
              children: [
                Expanded(child: Field(controller: _c, placeholder: 'Ask about any topic…', onSubmitted: _ask)),
                CBtn('send', onTap: () => _ask(_c.text)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
