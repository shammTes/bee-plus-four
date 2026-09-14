import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../core/theme/four_theme.dart';
import 'phet_sim_page.dart';

/// Offline PhET HTML5 labs for Physics · Chemistry · Biology · Math · Earth.
class VirtualLabScreen extends StatefulWidget {
  const VirtualLabScreen({super.key});

  @override
  State<VirtualLabScreen> createState() => _VirtualLabScreenState();
}

class _VirtualLabScreenState extends State<VirtualLabScreen>
    with SingleTickerProviderStateMixin {
  TabController? _tabs;
  List<_PhetSubject> subjects = [];
  bool loading = true;
  String? loadError;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    _tabs?.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    try {
      final raw =
          await rootBundle.loadString('assets/content/phet_catalog.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final list = <_PhetSubject>[];
      for (final s in (map['subjects'] as List? ?? const [])) {
        final m = Map<String, dynamic>.from(s as Map);
        final sims = <_PhetSim>[];
        for (final sim in (m['sims'] as List? ?? const [])) {
          final sm = Map<String, dynamic>.from(sim as Map);
          final asset = '${sm['asset'] ?? ''}';
          if (asset.isEmpty) continue;
          sims.add(_PhetSim(
            id: '${sm['id']}',
            title: '${sm['title']}',
            assetPath: asset,
          ));
        }
        if (sims.isEmpty) continue;
        list.add(_PhetSubject(
          id: '${m['id']}',
          label: '${m['label']}',
          sims: sims,
        ));
      }
      if (!mounted) return;
      _tabs?.dispose();
      _tabs = TabController(length: list.length, vsync: this);
      setState(() {
        subjects = list;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        loading = false;
        loadError = '$e';
      });
    }
  }

  void _open(_PhetSim sim) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) =>
            PhetSimPage(title: sim.title, assetPath: sim.assetPath),
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
                  : const [Color(0xFF0E7490), Color(0xFF4F46E5)],
            ),
            borderRadius: const BorderRadius.only(
              bottomLeft: Radius.circular(24),
              bottomRight: Radius.circular(24),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Virtual labs',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.w900)),
              Text(
                loading
                    ? 'Loading PhET…'
                    : 'Offline PhET HTML5 · ${subjects.fold<int>(0, (a, s) => a + s.sims.length)} sims',
                style: const TextStyle(color: Color(0xFFCCFBF1), fontSize: 13),
              ),
              const SizedBox(height: 2),
              const Text(
                'Fully offline · no internet required',
                style: TextStyle(color: Color(0xFF99F6E4), fontSize: 11),
              ),
              if (_tabs != null && subjects.isNotEmpty)
                TabBar(
                  controller: _tabs,
                  isScrollable: true,
                  labelColor: Colors.white,
                  unselectedLabelColor: Colors.white70,
                  indicatorColor: const Color(0xFFFBBF24),
                  tabs: subjects.map((s) => Tab(text: s.label)).toList(),
                ),
            ],
          ),
        ),
        if (loading)
          const Expanded(child: Center(child: CircularProgressIndicator()))
        else if (loadError != null)
          Expanded(
            child: Center(
              child: Text('Could not load PhET catalog.\n$loadError',
                  textAlign: TextAlign.center),
            ),
          )
        else if (_tabs == null)
          const Expanded(child: Center(child: Text('No labs')))
        else
          Expanded(
            child: TabBarView(
              controller: _tabs,
              children: subjects.map((subj) {
                return ListView.builder(
                  padding: const EdgeInsets.all(12),
                  itemCount: subj.sims.length + 1,
                  itemBuilder: (ctx, i) {
                    if (i == 0) {
                      return Padding(
                        padding: const EdgeInsets.fromLTRB(4, 4, 4, 12),
                        child: Text(
                          '${subj.sims.length} offline simulations · tap to open',
                          style: TextStyle(
                            fontWeight: FontWeight.w700,
                            color: dark
                                ? FourTheme.darkMuted
                                : FourTheme.muted,
                          ),
                        ),
                      );
                    }
                    final sim = subj.sims[i - 1];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor:
                              _colorFor(subj.id).withOpacity(0.15),
                          child: Icon(Icons.science,
                              color: _colorFor(subj.id), size: 20),
                        ),
                        title: Text(sim.title,
                            style:
                                const TextStyle(fontWeight: FontWeight.w800)),
                        subtitle: const Text('Offline PhET HTML5'),
                        trailing: const Icon(Icons.play_circle_outline),
                        onTap: () => _open(sim),
                      ),
                    );
                  },
                );
              }).toList(),
            ),
          ),
      ],
    );
  }

  Color _colorFor(String id) {
    switch (id) {
      case 'PHYSICS':
        return const Color(0xFF06B6D4);
      case 'CHEMISTRY':
        return const Color(0xFFF59E0B);
      case 'BIOLOGY':
        return const Color(0xFF10B981);
      case 'MATH':
        return const Color(0xFF8B5CF6);
      default:
        return const Color(0xFF0EA5E9);
    }
  }
}

class _PhetSubject {
  _PhetSubject({required this.id, required this.label, required this.sims});
  final String id;
  final String label;
  final List<_PhetSim> sims;
}

class _PhetSim {
  _PhetSim({
    required this.id,
    required this.title,
    required this.assetPath,
  });
  final String id;
  final String title;
  final String assetPath;
}
