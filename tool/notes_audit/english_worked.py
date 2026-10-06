"""English: give every lesson without a worked example a 'find and correct the error' walkthrough built from its grammar card
(rule + the incorrect example and its correction)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from patch import Book, worked
for bk in sys.argv[1:]:
    B = Book(bk); n = 0
    for u in B.d['units']:
        for l in u['lessons']:
            if any(c.get('type') == 'worked' for c in l['cards']):
                continue
            g = next((c for c in l['cards'] if c.get('type') == 'grammar' and any(isinstance(e, dict) and e.get('ok') is False and e.get('fix') for e in c.get('examples') or [])), None)
            if not g:
                continue
            bad = [e for e in g['examples'] if isinstance(e, dict) and e.get('ok') is False and e.get('fix')]
            rules = [r for r in (g.get('rule') or []) if isinstance(r, str) and 8 < len(r) < 260 and not r.lower().startswith('definition')]
            e = bad[0]
            steps = [f'**Step 1: Recall the rule.** {rules[0]}' if rules else '**Step 1: Recall the rule for this pattern.**',
                     f'**Step 2: Test the sentence.** "{e["text"]}" breaks this rule.',
                     f'**Step 3: Correct it.** "{e["fix"]}"']
            if len(rules) > 1:
                steps.append(f'**Check:** {rules[1]}')
            if len(bad) > 1:
                steps.append(f'**Same pattern:** "{bad[1]["text"]}" → "{bad[1]["fix"]}"')
            w = worked(f"{l['id']}-wk1", 'Find and correct the error', f'Find and correct the error: "{e["text"]}"', [s for s in steps], e['fix'], src='notes')
            B.add(l['id'], [w], after=g['id'])
            n += 1
    B.save(); print(bk, n)
