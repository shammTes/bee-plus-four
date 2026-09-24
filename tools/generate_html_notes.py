#!/usr/bin/env python3
"""Generate offline HTML unit notes with KaTeX from unit_notes_rich.json (and packs)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "assets" / "content"
OUT = CONTENT / "notes_html"
VENDOR_REL = "vendor"

CSS = """
:root {
  --bg: #0f172a;
  --card: #1e293b;
  --ink: #f1f5f9;
  --muted: #94a3b8;
  --accent: #14b8a6;
  --chip: #0f766e;
  --border: #334155;
}
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", sans-serif;
  line-height: 1.55;
  font-size: 16px;
}
.wrap { max-width: 720px; margin: 0 auto; padding: 16px 14px 48px; }
.hero {
  background: linear-gradient(135deg, #0f766e, #0d4f4f 55%, #0a2f2f);
  border-radius: 18px;
  padding: 18px 16px;
  margin-bottom: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,.25);
}
.badge {
  display: inline-block;
  background: rgba(255,255,255,.14);
  color: #ccfbf1;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: .04em;
  padding: 4px 10px;
  border-radius: 999px;
  margin-bottom: 8px;
}
h1 { font-size: 1.35rem; margin: 0 0 8px; font-weight: 800; }
.summary { color: #e2e8f0; font-size: .95rem; }
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 14px;
  margin: 12px 0;
}
.card h2 {
  margin: 0 0 10px;
  font-size: 1rem;
  color: var(--accent);
  font-weight: 800;
}
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; }
.chip {
  background: var(--chip);
  color: #ecfdf5;
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 999px;
  font-weight: 600;
}
.idea {
  border-left: 3px solid var(--accent);
  padding: 8px 0 8px 12px;
  margin: 8px 0;
  color: #e2e8f0;
}
.section h3 { margin: 0 0 6px; font-size: .95rem; }
.section p { margin: 0; color: #cbd5e1; }
.example, .exercise {
  background: #0b1220;
  border-radius: 12px;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #1e293b;
}
.example .label, .exercise .label {
  font-size: 11px; font-weight: 800; color: #5eead4; text-transform: uppercase;
  letter-spacing: .06em; margin-bottom: 6px;
}
.muted { color: var(--muted); font-size: .85rem; }
.katex-display { margin: 10px 0; overflow-x: auto; }
"""


def esc(s: object) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def mathify(text: str) -> str:
    return str(text or "")


def load_notes() -> list[dict]:
    paths = [
        CONTENT / "unit_notes_rich.json",
        CONTENT / "unit_notes.json",
        CONTENT / "unit_notes_g12.json",
        CONTENT / "unit_notes_g10_chemistry_clean.json",
        CONTENT / "unit_notes_english_grammar.json",
        CONTENT / "unit_notes_g9_english.json",
    ]
    by_key: dict[str, dict] = {}
    for p in paths:
        if not p.exists() or p.stat().st_size < 50:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        notes = d if isinstance(d, list) else d.get("notes") or d.get("units") or []
        for n in notes:
            if not isinstance(n, dict):
                continue
            g = str(n.get("grade") or "")
            s = str(n.get("subject") or "")
            u = int(n.get("unit_number") or 0)
            key = f"{g}|{s}|{u}"
            prev = by_key.get(key)
            score = len(str(n.get("summary") or "")) + 10 * len(n.get("sections") or [])
            if prev is None:
                by_key[key] = n
            else:
                prev_score = len(str(prev.get("summary") or "")) + 10 * len(prev.get("sections") or [])
                if score > prev_score:
                    by_key[key] = n
    return list(by_key.values())


def render_note(n: dict) -> str:
    g = esc(n.get("grade"))
    s = esc(n.get("subject"))
    u = int(n.get("unit_number") or 0)
    title = esc(n.get("title") or f"Unit {u}")
    summary = esc(mathify(n.get("summary") or ""))
    terms = n.get("key_terms") or []
    ideas = n.get("key_ideas") or []
    sections = n.get("sections") or []
    examples = n.get("examples") or []
    exercises = n.get("exercises") or []

    terms_html = "".join(f'<span class="chip">{esc(t)}</span>' for t in terms[:24])
    ideas_html = "".join(f'<div class="idea">{esc(mathify(i))}</div>' for i in ideas[:20])
    sec_html = []
    for sec in sections[:30]:
        if isinstance(sec, dict):
            h = esc(sec.get("heading") or "Section")
            e = esc(mathify(sec.get("explanation") or sec.get("body") or ""))
        else:
            h, e = "Section", esc(sec)
        sec_html.append(f'<div class="section card"><h3>{h}</h3><p>{e}</p></div>')
    ex_html = []
    for i, ex in enumerate(examples[:20], 1):
        if not isinstance(ex, dict):
            continue
        ex_html.append(
            f'<div class="example"><div class="label">Example {i}</div>'
            f'<div>{esc(mathify(ex.get("prompt") or ""))}</div>'
            f'<div class="muted" style="margin-top:8px"><strong>Solution:</strong> {esc(mathify(ex.get("solution") or ""))}</div></div>'
        )
    ez_html = []
    for i, ez in enumerate(exercises[:30], 1):
        if not isinstance(ez, dict):
            continue
        ez_html.append(
            f'<div class="exercise"><div class="label">Exercise {i}</div>'
            f'<div>{esc(mathify(ez.get("prompt") or ""))}</div>'
            f'<div class="muted" style="margin-top:8px"><strong>Answer:</strong> {esc(mathify(ez.get("answer") or ""))}</div>'
            f'<div class="muted"><strong>Why:</strong> {esc(mathify(ez.get("explanation") or ""))}</div></div>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5"/>
<title>{g} {s} · Unit {u} · {title}</title>
<link rel="stylesheet" href="{VENDOR_REL}/katex.min.css"/>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="badge">{g} · {s} · Unit {u}</div>
    <h1>{title}</h1>
    <p class="summary">{summary}</p>
  </div>
  {"<div class='card'><h2>Key terms</h2><div class='chip-row'>" + terms_html + "</div></div>" if terms_html else ""}
  {"<div class='card'><h2>Key ideas</h2>" + ideas_html + "</div>" if ideas_html else ""}
  {"".join(sec_html)}
  {"<div class='card'><h2>Worked examples</h2>" + "".join(ex_html) + "</div>" if ex_html else ""}
  {"<div class='card'><h2>Exercises</h2>" + "".join(ez_html) + "</div>" if ez_html else ""}
  <p class="muted">Offline notes · KaTeX math · Bee Plus 4</p>
</div>
<script src="{VENDOR_REL}/katex.min.js"></script>
<script src="{VENDOR_REL}/auto-render.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
  try {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "$", right: "$", display: false}},
        {{left: "\\\\(", right: "\\\\)", display: false}},
        {{left: "\\\\[", right: "\\\\]", display: true}}
      ],
      throwOnError: false
    }});
  }} catch (e) {{}}
}});
</script>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    notes = load_notes()
    index = []
    for n in notes:
        g = str(n.get("grade") or "GX")
        s = str(n.get("subject") or "SUB")
        u = int(n.get("unit_number") or 0)
        safe_s = re.sub(r"[^A-Za-z0-9]+", "_", s)
        name = f"{g}_{safe_s}_u{u}.html"
        path = OUT / name
        path.write_text(render_note(n), encoding="utf-8")
        index.append(
            {
                "grade": g,
                "subject": s,
                "unit_number": u,
                "title": n.get("title") or f"Unit {u}",
                "html_asset": f"assets/content/notes_html/{name}",
            }
        )
    (OUT / "index.json").write_text(json.dumps({"notes": index, "count": len(index)}, indent=2), encoding="utf-8")
    print(f"Wrote {len(index)} HTML notes → {OUT}")


if __name__ == "__main__":
    main()
