// Stage 3: vertical reels feed for .4reel resources. PageView, only prev/current/next players alive (others disposed),
// the next reel is prepared paused so its first chunk is already decrypted and buffered when you swipe.
// Tap = pause/play, double-tap right/left = ±10 s, thin draggable seek bar, title overlay, FLAG_SECURE, resume.
import 'dart:async';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:four_format/four_format.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../high/theme/tokens.dart';
import '../high/widgets/page.dart';
import 'library.dart';
import 'native_video.dart';

const _white = Color(0xFFFFFFFF);

class ReelsPage extends StatefulWidget with NoNav {
  const ReelsPage({super.key, required this.reels, this.initial = 0});
  final List<ResEntry> reels;
  final int initial;
  @override
  State<ReelsPage> createState() => _ReelsPageState();
}

class _ReelsPageState extends State<ReelsPage> {
  late final PageController _pc = PageController(initialPage: widget.initial);
  late int _cur = widget.initial;

  @override
  void initState() {
    super.initState();
    ResourceLibrary.setSecure(true);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  }

  @override
  void dispose() {
    ResourceLibrary.setSecure(false);
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    _pc.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ColoredBox(
      color: const Color(0xFF000000),
      child: Stack(
        fit: StackFit.expand,
        children: [
          PageView.builder(
            controller: _pc,
            scrollDirection: Axis.vertical,
            // builds the neighbour pages off-screen so prev/next players exist (and next is buffered) before the swipe
            allowImplicitScrolling: true,
            itemCount: widget.reels.length,
            onPageChanged: (i) => setState(() => _cur = i),
            itemBuilder: (_, i) => ReelView(
              key: ValueKey(widget.reels[i].id),
              entry: widget.reels[i],
              active: i == _cur,
              alive: (i - _cur).abs() <= 1,
            ),
          ),
          Positioned(
            top: MediaQuery.paddingOf(context).top + 8,
            left: 8,
            child: GestureDetector(
              onTap: () => HighNav.of(context).back(),
              child: const SizedBox(width: 44, height: 44, child: CustomPaint(painter: _BackPainter())),
            ),
          ),
          Positioned(
            top: MediaQuery.paddingOf(context).top + 20,
            right: 16,
            child: Text('${_cur + 1} / ${widget.reels.length}', style: ts(13, w800, const Color(0xCCFFFFFF))),
          ),
        ],
      ),
    );
  }
}

/// One reel. Holds a native player only while [alive]; plays only while [active].
class ReelView extends StatefulWidget {
  const ReelView({super.key, required this.entry, required this.active, required this.alive});
  final ResEntry entry;
  final bool active, alive;
  @override
  State<ReelView> createState() => _ReelViewState();
}

class _ReelViewState extends State<ReelView> {
  NativeVideo? _v;
  Future<void>? _opening;
  VideoState? _st;
  Timer? _poll, _flashT;
  bool _paused = false, _dragging = false, _shown = false;
  double _dragFrac = 0;
  String? _flash;
  Object? _err;
  int _lastSaved = 0;

  String get _posKey => 'four_res_pos_${widget.entry.id}';

  @override
  void initState() {
    super.initState();
    if (widget.alive) _open();
  }

  @override
  void didUpdateWidget(ReelView old) {
    super.didUpdateWidget(old);
    if (widget.alive && _v == null && _opening == null) _open();
    if (!widget.alive && (_v != null || _opening != null)) _close();
    if (widget.active != old.active) _applyActive();
  }

  Future<void> _open() => _opening = () async {
    try {
      final lib = ResourceLibrary.instance;
      final src = await FileSource.open(widget.entry.path);
      final r = await FourReader.open(src, lib.gate.masterKey);
      final key = await r.contentKey();
      await r.close();
      final v = await NativeVideo.open(widget.entry.path, key); // prepares paused → first chunk decrypted + buffered
      await v.loop(true);
      final saved = (await SharedPreferences.getInstance()).getInt(_posKey) ?? 0;
      if (saved > 3000) await v.seek(saved);
      if (!mounted || !widget.alive) {
        await v.dispose();
        return;
      }
      _v = v;
      await _applyActive();
    } catch (e) {
      if (mounted) setState(() => _err = e);
    } finally {
      _opening = null;
    }
  }();

  Future<void> _close() async {
    await _opening;
    _poll?.cancel();
    final v = _v;
    _v = null;
    _shown = false;
    if (v != null) {
      final s = _st;
      if (s != null) await _save(s.pos, s.dur);
      await v.dispose();
    }
    if (mounted) setState(() {});
  }

  Future<void> _applyActive() async {
    final v = _v;
    if (v == null) return;
    if (widget.active && !_paused) {
      await v.play();
      _poll?.cancel();
      _poll = Timer.periodic(const Duration(milliseconds: 250), (_) => _tick());
    } else {
      await v.pause();
      _poll?.cancel();
      _tick();
    }
    if (mounted) setState(() {});
  }

  Future<void> _tick() async {
    final v = _v;
    if (v == null) return;
    final s = await v.state();
    if (!mounted || s == null) return;
    setState(() {
      _st = s;
      if (s.w > 0 && (s.pos > 0 || s.playing)) _shown = true;
      if (s.error != null) _err = s.error;
    });
    if ((s.pos - _lastSaved).abs() > 3000) _save(s.pos, s.dur);
  }

  Future<void> _save(int pos, int dur) async {
    _lastSaved = pos;
    final prefs = await SharedPreferences.getInstance();
    if (dur > 0 && pos > dur - 3000) {
      await prefs.remove(_posKey);
    } else {
      await prefs.setInt(_posKey, pos);
    }
  }

  @override
  void dispose() {
    _poll?.cancel();
    _flashT?.cancel();
    final v = _v, s = _st;
    if (s != null) _save(s.pos, s.dur);
    v?.dispose();
    super.dispose();
  }

  void _togglePause() {
    _paused = !_paused;
    _applyActive();
  }

  void _skip(int ms) {
    final v = _v, s = _st;
    if (v == null || s == null) return;
    v.seek((s.pos + ms).clamp(0, s.dur > 0 ? s.dur - 200 : s.pos + ms));
    _flashT?.cancel();
    setState(() => _flash = ms > 0 ? '+10 s' : '−10 s');
    _flashT = Timer(const Duration(milliseconds: 650), () {
      if (mounted) setState(() => _flash = null);
    });
    _tick();
  }

  @override
  Widget build(BuildContext context) {
    final m = widget.entry.meta, s = _st, v = _v, t = widget.entry.thumb;
    final dur = s?.dur ?? 0;
    final frac = _dragging ? _dragFrac : (dur > 0 ? (s!.pos / dur).clamp(0.0, 1.0) : 0.0);
    final aspect = (s != null && s.w > 0 && s.h > 0) ? s.w / s.h : 9 / 16;
    final bottom = MediaQuery.paddingOf(context).bottom;
    return LayoutBuilder(
      builder: (context, box) => Stack(
        fit: StackFit.expand,
        children: [
          // cover = thumbnail until the first frame is up (no black flash while swiping)
          if (t != null && !_shown) Image.memory(t, fit: BoxFit.cover, gaplessPlayback: true, cacheWidth: 360),
          if (v != null) Center(child: AspectRatio(aspectRatio: aspect, child: Texture(textureId: v.id, filterQuality: FilterQuality.low))),
          GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: _togglePause,
            onDoubleTapDown: (d) => _skip(d.localPosition.dx < box.maxWidth / 2 ? -10000 : 10000),
            onDoubleTap: () {},
          ),
          if (_err != null)
            Center(child: Text(_err is FourKeyException ? 'Unlock 4 to watch this reel.' : 'Could not play this reel.', style: ts(14, w800, _white))),
          if (_paused && v != null) const Center(child: SizedBox(width: 72, height: 72, child: CustomPaint(painter: _BigPlay()))),
          if (_flash != null)
            Center(
              child: DecoratedBox(
                decoration: BoxDecoration(color: const Color(0x88000000), borderRadius: BorderRadius.circular(30)),
                child: Padding(padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 10), child: Text(_flash!, style: ts(16, w900, _white))),
              ),
            ),
          Positioned(
            left: 16,
            right: 16,
            bottom: bottom + 26,
            child: IgnorePointer(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                spacing: 4,
                children: [
                  Text(m.title, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(16, w900, _white).copyWith(shadows: const [Shadow(blurRadius: 6, color: Color(0xAA000000))])),
                  Text('${m.subject} · Grade ${m.grade}${m.unit.isNotEmpty ? ' · Unit ${m.unit}' : ''}', style: ts(13, w700, const Color(0xDDFFFFFF)).copyWith(shadows: const [Shadow(blurRadius: 6, color: Color(0xAA000000))])),
                ],
              ),
            ),
          ),
          // thin seek bar: 3 px, grows while dragging; tall invisible hit area
          Positioned(
            left: 0,
            right: 0,
            bottom: bottom,
            height: 22,
            child: GestureDetector(
              behavior: HitTestBehavior.opaque,
              onHorizontalDragStart: (d) => setState(() {
                _dragging = true;
                _dragFrac = (d.localPosition.dx / box.maxWidth).clamp(0.0, 1.0);
              }),
              onHorizontalDragUpdate: (d) => setState(() => _dragFrac = (d.localPosition.dx / box.maxWidth).clamp(0.0, 1.0)),
              onHorizontalDragEnd: (_) {
                _v?.seek((_dragFrac * dur).round());
                setState(() => _dragging = false);
              },
              child: CustomPaint(painter: _ThinBar(frac, _dragging)),
            ),
          ),
          if (_dragging)
            Positioned(
              bottom: bottom + 60,
              left: 0,
              right: 0,
              child: Center(child: Text('${fmtMs((_dragFrac * dur).round())} / ${fmtMs(dur)}', style: ts(18, w900, _white))),
            ),
        ],
      ),
    );
  }
}

class _ThinBar extends CustomPainter {
  _ThinBar(this.f, this.big);
  final double f;
  final bool big;
  @override
  void paint(Canvas c, Size s) {
    final h = big ? 6.0 : 3.0, y = s.height - h;
    c.drawRect(Rect.fromLTWH(0, y, s.width, h), Paint()..color = const Color(0x44FFFFFF));
    c.drawRect(Rect.fromLTWH(0, y, s.width * f, h), Paint()..color = const Color(0xEEFFFFFF));
    if (big) c.drawCircle(Offset(s.width * f, y + h / 2), 8, Paint()..color = _white);
  }

  @override
  bool shouldRepaint(_ThinBar o) => o.f != f || o.big != big;
}

class _BigPlay extends CustomPainter {
  const _BigPlay();
  @override
  void paint(Canvas c, Size s) {
    final cx = s.width / 2, cy = s.height / 2;
    c.drawPath(Path()..moveTo(cx - 14, cy - 22)..lineTo(cx + 22, cy)..lineTo(cx - 14, cy + 22)..close(), Paint()..color = const Color(0xBBFFFFFF));
  }

  @override
  bool shouldRepaint(_BigPlay o) => false;
}

class _BackPainter extends CustomPainter {
  const _BackPainter();
  @override
  void paint(Canvas c, Size s) {
    final p = Paint()
      ..color = _white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.6
      ..strokeCap = StrokeCap.round;
    c.drawPath(Path()..moveTo(s.width * .58, s.height * .3)..lineTo(s.width * .38, s.height * .5)..lineTo(s.width * .58, s.height * .7), p);
  }

  @override
  bool shouldRepaint(_BackPainter o) => false;
}
