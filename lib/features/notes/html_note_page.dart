import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// Offline HTML notes. Inlines KaTeX so math renders with no network.
class HtmlNotePage extends StatefulWidget {
  const HtmlNotePage({
    super.key,
    required this.title,
    required this.assetPath,
    this.subtitle = '',
    this.embedded = false,
    this.anchor = '',
  });

  final String title;
  final String assetPath;
  final String subtitle;
  final bool embedded;
  final String anchor;

  @override
  State<HtmlNotePage> createState() => _HtmlNotePageState();
}

class _HtmlNotePageState extends State<HtmlNotePage> {
  WebViewController? _controller;
  String? _error;
  bool _loading = true;
  static String? _injectCache;
  static final Map<String, String> _htmlCache = {};

  @override
  void initState() {
    super.initState();
    _init();
  }

  Future<String> _assetOrEmpty(String path) async {
    try {
      return await rootBundle.loadString(path);
    } catch (_) {
      return '';
    }
  }

  Future<String> _fontFace(String family, String file,
      {String style = 'normal', String weight = 'normal'}) async {
    try {
      final data = await rootBundle.load('assets/content/vendor/katex/fonts/$file');
      final b64 = base64Encode(data.buffer.asUint8List());
      return "@font-face{font-family:'$family';src:url(data:font/woff2;base64,$b64) format('woff2');font-weight:$weight;font-style:$style;font-display:swap;}";
    } catch (_) {
      return '';
    }
  }

  Future<String> _buildInject() async {
    if (_injectCache != null) return _injectCache!;
    final katexCss = await _assetOrEmpty('assets/content/vendor/katex/katex.min.css');
    final katexJs = await _assetOrEmpty('assets/content/vendor/katex/katex.min.js');
    final autoJs = await _assetOrEmpty('assets/content/vendor/katex/auto-render.min.js');
    final faces = StringBuffer();
    faces.write(await _fontFace('KaTeX_Main', 'KaTeX_Main-Regular.woff2'));
    faces.write(await _fontFace('KaTeX_Main', 'KaTeX_Main-Bold.woff2', weight: 'bold'));
    faces.write(await _fontFace('KaTeX_Math', 'KaTeX_Math-Italic.woff2', style: 'italic'));
    faces.write(await _fontFace('KaTeX_Math', 'KaTeX_Math-BoldItalic.woff2',
        style: 'italic', weight: 'bold'));
    faces.write(await _fontFace('KaTeX_Size1', 'KaTeX_Size1-Regular.woff2'));
    faces.write(await _fontFace('KaTeX_Size2', 'KaTeX_Size2-Regular.woff2'));
    faces.write(await _fontFace('KaTeX_Size4', 'KaTeX_Size4-Regular.woff2'));
    faces.write(await _fontFace('KaTeX_AMS', 'KaTeX_AMS-Regular.woff2'));
    const fallbackCss = '''
      html,body{font-family:Georgia,"Noto Serif","Times New Roman",serif !important;}
      h1,h2,h3,h4,.kicker,nav.bar a,summary{font-family:system-ui,-apple-system,"Segoe UI",sans-serif !important;}
      .hand,.sticky{font-family:"Segoe Script","Comic Sans MS",cursive !important;}
      .katex-display{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;}
      [id^="u"],section[id]{scroll-margin-top:12px;}
    ''';
    _injectCache = '''
<style>${faces.toString()}$katexCss$fallbackCss</style>
<script>$katexJs</script>
<script>$autoJs</script>
<script>
function fourRenderMath(){
  try{
    if(window.renderMathInElement){
      renderMathInElement(document.body,{
        delimiters:[
          {left:'\\$\\$',right:'\\$\\$',display:true},
          {left:'\\$',right:'\\$',display:false},
          {left:'\\\\(',right:'\\\\)',display:false},
          {left:'\\\\[',right:'\\\\]',display:true}
        ],
        throwOnError:false,
        strict:false
      });
    }
  }catch(e){}
}
function fourJump(id){
  if(!id) return;
  var el = document.getElementById(id);
  if(el){ el.scrollIntoView({behavior:'instant', block:'start'}); }
}
document.addEventListener('DOMContentLoaded', fourRenderMath);
window.addEventListener('load', fourRenderMath);
</script>
''';
    return _injectCache!;
  }

  Future<String> _offlineHtml(String raw) async {
    var html = raw;
    html = html.replaceAll(
      RegExp(r'<link[^>]+fonts\\.googleapis\\.com[^>]*>', caseSensitive: false),
      '',
    );
    html = html.replaceAll(
      RegExp(r'<link[^>]+katex[^>]*>', caseSensitive: false),
      '',
    );
    html = html.replaceAll(
      RegExp(r'<script[^>]+katex[^>]*></script>', caseSensitive: false),
      '',
    );
    html = html.replaceAll(
      RegExp(r'<script[^>]+auto-render[\\s\\S]*?</script>', caseSensitive: false),
      '',
    );
    final inject = await _buildInject();
    if (html.contains('</head>')) {
      html = html.replaceFirst('</head>', '$inject</head>');
    } else {
      html = inject + html;
    }
    if (!html.toLowerCase().contains('charset')) {
      html = html.replaceFirst('<head>', '<head><meta charset="UTF-8">');
    }
    return html;
  }

  Future<void> _jump(WebViewController c) async {
    final id = widget.anchor.trim();
    if (id.isEmpty) return;
    final safe = id.replaceAll(RegExp(r"[^A-Za-z0-9_-]"), '');
    await c.runJavaScript(
      "fourJump('$safe'); setTimeout(function(){ fourJump('$safe'); }, 80); setTimeout(function(){ fourJump('$safe'); fourRenderMath(); }, 240);",
    );
  }

  Future<void> _init() async {
    try {
      final cached = _htmlCache[widget.assetPath];
      final html = cached ??
          await _offlineHtml(await rootBundle.loadString(widget.assetPath));
      _htmlCache[widget.assetPath] = html;
      final c = WebViewController()
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..setBackgroundColor(const Color(0xFFF3EAD8))
        ..enableZoom(true)
        ..setNavigationDelegate(
          NavigationDelegate(
            onPageFinished: (_) {
              _jump(c);
              if (mounted) setState(() => _loading = false);
            },
          ),
        );
      await c.loadHtmlString(html);
      if (!mounted) return;
      setState(() {
        _controller = c;
        _loading = false;
      });
      await _jump(c);
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'Could not open notes:\\n${widget.assetPath}\\n$e';
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
        title: Text(widget.title, maxLines: 1, overflow: TextOverflow.ellipsis),
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
    final gradeWord = 'Grade${g.replaceAll('G', '')}';
    final guesses = [
      'assets/content/interactive_notes/${gradeWord}_${nice}_Interactive_Notes.html',
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
