// Add-on resources UI: Home card, Resources page, "Extra resources" strip on notes unit pages.
// The PDF viewer (pdfrx / PDFium) lives in pdf_page.dart and is only built when a PDF is opened.
import 'package:flutter/foundation.dart' show Uint8List;
import 'package:flutter/widgets.dart';
import 'package:four_format/four_format.dart';

import '../high/screens/toast.dart';
import '../high/theme/tokens.dart';
import '../high/widgets/art.dart' show Ic;
import '../high/widgets/kit.dart';
import '../high/widgets/coach.dart' show CoachKeys;
import '../high/widgets/page.dart';
import '../licensing/lock_screen.dart';
import 'gate.dart';
import 'library.dart';
import 'native_video.dart' show fmtMs;
import 'pdf_page.dart';
import 'reels_page.dart';
import 'video_page.dart';
import 'web_page.dart';

String _subjectLabel(String s) => s.isEmpty ? 'General' : s.split('_').map((w) => w.isEmpty ? w : '${w[0].toUpperCase()}${w.substring(1)}').join(' ');

/// [scope]: the list the tile was shown in; reels swipe through the reels of that list (same subject/unit filter).
void openResource(BuildContext context, ResEntry e, {List<ResEntry>? scope}) {
  final lib = ResourceLibrary.instance;
  if (lib.mode == GateMode.locked) return openUnlock(context);
  if (e.meta.type == FourType.reel) {
    final reels = [for (final x in scope ?? lib.entries) if (x.meta.type == FourType.reel) x];
    if (!reels.any((x) => x.id == e.id)) reels.insert(0, e);
    HighNav.of(context).push(ReelsPage(reels: reels, initial: reels.indexWhere((x) => x.id == e.id)));
    return;
  }
  if (e.meta.type == FourType.web) {
    openWebResource(context, e);
    return;
  }
  HighNav.of(context).push(e.meta.type == FourType.pdf ? PdfResourcePage(entry: e) : VideoResourcePage(entry: e));
}

void openUnlock(BuildContext context) {
  final g = ResourceGate.instance;
  if (g == null) return;
  final nav = HighNav.of(context);
  nav.push(
    LockScreen(
      unlock: g.unlock,
      onUnlocked: () {
        nav.back();
        ResourceLibrary.instance.reload();
      },
    ),
  );
}

/// Home tile.
class ResourcesCard extends StatelessWidget implements Spaced {
  const ResourcesCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    if (!ResourceLibrary.instance.available) return const SizedBox.shrink();
    return KeyedSubtree(key: CoachKeys.resources, child: Panel(
      tone: 'blue',
      margin: bareM(context, this, blockMargin),
      padding: const EdgeInsets.all(14),
      onTap: () => HighNav.of(context).open('resources', () => const ResourcesPage()),
      child: Row(
        spacing: 12,
        children: [
          const Badge('blue', 'book', s: 42),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Extra resources', style: ts(15, w900, p.ink)),
                Text('Add-on PDFs and videos · tap Refresh after copying files', style: ts(12.5, w700, p.ink2)),
              ],
            ),
          ),
          Ic('right', size: 20, color: p.ink3),
        ],
      ),
    ));
  }
}

class ResourcesPage extends StatefulWidget {
  const ResourcesPage({super.key});
  @override
  State<ResourcesPage> createState() => _ResourcesPageState();
}

class _ResourcesPageState extends State<ResourcesPage> {
  final lib = ResourceLibrary.instance;
  String? _subject;

  @override
  void initState() {
    super.initState();
    lib.addListener(_changed);
    lib.ensureLoaded();
  }

  @override
  void dispose() {
    lib.removeListener(_changed);
    super.dispose();
  }

  void _changed() {
    if (mounted) setState(() {});
  }

  Future<void> _refresh() async {
    try {
      final r = await lib.refresh();
      if (!mounted) return;
      toast(context, r.error ?? (r.added == 0 && r.failed == 0 ? 'No new files found' : 'Added ${r.added}${r.failed > 0 ? ' · ${r.failed} could not be opened' : ''}'));
    } catch (e) {
      if (mounted) toast(context, 'Refresh needs Android: $e');
    }
  }

  Future<void> _folder() async {
    try {
      await lib.pickFolder();
    } catch (e) {
      if (mounted) toast(context, 'Folder picker needs Android');
    }
  }

  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    final subjects = {for (final e in lib.entries) e.meta.subject}.toList()..sort();
    final shown = [
      for (final e in lib.entries)
        if (_subject == null || e.meta.subject == _subject) e,
    ]..sort((a, b) => (a.meta.grade, a.meta.subject, a.meta.unit, a.meta.title).toString().compareTo((b.meta.grade, b.meta.subject, b.meta.unit, b.meta.title).toString()));
    return PageShell(
      top: TopBar(
        title: 'Extra resources',
        sub: lib.mode == GateMode.locked ? 'Unlock 4 to open these files' : '${lib.entries.length} file${lib.entries.length == 1 ? '' : 's'}',
        onBack: () => HighNav.of(context).back(),
        tab: false,
        actions: [CBtn('search', label: lib.busy ? 'Refreshing…' : 'Refresh', onTap: lib.busy ? () {} : _refresh)],
      ),
      body: ScreenList(
        children: [
          Panel(
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              spacing: 8,
              children: [
                Text('How to add files', style: ts(14.5, w900, p.ink)),
                Text('1. Copy the .4pdf / .4vid files to this phone (cable or SHAREit).\n2. Choose that folder once.\n3. Tap Refresh. Files are copied inside 4; you can then delete the originals.', style: ts(13, w700, p.ink2, height: 1.4)),
                Row(
                  spacing: 10,
                  children: [
                    Expanded(child: Btn(lib.folder == null ? 'Choose folder' : 'Change folder', kind: BtnKind.soft, onTap: _folder)),
                    Expanded(child: Btn(lib.busy ? 'Refreshing…' : 'Refresh', onTap: lib.busy ? null : _refresh)),
                  ],
                ),
              ],
            ),
          ),
          if (lib.mode == GateMode.locked)
            Panel(
              tone: 'peach',
              padding: const EdgeInsets.all(14),
              onTap: () => openUnlock(context),
              child: Row(
                spacing: 12,
                children: [
                  const _LockIcon(size: 34),
                  Expanded(child: Text('${lib.lockedFiles} file${lib.lockedFiles == 1 ? '' : 's'} waiting. Only phones that unlocked 4 can open them. Tap to unlock.', style: ts(13.5, w800, p.ink))),
                ],
              ),
            ),
          if (subjects.length > 1)
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                spacing: 8,
                children: [
                  _Chip('All', on: _subject == null, onTap: () => setState(() => _subject = null)),
                  for (final s in subjects) _Chip(_subjectLabel(s), on: _subject == s, onTap: () => setState(() => _subject = s)),
                ],
              ),
            ),
          if (lib.loaded && shown.isEmpty && lib.mode != GateMode.locked)
            Padding(
              padding: const EdgeInsets.all(24),
              child: Text('No resources yet.', textAlign: TextAlign.center, style: ts(14, w800, p.ink3)),
            ),
          for (final e in shown) ResourceTile(entry: e, scope: shown),
        ],
      ),
    );
  }
}

class _Chip extends StatelessWidget {
  const _Chip(this.label, {required this.on, required this.onTap});
  final String label;
  final bool on;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p;
    return GestureDetector(
      onTap: onTap,
      child: DecoratedBox(
        decoration: BoxDecoration(color: on ? p.coral : p.surface2, borderRadius: BorderRadius.circular(99)),
        child: Padding(padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8), child: Text(label, style: ts(13, w800, on ? p.onCoral : p.ink2))),
      ),
    );
  }
}

class _Thumb extends StatelessWidget {
  const _Thumb(this.e, {this.w = 56, this.h = 72});
  final ResEntry e;
  final double w, h;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, t = e.thumb;
    final video = e.meta.type == FourType.video || e.meta.type == FourType.reel;
    final img = _img(p, t);
    if (!video) return img;
    return Stack(
      children: [
        img,
        Positioned(
          right: 4,
          bottom: 4,
          child: DecoratedBox(
            decoration: BoxDecoration(color: const Color(0xCC000000), borderRadius: BorderRadius.circular(5)),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
              child: Text(e.meta.durationMs != null ? fmtMs(e.meta.durationMs!) : '▶', style: ts(10, w900, const Color(0xFFFFFFFF))),
            ),
          ),
        ),
      ],
    );
  }

  Widget _img(Palette p, Uint8List? t) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(10),
      child: SizedBox(
        width: w,
        height: h,
        child: t != null
            ? Image.memory(t, fit: BoxFit.cover, cacheWidth: (w * 2).round(), gaplessPlayback: true)
            : ColoredBox(
                color: p.surface2,
                child: Center(child: Text(switch (e.meta.type) { FourType.pdf => 'PDF', FourType.web => 'WEB', _ => 'VIDEO' }, style: ts(11, w900, p.ink3))),
              ),
      ),
    );
  }
}

class ResourceTile extends StatelessWidget {
  const ResourceTile({super.key, required this.entry, this.scope});
  final ResEntry entry;
  final List<ResEntry>? scope;
  @override
  Widget build(BuildContext context) {
    final p = Kit.of(context).p, m = entry.meta;
    return Panel(
      margin: const EdgeInsets.symmetric(vertical: 6),
      padding: const EdgeInsets.all(10),
      onTap: () => openResource(context, entry, scope: scope),
      child: Row(
        spacing: 12,
        children: [
          _Thumb(entry),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 2,
              children: [
                Text(m.title, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(14.5, w900, p.ink)),
                Text('${_subjectLabel(m.subject)} · Grade ${m.grade}${m.unit.isNotEmpty ? ' · Unit ${m.unit}' : ''}', style: ts(12.5, w700, p.ink2)),
                Text('${m.type == FourType.web ? 'INTERACTIVE' : m.type.name.toUpperCase()}${m.durationMs != null ? ' · ${fmtMs(m.durationMs!)}' : ''} · ${(entry.size / 1e6).toStringAsFixed(1)} MB', style: ts(11.5, w700, p.ink3)),
                if (m.creditLine.isNotEmpty) Text(m.creditLine, maxLines: 1, overflow: TextOverflow.ellipsis, style: ts(10.5, w700, p.ink3)),
              ],
            ),
          ),
          Ic('right', size: 20, color: p.ink3),
        ],
      ),
    );
  }
}

/// Horizontal strip on a notes unit page. Builds nothing when the unit has no add-ons.
class ResourceStrip extends StatefulWidget {
  const ResourceStrip({super.key, required this.bookId, required this.unitNumber, required this.unitId});
  final String bookId, unitId;
  final int unitNumber;
  @override
  State<ResourceStrip> createState() => _ResourceStripState();
}

class _ResourceStripState extends State<ResourceStrip> {
  final lib = ResourceLibrary.instance;
  @override
  void initState() {
    super.initState();
    if (!lib.available) return;
    lib.addListener(_changed);
    lib.ensureLoaded();
  }

  @override
  void dispose() {
    lib.removeListener(_changed);
    super.dispose();
  }

  void _changed() {
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    if (!lib.available || !lib.loaded) return const SizedBox.shrink();
    final items = lib.forUnit(widget.bookId, widget.unitNumber, widget.unitId);
    if (items.isEmpty) return const SizedBox.shrink();
    final p = Kit.of(context).p;
    return Padding(
      padding: const EdgeInsets.only(top: 8, bottom: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        spacing: 8,
        children: [
          Text('Extra resources', style: ts(15, w900, p.ink)),
          SizedBox(
            height: 132,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: items.length,
              separatorBuilder: (_, _) => const SizedBox(width: 10),
              itemBuilder: (c, i) => GestureDetector(
                onTap: () => openResource(c, items[i], scope: items),
                child: SizedBox(
                  width: 92,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    spacing: 4,
                    children: [
                      _Thumb(items[i], w: 92, h: 92),
                      Text(items[i].meta.title, maxLines: 2, overflow: TextOverflow.ellipsis, style: ts(11.5, w800, p.ink2, height: 1.15)),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _LockIcon extends StatelessWidget {
  const _LockIcon({this.size = 24});
  final double size;
  @override
  Widget build(BuildContext context) {
    final c = Kit.of(context).p.ink;
    return CustomPaint(size: Size.square(size), painter: _LockPainter(c));
  }
}

class _LockPainter extends CustomPainter {
  _LockPainter(this.c);
  final Color c;
  @override
  void paint(Canvas canvas, Size s) {
    final pt = Paint()
      ..color = c
      ..style = PaintingStyle.stroke
      ..strokeWidth = s.width * .09;
    final w = s.width;
    canvas.drawRRect(RRect.fromLTRBR(w * .18, w * .45, w * .82, w * .92, Radius.circular(w * .1)), pt);
    canvas.drawArc(Rect.fromLTRB(w * .3, w * .12, w * .7, w * .62), 3.1416, 3.1416, false, pt);
  }

  @override
  bool shouldRepaint(_LockPainter o) => o.c != c;
}
