// Turns a search over the Tutor index into an answer: the best explanation chunk (a notes card, glossary entry, tip,
// unit-quiz question, exam-pack concept or, when the notes say little, a past-paper explanation) laid out step by step,
// where it lives in the app (+ a deep link), other matching notes cards, a lab / interactive card to try, related
// exercise-bank questions and matching matric / model questions.
import '../data/models.dart';
import '../data/repository.dart';
import '../notes/jr/data/notes_models.dart';
import '../notes/jr/data/repository.dart';
import 'tutor_index.dart';

/// one line of an answer: h = heading, p = paragraph, step = numbered step, ans = the answer line, row = table row
class TBlock {
  const TBlock(this.kind, this.text, {this.n = 0});
  final String kind, text;
  final int n;
}

/// a place in the notes: [focus] is a UnitPage focus key (`lessonId~i`, `sec:memory`, `sec:questions`) or null
class TRef {
  TRef(this.doc, this.title, this.where, this.unit, this.focus, {this.media = ''});
  final int doc;
  final String title, where, media;
  final TUnit? unit;
  final String? focus;
}

/// filters: hard ones restrict the search, the "focus" ones (the notes book the student came from) only rank first
class TutorScope {
  const TutorScope({this.subject, this.grade, this.focusSubject, this.focusGrade});
  final String? subject, focusSubject;
  final int? grade, focusGrade;
  bool get hard => subject != null || grade != null;
}

class TutorAnswer {
  TutorAnswer({
    required this.query,
    this.refuse = false,
    this.title = '',
    this.where = '',
    this.blocks = const [],
    this.notesTex = true,
    this.open,
    this.also = const [],
    this.lab,
    this.practice = const [],
    this.matric = const [],
    this.notes = const [],
    this.result,
  });
  final String query, title, where;
  final bool refuse, notesTex;
  final List<TBlock> blocks;
  final TRef? open;
  final List<TRef> also;
  final TRef? lab;
  final List<Question> practice, matric;

  /// small print: typo fixes, filter fallbacks, textbook reference
  final List<String> notes;
  final TutorResult? result;
}

class TutorAnswerer {
  TutorAnswerer(this.ix, this.repo, this.notesRepo);
  final TutorIndex ix;
  final ExamRepo repo;
  final NotesRepo notesRepo;

  static const minScore = 2.5;

  Future<TutorAnswer> answer(String query, [TutorScope scope = const TutorScope()]) async {
    var r = ix.search(query, subject: scope.subject, grade: scope.grade, preferSubject: scope.focusSubject, preferGrade: scope.focusGrade);
    final notes = <String>[];
    // nothing inside the filters: widen (grade first, then subject) and say so
    if (r.explain.isEmpty && (r.grade != null || r.subject != null)) {
      final g = r.grade, s = r.subject;
      final wider = g != null ? ix.search(query, subject: s, grade: null, ignoreQueryFilters: true) : ix.search(query, ignoreQueryFilters: true);
      final wider2 = wider.explain.isEmpty && s != null ? ix.search(query, ignoreQueryFilters: true) : wider;
      if (!wider2.empty) {
        notes.add('Nothing in ${[if (g != null) 'Grade $g', if (s != null) TutorIndex.subjectLabel(s)].join(' ')} matched, so I searched more widely.');
        r = wider2;
      }
    }
    if (r.fixed.isNotEmpty) {
      notes.add('Showing results for ${r.fixed.values.map((w) => '“$w”').join(', ')} (you typed ${r.fixed.keys.map((w) => '“$w”').join(', ')}).');
    }
    // Tigrinya only appears as glosses inside long English cards, so its BM25 scores run low: any match counts
    final ti = RegExp('[\u1200-\u137f]').hasMatch(query);
    if (r.empty || (r.best < minScore && !ti)) return TutorAnswer(query: query, refuse: true, result: r);

    final practice = await _questions(r.practice, 4);
    final matric = await _questions(r.matric, 4);
    var top = r.explain.isEmpty ? null : r.explain.first;
    final qBest = [...r.matric, ...r.practice].fold<TutorHit?>(null, (a, h) => a == null || h.score > a.score ? h : a);
    TutorAnswer? main;
    // the notes say little about it: answer from the best past-paper question with an explanation
    if (top == null || (qBest != null && top.score < .55 * qBest.score)) {
      final q = [...matric, ...practice].where((q) => q.steps.isNotEmpty).firstOrNull;
      if (q != null) main = _fromQuestion(query, q, r);
    }
    // best notes hit that resolves (a book that fails to parse is skipped, not fatal)
    for (final h in r.explain) {
      if (main != null || h.score < .5 * r.explain.first.score) break;
      main = await _fromDoc(query, h.doc, r);
      if (main != null) top = h;
    }
    if (main == null && top != null) {
      final q = [...matric, ...practice].where((q) => q.steps.isNotEmpty).firstOrNull;
      if (q != null) main = _fromQuestion(query, q, r);
    }
    if (main == null) return TutorAnswer(query: query, refuse: true, result: r);

    final seen = <String>{main.title.toLowerCase()};
    final also = <TRef>[
      for (final h in r.explain)
        if (h.doc != top?.doc &&
            ix.kind[h.doc] != TK.concept &&
            h.score >= .35 * r.explain.first.score &&
            seen.add(ix.keys[h.doc].split('\t').last.toLowerCase()))
          _ref(h.doc),
    ].take(3).toList();
    TRef? lab;
    if (r.media.isNotEmpty) {
      final best = r.media.first.score;
      final sim = r.media.where((h) => ix.keys[h.doc].startsWith('sim\t') && h.score >= .75 * best).firstOrNull ?? r.media.first;
      if (sim.score >= .45 * (top?.score ?? sim.score)) lab = _ref(sim.doc);
    }
    return TutorAnswer(
      query: query,
      title: main.title,
      where: main.where,
      blocks: main.blocks,
      notesTex: main.notesTex,
      open: main.open ?? _topicRef(r),
      also: also,
      lab: lab,
      practice: practice.where((q) => !main!.matric.contains(q)).toList(),
      matric: matric,
      notes: [...notes, ...main.notes],
      result: r,
    );
  }

  TRef _ref(int d) {
    final k = ix.kind[d], l = ix.lessonOf(d);
    final focus = switch (k) {
      TK.glossary || TK.tip => 'sec:memory',
      TK.unitQ => 'sec:questions',
      TK.intro || TK.concept => null,
      _ => l == null ? null : '${l.id}~${ix.pos[d]}',
    };
    final key = ix.keys[d];
    final tab = key.indexOf('\t');
    return TRef(d, tab < 0 ? key : key.substring(tab + 1), ix.where(d), ix.unitOf(d), focus, media: k == TK.media && tab > 0 ? key.substring(0, tab) : '');
  }

  /// the hits' questions, reading only the packs they are in: the exam packs of those ids (stubs until read, see
  /// ExamRepo.lazyExams), the Exercise bank sets of their grade + subject, a lazy matric subject when needed
  Future<List<Question>> _questions(List<TutorHit> hits, int max) async {
    final head = hits.take(max + 1).toList();
    final ids = [for (final h in head) ix.keys[h.doc]];
    final exams = [
      for (final (i, h) in head.indexed)
        if (ix.kind[h.doc] == TK.exam) ids[i],
    ];
    final bank = [
      for (final (i, h) in head.indexed)
        if (TK.practice(ix.kind[h.doc]) && repo.exerciseKeyOf(ids[i]) != null) ids[i],
    ];
    await Future.wait([if (exams.isNotEmpty) repo.ensureExamsFor(exams), if (bank.isNotEmpty) repo.ensureExercisesForIds(bank)]);
    final out = <Question>[];
    for (final h in head) {
      if (out.length >= max) break;
      final id = ix.keys[h.doc];
      var q = repo.byId[id];
      if (q == null && ix.kind[h.doc] == TK.lazy) {
        final label = ix.lazySubjects[ix.subjectOf(h.doc)];
        if (label != null) await repo.ensureLazySubject(label);
        q = repo.byId[id];
      }
      if (q != null && !q.isStub && !out.any((x) => x.stem == q!.stem)) out.add(q);
    }
    return out;
  }

  TutorAnswer _fromQuestion(String query, Question q, TutorResult r) {
    final ans = q.isScored ? (q.isMatch ? q.answerText : '${q.answer}. ${q.opts[q.answer] ?? ''}') : q.answer;
    final stem = q.stem.length > 600 ? '${q.stem.substring(0, 600)}…' : q.stem;
    final hit = [...r.matric, ...r.practice].where((h) => ix.keys[h.doc] == q.id).firstOrNull;
    final u = hit == null ? null : ix.unitOf(hit.doc);
    final unit = u == null ? null : TRef(hit!.doc, 'Unit ${u.number}: ${u.title}', ix.where(hit.doc), u, null);
    return TutorAnswer(
      query: query,
      title: 'From a past paper: ${q.exam.name} ${q.exam.year}',
      where: '${q.exam.name} ${q.exam.year} · ${q.label}',
      notesTex: false,
      blocks: [
        TBlock('p', stem),
        if (ans.trim().isNotEmpty) TBlock('ans', ans),
        for (final (i, s) in q.steps.indexed) TBlock('step', s, n: i + 1),
      ],
      open: unit,
      matric: [q],
      result: r,
    );
  }

  /// for an answer taken from a past paper: the notes card that is really about the topic (has its rarest word), if any
  TRef? _topicRef(TutorResult r) {
    final w = ix.rarest(r.terms);
    if (w == null) return null;
    final h = r.explain.where((h) => ix.kind[h.doc] != TK.concept && ix.has(h.doc, w)).firstOrNull;
    return h == null ? null : _ref(h.doc);
  }

  Future<TutorAnswer?> _fromDoc(String query, int d, TutorResult r) async {
    final k = ix.kind[d], ref = _ref(d);
    if (k == TK.concept) {
      final c = (await TutorIndex.concepts())['$d'];
      if (c == null || c.$1.trim().isEmpty) return null;
      final tb = c.$2.isEmpty ? null : c.$2;
      final notesHit = r.explain.where((h) => ix.kind[h.doc] != TK.concept).firstOrNull;
      return TutorAnswer(
        query: query,
        title: ref.title,
        where: ix.where(d),
        blocks: _paras(c.$1),
        notesTex: false,
        open: notesHit == null ? null : _ref(notesHit.doc),
        notes: [?tb],
        result: r,
      );
    }
    final u = ix.unitOf(d);
    if (u == null) return null;
    final NotesBook book;
    try {
      book = await notesRepo.unitBook(u.book, u.id); // just this unit (assets/high/notes/split), cached
    } catch (_) {
      return null;
    }
    final unit = book.unit(u.id);
    if (unit == null) return null;
    var blocks = <TBlock>[];
    var title = ref.title;
    final p = ix.pos[d];
    switch (k) {
      case TK.glossary:
        if (p >= unit.glossary.length) return null;
        final g = unit.glossary[p];
        title = g.term;
        blocks = [TBlock('p', '**${g.term}**: ${g.meaning}')];
      case TK.tip:
        if (p >= unit.tips.length) return null;
        title = 'Tip';
        blocks = _paras(unit.tips[p].text);
      case TK.unitQ:
        if (p >= unit.exercise.questions.length) return null;
        final q = unit.exercise.questions[p];
        title = 'Unit quiz question';
        final a = q.options[q.answer] != null ? '${q.answer}. ${q.options[q.answer]}' : q.answer;
        blocks = [TBlock('p', q.q), TBlock('ans', a), for (final (i, w) in q.why.indexed) TBlock('step', w, n: i + 1)];
      case TK.intro:
        title = 'Unit ${unit.number}: ${unit.title}';
        blocks = _paras(unit.intro);
      default:
        final l = ix.lessonOf(d);
        final lesson = l == null ? null : unit.lessons.where((x) => x.id == l.id).firstOrNull;
        if (lesson == null || p >= lesson.cards.length) return null;
        final c = lesson.cards[p];
        if (c.title.isNotEmpty) title = c.title;
        blocks = cardBlocks(c);
    }
    if (blocks.isEmpty) return null;
    return TutorAnswer(query: query, title: title, where: ix.where(d), blocks: blocks, open: ref, result: r);
  }

  static List<TBlock> _paras(String s) {
    final ps = s.split(RegExp(r'\n\s*\n')).map((x) => x.trim()).where((x) => x.isNotEmpty).toList();
    return ps.length <= 1 ? [for (final x in ps) TBlock('p', x)] : [for (final (i, x) in ps.indexed) TBlock('step', x, n: i + 1)];
  }

  /// a notes card as answer lines (several paragraphs / steps become numbered steps)
  static List<TBlock> cardBlocks(NoteCard c) {
    List<TBlock> list(List<String> xs) {
      final ys = [
        for (final x in xs)
          if (x.trim().isNotEmpty) x.trim(),
      ];
      return ys.length == 1 ? [TBlock('p', ys.first)] : [for (final (i, y) in ys.indexed) TBlock('step', y, n: i + 1)];
    }

    return switch (c) {
      WorkedCard() => [
        TBlock('p', c.problem),
        for (final (i, s) in c.steps.indexed) TBlock('step', s.math != null && s.math!.isNotEmpty ? '${s.text} \$${s.math}\$' : s.text, n: i + 1),
        if (c.answer.isNotEmpty) TBlock('ans', c.answer),
      ],
      TableCard() => [
        ...list(c.body),
        if (c.head.isNotEmpty) TBlock('h', c.head.join(' · ')),
        for (final row in c.rows.take(10)) TBlock('row', row.join(' · ')),
      ],
      CheckCard() => [
        TBlock('p', c.q),
        if (c.options[c.answer] != null) TBlock('ans', '${c.answer}. ${c.options[c.answer]}'),
        if (c.why.isNotEmpty) TBlock('p', c.why),
      ],
      GrammarCard() => [
        ...list([...c.body, ...c.rule]),
        if (c.pattern != null) TBlock('h', c.pattern!),
        for (final e in c.examples.take(6)) TBlock('row', '${e.ok ? '✓' : '✗'} ${e.text}${e.fix != null ? ' → ${e.fix}' : ''}'),
      ],
      MnemonicCard() => [...list(c.body), for (final l in c.letters) TBlock('row', '**${l.l}** ${l.w}${l.m.isNotEmpty ? ': ${l.m}' : ''}')],
      StepsCard() => [...list(c.body), for (final (i, s) in c.steps.indexed) TBlock('step', s.text, n: i + 1)],
      StatesCard() => [...list(c.body), for (final s in c.states) TBlock('row', '**${s.label}**: ${s.text}')],
      GraphCard() => [...list(c.body), for (final (i, s) in c.steps.indexed) TBlock('step', s.text, n: i + 1)],
      VocabCard() => [TBlock('p', '**${c.word}**: ${c.meaning}'), if (c.example.isNotEmpty) TBlock('row', c.example)],
      ReadingCard() => [...list(c.body), if (c.paras.isNotEmpty) TBlock('p', c.paras.first)],
      ModelCard() => list([...c.body, ...c.task]),
      _ => list(c.body),
    };
  }
}
