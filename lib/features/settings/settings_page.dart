import 'package:flutter/material.dart';

import '../../core/l10n/app_strings.dart';
import '../../core/settings/app_settings.dart';
import '../../core/theme/four_theme.dart';

/// Settings — opened from Home (not buried in Tools).
class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    final s = AppSettings.instance;
    final dark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: Text(AppStrings.settings,
            style: const TextStyle(fontWeight: FontWeight.w800)),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          SwitchListTile(
            title: Text(AppStrings.darkMode,
                style: const TextStyle(fontWeight: FontWeight.w800)),
            subtitle: Text(
              dark ? 'Modern dark · cyan accents' : 'Light · current look',
              style: TextStyle(
                color: dark ? FourTheme.darkMuted : FourTheme.muted,
              ),
            ),
            value: s.darkMode,
            onChanged: (v) async {
              await s.setDark(v);
              setState(() {});
            },
          ),
          const Divider(),
          Text(AppStrings.language,
              style: const TextStyle(fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          SegmentedButton<bool>(
            segments: [
              ButtonSegment(value: false, label: Text(AppStrings.english)),
              ButtonSegment(
                  value: true, label: Text(AppStrings.tigrinyaLabel)),
            ],
            selected: {s.tigrinya},
            onSelectionChanged: (set) async {
              await s.setTigrinya(set.first);
              setState(() {});
            },
          ),
          const SizedBox(height: 28),
          Text(AppStrings.about,
              style:
                  const TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
          const SizedBox(height: 8),
          Text(AppStrings.developedBy, style: const TextStyle(height: 1.5)),
          const SizedBox(height: 8),
          const Text(
            'Developed by SHAMM TESFALEM\nPhone: 07162947',
            style: TextStyle(height: 1.5),
          ),
        ],
      ),
    );
  }
}
