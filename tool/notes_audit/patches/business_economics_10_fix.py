import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from patch import *
from subs import apply
B = Book('business_economics_10')
c = B.card('be10-u3-tb7')
c.pop('body', None)
c.update(type='table', title='General journal entry (page 1)', head=['Date', 'Account title and explanation', 'P.R.', 'Debit (Nfa)', 'Credit (Nfa)'],
         rows=[['Sept. 5', 'Office Equipment', '15', '45,000', ''], ['', '      Cash', '11', '', '45,000'], ['', '(Bought office equipment, Cheque No. 1)', '', '', '']])
B.add(B.where('be10-u3-tb7')[1]['id'] if False else 'be10-u3-l3-3', [
 table('be10-u3-tb7b', 'General journal vs special cash journal', ['Journal', 'Used for', 'Columns', 'Posting'],
       [['General journal', 'Non-repetitive or non-cash transactions', 'Two money columns (Debit, Credit)', 'Daily, entry by entry'],
        ['Special cash journal', 'All cash receipts and cash payments', 'Several columns (Cash Dr/Cr, General Dr/Cr)', 'Column totals, monthly']], src='notes'),
 text('be10-u3-tb7c', 'Posting tips', ["The **Post Reference (P.R.)** column stays blank until the amount has been posted; a number in it shows the entry has been transferred to that ledger account.",
       "With a special cash journal, do not post each cash entry daily — post only the **column totals** at the end of the month. This saves a great deal of posting work."], src='notes'),
], after='be10-u3-tb7')
B.save()
apply('business_economics_10', [(" (same as Dehab's transaction 2 in the textbook)", "")])
