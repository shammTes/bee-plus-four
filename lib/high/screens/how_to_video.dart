// Settings → "How to use the app": the bundled tutorial video (assets/high/howto/Four_HowTo.mp4) with a chapter list.
// Lazy: Settings imports this file deferred, and nothing reads the asset until this page is opened; ExoPlayer then
// streams it straight from the APK (FourVideo.kt createAsset). Off Android (tests, web) only the chapter list shows.
import 'dart:async';

import 'package:flutter/foundation.dart' show TargetPlatform, defaultTargetPlatform, kIsWeb;
import 'package:flutter/widgets.dart';

import '../../resources/native_video.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';

const kHowToAsset = 'assets/high/howto/Four_HowTo.mp4';

/// (start in ms, title): keep in step with the video (tool/howto/chapters.txt)
const kHowToChapters = <(int, String)>[
  // CHAPTERS-BEGIN
  (0, 'Start'),
  (2758, 'Unlock 4 (scan QR or type code)'),
  (29286, 'Home and choosing your grade'),
  (65838, 'Notes: subjects, units, cards'),
  (98712, 'Memory tricks, games and unit quiz'),
  (130574, 'Exercise: practice and Daily Quiz'),
  (195586, 'Matric and model exams (Grades 11–12)'),
  (238850, 'Search'),
  (251355, 'Tutor: ask a question'),
  (273562, 'Virtual lab (Try it)'),
  (297884, 'Pictures, 3D models and animations'),
  (318666, 'Videos, reels and locked PDFs'),
  (344505, 'Study Coach: check-in and 30-day plan'),
  (386896, 'Study tips and worksheets'),
  (438160, 'Your progress'),
  (478620, 'Settings: name, theme, look'),
  (519126, 'Monthly update (file)'),
  (551034, 'Help and contact'),
  // CHAPTERS-END
];

class HowToVideoPage extends StatefulWidget with NoNav {
  const HowToVideoPage({super.key});
  @override
  State<HowToVideoPage> createState() => _HowToVideoPageState();
}

class _HowToVideoPageState extends State<HowToVideoPage> {
  NativeVideo? _v;
  VideoState? _st;
  Object? _err;
  Timer? _poll;
  bool _dragging = false;
  double _dragFrac = 0;

  static bool get _canPlay => !kIsWeb && defaultTargetPlatform == TargetPlatform.android;

  @override
  void initState() {
    super.initState();
    if (_canPlay) _open();
  }

  Future<void> _open() async {
    try {
      final v = await NativeVideo.openAsset(kHowToAsset);
      if (!mounted) {
        await v.dispose();
        return;
      }
      _v = v;
      await v.play();
      _poll = Timer.periodic(const Duration(milliseconds: 300), (_) => _tick());
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
    setState(() {
      _st = s;
      if (s.error != null) _err ??= s.error;
    });
  }

  @override
  void dispose() {
    _poll?.cancel();
    _v?.dispose();
    super.dispose();
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
    _tick();
  }

  Future<void> _jump(int ms) async {
    final v = _v;
    if (v == null) return;
    await v.seek(ms);
    await v.play();
    _tick();
  }

  int get _current {
    final pos = _st?.pos ?? 0;
    var i = 0;
    for (var j = 0; j < kHowToChapters.length; j++) {
      if (kHowToChapters[j].$1 <= pos + 250) i = j;
    }
    return i;
  }

  @override
  Widget build(BuildContext context) {
    final k = Kit.of(context), p = k.p;
    final cur = _current;
    return PageShell(
      top: TopBar(title: 'How to use the app', sub: 'Tap a part to jump to it', onBack: () => HighNav.of(context).back(), tab: false),
      body: Column(
        children: [
          Padding(padding: const EdgeInsets.fromLTRB(16, 4, 16, 8), child: _player(context)),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 24),
              itemCount: kHowToChapters.length,
              itemBuilder: (context, i) {
                final (ms, title) = kHowToChapters[i];
                final on = i == cur && _st != null;
                return Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Press(
                    onTap: _canPlay ? () => _jump(ms) : null,
                    deco: on ? k.d.btnSoftPressed() : k.d.btnSoft(),
                    pressedDeco: k.d.btnSoftPressed(),
                    dy: 3,
                    label: '$title, ${fmtMs(ms)}',
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
                    child: Row(
                      spacing: 12,
                      children: [
                        SizedBox(width: 44, child: Text(fmtMs(ms), style: ts(12.5, w800, on ? p.peach.deep : p.ink3))),
                        Expanded(child: Text(title, style: ts(14, w900, on ? p.peach.deep : p.ink))),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _player(BuildContext context) {
    const white = Color(0xFFFFFFFF);
    final h = (MediaQuery.sizeOf(context).height * .46).clamp(220.0, 520.0);
    final s = _st, v = _v;
    final dur = s?.dur ?? 0;
    final frac = _dragging ? _dragFrac : (dur > 0 ? ((s?.pos ?? 0) / dur).clamp(0.0, 1.0) : 0.0);
    Widget msg(String t) => Center(child: Padding(padding: const EdgeInsets.all(16), child: Text(t, textAlign: TextAlign.center, style: ts(13.5, w800, white))));
    return ClipRRect(
      borderRadius: BorderRadius.circular(18),
      child: ColoredBox(
        color: const Color(0xFF2B2118),
        child: SizedBox(
          height: h,
          child: Row(
            children: [
              Expanded(
                child: Stack(
                  fit: StackFit.expand,
                  children: [
                    if (!_canPlay)
                      msg('The video plays on the phone. Open 4 on your Android phone to watch it.')
                    else if (_err != null)
                      msg('Could not play the video.')
                    else if (v != null)
                      Center(child: AspectRatio(aspectRatio: (s != null && s.w > 0 && s.h > 0) ? s.w / s.h : 540 / 1170, child: Texture(textureId: v.id, filterQuality: FilterQuality.low))),
                    if (v != null) GestureDetector(behavior: HitTestBehavior.opaque, onTap: _playPause),
                    if (v != null && !(s?.playing ?? false))
                      Center(
                        child: IgnorePointer(
                          child: Container(
                            width: 60,
                            height: 60,
                            decoration: const BoxDecoration(color: Color(0x88000000), shape: BoxShape.circle),
                            child: const CustomPaint(painter: _PlayIcon()),
                          ),
                        ),
                      ),
                    if (v != null)
                      Positioned(
                        left: 0,
                        right: 0,
                        bottom: 0,
                        child: DecoratedBox(
                          decoration: const BoxDecoration(gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [Color(0x00000000), Color(0xAA000000)])),
                          child: Padding(
                            padding: const EdgeInsets.fromLTRB(10, 14, 10, 4),
                            child: Row(
                              spacing: 8,
                              children: [
                                Text(fmtMs(_dragging ? (_dragFrac * dur).round() : s?.pos ?? 0), style: ts(11.5, w800, white)),
                                Expanded(
                                  child: LayoutBuilder(
                                    builder: (context, c) {
                                      double f(Offset o) => (o.dx / c.maxWidth).clamp(0.0, 1.0);
                                      return GestureDetector(
                                        behavior: HitTestBehavior.opaque,
                                        onHorizontalDragStart: (d) => setState(() {
                                          _dragging = true;
                                          _dragFrac = f(d.localPosition);
                                        }),
                                        onHorizontalDragUpdate: (d) => setState(() => _dragFrac = f(d.localPosition)),
                                        onHorizontalDragEnd: (_) {
                                          v.seek((_dragFrac * dur).round());
                                          setState(() => _dragging = false);
                                        },
                                        onTapUp: (d) => v.seek((f(d.localPosition) * dur).round()),
                                        child: SizedBox(height: 26, child: CustomPaint(painter: _Bar(frac))),
                                      );
                                    },
                                  ),
                                ),
                                Text(fmtMs(dur), style: ts(11.5, w800, white)),
                              ],
                            ),
                          ),
                        ),
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Bar extends CustomPainter {
  const _Bar(this.f);
  final double f;
  @override
  void paint(Canvas c, Size s) {
    final y = s.height / 2;
    c.drawRRect(RRect.fromLTRBR(0, y - 2, s.width, y + 2, const Radius.circular(2)), Paint()..color = const Color(0x55FFFFFF));
    c.drawRRect(RRect.fromLTRBR(0, y - 2, s.width * f, y + 2, const Radius.circular(2)), Paint()..color = const Color(0xFFE88A6E));
    c.drawCircle(Offset(s.width * f, y), 6.5, Paint()..color = const Color(0xFFFFFFFF));
  }

  @override
  bool shouldRepaint(_Bar o) => o.f != f;
}

class _PlayIcon extends CustomPainter {
  const _PlayIcon();
  @override
  void paint(Canvas c, Size s) {
    final cx = s.width / 2, cy = s.height / 2;
    c.drawPath(Path()
      ..moveTo(cx - 8, cy - 12)
      ..lineTo(cx + 13, cy)
      ..lineTo(cx - 8, cy + 12)
      ..close(), Paint()..color = const Color(0xFFFFFFFF));
  }

  @override
  bool shouldRepaint(_PlayIcon o) => false;
}
