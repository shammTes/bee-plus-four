#!/usr/bin/env python3
"""Post-process unit_notes_rich: clean OCR, strengthen G9 Math worked solutions."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "assets" / "content"

def clean(s: str) -> str:
    if not s: return ""
    s = s.replace("\uf0b7", "•").replace("", "•").replace("", " ")
    s = s.replace("", "∈").replace("", "∉").replace("", "×")
    s = s.replace("Þ", "fi").replace("ß", "ss")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def polish_note(n: dict) -> dict:
    n = dict(n)
    n["grade"] = str(n.get("grade", "")).upper().replace("GRADE ", "G")
    if n["grade"].isdigit():
        n["grade"] = "G" + n["grade"]
    n["subject"] = str(n.get("subject", "")).upper().replace(" ", "_")
    n["unit_number"] = int(n.get("unit_number") or 0)
    n["title"] = clean(str(n.get("title") or ""))
    n["summary"] = clean(str(n.get("summary") or ""))
    n["key_terms"] = [clean(str(t)) for t in (n.get("key_terms") or []) if clean(str(t))]
    n["key_ideas"] = [clean(str(t)) for t in (n.get("key_ideas") or []) if clean(str(t))]
    n["key_idea_ti"] = ""
    sections = []
    for sec in n.get("sections") or []:
        h, e = clean(str(sec.get("heading") or "")), clean(str(sec.get("explanation") or ""))
        if len(e) >= 40:
            sections.append({"heading": h, "explanation": e})
    n["sections"] = sections
    examples = []
    for i, ex in enumerate(n.get("examples") or [], 1):
        prompt = clean(str(ex.get("prompt") or ""))
        sol = clean(str(ex.get("solution") or ""))
        if not sol or "see worked" in sol.lower() or (len(sol) < 60 and "textbook" in sol.lower()):
            sol = (
                f"Worked approach (Unit {n['unit_number']} — {n['title']}):\n"
                f"1) Write the given information.\n"
                f"2) Apply the definition or formula from this unit.\n"
                f"3) Simplify and state the final answer clearly.\n"
                f"Given: {prompt[:300]}"
            )
        examples.append({"id": ex.get("id") or f"{n['grade']}_{n['subject']}_U{n['unit_number']}_EX{i}", "prompt": prompt, "solution": sol})
    n["examples"] = examples
    exercises = []
    for i, ex in enumerate(n.get("exercises") or [], 1):
        prompt = clean(str(ex.get("prompt") or ""))
        ans = clean(str(ex.get("answer") or ""))
        expl = clean(str(ex.get("explanation") or ""))
        if not ans or "textbook" in ans.lower():
            ans = "Apply the unit method step by step; verify with definitions in the notes."
        if not expl:
            expl = f"Use the rules from Unit {n['unit_number']}: {n['title']}."
        exercises.append({
            "id": ex.get("id") or f"{n['grade']}_{n['subject']}_U{n['unit_number']}_Q{i}",
            "type": ex.get("type") or "practice",
            "prompt": prompt, "answer": ans, "explanation": expl,
        })
    n["exercises"] = exercises
    return n

G9_MATH_EXTRA = {
    1: [
        {"id":"G9_MATH_U1_EX1","prompt":"Let A = {1, 2, 3, 4, 5, 6, 7}. Write ∈ / ∉ statements for 2 and 8.","solution":"2 ∈ A (2 is an element of A).\n8 ∉ A (8 is not an element of A)."},
        {"id":"G9_MATH_U1_EX2","prompt":"A = {x,y,z,u,v}, B = {1,2,3,4,5}. Equal? Equivalent?","solution":"A ≠ B (different elements).\n|A|=|B|=5 → equivalent sets (A ∼ B)."},
        {"id":"G9_MATH_U1_EX3","prompt":"A={2,4,5}, B={1,3,6}. Find A × B.","solution":"A × B = {(2,1),(2,3),(2,6),(4,1),(4,3),(4,6),(5,1),(5,3),(5,6)} (9 ordered pairs)."},
        {"id":"G9_MATH_U1_EX4","prompt":"A={1,2}, B={1,2,3}. Subset vs proper subset.","solution":"A ⊆ B. Since A ≠ B, A is a proper subset (A ⊂ B). B ⊈ A."},
        {"id":"G9_MATH_U1_EX5","prompt":"U={1..6}, A={1,2,3}, B={3,4,5}. Find ∪, ∩, −, complement of A.","solution":"A∪B={1,2,3,4,5}; A∩B={3}; A−B={1,2}; A′={4,5,6}."},
    ],
    3: [
        {"id":"G9_MATH_U3_EX1","prompt":"Line through (0,2) with slope 3. Write y = mx + b.","solution":"m=3, b=2 → y = 3x + 2."},
        {"id":"G9_MATH_U3_EX2","prompt":"Slope through A(1,2) and B(4,8).","solution":"m = (8−2)/(4−1) = 6/3 = 2."},
    ],
    4: [
        {"id":"G9_MATH_U4_EX1","prompt":"Solve x² − 5x + 6 = 0 by factoring.","solution":"(x−2)(x−3)=0 → x=2 or x=3."},
        {"id":"G9_MATH_U4_EX2","prompt":"Vertex of y = x² − 4x + 3.","solution":"x = −b/(2a)=2; y=4−8+3=−1. Vertex (2,−1). Opens up (a>0)."},
    ],
}

def main():
    CONTENT.mkdir(parents=True, exist_ok=True)
    path = CONTENT / "unit_notes_rich.json"
    if not path.exists():
        path = CONTENT / "unit_notes.json"
    if not path.exists():
        print("no notes to polish"); return
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        notes = data.get("notes") or data.get("units") or []
        if not notes and "books" in data:
            notes = []
            for b in data["books"]:
                notes.extend(b.get("units") or b.get("notes") or [])
    else:
        notes = data
    out = []
    for n in notes:
        if not isinstance(n, dict):
            continue
        p = polish_note(n)
        if p["grade"] == "G9" and p["subject"] == "MATH" and p["unit_number"] in G9_MATH_EXTRA:
            p["examples"] = G9_MATH_EXTRA[p["unit_number"]] + p["examples"]
        out.append(p)
    out.sort(key=lambda n: (n["grade"], n["subject"], n["unit_number"]))
    (CONTENT / "unit_notes.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    (CONTENT / "unit_notes_rich.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    for g in ("G9","G10","G11","G12"):
        sub = [n for n in out if n["grade"]==g]
        (CONTENT / f"unit_notes_{g.lower()}.json").write_text(json.dumps(sub, ensure_ascii=False), encoding="utf-8")
    g9m = [n for n in out if n["grade"]=="G9" and n["subject"]=="MATH"]
    print(f"polished {len(out)} notes; G9 MATH units={len(g9m)}")
    for n in g9m:
        print(f"  U{n['unit_number']} {n['title']} sec={len(n['sections'])} ex={len(n['examples'])}")

if __name__ == "__main__":
    main()
