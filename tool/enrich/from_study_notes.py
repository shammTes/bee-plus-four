#!/usr/bin/env python3
"""Inject check + worked cards into thin lessons from Study_Notes.json review exercises.

History is never modified. English is skipped (separate pipeline).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "assets/high/notes/notes"
STUDY = Path("/workspace/tmp-sync/drive/Study_Notes.json")

SUBJECT_TO_BOOK = {
    "Mathematics": "mathematics",
    "Physics": "physics",
    "Chemistry": "chemistry",
    "Biology": "biology",
    "Geography": "geography",
    "Agriculture": "agriculture",
    "Business and Economics": "business_economics",
}

# Max new check cards per thin lesson this run
CHECKS_PER_LESSON = 2
# Cap total new checks across a book so the PR stays reviewable
MAX_NEW_CHECKS_PER_BOOK = 24


def letters_options(opts: list[str]) -> dict[str, str]:
    return {chr(65 + i): o for i, o in enumerate(opts[:5])}


def answer_letter(opts: list[str], correct: str) -> str | None:
    for i, o in enumerate(opts[:5]):
        if o.strip() == (correct or "").strip():
            return chr(65 + i)
    # fuzzy: strip $$ and spaces
    def norm(s: str) -> str:
        return re.sub(r"\s+", "", s or "").replace("$$", "")

    nc = norm(correct)
    for i, o in enumerate(opts[:5]):
        if norm(o) == nc:
            return chr(65 + i)
    return None


def explanation_steps(explanation: str) -> list[dict]:
    text = (explanation or "").strip()
    if not text:
        return [{"text": "Review the definition, then eliminate wrong options."}]
    # Prefer **Step N:** chunks
    parts = re.split(r"(?=\*\*Step\s+\d+)", text)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= 2:
        out = []
        for p in parts[:8]:
            # keep first line as heading-ish, rest as body lines
            lines = [ln.strip() for ln in p.splitlines() if ln.strip()]
            for ln in lines[:4]:
                out.append({"text": ln[:500]})
            if len(out) >= 10:
                break
        return out or [{"text": text[:400]}]
    # fallback: split paragraphs
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return [{"text": p[:500]} for p in paras[:6]] or [{"text": text[:400]}]


def next_suffix(existing_ids: set[str], unit_id: str, kind: str) -> int:
    # kind chk / wrk / tbl
    pat = re.compile(rf"^{re.escape(unit_id)}-{kind}(\d+)$")
    nums = [int(m.group(1)) for i in existing_ids if (m := pat.match(i))]
    # also older style chk7c1
    pat2 = re.compile(rf"^{re.escape(unit_id)}-{kind}\d*c?(\d+)$")
    for i in existing_ids:
        m = pat2.match(i)
        if m:
            try:
                nums.append(int(m.group(1)))
            except ValueError:
                pass
    return (max(nums) if nums else 0) + 1


def collect_ids(obj) -> set[str]:
    found = set()
    if isinstance(obj, dict):
        if isinstance(obj.get("id"), str):
            found.add(obj["id"])
        for v in obj.values():
            found |= collect_ids(v)
    elif isinstance(obj, list):
        for x in obj:
            found |= collect_ids(x)
    return found


def lesson_has_type(lesson: dict, typ: str) -> bool:
    return any(c.get("type") == typ for c in (lesson.get("cards") or []) if isinstance(c, dict))


def used_study_q_ids(book: dict) -> set[str]:
    """Track which Study_Notes question texts already appear as check.q to avoid dupes."""
    used = set()
    for u in book.get("units") or []:
        for L in u.get("lessons") or []:
            for c in L.get("cards") or []:
                if c.get("type") == "check" and c.get("q"):
                    used.add(c["q"].strip())
                if c.get("src_qid"):
                    used.add(c["src_qid"])
    return used


def detect_indent(text: str) -> int | str:
    for line in text.splitlines()[1:40]:
        if line.startswith("  ") and not line.startswith("   "):
            return 2
        if line.startswith("\t"):
            return "\t"
        if line.startswith(" "):
            # count leading spaces of first indented line
            n = len(line) - len(line.lstrip(" "))
            if n:
                return n
    return 1

def enrich_book(book_path: Path, chapters: list[dict]) -> dict:
    raw = book_path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    used_q = used_study_q_ids(book)
    # chapter_number -> exercises pool
    by_ch = {int(c["chapter_number"]): c for c in chapters}
    new_checks = 0
    touched_lessons = 0

    for unit in book.get("units") or []:
        ch_num = unit.get("number")
        if ch_num is None:
            continue
        chapter = by_ch.get(int(ch_num))
        if not chapter:
            continue
        pool = [
            q
            for q in (chapter.get("review_exercises") or [])
            if q.get("type") == "MC" and isinstance(q.get("options"), list) and len(q["options"]) >= 2
        ]
        # rotate unused
        pool = [q for q in pool if q.get("question", "").strip() not in used_q and q.get("id") not in used_q]

        for lesson in unit.get("lessons") or []:
            if new_checks >= MAX_NEW_CHECKS_PER_BOOK:
                break
            if lesson_has_type(lesson, "check") and lesson_has_type(lesson, "worked"):
                continue
            if not pool:
                break

            page = 1
            if lesson.get("pages"):
                try:
                    page = int(lesson["pages"][0])
                except Exception:
                    page = 1

            added_here = 0
            while added_here < CHECKS_PER_LESSON and pool and new_checks < MAX_NEW_CHECKS_PER_BOOK:
                q = pool.pop(0)
                opts = q["options"]
                letter = answer_letter(opts, q.get("correct_answer") or "")
                if not letter:
                    continue
                n = next_suffix(ids, unit["id"], "chk")
                chk_id = f"{unit['id']}-chk{n}"
                while chk_id in ids:
                    n += 1
                    chk_id = f"{unit['id']}-chk{n}"
                wrk_n = next_suffix(ids, unit["id"], "wrk")
                wrk_id = f"{unit['id']}-wrk{wrk_n}"
                while wrk_id in ids:
                    wrk_n += 1
                    wrk_id = f"{unit['id']}-wrk{wrk_n}"

                why = (q.get("explanation") or "").strip()
                if len(why) > 1200:
                    why = why[:1190] + "…"

                check = {
                    "id": chk_id,
                    "type": "check",
                    "title": "Quick check",
                    "page": page,
                    "src": "study_notes",
                    "src_qid": q.get("id"),
                    "q": q["question"],
                    "options": letters_options(opts),
                    "answer": letter,
                    "why": why or f"Correct answer: {letter}",
                }
                worked = {
                    "id": wrk_id,
                    "type": "worked",
                    "title": "Step-by-step",
                    "page": page,
                    "src": "study_notes",
                    "src_qid": q.get("id"),
                    "problem": q["question"],
                    "steps": explanation_steps(q.get("explanation") or ""),
                    "answer": letter,
                }
                lesson.setdefault("cards", []).append(check)
                lesson.setdefault("cards", []).append(worked)
                ids.add(chk_id)
                ids.add(wrk_id)
                used_q.add(q["question"].strip())
                if q.get("id"):
                    used_q.add(q["id"])
                added_here += 1
                new_checks += 1

            if added_here:
                touched_lessons += 1

                # light table once per unit if unit has no table cards yet
                unit_has_table = any(
                    c.get("type") == "table"
                    for L in unit.get("lessons") or []
                    for c in (L.get("cards") or [])
                )
                if not unit_has_table and chapter.get("chapter_title"):
                    tn = next_suffix(ids, unit["id"], "tbl")
                    tid = f"{unit['id']}-tbl{tn}"
                    while tid in ids:
                        tn += 1
                        tid = f"{unit['id']}-tbl{tn}"
                    # Build a tiny topic / tip table from first few exercise topics
                    topics = []
                    for qq in (chapter.get("review_exercises") or [])[:12]:
                        t = (qq.get("topic") or "").strip()
                        if t and t not in topics:
                            topics.append(t)
                    if len(topics) >= 2:
                        rows = [[t, "Review exercise topic — practice related checks"] for t in topics[:5]]
                        table = {
                            "id": tid,
                            "type": "table",
                            "title": "Topics to master",
                            "page": page,
                            "src": "study_notes",
                            "head": ["Topic", "How to use"],
                            "rows": rows,
                        }
                        lesson["cards"].append(table)
                        ids.add(tid)

        if new_checks >= MAX_NEW_CHECKS_PER_BOOK:
            break

    if new_checks:
        book_path.write_text(json.dumps(book, ensure_ascii=False, indent=indent) + "\n")
    return {"file": book_path.name, "new_checks": new_checks, "lessons": touched_lessons}


def main():
    study = json.loads(STUDY.read_text())
    chapters = [c for c in study["chapter_notes"] if c.get("subject") != "History"]
    # group by subject+grade
    groups: dict[tuple[str, str], list] = {}
    for c in chapters:
        subj = c["subject"]
        if subj not in SUBJECT_TO_BOOK:
            continue  # skip English 11-12 etc.
        groups.setdefault((SUBJECT_TO_BOOK[subj], str(c["grade"])), []).append(c)

    stats = []
    for (prefix, grade), chs in sorted(groups.items()):
        path = NOTES / f"{prefix}_{grade}.json"
        if not path.exists():
            print("skip missing", path.name)
            continue
        # snapshot history untouched guarantee: never open history_*
        assert "history" not in path.name
        before = path.read_bytes()
        st = enrich_book(path, chs)
        after = path.read_bytes()
        st["bytes_delta"] = len(after) - len(before)
        stats.append(st)
        print(f"{st['file']}: +{st['new_checks']} checks across {st['lessons']} lessons (Δ{st['bytes_delta']} B)")

    # ensure history files unchanged fingerprint
    for p in sorted(NOTES.glob("history_*.json")):
        print("history untouched:", p.name, p.stat().st_size)

    Path("/tmp/enrich_continue10_stats.json").write_text(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
