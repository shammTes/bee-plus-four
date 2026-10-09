#!/usr/bin/env python3
"""Oct 9 2026 English update (idempotent):
  * Grade 9 Unit 6: lesson 6.2 fixed, new lesson 6.3 Prepositions (place, time, movement, confusing pairs, partner words,
    the textbook Lesson 6.5 B exercise solved step by step) + 26 exercise questions.
  * Grade 10: plainer wording in every unit, imported exam cards rewritten and moved to the lesson that teaches them.
  * Grade 10 Unit 8 lesson 8.3: present perfect continuous completed (uses, time words, side-by-side with the present
    perfect simple and the past continuous, common mistakes, state verbs) + 14 exercise questions.

  python3 tool/english/oct9_update/run.py
then regenerate: tool/split_notes.py, tool/build_tutor_index.py, tools/map_unit_questions.py, tools/verify_unit_links.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'teacher_feedback'))
sys.path.insert(0, HERE)
from lib import Book  # noqa: E402
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location('tf_run', os.path.join(HERE, '..', 'teacher_feedback', 'run.py'))
tf_run = importlib.util.module_from_spec(_spec)  # teacher-feedback helpers: suspicious answer keys, pages, index update
_spec.loader.exec_module(tf_run)
import g9_prep  # noqa: E402
import g10_simple  # noqa: E402
import g10_ppc  # noqa: E402


def main():
    b9, b10 = Book(9), Book(10)
    n9 = g9_prep.apply(b9)
    g10_simple.apply(b10)
    n10 = g10_ppc.apply(b10)
    for b in (b9, b10):
        tf_run.fix_pages(b)
        for s in tf_run.suspicious(b):
            print('CHECK', s)
        b.save()
    tf_run.update_indexes({9: b9, 10: b10})
    print(f'G9 Unit 6 preposition questions: {n9}; G10 Unit 8 new PPC questions: {n10}')


if __name__ == '__main__':
    main()
