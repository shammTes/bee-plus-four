#!/usr/bin/env python3
"""Rebuild Grade 9 Biology Unit 2 (Taxonomy) in assets/high/notes/notes/biology_9.json.

    python3 tool/enrich/bio9_u2/build.py

Writes the unit (lessons, tables, diagrams, checks, worked examples, games, exercise), the SVG diagrams in
assets/high/notes/notes/svg/biology_9/ and the unit's topic list in assets/high/notes/notes/index.json.
Unit id bio9-u2 and lesson ids bio9-u2-l2-1..3 are kept (unit_questions.json, media placements and the tutor use them).
Afterwards run tool/split_notes.py and tool/build_tutor_index.py.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
NOTES = os.path.join(ROOT, 'assets', 'high', 'notes', 'notes')

from l1 import L21  # noqa: E402
from l2 import L22, L23  # noqa: E402
from l3 import L24, L25, L26  # noqa: E402
from l4 import L27  # noqa: E402
from l5 import L28, L29  # noqa: E402
import ex2  # noqa: E402,F401  (fills ex.QS)
from ex import QS  # noqa: E402
import svgs  # noqa: E402

LESSONS = [L21, L22, L23, L24, L25, L26, L27, L28, L29]

GLOSSARY = [
    ('Taxonomy', 'The branch of biology that names and classifies organisms.', 53),
    ('Taxon', 'A group of organisms at any rank of classification (plural: taxa), e.g. a phylum or an order.', 54),
    ('Binomial nomenclature', 'Linnaeus’s two-name system: genus + species, e.g. *Homo sapiens*.', 56),
    ('Species', 'The lowest rank; members are very similar and interbreed to produce fertile offspring.', 55),
    ('Genus', 'A group of closely related species; the first part of a scientific name (plural: genera).', 55),
    ('Dichotomous key', 'An identification key made of couplets — pairs of mutually exclusive statements.', 58),
    ('Couplet', 'One pair of opposite statements in a dichotomous key.', 58),
    ('Prokaryote', 'An organism whose cell has no true nucleus or membrane-bound organelles (Monera).', 61),
    ('Eukaryote', 'An organism whose cells have a true nucleus (Protista, Fungi, Plantae, Animalia).', 61),
    ('Autotroph', 'An organism that produces complex organic compounds from simple inorganic molecules.', 61),
    ('Heterotroph', 'An organism that cannot make its own food and depends on complex organic substances.', 62),
    ('Saprophyte', 'An organism that feeds on dead or decaying organic matter (decomposer).', 64),
    ('Binary fission', 'Asexual division of one cell into two daughter cells (bacteria, protists).', 64),
    ('Conjugation', 'Exchange or transfer of genetic material between two cells (E. coli, Paramecium, Spirogyra).', 64),
    ('Plankton', 'Tiny organisms that drift in water: phytoplankton (algae) and zooplankton (tiny animals).', 71),
    ('Pseudopodium', 'A “false foot”: an outflow of cytoplasm used for movement and feeding (Amoeba).', 67),
    ('Hypha', 'A thread of a fungus (plural: hyphae).', 76),
    ('Mycelium', 'A mass of fungal hyphae (plural: mycelia).', 76),
    ('Lichen', 'A mutualistic association of a fungus and a green alga.', 80),
    ('Mutualism', 'A symbiosis in which both partners benefit.', 80),
    ('Spore', 'A small reproductive cell that grows into a new organism without fertilisation.', 82),
    ('Sporophyte', 'The spore-bearing generation of a plant.', 82),
    ('Gametophyte', 'The gamete-producing generation of a plant (a fern’s heart-shaped prothallus).', 82),
    ('Prothallus', 'The small, independent, heart-shaped gametophyte of a fern.', 84),
    ('Frond', 'The leaf of a fern.', 84),
    ('Zygote', 'The cell formed when two gametes fuse at fertilisation.', 82),
    ('Hermaphrodite', 'An animal with both male and female sex organs (earthworm, tapeworm).', 92),
    ('Parthenogenesis', 'Development of a new organism from an unfertilised egg.', 88),
    ('Regeneration', 'Regrowth of lost tissue or a body part in an adult organism.', 88),
    ('Metamorphosis', 'A marked change in form during the life cycle (insects, frogs).', 101),
    ('Closed circulatory system', 'Blood flows inside vessels all the time (annelids, vertebrates).', 94),
    ('Poikilothermic', 'Having a body temperature that varies with the surroundings (cold-blooded).', 103),
    ('Homoeothermic', 'Keeping a constant body temperature (warm-blooded): birds and mammals.', 108),
    ('Habitat', 'The natural place where an organism lives.', 88),
]

TIPS = [
    ('Learn the five-kingdom table column by column: cell type, then wall, then nutrition. Most exam questions test just one column.', 63),
    ('For any “which kingdom/phylum/class” question, narrow down rank by rank: kingdom first, then phylum, then class.', 62),
    ('Scientific names: capital genus, small species, italics in print, separate underlines by hand.', 57),
    ('Keys: start at couplet 1 every time and write down your path (1 → 2 → 4 …).', 59),
    ('Disease chains: Plasmodium → malaria → female Anopheles; Trypanosoma → sleeping sickness → tsetse fly; Entamoeba → dysentery → dirty water.', 69),
    ('Fungi numbers: ascus 8 ascospores, basidium 4 basidiospores, yeast ascus 4.', 78),
    ('Plants: vessels → seeds → flowers. The gametophyte shrinks at every step.', 84),
    ('Arthropods: count legs — 6 insect, 8 arachnid; antennae — 2 pairs crustacean, none arachnid.', 96),
    ('Vertebrate hearts: 2-3-3-4-4 (fish, amphibian, reptile, bird, mammal; crocodile has 4).', 103),
]


def games():
    g = []
    g.append({'id': 'bio9-u2-g1', 'type': 'sort', 'title': 'Sort the organisms into their kingdoms', 'lesson': 'bio9-u2-l2-3',
              'groups': [{'id': 'mo', 'label': 'Monera'}, {'id': 'pr', 'label': 'Protista'}, {'id': 'fu', 'label': 'Fungi'}, {'id': 'pl', 'label': 'Plantae'}, {'id': 'an', 'label': 'Animalia'}],
              'items': [{'text': t, 'group': k} for t, k in [
                  ('E. coli (bacterium)', 'mo'), ('Cyanobacteria', 'mo'), ('Nitrifying bacteria', 'mo'), ('Amoeba', 'pr'), ('Paramecium', 'pr'), ('Euglena', 'pr'), ('Spirogyra', 'pr'),
                  ('Plasmodium', 'pr'), ('Yeast', 'fu'), ('Rhizopus (bread mould)', 'fu'), ('Mushroom', 'fu'), ('Penicillium', 'fu'), ('Moss', 'pl'), ('Fern', 'pl'), ('Pine tree', 'pl'),
                  ('Teff', 'pl'), ('Sponge', 'an'), ('Hydra', 'an'), ('Earthworm', 'an'), ('Spider', 'an'), ('Frog', 'an'), ('Human', 'an')]]})
    g.append({'id': 'bio9-u2-g2', 'type': 'builder', 'title': 'Build the hierarchy and the keys', 'lesson': 'bio9-u2-l2-1', 'items': [
        {'words': ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species'], 'hint': 'King Philip Came Over For Good Soup', 'why': 'Largest group first, smallest last.'},
        {'words': ['Animalia', 'Chordata', 'Mammalia', 'Primates', 'Hominidae', 'Homo', 'sapiens'], 'hint': 'Classify a human, kingdom first', 'why': 'Human: Animalia → Chordata → Mammalia → Primates → Hominidae → Homo → sapiens.'},
        {'words': ['Plantae', 'Angiospermae', 'Monocotyledon', 'Commelinales', 'Poaceae', 'Zea', 'mays'], 'hint': 'Classify maize, kingdom first', 'why': 'Maize: Zea mays, a monocot in the grass family Poaceae.'},
        {'words': ['gills?', 'wings?', 'flesh eating?', 'hoof divided?', 'height over 1.5 m?'], 'hint': 'Order the couplets of the textbook key (fish, bat, hyena, donkey, cow/goat)', 'why': 'Fish leaves at 1, bat at 2, hyena at 3, donkey at 4, cow and goat at 5.'},
        {'words': ['Bryophytes', 'Pteridophytes', 'Gymnosperms', 'Angiosperms'], 'hint': 'Simplest plant group first', 'why': 'Brave Pupils Get A’s: vessels, then seeds, then flowers.'},
        {'words': ['egg', 'larva', 'pupa', 'adult'], 'extra': ['nymph'], 'hint': 'Complete metamorphosis of a butterfly', 'why': 'Complete = four stages with a pupa; nymph belongs to incomplete metamorphosis.'},
    ]})
    g.append({'id': 'bio9-u2-g3', 'type': 'sort', 'title': 'Sort the protists and fungi into their groups', 'lesson': 'bio9-u2-l2-5',
              'groups': [{'id': 'pz', 'label': 'Protozoa (ingest)'}, {'id': 'al', 'label': 'Algae (photosynthesis)'}, {'id': 'fg', 'label': 'Fungi (absorb)'}],
              'items': [{'text': t, 'group': k} for t, k in [('Amoeba', 'pz'), ('Paramecium', 'pz'), ('Trypanosoma', 'pz'), ('Plasmodium', 'pz'), ('Euglena', 'al'), ('Chlamydomonas', 'al'),
                                                             ('Volvox', 'al'), ('Ulva', 'al'), ('Diatoms', 'al'), ('Yeast', 'fg'), ('Rhizopus', 'fg'), ('Mushroom', 'fg'), ('Candida albicans', 'fg')]]})
    g.append({'id': 'bio9-u2-g4', 'type': 'sort', 'title': 'Sort the animals into their phylum or class', 'lesson': 'bio9-u2-l2-8',
              'groups': [{'id': 'in', 'label': 'Insects'}, {'id': 'ar', 'label': 'Arachnids'}, {'id': 'cr', 'label': 'Crustaceans'}, {'id': 'my', 'label': 'Myriapods'}, {'id': 'wo', 'label': 'Worms (flat, round, segmented)'}],
              'items': [{'text': t, 'group': k} for t, k in [('Bee', 'in'), ('Ant', 'in'), ('Grasshopper', 'in'), ('House fly', 'in'), ('Spider', 'ar'), ('Scorpion', 'ar'), ('Tick', 'ar'),
                                                             ('Crab', 'cr'), ('Shrimp', 'cr'), ('Lobster', 'cr'), ('Centipede', 'my'), ('Millipede', 'my'), ('Tapeworm', 'wo'), ('Ascaris', 'wo'), ('Earthworm', 'wo')]]})
    g.append({'id': 'bio9-u2-g5', 'type': 'sort', 'title': 'Sort the vertebrates into their classes', 'lesson': 'bio9-u2-l2-9',
              'groups': [{'id': 'f', 'label': 'Fishes'}, {'id': 'a', 'label': 'Amphibians'}, {'id': 'r', 'label': 'Reptiles'}, {'id': 'b', 'label': 'Birds'}, {'id': 'm', 'label': 'Mammals'}],
              'items': [{'text': t, 'group': k} for t, k in [('Shark', 'f'), ('Tilapia', 'f'), ('Sea horse', 'f'), ('Frog', 'a'), ('Toad', 'a'), ('Salamander', 'a'), ('Snake', 'r'), ('Crocodile', 'r'),
                                                             ('Tortoise', 'r'), ('Ostrich', 'b'), ('Pigeon', 'b'), ('Duck', 'b'), ('Bat', 'm'), ('Platypus', 'm'), ('Kangaroo', 'm'), ('Whale', 'm')]]})
    g.append({'id': 'bio9-u2-g6', 'type': 'match', 'title': 'Match the parasite to its disease', 'lesson': 'bio9-u2-l2-5', 'pairs': [
        {'a': 'Plasmodium falciparum', 'b': 'Malignant malaria'}, {'a': 'Trypanosoma', 'b': 'Sleeping sickness'}, {'a': 'Entamoeba histolytica', 'b': 'Amoebic dysentery'},
        {'a': 'Candida albicans', 'b': 'Thrush'}, {'a': 'Dermatophytes', 'b': 'Ringworm, athlete’s foot'}, {'a': 'Rust fungus', 'b': 'Wheat rust'}]})
    g.append({'id': 'bio9-u2-g7', 'type': 'tf', 'title': 'True or false: taxonomy facts', 'seconds': 15, 'items': [
        {'text': 'Species is the largest rank of classification.', 'answer': False, 'why': 'Kingdom is the largest; species is the smallest.'},
        {'text': 'Fungal cell walls are made of chitin.', 'answer': True, 'why': 'Plants use cellulose; fungi use chitin.'},
        {'text': 'Cyanobacteria have a true nucleus.', 'answer': False, 'why': 'They are prokaryotes (Monera).'},
        {'text': 'Mosses have no vascular tissue.', 'answer': True, 'why': 'That is why they stay small and live in damp places.'},
        {'text': 'A spider is an insect.', 'answer': False, 'why': 'It has 8 legs and 2 body parts — an arachnid.'},
        {'text': 'Birds and mammals are homoeothermic.', 'answer': True, 'why': 'They keep a constant body temperature.'},
        {'text': 'Viruses belong to kingdom Monera.', 'answer': False, 'why': 'Viruses are not cells and are not placed in any kingdom.'},
        {'text': 'Echinoderms are all marine.', 'answer': True, 'why': 'Starfish, sea urchins and sea cucumbers live only in the sea.'},
        {'text': 'In ferns the gametophyte is the dominant generation.', 'answer': False, 'why': 'In ferns the sporophyte is dominant; the gametophyte (prothallus) is tiny.'},
        {'text': 'Sharks use internal fertilisation.', 'answer': True, 'why': 'Unlike most fishes, sharks fertilise internally.'}]})
    g.append({'id': 'bio9-u2-g8', 'type': 'flash', 'title': 'Key word flash cards', 'cards': [{'front': a, 'back': b} for a, b, _ in GLOSSARY]})
    g.append({'id': 'bio9-u2-g9', 'type': 'fill', 'title': 'Fill the gap', 'items': [
        {'text': 'The five-kingdom system was proposed by ____ in 1969.', 'answer': 'Whittaker', 'choices': ['Whittaker', 'Linnaeus', 'Aristotle']},
        {'text': 'A mass of fungal hyphae is a ____.', 'answer': 'mycelium', 'choices': ['mycelium', 'prothallus', 'cyst']},
        {'text': 'The tiny heart-shaped gametophyte of a fern is the ____.', 'answer': 'prothallus', 'choices': ['prothallus', 'rhizome', 'frond']},
        {'text': '____ is spread by the female Anopheles mosquito.', 'answer': 'Malaria', 'choices': ['Malaria', 'Sleeping sickness', 'Thrush']},
        {'text': 'Earthworms and some leeches have a ____ that forms the egg cocoon.', 'answer': 'clitellum', 'choices': ['clitellum', 'scolex', 'mantle']},
        {'text': 'The ____ of bony fishes gives buoyancy.', 'answer': 'swim bladder', 'choices': ['swim bladder', 'operculum', 'fin']},
        {'text': 'Egg-laying mammals are called ____.', 'answer': 'monotremes', 'choices': ['monotremes', 'marsupials', 'placentals']},
        {'text': 'Cyanobacteria can fix atmospheric ____.', 'answer': 'nitrogen', 'choices': ['nitrogen', 'oxygen', 'carbon']}]})
    for x in g:
        x.setdefault('lesson', None)
        x['src'] = 'notes'
    return g


def unit_map():
    nodes = [{'id': 'unit', 'label': 'Taxonomy', 'kind': 'unit', 'cards': ['bio9-u2-c01']}]
    edges = []
    for l in LESSONS:
        nid = 'l' + l['id'].split('-l')[1].replace('-', '_')
        nodes.append({'id': nid, 'label': l['title'], 'kind': 'topic', 'lesson': l['id'], 'cards': [c['id'] for c in l['cards'] if c['type'] == 'text'][:4]})
        edges.append({'from': 'unit', 'to': nid, 'label': 'includes'})
    for a, b in zip(nodes[1:], nodes[2:]):
        edges.append({'from': a['id'], 'to': b['id'], 'label': 'next'})
    ideas = [('k_ranks', 'Seven ranks (KPCOFGS)', 'l2_1', 'bio9-u2-c03'), ('k_binomial', 'Binomial nomenclature', 'l2_1', 'bio9-u2-c04'), ('k_key', 'Dichotomous key', 'l2_2', 'bio9-u2-c05'),
             ('k_kingdoms', 'Five kingdoms', 'l2_3', 'bio9-u2-c08'), ('k_altgen', 'Alternation of generations', 'l2_7', 'bio9-u2-c24'), ('k_symmetry', 'Body symmetry', 'l2_8', 'bio9-u2-c27')]
    for i, lab, frm, card in ideas:
        nodes.append({'id': i, 'label': lab, 'kind': 'idea', 'cards': [card]})
        edges.append({'from': frm, 'to': i, 'label': 'key idea'})
    return {'root': 'unit', 'nodes': nodes, 'edges': edges, 'src': 'notes'}


def main():
    p = os.path.join(NOTES, 'biology_9.json')
    with open(p, encoding='utf-8') as f:
        book = json.load(f)
    i = next(k for k, u in enumerate(book['units']) if u['id'] == 'bio9-u2')
    old = book['units'][i]
    diagrams = {}
    os.makedirs(os.path.join(NOTES, 'svg', 'biology_9'), exist_ok=True)
    for old_svg in ('bio9_u2_key.svg', 'bio9_u2_kingdoms.svg', 'bio9_u2_ranks.svg'):  # unused leftovers, replaced below
        q = os.path.join(NOTES, 'svg', 'biology_9', old_svg)
        if os.path.exists(q):
            os.remove(q)
    for k, (fn, title, page) in svgs.ALL.items():
        rel = f'svg/biology_9/bio9_u2_{k}.svg'
        with open(os.path.join(NOTES, rel), 'w', encoding='utf-8') as f:
            f.write(fn())
        diagrams[k] = {'svg': rel, 'title': title, 'page': page, 'pins': []}
    used = {c['diagram'] for l in LESSONS for c in l['cards'] if 'diagram' in c}
    assert used <= set(diagrams), used - set(diagrams)
    ids = [c['id'] for l in LESSONS for c in l['cards']] + [q['id'] for q in QS]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    unit = {
        'id': 'bio9-u2', 'number': 2, 'title': 'Taxonomy', 'status': 'done', 'pages': old.get('pages', [53, 117]), 'tone': old.get('tone', 'peach'),
        'intro': 'Taxonomy is the science of **naming and classifying** living things. In this unit you will learn **why** we classify, how **Linnaeus** arranged organisms into **seven ranks** (Kingdom → Phylum → Class → Order → Family → Genus → Species) and gave each species a **two-part Latin name**, how to use and build a **dichotomous key**, and then walk through **all five kingdoms** of Whittaker’s system — Monera, Protista, Fungi, Plantae and Animalia — with their groups, examples, life cycles and importance.\n\nWork lesson by lesson: read the steps, study the tables and diagrams, answer every quick check, try the worked examples before opening the answer, then do the practice set and the 36-question unit exercise.',
        'intro_page': 53,
        'diagrams': diagrams,
        'lessons': LESSONS,
        'glossary': [{'term': a, 'meaning': b, 'page': c, 'src': 'notes'} for a, b, c in GLOSSARY],
        'tips': [{'text': a, 'page': b, 'src': 'notes'} for a, b in TIPS],
        'games': games(),
        'exercise': {'questions': QS},
        'unitMap': unit_map(),
    }
    for k in old:
        if k not in unit:
            unit[k] = old[k]
    book['units'][i] = unit
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(book, f, ensure_ascii=False, indent=2)
        f.write('\n')
    # index.json topics for this unit
    ip = os.path.join(NOTES, 'index.json')
    with open(ip, encoding='utf-8') as f:
        raw = f.read()
    idx = json.loads(raw)

    def walk(o):
        if isinstance(o, dict):
            if o.get('id') == 'bio9-u2' and 'topics' in o:
                o['topics'] = [{'id': l['id'], 'number': l['number'], 'title': l['title'], 'page': l['pages'][0],
                                'cards': [c['id'] for c in l['cards'] if c['type'] == 'text']} for l in LESSONS]
                return True
            return any(walk(v) for v in o.values())
        if isinstance(o, list):
            return any(walk(v) for v in o)
        return False
    assert walk(idx), 'bio9-u2 not in index.json'
    with open(ip, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'bio9-u2: {len(LESSONS)} lessons, {sum(len(l["cards"]) for l in LESSONS)} cards, {len(diagrams)} diagrams, {len(QS)} questions')


if __name__ == '__main__':
    main()
