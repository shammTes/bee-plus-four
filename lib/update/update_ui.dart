// Update card (Home), update page and the Settings "App updates" section. Updates come only as a file.
import 'package:flutter/widgets.dart';

import '../high/screens/toast.dart';
import '../high/theme/tokens.dart';
import '../high/widgets/kit.dart';
import '../high/widgets/page.dart';
import 'updater.dart';

/// "primary:SHAREit/apps" style label of a SAF tree uri.
String folderLabel(String uri) {
  final i = uri.indexOf('/tree/');
  final id = Uri.decodeComponent(i < 0 ? uri : uri.substring(i + 6).split('/').first);
  final c = id.indexOf(':');
  final path = c < 0 ? id : id.substring(c + 1);
  return path.isEmpty ? 'Phone storage' : path;
}

Future<void> _install(BuildContext context) async {
  final r = await Updater.instance.install();
  if (r == 'permission' && context.mounted) toast(context, 'Allow "Install unknown apps" for 4, then come back');
}

Future<void> _share(BuildContext context) async {
  final m = await Updater.instance.shareSelf();
  if (m.isNotEmpty && context.mounted) toast(context, m);
}

Future<void> _find(BuildContext context) async {
  final m = await Updater.instance.pickFile();
  if (m.isNotEmpty && context.mounted) toast(context, m);
}

/// Home: appears only when a checked, newer 4 APK was found on the phone.
class UpdateCard extends StatelessWidget implements Spaced {
  const UpdateCard({super.key});
  @override
  EdgeInsets get blockMargin => const EdgeInsets.symmetric(vertical: 14);
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: Updater.instance,
    builder: (context, _) {
      final u = Updater.instance, p = Kit.of(context).p, l = u.local;
      if (l == null) return const SizedBox.shrink();
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
                  Text('New 4 version ${l.versionName}', style: ts(15, w900, p.ink)),
                  Text('Found in ${l.from.isEmpty ? 'a shared file' : l.from} · checked', style: ts(12.5, w700, p.ink2)),
                ],
              ),
            ),
            Btn('Install', kind: BtnKind.tone, tone: 'mint', padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10), fontSize: 13.5, onTap: () => _install(context)),
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
      final u = Updater.instance, p = Kit.of(context).p, l = u.local;
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
                  if (l != null) ...[
                    Text('4 ${l.versionName}', style: ts(18, w900, p.ink)),
                    Text('Found in ${l.from.isEmpty ? 'a shared file' : l.from} and checked: it is genuine 4, newer, and signed like this app.', style: ts(13.5, w700, p.ink2, height: 1.4)),
                    Btn('Install', icon: 'check', block: true, onTap: () => _install(context)),
                  ] else
                    Text(u.scanning ? 'Looking for an update file…' : 'No newer 4 file found on this phone yet.', style: ts(14, w800, p.ink2)),
                  if (u.message != null) Text(u.message!, style: ts(12.5, w800, p.coral, height: 1.35)),
                  Text('Android asks you to confirm the install (one tap). Your unlock, progress and resources stay.', style: ts(12, w700, p.ink3)),
                ],
              ),
            ),
            const UpdateSettings(),
          ],
        ),
      );
    },
  );
}

/// Settings section (also on the update page).
class UpdateSettings extends StatelessWidget {
  const UpdateSettings({super.key});
  @override
  Widget build(BuildContext context) => ListenableBuilder(
    listenable: Updater.instance,
    builder: (context, _) {
      final u = Updater.instance, p = Kit.of(context).p, f = u.updateFolder;
      return Panel(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          spacing: 10,
          children: [
            Text(
              'Updates come as a file, never over the internet. Get the new 4 APK from a friend (SHAREit, Bluetooth, Nearby Share or cable). 4 looks in your resources folder${f != null ? ' and update folder' : ''} each time it opens.',
              style: ts(12.5, w700, p.ink2, height: 1.4),
            ),
            Btn(u.scanning ? 'Looking…' : 'Find update file', icon: 'search', kind: BtnKind.soft, block: true, onTap: u.scanning ? null : () => _find(context)),
            Btn(f == null ? 'Watch a folder for updates (e.g. SHAREit)' : 'Update folder: ${folderLabel(f)}', icon: 'repeat', kind: BtnKind.soft, block: true, onTap: () async {
              final ok = await u.pickUpdateFolder();
              if (context.mounted && u.updateFolder != null) toast(context, ok ? 'Update found' : 'Watching ${folderLabel(u.updateFolder!)}');
            }),
            Btn(u.sharing ? 'Preparing…' : 'Send 4 to a friend (${u.currentName})', icon: 'send', kind: BtnKind.soft, block: true, onTap: u.sharing ? null : () => _share(context)),
          ],
        ),
      );
    },
  );
}
