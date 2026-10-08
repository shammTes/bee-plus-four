"""Generic clean-up of the imported 'study notes' material in every English book:
plain text instead of LaTeX, friendly step headings, no 'matriculation trap' jargon, whys that start with the right
answer, a real tip and similar questions for every exercise question, and 'the first option' fixed to the real letter."""
import collections
import re
import zlib

from lib import _walk_strings

HEAD = [
    (r'Analy[sz]e the grammatical structure', 'Look at the sentence'),
    (r'Identify the (?:matriculation|exam) trap', 'Watch out for the trap'),
    (r'Tigrinya Explanation(?: \(ትርጉም\))?', 'In Tigrinya'),
]
HEAD_ONLY = re.compile(r'^\s*\**\s*(?:Step \d+:\s*)?(?:Analy[sz]e the grammatical structure|Identify the (?:matriculation|exam) trap|Tigrinya Explanation(?: \(ትርጉም\))?|Look at the sentence|Watch out for the trap|In Tigrinya)\s*\**\s*$')
WORDS = [
    (r'\bmatriculation trap\b', 'exam trap'), (r'\bon the ESSLCE\b', 'in the national exam'), (r'\bthe ESSLCE\b', 'the national exam'),
    (r'\bESSLCE\b', 'national exam'), (r'\bnegative L1 transfer\b', 'direct translation from Tigrinya'), (r'\bL1 transfer\b', 'translation from Tigrinya'),
    (r'\bL1 interference\b', 'translation from Tigrinya'), (r'\bmorphological markers\b', 'word endings'), (r'\bsyntactic\b', 'grammar'),
    (r'\bgrammatical word classes\b', 'word classes'), (r'\bnominali[sz]ed form\b', 'noun form'), (r'\bpolarity opposition\b', 'opposite tag rule'),
    (r'\bdummy (?:auxiliary|do-support|do)\b', 'do/does/did'), (r'\bdo-support\b', 'do/does/did'),
    (r'\btypical case concord trap in matriculation exams\b', 'common pronoun trap in exams'), (r'\bcase concord\b', 'pronoun form'),
    (r'\bregular polarity rules\b', 'the normal positive/negative rule'), (r'\bsyntactically and pragmatically correct\b', 'correct and natural'),
    (r'\b[Ss]yntactically\b', 'grammatically'), (r'\bdue to L1 translation\b', 'because of translating from Tigrinya'),
    (r'\bdirect L1 translation\b', 'direct translation from Tigrinya'), (r'\bTigrinya L1 omission error\b', 'mistake made by translating from Tigrinya'),
    (r'\bL1 spelling-to-sound transfer\b', 'Tigrinya spelling habits'), (r'\ban L1 \(Tigrinya\) word-order error\b', 'a Tigrinya word-order mistake'),
    (r'\ba common L1 error\b', 'a common mistake from Tigrinya'), (r'\ba typical L1 deletion error\b', 'a typical mistake from Tigrinya'),
    (r'\bfree from L1 double-subject errors\b', 'free from double-subject mistakes'), (r'\bthe L1 omission error\b', 'the missing-verb mistake'),
    (r'\bL1\b', 'first-language (Tigrinya)'),
    (r'\bstative verbs\b', 'state verbs'), (r'\bstative verb\b', 'state verb'), (r'\bStative verbs\b', 'State verbs'), (r'\b[Ss]tative\b', 'state'),
    (r'\(predicate nominative\)', ''), (r'\bnominalizing suffix\b', 'noun-making suffix'), (r'\bnominalization\b', 'making a noun'),
    (r'\bInflectional endings change form, not class\b', 'Endings like these change the form of a word, not its word class'),
]
DUMMY = {'She goes to school every day.', 'She go to school every day.', 'This is a correct model sentence.', 'This be wrong model sentence.'}


def delatex(s):
    if '$$' not in s and '\\(' not in s:
        return s

    def inner(m):
        x = m.group(1)
        for _ in range(3):
            x = re.sub(r'\\(?:text|mathrm|textbf|textit|mathbf)\s*\{([^{}]*)\}', r'\1', x)
        for a, b in (('\\rightarrow', '→'), ('\\Rightarrow', '→'), ('\\to', '→'), ('\\times', '✗'), ('\\checkmark', '✔'), ('\\ldots', '…'),
                     ('\\dots', '…'), ('\\cdots', '…'), ('\\quad', ' '), ('\\qquad', ' '), ('\\,', ' '), ('\\;', ' '), ('\\neq', '≠'), ('\\pm', '±')):
            x = x.replace(a, b)
        x = re.sub(r'_\{(\d+)\}|_(\d)', lambda mm: mm.group(1) or mm.group(2), x)
        x = re.sub(r'_\{([^{}]*)\}', r' (\1)', x)
        x = re.sub(r'\^\{([^{}]*)\}', r'\1', x)
        x = x.replace('\\', '').replace('{', '').replace('}', '')
        return re.sub(r'\s+', ' ', x).strip()
    s = re.sub(r'\$\$(.+?)\$\$', inner, s, flags=re.S)
    s = re.sub(r'\\\((.+?)\\\)', inner, s, flags=re.S)
    return s


def _fix_text(s, why=False):
    s = delatex(s)
    for rx, rp in HEAD:
        s = re.sub(rx, rp, s)
    for rx, rp in WORDS:
        s = re.sub(rx, rp, s)
    return s


def first_option(s, ans):
    """'the first option/sentence' in an explanation must name the real answer letter"""
    if not isinstance(ans, str) or ans == 'A':
        return s
    return re.sub(r'\b([Tt])he first (?:option|sentence)', lambda m: ('Option' if m.group(1) == 'T' else 'option') + f' {ans}', s)


def _clean_why_list(q):
    out = []
    for w in q['why']:
        if not isinstance(w, str) or not w.strip() or HEAD_ONLY.match(w):
            continue
        out.append(first_option(_fix_text(w), q['answer']))
    if q['type'] == 'mcq' and q.get('options'):
        a = q['answer']
        lead = f'Answer {a}: {q["options"].get(a, "")}'.rstrip(': ')
        if out and re.match(r'^Answer [A-E]\b', out[0]):
            out[0] = lead
        else:
            out.insert(0, lead)
    q['why'] = out or q['why']


def _clean_steps(c):
    steps, out, i = c['steps'], [], 0
    while i < len(steps):
        t = _fix_text(steps[i].get('text', '') or '')
        m = HEAD_ONLY.match(t)
        if m and i + 1 < len(steps) and not HEAD_ONLY.match(_fix_text(steps[i + 1].get('text', '') or '')):
            head = re.sub(r'\*', '', t).strip()
            nxt = _fix_text(steps[i + 1].get('text', '') or '')
            t = f'**{head}.** {nxt}'
            i += 1
        elif not t.strip():
            i += 1
            continue
        t = re.sub(r"\s*\((?:Option|option) [A-E]\)", '', t)
        t = re.sub(r'\s*Option [A-E] is (?:the )?correct\.?', '', t)
        out.append({**steps[i], 'text': t})
        i += 1
    if len(out) >= 2:
        c['steps'] = out[:10]
    if c.get('answer') and isinstance(c['answer'], str):
        c['answer'] = _fix_text(c['answer'])


_STOP = set('the a an to of in on at is are was were be and or for with by it this that ____ complete choose correct sentence'.split())


def _words(t):
    return {w for w in re.findall(r"[a-z']+", t.lower()) if w not in _STOP and len(w) > 2}


def _closest(q, pool, k):
    """the k ready-made similar items of the unit that share the most words with this question (answer included)"""
    key = _words(q['q'] + ' ' + _answer_text(q) + ' ' + ' '.join(w for w in q['why'] if isinstance(w, str)))
    ranked = sorted(range(len(pool)), key=lambda i: (-len(key & _words(pool[i]['q'] + ' ' + pool[i]['a'])), i))
    return [pool[i] for i in ranked[:k]]


def _answer_text(q):
    a = q['answer']
    if q['type'] == 'mcq' and isinstance(q.get('options'), dict):
        return f"{a}: {q['options'].get(a, '')}"
    if q['type'] == 'tf':
        return 'True' if a else 'False'
    return str(a)


def clean_book(b, dummy_examples=None):
    """dummy_examples: {card id: [(text, ok, fix)]} replacing the placeholder examples of imported cards"""
    stats = collections.Counter()
    for u in b.d['units']:
        for l in u['lessons']:
            for c in l['cards']:
                if c['type'] == 'worked':
                    _clean_steps(c)
                for o, k in list(_walk_strings(c)):
                    s = _fix_text(o[k])
                    if c['type'] == 'check':
                        s = first_option(s, c.get('answer'))
                    if s != o[k]:
                        o[k] = s
                        stats['card strings'] += 1
                if c['type'] == 'grammar' and any(e['text'] in DUMMY for e in c.get('examples', [])):
                    new = (dummy_examples or {}).get(c['id'])
                    if new:
                        c['examples'] = [dict(text=e[0], ok=e[1], **({'fix': e[2]} if len(e) > 2 and e[2] else {})) for e in new]
                        stats['placeholder examples'] += 1
                    else:
                        stats['placeholder left: ' + c['id']] += 1
        # exercise questions
        qs = u['exercise']['questions']
        tips = collections.Counter(q['tip'] for q in qs if q.get('tip') and not q['tip'].startswith('Read the whole'))
        pool = [s for q in qs for s in (q.get('similar') or [])]
        best_tip = tips.most_common(1)[0][0] if tips else None
        for n, q in enumerate(qs):
            before = repr(q)
            _clean_why_list(q)
            q['q'] = _fix_text(q['q'])
            if q['type'] == 'fill' and q.get('choices') and q['choices'][0] == q['answer'] and len(q['choices']) > 1:
                # the app shows choices in file order: do not leave the answer always in place A
                k = zlib.crc32(q['id'].encode()) % len(q['choices'])
                q['choices'] = q['choices'][k:] + q['choices'][:k]
                stats['fill choices rotated'] += 1
            if q.get('tip'):
                q['tip'] = _fix_text(q['tip'])
            if (not q.get('tip') or q['tip'].startswith('Read the whole')) and best_tip:
                q['tip'] = best_tip
            if not q.get('similar') and pool:
                q['similar'] = [dict(s) for s in _closest(q, pool, 2)]
                stats['similar added'] += 1
            elif not q.get('similar') and len(qs) > 2:
                # no ready-made similar items in this unit: point to two other questions of the same unit, with their answers
                q['similar'] = [dict(q=o['q'], a=_answer_text(o)) for o in (qs[(n + 1) % len(qs)], qs[(n + 2) % len(qs)])]
                stats['similar added (same unit)'] += 1
            if repr(q) != before:
                stats['questions'] += 1
        for g in u.get('glossary', []):
            g['meaning'] = _fix_text(g['meaning'])
        for t in u.get('tips', []):
            t['text'] = _fix_text(t['text'])
    return stats
