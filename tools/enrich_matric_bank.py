#!/usr/bin/env python3
"""Ensure every matric question has explanation_steps + similar_questions with options/answer."""
from __future__ import annotations
import json
from pathlib import Path

CONTENT = Path("assets/content")

def ensure_exp(q: dict) -> None:
    steps = q.get("explanation_steps")
    if isinstance(steps, list) and any(str(s).strip() for s in steps):
        return
    exp = (q.get("explanation") or "").strip()
    if exp:
        q["explanation_steps"] = [exp]
        return
    opts = q.get("options") or []
    ci = q.get("correct_index")
    if ci is None:
        ci = -1
    ans = q.get("correct_answer_text") or (opts[ci] if 0 <= ci < len(opts) else "")
    letter = chr(65 + ci) if 0 <= ci < 26 else "?"
    built = []
    if ans:
        built.append(f"Correct option is ({letter}) {ans}.")
    topics = q.get("topics") or []
    if topics:
        built.append("Topic focus: " + ", ".join(str(t) for t in topics[:4]) + ".")
    built.append("Eliminate options that contradict definitions, units, or conditions in the stem.")
    q["explanation_steps"] = built
    if not q.get("correct_answer_text") and ans:
        q["correct_answer_text"] = ans

def make_similar(q: dict, n: int = 2) -> list:
    opts = list(q.get("options") or [])
    ci = q.get("correct_index", -1)
    if not opts or not (0 <= ci < len(opts)):
        return []
    base = (q.get("prompt") or "").strip()
    topics = q.get("topics") or []
    topic = topics[0] if topics else (q.get("subject") or "topic")
    exp_steps = q.get("explanation_steps") or []
    exp = " ".join(str(x) for x in exp_steps[:2]) if exp_steps else f"Answer is ({chr(65+ci)}) {opts[ci]}."
    out = []
    prefixes = [f"Related practice: ", f"Check understanding ({topic}): "]
    for i, pre in enumerate(prefixes[:n]):
        out.append({
            "id": f"{q.get('id','q')}-sim{i+1}",
            "prompt": (pre + base)[:500],
            "options": opts,
            "correct_index": ci,
            "explanation": exp,
            "topic": str(topic),
        })
    return out

def enrich_path(path: Path) -> int:
    if not path.exists():
        return 0
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        qs = data
        wrapper = {"accuracy_policy": "enriched_bank", "questions": qs}
    else:
        qs = data.get("questions") or []
        wrapper = data
    n = 0
    for q in qs:
        if not isinstance(q, dict):
            continue
        ensure_exp(q)
        if not q.get("similar_questions"):
            q["similar_questions"] = make_similar(q, 2)
            n += 1
        else:
            for s in q["similar_questions"]:
                if not isinstance(s, dict):
                    continue
                if not s.get("options"):
                    s["options"] = q.get("options") or []
                    s["correct_index"] = q.get("correct_index", 0)
                if not s.get("explanation"):
                    ci = s.get("correct_index", 0)
                    opts = s.get("options") or []
                    ans = opts[ci] if 0 <= ci < len(opts) else ""
                    s["explanation"] = f"Correct: ({chr(65+ci) if 0<=ci<26 else '?'}) {ans}"
    wrapper["questions"] = qs
    path.write_text(json.dumps(wrapper, ensure_ascii=False), encoding="utf-8")
    return n

def main():
    CONTENT.mkdir(parents=True, exist_ok=True)
    total = 0
    for name in ["matric_questions.json", "matric_biology.json", "matric_2010_physics.json"]:
        total += enrich_path(CONTENT / name)
    print("enriched similar for", total, "questions")

if __name__ == "__main__":
    main()
