#!/usr/bin/env python3
"""Deep expansion of Grade 11 Biology sections in assets/high/notes/notes/biology_11.json.

    python3 tool/enrich/bio11_deep/build.py

Sections (textbook numbering): 1.1.1 pituitary, 1.1.2 thyroid, 1.1.4 adrenal, 1.1.5 pancreas, 1.1.6 sex glands, 1.1.7 thymus
(lesson bio11-u1-l1-1); 2.2 male and 2.3 female reproductive system incl. 2.3.1-2.3.4 (bio11-u2-l2-2, -l2-3);
3.1.3 axial and appendicular skeleton (bio11-u3-l3-1); 6.1.3 plant hormones (bio11-u6-l6-1); 6.3.2 root growth regions
(bio11-u6-l6-3); 6.4.1-6.4.3 stem, leaf, flower (bio11-u6-l6-4).

Unlike the bio9_u2 rebuild this is a *merge*: unit/lesson ids and every existing card are kept. A lesson is described as a
list of existing card ids (kept in place) and card dicts (new cards, or replacements that keep the old id). Old cards that
the list does not mention are appended at the end so nothing is lost. Exercise questions, glossary terms and tips are
merged by id / term / text, so the script can be re-run safely.

Writes the SVG diagrams to assets/high/notes/notes/svg/biology_11/ and updates the lessons' topic card lists in
assets/high/notes/notes/index.json. Afterwards run tool/split_notes.py, tools/map_unit_questions.py,
tools/verify_unit_links.py and tool/build_tutor_index.py.
"""
import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')

import u1, ex_u1  # noqa: E402
import u2, ex_u2  # noqa: E402
import u3, ex_u3  # noqa: E402
import u6, ex_u6  # noqa: E402
import svgs  # noqa: E402

GLOSSARY = {
    'bio11-u1': [
        ('Target cell', 'A cell with receptors for a particular hormone, so it responds to that hormone.', 1),
        ('Negative feedback', 'Control in which a change (e.g. a high hormone level) causes a response that reverses it.', 7),
        ('Tropic hormone', 'A pituitary hormone whose target is another endocrine gland (TSH, ACTH, FSH, LH).', 3),
        ('Hypothalamus', 'Part of the brain that controls the pituitary by releasing hormones and nerve impulses.', 3),
        ('Steroid hormone', 'A lipid hormone made from cholesterol (cortisol, aldosterone, testosterone, oestrogen, progesterone).', 9),
        ('Acromegaly', 'Enlargement of the bones of the face, hands and feet caused by too much growth hormone in an adult.', 17),
        ('Diabetes insipidus', 'Large volumes of dilute urine with no glucose, caused by lack of ADH.', 18),
        ('Myxoedema', 'Adult hypothyroidism: puffy face, weight gain, sluggishness, sensitivity to cold.', 18),
        ('Addison’s disease', 'Failure of the adrenal cortex (lack of cortisol and aldosterone).', 20),
        ('Thymosin', 'Hormone of the thymus that promotes the maturation of T lymphocytes.', 13),
        ('Calcitonin', 'Thyroid hormone that lowers blood calcium by moving calcium into bone.', 7),
    ],
    'bio11-u2': [
        ('Spermatogenesis', 'Formation of sperm cells in the seminiferous tubules of the testes, from puberty.', 29),
        ('Seminiferous tubules', 'Highly coiled tubules in the testis where sperm are made.', 28),
        ('Acrosome', 'Cap at the front of the sperm head containing enzymes that dissolve a way into the ovum.', 29),
        ('Epididymis', 'Coiled tube on the outer surface of each testis where sperm are stored and matured.', 29),
        ('Semen', 'Sperm plus the fluids of the seminal vesicles, prostate and Cowper’s glands.', 30),
        ('Oogenesis', 'Production of ova in the ovaries.', 34),
        ('Ovulation', 'Release of a mature ovum from the ovary (about day 14).', 34),
        ('Corpus luteum', 'Yellow body formed from the empty follicle after ovulation; secretes progesterone.', 33),
        ('Endometrium', 'The inner lining of the uterus, thickened each cycle and shed in menstruation.', 36),
        ('Menopause', 'The permanent end of menstrual cycles, usually at 40–50 years.', 37),
        ('Placenta', 'Organ joining embryo and uterus wall; exchanges food, gases and wastes and secretes hormones.', 40),
        ('Amnion', 'Membrane sac filled with amniotic fluid that cushions the embryo.', 41),
        ('Afterbirth', 'The placenta and remaining umbilical cord expelled after the baby is born.', 43),
    ],
    'bio11-u3': [
        ('Axial skeleton', 'The 80 bones of the skull, vertebral column, sternum and ribs.', 59),
        ('Appendicular skeleton', 'The 126 bones of the limbs and the pectoral and pelvic girdles.', 63),
        ('Fontanel', 'Soft spot between a baby’s skull bones; closes by about two years.', 61),
        ('Atlas', 'First cervical vertebra; carries the skull and allows nodding.', 62),
        ('Axis', 'Second cervical vertebra; allows rotation of the head.', 62),
        ('Floating ribs', 'The last two pairs of ribs, not attached to the sternum.', 63),
        ('Pectoral girdle', 'Shoulder girdle: two scapulae and two clavicles.', 63),
        ('Pelvic girdle', 'Hip girdle: two hip bones fused into a ring with the sacrum.', 63),
        ('Opposable thumb', 'A thumb that can be moved to touch the fingertips, thanks to a saddle joint.', 65),
    ],
    'bio11-u6': [
        ('Plant growth regulator', 'Another name for a plant hormone, because it can stimulate or inhibit growth.', 109),
        ('Apical dominance', 'Suppression of lateral buds by auxin from the terminal bud.', 109),
        ('Phototropism', 'Growth movement of a plant part in response to light from one side.', 110),
        ('2,4-D', 'Synthetic auxin used as a selective weed killer: kills dicots, spares monocots.', 110),
        ('Region of elongation', 'Root zone where cells lengthen by taking in water; causes growth in length.', 118),
        ('Root hair', 'Slender outgrowth of one epidermal cell that absorbs water and minerals.', 119),
        ('Node', 'Point on a stem where a leaf is attached.', 122),
        ('Cambium', 'Dividing cells between xylem and phloem that make new vascular tissue (dicots).', 123),
        ('Palisade layer', 'Upper mesophyll of long cells packed with chloroplasts.', 126),
        ('Stomata', 'Pores in the leaf epidermis that allow gas exchange and control water loss.', 127),
        ('Monoecious', 'Having separate male and female flowers on the same plant (maize).', 129),
        ('Dioecious', 'Having male and female flowers on different plants (papaya).', 129),
        ('Double fertilization', 'Fusion of one male nucleus with the egg and another with the two polar nuclei.', 130),
    ],
}

TIPS = {
    'bio11-u1': [
        ('For every hormone learn six things in this order: gland → hormone → chemical nature → target → function → excess/deficiency. The tables in 1.1.1–1.1.7 are laid out exactly like that.', 3),
        ('Age decides GH disorders: child = gigantism or dwarfism, adult = acromegaly. Thyroxine: child = cretinism, adult = myxoedema.', 17),
        ('Two diabetes: mellitus = insulin (sugar in urine); insipidus = ADH (dilute urine, no sugar).', 19),
    ],
    'bio11-u2': [
        ('Draw the sperm route as five boxes (testis → epididymis → vas deferens → [glands] → urethra) before answering any male-system question.', 28),
        ('Ovulation is about 14 days BEFORE the next period, whatever the cycle length.', 36),
        ('Fertilization: oviduct. Implantation: uterus. Follicle: oestrogen. Corpus luteum: progesterone.', 39),
    ],
    'bio11-u3': [
        ('Bone counts: axial 80 = 22 + 6 + 1 + 26 + 1 + 24; appendicular 126 = 4 + 60 + 2 + 60.', 59),
        ('Vertebrae: 7-12-5-5-4 (33 in a child, 26 bones in an adult). Ribs: 7 true, 3 false, 2 floating.', 62),
    ],
    'bio11-u6': [
        ('Plant hormones: All Good Cooks Ask Eggs — auxin aims, gibberellin grows, cytokinin cuts, ABA asleep, ethylene eat-ready.', 109),
        ('Root tip from the bottom: Can Dogs Eat Meat — cap, division, elongation, maturation.', 118),
        ('Stem outside → in: Every Cat Visits Paris. Leaf top → bottom: Clever Unicorns Prefer Sweet Vanilla Lollipops.', 123),
        ('Ovule → seed, ovary → fruit. Pollination moves pollen; fertilization fuses nuclei.', 130),
    ],
}

# key-idea nodes added to each unit map: (node id, label, topic node, card id)
IDEAS = {
    'bio11-u1': [('k_pit_table', 'Pituitary hormones', 'l1_1', 'bio11-u1-s111-t1'), ('k_feedback', 'Negative feedback', 'l1_1', 'bio11-u1-s112-s1'),
                 ('k_adrenal', 'Adrenal cortex vs medulla', 'l1_1', 'bio11-u1-s114-t1'), ('k_glucose', 'Insulin and glucagon', 'l1_1', 'bio11-u1-s115-s1')],
    'bio11-u2': [('k_sperm', 'Sperm structure', 'l2_2', 'bio11-u2-s22-s2'), ('k_glands', 'Accessory glands', 'l2_2', 'bio11-u2-s22-tb2'),
                 ('k_cycle', 'Menstrual cycle phases', 'l2_3', 'bio11-u2-s231-s1'), ('k_twins', 'Twins', 'l2_3', 'bio11-u2-s233-tb2')],
    'bio11-u3': [('k_206', 'Counting 206 bones', 'l3_1', 'bio11-u3-s313-s1'), ('k_spine', 'Vertebral regions', 'l3_1', 'bio11-u3-s313-s2'),
                 ('k_limbs', 'Arm and leg plan', 'l3_1', 'bio11-u3-s313-tb4')],
    'bio11-u6': [('k_hormones', 'Five plant hormones', 'l6_1', 'bio11-u6-s613-tb1'), ('k_rootzones', 'Root tip regions', 'l6_3', 'bio11-u6-s632-s1'),
                 ('k_stemts', 'Dicot vs monocot stem', 'l6_4', 'bio11-u6-s641-s1'), ('k_leafts', 'Leaf layers', 'l6_4', 'bio11-u6-s642-s1'),
                 ('k_dfert', 'Double fertilization', 'l6_4', 'bio11-u6-s643-s2')],
}

UNITS = [
    ('bio11-u1', 'u1', u1, ex_u1.QS, svgs.U1),
    ('bio11-u2', 'u2', u2, ex_u2.QS, svgs.U2),
    ('bio11-u3', 'u3', u3, ex_u3.QS, svgs.U3),
    ('bio11-u6', 'u6', u6, ex_u6.QS, svgs.U6),
]


def merge_unit(unit, short, mod, qs, svg_defs):
    uid = unit['id']
    lessons = {l['id']: l for l in unit['lessons']}
    by_id = {c['id']: c for l in unit['lessons'] for c in l['cards']}
    move = getattr(mod, 'MOVE', {})
    retitle = getattr(mod, 'RETITLE', {})
    # 1) diagrams
    os.makedirs(os.path.join(NOTES, 'svg', 'biology_11'), exist_ok=True)
    svg_text = {}
    for k in mod.DIAGRAM_KEYS:
        fn, title, page = svg_defs[k]
        rel = f'svg/biology_11/bio11_{short}_{k}.svg'
        s = fn()
        with open(os.path.join(NOTES, rel), 'w', encoding='utf-8') as f:
            f.write(s)
        unit.setdefault('diagrams', {})[k] = {'svg': rel, 'title': title, 'page': page, 'pins': []}
        svg_text[k] = s
    # 2) lessons
    used = set()
    for lid, items in mod.LESSONS.items():
        assert lid in lessons, lid
        out = []
        for it in items:
            if isinstance(it, str):
                assert it in by_id, f'{uid}: unknown card {it}'
                c = copy.deepcopy(by_id[it])
            else:
                c = copy.deepcopy(it)
            assert c['id'].startswith(uid + '-'), c['id']
            if c['id'] in retitle:
                c['title'] = retitle[c['id']]
            used.add(c['id'])
            out.append(c)
        lessons[lid]['_new'] = out
    for lid in mod.LESSONS:
        l = lessons[lid]
        left = [c for c in l['cards'] if c['id'] not in used and c['id'] not in move]
        if left:
            print(f'  note: {lid} keeps unreferenced cards at the end: {[c["id"] for c in left]}')
        l['cards'] = l.pop('_new') + left
    # cards moved out of lessons we did not rebuild
    for l in unit['lessons']:
        if l['id'] not in mod.LESSONS:
            l['cards'] = [c for c in l['cards'] if c['id'] not in used]
    # 3) checks: unique ids, diagrams exist, step keys exist in the SVG
    ids = [c['id'] for l in unit['lessons'] for c in l['cards']]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, f'{uid}: duplicate card ids {dup}'
    for l in unit['lessons']:
        for c in l['cards']:
            if 'diagram' in c:
                assert c['diagram'] in unit.get('diagrams', {}), (c['id'], c['diagram'])
            if c['type'] == 'steps' and c['diagram'] in svg_text:
                for st in c['steps']:
                    if st.get('show'):
                        assert f'data-hl="{st["show"]}"' in svg_text[c['diagram']], (c['id'], st['show'])
            if c['type'] == 'check':
                assert c['answer'] in c['options'], c['id']
    # 4) exercise questions merged by id
    ex = unit.setdefault('exercise', {}).setdefault('questions', [])
    pos = {q['id']: i for i, q in enumerate(ex)}
    for q in qs:
        if q['type'] == 'mcq':
            assert q['answer'] in q['options'], q['id']
        if q['type'] == 'fill':
            assert q['answer'] in q['choices'], q['id']
        if q['id'] in pos:
            ex[pos[q['id']]] = q
        else:
            pos[q['id']] = len(ex)
            ex.append(q)
    qids = [q['id'] for q in ex]
    assert len(qids) == len(set(qids)), f'{uid}: duplicate question ids'
    assert not set(qids) & set(ids), f'{uid}: question id clashes with a card id'
    # 5) glossary and tips
    have = {g['term'].lower() for g in unit.get('glossary', [])}
    for t, m, p in GLOSSARY.get(uid, []):
        if t.lower() not in have:
            unit.setdefault('glossary', []).append({'term': t, 'meaning': m, 'page': p, 'src': 'notes'})
    have = {t['text'] for t in unit.get('tips', [])}
    for t, p in TIPS.get(uid, []):
        if t not in have:
            unit.setdefault('tips', []).append({'text': t, 'page': p, 'src': 'notes'})
    # 6) unit map ideas
    um = unit.get('unitMap')
    if um:
        nids = {n['id'] for n in um['nodes']}
        for nid, lab, frm, card in IDEAS.get(uid, []):
            assert card in ids, card
            if nid not in nids and frm in nids:
                um['nodes'].append({'id': nid, 'label': lab, 'kind': 'idea', 'cards': [card]})
                um['edges'].append({'from': frm, 'to': nid, 'label': 'key idea'})
    return list(mod.LESSONS)


def main():
    p = os.path.join(NOTES, 'biology_11.json')
    with open(p, encoding='utf-8') as f:
        book = json.load(f)
    units = {u['id']: u for u in book['units']}
    touched = {}
    for uid, short, mod, qs, svg_defs in UNITS:
        touched[uid] = merge_unit(units[uid], short, mod, qs, svg_defs)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(book, f, ensure_ascii=False, indent=2)
        f.write('\n')
    # index.json: lesson topic card lists = old ids that still exist + new text cards, in lesson order
    ip = os.path.join(NOTES, 'index.json')
    with open(ip, encoding='utf-8') as f:
        idx = json.load(f)
    lessons = {l['id']: l for u in book['units'] for l in u['lessons']}
    done = set()

    def walk(o):
        if isinstance(o, dict):
            if o.get('id') in touched and 'topics' in o:
                for t in o['topics']:
                    if t['id'] in touched[o['id']]:
                        old = set(t.get('cards', []))
                        t['cards'] = [c['id'] for c in lessons[t['id']]['cards'] if c['id'] in old or c['type'] == 'text']
                        done.add(t['id'])
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(idx)
    missing = {l for ls in touched.values() for l in ls} - done
    assert not missing, f'topics not found in index.json: {missing}'
    with open(ip, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
        f.write('\n')
    for uid, ls in touched.items():
        u = units[uid]
        print(f'{uid}: ' + ', '.join(f'{l} {len(lessons[l]["cards"])} cards' for l in ls) + f'; exercise {len(u["exercise"]["questions"])} questions; {len(u["diagrams"])} diagrams')


if __name__ == '__main__':
    main()
