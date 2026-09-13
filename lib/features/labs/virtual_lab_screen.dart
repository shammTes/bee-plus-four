import 'package:flutter/material.dart';

import '../../core/theme/four_theme.dart';

/// Offline virtual lab concepts for Physics · Chemistry · Biology.
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
              const Text('Guided experiments · safety first',
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
            children: [
              _LabList(labs: _physics),
              _LabList(labs: _chemistry),
              _LabList(labs: _biology),
            ],
          ),
        ),
      ],
    );
  }
}

class _Lab {
  const _Lab(this.title, this.aim, this.steps, this.safety);
  final String title;
  final String aim;
  final List<String> steps;
  final String safety;
}

const _physics = [
  _Lab(
    'Ohm\'s law bench',
    'Relate V, I and R using a simple series circuit.',
    [
      'Sketch a series loop: cell → ammeter → resistor → voltmeter across resistor.',
      'Record current I and voltage V for 3 resistor values.',
      'Plot V against I. Slope ≈ R.',
      'Discuss sources of error (contact resistance, meter accuracy).',
    ],
    'Never short the cell. Keep dry hands on power sources.',
  ),
  _Lab(
    'Reflection on a plane mirror',
    'Verify angle of incidence equals angle of reflection.',
    [
      'Pin a plane mirror vertically on paper.',
      'Send rays at 30°, 45°, 60° using pins or a ray box.',
      'Measure i and r with a protractor.',
      'Compare results and state the law of reflection.',
    ],
    'Handle glass mirrors carefully.',
  ),
];

const _chemistry = [
  _Lab(
    'Acid–base titration idea',
    'Estimate concentration using indicator colour change.',
    [
      'Rinse burette with the solution to be filled.',
      'Pipette a fixed volume of analyte into a conical flask.',
      'Add 2–3 drops of indicator.',
      'Titrate to the first permanent colour change. Repeat for concordance.',
    ],
    'Wear eye protection. Wipe spills of acid/base immediately.',
  ),
  _Lab(
    'Rate of reaction (marble + acid)',
    'Observe how concentration affects CO₂ production rate.',
    [
      'Add equal marble chips to equal volumes of acid at two concentrations.',
      'Collect gas or measure mass loss over time.',
      'Compare curves — steeper slope = faster rate.',
      'Link to collision theory.',
    ],
    'Do not seal flasks tightly while gas is produced.',
  ),
];

const _biology = [
  _Lab(
    'Onion epidermis microscopy',
    'Observe plant cells: wall, cytoplasm, nucleus.',
    [
      'Peel a thin onion epidermis layer.',
      'Mount in water; add iodine stain; cover slip at 45°.',
      'Focus under low power then high power.',
      'Draw and label cell wall, nucleus, cytoplasm.',
    ],
    'Handle glass slides and coverslips carefully.',
  ),
  _Lab(
    'Food tests overview',
    'Detect starch, reducing sugar, protein, lipid.',
    [
      'Starch: iodine → blue-black.',
      'Reducing sugar: Benedict\'s + heat → brick red.',
      'Protein: Biuret → purple.',
      'Lipid: ethanol emulsion → cloudy white.',
    ],
    'Heat Benedict\'s in a water bath — not direct flame on open tube.',
  ),
];

class _LabList extends StatelessWidget {
  const _LabList({required this.labs});
  final List<_Lab> labs;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: labs.length,
      itemBuilder: (context, i) {
        final lab = labs[i];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ExpansionTile(
            leading: CircleAvatar(
              backgroundColor: FourTheme.primarySoft,
              child: Text('${i + 1}',
                  style: const TextStyle(
                      fontWeight: FontWeight.w900,
                      color: FourTheme.primaryDark)),
            ),
            title: Text(lab.title,
                style: const TextStyle(fontWeight: FontWeight.w800)),
            subtitle: Text(lab.aim, maxLines: 2),
            childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            children: [
              const Text('Procedure',
                  style: TextStyle(fontWeight: FontWeight.w800)),
              const SizedBox(height: 6),
              ...lab.steps.map((s) => Padding(
                    padding: const EdgeInsets.only(bottom: 6),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('• '),
                        Expanded(child: Text(s)),
                      ],
                    ),
                  )),
              const SizedBox(height: 8),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF7ED),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text('Safety: ${lab.safety}',
                    style: const TextStyle(fontWeight: FontWeight.w600)),
              ),
            ],
          ),
        );
      },
    );
  }
}
