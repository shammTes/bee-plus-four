// Offline mirror of one interactive web page: the entry HTML plus every asset it references, so it can
// be zipped into a .4web bundle and run with no network. Pure dart:io (also runs in `dart test` on a PC).
//
// What it follows: src/href/poster/data attributes, srcset, inline + linked CSS url(...)/@import, and
// string literals inside JS/JSON that look like relative asset paths ("img/a.png", './data/x.json').
// Cross-origin files referenced from HTML/CSS (CDN scripts, fonts) are stored under `_ext/<host>/…`
// and the reference is rewritten. Anything fetched at run time from computed URLs or APIs cannot be
// seen here; [MirrorResult.unresolved] lists what failed so the user is told the page may need a server.
import 'dart:async';
import 'dart:convert';
import 'dart:io';

class MirrorResult {
  MirrorResult(this.entry, this.files, this.unresolved, this.external);
  final String entry; // path of the start page inside the bundle
  final Map<String, int> files; // path → bytes
  final List<String> unresolved; // urls that 404'd / failed
  final Set<String> external; // hosts the page pulls code/data from at run time (best guess)
  int get totalBytes => files.values.fold(0, (a, b) => a + b);
}

class MirrorException implements Exception {
  MirrorException(this.message);
  final String message;
  @override
  String toString() => message;
}

class WebMirror {
  WebMirror({this.maxFiles = 1500, this.maxBytes = 150 << 20, HttpClient? client, this.onProgress})
    : _http = client ?? (HttpClient()..connectionTimeout = const Duration(seconds: 20)..userAgent = 'Mozilla/5.0 (Linux; Android 10) FourEncryptor/1.0');

  final int maxFiles, maxBytes;
  final HttpClient _http;
  final void Function(int files, int bytes, String current)? onProgress;

  static const _assetExt = r'(?:png|jpe?g|gif|webp|svg|bmp|ico|css|js|mjs|json|xml|txt|csv|html?|woff2?|ttf|otf|eot|mp3|ogg|wav|m4a|mp4|webm|vtt|glb|gltf|bin|wasm|atlas|fnt|obj|mtl|pdf)';
  static final _attr = RegExp(r'''\b(?:src|href|poster|data-src|data|background)\s*=\s*(?:"([^"]*)"|'([^']*)')''', caseSensitive: false);
  static final _srcset = RegExp(r'''\bsrcset\s*=\s*(?:"([^"]*)"|'([^']*)')''', caseSensitive: false);
  static final _cssUrl = RegExp(r'''url\(\s*(?:"([^"]*)"|'([^']*)'|([^)'"]*))\s*\)''', caseSensitive: false);
  static final _cssImport = RegExp(r'''@import\s+(?:"([^"]*)"|'([^']*)')''', caseSensitive: false);
  static final _jsLit = RegExp('''["'`]((?:\\.{1,2}/|/)?[A-Za-z0-9_\\-][A-Za-z0-9_\\-./%]*\\.$_assetExt)(?:\\?[^"'`]*)?["'`]''', caseSensitive: false);

  late Uri _root; // directory of the entry page; same-origin files under it keep their relative path
  final _files = <String, List<int>>{};
  final _done = <String>{};
  final _unresolved = <String>[];
  final _external = <String>{};
  var _bytes = 0;

  /// Downloads [entryUrl] and its assets. Returns the bundle in memory (path → bytes).
  Future<(MirrorResult, Map<String, List<int>>)> mirror(Uri entryUrl) async {
    _root = entryUrl.replace(query: '', fragment: '').removeFragment();
    final path = _root.path;
    final dir = path.endsWith('/') ? path : path.substring(0, path.lastIndexOf('/') + 1);
    _root = _root.replace(path: dir, query: null);
    final entryLocal = _localFor(entryUrl.removeFragment().replace(query: null), isEntry: true);
    final queue = <(Uri, String)>[(entryUrl.removeFragment(), 'html')];
    final optional = <String>{};
    while (queue.isNotEmpty) {
      final (url, kind) = queue.removeAt(0);
      final key = url.replace(query: url.query.isEmpty ? null : url.query).toString();
      if (!_done.add(key)) continue;
      if (_files.length >= maxFiles) throw MirrorException('more than $maxFiles files: page too big for an offline bundle');
      final res = await _get(url);
      if (res == null) {
        if (url == entryUrl.removeFragment()) throw MirrorException('could not download $url');
        if (!optional.contains(key)) _unresolved.add(url.toString()); // guesses from JS literals are optional
        continue;
      }
      var (bytes, ctype) = res;
      final local = url == entryUrl.removeFragment() ? entryLocal : _localFor(url);
      final k = _kindOf(local, ctype, kind);
      if (k == 'html' || k == 'css' || k == 'js') {
        final text = utf8.decode(bytes, allowMalformed: true);
        final found = <(Uri, String)>[];
        final guessed = <(Uri, String)>[];
        final rewritten = switch (k) {
          'html' => _scanHtml(text, url, local, found, guessed),
          'css' => _scanCss(text, url, local, found),
          _ => _scanJs(text, url, guessed),
        };
        if (rewritten != text) bytes = utf8.encode(rewritten);
        queue.addAll(found);
        for (final g in guessed) {
          final gk = g.$1.toString();
          if (!_done.contains(gk) && !queue.any((q) => q.$1 == g.$1)) {
            optional.add(gk);
            queue.add(g);
          }
        }
      }
      _files[local] = bytes;
      _bytes += bytes.length;
      if (_bytes > maxBytes) throw MirrorException('bundle larger than ${maxBytes >> 20} MB');
      onProgress?.call(_files.length, _bytes, local);
    }
    for (final u in _unresolved) {
      final h = Uri.tryParse(u)?.host ?? '';
      if (h.isNotEmpty && h != _root.host) _external.add(h);
    }
    return (MirrorResult(entryLocal, {for (final e in _files.entries) e.key: e.value.length}, _unresolved, _external), _files);
  }

  String _kindOf(String local, String ctype, String hint) {
    final l = local.toLowerCase();
    if (ctype.contains('html') || l.endsWith('.html') || l.endsWith('.htm')) return 'html';
    if (ctype.contains('css') || l.endsWith('.css')) return 'css';
    if (ctype.contains('javascript') || l.endsWith('.js') || l.endsWith('.mjs')) return 'js';
    if (ctype.contains('json') || l.endsWith('.json')) return 'js'; // scan JSON manifests for asset paths too
    return 'bin';
  }

  /// Bundle path for a URL: same origin under the entry folder → relative path; else `_ext/host/path`.
  String _localFor(Uri u, {bool isEntry = false}) {
    var p = Uri.decodeComponent(u.path);
    if (u.origin == _root.origin && p.startsWith(_root.path)) {
      p = p.substring(_root.path.length);
    } else {
      p = '_ext/${u.host}${p.startsWith('/') ? p : '/$p'}';
    }
    if (p.isEmpty || p.endsWith('/')) p = '${p}index.html';
    if (u.query.isNotEmpty && !isEntry) {
      final dot = p.lastIndexOf('.');
      final tag = u.query.hashCode.toUnsigned(32).toRadixString(16);
      p = dot > p.lastIndexOf('/') ? '${p.substring(0, dot)}_$tag${p.substring(dot)}' : '${p}_$tag';
    }
    // keep names short and safe for zip/Android file systems (Google-style hashed paths can be 1000+ chars)
    p = p.split('/').map((seg) {
      final clean = seg.replaceAll(RegExp(r'[\\:*?"<>|=,&]'), '_');
      if (clean.length <= 80) return clean;
      final dot = clean.lastIndexOf('.');
      final ext = dot > clean.length - 8 ? clean.substring(dot) : '';
      return '${clean.substring(0, 40)}_${clean.hashCode.toUnsigned(32).toRadixString(16)}$ext';
    }).join('/');
    return p.replaceAll('..', '_');
  }

  String _rel(String fromLocal, String toLocal) {
    final from = fromLocal.split('/')..removeLast();
    final to = toLocal.split('/');
    var i = 0;
    while (i < from.length && i < to.length - 1 && from[i] == to[i]) {
      i++;
    }
    return [...List.filled(from.length - i, '..'), ...to.sublist(i)].join('/');
  }

  Uri? _resolve(Uri base, String raw) {
    final s = raw.trim();
    if (s.isEmpty || s.startsWith('#') || s.startsWith('data:') || s.startsWith('blob:') || s.startsWith('javascript:') || s.startsWith('mailto:') || s.startsWith('tel:') || s.contains('{{') || s.contains(r'${')) return null;
    try {
      final u = base.resolve(s.replaceAll('&amp;', '&'));
      if (u.scheme != 'http' && u.scheme != 'https') return null;
      return u.removeFragment();
    } catch (_) {
      return null;
    }
  }

  /// Same-origin anything, or cross-origin when it is a static asset (script/style/font/image).
  bool _wanted(Uri u, String tagHint) {
    if (u.origin == _root.origin) return true;
    final l = u.path.toLowerCase();
    return RegExp('\\.$_assetExt\$').hasMatch(l) && !l.endsWith('.html') && !l.endsWith('.htm') || tagHint == 'script' || tagHint == 'style';
  }

  static final _scriptBlock = RegExp(r'(<script\b[^>]*>)([\s\S]*?)(</script\s*>)', caseSensitive: false);

  String _scanHtml(String html, Uri base, String local, List<(Uri, String)> out, List<(Uri, String)> guessed) {
    // markup outside inline scripts is rewritten; inline script text is only scanned for asset-looking literals
    final buf = StringBuffer();
    var last = 0;
    for (final m in _scriptBlock.allMatches(html)) {
      buf.write(_scanMarkup(html.substring(last, m.start) + m.group(1)!, base, local, out));
      _scanJs(m.group(2)!, base, guessed);
      buf..write(m.group(2))..write(m.group(3));
      last = m.end;
    }
    buf.write(_scanMarkup(html.substring(last), base, local, out));
    return buf.toString();
  }

  String _scanMarkup(String html, Uri base, String local, List<(Uri, String)> out) {
    // <base href> changes resolution
    final b = RegExp(r'''<base\s+href\s*=\s*["']([^"']+)["']''', caseSensitive: false).firstMatch(html);
    if (b != null) base = _resolve(base, b.group(1)!) ?? base;
    var s = html.replaceAllMapped(_attr, (m) {
      final raw = m.group(1) ?? m.group(2)!;
      final u = _resolve(base, raw);
      final before = html.substring((m.start - 200).clamp(0, m.start), m.start).toLowerCase();
      final tag = before.lastIndexOf('<script') > before.lastIndexOf('>') ? 'script' : (before.lastIndexOf('<link') > before.lastIndexOf('>') ? 'style' : '');
      if (u == null) return m[0]!;
      final isAnchor = before.lastIndexOf('<a ') > before.lastIndexOf('>');
      if (isAnchor && u.origin != _root.origin) return m[0]!; // outbound link: left as is (blocked in 4)
      if (!_wanted(u, tag)) {
        if (tag.isNotEmpty) _external.add(u.host);
        return m[0]!;
      }
      final target = _localFor(u);
      out.add((u, _kindOf(target, '', 'bin')));
      final q = m[0]!.contains('"') ? '"' : "'";
      final attr = m[0]!.substring(0, m[0]!.indexOf('=')).trim();
      return '$attr=$q${_rel(local, target)}$q';
    });
    s = s.replaceAllMapped(_srcset, (m) {
      final raw = m.group(1) ?? m.group(2)!;
      final parts = <String>[];
      for (final c in raw.split(',')) {
        final bits = c.trim().split(RegExp(r'\s+'));
        final u = bits.isEmpty ? null : _resolve(base, bits.first);
        if (u == null || !_wanted(u, '')) {
          parts.add(c.trim());
          continue;
        }
        final t = _localFor(u);
        out.add((u, 'bin'));
        parts.add([_rel(local, t), ...bits.skip(1)].join(' '));
      }
      return 'srcset="${parts.join(', ')}"';
    });
    // inline <style> and style="" attributes
    return _scanCss(s, base, local, out);
  }

  String _scanCss(String css, Uri base, String local, List<(Uri, String)> out) {
    String fix(Match m, String Function(String) wrap) {
      final raw = m.group(1) ?? m.group(2) ?? m.group(3) ?? '';
      final u = _resolve(base, raw);
      if (u == null || !_wanted(u, 'style')) return m[0]!;
      final t = _localFor(u);
      out.add((u, t.endsWith('.css') ? 'css' : 'bin'));
      return wrap(_rel(local, t));
    }

    return css.replaceAllMapped(_cssImport, (m) => fix(m, (r) => '@import "$r"')).replaceAllMapped(_cssUrl, (m) => fix(m, (r) => 'url("$r")'));
  }

  /// JS is not rewritten (too risky); relative literals resolve against the page, so files are saved where the page expects them.
  String _scanJs(String js, Uri base, List<(Uri, String)> out) {
    for (final m in _jsLit.allMatches(js)) {
      final raw = m.group(1)!;
      // relative paths in JS resolve against the document, not the script file
      for (final b in {base, _root}) {
        final u = _resolve(b, raw);
        if (u != null && u.origin == _root.origin) out.add((u, _kindOf(u.path, '', 'bin')));
      }
    }
    return js;
  }

  Future<(List<int>, String)?> _get(Uri u, [int redirects = 0]) async {
    try {
      final rq = await _http.getUrl(u);
      rq.followRedirects = true;
      final rs = await rq.close().timeout(const Duration(seconds: 60));
      if (rs.statusCode != 200) {
        await rs.drain<void>();
        return null;
      }
      final b = BytesBuilder(copy: false);
      await for (final c in rs.timeout(const Duration(seconds: 60))) {
        b.add(c);
        if (b.length > maxBytes) throw MirrorException('file too large: $u');
      }
      return (b.takeBytes(), rs.headers.contentType?.mimeType ?? '');
    } on MirrorException {
      rethrow;
    } catch (_) {
      return null;
    }
  }

  /// Writes the mirrored files under [dir] (later zipped natively).
  static Future<void> writeTo(Directory dir, Map<String, List<int>> files) async {
    for (final e in files.entries) {
      final f = File('${dir.path}/${e.key}');
      await f.parent.create(recursive: true);
      await f.writeAsBytes(e.value);
    }
  }

  void close() => _http.close(force: true);
}
