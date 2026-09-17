import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';

import '../../core/content/content_repository.dart';
import '../../core/curriculum/streams.dart';
import '../../core/licensing/unlock_store.dart';
import '../../core/theme/four_theme.dart';
import '../settings/settings_page.dart';
import 'grade_hub_page.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
    required this.grade,
    required this.stream,
    required this.onGrade,
    required this.onStream,
    required this.onGradeAndStream,
    required this.onOpenNotes,
    required this.onOpenPractice,
    required this.onOpenBot,
    required this.onOpenExams,
    this.onOpenTools,
    this.onOpenLabs,
  });

  final String grade;
  final String stream;
  final ValueChanged<String> onGrade;
  final ValueChanged<String> onStream;
  final void Function(String grade, String stream) onGradeAndStream;
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
  }

  void _openTrack(String grade, String stream) {
    widget.onGradeAndStream(grade, stream);
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => GradeHubPage(
          grade: grade,
          stream: stream,
          onGradeSelected: widget.onGrade,
          onStreamSelected: widget.onStream,
        ),
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
          ],
        ),
      ),
    );
  }

  Widget _gradeTile({
    required String label,
    required String grade,
    required String stream,
    required bool selected,
    required bool dark,
  }) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(4),
        child: Material(
          color: selected
              ? const Color(0xFFFBBF24)
              : (dark ? const Color(0xFF1E293B) : Colors.white),
          borderRadius: BorderRadius.circular(16),
          elevation: selected ? 2 : 0,
          child: InkWell(
            borderRadius: BorderRadius.circular(16),
            onTap: () => _openTrack(grade, stream),
            child: Container(
              height: 64,
              alignment: Alignment.center,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: selected
                      ? const Color(0xFFF59E0B)
                      : (dark ? Colors.white12 : const Color(0xFFE2E8F0)),
                ),
              ),
              child: Text(
                label,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: label.length > 4 ? 13 : 20,
                  fontWeight: FontWeight.w900,
                  height: 1.15,
                  color: selected
                      ? const Color(0xFF0F172A)
                      : (dark ? Colors.white : const Color(0xFF0F172A)),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final repo = ContentRepository.instance;
    final dark = Theme.of(context).brightness == Brightness.dark;

    return FutureBuilder(
      future: repo.matricBundle(),
      builder: (context, snap) {
        final matricCount =
            snap.hasData ? (snap.data as dynamic).questions.length : '—';

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
                    const SizedBox(height: 16),
                    const Text('4',
                        style: TextStyle(
                            color: Colors.white,
                            fontSize: 36,
                            fontWeight: FontWeight.w900,
                            letterSpacing: -0.5)),
                    const Text('Pick grade · Science or Arts for G11/G12',
                        style: TextStyle(
                            color: Color(0xFFCCFBF1),
                            fontSize: 14,
                            fontWeight: FontWeight.w600)),
                    const SizedBox(height: 14),
                    GestureDetector(
                      onTap: _showDeviceQr,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: Colors.black.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.white24),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.qr_code_2,
                                color: Colors.white, size: 22),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Text(
                                deviceId,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.w800,
                                    fontSize: 12,
                                    letterSpacing: 0.6),
                              ),
                            ),
                            const Text('Unlock',
                                style: TextStyle(
                                    color: Color(0xFFFBBF24),
                                    fontWeight: FontWeight.w900,
                                    fontSize: 12)),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 20, 16, 6),
                child: Text(
                  'Junior',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 13,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12),
                child: Row(
                  children: [
                    _gradeTile(
                      label: 'G9',
                      grade: 'G9',
                      stream: CurriculumStreams.science,
                      selected: widget.grade == 'G9',
                      dark: dark,
                    ),
                    _gradeTile(
                      label: 'G10',
                      grade: 'G10',
                      stream: CurriculumStreams.science,
                      selected: widget.grade == 'G10',
                      dark: dark,
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 6),
                child: Text(
                  'Grade 11',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 13,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12),
                child: Row(
                  children: [
                    _gradeTile(
                      label: '11 Science',
                      grade: 'G11',
                      stream: CurriculumStreams.science,
                      selected: widget.grade == 'G11' &&
                          widget.stream == CurriculumStreams.science,
                      dark: dark,
                    ),
                    _gradeTile(
                      label: '11 Arts',
                      grade: 'G11',
                      stream: CurriculumStreams.arts,
                      selected: widget.grade == 'G11' &&
                          widget.stream == CurriculumStreams.arts,
                      dark: dark,
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 6),
                child: Text(
                  'Grade 12',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 13,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 12),
                child: Row(
                  children: [
                    _gradeTile(
                      label: '12 Science',
                      grade: 'G12',
                      stream: CurriculumStreams.science,
                      selected: widget.grade == 'G12' &&
                          widget.stream == CurriculumStreams.science,
                      dark: dark,
                    ),
                    _gradeTile(
                      label: '12 Arts',
                      grade: 'G12',
                      stream: CurriculumStreams.arts,
                      selected: widget.grade == 'G12' &&
                          widget.stream == CurriculumStreams.arts,
                      dark: dark,
                    ),
                  ],
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
                child: Text(
                  'Matriculation exams',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 15,
                    color: dark ? FourTheme.darkText : FourTheme.ink,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Material(
                  color: Colors.transparent,
                  child: InkWell(
                    borderRadius: BorderRadius.circular(22),
                    onTap: widget.onOpenExams,
                    child: Ink(
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFF7C3AED), Color(0xFF4F46E5)],
                        ),
                        borderRadius: BorderRadius.circular(22),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF7C3AED).withOpacity(0.35),
                            blurRadius: 16,
                            offset: const Offset(0, 8),
                          ),
                        ],
                      ),
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(20, 22, 20, 22),
                        child: Row(
                          children: [
                            Container(
                              width: 56,
                              height: 56,
                              decoration: BoxDecoration(
                                color: Colors.white.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(16),
                              ),
                              child: const Icon(Icons.assignment_rounded,
                                  color: Colors.white, size: 30),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Text(
                                    'Matriculation',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 22,
                                      fontWeight: FontWeight.w900,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    '$matricCount questions · subject · year',
                                    style: const TextStyle(
                                      color: Color(0xFFE9D5FF),
                                      fontWeight: FontWeight.w600,
                                      fontSize: 13,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            const Icon(Icons.arrow_forward_ios,
                                color: Colors.white, size: 18),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 22, 16, 8),
                child: Text(
                  'Also',
                  style: TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 13,
                    color: dark ? FourTheme.darkMuted : FourTheme.muted,
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.fromLTRB(12, 0, 12, 28),
                child: Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    _MiniChip(
                        icon: Icons.auto_stories_rounded,
                        label: 'Notes',
                        onTap: widget.onOpenNotes),
                    _MiniChip(
                        icon: Icons.quiz_rounded,
                        label: 'Practice',
                        onTap: widget.onOpenPractice),
                    _MiniChip(
                        icon: Icons.smart_toy_rounded,
                        label: 'Coach',
                        onTap: widget.onOpenBot),
                    if (widget.onOpenLabs != null)
                      _MiniChip(
                          icon: Icons.science_rounded,
                          label: 'Labs',
                          onTap: widget.onOpenLabs!),
                    if (widget.onOpenTools != null)
                      _MiniChip(
                          icon: Icons.handyman_rounded,
                          label: 'Tools',
                          onTap: widget.onOpenTools!),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class _MiniChip extends StatelessWidget {
  const _MiniChip({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  final IconData icon;
  final String label;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Material(
      color: dark ? const Color(0xFF1E293B) : Colors.white,
      borderRadius: BorderRadius.circular(14),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(14),
            border: Border.all(
              color: dark ? Colors.white12 : const Color(0xFFE2E8F0),
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 18, color: FourTheme.primary),
              const SizedBox(width: 8),
              Text(label,
                  style: TextStyle(
                    fontWeight: FontWeight.w800,
                    fontSize: 13,
                    color: dark ? Colors.white : const Color(0xFF0F172A),
                  )),
            ],
          ),
        ),
      ),
    );
  }
}
