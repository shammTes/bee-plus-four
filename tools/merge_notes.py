#!/usr/bin/env python3
"""Merge rich + generated unit notes; write unit_notes.json and safety stubs."""
from __future__ import annotations
import json
from pathlib import Path

CONTENT = Path("assets/content")

def load(p: Path):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except Exception:
        return []

def key(n):
    return (
        str(n.get("grade", "")).upper(),
        str(n.get("subject", "")).upper(),
        int(n.get("unit_number") or 0),
    )

def score(n):
    return (
        len(n.get("summary") or "")
        + sum(len(x.get("explanation") or "") for x in (n.get("sections") or []))
        + 20 * len(n.get("examples") or [])
        + 10 * len(n.get("exercises") or [])
    )

def main():
    CONTENT.mkdir(parents=True, exist_ok=True)
    base = {}
    for path in [
        CONTENT / "unit_notes_rich.json",
        CONTENT / "unit_notes.json",
    ]:
        for n in load(path):
            if not isinstance(n, dict):
                continue
            k = key(n)
            if k not in base or score(n) > score(base[k]):
                base[k] = n
    if not base:
        (CONTENT / "unit_notes.json").write_text("[]", encoding="utf-8")
        print("FINAL notes 0")
    else:
        notes = sorted(base.values(), key=key)
        (CONTENT / "unit_notes.json").write_text(
            json.dumps(notes, ensure_ascii=False), encoding="utf-8"
        )
        print("FINAL notes", len(notes))

    # safety stubs
    exam = CONTENT / "exam_catalog.json"
    if not exam.exists():
        exam.write_text(
            '{"matriculation":[],"model_exam_years":[]}', encoding="utf-8"
        )
    pq = CONTENT / "practice_questions.json"
    if not pq.exists():
        pq.write_text("[]", encoding="utf-8")
    pi = CONTENT / "practice_index.json"
    if not pi.exists():
        pi.write_text(
            json.dumps(
                {
                    "files": [
                        "practice_from_notes.json",
                        "practice_questions.json",
                    ],
                    "lite": "practice_lite.json",
                }
            ),
            encoding="utf-8",
        )
    un = CONTENT / "unit_notes.json"
    if not un.exists():
        un.write_text("[]", encoding="utf-8")

if __name__ == "__main__":
    main()
