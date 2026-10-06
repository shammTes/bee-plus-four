// Registry of the physics-lab sims (LabSpec, see lab_kit.dart). Spread into kSims after the older sims so 'lens' and
// 'mirror' resolve to the extended lab versions.
import 'sims.dart';
import 'sims_em.dart';
import 'sims_optics.dart';

final Map<String, SimSpec Function(Map<String, dynamic>)> labSims = {...opticsLabs, ...emLabs};
