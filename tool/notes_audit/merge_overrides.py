#!/usr/bin/env python3
"""One-off: the unit_<id>.json override files (Grade 11 + bio9-u2) REPLACED the much richer units in the book files
at runtime, and one of them (math11-u1) even broke parsing (a card with page = string). This ports the real content
cards (c##, wrk-extra, xtra2) the overrides added into the book units, completes the strings that were cut off, and
deletes the overrides. Template filler (checklist / misconception / 'Local link' / char-split steps) is dropped.
Physics overrides are left alone (handled in a separate PR)."""
import glob, json, os, re

BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'assets/high/notes/notes')
FIX = {  # cut-off string -> completion appended
    'bio11-u1-c18': {0: ' (high blood glucose). **Too much thyroxine** → overactive thyroid (fast heartbeat, weight loss); **too little** in children → stunted growth and slow mental development.'},
    'bio11-u2-c13': {0: 'rone): deeper voice, facial and body hair, broader shoulders, bigger muscles; in girls (oestrogen): breasts develop, hips widen, menstruation begins, body hair grows.'},
    'bio11-u3-c10': {0: 'tilage on the bone ends and a capsule filled with **synovial fluid** that reduces friction. Examples: **ball-and-socket** (shoulder, hip: movement in all directions), **hinge** (elbow, knee: movement in one plane), **pivot** (between the first two neck vertebrae: turning the head), **gliding** (wrist and ankle bones).'},
    'bio11-u5-c13': {0: ' by receptors, a control centre (often the brain or a gland) sends a message, and an effector brings the level back to normal. Example: when body temperature rises, sweating and widening of skin blood vessels cool the body down.'},
    'bio11-u5-c14': {0: 'alls → the pancreas releases **glucagon** → the liver changes glycogen back to glucose → level rises again. Both hormones act by negative feedback.'},
    'chem11-u1-c16': {0: 'ugh both reactions are still going on.', 1: 'xothermic forward reaction): increasing the pressure shifts the equilibrium to the right (fewer gas molecules, 4 → 2), so more ammonia forms; increasing the temperature shifts it to the left, so less ammonia forms.'},
    'chem11-u3-c13': {0: 'ond and graphite are exceptions with very high melting points), and tend to gain electrons to form negative ions or share electrons in covalent bonds. Their oxides are usually acidic (e.g. CO₂, SO₂).'},
    'geo11-u1-c22': {0: 'mantle. Plates move apart at **divergent** (constructive) boundaries, towards each other at **convergent** (destructive) boundaries, and slide past each other at **transform** boundaries. Most earthquakes and volcanoes occur along plate boundaries.'},
    'geo11-u1-c23': {0: ' mountains such as the Alps, the Himalayas and the Atlas are called **fold mountains**. **Tension** pulls rocks apart and makes **faults**: a block dropped between two faults is a **rift valley** (like the Great Rift Valley that passes through the Danakil depression); a block raised between faults is a **horst** (block mountain).'},
    'geo11-u2-c19': {0: 'ing soluble rocks such as limestone). **Transport:** traction (rolling big boulders), saltation (bouncing pebbles), suspension (fine particles carried in the water) and solution (dissolved minerals). **Deposition** happens when the river slows down and drops its load, for example on flood plains and in deltas.'},
    'geo11-u3-c08': {0: ' water, friction with the sea bed slows the bottom of the wave, the wave gets higher and finally breaks. The forward rush of water up the beach is the **swash**; the water running back down is the **backwash**. **Constructive** waves (strong swash) build beaches; **destructive** waves (strong backwash) erode them.'},
    'geo11-u3-c09': {0: 'as limestone and chalk). These processes form coastal landforms: **cliffs**, **wave-cut platforms**, **caves**, **arches** and **stacks**. Deposition by waves forms **beaches**, **spits** and **bars**.'},
    'geo11-u4-c17': {0: 'elation to the surrounding area (roads, rivers, other towns, resources). Settlement patterns: **nucleated** (houses grouped together), **dispersed** (houses scattered, as on large farms) and **linear** (houses along a road, river or coast).'},
    'geo11-u5-c06': {0: ' all the time: for example, climate controls which plants grow, plants protect the soil, and soil and water support animals and people. A change in one part (such as cutting down forests) affects all the others.'},
    'geo11-u5-c07': {0: 'estock. Some changes help people (terraces conserve soil, dams store water), but careless use causes **soil erosion**, **deforestation**, **desertification**, loss of wildlife and pollution. Sustainable use means meeting today’s needs without harming the resources future generations will need.'},
    'geo11-u6-c08': {0: 't, **Ethiopia** to the south and **Djibouti** to the south-east, and has a long coastline (about 1,200 km on the mainland) along the **Red Sea** to the east, including the **Dahlak archipelago**. Its position on the Red Sea, near the Bab el-Mandeb strait, gives it strategic importance for trade.'},
    'geo11-u6-c09': {0: 'Debubawi Keyih Bahri (Southern Red Sea). Each zoba is divided into sub-zobas.'},
    'geo11-u8-c10': {0: 'e** (far apart) contours = gentle slope; evenly spaced contours = uniform slope. Contours never cross each other (except at an overhanging cliff).'},
    'geo11-u8-c11': {0: 'contours spaced widely in the middle and close together at the edges. **Saddle:** a low area between two hills. **Cliff:** contours very close together or merging. **Gorge:** very close contours on both sides of a narrow valley.'},
    'math11-u1-c09': {1: '− r₂) (the x-intercepts are r₁ and r₂). For example, f(x) = x² − 4x + 3 = (x − 2)² − 1 = (x − 1)(x − 3): the y-intercept is 3, the vertex is (2, −1) and the roots are 1 and 3.'},
    'math11-u2-c07': {0: 'from (0, 0) to (h, k); a > 0 keeps the graph above the starting point, a < 0 reflects it below. Domain: x ≥ h. Example: f(x) = √(x − 2) + 1 starts at (2, 1); its domain is x ≥ 2 and its range is y ≥ 1.'},
    'math11-u3-c07': {1: 'ients; n > m → no horizontal asymptote. Example: f(x) = (2x + 1)/(x − 3) has the vertical asymptote x = 3 and the horizontal asymptote y = 2/1 = 2.'},
    'math11-u5-c09': {0: 'pe but not necessarily the same size. If the scale factor is k, then the ratio of their perimeters is k and the ratio of their areas is k². Example: two similar triangles with sides 3 cm and 6 cm have k = 2, so the larger one has twice the perimeter and four times the area.'},
    'math11-u6-c07': {0: '1 + r)ⁿ, where r is the rate per period as a decimal and n is the number of periods. Example: 10,000 Nakfa at 5% simple interest for 3 years gives I = 10,000 × 0.05 × 3 = 1,500 Nakfa; at 5% compound interest A = 10,000 × 1.05³ ≈ 11,576.25 Nakfa.'},
}
KEEP = re.compile(r'-c\d+$|-wrk-extra\d*$|-xtra2$')


def main():
    books = {}
    for bf in glob.glob(os.path.join(BASE, '*_*.json')):
        b = os.path.basename(bf)
        if b.startswith('unit_') or 'index' in b:
            continue
        d = json.load(open(bf))
        books[b] = d
    for f in sorted(glob.glob(os.path.join(BASE, 'unit_*.json'))):
        uid = os.path.basename(f)[5:-5]
        if uid.startswith('phys'):
            continue
        o = json.load(open(f))
        bname, unit = next((b, u) for b, d in books.items() for u in d['units'] if u['id'] == uid)
        have = {c['id'] for l in unit['lessons'] for c in l['cards']}
        lessons = {l['id']: l for l in unit['lessons']}
        for l in o['lessons']:
            target = lessons.get(l['id']) or unit['lessons'][-1]
            for c in l['cards']:
                if c['id'] in have or not KEEP.search(c['id']):
                    continue
                if not isinstance(c.get('page'), int):
                    c['page'] = target['pages'][0]
                if any(len(s.get('text', '')) <= 1 for s in c.get('steps', [])):
                    continue
                for i, add in FIX.get(c['id'], {}).items():
                    c['body'][i] = c['body'][i].rstrip() + ('' if add.startswith(' ') else '') + add if c['body'][i].endswith(' ') or add.startswith(' ') else c['body'][i] + add
                c['src'] = c.get('src', 'notes')
                target['cards'].append(c)
                have.add(c['id'])
        qs = unit.setdefault('exercise', {}).setdefault('questions', [])
        qtext = {q['q'].strip().lower() for q in qs}
        qids = {q['id'] for q in qs}
        for q in o.get('exercise', {}).get('questions', []):
            if q['q'].strip().lower() in qtext:
                continue
            if q['id'] in qids:
                q['id'] = q['id'] + 'x'
            q.setdefault('similar', [])
            qs.append(q)
        os.remove(f)
        print('merged', uid, '->', bname)
    for b, d in books.items():
        open(os.path.join(BASE, b), 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
