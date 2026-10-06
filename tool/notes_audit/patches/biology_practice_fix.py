"""Add the energy-value table that the imported practice questions rely on; reword table/pro-tip references."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *
from subs import apply
B = Book('biology_10')
lid = B.d['units'][0]['lessons'][0]['id']
if not any(c['id'] == 'bio10-u1-energy-tbl' for l in B.d['units'][0]['lessons'] for c in l['cards']):
    B.add(lid, [table('bio10-u1-energy-tbl', 'Energy released by nutrients (Table 1.1)', ['Nutrient', 'Energy released per gram'],
        [['Carbohydrate', '17.1 kJ/g'], ['Protein', '22.0 kJ/g'], ['Lipid (fat/oil)', '38.0 kJ/g'], ['Water, vitamins, minerals', '0 kJ/g (no energy)']], src='notes'),
        text('bio10-u1-energy-txt', 'Using the energy table', ['Energy from a food = mass of each nutrient (g) × its energy value (kJ/g), added together. Example: 10 g fat gives 10 × 38.0 = 380 kJ, more than twice the energy of 10 g of carbohydrate (171 kJ).'], src='notes')])
B.save()
apply('biology_10', [('Table 1.1 gives', 'The energy table (Table 1.1 in this unit) gives'), ('From Table 1.1,', 'From the energy table (Table 1.1 in this unit),'),
                     ('from Table 1.1', 'from the energy table (Table 1.1 in this unit)'), ('of Table 1.1', 'in the energy table (Table 1.1 in this unit)'),
                     ('in Table 1.1 (', 'in the energy table (Table 1.1 in this unit) (')], strict=False)
apply('biology_11', [("The unit's Pro-Tip gives SEVEN UP:", 'The memory aid SEVEN UP gives the path of sperm:')], strict=False)
