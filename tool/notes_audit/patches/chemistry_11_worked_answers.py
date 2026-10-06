import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *
B = Book('chemistry_11')
def addsteps(cid, extra, ans):
    c = B.card(cid)
    if not any(s.get('text') == extra[-1] for s in c['steps']):
        c['steps'] = c['steps'] + [{'text': t} for t in extra]
    c['answer'] = ans
B.card('chem11-u1-wrk1')['answer'] = 'When the rate of the forward reaction equals the rate of the reverse reaction'
addsteps('chem11-u2-wrk1', ['$$2 + x - 8 = 0 \\Rightarrow x = +6$$'], 'Sulphur has oxidation number +6')
addsteps('chem11-u3-wrk1', ['The reactant is methanoic (formic) acid, HCOOH; concentrated H₂SO₄ removes H₂O from it.'], 'Methanoic (formic) acid, HCOOH')
addsteps('chem11-u3-wrk2', ['**Step 3: Choose the compromise**', 'Industry uses about 200 atm and a moderate temperature of about 450 °C with an iron catalyst: a reasonable yield obtained at a fast enough rate.'],
         'High pressure (about 200 atm) and a moderate temperature (about 450 °C) with an iron catalyst')
B.card('chem11-u4-wrk1')['answer'] = 'Sodium (electrolysis of molten NaCl in the Downs cell)'
B.card('chem11-u4-wrk2')['answer'] = 'Bauxite, Al₂O₃·xH₂O'
B.save()
