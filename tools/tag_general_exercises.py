#!/usr/bin/env python3
"""Tag untagged ("General") Exercise-bank items to notes units.

  python3 tools/tag_general_exercises.py --calibrate   # accuracy on already-tagged practice items, no writes
  python3 tools/tag_general_exercises.py               # tag + write files + exercises/index.json counts
  python3 tools/tag_general_exercises.py --flags       # print key-check flags for the untagged items

Strongest evidence first:
  1. hand decisions in tool/matric_unit_sync/general_tags.json: "unit": id -> unit or null to keep General;
     "move": id -> unit of another subject (item is moved to that subject's book of the unit's grade);
     "retag": id -> unit for items that already have a (wrong) unit
  1b. textbook refs in src (e.g. practice_g9_biology#bio9_u3_q032); a ref to another subject's unit moves the
     item to that subject's book (the Physics 9 weather items -> geography_9.json, geo9-u3)
  2. English 9 (school papers): grammar rules on prompt + options + explanation (ENG9_RULES); reading-passage,
     story true/false and spelling items stay General (no Grade 9 unit teaches them)
  3. Maths, Chemistry, Physics: keyword rules on the prompt (then prompt + options), SUBJ_RULES
  3b. Agriculture: keyword rules too (livestock, farm management, forestry, conservation, crops, resources, intro)
  4. other subjects (and rule misses): text classifier = TF-IDF of the item vs every notes unit of the same subject (unit title,
     lesson titles, unit text) + nearest neighbours among unit-tagged exercise items and textbook-ref/medium
     matric links. Units of the item's own grade are preferred (other grades x GRADE_W); an item is tagged
     only if the score clears the calibrated thresholds, otherwise:
  5. sequence neighbours: practice ids are numbered in topic blocks; an unsure item takes the unit of its nearest
     tagged neighbours before and after (within 3 ids) if they agree and the unit is in the classifier's top 3.
Items of another grade end up under that grade's unit (same subject), e.g. a sequence question in the Grade 10
file goes to Grade 12 "Sequence and Series"; it still shows under its own grade's General list too.
Only items with unit null (and the hand retag list) are touched. Idempotent.
"""
import argparse, collections, glob, json, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unitmap_lib import ROOT, NOTES, EXER, UQ, load_units, load_exams, strings, toks, norm, TfIdf, Knn

OUT = os.path.join(ROOT, 'tool/matric_unit_sync')
GRADE_W = 0.8
MED = (0.2, 0.05)   # top score, margin -> confident
LOW = (0.14, 0.03)
WEAK = (0.08, 0.04)  # text subjects only (short factual items score low but rank well); see --calibrate
WEAK_SUBJ = {'biology', 'business_economics', 'geography', 'history'}

ENG9_RULES = [
    (r'passage|refers to|\btitle\b|main idea|the writer|according to|\bstory\b|Senait|Abraham|Hamid|^why\b|^how did|^who made|^where was|described as|\bmeans\b', None),
    (r'spell', None),
    (r'^(?:the word )?\w+ in (?:that sentence|\'[^\']+\') is|the word \w+ is|\bis an?$|is used as an?$|^choose the (?:verb|noun|adverb|adjective|preposition|pronoun|conjunction)|adverb of|proper noun', 'eng9-u3'),
    (r'reported|indirect|direct speech|\bsaid,|\btold me,|in quotes|reporting|after (?:she|he) said|said becomes', 'eng9-u5'),
    (r'continuous passive|perfect passive|is being|are being|was being|were being|has been \w+ed by|have been \w+ed by|has been arrested', 'eng9-u8'),
    (r'passive|modal passive|by the \w+\.$', 'eng9-u2'),
    (r'\bif\b.*\bhad\b.*would have|third conditional|conditional type 3', 'eng9-u10'),
    (r'\bif\b|conditional|unless', 'eng9-u9'),
    (r'question tag|tag question|, (?:isn|aren|wasn|weren|don|doesn|didn|won|can)\'?t (?:he|she|it|they|we|you|i)\b', 'eng9-u7'),
    (r'\barticles?\b', 'eng9-u7'),
    (r'agree|singular|plural verb', 'eng9-u6'),
    (r'\bso that\b|\balthough\b|\bbecause\b|linking|connector', 'eng9-u4'),
    (r'yesterday|\bago\b|\blast (?:night|week|year)|\bhad\b|\bhadn|\bwhile\b|didn\'?t|should have|when (?:i|she|he|they|we) (?:was|were)|after (?:the|school|dinner|she|he|we|i)|before|past (?:participle|simple|continuous|perfect|tense)|grammatical pair|correct sequence|best pair', 'eng9-u1'),
]
ENG9_RULES = [(re.compile(a, re.I), b) for a, b in ENG9_RULES]
# option-only cues (the prompt is a bare sentence to transform)
ENG9_OPT = [
    (r'\b(?:must|should|can|could|will|may) be \w+(?:ed|en)\b', 'eng9-u2'),
    (r'\b(?:is|are|was|were) being \w+', 'eng9-u8'),
    (r'\b(?:has|have|had) been \w+(?:ed|en)\b.*\bby\b', 'eng9-u8'),
    (r'\b(?:is|are|was|were) (?:\w+ed|written|given|sent|told|spoken|eaten|built|sung|broken|taught|known|made|done)\b.*\bby\b', 'eng9-u2'),
    (r'\b(?:said|told \w+|explained|asked) (?:that|if|whether)\b', 'eng9-u5'),
]
ENG9_OPT = [(re.compile(a, re.I), b) for a, b in ENG9_OPT]


def eng9_unit(q):
    for rx, u in ENG9_RULES:
        if rx.search(q['prompt']):
            return u, 'rule'
    opts = ' / '.join(map(str, q['options']))
    for rx, u in ENG9_OPT:
        if rx.search(opts):
            return u, 'rule (options)'
    e = q.get('explanation') or ''
    for rx, u in ENG9_RULES[3:]:
        if rx.search(e):
            return u, 'rule (explanation)'
    return None, 'no grammar rule'


# subject keyword rules on the prompt (+ options), tried before the classifier. A target is a unit id or
# {grade: unit} (the item's grade, else the 0 entry).
SUBJ_RULES = {
    'agriculture': [
        (r'farming system|mixed farming|agro-?pastoral|pastoralism|subsistence|commercial farm|peri-urban|urban farming|history of agriculture|domestication|branch(?:es)? of agricultur|agronomy|role of agriculture', 'agri11-u1'),
        (r'\b(?:livestock|cattle|cow|calf|calves|ruminant|rumen|abomasum|dairy|milk|poultry|chicken|hen|broiler|layer|sheep|goat|camel|pig|breed|crossbre|heterosis|hybrid vigou?r|feed|fodder|forage|silage|hay|animal|vaccin|parasite|deworm|tick|disease of|veterinar|meat|beef|egg|wool|artificial insemination|cloning|refugia)', 'agri12-u1'),  # \b: 'hen' must not match 'when'
        (r'farm (?:management|record|business|budget|plan)|budget|income statement|complementary products|economic problem|\brisk\b|insurance|cobweb|contract|\bsupply\b|\bdemand\b|value chain|gini|subsid|record[- ]keeping|break-even|cost|profit|revenue|marginal|accounting|balance sheet|assets|liabilit|cooperative|market|price|loan|credit|interest rate|iso-?quant|production function|\bMRPS\b|producer surplus|comparative advantage|diminishing returns|rational farmer|stage of production|enterprise|opportunity cost|depreciation|inventory', 'agri12-u4'),
        (r'forest|tree|wildlife|agroforestry|afforestation|deforestation|reforestation|timber|nursery|seedling', 'agri12-u2'),
        (r'erosion|conservation|terrac|irrigat|drainage|water harvest|land degradation|gully|contour|check dam|mulch|drip|sprinkler|waterlogg|salinity', 'agri12-u3'),
        (r'crop|seed|plant(?:ing|ed|s)?\b|sowing|weed|pest|harvest|fertili[sz]er|manure|compost|intercrop|\bLER\b|rotation|horticult|fruit|vegetable|cereal|legume|pulse|germinat|companion|tillage|land preparation|teff|wheat|maize|sorghum|barley|berry|photosynthes|yield|residue|shifting cultivation', 'agri11-u3'),
        (r'climate|rainfall|temperature|soil|biodiversity|agro-?ecolog|water resource|ecosystem|decomposer|nutrient cycl|nitrogen fixation|sustainab', 'agri11-u2'),
        (r'farming system|mixed farming|agro-?pastoral|pastoral|nomad|subsistence|commercial farming|history of agriculture|domestication|role of agriculture|branches of|definition of agriculture|meaning of the word|constraint|land reform|food security|agricultur', 'agri11-u1'),
    ],
    'mathematics': [
        (r'sequence|series|progression|\bA\.?P\.?\b|\bG\.?P\.?\b|nth term|\d+(?:st|nd|rd|th) term|sum of the first|sum to infinity|consecutive terms|common (?:difference|ratio)|0\.\d+\.\.\.|recurring', 'math12-u1'),
        (r'matri(?:x|ces)|determinant|cramer', 'math12-u4'),
        (r'similar (?:triangles|polygons|figures|cubes|solids)|similarity|scale factor|ratio of (?:their )?(?:areas|perimeters|sides|medians|volumes)|~|proportionality|altitude to the hypotenuse|geometric mean', 'math11-u5'),
        (r'probabilit|\bmean\b|median|\bmode\b|variance|standard deviation|frequency|\bdata\b|sampl|quartile|histogram|dice|\bcoins?\b|at random', 'math12-u2'),
        (r'axiom|postulate|conjecture|deductive|inductive reasoning|counterexample|converse|contrapositive|undefined term', 'math10-u2'),
        (r'\b(?:sin|cos|tan|cot|sec|csc|cosec)\b|trigonometr|pythag|hypotenuse|right(?:[- ]angled?)? triangle|angle of (?:elevation|depression)|law of (?:sines|cosines)|sides 3, 4,? (?:and )?5|(?:rectangle|square|wide).*diagonal|diagonal of (?:a|the) (?:rectangle|square)', 'math9-u6'),
        (r'sqrt|√|square root', 'math11-u2'),
        (r'\blog|logarithm|exponential|\be\^|half-life|compound(?:ed)? (?:interest|continuously)', {9: 'math9-u5', 0: 'math11-u4'}),
        (r'rational (?:function|expression|equation)|asymptote', 'math11-u3'),
        (r'transversal|corresponding angles?|alternate (?:interior )?angles?|vertically opposite', 'math10-u3'),
        (r'slope|gradient of|midpoint|distance between|distance formula|equation of (?:the|a) (?:line|circle)|lines? (?:y|\dx) ?=|\bintercept|divid\w* .* ratio|collinear|x\^2 \+ y\^2|centre|center of the circle|radius of the circle|coordinates', {9: 'math9-u3', 10: 'math10-u4', 0: 'math12-u3'}),
        (r'polygon|interior angle|exterior angle|chord|tangent|\barc\b|inscribed|secant|central angle|number of diagonals|hexagon|pentagon|octagon|quadrilateral|rhombus|trapezium|parallelogram', 'math10-u3'),
        (r'surface area|volume|perimeter|\barea\b|congruen|cylinder|cone|sphere|prism|pyramid|cube', 'math10-u5'),
        (r'reflection|rotation|translation|transformation|dilation', 'math10-u4'),
        (r'monomial|binomial|trinomial|polynomial|degree of|coefficient|remainder theorem|factor theorem|leading term|synthetic division|\(\d*x [+-] \d+\)\(|÷ ?\d*x', {9: 'math9-u8', 0: 'math11-u1'}),
        (r'quadratic|parabola|vertex|discriminant|x\^2|x²', {9: 'math9-u4', 0: 'math11-u1'}),
        (r'\bsets?\b|union|intersection|subset|venn|complement of', 'math9-u1'),
        (r'percent|%|interest|profit|loss|commission|discount|brokerage|partnership|bank', {9: 'math9-u7', 10: 'math9-u7', 0: 'math11-u6'}),
        (r'relation|function|domain|range|inverse|f\(x\)|one-to-one|onto', {9: 'math9-u2', 0: 'math10-u1'}),
        (r'linear (?:equation|function|inequalit)|system of equations|simultaneous', {0: 'math9-u3'}),
        (r'absolute value|\|x|variation|varies (?:directly|inversely)|^solve:? -?\d*x [+-]', {0: 'math9-u2'}),
        (r'triangle|angle', 'math10-u3'),
    ],
    'chemistry': [
        (r'radioactiv|half-life|nuclear|alpha (?:decay|particle)|beta (?:decay|particle)|gamma|isotope.*decay|fission|fusion', 'chem12-u3'),
        (r'oxidation (?:number|state)|redox|oxidi[sz]|reduc(?:ed|ing|tion)|electrolys|e[\s_]?cell|electrode|galvanic|voltaic|anode|cathode|faraday|electroplat|corrosion|rust', 'chem11-u2'),
        (r'\bp[Hh]\b|\bpOH\b|buffer|titrat|neutrali[sz]|\bK[ab][12]?\b|pKa|pKb|hydrolysis|conjugate|\b(?:HCl|NaOH|KOH|NH4Cl|HNO3|CH3COOH|CH3COONa|Ba\(OH\)2|Ca\(OH\)2)\b', 'chem10-u4'),
        (r'\bmoles?\b|molar mass|empirical|molecular formula|percent(?:age)? (?:yield|composition)|stoichiometr|limiting|avogadro|balanc', 'chem9-u3'),
        (r'nitrogen|ammonia|sulphur|sulfur|haber|contact process|nonmetal|phosphorus|ozone|manufactur|allotrop|graphite|diamond', 'chem11-u3'),
        (r'alkane|alkene|alkyne|iupac|isomer|ester|alcohol|organic|hydrocarbon|functional group|benzene|carboxylic|aldehyde|ketone|ethanol|methane|propan|butan|xylene|polymer|\bC\d*H\d', 'chem12-u2'),
        (r'vsepr|molecular shape|shape of|bond angle|hybridi[sz]|crystal|lattice|tetrahedral|trigonal|linear molecule', 'chem12-u1'),
        (r'equilibri|\bK[cp]\b|le chatelier|reversible', 'chem11-u1'),
        (r'rate of (?:a |the )?reaction|reaction rate|catalyst|activation energy|collision theory', 'chem11-u1'),
        (r'gas law|boyle|charles|avogadro\'s law|ideal gas|\bPV\b|kinetic molecular|partial pressure|dalton\'s law|graham|effusion|diffusion of gas|\bSTP\b', 'chem11-u5'),
        (r'\bp[Hh]\b|\bpOH\b|neutrali[sz]|\bacids?\b|\bbases?\b|\bsalts?\b|buffer|indicator|titrat|bronsted|arrhenius|lewis acid|hydrolysis|proton donor|amphoter', 'chem10-u4'),
        (r'enthalpy|exothermic|endothermic|heat of (?:reaction|combustion|formation|neutrali)|hess|calorimet|ΔH', 'chem10-u5'),
        (r'molarity|molality|solubility|solution|solute|solvent|concentration|colligative|dilut|ppm|saturated', 'chem10-u3'),
        (r'ionic bond|covalent|metallic bond|intermolecular|hydrogen bond|van der waals|dipole|lewis (?:structure|dot)|electronegativ|bond(?:ing|s)?\b', 'chem10-u2'),
        (r'electron configuration|subshell|orbital|periodic|ionization energy|atomic radius|group \d|period \d|noble gas|halogen|alkali metal|quantum number', 'chem10-u1'),
        (r'aluminium|aluminum|iron|copper|zinc|sodium|metals?\b|alloy|ore|blast furnace', 'chem11-u4'),
        (r'proton|neutron|electron|atomic number|mass number|isotope|subatomic|atom', 'chem9-u2'),
        (r'mixture|element|compound|physical change|chemical change|state of matter|sublimation|matter', 'chem9-u1'),
        (r'apparatus|laboratory|lab safety|beaker|burette|pipette|scientific method', 'chem9-u4'),
    ],
    'physics': [
        (r'wind|rainfall|climate|weather|humidity|cloud|atmospher|altitude|pressure belt|inversion|evaporat|condens|monsoon', None),  # geography items filed under physics: keep General
        (r'photoelectric|photon|quantum|bohr|atomic spectr|de broglie|work function|energy level', 'phys12-u2'),
        (r'pressure|fluid|buoyan|archimedes|pascal|hydraulic|float|density|upthrust|bernoulli', 'phys12-u1'),
        (r'refract|lens|light (?:passes|travels|enters) from|from (?:air|vacuum) (?:in)?to|in a medium|\bn = \d|critical angle|total internal|dispersion|prism|myopia|hypermetropia|short-sight|long-sight|distant objects|magnif|microscope|telescope|focal length.*lens|spectacles|\bcolou?rs?\b|filter', 'phys11-u1'),
        (r'magnet|induction|solenoid|transformer|generator|electromagnet|flux|motor effect|fleming', 'phys11-u2'),
        (r'\bwaves?\b|sound|frequency|wavelength|echo|pitch|amplitude|resonance|ultrasound|loudness|decibel|electromagnetic spectrum', 'phys11-u3'),
        (r'mirror|reflection|reflected|virtual image|real image|pinhole|shadow|eclipse|speed of light', 'phys10-u5'),
        (r'charge|coulomb|electric field|electroscope|capacitor|electrostatic|static electricity|conductor|insulator|semiconductor', 'phys10-u3'),
        (r'current|resist|ohm|circuit|voltage|potential difference|\bemf\b|kwh|kilowatt|watt|ammeter|voltmeter|galvanometer|fuse|cells? in (?:series|parallel)|electric(?:al)? (?:energy|power)|bulb', 'phys10-u4'),
        (r'temperature|heat|thermometer|celsius|fahrenheit|kelvin|specific heat|latent|conduction|convection|radiation|thermodynamic|thermal|expansion|melting|boiling|isobaric|isothermal|adiabatic|isochoric|first law', 'phys10-u2'),
        (r'projectile|circular|centripetal|relative velocity|torque|moment|angular|banked|orbit', 'phys10-u1'),
        (r'machine|efficiency|mechanical advantage|velocity ratio|\bMA\b|\bVR\b|lever|pulley|work done|kinetic energy|potential energy|power|\bwork\b|energy|joule', 'phys9-u4'),
        (r'newton|force|friction|momentum|impulse|inertia|mass|weight|collision|recoil|tension', 'phys9-u3'),
        (r'velocity|acceleration|displacement|speed|distance|free fall|motion|uniform', 'phys9-u2'),
        (r'si unit|significant|measurement|vector|scalar|error|prefix|dimension|convert|vernier|micrometer|unit of', 'phys9-u1'),
    ],
}
SUBJ_RULES = {k: [(re.compile(a, re.I), b) for a, b in v] for k, v in SUBJ_RULES.items()}


PROMPT_ONLY = {'agriculture'}  # option words (feed, market, ...) mislead here


def rule_unit(q, subj, grade, U):
    srcs = [q['prompt']] if subj in PROMPT_ONLY else [q['prompt'], q['prompt'] + ' ' + ' / '.join(map(str, q['options']))]
    for src in srcs:
        for rx, t in SUBJ_RULES.get(subj, []):
            if rx.search(src):
                if t is None:
                    return 'GENERAL'
                u = t if isinstance(t, str) else t.get(grade, t.get(0))
                if u in U:
                    return u
    return None


def files():
    idx = json.load(open(os.path.join(EXER, 'index.json')))
    for g, subs in idx['grades'].items():
        for s, e in subs.items():
            yield os.path.join(EXER, e['file']), s, int(g)
    sp = os.path.join(EXER, 'school/index.json')
    for g, subs in json.load(open(sp))['grades'].items():
        for s, e in subs.items():
            yield os.path.join(EXER, 'school', e['file']), s, int(g)


def qtext(q):
    return q['prompt'] + ' ' + ' '.join(map(str, q.get('options') or [])) + ' ' + (q.get('explanation') or '')[:600]


def build():
    units = load_units()
    U = {u['id']: u for u in units}
    docs, books = [], {}
    for u in units:
        nb = books.get(u['file']) or books.setdefault(u['file'], json.load(open(os.path.join(NOTES, u['file']))))
        uu = next(x for x in nb['units'] if x['id'] == u['id'])
        body = ' '.join(strings({k: v for k, v in uu.items() if k != 'exercise'}))
        docs.append(toks((u['title'] + ' ') * 4 + (' '.join(u['lessons']) + ' ') * 2 + body))
    tf = TfIdf(docs)
    train = []
    for path, s, g in files():
        for q in json.load(open(path))['questions']:
            if q.get('unit') in U and s != 'english':
                train.append((toks(qtext(q)), q['unit'], 'ex|' + q['id']))
    ex = {q['id']: q for f, e, q in load_exams()}
    for uid, l in json.load(open(UQ))['units'].items():
        if uid.startswith('eng'):
            continue
        for m in l:
            if m['confidence'] in ('high', 'medium') and not m.get('secondary') and m['id'] in ex:
                q = ex[m['id']]
                o = q.get('options')
                t = (q.get('stem') or '') + ' ' + (' '.join(map(str, o.values())) if isinstance(o, dict) else '') + ' ' + ' '.join(map(str, q.get('explanation_steps') or []))
                train.append((toks(t), uid, 'mx|' + m['id']))
    knn = Knn(train)
    return units, U, tf, knn


def classify(q, subj, grade, units, tf, knn, exclude=None):
    allowed_i = [i for i, u in enumerate(units) if u['subject'] == subj]
    allowed = {units[i]['id'] for i in allowed_i}
    t = toks(qtext(q))
    ds = {units[i]['id']: s for i, s in tf.scores(tf.query(t), allowed_i)}
    kv = collections.defaultdict(float)
    ex = (lambda k: k == exclude) if exclude else (lambda k: False)
    for l, s in knn.neighbours(t, 10, exclude=ex, allowed=allowed):
        kv[l] += s
    gw = {units[i]['id']: (1.0 if units[i]['grade'] == grade else GRADE_W) for i in allowed_i}
    return sorted(((u, (ds.get(u, 0) + 0.05 * kv.get(u, 0)) * gw[u]) for u in allowed), key=lambda x: -x[1])


def conf(sc, subj=None):
    if len(sc) < 2:
        return 'medium' if sc and sc[0][1] >= MED[0] else None
    top, mar = sc[0][1], sc[0][1] - sc[1][1]
    if top >= MED[0] and mar >= MED[1]:
        return 'medium'
    if top >= LOW[0] and mar >= LOW[1]:
        return 'low'
    if subj in WEAK_SUBJ and top >= WEAK[0] and mar >= WEAK[1]:
        return 'weak'
    return None


# ------------------------------------------------------------------ key checks
WAIT = re.compile(r'\bwait\b|recalculat|let me (?:re|check|try)|\bhmm\b|i made an error|closest is|none (?:of the options )?match|not in (?:the )?options|doesn\'t match|does not match', re.I)
LETTER = re.compile(r'(?:answer|correct (?:option|choice)|option)\s*(?:is|:)?\s*\(?([A-E])\)?(?![\w\'’])', re.I)


def nrm(s):
    return re.sub(r'\s+', ' ', str(s).lower().replace('−', '-')).strip(' .;:')


def flags(q):
    out = []
    o = [str(x) for x in q['options']]
    k = q['answer']
    e = q.get('explanation') or ''
    if WAIT.search(e):
        out.append('wait/recalculate in explanation')
    if sum(nrm(x) == nrm(o[k]) for x in o) > 1:
        out.append('key text in two options')
    for m in LETTER.finditer(e):
        L = 'ABCDE'.index(m.group(1).upper())
        if L != k and L < len(o):
            out.append(f'explanation says option {m.group(1).upper()}')
            break
    m = re.search(r'(?:answer|correct answer)\s*(?:is|:)\s*([^.;\n]{1,60})', e, re.I)
    if m:
        said = nrm(m.group(1))
        hits = [i for i, x in enumerate(o) if nrm(x) and (nrm(x) == said or (len(nrm(x)) > 3 and said.startswith(nrm(x))))]
        if hits and k not in hits:
            out.append(f'explanation answer "{m.group(1).strip()}" is option {"ABCDE"[hits[0]]}')
    eqs = re.findall(r'=\s*([^=,;\n]{1,25}?)(?:[.;,]\s|[.;,]?$|\s(?:so|which|and|therefore|thus|hence)\b)', e)
    if eqs:
        last = nrm(eqs[-1])
        hits = [i for i, x in enumerate(o) if nrm(x) == last]
        if hits and k not in hits:
            out.append(f'explanation ends "= {eqs[-1].strip()}" = option {"ABCDE"[hits[0]]}')
    def said(x):
        x = nrm(x)
        return bool(x) and re.search(r'(?<![\w./^-])' + re.escape(x) + r'(?![\w/^]|\.\d)', nrm(e)) is not None
    if not said(o[k]):
        others = [i for i, x in enumerate(o) if i != k and said(x) and not said_in_prompt(q, x)]
        if len(others) == 1:
            out.append(f'explanation names option {"ABCDE"[others[0]]} "{o[others[0]][:30]}", not the key')
    if not e.strip():
        out.append('no explanation')
    return out


def said_in_prompt(q, x):
    return nrm(x) in nrm(q['prompt'])


SRC = re.compile(r'#([a-z]+)(\d+)_u0*(\d+)_')


def src_unit(q, U):
    m = SRC.search(str(q.get('src') or ''))
    u = m and f'{m.group(1)}{m.group(2)}-u{m.group(3)}'
    return u if u in U else None


SEQ = re.compile(r'(.*_practice_.*)_(\d+)$')


def neighbour_unit(q, seq, near=3):
    """Unit shared by the closest tagged items before and after q in its source sequence (ids are
    numbered in topic blocks), or None if they disagree or one side has no tagged item within `near`."""
    m = SEQ.match(q['id'])
    if not m:
        return None
    s, n = m.group(1), int(m.group(2))
    def side(d):
        for k in range(1, near + 1):
            if (u := seq.get((s, n + d * k))):
                return u
    a, b = side(-1), side(1)
    return a if a and a == b else None


def seq_map(qs):
    return {(m.group(1), int(m.group(2))): q.get('unit') for q in qs if (m := SEQ.match(q['id']))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--calibrate', action='store_true')
    ap.add_argument('--flags', action='store_true')
    ap.add_argument('--sample', type=int, default=0, help='print N random tags per book for hand checking')
    a = ap.parse_args()
    hand_p = os.path.join(OUT, 'general_tags.json')
    hand = json.load(open(hand_p)) if os.path.exists(hand_p) else {'unit': {}}
    if a.flags:
        for path, s, g in files():
            for q in json.load(open(path))['questions']:
                if not q.get('unit') and (f := flags(q)):
                    print(q['id'], '|', f, '| key', q['answer'], q['options'][q['answer']][:50], '|', q['prompt'][:90])
        return
    units, U, tf, knn = build()
    if a.calibrate:
        rows = collections.Counter()
        for path, s, g in files():
            if s == 'english' or '/school/' in path:
                continue
            qs = json.load(open(path))['questions']
            seq = seq_map(qs)
            for q in qs:
                if q.get('unit') in U and str(q.get('src', '')).startswith('practice_'):
                    sc = classify(q, s, g, units, tf, knn, exclude='ex|' + q['id'])
                    c = conf(sc, s)
                    rows[(c, sc[0][0] == q['unit'])] += 1
                    if not c:
                        nu = neighbour_unit(q, seq)
                        if nu and nu in [x[0] for x in sc[:3]]:
                            rows[('neighbours', nu == q['unit'])] += 1
        for c in ('medium', 'low', 'weak', None, 'neighbours'):
            n = rows[(c, True)] + rows[(c, False)]
            print(c, n, f'{rows[(c, True)] / max(n, 1):.0%}')
        return
    idx_p = os.path.join(EXER, 'index.json')
    idx = json.load(open(idx_p))
    report = collections.defaultdict(lambda: collections.Counter())
    samples = collections.defaultdict(list)
    books = [(path, s, g, json.load(open(path))) for path, s, g in files()]
    byfile = {p: d for p, s, g, d in books}
    changed, moves = set(), []
    for path, s, g, data in books:
        for q in data['questions']:
            # hand retags of items that already carry a unit (e.g. torque items on the wrong grade)
            if q['id'] in hand.get('retag', {}) and q.get('unit') != hand['retag'][q['id']]:
                q['unit'] = hand['retag'][q['id']]
                changed.add(path)
                report['(retagged by hand)']['tagged'] += 1
        keep, pending = [], []
        for q in data['questions']:
            if q.get('unit'):
                keep.append(q)
                continue
            book = f'{s} {g}' + (' (school)' if '/school/' in path else '')
            report[book]['before'] += 1
            move = None
            if q['id'] in hand.get('move', {}):
                # item belongs to another subject's book: move it there under the given unit
                u, via = hand['move'][q['id']], 'hand (moved)'
                move = os.path.join(os.path.dirname(path), f"{U[u]['subject']}_{U[u]['grade']}.json")
                assert move in byfile, move
            elif q['id'] in hand['unit']:
                u, via = hand['unit'][q['id']], 'hand'
            elif (ru := src_unit(q, U)):
                # textbook ref carried in src (e.g. practice_g9_biology#bio9_u3_q032)
                u, via = ru, 'textbook ref'
                if U[ru]['subject'] != s:
                    move = os.path.join(os.path.dirname(path), f"{U[ru]['subject']}_{U[ru]['grade']}.json")
                    if move not in byfile:
                        u, via, move = None, 'textbook ref: other subject, no book', None
            elif s == 'english':
                u, via = eng9_unit(q) if g == 9 else (None, 'no rule')
            elif (ru := rule_unit(q, s, g, U)):
                u, via = (ru, 'rule')
                if ru == 'GENERAL':
                    # geography items that sit in a physics book: move them to that grade's geography book
                    dest = os.path.join(os.path.dirname(path), f'geography_{g}.json')
                    if dest in byfile:
                        sc = classify(q, 'geography', g, units, tf, knn)
                        u, via, move = sc[0][0], 'moved to geography', dest
                    else:
                        u, via = None, 'rule: other subject'
            else:
                sc = classify(q, s, g, units, tf, knn)
                c = conf(sc, s)
                u, via = (sc[0][0], c) if c else (None, 'unsure')
                if not u:
                    pending.append((q, sc, book))
            if u:
                q['unit'] = u
                changed.add(path)
                report[book]['tagged'] += 1
                report[book]['other grade'] += U[u]['grade'] != g
                samples[book].append((u, via, q['prompt'][:100]))
                if move:
                    report[book]['moved'] += 1
                    moves.append((move, q))
                    continue
            else:
                report[book]['general'] += 1
            keep.append(q)
        # second pass: unsure items whose tagged neighbours in the source sequence agree on a unit
        # that is also among the classifier's top 3
        seq = seq_map(keep)
        for q, sc, book in pending:
            nu = neighbour_unit(q, seq)
            if nu and nu in [x[0] for x in sc[:3]]:
                q['unit'] = nu
                changed.add(path)
                report[book]['tagged'] += 1
                report[book]['general'] -= 1
                report[book]['other grade'] += U[nu]['grade'] != g
                samples[book].append((nu, 'neighbours', q['prompt'][:100]))
        data['questions'] = keep
    for dest, q in moves:
        byfile[dest]['questions'].append(q)
        changed.add(dest)
    for path, s, g, data in books:
        if path in changed:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        if '/school/' not in path:
            ent = idx['grades'][str(g)][s]
            cnt = collections.Counter(q.get('unit') or 'general' for q in data['questions'])
            ent['count'] = len(data['questions'])
            ent['units'] = dict(sorted(cnt.items()))
    idx['total'] = sum(e['count'] for gg in idx['grades'].values() for e in gg.values())
    with open(idx_p, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for b, c in sorted(report.items()):
        print(f'{b:28} untagged {c["before"]:4} -> tagged {c["tagged"]:4} (other grade {c["other grade"]}, moved {c["moved"]}), General {c["general"]}')
    if a.sample:
        rnd = random.Random(7)
        for b, l in sorted(samples.items()):
            print('##', b)
            for x in rnd.sample(l, min(a.sample, len(l))):
                print('  ', x)


if __name__ == '__main__':
    main()
