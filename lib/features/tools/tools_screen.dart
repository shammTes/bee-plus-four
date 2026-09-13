import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/theme/four_theme.dart';

class ToolsScreen extends StatefulWidget {
  const ToolsScreen({super.key});

  @override
  State<ToolsScreen> createState() => _ToolsScreenState();
}

class _ToolsScreenState extends State<ToolsScreen> {
  String _expr = '';
  String _result = '0';

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
      var s = raw.replaceAll('×', '*').replaceAll('÷', '/').replaceAll('−', '-');
      if (s.isEmpty) return '0';
      // Support chained simple ops left-to-right for one operator family at a time
      final ops = ['+', '-', '*', '/'];
      for (final op in ops) {
        if (!s.contains(op)) continue;
        // avoid matching leading minus
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
              break;
            case '-':
              acc -= b;
              break;
            case '*':
              acc *= b;
              break;
            case '/':
              if (b == 0) return '∞';
              acc /= b;
              break;
          }
        }
        return acc == acc.roundToDouble()
            ? acc.toInt().toString()
            : acc.toStringAsFixed(6).replaceAll(RegExp(r'\.?0+\$'), '');
      }
      return double.parse(s).toString();
    } catch (_) {
      return 'Error';
    }
  }

  Widget _key(String label,
      {Color? bg, Color? fg, int flex = 1, double height = 58}) {
    return Expanded(
      flex: flex,
      child: Padding(
        padding: const EdgeInsets.all(5),
        child: Material(
          color: bg ?? const Color(0xFF1E293B),
          borderRadius: BorderRadius.circular(16),
          elevation: 2,
          child: InkWell(
            borderRadius: BorderRadius.circular(16),
            onTap: () => _tap(label),
            child: SizedBox(
              height: height,
              child: Center(
                child: Text(
                  label,
                  style: TextStyle(
                    color: fg ?? Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.w800,
                  ),
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
    final top = MediaQuery.paddingOf(context).top;
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
        ),
      ),
      child: ListView(
        padding: EdgeInsets.fromLTRB(16, top + 12, 16, 24),
        children: [
          const Text('Calculator',
              style: TextStyle(
                  color: Colors.white,
                  fontSize: 22,
                  fontWeight: FontWeight.w900)),
          const SizedBox(height: 16),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color(0xFF020617),
              borderRadius: BorderRadius.circular(24),
              border: Border.all(color: const Color(0xFF334155)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  _expr.isEmpty ? ' ' : _expr,
                  style: const TextStyle(
                    color: Color(0xFF94A3B8),
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  _result,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 42,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Row(children: [
            _key('C', bg: const Color(0xFF334155)),
            _key('±', bg: const Color(0xFF334155)),
            _key('⌫', bg: const Color(0xFF334155)),
            _key('÷', bg: FourTheme.primary, fg: Colors.white),
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
          const SizedBox(height: 20),
          FourTheme.glassPanel(
            child: const Text(
              'Tip: Use Practice + Coach for exam prep. Labs are under Home → Virtual labs.',
              style: TextStyle(color: FourTheme.ink, height: 1.4),
            ),
          ),
        ],
      ),
    );
  }
}
