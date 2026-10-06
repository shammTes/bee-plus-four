import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *

B = Book('english_11')
for cid, key in (('eng11-u15-c01', 'rule'), ('eng11-u15-c02', 'body')):
    c = B.card(cid)
    arr = c[key]
    for i, s in enumerate(arr):
        if s.startswith('To construct a grammatically correct question tag') and not s.endswith('.'):
            arr[i] = s + ' — e.g. "She works here, *doesn\'t she*?", "They left early, *didn\'t they*?").'
        if s.startswith('Several irregular patterns') and s.rstrip().endswith('"Let\'s take a'):
            arr[i] = s.rstrip() + ' break, *shall we*?"). Imperatives usually take *will you?* or *won\'t you?* (e.g., "Close the door, *will you*?"), and statements with negative words such as *never, hardly, nobody* take a positive tag (e.g., "He never comes late, *does he*?").'
B.save()

B = Book('geography_11')
B.set('geo11-u2-c18', body=['**Gradation** is the levelling of the land surface by **degradation** (wearing down: weathering and erosion) and **aggradation** (building up by deposition). Agents: running water, wind, moving ice (glaciers), waves and groundwater; gravity also moves material downslope (mass wasting).'])
B.set('geo11-u3-c10', rows=[
    ['Cliff and wave-cut platform', 'Waves undercut the cliff at its base (wave-cut notch); the overhang collapses and the cliff retreats, leaving a gently sloping rock wave-cut platform at its foot.'],
    ['Headland and bay', 'Where hard and soft rocks alternate, soft rock is eroded into bays; hard rock remains as headlands.'],
    ['Cave → arch → stack → stump', 'Waves erode a crack into a cave; caves on both sides of a headland meet as an arch; the arch roof collapses leaving a stack, which is worn down to a stump.']])
B.save()

B = Book('geography_12')
B.set('geo12-u6-wrk7', steps=[{'text': '**Step 1: Recall the energy sources used in Eritrea**'},
      {'text': 'Traditional biomass energy sources (firewood, charcoal, dung and crop residues) account for about three-fourths ($$75\\%$$) of the total energy consumption in the country.'},
      {'text': '**Step 2: Conclude**'}, {'text': 'The proportion is $$75\\%$$ — which is why deforestation and the search for alternatives (solar, wind, geothermal, biogas) matter so much.'}],
      answer='About three-fourths (75 %)')
B.save()
