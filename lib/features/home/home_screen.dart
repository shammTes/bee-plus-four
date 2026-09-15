import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';

import '../../core/content/content_repository.dart';
import '../../core/licensing/unlock_store.dart';
import '../../core/theme/four_theme.dart';
import '../settings/settings_page.dart';
import '../textbooks/textbooks_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
    required this.grade,
    required this.onGrade,
    required this.onOpenNotes,
    required this.onOpenPractice,
    required this.onOpenBot,
    required this.onOpenExams,
    this.onOpenTools,
    this.onOpenLabs,
  });

  final String grade;
  final ValueChanged<String> onGrade;
  final VoidCallback onOpenNotes;
  final VoidCallback onOpenPractice;
  final VoidCallback onOpenBot;
  final VoidCallback onOpenExams;
  final VoidCallback? onOpenTools;
  final VoidCallback? onOpenLabs;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String deviceId = '…';

  @override
  void initState() {
    super.initState();
    UnlockStore.instance.deviceId().then((id) {
      if (mounted) setState(() => deviceId = id);
    });
    WidgetsBinding.instance.addPostFrameCallback((_) => _maybeOnboard());
  }

  Future<void> _maybeOnboard() async {
    if (UnlockStore.instance.seenOnboarding) return;
    if (!mounted) return;
    await showDialog<void>(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        title: const Text('Welcome to 4'),
        content: const Text(
          'Quick path:\n'
          '1) Pick your grade on Home\n'
          '2) Notes → unit cards\n'
          '3) Textbooks → full PDF books\n'
          '4) Practice → unit mastery\n'
          '5) Coach · Labs · Tools\n\n'
          'Show your Device QR to Bee Seller to unlock.\n'
          'Settings (gear) for dark mode and language.',
        ),
        actions: [
          FilledButton(
            onPressed: () async {
              await UnlockStore.instance.markOnboardingSeen();
              if (ctx.mounted) Navigator.pop(ctx);
            },
            child: const Text('Got it'),
          ),
        ],
      ),
    );
  }

  void _showDeviceQr() {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(24, 8, 24, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Device ID',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
            const SizedBox(height: 8),
            const Text(
              'Show this QR to Bee Seller to unlock the app.',
              textAlign: TextAlign.center,
              style: TextStyle(color: FourTheme.muted),
            ),
            const SizedBox(height: 16),
            if (deviceId.length > 2)
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: const Color(0xFFE2E8F0)),
                ),
                child: QrImageView(
                  data: deviceId,
                  version: QrVersions.auto,
                  size: 200,
                  backgroundColor: Colors.white,
                  eyeStyle: const QrEyeStyle(
                    eyeShape: QrEyeShape.square,
                    color: Color(0xFF0F172A),
                  ),
                  dataModuleStyle: const QrDataModuleStyle(
                    dataModuleShape: QrDataModuleShape.square,
                    color: Color(0xFF0F172A),
                  ),
                ),
              )
            else
              const CircularProgressIndicator(),
            const SizedBox(height: 12),
            SelectableText(
              deviceId,
              style: const TextStyle(
                fontWeight: FontWeight.w800,
                letterSpacing: 1.2,
                fontSize: 13,
              ),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () {
                Clipboard.setData(ClipboardData(text: deviceId));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Device ID copied')),
                );
              },
              icon: const Icon(Icons.copy),
              label: const Text('Copy ID'),
            ),
          ],
        ),
      ),
    );
  }

  void _showAbout() {
    showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.fromLTRB(24, 8, 24, 32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('About 4',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
            const SizedBox(height: 12),
            const Text(
              'Developed by SHAMM TESFALEM\nPhone: 07162947',
              style: TextStyle(height: 1.5, fontSize: 15),
            ),
            const SizedBox(height: 16),
            Text('Device ID: $deviceId',
                style: const TextStyle(
                    fontWeight: FontWeight.w800, letterSpacing: 0.5)),
            const SizedBox(height: 8),
            const Text(
              'Offline high-school study · G9–G12 · Eritrea curriculum focus.',
              style: TextStyle(color: FourTheme.muted),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final repo = ContentRepository.instance;
    final dark = Theme.of(context).brightness == Brightness.dark;
    return FutureBuilder(
      future: Future.wait([
        repo.notes(),
        repo.questions(),
        repo.matricBundle(),
      ]),
      builder: (context, snap) {
        final noteCount = snap.hasData ? (snap.data![0] as List).length : '—';
        final qCount = snap.hasData ? (snap.data![1] as List).length : '—';
        final matricCount =
            snap.hasData ? (snap.data![2] as dynamic).questions.length : '—';

        return Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: dark
                  ? const [
                      Color(0xFF0B1220),
                      Color(0xFF111827),
                      Color(0xFF0B1220)
                    ]
                  : const [
                      Color(0xFFE0F2FE),
                      Color(0xFFF5F3FF),
                      Color(0xFFF8FAFC)
                    ],
            ),
          ),
          child: ListView(
            children: [
              Container(
                decoration: BoxDecoration(
                  gradient: dark
                      ? FourTheme.heroGradientDark
                      : FourTheme.heroGradient,
                  borderRadius: const BorderRadius.only(
                    bottomLeft: Radius.circular(28),
                    bottomRight: Radius.circular(28),
                  ),
                ),
                padding: EdgeInsets.fromLTRB(
                  20,
                  MediaQuery.paddingOf(context).top + 16,
                  20,
                  22,
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 48,
                          height: 48,
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.2),
                            borderRadius: BorderRadius.circular(14),
                          ),
                          alignment: Alignment.center,
                          child: const Text('4',
                              style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 26,
                                  fontWeight: FontWeight.w900)),
                        ),
                        const Spacer(),
                        IconButton(
                          onPressed: _showDeviceQr,
                          icon: const Icon(Icons.qr_code_2, color: Colors.white),
                          tooltip: 'Device QR',
                        ),
                        IconButton(
                          onPressed: () => Navigator.of(context).push(
                            MaterialPageRoute(
                                builder: (_) => const SettingsPage()),
                          ),
                          icon: const Icon(Icons.settings_outlined,
                              color: Colors.white),
                          tooltip: 'Settings',
                        ),
                        IconButton(
                          onPressed: _showAbout,
                          icon: const Icon(Icons.info_outline,
                              color: Colors.white),
                          tooltip: 'About',
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    const Text('4',
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 34,
                            fontWeight: FontWeight.w900,
                            letterSpacing: -0.5)),
                    const SizedBox(height: 4),
                    const Text('Study · Practice · Master',
                        style: TextStyle(
                            color: Color(0xFFCCFBF1),
                            fontSize: 14,
                            fontWeight: FontWeight.w600)),
                    const SizedBox(height: 12),
                    GestureDetector(
                      onTap: _showDeviceQr,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 10),
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(14),
                          border: Border.all(color: Colors.white24),
                        ),
                        child: Row(
                          children: [
                            Container(
                              width: 44,
                              height: 44,
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(8),
                              ),
                              padding: const EdgeInsets.all(4),
                              child: deviceId.length > 2
                                  ? QrImageView(
                                      data: deviceId,
                                      version: QrVersions.auto,
                                      size: 36,
                                      padding: EdgeInsets.zero,
                                      backgroundColor: Colors.white,
                                    )
                                  : const SizedBox.shrink(),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text('Device QR',
                                      style: TextStyle(
                                          color: Colors.white70,
                                          fontSize: 11,
                                          fontWeight: FontWeight.w700)),
                                  Text(deviceId,
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                      style: const TextStyle(
                                          color: Colors.white,
                                          fontWeight: FontWeight.w800,
                                          letterSpacing: 0.8,
                                          fontSize: 12)),
                                ],
                              ),
                            ),
                            const Icon(Icons.fullscreen,
                                color: Colors.white70, size: 20),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 14),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: ['G9', 'G10', 'G11', 'G12'].map((g) {
                          final sel = g == widget.grade;
                          return Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: ChoiceChip(
                              label: Text(g),
                              selected: sel,
                              onSelected: (_) => widget.onGrade(g),
                              selectedColor: const Color(0xFFFBBF24),
                              backgroundColor: Colors.white,
                              labelStyle: const TextStyle(
                                color: Color(0xFF0F172A),
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                child: Row(
                  children: [
                    _StatTile(label: 'Notes', value: '$noteCount'),
                    const SizedBox(width: 8),
                    _StatTile(label: 'Practice', value: '$qCount'),
                    const SizedBox(width: 8),
                    _StatTile(label: 'Matric', value: '$matricCount'),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    _ActionCard(
                      title: 'Notes',
                      subtitle: 'Units · illustrated · practice',
                      icon: Icons.auto_stories_rounded,
                      color: FourTheme.primary,
                      onTap: widget.onOpenNotes,
                    ),
                    _ActionCard(
                      title: 'Textbooks',
                      subtitle: 'G9–G12 offline PDF library',
                      icon: Icons.menu_book_rounded,
                      color: const Color(0xFF0F766E),
                      onTap: () => Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => TextbooksScreen(
                            initialGrade: widget.grade,
                          ),
                        ),
                      ),
                    ),
                    _ActionCard(
                      title: 'Practice',
                      subtitle: 'Unit · multi · mastery',
                      icon: Icons.quiz_rounded,
                      color: FourTheme.violet,
                      onTap: widget.onOpenPractice,
                    ),
                    _ActionCard(
                      title: 'Coach',
                      subtitle: 'Notes · quiz · matric mode',
                      icon: Icons.smart_toy_rounded,
                      color: FourTheme.accentDeep,
                      onTap: widget.onOpenBot,
                    ),
                    _ActionCard(
                      title: 'Exams',
                      subtitle: 'Matriculation · model papers',
                      icon: Icons.assignment_rounded,
                      color: FourTheme.mint,
                      onTap: widget.onOpenExams,
                    ),
                    if (widget.onOpenLabs != null)
                      _ActionCard(
                        title: 'Virtual labs',
                        subtitle: 'PhET offline · Physics · Chem · Bio · Math',
                        icon: Icons.science_rounded,
                        color: const Color(0xFF0EA5E9),
                        onTap: widget.onOpenLabs!,
                      ),
                    if (widget.onOpenTools != null)
                      _ActionCard(
                        title: 'Tools',
                        subtitle: 'Study · Calculator',
                        icon: Icons.handyman_rounded,
                        color: const Color(0xFFF59E0B),
                        onTap: widget.onOpenTools!,
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
            ],
          ),
        );
      },
    );
  }
}

class _StatTile extends StatelessWidget {
  const _StatTile({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Expanded(
      child: FourTheme.glassPanel(
        dark: dark,
        child: Column(
          children: [
            Text(value,
                style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 18,
                    color: dark ? FourTheme.darkText : FourTheme.ink)),
            Text(label,
                style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted)),
          ],
        ),
      ),
    );
  }
}

class _ActionCard extends StatelessWidget {
  const _ActionCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.onTap,
  });

  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(18),
          child: Ink(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [color, color.withOpacity(0.85)],
              ),
              borderRadius: BorderRadius.circular(18),
              boxShadow: [
                BoxShadow(
                  color: color.withOpacity(0.25),
                  blurRadius: 12,
                  offset: const Offset(0, 6),
                ),
              ],
            ),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Icon(icon, color: Colors.white),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(title,
                            style: const TextStyle(
                                color: Colors.white,
                                fontSize: 17,
                                fontWeight: FontWeight.w900)),
                        Text(subtitle,
                            style: TextStyle(
                                color: Colors.white.withOpacity(0.9),
                                fontSize: 12,
                                fontWeight: FontWeight.w600)),
                      ],
                    ),
                  ),
                  const Icon(Icons.arrow_forward_ios_rounded,
                      color: Colors.white70, size: 16),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
