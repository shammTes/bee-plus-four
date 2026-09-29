import 'package:flutter/widgets.dart';

import '../state/app_state.dart';
import '../theme/tokens.dart';
import '../widgets/kit.dart';
import '../widgets/page.dart';

/// First-run walkthrough. The student must tap the real control named in each step.
class TourCard extends StatefulWidget {
  const TourCard({super.key});
  @override
  State<TourCard> createState() => _TourCardState();
}

class _TourCardState extends State<TourCard> {
  final _name = TextEditingController();

  @override
  void dispose() {
    _name.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final s = HighScope.of(context);
    final step = s.tourStep;
    if (step == null || step < 0 || step >= _copy.length) return const SizedBox.shrink();
    final p = Kit.of(context).p;
    final c = _copy[step];
    final bottom = 14 + MediaQuery.paddingOf(context).bottom + (s.tourWants('name') || s.tourWants('finish') ? 12 : 92);
    return Padding(
      padding: EdgeInsets.only(bottom: bottom),
      child: DecoratedBox(
        decoration: BoxDecoration(color: const Color(0xFFFFFCF7), borderRadius: BorderRadius.circular(24), boxShadow: const [BoxShadow(color: Color(0x332A1A12), blurRadius: 18, offset: Offset(0, 8))]),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 14, 16, 14),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(c.$1, style: _gz(18, FontWeight.w900, p.ink)),
              const SizedBox(height: 6),
              Text(c.$2, style: _gz(15, FontWeight.w700, const Color(0xFF5C4A3A))),
              if (s.tourWants('name')) ...[
                const SizedBox(height: 10),
                Field(controller: _name, placeholder: 'ስምካ', maxLength: 24, onSubmitted: (_) => _saveName(s)),
                const SizedBox(height: 8),
                Btn('ቀጽል', icon: 'play', block: true, onTap: () => _saveName(s)),
              ],
              if (s.tourWants('finish')) ...[
                const SizedBox(height: 8),
                Text('Developed by Shamm Tesfalem, 07162947', style: ts(12.5, w800, p.ink3)),
                const SizedBox(height: 8),
                Btn('ወዲእ', icon: 'check', block: true, onTap: () => s.tourAct('finish')),
              ],
            ],
          ),
        ),
      ),
    );
  }

  void _saveName(HighState s) {
    s.setName(_name.text.trim().isEmpty ? 'Student' : _name.text.trim());
    s.tourAct('name');
  }
}

TextStyle _gz(double size, FontWeight w, Color color) => TextStyle(
      fontFamily: 'HighGeez',
      fontFamilyFallback: const ['HighNunito', 'HighGeez'],
      fontSize: size,
      fontWeight: w,
      color: color,
      height: 1.45,
    );

const _copy = <(String, String)>[
  ('ሰላም', 'እዚ መተግበሪ 4 እዩ። ንክፍሊ 9 ክሳብ 12፣ ብዘይ ኢንተርነት። ስምካ ጽሓፍ እሞ «ቀጽል» ጠውቕ።'),
  ('ክፍልታት', 'እዞም ኣርባዕተ ቁልፊ ክፍሊ 9፣ 10፣ 11ን 12ን እዮም። ክፍሊ 11ን 12ን ሳይንስን ኪነትን ኣለዎም። ናይ ክፍሊ 9 ቁልፊ ጠውቕ።'),
  ('ትምህርቲ', 'ኣብዚ ትምህርትታት ብዝርዝር ኣለዉ። ሓደ ትምህርቲ ጠውቕ፣ ንኣሃዱታት ክትሪኢ።'),
  ('ኣሃዱታት', 'እዚ ናይቲ ትምህርቲ ኣሃዱታት እዩ። ማስታወሻ፣ ልምምድን ማትሪክን ካብዚ ትኸፍት። ሕጂ ናይ ድሕሪት ቁልፊ ጠውቕ።'),
  ('ተመለስ', 'ጽቡቕ። ደጊምካ ናይ ድሕሪት ቁልፊ ጠውቕ፣ ናብ መጀመርታ ገጽ ክትምለስ።'),
  ('ማስታወሻ', 'ኣብ ታሕቲ ዘሎ «Notes» ናይ መጽሓፍ ማስታወሻ እዩ። ነቲ ቁልፊ ጠውቕ።'),
  ('ልምምድ', 'እዚ ናይ ልምምድ ገጽ እዩ። ሕቶታት ብክፍልን ትምህርትን ኣለዉ። ሕጂ «Exercise» ጠውቕ።'),
  ('ማትሪክ', 'እዚ ናይ ፈተና ማትሪክን ሞዴልን እዩ። መልሲን መግለጺን ኣሎ። «Matric» ጠውቕ።'),
  ('መምህር', 'እዚ 4 ንሕቶታትካ ካብ መጽሓፍ የብርህ። ኢንተርነት ኣየድልን። «Tutor» ጠውቕ።'),
  ('መጀመርታ', 'ናብ መጀመርታ ገጽ ንምምላስ «Home» ጠውቕ።'),
  ('ስንድኦት', 'ኣብ ላዕሊ ናይ ስእሊ መለለዪ ኣሎ። ጠውቕዎ፣ ስንድኦትን ብዛዕባን ክትከፍት።'),
  ('ተዛዚሙ', 'ኩሉ ነገር ኣብዚ ስልኪ እዩ። ካብ ሕጂ ብቕልጡፍ ትመሃር። «ወዲእ» ጠውቕ።'),
];
