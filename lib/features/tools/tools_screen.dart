import 'package:flutter/material.dart';

import 'phet_sim_page.dart';

class ToolsScreen extends StatefulWidget {
  /// Optional grade/subject for app_shell compat (subject-scoped tools later).
  const ToolsScreen({super.key, this.grade, this.subject});

  final String? grade;
  final String? subject;

  @override
  State<ToolsScreen> createState() => _ToolsScreenState();
}

class _ToolsScreenState extends State<ToolsScreen> {
  String display = '0';

  void _key(String k) {
    setState(() {
      if (k == 'C') {
        display = '0';
        return;
      }
      if (k == '=') {
        try {
          final ops = ['+', '-', '*', '/'];
          final op = ops.cast<String?>().firstWhere(
                (o) => o != null && display.contains(o),
                orElse: () => null,
              );
          if (op == null) return;
          final parts = display.split(op);
          if (parts.length != 2) return;
          final a = double.parse(parts[0]);
          final b = double.parse(parts[1]);
          final r = switch (op) {
            '+' => a + b,
            '-' => a - b,
            '*' => a * b,
            '/' => b == 0 ? double.nan : a / b,
            _ => double.nan,
          };
          display = r == r.roundToDouble() ? r.toInt().toString() : r.toString();
        } catch (_) {
          display = 'Error';
        }
        return;
      }
      if (display == '0' && !['+', '-', '*', '/'].contains(k)) {
        display = k;
      } else {
        display += k;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final keys = [
      ['7', '8', '9', '/'],
      ['4', '5', '6', '*'],
      ['1', '2', '3', '-'],
      ['C', '0', '=', '+'],
    ];
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Tools', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        const Text('Calculator', style: TextStyle(fontWeight: FontWeight.w600)),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                Align(
                  alignment: Alignment.centerRight,
                  child: Text(display, style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
                ),
                const SizedBox(height: 12),
                for (final row in keys)
                  Row(
                    children: row
                        .map(
                          (k) => Expanded(
                            child: Padding(
                              padding: const EdgeInsets.all(4),
                              child: OutlinedButton(
                                onPressed: () => _key(k),
                                child: Text(k),
                              ),
                            ),
                          ),
                        )
                        .toList(),
                  ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        Card(
          color: const Color(0xFF0F766E),
          child: ListTile(
            leading: const CircleAvatar(
              backgroundColor: Colors.white24,
              child: Icon(Icons.science, color: Colors.white),
            ),
            title: const Text(
              'Virtual lab (PhET)',
              style: TextStyle(color: Colors.white, fontWeight: FontWeight.w800),
            ),
            subtitle: const Text(
              'Offline simulations · physics & chemistry',
              style: TextStyle(color: Color(0xFFCCFBF1)),
            ),
            trailing: const Icon(Icons.chevron_right, color: Colors.white),
            onTap: () {
              Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const PhetCatalogPage()),
              );
            },
          ),
        ),
        const SizedBox(height: 16),
        const Text(
          'Dictionary and more tools load from offline JSON packs as you upload them.',
          style: TextStyle(fontSize: 13),
        ),
      ],
    );
  }
}
