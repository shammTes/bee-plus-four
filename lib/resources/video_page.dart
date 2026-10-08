// 16:9 player for encrypted .4vid resources: seek bar, 0.5–2× speed, fullscreen landscape, double-tap ±10 s,
// tap to show/hide controls, FLAG_SECURE, resume position. Widgets only (no Material, no WebView).
import 'dart:async';

import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:four_format/four_format.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../high/theme/tokens.dart';
import '../high/widgets/kit.dart';
import '../high/widgets/page.dart';
import 'library.dart';
import 'native_video.dart';

const kSpeeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0];

class VideoResourcePage extends StatefulWidget with NoNav {
  const VideoResourcePage({super.key, required this.entry});
  final ResEntry entry;
  @override
  State<VideoResourcePage> createState() => _VideoResourcePageState();
}

class _VideoResourcePageState extends State<VideoResourcePage> {
  NativeVideo? _v;
  VideoState? _st;
  Object? _err;
  Timer? _poll, _hide;
  bool _controls = true, _full = false, _dragging = false;
  double _dragFrac = 0;
  int _speedI = 2, _lastSaved = 0;
  String? _flash; // "+10 s" / "−10 s" bubble
  Timer? _flashT;

  String get _posKey => 'four_res_pos_${widget.entry.id}';

  @override
  void initState() {
    super.initState();
    ResourceLibrary.setSecure(true);
    _open();
  }

  Future<void> _open() async {
    try {
      final lib = ResourceLibrary.instance;
      final src = await FileSource.open(widget.entry.path);
      final r = await FourReader.open(src, lib.gate.masterKey);
      final key = await r.contentKey();
      await r.close();
      final v = await NativeVideo.open(widget.entry.path, key);
      if (!mounted) {
        await v.dispose();
        return;
      }
      _v = v;
      final saved = (await SharedPreferences.getInstance()).getInt(_posKey) ?? 0;
      final dur = widget.entry.meta.durationMs ?? 0;
      if (saved > 5000 && (dur == 0 || saved < dur - 5000)) await v.seek(saved);
      await v.play();
      _poll = Timer.periodic(const Duration(milliseconds: 250), (_) => _tick());
      _autoHide();
      setState(() {});
    } catch (e) {
      if (mounted) setState(() => _err = e);
    }
  }

  Future<void> _tick() async {
    final v = _v;
    if (v == null || !mounted) return;
    final s = await v.state();
    if (!mounted || s == null) return;
    setState(() => _st = s);
    if (s.error != null) _err ??= s.error;
    if ((s.pos - _lastSaved).abs() > 3000) _save(s.pos, s.dur);
    if (s.ended && !_controls) setState(() => _controls = true);
  }

  Future<void> _save(int pos, int dur) async {
    _lastSaved = pos;
    final prefs = await SharedPreferences.getInstance();
    // finished → start from the beginning next time
    if (dur > 0 && pos > dur - 5000) {
      await prefs.remove(_posKey);
    } else {
      await prefs.setInt(_posKey, pos);
    }
  }

  @override
  void dispose() {
    _poll?.cancel();
    _hide?.cancel();
    _flashT?.cancel();
    final s = _st;
    if (s != null) _save(s.pos, s.dur);
    _v?.dispose();
    ResourceLibrary.setSecure(false);
    if (_full) _setFull(false, rebuild: false);
    super.dispose();
  }

  void _autoHide() {
    _hide?.cancel();
    _hide = Timer(const Duration(seconds: 3), () {
      if (mounted && (_st?.playing ?? false) && !_dragging) setState(() => _controls = false);
    });
  }

  void _toggleControls() {
    setState(() => _controls = !_controls);
    if (_controls) _autoHide();
  }

  Future<void> _playPause() async {
    final v = _v, s = _st;
    if (v == null) return;
    if (s?.playing ?? false) {
      await v.pause();
    } else {
      if (s?.ended ?? false) await v.seek(0);
      await v.play();
    }
    _autoHide();
    _tick();
  }

  void _skip(int ms) {
    final v = _v, s = _st;
    if (v == null || s == null) return;
    final t = (s.pos + ms).clamp(0, s.dur > 0 ? s.dur : s.pos + ms);
    v.seek(t);
    _flashT?.cancel();
    setState(() => _flash = ms > 0 ? '+10 s' : '−10 s');
    _flashT = Timer(const Duration(milliseconds: 700), () {
      if (mounted) setState(() => _flash = null);
    });
    _tick();
  }

  void _cycleSpeed() {
    _speedI = (_speedI + 1) % kSpeeds.length;
    _v?.speed(kSpeeds[_speedI]);
    setState(() {});
    _autoHide();
  }

  void _setFull(bool on, {bool rebuild = true}) {
    if (on) {
      SystemChrome.setPreferredOrientations(const [DeviceOrientation.landscapeLeft, DeviceOrientation.landscapeRight]);
      SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    } else {
      SystemChrome.setPreferredOrientations(const [DeviceOrientation.portraitUp]);
      SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    }
    _full = on;
    if (rebuild && mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, m = widget.entry.meta;
    final player = _player();
    if (_full) {
      return PopScope(
        canPop: false,
        onPopInvokedWithResult: (did, _) {
          if (!did) _setFull(false);
        },
        child: ColoredBox(color: const Color(0xFF000000), child: player),
      );
    }
    return PageShell(
      top: TopBar(title: m.title, sub: m.creditLine.isEmpty ? 'Video' : 'Video · ${m.creditLine}', onBack: () => HighNav.of(context).back(), tab: false),
      body: ListView(
        padding: EdgeInsets.zero,
        children: [
          AspectRatio(aspectRatio: 16 / 9, child: ColoredBox(color: const Color(0xFF000000), child: player)),
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 16, 20, 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 4,
              children: [
                Text(m.title, style: ts(17, w900, p.ink)),
                Text('${m.subject} · Grade ${m.grade}${m.unit.isNotEmpty ? ' · Unit ${m.unit}' : ''}${m.durationMs != null ? ' · ${fmtMs(m.durationMs!)}' : ''}', style: ts(13, w700, p.ink2)),
                const SizedBox(height: 8),
                Text('Double-tap left or right to skip 10 s. Tap the video to show controls.', style: ts(12.5, w700, p.ink3)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _player() {
    final s = _st, v = _v;
    const white = Color(0xFFFFFFFF);
    if (_err != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Text(_err is FourKeyException ? 'This phone cannot open this video. Unlock 4 first.' : 'Could not play this video. Copy it again and tap Refresh.', textAlign: TextAlign.center, style: ts(14, w800, white)),
        ),
      );
    }
    final aspect = (s != null && s.w > 0 && s.h > 0) ? s.w / s.h : 16 / 9;
    final dur = s?.dur ?? 0;
    final frac = _dragging ? _dragFrac : (dur > 0 ? (s!.pos / dur).clamp(0.0, 1.0) : 0.0);
    return LayoutBuilder(
      builder: (context, box) => Stack(
        fit: StackFit.expand,
        children: [
          if (v != null) Center(child: AspectRatio(aspectRatio: aspect, child: Texture(textureId: v.id, filterQuality: FilterQuality.low))),
          // gestures: tap = controls, double-tap left/right half = ∓10 s
          GestureDetector(
            behavior: HitTestBehavior.opaque,
            onTap: _toggleControls,
            onDoubleTapDown: (d) => _skip(d.localPosition.dx < box.maxWidth / 2 ? -10000 : 10000),
            onDoubleTap: () {},
          ),
          if (v == null || (s?.buffering ?? true)) const Center(child: _Spinner()),
          if (_flash != null)
            Center(
              child: DecoratedBox(
                decoration: BoxDecoration(color: const Color(0x99000000), borderRadius: BorderRadius.circular(30)),
                child: Padding(padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 10), child: Text(_flash!, style: ts(16, w900, white))),
              ),
            ),
          if (_controls && v != null) ...[
            Center(
              child: GestureDetector(
                onTap: _playPause,
                child: Container(
                  width: 64,
                  height: 64,
                  decoration: const BoxDecoration(color: Color(0x88000000), shape: BoxShape.circle),
                  child: CustomPaint(painter: _PlayPainter(playing: s?.playing ?? false)),
                ),
              ),
            ),
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: DecoratedBox(
                decoration: const BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Color(0x00000000), Color(0xAA000000)])),
                child: Padding(
                  padding: EdgeInsets.fromLTRB(12, 18, 12, _full ? 14 : 6),
                  child: Row(
                    spacing: 10,
                    children: [
                      Text(fmtMs(_dragging ? (_dragFrac * dur).round() : s?.pos ?? 0), style: ts(12, w800, white)),
                      Expanded(child: _SeekBar(frac: frac, buffered: dur > 0 ? ((s?.buffered ?? 0) / dur).clamp(0.0, 1.0) : 0, onStart: (f) => setState(() {
                        _dragging = true;
                        _dragFrac = f;
                        _hide?.cancel();
                      }), onUpdate: (f) => setState(() => _dragFrac = f), onEnd: () {
                        v.seek((_dragFrac * dur).round());
                        setState(() => _dragging = false);
                        _autoHide();
                      })),
                      Text(fmtMs(dur), style: ts(12, w800, white)),
                      GestureDetector(onTap: _cycleSpeed, child: Text('${kSpeeds[_speedI]}×'.replaceAll('.0×', '×'), style: ts(13, w900, white))),
                      GestureDetector(
                        onTap: () => _setFull(!_full),
                        child: SizedBox(width: 26, height: 26, child: CustomPaint(painter: _FullPainter(_full))),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}

class _SeekBar extends StatelessWidget {
  const _SeekBar({required this.frac, required this.buffered, required this.onStart, required this.onUpdate, required this.onEnd});
  final double frac, buffered;
  final ValueChanged<double> onStart, onUpdate;
  final VoidCallback onEnd;
  @override
  Widget build(BuildContext context) => LayoutBuilder(
    builder: (context, c) {
      double f(Offset o) => (o.dx / c.maxWidth).clamp(0.0, 1.0);
      return GestureDetector(
        behavior: HitTestBehavior.opaque,
        onHorizontalDragStart: (d) => onStart(f(d.localPosition)),
        onHorizontalDragUpdate: (d) => onUpdate(f(d.localPosition)),
        onHorizontalDragEnd: (_) => onEnd(),
        onTapDown: (d) => onStart(f(d.localPosition)),
        onTapUp: (_) => onEnd(),
        child: SizedBox(height: 28, child: CustomPaint(painter: _BarPainter(frac, buffered))),
      );
    },
  );
}

class _BarPainter extends CustomPainter {
  _BarPainter(this.f, this.b);
  final double f, b;
  @override
  void paint(Canvas c, Size s) {
    final y = s.height / 2;
    final r = RRect.fromLTRBR(0, y - 2, s.width, y + 2, const Radius.circular(2));
    c.drawRRect(r, Paint()..color = const Color(0x55FFFFFF));
    c.drawRRect(RRect.fromLTRBR(0, y - 2, s.width * b, y + 2, const Radius.circular(2)), Paint()..color = const Color(0x88FFFFFF));
    c.drawRRect(RRect.fromLTRBR(0, y - 2, s.width * f, y + 2, const Radius.circular(2)), Paint()..color = const Color(0xFFE88A6E));
    c.drawCircle(Offset(s.width * f, y), 7, Paint()..color = const Color(0xFFFFFFFF));
  }

  @override
  bool shouldRepaint(_BarPainter o) => o.f != f || o.b != b;
}

class _PlayPainter extends CustomPainter {
  _PlayPainter({required this.playing});
  final bool playing;
  @override
  void paint(Canvas c, Size s) {
    final p = Paint()..color = const Color(0xFFFFFFFF);
    final cx = s.width / 2, cy = s.height / 2;
    if (playing) {
      c.drawRect(Rect.fromLTWH(cx - 9, cy - 11, 6, 22), p);
      c.drawRect(Rect.fromLTWH(cx + 3, cy - 11, 6, 22), p);
    } else {
      c.drawPath(Path()..moveTo(cx - 7, cy - 12)..lineTo(cx + 12, cy)..lineTo(cx - 7, cy + 12)..close(), p);
    }
  }

  @override
  bool shouldRepaint(_PlayPainter o) => o.playing != playing;
}

class _FullPainter extends CustomPainter {
  _FullPainter(this.full);
  final bool full;
  @override
  void paint(Canvas c, Size s) {
    final p = Paint()
      ..color = const Color(0xFFFFFFFF)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.2;
    final w = s.width, m = w * .12, a = w * .28;
    // corner brackets: outward = enter fullscreen, inward = exit
    for (final (cx, cy, dx, dy) in [(m, m, 1.0, 1.0), (w - m, m, -1.0, 1.0), (m, w - m, 1.0, -1.0), (w - m, w - m, -1.0, -1.0)]) {
      if (!full) {
        c.drawPath(Path()..moveTo(cx, cy + dy * a)..lineTo(cx, cy)..lineTo(cx + dx * a, cy), p);
      } else {
        final ix = cx + dx * a, iy = cy + dy * a;
        c.drawPath(Path()..moveTo(ix - dx * a, iy)..lineTo(ix, iy)..lineTo(ix, iy - dy * a), p);
      }
    }
  }

  @override
  bool shouldRepaint(_FullPainter o) => o.full != full;
}

class _Spinner extends StatefulWidget {
  const _Spinner();
  @override
  State<_Spinner> createState() => _SpinnerState();
}

class _SpinnerState extends State<_Spinner> with SingleTickerProviderStateMixin {
  late final _c = AnimationController(vsync: this, duration: const Duration(milliseconds: 900))..repeat();
  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => RotationTransition(
    turns: _c,
    child: const SizedBox(width: 36, height: 36, child: CustomPaint(painter: _ArcPainter())),
  );
}

class _ArcPainter extends CustomPainter {
  const _ArcPainter();
  @override
  void paint(Canvas c, Size s) => c.drawArc(
    Offset.zero & s,
    0,
    4.2,
    false,
    Paint()
      ..color = const Color(0xFFFFFFFF)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.5
      ..strokeCap = StrokeCap.round,
  );
  @override
  bool shouldRepaint(_ArcPainter o) => false;
}
