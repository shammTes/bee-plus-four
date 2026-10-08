#!/usr/bin/env python3
"""Apply hand-checked fixes to legacy practice items in the Exercise bank.

Reads tool/matric_unit_sync/exercise_fixes.json:
  answer      id -> [new index, option text]  (text is asserted, so a reshuffle fails loudly)
  explanation id -> new explanation
  drop        id -> reason (item removed)
Then tags the unit-less English 11 practice items (shown only under
"General") to an English 11 notes unit with the keyword rules below.
Updates assets/high/exercises/index.json counts. Idempotent.

  python3 tools/fix_legacy_exercises.py && python3 tools/verify_exercises.py
"""
import collections, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, 'assets/high/exercises')
FIX = os.path.join(ROOT, 'tool/matric_unit_sync/exercise_fixes.json')

# English 11 practice item -> unit. First matching rule wins; the prompt is
# tried before the explanation.
ENG11_RULES = [
 (r'indirect speech|reported speech|direct speech|reporting verb|in reported|backshift', 'eng11-u5'),
 (r"quotation|dialogue|'wait' he shouted|said john|she replied|shouted the boy", 'eng11-u5'),
 (r'question tag|tag question', 'eng11-u15'),
 (r'passive', 'eng11-u4'),
 (r'conditional|\bwish\b|\bif clause', 'eng11-u6'),
 (r'\bmodal|\bmust\b|\bshould\b|\bmight\b', 'eng11-u3'),
 (r'gerund|infinitive|participle|participial', 'eng11-u7'),
 (r'agree(?:ment|s)? with|subject-verb|subject–verb', 'eng11-u2'),
 (r"contraction|\bits\b.{0,6}\bit's\b|\bit's\b", 'eng11-u24'),
 (r'pronoun', 'eng11-u10'),
 (r"possessive|apostrophe", 'eng11-u9'),
 (r'end mark|punctuat|comma|semicolon|colon|dash|hyphen|ellipsis|bracket|parenthes|slash', 'eng11-u1'),
 (r'redundan|fragment|run-on|comma splice|error', 'eng11-u24'),
 (r'not only|either|neither|therefore|however|moreover|conjunction|fanboys|correlative|in order that|as if|whenever|no sooner|so\.\.\.that|combine', 'eng11-u25'),
 (r'tense|past perfect|present perfect|future', 'eng11-u12'),
 (r'question', 'eng11-u14'),
 (r'pronoun', 'eng11-u10'),
 (r'\bnouns?\b|plural', 'eng11-u9'),
 (r'adjective|adverb|part of speech|parts of speech|word class|suffix|prefix|interjection|type of word|kind of word', 'eng11-u16'),
 (r'\bverbs?\b|transitive|helping|auxiliary|linking verb', 'eng11-u11'),
 (r'preposition', 'eng11-u18'),
 (r'adjective|adverb|part of speech|parts of speech|word class|suffix|prefix', 'eng11-u16'),
 (r'clause|sentence|subject|predicate|object|complement|appositive|phrase', 'eng11-u1'),
]
ENG11_RULES = [(re.compile(a, re.I), b) for a, b in ENG11_RULES]


def eng11_unit(q):
    for src in (q['prompt'], q.get('explanation') or ''):
        for rx, u in ENG11_RULES:
            if rx.search(src):
                return u
    return None


def main():
    fx = json.load(open(FIX, encoding='utf-8'))
    idx_path = os.path.join(EX, 'index.json')
    idx = json.load(open(idx_path, encoding='utf-8'))
    seen = set(); stats = collections.Counter(); tagged = collections.Counter()
    for g, subs in idx['grades'].items():
        for subj, ent in subs.items():
            path = os.path.join(EX, ent['file'])
            data = json.load(open(path, encoding='utf-8'))
            out = []
            for q in data['questions']:
                i = q['id']
                if i in fx['drop']:
                    seen.add(i); stats['dropped'] += 1; continue
                if i in fx['answer']:
                    k, text = fx['answer'][i]
                    if q['options'][k] != text:
                        sys.exit(f'{i}: option {k} is {q["options"][k]!r}, expected {text!r}')
                    seen.add(i); stats['answer'] += q['answer'] != k; q['answer'] = k
                if i in fx['explanation']:
                    seen.add(i); stats['explanation'] += q['explanation'] != fx['explanation'][i]
                    q['explanation'] = fx['explanation'][i]
                if subj == 'english' and g == '11' and not q.get('unit'):
                    u = eng11_unit(q)
                    if u:
                        q['unit'] = u; tagged[u] += 1
                out.append(q)
            if out != json.load(open(path, encoding='utf-8'))['questions']:
                data['questions'] = out
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            cnt = collections.Counter(q.get('unit') or 'general' for q in out)
            ent['count'] = len(out); ent['units'] = dict(sorted(cnt.items()))
    idx['total'] = sum(e['count'] for gg in idx['grades'].values() for e in gg.values())
    with open(idx_path, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=1); f.write('\n')
    want = set(fx['drop']) | set(fx['answer']) | set(fx['explanation'])
    print(f'changed answers {stats["answer"]}, explanations {stats["explanation"]}, '
          f'dropped {stats["dropped"]}, english 11 tagged {sum(tagged.values())} {dict(tagged)}')
    print(f'fix ids already applied/not found: {len(want - seen)}')


if __name__ == '__main__':
    main()
