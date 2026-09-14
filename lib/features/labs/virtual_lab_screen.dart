import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../core/theme/four_theme.dart';

/// Offline virtual lab — interactive mini simulations + guided demos.
class VirtualLabScreen extends StatefulWidget {
  const VirtualLabScreen({super.key});

  @override
  State<VirtualLabScreen> createState() => _VirtualLabScreenState();
}

class _VirtualLabScreenState extends State<VirtualLabScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabs;

  @override
  void initState() {
    super.initState();
    _tabs = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabs.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final top = MediaQuery.paddingOf(context).top;
    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: EdgeInsets.fromLTRB(16, top + 10, 16, 8),
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [Color(0xFF0284C7), Color(0xFF0369A1)],
            ),
            borderRadius: BorderRadius.only(
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
              const Text('Interactive demos · move the sliders',
                  style:
                      TextStyle(color: Color(0xFFBAE6FD), fontSize: 13)),
              const SizedBox(height: 8),
              TabBar(
                controller: _tabs,
                labelColor: Colors.white,
                unselectedLabelColor: Colors.white70,
                indicatorColor: const Color(0xFFFBBF24),
                tabs: const [
                  Tab(text: 'Physics'),
                  Tab(text: 'Chemistry'),
                  Tab(text: 'Biology'),
                ],
              ),
            ],
          ),
        ),
        Expanded(
          child: TabBarView(
            controller: _tabs,
            children: const [
              _PhysicsLabs(),
              _ChemistryLabs(),
              _BiologyLabs(),
            ],
          ),
        ),
      ],
    );
  }
}

class _PhysicsLabs extends StatefulWidget {
  const _PhysicsLabs();
  @override
  State<_PhysicsLabs> createState() => _PhysicsLabsState();
}

class _PhysicsLabsState extends State<_PhysicsLabs> {
  double depthM = 2;
  double density = 1000; // kg/m³ water

  @override
  Widget build(BuildContext context) {
    final g = 9.8;
    final pressure = density * g * depthM; // Pa
    final kPa = pressure / 1000;

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _DemoCard(
          title: 'Hydrostatic pressure',
          subtitle: 'P = ρ g h  · drag depth',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Depth: ${depthM.toStringAsFixed(1)} m',
                  style: const TextStyle(fontWeight: FontWeight.w800)),
              Slider(
                value: depthM,
                min: 0.5,
                max: 20,
                divisions: 39,
                label: '${depthM.toStringAsFixed(1)} m',
                onChanged: (v) => setState(() => depthM = v),
              ),
              Text('Fluid density: ${density.round()} kg/m³',
                  style: const TextStyle(fontWeight: FontWeight.w800)),
              Slider(
                value: density,
                min: 700,
                max: 13600,
                divisions: 50,
                label: density.round().toString(),
                onChanged: (v) => setState(() => density = v),
              ),
              const SizedBox(height: 8),
              // Visual column of fluid
              Container(
                height: 120,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: const Color(0xFF0284C7)),
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      const Color(0xFFBAE6FD),
                      Color.lerp(const Color(0xFF0284C7), const Color(0xFF0F172A),
                          (depthM / 20).clamp(0, 1))!,
                    ],
                  ),
                ),
                alignment: Alignment.center,
                child: Text(
                  '${kPa.toStringAsFixed(1)} kPa\n(${pressure.toStringAsFixed(0)} Pa)',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      fontSize: 16,
                      shadows: [Shadow(blurRadius: 4, color: Colors.black54)]),
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'Deeper or denser fluid → higher pressure. '
                'This is the same idea as Unit: Fluid Mechanics.',
                style: TextStyle(color: FourTheme.muted, height: 1.35),
              ),
            ],
          ),
        ),
        _DemoCard(
          title: 'Ohm’s law circuit',
          subtitle: 'V = I R',
          child: _OhmDemo(),
        ),
      ],
    );
  }
}

class _OhmDemo extends StatefulWidget {
  @override
  State<_OhmDemo> createState() => _OhmDemoState();
}

class _OhmDemoState extends State<_OhmDemo> {
  double volts = 12;
  double ohms = 6;
  @override
  Widget build(BuildContext context) {
    final amps = ohms == 0 ? 0.0 : volts / ohms;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Voltage: ${volts.toStringAsFixed(1)} V',
            style: const TextStyle(fontWeight: FontWeight.w800)),
        Slider(
            value: volts,
            min: 1,
            max: 24,
            onChanged: (v) => setState(() => volts = v)),
        Text('Resistance: ${ohms.toStringAsFixed(1)} Ω',
            style: const TextStyle(fontWeight: FontWeight.w800)),
        Slider(
            value: ohms,
            min: 1,
            max: 20,
            onChanged: (v) => setState(() => ohms = v)),
        Text('Current I = ${amps.toStringAsFixed(2)} A',
            style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w900,
                color: Color(0xFF0284C7))),
        const Text('Higher resistance → smaller current for the same voltage.',
            style: TextStyle(color: FourTheme.muted)),
      ],
    );
  }
}

class _ChemistryLabs extends StatefulWidget {
  const _ChemistryLabs();
  @override
  State<_ChemistryLabs> createState() => _ChemistryLabsState();
}

class _ChemistryLabsState extends State<_ChemistryLabs> {
  double ph = 7;

  Color _phColor(double p) {
    if (p < 3) return const Color(0xFFDC2626);
    if (p < 6) return const Color(0xFFF97316);
    if (p < 8) return const Color(0xFF22C55E);
    if (p < 11) return const Color(0xFF3B82F6);
    return const Color(0xFF7C3AED);
  }

  String _label(double p) {
    if (p < 7) return 'Acidic';
    if (p > 7) return 'Basic (alkaline)';
    return 'Neutral';
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _DemoCard(
          title: 'pH scale',
          subtitle: 'Acids · neutral · bases',
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('pH = ${ph.toStringAsFixed(1)}  ·  ${_label(ph)}',
                  style: const TextStyle(fontWeight: FontWeight.w900)),
              Slider(
                value: ph,
                min: 0,
                max: 14,
                divisions: 28,
                activeColor: _phColor(ph),
                onChanged: (v) => setState(() => ph = v),
              ),
              Container(
                height: 48,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  gradient: const LinearGradient(colors: [
                    Color(0xFFDC2626),
                    Color(0xFFFBBF24),
                    Color(0xFF22C55E),
                    Color(0xFF3B82F6),
                    Color(0xFF7C3AED),
                  ]),
                ),
                child: Align(
                  alignment: Alignment((ph / 7) - 1, 0),
                  child: Container(
                    width: 6,
                    height: 48,
                    color: Colors.white,
                  ),
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'pH < 7 acid, pH = 7 neutral, pH > 7 base. '
                'Each unit is a 10× change in [H⁺].',
                style: TextStyle(color: FourTheme.muted, height: 1.35),
              ),
            ],
          ),
        ),
        _DemoCard(
          title: 'Safety first',
          subtitle: 'Real lab rules',
          child: const Text(
            '• Wear eye protection with acids/bases\n'
            '• Never taste chemicals\n'
            '• Add acid to water, not water to concentrated acid\n'
            '• Report spills to the teacher',
            style: TextStyle(height: 1.45, fontWeight: FontWeight.w600),
          ),
        ),
      ],
    );
  }
}

class _BiologyLabs extends StatefulWidget {
  const _BiologyLabs();
  @override
  State<_BiologyLabs> createState() => _BiologyLabsState();
}

class _BiologyLabsState extends State<_BiologyLabs>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulse;
  double bpm = 72;

  @override
  void initState() {
    super.initState();
    _pulse = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: (60000 / bpm).round()),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _pulse.dispose();
    super.dispose();
  }

  void _setBpm(double v) {
    setState(() {
      bpm = v;
      _pulse.duration = Duration(milliseconds: (60000 / bpm).round());
      if (!_pulse.isAnimating) _pulse.repeat(reverse: true);
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _DemoCard(
          title: 'Heart rate model',
          subtitle: 'Pulse animation · rest vs exercise',
          child: Column(
            children: [
              AnimatedBuilder(
                animation: _pulse,
                builder: (context, _) {
                  final s = 0.85 + 0.15 * _pulse.value;
                  return Transform.scale(
                    scale: s,
                    child: const Icon(Icons.favorite,
                        size: 88, color: Color(0xFFDC2626)),
                  );
                },
              ),
              Text('${bpm.round()} bpm',
                  style: const TextStyle(
                      fontSize: 22, fontWeight: FontWeight.w900)),
              Slider(
                value: bpm,
                min: 50,
                max: 160,
                divisions: 22,
                label: bpm.round().toString(),
                onChanged: _setBpm,
              ),
              const Text(
                'Exercise raises heart rate so muscles get more oxygen. '
                'Resting adult rate is often ~60–100 bpm.',
                style: TextStyle(color: FourTheme.muted, height: 1.35),
              ),
            ],
          ),
        ),
        _DemoCard(
          title: 'Cell basics reminder',
          subtitle: 'Demo note',
          child: const Text(
            'Nucleus holds DNA · mitochondria release energy · '
            'membrane controls what enters and leaves. '
            'Use Notes → Biology units for full curriculum depth.',
            style: TextStyle(height: 1.4, fontWeight: FontWeight.w600),
          ),
        ),
      ],
    );
  }
}

class _DemoCard extends StatelessWidget {
  const _DemoCard({
    required this.title,
    required this.subtitle,
    required this.child,
  });
  final String title;
  final String subtitle;
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: const Color(0xFFE2E8F0)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style:
                  const TextStyle(fontWeight: FontWeight.w900, fontSize: 17)),
          Text(subtitle,
              style: const TextStyle(color: FourTheme.muted, fontSize: 12)),
          const SizedBox(height: 12),
          child,
        ],
      ),
    );
  }
}
