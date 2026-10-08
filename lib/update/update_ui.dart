// Update card (Home), update page and the Settings "App updates" section.
import 'package:flutter/widgets.dart';

import '../high/screens/toast.dart';
import '../high/theme/tokens.dart';
import '../high/widgets/art.dart' show Ic;
import '../high/widgets/kit.dart';
import '../high/widgets/page.dart';
import 'updater.dart';

String _mb(int b) => '${(b / 1e6).toStringAsFixed(b > 1e8 ? 0 : 1)} MB';

/// Home: appears only when an update (online or a shared APK) is ready to get.
class UpdateCard extends StatelessWidget implements Spaced {
  const UpdateCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: Updater.instance,
    builder: (context, _) {
      final u = Updater.instance, p = Kit.of(context).p;
      if (!u.hasUpdate) return const SizedBox.shrink();
      final name = u.available?.versionName ?? u.local!.versionName;
      return Panel(
        tone: 'mint',
        margin: bareM(context, this, blockMargin),
        padding: const EdgeInsets.all(14),
        onTap: () => HighNav.of(context).open('update', () => const UpdatePage()),
        child: Row(
          spacing: 12,
          children: [
            const Badge('mint', 'repeat', s: 42),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('New 4 version $name', style: ts(15, w900, p.ink)),
                  Text(u.local != null && u.available == null ? 'Found in your shared folder · tap to install' : 'Tap to download${u.available!.size > 0 ? ' (${_mb(u.available!.size)})' : ''}', style: ts(12.5, w700, p.ink2)),
                ],
              ),
            ),
            Ic('right', size: 20, color: p.ink3),
          ],
        ),
      );
    },
  );
}

class UpdatePage extends StatelessWidget {
  const UpdatePage({super.key});
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: Updater.instance,
    builder: (context, _) {
      final u = Updater.instance, p = Kit.of(context).p, m = u.available;
      final busy = u.step == UpdateStep.downloading || u.step == UpdateStep.verifying || u.step == UpdateStep.checking;
      return PageShell(
        top: TopBar(title: 'App update', sub: 'Installed: ${u.currentName}', onBack: () => HighNav.of(context).back(), tab: false),
        body: ScreenList(
          children: [
            Panel(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                spacing: 10,
                children: [
                  if (m != null) ...[
                    Text('4 ${m.versionName}', style: ts(18, w900, p.ink)),
                    if (m.notes.isNotEmpty) Text(m.notes, style: ts(13.5, w700, p.ink2, height: 1.4)),
                    if (m.size > 0) Text('Download size ${_mb(m.size)}', style: ts(12.5, w700, p.ink3)),
                  ] else if (u.local != null) ...[
                    Text('4 ${u.local!.versionName}', style: ts(18, w900, p.ink)),
                    Text('Found in your shared folder and checked: it is genuine 4, signed like this app.', style: ts(13.5, w700, p.ink2)),
                  ] else
                    Text(u.message ?? 'No update found yet.', style: ts(14, w800, p.ink2)),
                  if (u.step == UpdateStep.downloading || u.step == UpdateStep.verifying) Bar(u.progress * 100, tone: 'mint'),
                  if (u.step == UpdateStep.verifying) Text('Checking the download…', style: ts(12.5, w700, p.ink3)),
                  if (u.message != null && (m != null || u.local != null)) Text(u.message!, style: ts(12.5, w800, p.coral)),
                  if (u.step == UpdateStep.ready || (u.local != null && m == null))
                    Btn('Install', icon: 'check', block: true, onTap: () => u.install())
                  else if (m != null)
                    Btn(u.step == UpdateStep.downloading ? 'Downloading ${(u.progress * 100).round()}%' : (u.step == UpdateStep.failed ? 'Resume download' : 'Download'), block: true, onTap: busy ? null : () => u.download()),
                  Btn(u.step == UpdateStep.checking ? 'Checking…' : 'Check again', kind: BtnKind.soft, block: true, onTap: busy ? null : () => u.check()),
                  Text('Android asks you to confirm the install (one tap). Your unlock, progress and resources stay.', style: ts(12, w700, p.ink3)),
                ],
              ),
            ),
          ],
        ),
      );
    },
  );
}

/// Settings section.
class UpdateSettings extends StatelessWidget {
  const UpdateSettings({super.key});
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: Updater.instance,
    builder: (context, _) {
      final u = Updater.instance;
      return Panel(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          spacing: 10,
          children: [
            Seg(
              current: u.wifiOnly ? 'wifi' : 'any',
              items: const [
                (id: 'wifi', label: 'Wi-Fi only', icon: 'check', count: null, tone: 'mint', enabled: true),
                (id: 'any', label: 'Wi-Fi or data', icon: 'check', count: null, tone: 'mint', enabled: true),
              ],
              onPick: (v) => u.setWifiOnly(v == 'wifi'),
            ),
            Btn(
              u.step == UpdateStep.checking ? 'Checking…' : 'Check for updates (${u.currentName})',
              icon: 'repeat',
              kind: BtnKind.soft,
              block: true,
              onTap: () async {
                final m = await u.check();
                if (!context.mounted) return;
                if (m != null) {
                  HighNav.of(context).open('update', () => const UpdatePage());
                } else {
                  toast(context, u.message ?? '');
                }
              },
            ),
          ],
        ),
      );
    },
  );
}
