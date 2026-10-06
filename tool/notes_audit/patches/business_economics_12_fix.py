import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *
B = Book('business_economics_12')
B.set('be12-u1-c05', problem=['A toy economy in 2010 produces only two final goods, all bought by households: 500 bicycles sold at 2,000 Nfa each and 500 radios sold at 200 Nfa each.', 'Calculate GDP.'],
      steps=[{'text': '**Given:** two final goods, their prices and quantities.'}, {'text': '**Required:** GDP.'},
             {'text': 'GDP = Σ (P × Q) for final goods only.'}, {'text': 'Bicycles = 500 × 2,000 = 1,000,000 Nfa.'},
             {'text': 'Radios = 500 × 200 = 100,000 Nfa.'}, {'text': 'GDP = 1,000,000 + 100,000 = **1,100,000 Nfa**.'},
             {'text': 'A longer table with more goods works the same way: multiply each final good’s price by its quantity and add.'}],
      answer='GDP = 1,100,000 Nfa')
B.set('be12-u1-c26', steps=[{'text': 'Current ≈ X − M = 40 − 55 = **−15** (deficit).'}, {'text': 'Capital net = 20 − 8 = **+12**.'},
      {'text': 'Overall ≈ −15 + 12 = **−3** (still a small deficit to finance from reserves or extra borrowing).'},
      {'text': 'If exports had been 45 instead, overall = −10 + 12 = +2 million (a surplus) — same arithmetic, different signs.'}],
      answer='Current account −15 million (deficit), capital account +12 million, overall about −3 million Nfa (small deficit).')
B.save()
