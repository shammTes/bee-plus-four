// Ported from Junior (junior_flutter/lib/junior/screens/unit_page.dart) by tool/port_junior_notes.py; High glue edits marked "High:".
// Unit page (`R.nunit`): ONE scrolling page – notes cards of every lesson, memory tricks + key words, inline games, exercise
// questions – with a sticky jump bar (Notes · Memory · Games · Questions) that follows the section in view.
import 'dart:async';

import 'package:flutter/widgets.dart';

import '../data/notes_models.dart';
import '../data/subjects.dart';
import '../notes/cards.dart';
import '../notes/exercise.dart';
import '../notes/games.dart';
import '../notes/rich.dart';
import '../notes/session.dart';
import '../notes/svg_prep.dart';
import '../notes/ui.dart';
import '../state/app_state.dart';
import '../theme/clay.dart';
import '../theme/notes_styles.dart';
import '../theme/tokens.dart';
import '../widgets/clay_widgets.dart';
import '../widgets/page.dart';
import '../widgets/tx.dart';
import 'shell.dart';
// High: concept map + matric questions, High top bar
import '../../../screens/routes.dart' as hr;
import '../../../widgets/page.dart' as hp;
import '../data/repository.dart';
import '../../concept_map.dart';
import '../../../teacher/presenter.dart';
import '../../../widgets/kit.dart' as hc;
import '../../../theme/perf.dart';

class UnitPage extends StatefulWidget with hp.NoNav {
  const UnitPage({super.key, required this.bookId, required this.unitId, this.focus, this.section});
  /// High: open at a section ('map', 'questions', 'matric' …)
  final String? section;
  final String bookId, unitId;

  /// element to show at the top on open: a card key `lessonId~i`, `g:gameId` or `sec:section`
  final String? focus;
  @override
  State<UnitPage> createState() => UnitPageState();
}

class UnitPageState extends State<UnitPage> {
  NotesBook? _book;
  bool _ready = false;
  final _scroll = ScrollController();
  final _cardKeys = <String, GlobalKey>{};
  final _secKeys = <String, GlobalKey>{};
  final _gameKeys = <String, GlobalKey>{};
  final _quizKeys = <String, GlobalKey>{};
  String? _jumpOn;
  Timer? _progT;
  bool _focused = false;

  /// bumped when reading progress changes: only the progress line + bar rebuild, not every card on screen
  final _progTick = ValueNotifier<int>(0);

  /// scroll tracking runs at most every [_trackGap] (plus once when the list settles), not for every scrolled pixel
  static const _trackGap = Duration(milliseconds: 90);
  final _trackClock = Stopwatch();
  Timer? _trackT;

  /// the opened-at element is held at the top while pictures / maths above it finish sizing (until the user scrolls)
  GlobalKey? _holdKey;
  DateTime _holdUntil = DateTime(0);

  AppState get _s => AppScope.read(context);
  Unit? get unit => _book?.unit(widget.unitId);

  @override
  void initState() {
    super.initState();
    _load();
    _scroll.addListener(_onScroll);
  }

  Future<void> _load() async {
    final s = AppScope.read(context);
    // only this unit is read and parsed (split file, background isolate), not the whole textbook
    final b = await s.repo.unitBook(widget.bookId, widget.unitId);
    final u = b.unit(widget.unitId);
    if (u != null) {
      final ctx = UnitCtx(u, widget.bookId, s.repo.svgPath);
      await SvgStore.preload(s.repo.bundle, ctx.svgPaths);
    }
    if (!mounted) return;
    s.setLast(widget.bookId, widget.unitId);
    setState(() {
      _book = b;
      _ready = true;
    });
    WidgetsBinding.instance.addPostFrameCallback((_) => _afterFirstLayout());
  }

  void _afterFirstLayout() {
    if (!mounted) return;
    final f = widget.focus ?? (widget.section != null ? 'sec:${widget.section}' : null);
    if (f != null && !_focused) {
      _focused = true;
      final key = f.startsWith('g:') ? _gameKeys[f.substring(2)] : (f.startsWith('sec:') ? _secKeys[f.substring(4)] : _cardKeys[f]);
      if (key != null) {
        scrollToKey(key, smooth: false);
        _holdKey = key;
        _holdUntil = DateTime.now().add(const Duration(seconds: 3));
      }
    }
    _track();
  }

  @override
  void dispose() {
    _progT?.cancel();
    _trackT?.cancel();
    _progTick.dispose();
    _scroll.dispose();
    NotesSession.stopTimers();
    super.dispose();
  }

  // ---- scrolling
  /// scroll an element just under the sticky jump bar (web `scroll-margin-top: 84px`, lands 96px below the screen top): smooth when near, a jump when far
  void scrollToKey(GlobalKey key, {bool smooth = true, int tries = 0}) {
    final ctx = key.currentContext;
    if (ctx == null) return _seek(key, tries);
    if (!_scroll.hasClients) return;
    final ro = ctx.findRenderObject() as RenderBox?;
    final vpBox = _scroll.position.context.notificationContext?.findRenderObject() as RenderBox?;
    if (ro == null || !ro.hasSize || vpBox == null || !vpBox.hasSize) return;
    // measured from the screen top (the sticky jump bar overlaps the first 82px, like the web's #screen); Chrome settles
    // `scrollIntoView` + `scroll-margin-top: 84px` 96px below the screen top once the page is fully laid out
    final pos = _scroll.position;
    final dy = ro.localToGlobal(Offset.zero, ancestor: vpBox).dy;
    final target = (pos.pixels + dy - 96).clamp(pos.minScrollExtent, pos.maxScrollExtent);
    if (smooth && (target - pos.pixels).abs() < 2.5 * pos.viewportDimension) {
      _scroll.animateTo(target, duration: const Duration(milliseconds: 420), curve: Curves.easeInOut);
    } else {
      _scroll.jumpTo(target);
    }
  }

  /// list index of every keyed item (cards, sections, games): the list is lazy, so a far target has no context yet
  final _keyIndex = <GlobalKey, int>{};
  int _itemCount = 0;

  /// direction of the last item-based estimate in [_seek] (-1 up, 1 down, 0 none yet)
  int _seekDir = 0;

  /// [key]'s item is not built yet (it is further than the read-ahead): jump towards it, estimating from the items that
  /// are built, and try again next frame (the jump bar and "open at card" would otherwise do nothing)
  void _seek(GlobalKey key, int tries) {
    final idx = _keyIndex[key];
    if (idx == null || tries >= 24 || !_scroll.hasClients) return;
    if (tries == 0) _seekDir = 0;
    int? lo, hi;
    var h = 0.0, n = 0;
    for (final e in _keyIndex.entries) {
      final ro = e.key.currentContext?.findRenderObject();
      if (ro is! RenderBox || !ro.hasSize) continue;
      lo = lo == null || e.value < lo ? e.value : lo;
      hi = hi == null || e.value > hi ? e.value : hi;
      h += ro.size.height;
      n++;
    }
    final pos = _scroll.position;
    final avg = n == 0 ? pos.viewportDimension * .5 : h / n;
    final double target;
    if (lo == null || hi == null) {
      // nothing keyed is built here (a tall unkeyed item fills the screen): keep stepping the way the last estimate
      // pointed, a screen at a time; the max-extent ratio is only a first guess, and alternating it with the
      // item-height estimate can bounce between two spots without ever building the target
      target = tries > 0 && _seekDir != 0
          ? pos.pixels + _seekDir * pos.viewportDimension
          : pos.maxScrollExtent * idx / (_itemCount < 1 ? 1 : _itemCount);
    } else if (idx < lo) {
      _seekDir = -1;
      target = pos.pixels - (lo - idx) * avg;
    } else {
      _seekDir = 1;
      target = pos.pixels + (idx - hi + 1) * avg;
    }
    _scroll.jumpTo(target.clamp(pos.minScrollExtent, pos.maxScrollExtent));
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) scrollToKey(key, smooth: false, tries: tries + 1);
    });
  }

  void _onScroll() => _trackSoon();

  /// throttled [_track]: the card / section scan touches every mounted card's render box, so it is not run per pixel
  void _trackSoon() {
    if (!_trackClock.isRunning || _trackClock.elapsed >= _trackGap) {
      _trackClock
        ..reset()
        ..start();
      _trackT?.cancel();
      _trackT = null;
      _track();
      return;
    }
    _trackT ??= Timer(_trackGap, () {
      _trackT = null;
      if (mounted) _track();
    });
  }

  /// reading progress (a card counts once ≥30 % of it is on screen) + the jump bar's section (band 18 %–28 % of the screen)
  void _track() {
    final u = unit;
    if (u == null || !_scroll.hasClients) return;
    final screen = context.findRenderObject() as RenderBox?;
    if (screen == null || !screen.hasSize) return;
    final vpBox = _scroll.position.context.notificationContext?.findRenderObject() as RenderBox?;
    if (vpBox == null || !vpBox.hasSize) return;
    final vTop = vpBox.localToGlobal(Offset.zero).dy, vh = vpBox.size.height;
    var dirty = false;
    for (final e in _cardKeys.entries) {
      final ro = e.value.currentContext?.findRenderObject() as RenderBox?;
      if (ro == null || !ro.hasSize) continue;
      final top = ro.localToGlobal(Offset.zero).dy - vTop, h = ro.size.height;
      if (top > vh || top + h < 0) continue;
      final vis = (top + h).clamp(0, vh) - top.clamp(0, vh);
      if (h > 0 && vis / h >= .3) {
        final k = e.key.lastIndexOf('~');
        if (_s.markRead(u.id, e.key.substring(0, k), int.parse(e.key.substring(k + 1)))) dirty = true;
      }
    }
    if (dirty && _progT == null) {
      _progT = Timer(const Duration(milliseconds: 400), () {
        _progT = null;
        if (mounted) _progTick.value++;
      });
    }
    String? on;
    for (final e in _secKeys.entries) {
      final ro = e.value.currentContext?.findRenderObject() as RenderBox?;
      if (ro == null || !ro.hasSize) continue;
      final top = ro.localToGlobal(Offset.zero).dy - vTop, h = ro.size.height;
      if (top < vh * .28 && top + h > vh * .18) on = e.key;
    }
    if (on != null && on != _jumpOn) setState(() => _jumpOn = on);
  }

  void _gloss(Unit u, int i) {
    final g = u.glossary[i];
    Shell.of(context).showSheet(_GlossSheet(item: g));
  }

  void _resetEx(Unit u) {
    NotesSession.exs.remove(u.id);
    setState(() {});
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final k = _secKeys['questions'];
      if (k != null) scrollToKey(k);
    });
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), u = unit;
    final ib = _s.repo.byId(widget.bookId);
    final top = hp.TopBar(
      title: u == null ? '' : 'Unit ${u.number}',
      sub: ib?.title,
      onBack: () => Shell.of(context).pop(),
      tab: false,
      actions: [
        // High: present this unit's notes on a TV, one card per step
        if (u != null) hc.CBtn('play', label: 'Present', onTap: () => hp.HighNav.of(context).push(PresenterPage(slides: [NotesSlide(u, widget.bookId, _s.repo.svgPath)]))),
      ],
    );
    if (!_ready || u == null) return PageShell(top: top, body: const SizedBox.shrink());
    final items = _contentBuilders(context, k, u);
    return PageShell(
      top: top,
      body: ScrollConfiguration(
        behavior: const NoGlow(),
        child: NotificationListener<Notification>(
          onNotification: (n) {
            if (n is UserScrollNotification) _holdKey = null;
            if (n is ScrollMetricsNotification) {
              final hk = _holdKey;
              if (hk != null && DateTime.now().isBefore(_holdUntil)) {
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  if (mounted && _holdKey == hk) scrollToKey(hk, smooth: false);
                });
              }
              _trackSoon();
            }
            if (n is ScrollEndNotification) _track();
            return false;
          },
          child: CustomScrollView(
            controller: _scroll,
            cacheExtent: Perf.cacheExtent(context),
            slivers: [
              SliverPersistentHeader(pinned: true, delegate: _JumpDelegate(this, u, k)),
              SliverPadding(
                padding: EdgeInsets.fromLTRB(20, 6, 20, 30 + MediaQuery.paddingOf(context).bottom),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (context, i) => items[i](),
                    childCount: items.length,
                    addAutomaticKeepAlives: false,
                    addRepaintBoundaries: true,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  List<(String, String)> jumps(Kit k, Unit u) => [
    if (_map != null) ('map', 'Map'),
    ('notes', k.t('notes')),
    ('memory', k.t('memory')),
    if (u.games.isNotEmpty) ('games', k.t('games')),
    ('questions', 'Quiz'),
    if (_matricIds.isNotEmpty) ('matric', 'Matric'),
  ];

  // ---- High: concept map + matric questions for this unit
  UnitMap? get _map => _s.repo.unitExtras(widget.bookId, widget.unitId)?.maps[widget.unitId];
  List<String> get _matricIds => hr.Routes.unitQuestionIds(context, widget.unitId);

  void _jumpToCard(String cardId) {
    final key = _s.repo.unitExtras(widget.bookId, widget.unitId)?.cardKey[cardId];
    final gk = key == null ? null : _cardKeys[key];
    if (gk != null) {
      _holdKey = null;
      scrollToKey(gk);
    }
  }

  void jump(String sec) {
    _holdKey = null;
    final key = _secKeys[sec];
    if (key != null) scrollToKey(key);
  }

  String? get jumpOn => _jumpOn;

  List<Widget Function()> _contentBuilders(BuildContext context, Kit k, Unit u) {
    final p = k.p, s = k.s, b = _book!.info, sub = notesSubject(b.subject), tone = p.tone(sub.tone);
    final ctx = UnitCtx(u, widget.bookId, s.repo.svgPath);
    final rc = richColors(p);
    // progress line + bar listen to [_progTick], so marking cards read while scrolling only rebuilds these two
    Widget progress(Widget Function(int pct) b) => ValueListenableBuilder<int>(valueListenable: _progTick, builder: (_, _, _) => b(s.unitPct(u)));

    Widget secPill(String key, String icon, String title, Tone t) => Padding(
      padding: const EdgeInsets.only(bottom: 16), // margin-top 34 sits outside the section (it collapses through .usec)
      child: Align(
        alignment: Alignment.centerLeft,
        child: DecoratedBox(
          decoration: k.c.secPill(t),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(14, 10, 20, 10),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              spacing: 10,
              children: [
                k.icon(icon, size: 30, color: p.ink),
                Flexible(child: Tx(title, style: ts(23, FontWeight.w900, p.ink, height: 1.2))),
              ],
            ),
          ),
        ),
      ),
    );
    // builders whose item carries a GlobalKey (for [_keyIndex])
    final keyed = <Widget Function(), GlobalKey>{};
    Widget Function() tag(GlobalKey k, Widget Function() f) {
      keyed[f] = k;
      return f;
    }
    List<Widget Function()> sectionBuilders(String key, String icon, String title, Tone t, List<Widget Function()> kids) {
      final sk = _secKeys.putIfAbsent(key, GlobalKey.new);
      return [
        tag(
          sk,
          () => Padding(
            padding: const EdgeInsets.only(top: 34),
            child: Column(
              key: sk,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [secPill(key, icon, title, t)],
            ),
          ),
        ),
        ...kids,
      ];
    }

    // notes: lesson heads + cards — each card is its own lazy list item
    final noteBuilders = <Widget Function()>[];
    for (final (li, l) in u.lessons.indexed) {
      final lesson = l;
      final lessonIndex = li;
      noteBuilders.add(() => Padding(
        padding: EdgeInsets.only(top: lessonIndex == 0 ? 0 : 6, bottom: 12),
        child: Row(
          spacing: 14,
          children: [
            DecoratedBox(
              decoration: k.c.num(tone),
              child: SizedBox(
                width: 52,
                height: 52,
                child: Center(child: Tx(lesson.number, style: ts(20, FontWeight.w900, tone.deep, normal: true))),
              ),
            ),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Tx(lesson.title, style: ts(22, FontWeight.w900, p.ink, height: 1.2)),
                  if (lesson.pages.length >= 2) Tx(k.t('textbookPage', {'n': '${lesson.pages[0]}–${lesson.pages[1]}'}), style: ts(16, FontWeight.w700, p.ink2)),
                ],
              ),
            ),
          ],
        ),
      ));
      for (final (i, c) in lesson.cards.indexed) {
        final card = c;
        final key = '${lesson.id}~$i';
        final ck = _cardKeys.putIfAbsent(key, GlobalKey.new);
        noteBuilders.add(tag(ck, () => Padding(
          key: ck,
          padding: const EdgeInsets.only(bottom: 20),
          child: NoteCardView(ctx: ctx, card: card, ckey: key, onGloss: (gi) => _gloss(u, gi)),
        )));
      }
    }

    // memory / games / quiz — deferred until list builder asks for them
    final tricks = [for (final l in u.lessons) ...l.cards.whereType<MnemonicCard>()];
    final words = [...u.glossary]..sort((a, b) => a.term.compareTo(b.term));
    final memoryBuilders = <Widget Function()>[
      if (u.tips.isNotEmpty)
        () => NCard(
          tone: p.butter,
          padding: const EdgeInsets.all(20),
          margin: const EdgeInsets.only(bottom: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              KindLabel('tip', k.t('tip')),
              for (final tip in u.tips)
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: RichPara(tip.text, style: ts(18, FontWeight.w500, p.ink), colors: rc),
                ),
            ],
          ),
        ),
      for (final (i, c) in tricks.indexed)
        () {
          final card = c;
          final idx = i;
          return Padding(
            padding: EdgeInsets.only(top: idx == 0 ? 0 : 4, bottom: idx == tricks.length - 1 ? 16 : 0),
            child: NoteCardView(ctx: ctx, card: card, ckey: 'mem$idx', compact: true),
          );
        },
      if (words.isNotEmpty)
        () => NCard(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              KindLabel('book', k.t('keyWords')),
              for (final (i, g) in words.indexed)
                Padding(
                  padding: EdgeInsets.only(bottom: i == words.length - 1 ? 0 : 12),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Tx(g.term, style: ts(21, FontWeight.w900, p.ink)),
                      RichPara('${g.meaning} · ${k.t('textbookPage', {'n': g.page})}', style: ts(18, FontWeight.w700, p.ink2), colors: rc),
                    ],
                  ),
                ),
            ],
          ),
        ),
    ];

    final gameBuilders = <Widget Function()>[
      for (final g in u.games)
        tag(_gameKeys.putIfAbsent(g.id, GlobalKey.new), () {
          final game = g;
          return Padding(
            key: _gameKeys[game.id],
            padding: const EdgeInsets.only(bottom: 22),
            child: GameCard(ctx: ctx, game: game, onEnd: () => setState(() {})),
          );
        }),
    ];

    final quizBuilders = <Widget Function()>[
      // keyed like cards so the jump bar's [_seek] can find its place inside a long quiz (a long unkeyed run of
      // questions gave it nothing to measure, and it kept stepping the wrong way past the "Unit quiz" heading)
      for (final (i, q) in u.exercise.questions.indexed)
        tag(_quizKeys.putIfAbsent(q.id, GlobalKey.new), () {
          final qi = i;
          final qq = q;
          return Padding(
            key: _quizKeys[qq.id],
            padding: const EdgeInsets.only(bottom: 22),
            child: QCard(
              key: ValueKey('${u.id}/${qq.id}/${NotesSession.ex(u.id).hashCode}'),
              u: u,
              bid: widget.bookId,
              q: qq,
              index: qi,
              onChecked: () => setState(() {}),
            ),
          );
        }),
      () => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: QSummary(u: u, onReset: () => _resetEx(u)),
      ),
    ];

    final out = <Widget Function()>[
      () => Tx(u.title, style: ts(30, FontWeight.w900, p.ink, height: 1.15, spacing: -.3)),
      () => progress(
        (pct) => Padding(
          padding: const EdgeInsets.only(top: 4, bottom: 10),
          child: Tx('${k.t(sub.key)} ${b.grade} · ${k.t('progress', {'n': pct})}', style: ts(19, FontWeight.w700, p.ink2)),
        ),
      ),
      () => progress((pct) => PBar(pct / 100)),
      () => Padding(padding: const EdgeInsets.only(top: 16), child: hr.UnitLinkBar(unitId: u.id)),
      if (u.intro.isNotEmpty)
        () => NCard(
          padding: const EdgeInsets.all(20),
          margin: const EdgeInsets.only(top: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: RichPara(u.intro, style: ts(19, FontWeight.w700, p.ink), colors: rc),
              ),
              PgRef(u.introPage),
            ],
          ),
        ),
      if (_map != null) ...sectionBuilders('map', 'star', 'Concept map', p.mint, [
        () => ConceptMapView(map: _map!, tone: sub.tone, onCard: _jumpToCard),
      ]),
      ...sectionBuilders('notes', 'book', k.t('notes'), p.butter, noteBuilders),
      ...sectionBuilders('memory', 'tip', k.t('tipsTricks'), p.lilac, memoryBuilders),
      if (u.games.isNotEmpty) ...sectionBuilders('games', 'star', k.t('games'), p.blue, gameBuilders),
      ...sectionBuilders('questions', 'check', 'Unit quiz', p.sage, quizBuilders),
      if (_matricIds.isNotEmpty) ...sectionBuilders('matric', 'star', 'Matric questions', p.peach, [
        () => hr.UnitMatricCard(unitId: u.id, title: u.title, ids: _matricIds),
      ]),
      if (u.links.isNotEmpty) ...[
        () => Padding(
          padding: const EdgeInsets.only(top: 24, bottom: 12),
          child: Row(
            spacing: 10,
            children: [
              k.icon('lang', size: 30, color: p.ink),
              Expanded(child: Tx(k.t('learnMore'), style: ts(22, FontWeight.w900, p.ink))),
            ],
          ),
        ),
        () => NCard(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              for (final l in u.links)
                Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Tx('${l['title'] ?? ''}', style: ts(18, FontWeight.w500, p.blue.deep).copyWith(decoration: TextDecoration.underline, decorationColor: p.blue.deep)),
                      Tx('${l['license'] ?? ''}${l['note'] != null ? ' · ${l['note']}' : ''}', style: ts(15, FontWeight.w500, p.ink2)),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ],
    ];
    _keyIndex
      ..clear()
      ..addAll({
        for (final (i, f) in out.indexed) ?keyed[f]: i,
      });
    _itemCount = out.length;
    return out;
  }
}

/// `.jumpwrap` (sticky at top:-6px) with the `.jump` track and its keys
class _JumpDelegate extends SliverPersistentHeaderDelegate {
  _JumpDelegate(this.page, this.u, this.k);
  final UnitPageState page;
  final Unit u;
  final Kit k;
  @override
  double get maxExtent => 82;
  @override
  double get minExtent => 82; // sticky top:-6px inside the screen's 6px top padding: always fully visible

  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    final p = k.p, js = page.jumps(k, u), on = page.jumpOn;
    final st = ts(15.5, FontWeight.w900, p.ink2, normal: true);
    final bar = ClipRect(
      clipper: const _OpenBottom(),
      child: SizedBox(
        height: 82,
        child: DecoratedBox(
          decoration: ClayDecoration(
            fills: [SolidFill(p.jumpBg)],
            shadows: [Shadow3(0, 12, 12, -14, p.dark ? const Color.fromRGBO(0, 0, 0, .7) : p.sh(.45))],
          ),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20, 8, 20, 12),
            child: DecoratedBox(
              decoration: k.c.track(radius: 30),
              child: Padding(
                padding: const EdgeInsets.fromLTRB(5, 5, 5, 9),
                child: LayoutBuilder(
                  builder: (context, box) {
                    // flex: 1 1 auto – each key is as wide as its label, the spare room shared out equally
                    final ws = [
                      for (final j in js) (TextPainter(text: TextSpan(text: j.$2, style: st), textDirection: TextDirection.ltr, maxLines: 1)..layout()).width * (js.length > 5 ? .8 : 1) + 16,
                    ];
                    final avail = box.maxWidth - 6 * (js.length - 1), sum = ws.fold<double>(0, (a, b) => a + b);
                    final widths = sum <= avail ? [for (final w in ws) w + (avail - sum) / js.length] : [for (final w in ws) w - (sum - avail) * w / sum];
                    return Row(
                      spacing: 6,
                      children: [
                        for (final (i, j) in js.indexed)
                          SizedBox(
                            width: widths[i],
                            child: Press(
                              onTap: () => page.jump(j.$1),
                              selected: on == j.$1,
                              deco: k.c.key(radius: 24),
                              pressedDeco: k.c.keyOn(radius: 24),
                              dy: 4,
                              constraints: const BoxConstraints(minHeight: 48),
                              padding: const EdgeInsets.symmetric(horizontal: 8),
                              child: Center(
                                // High: 6 keys on a phone -> scale the label down instead of cutting it
                                child: FittedBox(
                                  fit: BoxFit.scaleDown,
                                  child: Tx(j.$2, maxLines: 1, style: st.copyWith(color: on == j.$1 ? p.sage.deep : p.ink2)),
                                ),
                              ),
                            ),
                          ),
                      ],
                    );
                  },
                ),
              ),
            ),
          ),
        ),
      ),
    );
    // own layer: the pinned bar (clay track + 6 keys) is not re-recorded for every scrolled frame
    return RepaintBoundary(child: bar);
  }

  @override
  bool shouldRebuild(_JumpDelegate old) => true;
}

/// clip the sides and top only: the header's shadow falls onto the content below
class _OpenBottom extends CustomClipper<Rect> {
  const _OpenBottom();
  @override
  Rect getClip(Size size) => Rect.fromLTRB(0, 0, size.width, size.height + 24);
  @override
  bool shouldReclip(_OpenBottom oldClipper) => false;
}

/// glossary word sheet (`glossSheet`)
class _GlossSheet extends StatelessWidget {
  const _GlossSheet({required this.item});
  final GlossaryItem item;
  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    return DecoratedBox(
      decoration: k.c.sheet(),
      child: Padding(
        padding: EdgeInsets.fromLTRB(22, 12, 22, 26 + MediaQuery.paddingOf(context).bottom),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Center(
              child: Container(
                width: 52,
                height: 6,
                margin: const EdgeInsets.only(bottom: 10),
                decoration: BoxDecoration(color: withA(p.ink2, .3), borderRadius: BorderRadius.circular(9)),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 4, bottom: 14),
              child: Tx(item.term, textAlign: TextAlign.center, style: ts(28, FontWeight.w900, p.ink)),
            ),
            RichPara(item.meaning, style: ts(19, FontWeight.w700, p.ink), colors: richColors(p), textAlign: TextAlign.center),
            Center(child: PgRef(item.page)),
            const SizedBox(height: 18),
            ClayButton(label: k.t('close'), onTap: () => Shell.of(context).closeSheet()),
          ],
        ),
      ),
    );
  }
}
