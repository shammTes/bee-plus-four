r"""Grade 11 Unit 1 — Introduction to Agriculture (pp. 1-37): history, roles, farming systems, constraints, branches."""
from common import set_unit, T, RM, MN, TB, DG, ST, WK, CK, QSet
from svglib import Fig, INK, BLUE, RED, GREEN, PURPLE, ORANGE, GREY, FILL
from agrilib import (box, tlines, wrap, flow, hflow, cycle, leader, ground, grass_tufts, sorghum, cow, goat, sheep, camel,
                     hen, person, maresha, sun, cloud, tree, BROWN, SOIL, LEAF, STRAW, WATER)

UID = 'agri11-u1'
set_unit(UID)


# ------------------------------------------------------------------ figures
def f_history():
    f = Fig(340, 300)
    f.title('From hunting to modern farming', 13)
    stages = [('Hunting, fishing, gathering', 'people move with the food', GREY),
              ('Domestication', 'dog first, then goat; seeds sown', GREEN),
              ('Settled farming', 'villages, storage of surplus', ORANGE),
              ('Improved farming', 'better seed, breeds, irrigation', BLUE),
              ('Mechanisation + science', 'tractors, harvesters, information', PURPLE)]
    for i, (a, b, c) in enumerate(stages):
        y = 30 + i * 53
        f.g(' '.join(f'k{j}' for j in range(i + 1, 6)))
        f.circle(30, y + 20, 15, c, 2, FILL[c]).text(30, y + 25, str(i + 1), 14, c)
        box(f, 54, y + 2, 276, 38, '', c, 12)
        f.text(64, y + 17, a, 12.5, INK, 'start')
        f.text(64, y + 33, b, 11, GREY, 'start', False)
        if i:
            f.line(30, y - 18, 30, y + 5, GREY, 2)
        f.end()
    f.text(170, 296, 'Eritrea: farming began about 4000 years ago', 11.5, GREEN)
    return f


def f_roles():
    f = Fig(340, 300)
    cx, cy = 170, 150
    roles = ['Food', 'Income', 'Foreign currency', 'Raw materials', 'Jobs', 'Fuel', 'Culture and status',
             'Environment', 'Draught energy', 'Building materials']
    cols = [GREEN, BLUE, PURPLE, ORANGE, RED, BROWN, PURPLE, GREEN, ORANGE, BROWN]
    import math
    for i, (r, c) in enumerate(zip(roles, cols)):
        a = math.radians(90 - 36 * i)
        x, y = cx + 128 * math.cos(a), cy - 118 * math.sin(a)
        f.line(cx + 46 * math.cos(a), cy - 40 * math.sin(a), x - 30 * math.cos(a), y + 14 * math.sin(a), GREY, 1.6)
        box(f, x - 46, y - 15, 92, 30, r, c if c in FILL else ORANGE, 11, fill='#FFFFFF' if c not in FILL else None)
    f.ellipse(cx, cy, 50, 34, GREEN, 2.4, FILL[GREEN])
    tlines(f, cx, cy, ['Agriculture', 'in Eritrea'], 13, GREEN)
    return f


def f_systems():
    f = Fig(340, 236)
    f.title('Share of the farming population (Table 1.1)', 12.5)
    rows = [('Nomadic pastoralism', 11, ORANGE, 'whole family moves with the herd'),
            ('Semi-nomadic pastoralism', 22, BLUE, 'village base + seasonal grazing'),
            ('Sedentary agro-pastoralism', 67, GREEN, 'permanent village, crops + animals')]
    for i, (name, p, c, note) in enumerate(rows):
        y = 34 + i * 64
        f.text(10, y + 10, name, 12, INK, 'start')
        f.rect(10, y + 17, 300, 20, GREY, 1, '#F7F3EE', 4)
        f.rect(10, y + 17, 3 * p, 20, None, 0, c, 4)
        f.text(10 + 3 * p + (6 if p < 80 else -6), y + 32, f'{p}%', 13, INK if p < 80 else '#FFFFFF', 'start' if p < 80 else 'end')
        f.text(10, y + 52, note, 11, GREY, 'start', False)
    f.text(170, 230, 'Smallholders farm about 95% of the cultivated land', 11, GREEN)
    return f


def f_mixed():
    f = Fig(340, 250)
    ground(f, 200, c='#E9D9BF')
    sorghum(f, 62, 200, 100)
    sorghum(f, 88, 200, 86)
    cow(f, 255, 200, 1.05, '#8B5A3C', udder=False, face=-1)
    f.curve_arrow(108, 95, 210, 95, -30, GREEN, 2.4, 9)
    tlines(f, 160, 52, ['straw, stover, bran', '= dry-season feed'], 11.5, GREEN)
    f.curve_arrow(220, 214, 92, 214, -22, BROWN, 2.4, 9)
    tlines(f, 156, 238, ['manure + ox draught for the maresha'], 11.5, BROWN)
    f.text(75, 22, 'crops', 13, INK).text(75, 37, 'grain for the family', 11, GREY, 'middle', False)
    f.text(262, 118, 'livestock', 13, INK).text(262, 133, 'milk, meat, cash', 11, GREY, 'middle', False)
    return f


def f_constraints():
    f = Fig(340, 330)
    box(f, 110, 6, 120, 30, 'Constraints', RED, 13)
    f.text(250, 26, 'grouped by origin', 10.5, GREY, 'start', False)
    cols = [(GREEN, 'Natural', ['Biotic: pests, weeds', 'Abiotic: erratic rain', 'Climate change']),
            (ORANGE, 'Anthropogenic', ['Land degradation', 'Land tenure', 'Soil erosion', 'Poor land use']),
            (BLUE, 'Socio-economic', ['Marketing + storage', 'Inputs', 'Infrastructure', 'Know-how', 'War', 'Tools'])]
    for i, (c, h, items) in enumerate(cols):
        x = 6 + i * 112
        f.line(170, 36, x + 50, 64, GREY, 1.4)
        box(f, x, 64, 104, 28, h, c, 12)
        for j, it in enumerate(items):
            lines = wrap(it, 17)
            y = 100 + j * 34
            f.rect(x, y, 104, 30, c, 1, '#FFFFFF', 5)
            tlines(f, x + 52, y + 15, lines, 10.5, INK, 'middle', False)
    f.text(170, 318, 'Yield factors: defining (given) · limiting (inputs) · reducing (pests)', 10.5, PURPLE)
    return f


def f_soilloss():
    f = Fig(340, 220)
    f.title('Soil lost to erosion (tons per hectare per year)', 12.5)
    data = [('Highlands', 50, 100, RED), ('Moist lowlands', 47, 47, ORANGE), ('Eastern escarpment', 37, 37, ORANGE), ('Dry lowlands', 6, 6, GREEN)]
    for i, (z, a, b, c) in enumerate(data):
        y = 36 + i * 44
        f.text(118, y + 16, z, 11.5, INK, 'end')
        f.rect(124, y + 3, a * 1.8, 20, None, 0, c)
        if b > a:
            f.rect(124 + a * 1.8, y + 3, (b - a) * 1.8, 20, c, 1.2, FILL[RED], 0, dash=True)
            f.text(120 + a * 1.8, y + 18, f'{a}–{b}', 12, '#FFFFFF', 'end')
        else:
            f.text(128 + a * 1.8, y + 18, str(a), 12, INK, 'start')
    f.text(170, 212, 'Steep slopes + heavy storms + bare soil = the highest losses', 11, GREY, 'middle', False)
    return f


def f_branches():
    f = Fig(340, 300)
    box(f, 95, 6, 150, 30, 'Agricultural science', GREEN, 12.5)
    groups = [('Plant sciences', GREEN, ['Horticulture', 'Agronomy', 'Soil science', 'Forestry', 'Forage + pasture']),
              ('Animal sciences', ORANGE, ['Animal husbandry', 'Nutrition', 'Breeding', 'Rangeland', 'Aquaculture']),
              ('Support + management', BLUE, ['Irrigation, drainage', 'Soil + water cons.', 'Economics', 'Extension', 'Mechanisation', 'Post-harvest', 'Plant protection', 'Veterinary', 'Agro-climatology', 'Land reclamation'])]
    for i, (h, c, items) in enumerate(groups):
        x = 4 + i * 112
        f.line(170, 36, x + 52, 52, GREY, 1.4)
        box(f, x, 52, 108, 30, h, c, 11.5)
        for j, it in enumerate(items):
            f.text(x + 8, 102 + j * 19, '• ' + it, 10.5, INK, 'start', False)
    return f


DIAGRAMS = {
    'history': (f_history(), 'Five stages in the history of agriculture', 2),
    'roles': (f_roles(), 'Ten roles agriculture plays in Eritrea (1.2.1–1.2.10)', 5),
    'systems': (f_systems(), 'The three main farming systems of Eritrea and their share of the farming population', 9),
    'mixed': (f_mixed(), 'Mixed farming: crops feed the animals, animals feed the soil and pull the plough', 11),
    'constraints': (f_constraints(), 'Constraints on agricultural development, grouped by origin', 18),
    'soilloss': (f_soilloss(), 'Estimated soil loss by zone (p. 24)', 24),
    'branches': (f_branches(), 'The three groups of agricultural sciences (Table 1.4)', 29),
}

# ------------------------------------------------------------------ 1.1 history
L1 = [
    T('def', 'What agriculture means', 1,
      'The word **agriculture** comes from two Latin words: **ager** = soil or land, and **cultura** = cultivation (tilling the land). So the word itself means "looking after the land to grow things".',
      '**Definition (learn it):** agriculture is the organized production of **food, feed** (for animals) and **fibres**. A broader definition adds the **processing and marketing** of crops, livestock and their by-products.',
      'Agriculture is both a **science** and an **art**:',
      '- **Science** — it uses scientific methods and knowledge (soil chemistry, plant breeding, animal nutrition).',
      '- **Art** — it also needs skill and judgement that only practice gives (when to plough, how deep, which ox to pair with which).',
      '**Eritrean example:** a farmer near Mendefera decides to sow barley after the first good rain in June (art: reading the season) and uses an improved seed from the Ministry of Agriculture (science).'),
    DG('hist-fig', 'The story of agriculture in five stages', 2, 'history',
       'Read the figure from top to bottom: each stage kept what was useful from the stage before.'),
    T('=agri11-u1-c06', '1.1.1 From hunting and gathering to crop and livestock production', 2,
      'Nobody knows exactly where and when agriculture began, because people in many places started to grow crops and keep animals. What we do know is the order of the steps:',
      '**Step 1 — Hunting, fishing and gathering.** Early people hunted animals, fished, and gathered fruits, leaves, bark and honey. They moved often, owned almost no private property and stored very little.',
      '**Step 2 — Settling and planting.** Life slowly became more settled. People planted some crops to add to wild food and began to **store surplus** for lean times. Storage is the first big advantage of farming.',
      '**Step 3 — Domestication of animals.** The **dog** is believed to be the first domesticated animal (hunting, guarding, company). The **goat** probably came next, to secure food when hunting was poor. The **horse** was among the first animals tamed for draught and carrying loads.',
      '**Step 4 — Better methods.** People selected better seed (sound propagating material such as seeds, bulbs and tubers), better breeds, built irrigation to add to rainfall, improved tools and storage.',
      '**Step 5 — Mechanisation and information.** Tractors, harvesters and combines now plough, plant and harvest far faster, with less labour and time, while keeping product quality.',
      '**In Eritrea** farming is believed to have started about **4000 years ago**. Most people still grow crops, keep animals, or do both.'),
    TB('compare', 'Gathering and hunting compared with farming', 3, ['Feature', 'Hunting and gathering', 'Organised farming'],
       [['Food supply', 'Uncertain; depends on what nature offers', 'More reliable; preferred foods are grown'],
        ['Way of life', 'Mobile, following food', 'Settled villages'],
        ['Storage', 'Little or none', 'Surplus stored for dry season and drought'],
        ['Ownership', 'Almost no private property', 'The product belongs to the farmer'],
        ['Animals', 'Wild animals hunted', 'Domesticated animals bred in confinement']], layout='compare'),
    T('domestic', 'Why domesticated animals spread so widely', 2,
      'Domesticated animals **thrive under artificial conditions** and **reproduce regularly in confinement**; wild animals rarely do. That is why herders could carry them to new places.',
      'As they spread, animals **adapted** to new environments. Example: the humped **zebu cattle** of Eritrea (Arado in the highlands, Barka in the western lowlands) tolerate heat, ticks and poor grazing much better than European breeds; the European **Holstein-Friesian** gives far more milk but needs cool weather and good feed.'),
    RM('rem', 'Remember', 4,
       '**ager** + **cultura** = agriculture.',
       'Order: hunting/gathering → settling + storing → domestication (dog first, then goat) → improved seed, breeds, irrigation → mechanisation.',
       'Farming in Eritrea: about **4000 years** old.'),
    WK('wk1', 'Worked example — the advantage of settling', 3,
       'Exercise 1.1 Q2: What advantages did settling in one place and growing crops and animals give early humans compared with hunting and gathering?',
       ['Think of what was **uncertain** in hunting: food might not be found. Farming makes food **more available and predictable**.',
        'Think of **ownership**: the crop or the herd belongs to the family that raised it.',
        'Think of **time**: a surplus can be **stored** for the dry season or a drought.',
        'Think of **choice**: people grow the foods they **prefer** (e.g. barley, teff) instead of eating whatever is found.'],
       'More reliable food, ownership of the product, stored surplus for lean times, and preferred foods.'),
    WK('wk2', 'Worked example — components of modern agriculture', 3,
       'Exercise 1.1 Q3: List some components of modern agriculture.',
       ['Start from the **inputs**: improved seed and breeds, fertilizers, pesticides, veterinary drugs.',
        'Add **water**: irrigation systems that supplement rainfall (e.g. drip irrigation at Sawa-Afhimbol).',
        'Add **machines**: tractors, planters, harvesters and combines.',
        'Add **knowledge**: agricultural information, research and extension, good storage methods.'],
       'Improved seed and breeds, fertilizer and pesticides, irrigation, mechanisation, good storage, and information/extension.'),
]

# ------------------------------------------------------------------ 1.2 roles
L2 = [
    DG('roles-fig', 'Ten roles of agriculture', 5, 'roles',
       'An exam may ask for "five roles". Pick any five and give **one Eritrean example** for each.'),
    T('=agri11-u1-c08', '1.2.1 Food supply', 5,
      'Agriculture feeds the nation. Eritrean farms produce:',
      '- **Cereals:** wheat, barley, sorghum, pearl millet, finger millet and teff (taff).',
      '- **Pulses:** peas, beans, lentils (and chickpea, faba bean).',
      '- **Oil crops:** sesame, groundnut, Niger seed, linseed, cottonseed.',
      '- **Fruits:** bananas, oranges, lemons, mangos, guavas, apples.',
      '- **Vegetables:** cabbage, kale, onion, tomato, lettuce.',
      '- **Animal foods:** meat, milk, eggs, honey, and by-products such as cream, butter, cheese and yogurt.',
      'Together these give the **carbohydrates, proteins, fats, vitamins and minerals** people need. Example: injera from teff or sorghum (carbohydrate) eaten with shiro from chickpea or peas (protein).'),
    T('=agri11-u1-c09', '1.2.2 Source of income', 5,
      'Farmers earn money by selling fruits, vegetables, grain, oil seeds, cotton, **live animals** (cattle, sheep, goats, poultry) and **animal products** (hides and skins, milk, butter, honey) on local markets or for export.',
      'As agriculture grows it also creates income for **other businesses**: factories that make animal feed, herbicides, pesticides and veterinary drugs, and traders and transporters.',
      '**Example:** a family near Keren sells goats at the Monday livestock market to pay school fees.'),
    T('=agri11-u1-c10', '1.2.3 Earner of foreign currency', 5,
      'Exported farm products bring **foreign currency**: live animals, skins and hides, meat, milk products, oil seeds (especially sesame), cotton, fresh or processed fruit and vegetables, flowers, spices, gums and resins.',
      'Eritrea uses this currency to **import** what it does not produce: petroleum, farm machinery, electronic equipment, medicine and fertilizer.'),
    T('=agri11-u1-c11', '1.2.4 Raw materials for industry', 6,
      'Agro-industries depend on farm products:',
      '- **Edible oil** from sesame, cottonseed and Niger seed.',
      '- **Flour and pasta** from wheat and other grains.',
      '- **Beer** from malting barley.',
      '- **Sugar** from sugar cane and sugar beet.',
      '- **Textiles** from cotton and wool.',
      '- **Dairy products** (cheese, butter, yogurt, powdered milk) from milk; **canned meat** from meat.',
      '- **Shoes, bags and belts** from hides and skins (leather industry).',
      'Processing gives useful **by-products** too: **oil-seed cake** and **molasses** are good animal feeds — another link between crops and livestock.'),
    T('=agri11-u1-c12', '1.2.5 Employment', 6,
      'Agriculture is the main source of livelihood in rural Eritrea: about **70 per cent** of the population is agrarian (p. 17).',
      'Besides the farm family, dairy, poultry and horticultural farms, processing plants, input shops, markets and transport all **employ people**. A strong farm sector keeps young people in the villages instead of moving to towns without work.'),
    T('=agri11-u1-c13', '1.2.6 Source of fuel', 7,
      'Most rural kitchens burn **wood, charcoal and dung**, all from agriculture and forests.',
      '**Watch out:** burning dung and crop residues for fuel takes organic matter and nutrients away from the soil. That is why improved stoves (such as the Eritrean **Adhanet** mogogo) are encouraged.'),
    T('=agri11-u1-c14', '1.2.7 Socio-cultural heritage', 7,
      'Livestock have social value: they act as **insurance or a bank** for rural families (sell an ox in a bad year), and they bring **prestige** — in Eritrea a farmer with many animals commands more respect. Animals are also given at weddings and slaughtered at holidays.'),
    T('=agri11-u1-c15', '1.2.8 Environmental impact (positive and negative)', 7,
      'Agriculture can harm or help the environment.'),
    TB('env', 'Environmental impact of agriculture', 7, ['Negative effects', 'Positive effects'],
       [['Deforestation for farmland and fuel', 'Afforestation and tree planting'],
        ['Over-cultivation and overgrazing', 'Land reclamation (terraces, check dams, enclosures)'],
        ['Soil contamination from misuse of pesticides and fertilizers', 'Animal manure used as fertilizer'],
        ['Air pollution from chemicals and burning', 'Pollination by bees']]),
    T('=agri11-u1-c16', '1.2.9 Source of energy (draught power)', 8,
      'Oxen, camels, donkeys and horses supply **energy** for ploughing, transport and carrying water. Two oxen pulling a **maresha** (traditional plough) save many days of hoeing; a donkey carries water and grain to and from the market.'),
    T('=agri11-u1-c17', '1.2.10 Source of construction materials', 8,
      'Wood for houses, furniture and fence poles comes from planted or natural trees. **Straw of sorghum and pearl millet** is used for fencing, walls and roofing — for example the round huts (agudo) of the western lowlands.'),
    WK('wk3', 'Worked example — products and by-products', 6,
       'Exercise 1.2 Q3: Name industries that get raw materials from agriculture, with their products and by-products.',
       ['Write each industry with its raw material and product: oil mill (sesame, Niger seed) → edible oil.',
        'Add the by-product: **oil-seed cake** → animal feed.',
        'Sugar factory (sugar cane) → sugar; by-product **molasses** → animal feed.',
        'Flour mill (wheat) → flour, pasta; by-product **bran** → feed. Brewery (malting barley) → beer; spent grain → feed.',
        'Dairy (milk) → butter, cheese, yogurt; tannery (hides, skins) → leather, shoes, bags; textile mill (cotton, wool) → cloth.'],
       'Oil mill → oil + cake; sugar → sugar + molasses; flour mill → flour + bran; brewery → beer; dairy → butter, cheese; tannery → leather; textile → cloth.'),
    MN('mn', 'Memory trick — the ten roles in textbook order', 5,
       'Food, Income, Foreign currency, Raw materials, Employment, Fuel, Socio-cultural, Environment, Energy (draught), Construction. Say them in the order of the textbook sections 1.2.1 to 1.2.10.'),
]

# ------------------------------------------------------------------ 1.3 farming systems
L3 = [
    T('=agri11-u1-c18', '1.3 What a farming system is', 9,
      '**A farming system** is the way the parts of a farm (land, crops, animals, family labour, tools, money) are **linked together**. The links include draught power, feed, manure, capital and social ties.',
      'Eritrean agriculture has stayed at **subsistence** level for generations: smallholders and agro-pastoralists manage about **95 %** of the cultivated land.',
      '- **Subsistence farmers** have few resources and eat most of what they produce, with little left to sell.',
      '- **Commercial farmers** produce mainly to **sell** and earn income, using more inputs and modern technology.',
      'Eritrea has **three major farming systems** — nomadic pastoralism, semi-nomadic pastoralism and sedentary agro-pastoralism — plus **intensive commercial** systems.'),
    DG('sys-fig', 'How many people follow each system', 9, 'systems'),
    T('nomadic', 'a) Nomadic pastoralism', 10,
      '**Pastoralism** = a farming system where **animals are the main component**. **Nomadism** = not settling in one place.',
      '- **Where:** dry, thinly populated semi-desert areas (0.8–10 people per km²): the **Red Sea coastal areas** and the **north-western lowlands**.',
      '- **How:** the **whole family moves** with the herd in search of pasture and water.',
      '- **Animals:** cattle are the most important (kept mainly for **milk**, not meat), with camels, sheep, goats and donkeys. Rainfall, water and disease decide the mix.',
      '- **Land:** owned and grazed **communally**. Wealth and prestige are counted in animals, not money.',
      '- **Value:** the source of most male animals sold in urban markets.',
      '- **Problem:** schools, clinics and veterinary services are hard to deliver to people who keep moving. Nomadism is now giving way to settled agro-pastoralism.'),
    T('seminomadic', 'b) Semi-nomadic pastoralism and transhumance', 10,
      'Semi-nomadic pastoralists have a **village base** and stay for some months where water and pasture are good; they then move with the animals to **seasonal grazing areas**, where they may also plant crops (sometimes in riverbeds).',
      '**Transhumance** is one form: the seasonal movement of people and livestock between zones — for example from the **hot lowlands to the cool highlands** during the hot season, and back when the lowland rains come.',
      'It is easier to bring basic services to semi-nomadic communities than to nomads. In Eritrea it occurs in **spate irrigation** areas such as **Sheeb** (Northern Red Sea).'),
    T('sedentary', 'c) Sedentary agro-pastoralism (mixed farming)', 11,
      'Families live in **permanent villages**, grow crops and keep livestock. This is **mixed farming**, the system of the **moist and arid highlands** (e.g. around Asmara, Mendefera, Adi Keyh). It can be intensive or extensive, for cash or for subsistence.',
      'Systems in Eritrea that integrate crops and livestock:',
      '- rain-fed **cereal–pulse** production',
      '- the crop–livestock mixed system',
      '- the agro-pastoralist rain-fed system',
      '- small-scale **irrigated horticulture**',
      '- agro-pastoral **spate irrigation**'),
    DG('mixed-fig', 'The two-way link in mixed farming', 11, 'mixed',
       'Crops give straw, stover and bran to the animals; animals give manure (fertility) and draught power (oxen pull the maresha) back to the crops.'),
    TB('=agri11-u1-c19', 'Mixed farming: advantages and disadvantages (Table 1.2)', 12, ['Advantages', 'Disadvantages'],
       [['Crops feed the animals; manure fertilises the crops', 'Free grazing can cause overgrazing and land degradation'],
        ['Diversified produce gives a balanced diet', 'Needs much labour'],
        ['Oxen, camels, donkeys provide draught power', 'Expensive for a first-time farmer'],
        ['Steady cash from several products', 'Specialising in one commodity is sometimes more profitable'],
        ['Insurance in drought: if crops fail, animals can be sold', 'Needs know-how in both crops and animals'],
        ['Good use of land and labour through the year', 'Only possible where both crops and livestock can be produced'],
        ['Crop residues used as feed raise profit', 'Crops are hard to grow in marginal, arid areas']]),
    T('intensive', 'd) Intensive commercial systems', 13,
      '**Intensive** = high inputs per hectare and per animal to get high output. Three examples:',
      '**i) Peri-urban dairy** — around Asmara, Keren and other towns, to sell milk. Breed: **Holstein-Friesian** and its crosses with local cattle. A Holstein can give **35–40 litres a day** in countries with well-developed dairies, but much less in Eritrea because of constraints. Feeds: crop residues, hay, alfalfa, elephant grass, wheat bran, wheat middlings, sorghum husk and sesame cake. Constraints: feed shortage, little land for forage and housing, poor husbandry, weak extension and veterinary services, diseases (tuberculosis, brucellosis, foot-and-mouth disease, mastitis).',
      '**ii) Commercial poultry** — most eggs still come from free-ranging village chickens, but commercial farms keep the **White Leghorn** in houses with feeders and drinkers. It suits warm climates and lays **up to 270 eggs a year**. Common diseases: Newcastle disease, Gumboro, Marek\'s disease, respiratory diseases.',
      '**iii) Commercial farms** — profit-oriented, selling to local or foreign markets. State farms such as **Elabered**, **Sawa-Afhimbol Agro-Industries** (drip irrigation) and **Alighidir** (cotton), plus fast-growing private farms producing cereals, oil seeds, fruit, vegetables and livestock.'),
    TB('systems-tbl', 'The farming systems side by side', 9, ['System', 'Who moves?', 'Main products', 'Where in Eritrea', 'Share'],
       [['Nomadic pastoralism', 'Whole family, all year', 'Milk, live animals', 'Red Sea coast, north-west lowlands', '11 %'],
        ['Semi-nomadic pastoralism', 'Herds move seasonally; village base', 'Animals + some crops', 'Spate areas, e.g. Sheeb', '22 %'],
        ['Sedentary agro-pastoralism', 'Nobody — permanent village', 'Cereals, pulses, animals', 'Moist and arid highlands', '67 %'],
        ['Intensive commercial', 'Nobody', 'Milk, eggs, crops for sale', 'Around towns; state and private farms', 'small']], layout='cards'),
    WK('wk4', 'Worked example — nomadic vs semi-nomadic', 17,
       'Exercise 1.3 Q1: Explain the differences between nomadic and semi-nomadic pastoralism.',
       ['Compare **who moves**: nomads move with the whole family all year; semi-nomads keep a village base and move the herd seasonally.',
        'Compare **crops**: nomads grow none; semi-nomads may plant crops in riverbeds or at seasonal grazing areas.',
        'Compare **services**: easier to provide schools and clinics to semi-nomads.',
        'Give the **share and place**: nomadic 11 % (coast, north-west); semi-nomadic 22 % (e.g. Sheeb spate area).'],
       'Nomads move the whole family all year and do not farm; semi-nomads have a base village, move seasonally and may grow some crops.'),
    WK('wk5', 'Worked example — reading Table 1.1', 9,
       'A sub-zone has 3 000 farming households that follow the national pattern. How many are in each system?',
       ['Nomadic: 11 % of 3 000 = 0.11 × 3 000 = **330**.',
        'Semi-nomadic: 22 % of 3 000 = 0.22 × 3 000 = **660**.',
        'Sedentary agro-pastoral: 67 % of 3 000 = 0.67 × 3 000 = **2 010**.',
        'Check: 330 + 660 + 2 010 = 3 000 ✓.'],
       '330 nomadic, 660 semi-nomadic, 2 010 sedentary agro-pastoral.'),
]

# ------------------------------------------------------------------ 1.4 constraints
L4 = [
    T('intro4', 'Why Eritrea does not yet grow enough food', 17,
      'More than **70 %** of Eritreans are farmers, yet the country still does not produce enough food. A **constraint** is anything that holds production back. The textbook sorts constraints in **two ways** — learn both.'),
    TB('yield', 'Way 1 — by effect on yield (Table 1.3)', 18, ['Group', 'Meaning', 'Examples'],
       [['Yield-defining', 'Given conditions; production cannot happen without them; beyond the farmer\'s control', 'CO₂ concentration, solar radiation, temperature, humidity, altitude and latitude, crop physiology, species, breeds, varieties'],
        ['Yield-limiting', 'Decide how close the crop or animal gets to its best yield', 'Water, plant nutrients (N, P and micronutrients), animal nutrition'],
        ['Yield-reducing', 'Cut the yield that would otherwise be achieved', 'Insects, rodents, diseases, weeds (parasitic and non-parasitic), pollutants, stress']], layout='cards'),
    MN('mn4', 'Quick test for the three groups', 18,
       'Ask: **Can the farmer change it?** No → defining (altitude, sunlight). **Can he add it?** → limiting (water, fertilizer, feed). **Does he have to fight it?** → reducing (pests, weeds, disease).'),
    DG('con-fig', 'Way 2 — by origin', 18, 'constraints'),
    T('=agri11-u1-c21', '1.4.1 Natural factors', 19,
      '**a) Biotic factors** — caused by living things; they lower both **quality and quantity**.',
      '- Insects: locusts and grasshoppers, armyworms, stalk-borers, weevils.',
      '- Diseases of crops and livestock caused by bacteria, fungi and viruses.',
      '- Livestock parasites: external (ticks, fleas, lice, mites) and internal (gastro-intestinal and blood parasites).',
      '- Weeds compete with the crop for **water, light and nutrients**. Parasitic weed: **Striga** (witchweed) on sorghum roots. Other weeds: wild oats in barley and wheat.',
      '**b) Abiotic factors** — from non-living things. Rainfall in most of Eritrea is **low, unevenly distributed and falls in heavy showers** over a short time. It often starts early and stops before the crop has finished filling grain, so repeated **droughts** cut yields.',
      '**c) Climate change** — greenhouse gases (**CO₂, CH₄, CFCs, N₂O**) trap heat. Results: higher temperatures, less and more erratic rain. Burning dung and crop residues for fuel, deforestation, grass burning and erosion all reduce the soil\'s ability to store carbon.'),
    T('=agri11-u1-c22', '1.4.2 Anthropogenic (human-made) factors', 21,
      '**a) Land degradation** — the land\'s physical, biological and economic potential declines. Causes: **overgrazing, over-cultivation, deforestation**, made worse by drought, steep slopes and torrential rain. Human history adds to it: trees cut for trenches and villages burned during the independence war, and land confiscation and tree destruction under Italian colonial rule. Effects: lower yields per input, fewer livestock, loss of vegetation, fuel-wood shortage, loss of topsoil.',
      '**b) Land tenure** — the system of owning, leasing or using land. Traditional systems: **dessa** (village land, redistributed; common in the highlands; average holding about **1 ha**; women had no land rights), **risti** (kinship land) and **demaniale** (state land). **Land Law No. 58 of 1994** made the state the owner and gave every Eritrean, **including women**, the right of **usufruct** (use). Redistribution every **5–7 years** still discourages long-term investment such as terraces; communal rangeland encourages overgrazing.',
      '**c) Soil erosion** — the removal of topsoil by **water or wind**. Organic matter is already low, so soils hold less water and crops suffer in dry spells. Estimated losses: **50–100 t/ha/year** in the highlands, **47** in the moist lowlands, **37** on the eastern escarpment and about **6** in the dry lowlands.',
      '**d) Inappropriate land use** — ploughing steep slopes and building houses on fertile plains. Traditionally hills were for settlement and grazing and plains for crops; urban growth is breaking this rule. **Land-use planning** allocates land to farming, settlement, forest, grazing and roads according to carrying capacity.'),
    DG('loss-fig', 'Where erosion is worst', 24, 'soilloss'),
    T('=agri11-u1-c23', '1.4.3 Socio-economic factors', 25,
      '- **Poor marketing and storage:** little credit, little price information, shortages of fertilizer, seed, pesticides, drugs and spare parts; perishable produce is lost on the way to market without cold rooms, silos or warehouses.',
      '- **Inadequate inputs:** too little fertilizer, improved seed, chemicals, better breeds and machinery. Local seed is well adapted but low-yielding.',
      '- **Poor infrastructure:** mountains and plains make it hard to link farms to markets and factories, although many roads, bridges and dams have been built since independence.',
      '- **Lack of know-how:** many farmers cannot read, extension is thin, and tradition is hard to change (e.g. herders keep large herds instead of investing their value).',
      '- **Effects of war:** bombing and fires destroyed crops, livestock and trees; the 1998–2000 border war hit the sector hard.',
      '- **Inadequate technical inputs:** primitive tools and a low-input, low-output system.'),
    WK('wk6', 'Worked example — classifying constraints', 18,
       'Classify each by effect on yield: (a) altitude of Asmara (2 325 m); (b) a nitrogen shortage in a teff field; (c) Striga in a sorghum field; (d) the Arado breed of a cow.',
       ['(a) Altitude cannot be changed by the farmer → **yield-defining**.',
        '(b) Nitrogen can be supplied as fertilizer or manure → **yield-limiting**.',
        '(c) Striga is a weed that takes away yield → **yield-reducing**.',
        '(d) The breed sets the genetic ceiling of milk yield → **yield-defining**.'],
       '(a) defining (b) limiting (c) reducing (d) defining.'),
    WK('wk7', 'Worked example — soil loss on a farm', 24,
       'A farmer has 2 ha on the eastern escarpment and 3 ha in the dry lowlands. Using the textbook estimates, how much soil is lost each year?',
       ['Escarpment: 2 ha × 37 t/ha = **74 t**.',
        'Dry lowlands: 3 ha × 6 t/ha = **18 t**.',
        'Total: 74 + 18 = **92 t** every year — about 9 large truckloads.'],
       '92 tonnes per year (74 t + 18 t).'),
]

# ------------------------------------------------------------------ 1.5 branches
L5 = [
    T('intro5', 'Agriculture is an applied, multidisciplinary science', 28,
      'Agricultural science rests on **basic sciences**: biology, chemistry, physics, mathematics, geography and economics.',
      '- **Mathematics:** animal and plant breeding, soil physics, agricultural economics.',
      '- **Chemistry:** animal nutrition, soil fertility, plant protection, food processing, fertilizer formulation.',
      '- **Physics:** soil physics, densities, nutrient and water transport.',
      '- **Botany** (plant classification), **zoology** (animal science, entomology, microbiology) and **genetics** (the foundation of breeding).',
      'For convenience the subject is split into **three groups**: plant sciences, animal sciences, and production support and management systems.'),
    DG('br-fig', 'The branches at a glance (Table 1.4)', 29, 'branches'),
    T('=agri11-u1-c25', '1.5.1 Plant sciences', 30,
      '- **Horticulture:** fruits, vegetables, flowers, ornamentals, spices, medicinal and aromatic plants; also environmental horticulture (home gardens, landscaping, parks) and horticultural therapy.',
      '- **Agronomy** (Greek *agros* = field, *nomos* = to manage): principles and practice of **field-crop** production — cereals, pulses, oil, industrial and forage crops — including breeding and management.',
      '- **Soil science:** soil formation, classification, mapping, physical, chemical and biological properties.',
      '- **Forestry:** the art and science of managing forests, plantations and related resources.',
      '- **Forage and pasture:** producing forage plants and managing pastures for animals.'),
    T('=agri11-u1-c26', '1.5.2 Animal sciences', 31,
      '- **Animal husbandry:** keeping cattle, sheep, goats, camels, equines, poultry, pigs, rabbits and bees — breeding, feeding and management.',
      '- **Animal nutrition:** feeding a balanced diet for optimum production.',
      '- **Animal breeding:** improving animals by **selection** within a breed or **crossing** with other breeds (e.g. Holstein × Arado crosses).',
      '- **Rangeland management:** maintaining and improving grazing land.',
      '- **Aquaculture:** farming fish, shrimps, crabs, lobsters and oysters in ponds under controlled feeding and management.'),
    T('=agri11-u1-c27', '1.5.3 Production support and management systems', 32,
      '- **Irrigation and drainage engineering:** irrigation brings water from a source to the crop through canals or pipes (spate, sprinkler, basin, furrow, drip); **drainage** removes excess water from the surface and upper subsoil.',
      '- **Soil and water conservation engineering:** terraces, check dams, bunds — reducing soil loss and protecting water supply.',
      '- **Agricultural economics:** choosing the best combination of limited resources to **maximise profit**.',
      '- **Agricultural extension:** educating farmers so they apply new knowledge.',
      '- **Agricultural mechanisation:** machines for production, processing and transport — saves labour and time.',
      '- **Post-harvest and food-processing engineering:** cutting losses in quality and quantity.',
      '- **Plant protection:** keeping plants healthy and controlling insects, rodents, birds and weeds by integrated pest management (IPM).',
      '- **Veterinary science:** animal diseases and health, including diseases shared with humans (zoonoses).',
      '- **Agro-climatology:** recording, analysing and forecasting weather and climate for farming.',
      '- **Land reclamation:** rehabilitating degraded land and bringing virgin land into farming.'),
    TB('who', 'Who would you call? Matching problems to branches', 32, ['Problem on the farm', 'Branch'],
       [['Tomato seedlings wilt in a nursery in Keren', 'Horticulture / plant protection'],
        ['Gullies cut through a field near Adi Keyh', 'Soil and water conservation'],
        ['Cows in a dairy near Asmara give little milk', 'Animal nutrition / breeding'],
        ['Farmers do not know a new barley variety', 'Agricultural extension'],
        ['Water stands in a banana field at Tesseney', 'Drainage engineering'],
        ['Deciding between onions and tomatoes for profit', 'Agricultural economics']], layout='terms'),
    WK('wk8', 'Worked example — why irrigation matters in Eritrea', 34,
       'Exercise 1.4 Q1: Why is irrigation important for agricultural development in Eritrea?',
       ['Start with the problem: rainfall is **low, erratic and short**, so rain-fed crops often fail.',
        'Irrigation supplies water when rain does not → **stable yields** and protection against drought.',
        'It allows **more than one crop a year** and high-value crops (vegetables, fruit, bananas at Tesseney).',
        'Efficient methods such as **drip irrigation** (Sawa-Afhimbol) save scarce water.'],
       'It overcomes low and erratic rainfall, stabilises yields, allows several crops a year and high-value crops, and saves water when done efficiently.'),
]

LESSONS = {'agri11-u1-l1-1': L1, 'agri11-u1-l1-2': L2, 'agri11-u1-l1-3': L3, 'agri11-u1-l1-4': L4, 'agri11-u1-l1-5': L5}

DROP = ['agri11-u1-c20', 'agri11-u1-c24']  # one-line summaries now covered in full by intro4 / intro5

PATCH = {
    'agri11-u1-l1-4-mx1': {'answer': 'D', 'why': 'The textbook (p. 25) lists war, poor marketing, lack of awareness and **inadequate agricultural inputs** as **socio-economic** factors. **Land tenure** is one of the **anthropogenic** factors (p. 20), together with land degradation, soil erosion and inappropriate land use. So land tenure is the one that is **not** socio-economic.'},
    'agri11-u1-chk8': {'q': 'Which of the following soil nutrients is a primary macronutrient, needed in large amounts and commonly supplied as urea?'},
}

# ------------------------------------------------------------------ practice
a = QSet('1.1–1.2 Practice — history and roles of agriculture', 's12')
a.M(1, 'The word "agriculture" comes from the Latin words "ager" and "cultura". What do they mean?', ['water and plant', 'soil/land and cultivation', 'animal and food', 'field and manage'], 'B',
    ['Step 1: "ager" means soil or land.', 'Step 2: "cultura" means cultivation or tilling.', 'Step 3: "field and manage" are the Greek roots of **agronomy** (agros, nomos), a trap.'],
    'Latin roots → agriculture; Greek roots → agronomy.', [('The Greek words "agros" and "nomos" form which word?', 'Agronomy (agros = field, nomos = to manage).')])
a.M(2, 'Which animal is believed to be the first one domesticated?', ['Goat', 'Horse', 'Dog', 'Cattle'], 'C',
    ['Step 1: The dog helped early hunters, guarded the camp and gave company.', 'Step 2: The goat probably came next, for food security.', 'Step 3: The horse was among the first tamed for draught and pack work.'],
    'Dog → goat → horse for draught: learn the order.', [('Which animal was probably domesticated second?', 'The goat.')])
a.M(3, 'Farming in Eritrea is believed to have started about', ['400 years ago', '1000 years ago', '4000 years ago', '40 000 years ago'], 'C',
    ['Step 1: The textbook (p. 3) gives about 4000 years.', 'Step 2: This is also Review Question 1.'], 'Four thousand — the same number as the 4 in "4 beats" of history.', [('Before people became farmers they were…', 'Hunters and gatherers.')])
a.S(3, 'Give two reasons why domesticated animals could be spread far from where they were first tamed.', 'They thrive under artificial (human-made) conditions and they reproduce regularly in confinement; they also adapt to new environments.',
    ['Step 1: Wild animals rarely breed in captivity; domesticated ones do.', 'Step 2: They can live on what people provide (feed, shelter).', 'Step 3: Over generations they adapt (e.g. heat-tolerant zebu cattle in Eritrea).'],
    'Think "captivity + breeding + adaptation".', [('Give one example of an animal adapted to a hot climate.', 'Zebu cattle such as the Barka breed, or the camel.')])
a.M(5, 'Which group lists only pulses?', ['Teff, barley, sorghum', 'Peas, beans, lentils', 'Sesame, groundnut, linseed', 'Onion, kale, tomato'], 'B',
    ['Step 1: Pulses are legumes grown for edible seeds.', 'Step 2: A = cereals, C = oil crops, D = vegetables.'], 'Pulses = the shiro and "ades" (lentil) foods.', [('Which group lists only oil crops? (a) sesame, Niger seed, linseed (b) wheat, millet, maize', '(a).')])
a.M(6, 'Molasses and oil-seed cake are', ['main products of the textile industry', 'by-products used as animal feed', 'types of fertilizer only', 'imported fuels'], 'B',
    ['Step 1: Molasses is left after sugar is made; oil-seed cake after oil is pressed.', 'Step 2: Both are rich feeds for cattle and sheep.'], 'By-product = what is left over after the main product.', [('Wheat bran is a by-product of which industry?', 'The flour mill; it is used as animal feed.')])
a.M(6, 'Malting barley is the raw material for', ['pasta', 'beer', 'sugar', 'edible oil'], 'B',
    ['Step 1: Barley grains are sprouted (malted) and brewed.', 'Step 2: Pasta is from wheat; sugar from cane/beet; oil from oil seeds.'], 'Match each raw material to one factory.', [('Which crop gives edible oil in Eritrea?', 'Sesame (also Niger seed, cottonseed).')])
a.S(5, 'How does agriculture earn foreign currency, and what is that currency used for?', 'By exporting farm products (live animals, hides and skins, meat, oil seeds such as sesame, cotton, fruit, flowers, gums and resins); the currency pays for imports such as petroleum, machinery, medicine and fertilizer.',
    ['Step 1: Exports are paid for in foreign money.', 'Step 2: Name products: live animals, sesame, hides, gum arabic.', 'Step 3: Name imports Eritrea cannot make: fuel, machinery, medicine, fertilizer.'],
    'Two halves: what goes out, what comes in.', [('Name two Eritrean farm exports.', 'Live animals and sesame (also hides and skins, gums).')])
a.TF(7, 'True or false: the pollination work of bees is a negative environmental effect of agriculture.', 'False',
    ['Step 1: Bees pollinate crops and wild plants.', 'Step 2: The textbook lists it as a **positive** effect, with afforestation, land reclamation and manure use.'], 'Negative = damage (deforestation, pollution); positive = repair or help.', [('Is overgrazing positive or negative?', 'Negative.')])
a.S(7, 'Explain how livestock act as a "bank" for an Eritrean farming family.', 'Animals store wealth: in a bad year or when money is needed (school fees, medicine, a wedding) the family sells an animal; the herd also grows by breeding, like savings earning interest.',
    ['Step 1: Few rural families have bank accounts.', 'Step 2: An animal can be sold at the market any week.', 'Step 3: Young animals add to the "savings".'], 'Insurance + savings + prestige.', [('Why do some herders keep very large herds?', 'Prestige and insurance — wealth is counted in animals.')])
a.F(8, 'The straw of sorghum and pearl millet is used for ____ and roofing.', 'fencing', ['fencing', 'fuel only', 'pasta', 'leather'],
    ['Step 1: Section 1.2.10: straw is used for fencing, house construction and roofing.'], 'Construction materials: wood + straw.', [('Wood from farms is used for houses, furniture and ____.', 'fence poles')])
a.S(8, 'Give three services draught animals give to Eritrean farmers.', 'Ploughing (oxen with the maresha), transport of people and goods (donkeys, camels, horses), and carrying water; also threshing by trampling.',
    ['Step 1: Think of the field: ploughing and threshing.', 'Step 2: Think of the road: transport to market.', 'Step 3: Think of the home: fetching water.'], 'Field, road, home.', [('Which animal carries goods across the hot lowlands?', 'The camel.')])

b = QSet('1.3 Practice — farming systems', 's13')
b.M(9, 'About what share of Eritrea\'s cultivated land is managed by subsistence smallholders and agro-pastoralists?', ['25 %', '50 %', '70 %', '95 %'], 'D',
    ['Step 1: Section 1.3 states about 95 per cent.', 'Step 2: Do not confuse with 70 % (share of the population that is agrarian) or 67 % (share in sedentary agro-pastoralism).'], 'Three numbers: 95 % land, 70 % people farm, 67 % sedentary.', [('What share of the population practises sedentary agro-pastoralism?', '67 %.')])
b.M(9, 'Which farming system has the largest share of the farming population?', ['Nomadic pastoralism', 'Semi-nomadic pastoralism', 'Sedentary agro-pastoralism', 'Commercial poultry'], 'C',
    ['Step 1: Table 1.1: nomadic 11 %, semi-nomadic 22 %, sedentary agro-pastoral 67 %.'], 'Each step down in movement doubles roughly: 11 → 22 → 67.', [('What share is nomadic?', '11 %.')])
b.M(10, 'Nomadic pastoralism in Eritrea is found mainly in', ['the central highlands', 'the Red Sea coastal areas and the north-western lowlands', 'around Asmara', 'the Sheeb spate area only'], 'B',
    ['Step 1: Nomadism needs very dry, thinly populated land (0.8–10 people/km²).', 'Step 2: That is the semi-desert coast and north-west.'], 'Dry + empty land → nomads.', [('Where is semi-nomadic pastoralism found?', 'In spate-irrigation areas such as Sheeb (Northern Red Sea).')])
b.M(10, 'In nomadic communities, cattle are kept mainly for', ['meat', 'milk', 'draught', 'hides'], 'B',
    ['Step 1: The textbook stresses milk as the main purpose.', 'Step 2: Male animals are sold to towns, but the herd is a milk herd.'], 'Nomads drink the herd, they do not eat it.', [('Which farming system supplies most male animals sold in towns?', 'Nomadic pastoralism.')])
b.S(11, 'What is transhumance? Give an Eritrean example.', 'The seasonal movement of people and livestock between zones, e.g. from the hot eastern lowlands up to the cool highlands in the hot season and back when the lowland rains come.',
    ['Step 1: It is a form of semi-nomadic life.', 'Step 2: It follows seasons, not random wandering.', 'Step 3: Example: herders of the escarpment and coast moving between lowland winter rains and highland summer rains.'], 'Trans = across; humus = ground: moving across zones.', [('Is transhumance random or seasonal?', 'Seasonal and regular.')])
b.M(13, 'The leading dairy breed in peri-urban dairies around Asmara is', ['Arado', 'Barka', 'Holstein-Friesian', 'White Leghorn'], 'C',
    ['Step 1: Peri-urban dairies use Holstein-Friesian and Holstein × local crosses.', 'Step 2: Arado and Barka are local zebu breeds; White Leghorn is a chicken.'], 'Holstein = black-and-white milk cow.', [('How much milk can a Holstein give where dairies are well developed?', '35–40 litres per day.')])
b.M(15, 'The White Leghorn can lay up to about', ['70 eggs a year', '120 eggs a year', '270 eggs a year', '700 eggs a year'], 'C',
    ['Step 1: Section 1.3 (p. 15): up to 270 eggs per year.', 'Step 2: Local free-range hens lay far fewer.'], 'Leghorn: hot-climate egg layer, about 270.', [('Name two common poultry diseases in Eritrea.', 'Newcastle disease and Gumboro (also Marek\'s disease).')])
b.S(12, 'Give three advantages and two disadvantages of mixed farming.', 'Advantages: crops feed animals and manure feeds crops; diverse produce and balanced diet; draught power; insurance in drought; steady cash. Disadvantages: overgrazing risk, high labour, costly to start, needs know-how in both, not possible in arid areas.',
    ['Step 1: Advantages come from the links between crops and animals.', 'Step 2: Disadvantages come from the extra work, cost and skill.'], 'Use Table 1.2 — two columns.', [('Why is mixed farming called "insurance"?', 'If crops fail in drought, animals can still be sold or give milk.')])
b.S(9, 'A district survey counts 1 500 farming households following the national pattern. How many are semi-nomadic?', '330 households',
    ['Step 1: Semi-nomadic share = 22 %.', 'Step 2: 0.22 × 1 500 = 330.'], 'Percent → decimal → multiply.', [('How many of 1 500 are sedentary agro-pastoral?', '0.67 × 1 500 = 1 005.')])
b.S(13, 'List four feeds used in peri-urban dairies and three diseases that threaten them.', 'Feeds: crop residues, hay, alfalfa, elephant grass, wheat bran, wheat middlings, sorghum husk, sesame cake. Diseases: tuberculosis, brucellosis, foot-and-mouth disease, mastitis.',
    ['Step 1: Roughages: residues, hay, alfalfa, elephant grass.', 'Step 2: Concentrates/by-products: bran, middlings, husk, sesame cake.', 'Step 3: Diseases from p. 14.'], 'Feeds = roughage + by-products.', [('Why do many dairy farmers depend on purchased feed?', 'They have no land to grow forage.')])
b.M(16, 'Which of these is a state farm that uses drip irrigation?', ['Sawa-Afhimbol Agro-Industries', 'A dessa village plot', 'A nomadic camp', 'A home garden'], 'A',
    ['Step 1: Figure 1.4 shows drip irrigation at Sawa-Afhimbol.', 'Step 2: Elabered and Alighidir are other large state farms.'], 'Remember three state farms: Elabered, Sawa-Afhimbol, Alighidir.', [('Name another large state farm.', 'Elabered (or Alighidir).')])

c = QSet('1.4 Practice — constraints', 's14')
c.M(18, 'Which is a yield-defining factor?', ['Nitrogen fertilizer', 'Irrigation water', 'Solar radiation', 'Stalk-borer'], 'C',
    ['Step 1: Defining factors are given and beyond the farmer\'s control.', 'Step 2: Nitrogen and water are limiting; stalk-borer is reducing.'], 'Ask: can the farmer change it?', [('Is a weed defining, limiting or reducing?', 'Reducing.')])
c.M(18, 'Water and plant nutrients are', ['yield-defining factors', 'yield-limiting factors', 'yield-reducing factors', 'socio-economic factors'], 'B',
    ['Step 1: They decide how close the crop comes to its best yield.', 'Step 2: The farmer can add them (irrigation, fertilizer).'], 'Limiting = something you can add.', [('Is the level of feeding in a dairy cow limiting or defining?', 'Limiting.')])
c.M(19, 'Striga is', ['an insect pest of barley', 'a parasitic weed on sorghum roots', 'a fungal disease of teff', 'a breed of goat'], 'B',
    ['Step 1: Striga (witchweed) attaches to sorghum roots and takes water and food.', 'Step 2: It is a biotic, yield-reducing factor.'], 'Striga = witchweed = sorghum\'s enemy.', [('Name a common weed in barley and wheat.', 'Wild oats.')])
c.S(19, 'Describe three features of Eritrean rainfall that make it a constraint.', 'It is low, unevenly distributed, and falls as heavy showers over a short period; it often starts early and stops before the crop has finished, so droughts recur.',
    ['Step 1: Amount: low.', 'Step 2: Distribution: uneven in space and time.', 'Step 3: Intensity: heavy showers → runoff and erosion rather than storage.'], 'Amount, distribution, intensity.', [('Why do heavy showers cause erosion?', 'Water falls faster than it can soak in, so it runs off carrying soil.')])
c.M(20, 'Which list contains only greenhouse gases?', ['O₂, N₂, Ar', 'CO₂, CH₄, N₂O, CFCs', 'H₂, He, O₃', 'N₂, CO₂, H₂O only'], 'B',
    ['Step 1: The textbook names CO₂, CH₄, CFCs and N₂O.', 'Step 2: Oxygen and nitrogen are not greenhouse gases.'], 'C-M-N-C: carbon dioxide, methane, nitrous oxide, CFCs.', [('Which greenhouse gas do ruminants release?', 'Methane (CH₄).')])
c.M(22, 'Under the traditional dessa system,', ['land belonged to the state', 'land belonged to the village and was redistributed', 'women had full land rights', 'land belonged to one kin group forever'], 'B',
    ['Step 1: dessa = village land, redistributed to residents.', 'Step 2: risti = kinship land; demaniale = state land.', 'Step 3: Women had no land rights under dessa.'], 'dessa = village; risti = kin; demaniale = state.', [('Which law gave all Eritreans, including women, usufruct rights?', 'Land Law No. 58 of 1994.')])
c.S(23, 'Why does redistributing land every 5–7 years discourage soil conservation?', 'A farmer will not spend years building terraces, check dams or planting trees on a plot that may be given to someone else at the next redistribution.',
    ['Step 1: Conservation works pay back slowly.', 'Step 2: Insecure tenure means the investor may lose the benefit.', 'Step 3: So farmers mine the soil instead of building it.'], 'Security of tenure → investment.', [('What has been tried to encourage tree planting?', 'Giving farmers tree tenure on government land.')])
c.S(24, 'A farmer has 1.5 ha in the highlands. Using the textbook range of 50–100 t/ha/year, what is the possible yearly soil loss?', 'Between 75 and 150 tonnes per year',
    ['Step 1: Minimum: 1.5 × 50 = 75 t.', 'Step 2: Maximum: 1.5 × 100 = 150 t.'], 'Multiply area by both ends of the range.', [('What about 4 ha in the moist lowlands (47 t/ha)?', '188 tonnes per year.')])
c.M(25, 'Which is NOT a socio-economic constraint?', ['Poor marketing', 'Lack of know-how', 'Effects of war', 'Soil erosion'], 'D',
    ['Step 1: Soil erosion is an **anthropogenic** factor (1.4.2).', 'Step 2: The other three are socio-economic (1.4.3).'], 'Anthropogenic list: degradation, tenure, erosion, land use.', [('Is land tenure socio-economic or anthropogenic in the textbook?', 'Anthropogenic.')])
c.S(21, 'Give four effects of land degradation.', 'Lower productivity per unit of input, fewer livestock, loss of vegetation cover, fuel-wood and wood shortage, loss of topsoil, ecological disruption.',
    ['Step 1: On crops: lower yields.', 'Step 2: On animals: less grazing, fewer animals.', 'Step 3: On the land: lost vegetation and topsoil.', 'Step 4: On people: fuel-wood shortage.'], 'Crops, animals, land, people.', [('Name three causes of land degradation.', 'Overgrazing, over-cultivation, deforestation.')])
c.S(26, 'Why can poor roads cause tomato prices to swing between seasons?', 'In the harvest season tomatoes flood nearby markets and prices fall, because farmers cannot reach distant markets or processing plants quickly; in the off-season supply is low and prices rise. Good roads and processing plants spread supply and steady the price.',
    ['Step 1: Tomatoes are perishable.', 'Step 2: Without roads they must be sold locally at once.', 'Step 3: Processing (paste) and transport would absorb the glut.'], 'Perishable + poor access = price swings.', [('What storage facilities prolong shelf life?', 'Refrigerators, cold rooms, atmosphere-controlled silos, warehouses.')])

d = QSet('1.5 Practice — branches of agricultural science', 's15')
d.M(30, 'Which branch deals with fruits, vegetables, flowers and spices?', ['Agronomy', 'Horticulture', 'Forestry', 'Aquaculture'], 'B',
    ['Step 1: Horticulture = garden crops (fruits, vegetables, ornamentals, spices, medicinal plants).', 'Step 2: Agronomy = field crops.'], 'Hortus = garden.', [('Which branch deals with cereals and pulses in the field?', 'Agronomy.')])
d.M(32, 'Removing excess water from the soil surface and upper subsoil is called', ['irrigation', 'drainage', 'mulching', 'terracing'], 'B',
    ['Step 1: Irrigation adds water; drainage removes excess water.'], 'Drain = take away.', [('Name two irrigation methods.', 'Furrow and drip (also basin, sprinkler, spate).')])
d.M(33, 'Which branch records and forecasts weather to help farmers?', ['Agro-climatology', 'Veterinary science', 'Land reclamation', 'Agricultural economics'], 'A',
    ['Step 1: Agro-climatology records, analyses and predicts weather and climate for production.'], 'Climate in the name.', [('Which branch rehabilitates degraded land?', 'Land reclamation.')])
d.S(32, 'Explain the difference between agricultural economics and agricultural extension.', 'Economics chooses the best combination of limited resources to maximise profit; extension educates farmers so they apply new knowledge.',
    ['Step 1: Economics = decisions about money and resources.', 'Step 2: Extension = teaching and communication with farmers.'], 'Economics decides; extension teaches.', [('Which branch reduces losses after harvest?', 'Post-harvest and food-processing engineering.')])
d.S(31, 'Where are fish kept in aquaculture? Name two other aquatic products.', 'In ponds, under controlled feeding and management; shrimps, crabs, lobsters or oysters.',
    ['Step 1: Aquaculture = fish farming.', 'Step 2: Ponds allow control of feed and water.'], 'Aqua = water + culture = farming.', [('Is aquaculture a plant or an animal science?', 'An animal science.')])
d.M(29, 'Which basic science is most important for plant and animal breeding?', ['Geography', 'Genetics', 'Physics', 'Accounting'], 'B',
    ['Step 1: Breeding is based on inheritance of traits.', 'Step 2: Genetics is the foundation of breeding (p. 29).'], 'Breeding = genes.', [('Which science helps in fertilizer formulation?', 'Chemistry.')])

QS = a.items + b.items + c.items + d.items

GLOSSARY = [
    ('Domestication', 'Bringing wild plants or animals under human control and breeding them for useful traits.', 2),
    ('Farming system', 'The way the parts of a farm (land, crops, animals, labour, capital) are linked together.', 9),
    ('Transhumance', 'Seasonal movement of people and livestock between zones, e.g. lowland to highland.', 11),
    ('Usufruct', 'The right to use land (and its products) without owning it.', 23),
    ('Yield-defining factor', 'A given condition beyond the farmer\'s control (sunlight, altitude, breed).', 18),
    ('Yield-limiting factor', 'An input that decides how close a crop or animal gets to its best yield (water, nutrients, feed).', 18),
    ('Yield-reducing factor', 'Something that takes away yield (pests, diseases, weeds, pollutants).', 18),
    ('Anthropogenic', 'Caused by human activity.', 20),
    ('Dessa', 'Traditional village land-tenure system with periodic redistribution.', 22),
]
TIPS = [('Three numbers: 95 % of cultivated land is smallholder; 70 % of people farm; 67 % are sedentary agro-pastoralists.', 9),
        ('Defining = given; limiting = add it; reducing = fight it.', 18)]
IDEAS = [('stages', 'Five stages of agriculture', 'l1_1', 'agri11-u1-ad-hist-fig'),
         ('systems', 'Nomadic 11 / semi 22 / sedentary 67 %', 'l1_3', 'agri11-u1-ad-sys-fig'),
         ('yield3', 'Defining, limiting, reducing', 'l1_4', 'agri11-u1-ad-yield')]
