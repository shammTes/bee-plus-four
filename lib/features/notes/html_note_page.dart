import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

class HtmlNotePage extends StatefulWidget {
  const HtmlNotePage({
    super.key,
    required this.title,
    required this.assetPath,
    this.subtitle = '',
    this.embedded = false,
  });

  final String title;
  final String assetPath;
  final String subtitle;
  final bool embedded;

  @override
  State<HtmlNotePage> createState() => _HtmlNotePageState();
}

class _HtmlNotePageState extends State<HtmlNotePage> {
  WebViewController? _controller;
  String? _error;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<void> _init() async {
    try {
      await rootBundle.load(widget.assetPath);
      final c = WebViewController()
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..setBackgroundColor(const Color(0xFFF3EAD8))
        ..enableZoom(true)
        ..setNavigationDelegate(
          NavigationDelegate(
            onPageFinished: (_) {
              if (mounted) setState(() => _loading = false);
            },
          ),
        );
      await c.loadFlutterAsset(widget.assetPath);
      if (!mounted) return;
      setState(() {
        _controller = c;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'Note HTML missing:\n${widget.assetPath}\n\n$e';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final body = _error != null
        ? Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Text(_error!, textAlign: TextAlign.center),
            ),
          )
        : Stack(
            children: [
              if (_controller != null) WebViewWidget(controller: _controller!),
              if (_loading) const Center(child: CircularProgressIndicator()),
            ],
          );
    if (widget.embedded) {
      return ColoredBox(color: const Color(0xFFF3EAD8), child: body);
    }
    return Scaffold(
      backgroundColor: const Color(0xFFF3EAD8),
      appBar: AppBar(
        title: Text(widget.title,
            maxLines: 1, overflow: TextOverflow.ellipsis),
      ),
      body: body,
    );
  }
}

class HtmlNotesIndex {
  HtmlNotesIndex._();
  static Map<String, String>? _map;

  static Future<String?> assetFor(String grade, String subject, int unit) async {
    _map ??= await _load();
    final g = grade.toUpperCase();
    final s = subject.toUpperCase();
    if (_map!.containsKey('$g|$s|$unit')) return _map!['$g|$s|$unit'];
    if (_map!.containsKey('$g|$s|0')) return _map!['$g|$s|0'];
    final names = {
      'MATH': 'Mathematics',
      'BIOLOGY': 'Biology',
      'CHEMISTRY': 'Chemistry',
      'PHYSICS': 'Physics',
      'GEOGRAPHY': 'Geography',
      'HISTORY': 'History',
      'AGRICULTURE': 'Agriculture',
      'BUSINESS_ECONOMICS': 'Business_Economics',
    };
    final nice = names[s] ?? s;
    final gradeNum = g.replaceAll('G', 'Grade');
    final guesses = [
      'assets/content/interactive_notes/${gradeNum}_${nice}_Interactive_Notes.html',
      'assets/content/interactive_notes/${g}_${s}_Interactive_Notes.html',
    ];
    for (final guess in guesses) {
      try {
        await rootBundle.load(guess);
        return guess;
      } catch (_) {}
    }
    return null;
  }

  static Future<Map<String, String>> _load() async {
    try {
      final raw = await rootBundle
          .loadString('assets/content/interactive_notes/index.json');
      final j = jsonDecode(raw);
      final map = <String, String>{};
      final list = (j is Map ? j['notes'] : j) as List? ?? const [];
      for (final e in list) {
        if (e is! Map) continue;
        final g = '${e['grade']}'.toUpperCase();
        final s = '${e['subject']}'.toUpperCase();
        final u = (e['unit_number'] as num?)?.toInt() ?? 0;
        final path = '${e['html_asset'] ?? ''}';
        if (path.isNotEmpty) map['$g|$s|$u'] = path;
      }
      return map;
    } catch (_) {
      return {};
    }
  }
}
