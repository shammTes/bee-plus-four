import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:webview_flutter/webview_flutter.dart';

/// Offline PhET virtual lab — loads HTML from assets/content/phet/.
class PhetSimPage extends StatefulWidget {
  const PhetSimPage({
    super.key,
    required this.title,
    required this.assetPath,
  });

  final String title;
  final String assetPath;

  @override
  State<PhetSimPage> createState() => _PhetSimPageState();
}

class _PhetSimPageState extends State<PhetSimPage> {
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
        ..setBackgroundColor(const Color(0xFF0F172A))
        ..setNavigationDelegate(
          NavigationDelegate(
            onPageFinished: (_) {
              if (mounted) setState(() => _loading = false);
            },
            onWebResourceError: (e) {
              if (mounted) {
                setState(() {
                  _error = e.description;
                  _loading = false;
                });
              }
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
        _error =
            'Lab file not embedded offline.\n${widget.assetPath}\n\nShare the PhET Drive pack and rebuild so CI unpacks HTML into assets/content/phet/.';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title, maxLines: 1, overflow: TextOverflow.ellipsis),
        actions: [
          if (_controller != null)
            IconButton(
              icon: const Icon(Icons.refresh),
              onPressed: () => _controller?.reload(),
            ),
        ],
      ),
      body: _error != null
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Text(_error!, textAlign: TextAlign.center, style: const TextStyle(height: 1.4)),
              ),
            )
          : Stack(
              children: [
                if (_controller != null) WebViewWidget(controller: _controller!),
                if (_loading) const Center(child: CircularProgressIndicator()),
              ],
            ),
    );
  }
}

class PhetCatalogPage extends StatefulWidget {
  const PhetCatalogPage({super.key});

  @override
  State<PhetCatalogPage> createState() => _PhetCatalogPageState();
}

class _PhetCatalogPageState extends State<PhetCatalogPage> {
  List<Map<String, String>> items = const [];
  bool loading = true;

  static const _fallback = [
    ('Forces & Motion', 'forces-and-motion-basics_all.html'),
    ('Build an Atom', 'build-an-atom_all.html'),
    ('Balancing Chemical Equations', 'balancing-chemical-equations_all.html'),
    ('Circuit Construction Kit DC', 'circuit-construction-kit-dc_all.html'),
    ('Energy Skate Park', 'energy-skate-park-basics_all.html'),
    ('Pendulum Lab', 'pendulum-lab_all.html'),
    ('Projectile Motion', 'projectile-motion_all.html'),
    ('Wave on a String', 'wave-on-a-string_all.html'),
    ('States of Matter', 'states-of-matter-basics_all.html'),
    ('Acid-Base Solutions', 'acid-base-solutions_all.html'),
    ('Concentration', 'concentration_all.html'),
    ('Molecule Shapes', 'molecule-shapes-basics_all.html'),
    ("Faraday's Law", 'faradays-law_all.html'),
    ("Ohm's Law", 'ohms-law_all.html'),
    ("Hooke's Law", 'hookes-law_all.html'),
    ('Buoyancy', 'buoyancy_all.html'),
    ('Density', 'density_all.html'),
    ('Graphing Lines', 'graphing-lines_all.html'),
    ('Area Builder', 'area-builder_all.html'),
    ('Natural Selection', 'natural-selection_all.html'),
  ];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final list = <Map<String, String>>[];
    try {
      final raw = await rootBundle.loadString('assets/content/phet_catalog.json');
      final decoded = jsonDecode(raw);
      if (decoded is Map && decoded['sims'] is List) {
        for (final e in decoded['sims'] as List) {
          if (e is Map) {
            final title = '${e['title'] ?? e['name'] ?? ''}';
            final file = '${e['file'] ?? e['html'] ?? ''}';
            if (title.isNotEmpty && file.isNotEmpty) {
              list.add({'title': title, 'file': file});
            }
          }
        }
      } else if (decoded is List) {
        for (final e in decoded) {
          if (e is Map) {
            list.add({
              'title': '${e['title'] ?? e['name'] ?? 'Lab'}',
              'file': '${e['file'] ?? e['html'] ?? ''}',
            });
          }
        }
      }
    } catch (_) {}
    if (list.isEmpty) {
      for (final e in _fallback) {
        list.add({'title': e.$1, 'file': e.$2});
      }
    }
    if (!mounted) return;
    setState(() {
      items = list;
      loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Virtual lab (PhET offline)')),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: items.length,
              separatorBuilder: (_, __) => const SizedBox(height: 8),
              itemBuilder: (context, i) {
                final it = items[i];
                final path = 'assets/content/phet/${it['file']}';
                return Card(
                  child: ListTile(
                    leading: const CircleAvatar(child: Icon(Icons.science)),
                    title: Text(it['title'] ?? ''),
                    subtitle: const Text('Offline · no internet'),
                    trailing: const Icon(Icons.play_arrow),
                    onTap: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => PhetSimPage(
                            title: it['title'] ?? 'Lab',
                            assetPath: path,
                          ),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
    );
  }
}
