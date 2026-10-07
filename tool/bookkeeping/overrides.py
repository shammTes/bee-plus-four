"""Hand transcriptions for the textbook tables that pdfplumber cannot read cleanly.

Keys are (grade, index into the automatic extraction) -> list of replacement tables (an empty list drops the
table). ADDED holds the textbook tables that have no ruling lines, so the automatic extraction misses them.
Figures are copied exactly as printed, including the textbook's own slips; the step-by-step explanation
points those out.
"""
GJ = ['Date', 'Account Title', 'P/R', 'Debit', 'Credit']
LG = ['Date', 'Item', 'P/R', 'Debit', 'Credit', 'Balance']
CJ = ['Cash Debit', 'General Debit', 'Date', 'Account Title', 'No', 'PR', 'General Credit', 'Fares Earned Credit', 'Cash Credit']
GL11 = ['Date (2010)', 'Explanation', 'Post. Ref.', 'Debit', 'Credit', 'Balance']


def T(title, head, rows, page, kind=None):
    t = {'title': title, 'head': head, 'rows': rows, 'page': page}
    if kind:
        t['kind'] = kind
    return t


OPEN_DR = [['Current year Sept. 1', 'Cash', '', '145,000.00', ''], ['', 'Supplies', '', '65,000.00', ''],
           ['', 'Automobiles', '', '740,000.00', ''], ['', 'Furniture and Fixtures', '', '15,000.00', ''],
           ['', 'Office Equipment', '', '50,000.00', ''], ['', 'Accounts Payable', '', '', '75,000.00'],
           ['', 'Taxes Payable', '', '', '25,000.00'], ['', 'Dehab’s Capital', '', '', '915,000.00'],
           ['', '(Sept. 1 Balance sheet)', '', '', '']]
BS_HEAD = ['Assets', 'Amount (Nakfa)', 'Liabilities and Capital', 'Amount (Nakfa)']
BS1 = [['Cash', '145,000.00', 'Accounts Payable', '75,000.00'], ['Supplies', '65,000.00', 'Taxes Payable', '25,000.00'],
       ['Automobiles', '740,000.00', 'Total Liabilities', '100,000.00'], ['Furniture and fixtures', '15,000.00', 'Capital', ''],
       ['Office Equipment', '50,000.00', 'Dehab’s Capital', '915,000.00'],
       ['Total Assets', '1,015,000.00', 'Total Liabilities and Capital', '1,015,000.00']]
J2_3 = [['2', 'Cash', '11', '900,000.00', ''], ['', 'Dehab’s Capital', '31', '', '900,000.00'], ['', '(Receipt No.1)', '', '', ''],
        ['5', 'Office Equipment', '15', '45,000.00', ''], ['', 'Cash', '11', '', '45,000.00'], ['', 'Cheque No.1', '', '', ''],
        ['10', 'Supplies', '12', '65,000.00', ''], ['', 'Accounts Payable', '21', '', '65,000.00'], ['', '(Invoice No.1)', '', '', '']]
CJ_ROWS = [['900,000.00', '', 'C/Y Sept 2', 'Dehab’s Capital', 'R1', '', '900,000.00', '', ''],
           ['', '45,000.00', '5', 'Office Equipment', 'Ck1', '', '', '', '45,000.00'],
           ['', '30,000.00', '15', 'Accounts Payable', 'Ck2', '', '', '', '30,000.00'],
           ['5,000.00', '', '20', 'Furniture & fixtures', 'R2', '', '5,000.00', '', ''],
           ['200,000.00', '', '30', '', '', '', '', '200,000.00', '']]


def cj(wages, posted=False, refs=False):
    pr = (lambda a: a) if posted else (lambda a: '')
    rows = [list(r) for r in CJ_ROWS]
    if posted:
        for r, p in zip(rows, ['31', '15', '21', '14', '']):
            r[5] = p
        rows[4][3], rows[4][4] = '√', 'R3'
    rows += [['', wages, '30', 'Wages Expense', 'Ck3' if posted else '', pr('51'), '', '', '70,000.00'],
             ['', '5,000.00', '', 'Rent Expense', 'Ck4' if posted else '', pr('52'), '', '', ''],
             ['', '2,500.00', '', 'Utilities Expense', 'Ck5' if posted else '', pr('53'), '', '', ''],
             ['', '7,500.00', '', 'Miscellaneous Expense', 'Ck6' if posted else '', pr('54'), '', '', ''],
             ['1,105,000.00', '145,000.00', '30', 'Totals', '', '', '905,000.00', '200,000.00', '145,000.00']]
    if refs:
        rows.append(['(11)', '(√)', '', '', '', '', '(√)', '(41)', '(11)'])
    return rows


OVERRIDES = {
    ('10', 3): [T('Dehab Taxi Service — Balance Sheet, September 1, current year', BS_HEAD, BS1, 67)],
    ('10', 9): [T('General Journal Page 1 — opening entry, Cash posted (P/R 11)', GJ,
                  [[r[0], r[1], '11' if r[1] == 'Cash' else '', r[3], r[4]] for r in OPEN_DR], 74),
                T('Account Title: Cash — Account Number 11 (after posting the opening entry)', LG,
                  [['C/Y Sept. 1', 'Balance', 'J1', '145,000.00', '', '145,000.00']], 74)],
    ('10', 16): [T('Dehab Taxi Service — Balance Sheet, September 1, current year (source of the opening entry)', BS_HEAD,
                   [r for r in BS1 if r[2] != 'Total Liabilities'] , 77),
                 T('General Journal — opening entry recorded from the balance sheet', GJ,
                   [['C/Y Sept 1' if i == 0 else '', r[1], '', r[3], r[4]] for i, r in enumerate(OPEN_DR)], 77)],
    ('10', 36): [T('General Journal Page 2 — Sept. 2 entry posted', GJ, J2_3[:3], 105),
                 T('Account Title: Cash — Account Number 11', LG,
                   [['Current Sept. 1', 'Balance', 'J1', '145,000.00', '', '145,000.00'], ['2', '', 'J2', '900,000.00', '', '1,045,000.00']], 105),
                 T('Account Title: Dehab Capital — Account Number 31', LG,
                   [['Current Sept. 1', 'Balance', 'J1', '', '915,000.00', '915,000.00'], ['2', '', 'J2', '', '900,000.00', '1,815,000.00']], 105)],
    ('10', 38): [T('Account Title: Office Equipment — Account Number 15', LG,
                   [['Current Sept. 1', 'Balance', 'J1', '50,000.00', '', '50,000.00'], ['5', '', 'J2', '45,000.00', '', '95,000.00']], 105),
                 T('Account Title: Cash — Account Number 11 (after the Sept. 5 posting)', LG,
                   [['Current Sept. 1', 'Balance', 'J1', '145,000.00', '', '145,000.00'], ['2', '', 'J2', '900,000.00', '', '1,045,000.00'],
                    ['5', '', '', '', '45,000.00', '1,000,000.00']], 105)],
    ('10', 39): [T('General Journal Page 2 — first three entries posted', GJ, J2_3, 106),
                 T('Account Title: Supplies — Account Number 12', LG,
                   [['Current Sept. 1', 'Balance', 'J1', '65,000.00', '', '65,000.00'], ['10', '', 'J2', '65,000.00', '', '130,000.00']], 106)],
    ('10', 40): [T('Account Title: Accounts Payable — Account Number 21', LG,
                   [['Current Sept. 1', 'Balance', 'J1', '', '75,000.00', '75,000.00'], ['10', '', 'J2', '', '65,000.00', '140,000.00']], 106)],
    ('10', 42): [T('Account Title: Cash — Account Number 11', LG,
                   [['C/Y Sept. 1', 'Bal', 'J1', '145,000.00', '', '145,000.00'], ['2', '', 'J2', '900,000.00', '', '1,045,000.00'],
                    ['5', '', 'J2', '', '45,000.00', '1,000,000.00'], ['15', '', 'J2', '', '30,000.00', '970,000.00'],
                    ['20', '', 'J2', '5,000.00', '', '975,000.00'], ['30', '', 'J2', '200,000.00', '', '1,175,000.00'],
                    ['30', '', 'J2', '', '70,000.00', '1,105,000.00']], 107)],
    ('10', 44): [T('Account Title: Automobiles — Account Number 13', LG, [['C/Y Sept. 1', 'Balance', 'J1', '740,000.00', '', '740,000.00']], 108)],
    ('10', 45): [T('Account Title: Furniture and Fixtures — Account Number 14', LG,
                   [['C/Y Sept. 1', 'Balance', 'J1', '15,000.00', '', '15,000.00'], ['20', '', 'J2', '', '5,000.00', '10,000.00']], 108)],
    ('10', 49): [T('Account Title: Dehab Capital — Account Number 31', LG,
                   [['C/Y Sept. 1', 'Balance', 'J1', '', '915,000.00', '915,000.00'], ['2', '', 'J2', '', '900,000.00', '1,815,000.00']], 108)],
    ('10', 53): [T('Account Title: Utilities Expenses — Account Number 53', LG, [['C/Y Sept. 30', '', 'J2', '25,000.00', '', '25,000.00']], 109)],
    ('10', 54): [T('Account Title: Miscellaneous Expenses — Account Number 54', LG, [['C/Y Sept. 30', '', 'J2', '7,500.00', '', '7,500.00']], 109)],
    ('10', 62): [T('Cash Journal Page 1 — all September transactions, footed', CJ, cj('55,000.00'), 116)],
    ('10', 64): [T('Cash Journal Page 1 — totals ready for posting', CJ, cj('50,000.00', refs=True), 117),
                 T('Account Title: Cash — Account Number 11 (special-column totals posted)', LG,
                   [['C/Y Sept. 1', 'Balance', 'J1', '145,000', '', '145,000'], ['30', '', 'C1', '1,105,000', '', '1,250,000'],
                    ['30', '', 'C1', '', '145,000', '1,105,000']], 117),
                 T('Account Title: Fares Earned — Account Number 41', LG, [['C/Y Sept. 30', '', 'C1', '', '200,000.00', '200,000.00']], 117)],
    ('10', 65): [T('Account Title: Dehab Capital — Account Number 31 (General Credit amount posted)', LG,
                   [['C/Y Sept. 1', 'Balance', 'J1', '', '915,000.00', '915,000.00'], ['2', '', 'C1', '', '900,000.00', '1,815,000.00']], 118)],
    ('10', 66): [T('Cash Journal Page 1 — after posting (account numbers in the PR column)', CJ, cj('50,000.00', posted=True, refs=True), 119)],
    ('10', 68): [T('Account Title: Cash — Account Number 11', LG,
                   [['C/Y Sept. 1', 'Balance', 'J1', '145,000', '', '145,000'], ['30', '', 'C1', '1,105,000', '', '1,250,000'],
                    ['30', '', 'C1', '', '145,000', '1,105,000']], 119)],
    ('10', 70): [T('Account Title: Automobiles — Account Number 13', LG, [['C/Y Sept. 1', 'Balance', 'J1', '740,000.00', '', '740,000.00']], 119)],
    ('10', 75): [T('Account Title: Dehab Capital — Account Number 31', LG,
                   [['C/Y Sept. 1', 'Balance', 'J1', '', '915,000.00', '915,000.00'], ['2', '', 'C2', '', '900,000.00', '1,815,000.00']], 120)],
    ('10', 93): [T('Dehab Taxi Service — Balance Sheet, September 30, current year', ['Assets', '', 'Nakfa', 'Liabilities and Capital', 'Nakfa'],
                   [['Cash', '', '1,105,000.00', 'Liabilities', ''], ['Supplies', '', '120,000.00', 'Accounts Payable', '110,000.00'],
                    ['Automobiles', '740,000', '', 'Taxes Payable', '25,000.00'], ['Less: Accu. Dep', '-6,167', '733,833.00', 'Total Liabilities', '135,000.00'],
                    ['Furniture & fixtures', '10,000', '', '', ''], ['Less: Accu. Dep', '-83', '9917.00', '', ''],
                    ['Office Equipment', '95,000', '', 'Capital', ''], ['Less: Accu. Dep', '-1,583', '93,417.00', 'Dehab’s Capital', '1,927,167.00'],
                    ['Total Assets', '', '2,070,000.00', 'Total Liabilities and Capital', '2,070,000.00']], 139, kind='statement')],
    ('10', 98): [T('Closing entries shown in T-accounts (amounts carried to Income Summary and Dehab Capital)',
                   ['Account', 'Debit side', 'Credit side', 'Balance after closing'],
                   [['Salaries Expense', '5,000', '5,000', '0'], ['Miscellaneous Expense', '7,500', '7,500', '0'],
                    ['Supplies Expense', '10,000', '10,000', '0'], ['Rent Expense', '55,000', '55,000', '0'],
                    ['Depreciation Expense', '7,833', '7,833', '0'], ['Fares earned', '200,000', '200,000', '0'],
                    ['Income Summary', '5,000; 7,500; 10,000; 5,000; 7,833; 112,167', '200,000; 114,000 (as printed)', '0'],
                    ['Dehab Capital', '', '1,815,000; 112,167', '1,927,167'], ['Dehab’s Drawing', '0', '', '0']], 142, kind='taccount')],
    ('10', 102): [T('Account Title: Utilities Expenses — Account Number 53 (closed)', LG,
                    [['Current Sept. 30', '', 'J2', '25,000.00', '', '25,000.00'], ['', '', 'J3', '', '25,000.00', '0.00']], 143)],
    ('11', 1): [T('Asmara Shoe and Clothing Business — Purchases Journal Page 1 (posted)', ['Date', 'Account Credited', 'Credit Terms', 'Post Ref.', 'Purchases Dr. / Accounts Payable Cr.'],
                  [['2010 Jan. 1', 'Bana', '2/10.n/30', '√', '15,000'], ['11', 'Gash Setit', '2/10.n/30', '√', '12,000'],
                   ['19', 'Selam', '2/10.n/30', '√', '3,200'], ['22', 'Denden', '2/10.n/30', '√', '3,000'],
                   ['26', 'Fenkil', '2/10.n/30', '√', '1,900'], ['', 'Total', '', '(51)/(22)', '35,100']], 71)],
    ('11', 2): [T('Accounts Payable Subsidiary Ledger — Bana', GL11, [['Jan. 1', '', 'PJ1', '', '15,000', '15,000']], 71)],
    ('11', 3): [T('General Ledger — Purchases 51', GL11, [['Jan. 31', '', 'PJ1', '35,100', '', '35,100']], 71)],
    ('11', 4): [T('Accounts Payable Subsidiary Ledger — Denden', GL11, [['Jan. 22', '', 'PJ1', '', '3,000', '3,000']], 71),
                T('General Ledger — Accounts Payable 22', GL11, [['Jan. 31', '', 'PJ1', '', '35,100', '35,100']], 71)],
    ('11', 56): [T('Asmara Shoe and Clothing Business — General Journal Page 5 (Exhibit 2.17)', ['Date (2010)', 'Account Title and Explanation', 'Post. Ref.', 'Debit', 'Credit'],
                   [['January 3', 'Delivery Equipment', '17', '50,000.00', ''], ['', 'Accounts Payable – Nejat', '22/√', '', '50,000.00'],
                    ['', '(To record the purchase of a Delivery Equipment on account from Nejat)', '', '', ''],
                    ['6', 'Accounts Payable – Bana', '22/√', '1,000.00', ''], ['', 'Purchase Returns and Allowances', '52', '', '1,000.00'],
                    ['', '(To record the return of merchandise previously purchased on account from Bana)', '', '', ''],
                    ['10', 'Sales Returns and Allowances', '42', '300.00', ''], ['', 'Accounts Receivable – Mereb', '12/√', '', '300.00'],
                    ['', '(To record the of merchandise previously sold on account to Mereb)', '', '', ''],
                    ['16', 'Supplies', '13', '1,200.00', ''], ['', 'Accounts Payable – Amna', '22/√', '', '1,200.00'],
                    ['', '(To record the purchase of supplies on account from Amna)', '', '', ''],
                    ['20', 'Accounts Payable – Gash-Setit', '22/√', '800.00', ''], ['', 'Purchase Returns and Allowances', '52', '', '800.00'],
                    ['', '(To record the return of merchandise previously purchased on account from Gash-Setit)', '', '', ''],
                    ['21', 'Sales Returns and Allowances', '42', '1,450.00', ''], ['', 'Accounts Receivable – Busha', '12/√', '', '1,450.00'],
                    ['', '(To record the merchandise previously sold on account to Busha)', '', '', '']], 103)],
    ('11', 114): [T('Ato Haile Grocery Shop — partial worksheet', ['Account Title', 'Income Statement Debit', 'Income Statement Credit', 'Balance Sheet Debit', 'Balance Sheet Credit'],
                    [['Haile’s Capital', '', '', '', '17,000.00'], ['Haile’s Drawing', '', '', '500.00', ''],
                     ['Income Summary', '8,000.00', '7,000.00', '', ''], ['Sales', '', '7,800.00', '', ''], ['Purchases', '4,200.00', '', '', ''],
                     ['Insurance Expense', '50.00', '', '', ''], ['Miscellaneous Expense', '80.00', '', '', ''], ['Rent Expense', '400.00', '', '', ''],
                     ['Salary Expense', '720.00', '', '', ''], ['Supplies Expense', '85.00', '', '', ''],
                     ['', '13,535.00', '14,800.00', '22,265.00', '21,000.00'], ['Net Income', '1,265.00', '', '', '1,265.00'],
                     ['', '14,800.00', '14,800.00', '22,265.00', '22,265.00']], 138, kind='worksheet')],
}
for i in (77, 78, 79, 80, 81):
    OVERRIDES[('11', i)] = None  # header-less adjusting-entry pieces: same rows as the combined table #82, re-headed below

ADDED = {
    '10': [
        T('Financial worth of Lia', ['Item owned', 'Nakfa'], [['Money in pocket', '25.00'], ['Cash in bank', '100.00'], ['Clothes', '190.00'],
                                                         ['Books', '250.00'], ['Total property owned', '565.00']], 64, kind='statement'),
        T('What Zeineb owns', ['Item owned', 'Nakfa'], [['Money in pocket', '50.00'], ['Cash in bank', '100.00'], ['Clothes', '1,000.00'],
                                                       ['Bicycle', '750.00'], ['Mobile phone', '3,000.00']], 64, kind='statement'),
        T('T-accounts: additional investment (Transaction 1)', ['Account', 'Debit side', 'Credit side'],
          [['Cash (asset)', 'Balance 145,000; Increase 900.000; new balance 1,045,000', ''],
           ['Capital', '', 'Balance 915,000; Increase 900.000; new balance 1,815,000']], 95, kind='taccount'),
        T('T-accounts: office equipment bought for cash (Transaction 2)', ['Account', 'Debit side', 'Credit side'],
          [['Cash', '1,015,000 (printed); Balance 900,000 (printed)', 'Decrease 45,000'], ['Office Equipment', 'Increase 45,000', '']], 95, kind='taccount'),
        T('Accounts after the depreciation adjustment is posted', ['Account', 'Debit balance', 'Credit balance'],
          [['Automobiles', '740,000', ''], ['Accumulated Depreciation- Automobiles', '', '6,167'], ['Depreciation Expense', '7,833', ''],
           ['Furniture and Fixtures', '10,000', ''], ['Accumulated Depreciation- Furniture and Fixtures', '', '83'],
           ['Office Equipment', '95,000', ''], ['Accumulated Depreciation- Office Equipment', '', '1,583']], 132, kind='taccount'),
        T('Accumulated depreciation deducted from its asset on the balance sheet', ['Item', 'Nakfa', 'Book value (Nakfa)'],
          [['Automobiles', '74,000', ''], ['Less: Accumulated Depreciation Expense-Automobiles', '6,167', '67,833'],
           ['Furniture and Fixtures', '10,000', ''], ['Less: Accumulated Depreciation Expense-Automobiles', '83', '9,917'],
           ['Office Equipment', '95,000', ''], ['Less: Accumulated Depreciation Expense-Automobiles', '1,583', '93,417']], 132, kind='statement'),
        T('Dahalk Company — Trial Balance, September 30 (incorrect, Exercise 3.5.1)', ['Account Title', 'Debit', 'Credit'],
          [['Cash', '29,000.00', ''], ['Office furniture', '', '4,000.00'], ['Equipment', '', '500.00'], ['Accounts Payable', '3,000.00', ''],
           ['Capital', '', '12,500.00'], ['Sales Income', '33,000.00', ''], ['Rent Expense', '1,000.00', ''], ['Salary Expense', '10,000.00', ''],
           ['General Expense', '', '4,000.00'], ['Total', '76,000.00', '21,000.00']], 135, kind='trial'),
    ],
    '11': [
        T('Asmara Shoes and Clothing Business — Balance Sheet, January 1, 2010 (Exhibit 2.1)', ['Assets', 'Nakfa', 'Liabilities and Owner’s Equity', 'Nakfa'],
          [['Cash', '65,000', 'Liabilities: Accounts Payable', '0'], ['Supplies', '2,500', 'Capital: Semhar, Capital', '85,500'],
           ['Merchandise Inventory', '18,000', '', ''], ['Total Assets', '85,500', 'Total Liabilities and Capital', '85,500']], 64, kind='statement'),
        T('Cash Register Slip — Sunshine Super Market (Exhibit 2.12)', ['Item', 'Quantity × price', 'Amount'],
          [['Shoes LV6', '1x@550.00', '550.00'], ['T-Shirt', '2x @180.00', '360.00'], ['CASH', '', '910.00']], 93, kind='statement'),
        T('Cross footing the cash receipts journal (Exhibit 2.15)', ['Cash Dr', 'Sales Discounts Dr.', 'Sales Cr.', 'Accounts Receivable Cr.', 'Sundry Accounts Cr.'],
          [['59,658.50', '691.50', '7,600.00', '32,750.00', '20,000.00'], ['Total debits 60,350.00', '', 'Total credits 60,350.00', '', '']], 96, kind='crossfoot'),
        T('Merchandise inventory adjustments in T-accounts', ['Account', 'Debit side', 'Credit side', 'Balance'],
          [['Merchandise Inventory', 'Jan. 1 Bal 18,000; Jan. 31 (Adj.) 16,500', 'Jan. 31 (Adj.) 18,000', 'Jan. 31: 16,500'],
           ['Income Summary', 'Jan. 31 (Adj.) 18,000', 'Jan. 31 (Adj.) 16,500', '']], 112, kind='taccount'),
        T('Supplies adjustment in T-accounts', ['Account', 'Debit side', 'Credit side', 'Balance'],
          [['Supplies', 'Jan. 1 Bal 2,500; Jan. 16 1,200; Jan. 31 375', 'Jan. 31 (Adj.) 2,850', 'Jan. 31: 1,225'],
           ['Supplies Expense', 'Jan. 31 (Adj.) 2,850', '', '']], 112, kind='taccount'),
        T('Prepaid insurance adjustment in T-accounts', ['Account', 'Debit side', 'Credit side', 'Balance'],
          [['Prepaid Insurance', 'Jan. 8 3,000', 'Jan. 31 (Adj.) 500', 'Jan. 31: 2,500'], ['Insurance Expense', 'Jan. 31 (Adj.) 500', '', '']], 113, kind='taccount'),
        T('Prepaid rent adjustment in T-accounts', ['Account', 'Debit side', 'Credit side', 'Balance'],
          [['Prepaid Rent', 'Jan. 8 9,000', 'Jan. 31 (Adj.) 1,000', 'Jan. 31: 8,000'], ['Rent Expense', 'Jan. 31 (Adj.) 1,000', '', '']], 113, kind='taccount'),
        T('Net sales and cost of goods sold sections', ['Item', 'Nakfa', 'Nakfa', 'Nakfa'],
          [['Sales', '', '', '70,400.00'], ['Less: Sales returns and allowances', '', '1,750.00', ''], ['Sales discount', '', '691.50', ''],
           ['', '', '', '2,441.50'], ['Net Sales', '', '', '67,958.50'], ['Beginning Merchandise Inventory', '', '', '18,000.00'],
           ['Purchases', '', '46,600.00', ''], ['Less: Purchases Returns and Allowances', '1,800.00', '', ''], ['Purchase Discounts', '340.00', '', ''],
           ['', '', '2,140.00', ''], ['Net Purchases', '', '44,460.00', ''], ['Add: Freight–In', '', '450.00', ''],
           ['Cost of Goods Purchased', '', '44,910.00', ''], ['Less: Ending Merchandise Inventory', '', '16,500.00', ''],
           ['', '', '', '28,410.00'], ['Cost of Goods Sold', '', '', '46,410.00']], 120, kind='statement'),
        T('Find the missing income statement items (Problem 4)', ['Sales', 'Sales Returns', 'Net Sales', 'Beginning Inventory', 'Net Purchases', 'Ending Inventory', 'Cost of Goods Sold', 'Gross Profit'],
          [['82,000', '3,000', '(a)', '28,000', '75,000', '(b)', '65,000', '14,000'], ['68,000', '(c)', '62,000', '15,000', '33,000', '17,000', '(d)', '(e)'],
           ['78,000', '(f)', '78,000', '(g)', '56,000', '25,000', '(h)', '14,000'], ['56,000', '1,000', '55,000', '16,000', '31,000', '(i)', '(j)', '12,000']], 125, kind='missing'),
        T('Sium Ready Made Clothing Shop — account balances, December 31 (Problem 5)', ['Account Title', 'Debit', 'Credit'],
          [['Cash', '3,793.00', ''], ['Accounts Receivable', '5,053.00', ''], ['Merchandise Inventor', '8,854.00', ''], ['Supplies', '1,323.00', ''],
           ['Prepaid Insurance', '1,200.00', ''], ['Office Equipment', '10,000.00', ''], ['Accumulated Depreciation—Office Equipment', '', '–'],
           ['Accounts Payable', '', '7,155.00'], ['Sium’s Capital', '', '22,998.00'], ['Sium’s Drawing', '675.00', ''],
           ['Income and Expense Summary', '–', '–'], ['Sales', '', '17,460.00'], ['Sales Returns and Allowances', '450.00', ''],
           ['Sales Discount', '211.00', ''], ['Purchases', '13,775.00', ''], ['Freight-in', '189.00', ''], ['Purchase returns and allowances', '', '775.00'],
           ['Purchase discount', '', '255.00'], ['Delivery Expense', '300.00', ''], ['Insurance Expense', '–', '–'], ['Miscellaneous Expense', '420.00', ''],
           ['Rent Expense', '600.00', ''], ['Salary Expense', '1,800.00', ''], ['Supplies Expense', '–', '–'], ['', '48,643.00', '48,643.00']], 125, kind='trial'),
        T('Adjustment data (Part IV, Problem 1)', ['Account Title', 'Account Balance in General Ledger', 'Ending Inventory'],
          [['Merchandise Inventory', '80,000.00', '4,500.00'], ['Supplies', '1,000.00', '350.00'], ['Prepaid Insurance', '500.00', '300.00']], 138, kind='statement'),
    ],
}

OVERRIDES.update({
    ('10', 0): [T('Lia’s mother: what she owns and what she owes (Activity 3.1.2)', ['Owns', 'Nakfa', 'Owes', 'Nakfa'],
                  [['Car', '75,000', 'Electric bill', '300'], ['Tools', '400', 'Money borrowed', '10,000'], ['House', '500,000', '', ''],
                   ['Furniture', '1,000', '', ''], ['Clothes', '300', '', ''], ['Money in bank', '10,000', '', ''], ['Total', '586,700', '', '']], 65, kind='statement')],
    ('10', 1): [T('Practice the accounting equation: Asset = Liability + Capital (Activity 3.1.3)', ['Asset (Nakfa)', 'Liability (Nakfa)', 'Capital (Nakfa)'],
                  [['4,000', '1,000', '?'], ['20,000', '4,000', '?'], ['9,500', '?', '5,500'], ['5,495', '1,345', '?'], ['?', '6,780', '6,220'],
                   ['?', '25,000', '75,000']], 66, kind='missing')],
    ('10', 55): [T('Which account is debited and which is credited? (Exercise)', ['No.', 'Transaction', 'Debit', 'Credit'],
                   [['1.', 'Paid cash for supplies.', 'Supplies', 'Cash'], ['2.', 'Received cash from repairs income.', '', ''],
                    ['3.', 'Paid cash for rent of garage for the month.', '', ''], ['4.', 'Paid cash for advertising in the “Hadas Eritrea”', '', ''],
                    ['5.', 'Paid cash for electricity for the month.', '', ''], ['6.', 'Paid cash for telephone for the month.', '', ''],
                    ['7.', 'Paid cash for postage stamps (Miscellaneous items).', '', ''], ['8.', 'Received cash from repairs income.', '', '']], 110, kind='dc_exercise')],
    ('10', 90): [T('Trial Balance, October 31, current year (Bidho)', ['Account Title', 'Debit', 'Credit'],
                   [['Cash', 'Nakfa 19,600', ''], ['Accounts Receivable', '30,800', ''], ['Office Supplies', '31,200', ''], ['Office Equipment', '70,000', ''],
                    ['Accounts Payable', '', '33,000'], ['Bidho, Capital', '', '94,500'], ['Bidho, Withdrawals', '8,200', ''], ['Fares Earned', '', '80,100'],
                    ['Salary Expense', '46,200', ''], ['Utilities Expense', '1,600', ''], ['Total', '207,600', '207,600']], 136, kind='trial')],
    ('11', 57): [T('Credit Memorandum CM 131 to Busha plc (Exhibit 2.18; invoice no. 201 of 15/02/2010, terms 3/10, n/30)',
                   ['Catalogue No.', 'Description', 'Quantity', 'Price', 'Amount'],
                   [['TV008', 'Panasonic CD-Player', '1', '1,450.00', '1,450.00'], ['', '', '', 'TOTAL', '1,450.00']], 104, kind='statement')],
    ('11', 68): None,
})
TITLE_FIX = {
    'DCeahpaibta Tl aSxtai tSeemrveincte': 'Dehab Taxi Service — Capital Statement',
    'PosDt eChlaobsi Tnga xTi rSiaerl vBiacelance': 'Dehab Taxi Service — Post-Closing Trial Balance',
    'listed below': 'Find the missing amount in the accounting equation (Part IV)',
    'Services is presented below:': 'Proving the cash journal: footings',
    'they give us the following picture:': 'General Journal Page 3 — all adjusting entries',
    'sold.)': 'Worksheet data: purchases and income summary (Problem 2)',
}
