import 'package:flutter/material.dart';

class ToolsScreen extends StatefulWidget {
  const ToolsScreen({super.key});
  @override
  State<ToolsScreen> createState() => _ToolsScreenState();
}
class _ToolsScreenState extends State<ToolsScreen> {
  String display = '0';
  void _key(String k) {
    setState(() {
      if (k == 'C') { display = '0'; return; }
      if (k == '=') {
        try {
          for (final op in ['+', '-', '*', '/']) {
            if (!display.contains(op)) continue;
            final p = display.split(op);
            if (p.length != 2) continue;
            final a = double.parse(p[0]); final b = double.parse(p[1]);
            final r = switch (op) { '+' => a+b, '-' => a-b, '*' => a*b, '/' => b==0?double.nan:a/b, _ => double.nan };
            display = r == r.roundToDouble() ? r.toInt().toString() : r.toString(); return;
          }
        } catch (_) { display = 'Error'; }
        return;
      }
      display = (display == '0' && !['+','-','*','/'].contains(k)) ? k : display + k;
    });
  }
  @override
  Widget build(BuildContext context) {
    final keys = [['7','8','9','/'],['4','5','6','*'],['1','2','3','-'],['C','0','=','+']];
    return ListView(padding: const EdgeInsets.all(16), children: [
      Text('Tools', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
      const SizedBox(height: 12),
      Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(children: [
        Align(alignment: Alignment.centerRight, child: Text(display, style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold))),
        for (final row in keys) Row(children: row.map((k) => Expanded(child: Padding(padding: const EdgeInsets.all(4),
          child: OutlinedButton(onPressed: () => _key(k), child: Text(k))))).toList()),
      ]))),
    ]);
  }
}
