#!/usr/bin/env python3
"""Verify that History files only GAINED items compared with a git ref (default HEAD of origin/main merge-base):
every existing card, question, glossary entry and field must be byte-for-byte identical and in the same place;
new lesson cards may only be appended at the end of a lesson, new questions only at the end of a unit exercise."""
import json, subprocess, sys
ref = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
bad = 0
for b in ['history_9', 'history_10', 'history_11', 'history_12']:
    p = f'assets/high/notes/notes/{b}.json'
    old = json.loads(subprocess.check_output(['git', 'show', f'{ref}:{p}']))
    new = json.load(open(p))
    added = {'cards': 0, 'questions': 0}

    def cmp(o, n, path):
        global bad
        if isinstance(o, dict) and isinstance(n, dict):
            for k in o:
                if k not in n:
                    print('REMOVED', path + '.' + k); bad += 1
                else:
                    cmp(o[k], n[k], path + '.' + k)
            for k in n:
                if k not in o and not (k == 'exercise' and path.count('.') == 2):
                    print('NEW KEY', path + '.' + k); bad += 1
        elif isinstance(o, list) and isinstance(n, list):
            if len(n) < len(o):
                print('SHORTER', path); bad += 1
            for i, x in enumerate(o):
                if i < len(n):
                    cmp(x, n[i], f'{path}[{i}]')
            if len(n) > len(o):
                if path.endswith('.cards'):
                    added['cards'] += len(n) - len(o)
                elif path.endswith('.questions'):
                    added['questions'] += len(n) - len(o)
                else:
                    print('GREW', path, len(o), '->', len(n)); bad += 1
        elif o != n:
            print('CHANGED', path, repr(o)[:80], '->', repr(n)[:80]); bad += 1
    cmp(old, new, b)
    print(b, 'added', added)
print('OK: existing History text untouched' if not bad else f'{bad} PROBLEMS')
sys.exit(1 if bad else 0)
