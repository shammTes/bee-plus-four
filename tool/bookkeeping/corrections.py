"""Figure corrections applied to tables.json before the notes are built (build_notes.py).

Every bookkeeping table was checked against the textbook PDF and re-added up: journals (each entry Dr = Cr), ledgers
(running balance line by line), trial balances, worksheets, special-journal footings and the financial statements.
The entries below are the places where the printed book (or the PDF extraction) is wrong; each says why.
Keys are (grade, table number in tables.json order, 1-based) plus the start of the title as a guard.
"""
import re

DASHES = re.compile(r'^_+$')


def clean_cell(c):
    """underline marks copied from the book ('______', '__350'), stray © for (c)"""
    c = c or ''
    if DASHES.match(c.strip()):
        return ''
    c = re.sub(r'^_+|_+$', '', c.strip()) if '_' in c else c
    return c.replace('©', '(c)')


def clean_text(s):
    """'A c c u m u l a t e d' / 'P o s t.' -> 'Accumulated' / 'Post.' (letters spaced out in the PDF)"""
    s = re.sub(r'\b(?:[A-Za-z] ){3,}[A-Za-z]\b\.?', lambda m: m.group(0).replace(' ', ''), s)
    s = re.sub(r'(\w) +,', r'\1,', s)  # 'Semhar , Drawing' -> 'Semhar, Drawing'
    s = re.sub(r'\b(Returns)\s*And\s+(allow|all)\.', r'\1 and Allow.', s)  # 'Sales ReturnsAnd allow.' -> 'Sales Returns and Allow.'
    return s


def _set(t, row, col, old, new):
    assert t['rows'][row][col] == old, (t['title'], row, col, t['rows'][row][col], old)
    t['rows'][row][col] = new


def fix10_17(t):
    # the PDF extraction dropped the Automobiles line (the book prints it; Total Assets 1,015,000 needs it)
    left = [r[:2] for r in t['rows'][:-1]]
    right = [r[2:] for r in t['rows'][:-1]]
    left.insert(2, ['Automobiles', '740,000.00'])
    right += [['', '']] * (len(left) - len(right))
    t['rows'] = [a + b for a, b in zip(left, right)] + [t['rows'][-1]]


def fix10_22(t):
    # book prints "Increase 900.000" (a full stop for the thousands comma)
    for r in t['rows']:
        r[1], r[2] = r[1].replace('900.000', '900,000'), r[2].replace('900.000', '900,000')


def fix10_23(t):
    # book prints "1,015,000" and "Balance 900,000" on the Cash debit side; after transaction 1 Cash is 1,045,000
    _set(t, 0, 1, '1,015,000 (printed); Balance 900,000 (printed)', 'Balance 1,045,000')


def fix10_47(t):
    # the footings were extracted with two figures in the header row
    t['head'] = ['Debit footings', 'Nakfa', 'Credit footings', 'Nakfa']
    t['rows'] = [['Cash Debit', '1,105,000', 'General Credit', '905,000'],
                 ['General Debit', '145,000', 'Fares Earned Credit', '200,000'],
                 ['', '', 'Cash Credit', '145,000'],
                 ['Total debits', '1,250,000', 'Total credits', '1,250,000']]


def fix10_wages(t):
    # book prints Wages Expense 50,000 here; it is 55,000 (journal, ledger, trial balance; the General Debit total 145,000)
    for r in t['rows']:
        if r[3] == 'Wages Expense':
            assert r[1] == '50,000.00'
            r[1] = '55,000.00'


def fix10_72(t):
    # book prints Automobiles "74,000" (it is 740,000, so book value 733,833) and labels every line "-Automobiles"
    t['rows'] = [['Automobiles', '740,000', ''],
                 ['Less: Accumulated Depreciation – Automobiles', '6,167', '733,833'],
                 ['Furniture and Fixtures', '10,000', ''],
                 ['Less: Accumulated Depreciation – Furniture and Fixtures', '83', '9,917'],
                 ['Office Equipment', '95,000', ''],
                 ['Less: Accumulated Depreciation – Office Equipment', '1,583', '93,417']]


def fix10_75(t):
    _set(t, 0, 1, 'Nakfa 19,600', '19,600')


def fix10_78(t):
    # assets are shown net of accumulated depreciation (7,833), so both totals are 2,062,167, not the printed 2,070,000
    # (1,105,000 + 120,000 + 733,833 + 9,917 + 93,417 = 135,000 + 1,927,167 = 2,062,167)
    _set(t, 5, 2, '9917.00', '9,917.00')
    _set(t, 8, 2, '2,070,000.00', '2,062,167.00')
    _set(t, 8, 4, '2,070,000.00', '2,062,167.00')


def fix10_81(t):
    # the book's figure swaps Salaries (55,000) and Rent (5,000), leaves Utilities Expense (2,500) out, and prints a
    # meaningless 114,000 in Income Summary. Rebuilt from the closing entries (Table 79) and the ledgers (Tables 82-88).
    t['rows'] = [
        ['Salaries Expense', 'Balance 55,000', 'Income Summary 55,000', '0'],
        ['Rent Expense', 'Balance 5,000', 'Income Summary 5,000', '0'],
        ['Utilities Expense', 'Balance 2,500', 'Income Summary 2,500', '0'],
        ['Miscellaneous Expense', 'Balance 7,500', 'Income Summary 7,500', '0'],
        ['Supplies Expense', 'Balance 10,000', 'Income Summary 10,000', '0'],
        ['Depreciation Expense', 'Balance 7,833', 'Income Summary 7,833', '0'],
        ['Fares Earned', 'Income Summary 200,000', 'Balance 200,000', '0'],
        ['Income Summary', 'Salaries Expense 55,000; Rent Expense 5,000; Utilities Expense 2,500; Miscellaneous Expense 7,500; '
                           'Supplies Expense 10,000; Depreciation Expense 7,833; Dehab Capital 112,167', 'Fares Earned 200,000', '0'],
        ['Dehab Capital', '', 'Balance 1,815,000; Income Summary 112,167', '1,927,167'],
    ]


def fix10_97(t):
    # accumulated depreciation on furniture is 83.00 (extracted as 8,300)
    _set(t, 5, 2, '8,300', '83.00')


def fix11_53(t):
    t['head'] = [clean_text(h) for h in t['head']]


def fix11_58(t):
    # the adjusted trial balance totals are 251,673.00 (the book prints 231,673.00); the book also leaves rows 14-29 of
    # the adjusted columns blank — filled in exactly as in the full worksheet (Table 59)
    ext = {13: ('', '70,400.00'), 14: ('1,750.00', ''), 15: ('691.50', ''), 16: ('46,600.00', ''), 17: ('', '1,800.00'),
           18: ('', '340.00'), 19: ('450.00', ''), 20: ('4,000.00', ''), 21: ('850.00', ''), 22: ('100.00', ''), 23: ('935.00', ''),
           24: ('280.00', ''), 25: ('2,850.00', ''), 26: ('500.00', ''), 27: ('1,000.00', ''), 28: ('833.00', '')}
    for i, (d, c) in ext.items():
        assert t['rows'][i][6] == '' and t['rows'][i][7] == ''
        t['rows'][i][6], t['rows'][i][7] = d, c
    _set(t, 29, 6, '231,673.00', '251,673.00')
    _set(t, 29, 7, '231,673.00', '251,673.00')


def fix11_59(t):
    _set(t, 13, 7, '70,400', '70,400.00')
    _set(t, 14, 6, '1750', '1,750.00')


def fix11_61(t):
    # gross profit = net sales 67,958.50 − cost of goods sold 46,410.00 = 21,548.50 (the book prints 1,548.50;
    # 21,548.50 − 11,348.00 operating expenses = the 10,200.50 net income)
    _set(t, next(i for i, r in enumerate(t['rows']) if r[0] == 'Gross Profit'), 4, '1,548.50', '21,548.50')


CORRECTIONS = {
    ('10', 17, 'Dehab Taxi Service — Balance Sheet'): fix10_17,
    ('10', 22, 'T-accounts: additional investment'): fix10_22,
    ('10', 23, 'T-accounts: office equipment'): fix10_23,
    ('10', 47, 'Proving the cash journal'): fix10_47,
    ('10', 48, 'Cash Journal Page 1 — totals'): fix10_wages,
    ('10', 52, 'Cash Journal Page 1 — after posting'): fix10_wages,
    ('10', 72, 'Accumulated depreciation deducted'): fix10_72,
    ('10', 75, 'Trial Balance, October 31'): fix10_75,
    ('10', 78, 'Dehab Taxi Service — Balance Sheet, September 30'): fix10_78,
    ('10', 81, 'Closing entries shown in T-accounts'): fix10_81,
    ('10', 97, 'Dehab Taxi Service — Post-Closing'): fix10_97,
    ('11', 53, 'Purchase Returns'): fix11_53,
    ('11', 58, ''): fix11_58,
    ('11', 59, 'Asmara Shoes and Clothing Business Worksheet'): fix11_59,
    ('11', 61, 'Asmara Shoes and Clothing Business Income Statement'): fix11_61,
}


def apply(data):
    """clean every cell, then apply the corrections; returns the number of tables changed"""
    n = 0
    for g, tabs in data.items():
        for k, t in enumerate(tabs, 1):
            before = repr((t['head'], t['rows']))
            t['rows'] = [[clean_text(clean_cell(c)) for c in r] for r in t['rows']]
            for (gg, kk, title), f in CORRECTIONS.items():
                if gg == g and kk == k:
                    assert t['title'].startswith(title), (g, k, t['title'])
                    f(t)
            n += before != repr((t['head'], t['rows']))
    return n
