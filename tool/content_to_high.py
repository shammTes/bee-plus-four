#!/usr/bin/env python3
"""Convert an owner-authored matric paper (the assets/content exam-catalog format, e.g.
assets/high/exams/algebra_geometry_2000_matric.json) into a High exam pack listed in assets/high/exams/index.json.

    python3 tool/content_to_high.py SRC OUT            # writes OUT (a file name inside assets/high/exams/)
    python3 tool/content_to_high.py SRC OUT --check    # exit 1 if OUT is missing or differs from a fresh conversion

What changes (nothing else does; stems, options, answers, accepted answers, explanations, ids and numbering are copied
byte for byte, and the source file is never written):
  * exam.subject "Algebra and Geometry" -> "Mathematics" (every High Algebra and Geometry paper is filed under
    Mathematics, so the paper shows on the Matric tab's Mathematics list, its topic practice and its notes-unit links)
  * question topics: the owner's tags (alg-*, geo-*) -> the Mathematics topic-index subtopic ids the other High
    papers use (TOPIC_MAP below), so topic titles, topic practice and the Tutor group it with the other papers.
    The owner's tags stay in "keywords".
  * exam.high_conversion records the source file and the tool.
After converting: add OUT to assets/high/exams/index.json, then run tool/exam_summary.py, tools/map_unit_questions.py,
tool/build_tutor_index.py (and tool/school_units.py --check).
"""
import argparse
import copy
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
EXAMS = os.path.join(ROOT, 'assets', 'high', 'exams')

SUBJECT_MAP = {'Algebra and Geometry': 'Mathematics'}

# owner tag -> Mathematics subtopic ids (topics_index_mathematics_20xx_matric.json); precedents from the High papers:
# quadratic inequalities -> quadratic-equations, % problems -> business-mathematics, Pythagoras word problems -> trigonometry
TOPIC_MAP = {
    'alg-exponents': ['exponents-logarithms'],
    'alg-logarithms': ['exponents-logarithms'],
    'alg-surds': ['absolute-value-radicals'],
    'alg-trigonometry': ['trigonometry'],
    'alg-relations': ['functions-inverse'],
    'alg-functions': ['functions-inverse'],
    'alg-equations': ['rational-functions'],
    'alg-linear-equations': ['linear-equations'],
    'alg-rational-functions': ['rational-functions'],
    'alg-polynomials': ['polynomials'],
    'alg-binomial': ['polynomials'],
    'alg-quadratics': ['quadratic-functions'],
    'alg-quadratic-equations': ['quadratic-equations'],
    'alg-inequalities': ['quadratic-equations'],
    'alg-variation': ['linear-equations'],
    'alg-mixtures': ['linear-systems'],
    'alg-ratio': ['business-mathematics'],
    'alg-percent': ['business-mathematics'],
    'alg-sequences': ['sequences-series'],
    'alg-series': ['sequences-series'],
    'alg-statistics': ['statistics'],
    'alg-probability': ['probability'],
    'alg-coordinate-geometry': ['coordinate-geometry'],
    'alg-circles': ['circle-equation'],
    'geo-triangles': ['geometric-reasoning'],
    'geo-quadrilaterals': ['polygons-congruence'],
    'geo-polygons': ['polygons-congruence', 'mensuration'],
    'geo-similarity': ['similar-triangles'],
    'geo-circles': ['circle-geometry'],
    'geo-transformations': ['transformations'],
    'geo-pythagoras': ['trigonometry'],
}


def convert(src_rel):
    src = json.load(open(os.path.join(ROOT, src_rel), encoding='utf-8'))
    out = copy.deepcopy(src)
    ex = out['exam']
    ex['subject'] = SUBJECT_MAP.get(ex.get('subject'), ex.get('subject'))
    ex['high_conversion'] = {'source': src_rel, 'tool': 'tool/content_to_high.py',
                             'changed': 'subject filed under Mathematics; topics mapped to Mathematics subtopic ids (owner tags kept in keywords)'}
    missing = set()
    for q in out['questions']:
        tags = q.get('topics') or []
        kw = q.get('keywords') or []
        q['keywords'] = kw + [t for t in tags if t not in kw]
        mapped = []
        for t in tags:
            if t not in TOPIC_MAP:
                missing.add(t)
                continue
            mapped += [m for m in TOPIC_MAP[t] if m not in mapped]
        q['topics'] = mapped
    if missing:
        sys.exit(f'unmapped topic tags: {sorted(missing)} (add them to TOPIC_MAP)')
    # the parts that must never change
    for a, b in zip(src['questions'], out['questions']):
        for k in a:
            if k not in ('topics', 'keywords'):
                assert a[k] == b[k], (a['id'], k)
    return json.dumps(out, ensure_ascii=False, indent=2) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src', help='source paper, relative to the repo root')
    ap.add_argument('out', help='output file name inside assets/high/exams/')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    text = convert(a.src)
    path = os.path.join(EXAMS, a.out)
    if a.check:
        ok = os.path.exists(path) and open(path, encoding='utf-8').read() == text
        print(f'{a.out} up to date' if ok else f'{a.out} missing or out of date: run python3 tool/content_to_high.py {a.src} {a.out}')
        sys.exit(0 if ok else 1)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print(f'wrote assets/high/exams/{a.out}')


if __name__ == '__main__':
    main()
