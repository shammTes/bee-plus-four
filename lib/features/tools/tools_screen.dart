import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/l10n/app_strings.dart';
import '../../core/theme/four_theme.dart';
import '../study/study_features_screen.dart';

class ToolsScreen extends StatefulWidget {
  const ToolsScreen({super.key, this.grade = 'G10', this.subject = 'MATH'});
  final String grade;
  final String subject;

  @override
  State<ToolsScreen> createState() => _ToolsScreenState();
}

class _ToolsScreenState extends State<ToolsScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabs;
  String _expr = '';
  String _result = '0';

  @override
  void initState() {
    super.initState();
    // Study first, then Calculator
    _tabs = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabs.dispose();
    super.dispose();
  }

  void _tap(String k) {
    HapticFeedback.selectionClick();
    setState(() {
      if (k == 'C') {
        _expr = '';
        _result = '0';
        return;
      }
      if (k == '⌫') {
        if (_expr.isNotEmpty) _expr = _expr.substring(0, _expr.length - 1);
        return;
      }
      if (k == '=') {
        _result = _eval(_expr);
        return;
      }
      if (k == '±') {
        if (_result != '0' && _expr.isEmpty) {
          _expr = _result.startsWith('-') ? _result.substring(1) : '-$_result';
        } else if (_expr.isNotEmpty) {
          _expr = _expr.startsWith('-') ? _expr.substring(1) : '-$_expr';
        }
        return;
      }
      _expr += k;
    });
  }

  String _eval(String raw) {
    try {
      var s =
          raw.replaceAll('×', '*').replaceAll('÷', '/').replaceAll('−', '-');
      if (s.isEmpty) return '0';
      for (final op in ['+', '-', '*', '/']) {
        if (!s.contains(op)) continue;
        final parts = <String>[];
        final buf = StringBuffer();
        for (var i = 0; i < s.length; i++) {
          final ch = s[i];
          if (ch == op && buf.isNotEmpty) {
            parts.add(buf.toString());
            buf.clear();
          } else {
            buf.write(ch);
          }
        }
        if (buf.isNotEmpty) parts.add(buf.toString());
        if (parts.length < 2) continue;
        double acc = double.parse(parts.first);
        for (var i = 1; i < parts.length; i++) {
          final b = double.parse(parts[i]);
          switch (op) {
            case '+':
              acc += b;
            case '-':
              acc -= b;
            case '*':
              acc *= b;
            case '/':
              if (b == 0) return '∞';
              acc /= b;
          }
        }
        return acc == acc.roundToDouble()
            ? acc.toInt().toString()
            : acc.toStringAsFixed(6).replaceAll(RegExp(r'\.?0+$'), '');
      }
      return double.parse(s).toString();
    } catch (_) {
      return 'Error';
    }
  }

  Widget _key(String label, {Color? bg, Color? fg, int flex = 1}) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Expanded(
      flex: flex,
      child: Padding(
        padding: const EdgeInsets.all(4),
        child: Material(
          color: bg ??
              (dark ? const Color(0xFF1A2332) : const Color(0xFF1E293B)),
          borderRadius: BorderRadius.circular(14),
          child: InkWell(
            onTap: () => _tap(label),
            borderRadius: BorderRadius.circular(14),
            child: SizedBox(
              height: 56,
              child: Center(
                child: Text(label,
                    style: TextStyle(
                      color: fg ?? Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w800,
                    )),
              ),
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    final dark = Theme.of(context).brightness == Brightness.dark;

    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 8),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: dark
                  ? const [Color(0xFF083344), Color(0xFF312E81)]
                  : const [Color(0xFF0F766E), Color(0xFF0E7490)],
            ),
            borderRadius: const BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Tools',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              TabBar(
                controller: _tabs,
                labelColor: Colors.white,
                unselectedLabelColor: Colors.white70,
                indicatorColor: const Color(0xFFFBBF24),
                tabs: const [
                  Tab(text: 'Study'),
                  Tab(text: 'Calculator'),
                ],
              ),
            ],
          ),
        ),
        Expanded(
          child: TabBarView(
            controller: _tabs,
            children: [
              StudyFeaturesScreen(
                  grade: widget.grade, subject: widget.subject),
              _calculator(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _calculator() {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text('Calculator',
            style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
        const SizedBox(height: 12),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: dark ? const Color(0xFF0B1220) : const Color(0xFF0F172A),
            borderRadius: BorderRadius.circular(18),
            border: dark
                ? Border.all(color: FourTheme.darkBorder)
                : null,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Text(_expr.isEmpty ? ' ' : _expr,
                  style: const TextStyle(
                      color: Color(0xFF94A3B8), fontSize: 18)),
              Text(_result,
                  style: const TextStyle(
                      color: Colors.white,
                      fontSize: 40,
                      fontWeight: FontWeight.w900)),
            ],
          ),
        ),
        const SizedBox(height: 12),
        Row(children: [
          _key('C', bg: const Color(0xFF334155)),
          _key('±', bg: const Color(0xFF334155)),
          _key('⌫', bg: const Color(0xFF334155)),
          _key('÷', bg: FourTheme.primary),
        ]),
        Row(children: [
          _key('7'),
          _key('8'),
          _key('9'),
          _key('×', bg: FourTheme.primary),
        ]),
        Row(children: [
          _key('4'),
          _key('5'),
          _key('6'),
          _key('−', bg: FourTheme.primary),
        ]),
        Row(children: [
          _key('1'),
          _key('2'),
          _key('3'),
          _key('+', bg: FourTheme.primary),
        ]),
        Row(children: [
          _key('0', flex: 2),
          _key('.'),
          _key('=', bg: const Color(0xFFFBBF24), fg: const Color(0xFF0F172A)),
        ]),
      ],
    );
  }
}
