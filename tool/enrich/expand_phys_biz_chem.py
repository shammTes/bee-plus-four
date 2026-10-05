#!/usr/bin/env python3
"""Expand Physics 10/11, Business 10u3/11u2, Chem9/Chem10u1 from Study_Notes.json."""
from __future__ import annotations

import json
import re
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "assets/high/notes/notes"
STUDY = Path("/workspace/tmp-sync/drive/Study_Notes.json")

HAS_TIGRINYA = re.compile(r"[\u1200-\u137F]")


def detect_indent(text: str) -> int:
    for line in text.splitlines()[1:40]:
        if line.startswith(" "):
            n = len(line) - len(line.lstrip(" "))
            if n:
                return n
    return 2


def collect_ids(obj) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        if isinstance(obj.get("id"), str):
            found.add(obj["id"])
        for v in obj.values():
            found |= collect_ids(v)
    elif isinstance(obj, list):
        for x in obj:
            found |= collect_ids(x)
    return found


def next_tb_id(ids: set[str], unit_id: str) -> str:
    n = 1
    while f"{unit_id}-tb{n}" in ids:
        n += 1
    cid = f"{unit_id}-tb{n}"
    ids.add(cid)
    return cid


def next_chk_id(ids: set[str], unit_id: str) -> str:
    n = 1
    while f"{unit_id}-chk{n}" in ids or f"{unit_id}-chk{n}c1" in ids:
        # also skip if any chkN exists
        if not any(i.startswith(f"{unit_id}-chk{n}") for i in ids):
            break
        n += 1
    # find max existing
    nums = []
    for i in ids:
        m = re.match(rf"^{re.escape(unit_id)}-chk(\d+)", i)
        if m:
            nums.append(int(m.group(1)))
    n = (max(nums) if nums else 0) + 1
    cid = f"{unit_id}-chk{n}"
    while cid in ids:
        n += 1
        cid = f"{unit_id}-chk{n}"
    ids.add(cid)
    return cid


def strip_topic_challenge(text: str) -> str:
    # Remove Topic Challenge blocks and answer keys
    text = re.split(r"###\s*📝\s*Topic Challenge", text)[0]
    text = re.split(r"###\s*📝\s*ናይቲ", text)[0]
    text = re.split(r"##\s+\d+\.\d+\s+Answers to Topic", text)[0]
    return text.strip()


def is_mostly_tigrinya(text: str) -> bool:
    ti = len(HAS_TIGRINYA.findall(text))
    return ti > 40 and ti > len(re.findall(r"[A-Za-z]", text)) * 0.3


def md_to_paragraphs(md: str) -> list[str]:
    """Convert markdown section body into paragraph list."""
    md = md.strip()
    # drop leading ## heading line
    lines = md.splitlines()
    if lines and lines[0].startswith("#"):
        lines = lines[1:]
    md = "\n".join(lines).strip()
    if not md:
        return []

    # Convert markdown tables to readable lines
    def table_to_text(block: str) -> str:
        rows = []
        for ln in block.splitlines():
            if re.match(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", ln):
                continue
            if "|" not in ln:
                continue
            cells = [c.strip().strip("*") for c in ln.strip().strip("|").split("|")]
            cells = [c for c in cells if c]
            if cells:
                rows.append(" — ".join(cells))
        return " | ".join(rows) if rows else block

    # Split out tables
    parts: list[str] = []
    buf: list[str] = []
    in_table = False
    table_buf: list[str] = []
    for ln in md.splitlines():
        if ln.strip().startswith("|"):
            if not in_table:
                if buf:
                    parts.append("\n".join(buf))
                    buf = []
                in_table = True
                table_buf = [ln]
            else:
                table_buf.append(ln)
        else:
            if in_table:
                parts.append(table_to_text("\n".join(table_buf)))
                table_buf = []
                in_table = False
            buf.append(ln)
    if in_table:
        parts.append(table_to_text("\n".join(table_buf)))
    if buf:
        parts.append("\n".join(buf))

    paras: list[str] = []
    for part in parts:
        # bullet blocks keep as separate paras or join
        chunks = re.split(r"\n\s*\n", part)
        for ch in chunks:
            ch = ch.strip()
            if not ch:
                continue
            # flatten single newlines inside paragraph except bullets
            if re.search(r"^\s*[-*•]|\^\s*\d+\.", ch, re.M) or ch.lstrip().startswith("*"):
                # keep bullet list as one paragraph with newlines -> join with spaces carefully
                items = []
                for bl in ch.splitlines():
                    bl = bl.strip()
                    if not bl:
                        continue
                    bl = re.sub(r"^[-*•]\s+", "• ", bl)
                    bl = re.sub(r"^\*\s+", "• ", bl)
                    items.append(bl)
                text = " ".join(items)
            else:
                text = re.sub(r"\s*\n\s*", " ", ch)
            # clean markdown bold/italics lightly (keep ** for app)
            text = re.sub(r"[ \t]+", " ", text).strip()
            # skip empty / challenge leftovers
            if not text or text.startswith("### 📝"):
                continue
            if is_mostly_tigrinya(text):
                continue
            # drop very short fluff
            if len(text) < 40 and not text.startswith("$$"):
                continue
            # cap very long paragraphs by sentence split
            if len(text) > 900:
                sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z$$\*])", text)
                cur = ""
                for s in sentences:
                    if not s:
                        continue
                    if len(cur) + len(s) < 750:
                        cur = (cur + " " + s).strip()
                    else:
                        if cur:
                            paras.append(cur)
                        cur = s
                if cur:
                    paras.append(cur)
            else:
                paras.append(text)
    return paras


def split_sections(content_en: str) -> list[tuple[str, str]]:
    """Return list of (heading, body_md) for ## sections."""
    if not content_en:
        return []
    parts = re.split(r"(?=^##\s+)", content_en, flags=re.M)
    out = []
    for p in parts:
        p = p.strip()
        if not p.startswith("##"):
            continue
        first, _, rest = p.partition("\n")
        title = first.lstrip("#").strip()
        # skip answers / tigrinya chapter duplicates
        if re.search(r"Answers to Topic", title, re.I):
            continue
        if is_mostly_tigrinya(title) or is_mostly_tigrinya(p[:500]):
            continue
        body = strip_topic_challenge(rest)
        if len(body) < 80:
            continue
        out.append((title, body))
    return out


def chunk_paras(paras: list[str], max_paras: int = 4, max_chars: int = 2200) -> list[list[str]]:
    """Break a long paragraph list into scrollable multi-card chunks."""
    if not paras:
        return []
    chunks: list[list[str]] = []
    cur: list[str] = []
    cur_len = 0
    for p in paras:
        if cur and (len(cur) >= max_paras or cur_len + len(p) > max_chars):
            chunks.append(cur)
            cur = []
            cur_len = 0
        cur.append(p)
        cur_len += len(p)
    if cur:
        chunks.append(cur)
    return chunks


def split_subcards(heading: str, body: str) -> list[tuple[str, list[str]]]:
    """Split a ## section into cards on ### headings; chunk long bodies."""
    chunks = re.split(r"(?=^###\s+)", body, flags=re.M)
    cards: list[tuple[str, list[str]]] = []

    def add_titled(title: str, paras: list[str]) -> None:
        if not paras:
            return
        parts = chunk_paras(paras)
        if len(parts) == 1:
            t = title if len(title) <= 100 else title[:97] + "…"
            cards.append((t, parts[0]))
            return
        for i, part in enumerate(parts, 1):
            t = f"{title} ({i}/{len(parts)})"
            if len(t) > 100:
                t = t[:97] + "…"
            cards.append((t, part))

    lead = chunks[0].strip() if chunks else ""
    if lead:
        paras = md_to_paragraphs("## lead\n" + lead)
        add_titled(heading, paras)
    for ch in chunks[1:]:
        first, _, rest = ch.partition("\n")
        sub = first.lstrip("#").strip()
        if "Topic Challenge" in sub or sub.startswith("📝"):
            continue
        if is_mostly_tigrinya(sub):
            continue
        paras = md_to_paragraphs("## x\n" + rest)
        if not paras:
            continue
        title = f"{heading} — {sub}" if not heading.startswith(sub[:20]) else sub
        add_titled(title, paras)
    return cards


def existing_body_prefixes(book: dict) -> set[str]:
    prefs: set[str] = set()
    for u in book.get("units") or []:
        for L in u.get("lessons") or []:
            for c in L.get("cards") or []:
                body = c.get("body")
                if isinstance(body, list) and body:
                    prefs.add(str(body[0])[:80].strip().lower())
                elif isinstance(body, str) and body:
                    prefs.add(body[:80].strip().lower())
    return prefs


def lesson_page(lesson: dict) -> int:
    pages = lesson.get("pages") or []
    if pages:
        try:
            return int(pages[0])
        except Exception:
            pass
    return 0


def extract_lesson_num(title: str) -> str | None:
    m = re.match(r"^(\d+\.\d+)", title.strip())
    return m.group(1) if m else None


def map_section_to_lessons(unit: dict, sec_title: str) -> list[dict]:
    """Map a Study Notes ## heading to one or more lessons in the unit."""
    lessons = unit.get("lessons") or []
    if not lessons:
        return []
    sec_num = extract_lesson_num(sec_title)
    # Direct number match: 1.1 -> lesson number 1.1
    if sec_num:
        exact = [L for L in lessons if str(L.get("number")) == sec_num]
        if exact:
            return exact
        # Prefix match e.g. section 3.1 matches lesson 3.1
        # Also if section is "3.1 & 3.2" match both
        amps = re.findall(r"(\d+\.\d+)", sec_title)
        matched = []
        for n in amps:
            matched.extend([L for L in lessons if str(L.get("number")) == n])
        if matched:
            # unique preserve order
            seen = set()
            out = []
            for L in matched:
                if L["id"] not in seen:
                    seen.add(L["id"])
                    out.append(L)
            return out

    # Keyword similarity
    sec_l = sec_title.lower()
    scored = []
    for L in lessons:
        lt = (L.get("title") or "").lower()
        score = 0
        # shared significant words
        sw = set(re.findall(r"[a-z]{4,}", sec_l))
        lw = set(re.findall(r"[a-z]{4,}", lt))
        score = len(sw & lw)
        scored.append((score, L))
    scored.sort(key=lambda x: -x[0])
    if scored and scored[0][0] >= 1:
        # return top match; if tie within 0, include close ones
        top = scored[0][0]
        return [L for s, L in scored if s >= max(1, top - 0) and s == top][:2]
    # fallback: first lesson
    return [lessons[0]]


def distribute_cards(lessons: list[dict], cards: list[tuple[str, list[str]]]) -> dict[str, list[tuple[str, list[str]]]]:
    """Distribute cards across matched lessons round-robin if multiple."""
    out: dict[str, list] = {L["id"]: [] for L in lessons}
    if len(lessons) == 1:
        out[lessons[0]["id"]] = cards
        return out
    # First card (lead) to first lesson; remaining round-robin or by title keywords
    for i, card in enumerate(cards):
        title, paras = card
        # try keyword match among lessons
        best = lessons[i % len(lessons)]
        best_score = -1
        tl = title.lower()
        for L in lessons:
            lw = set(re.findall(r"[a-z]{4,}", (L.get("title") or "").lower()))
            tw = set(re.findall(r"[a-z]{4,}", tl))
            sc = len(lw & tw)
            if sc > best_score:
                best_score = sc
                best = L
        if best_score <= 0:
            best = lessons[min(i, len(lessons) - 1)]
        out[best["id"]].append(card)
    return out


def letters_options(opts: list[str]) -> dict[str, str]:
    return {chr(65 + i): o for i, o in enumerate(opts[:5])}


def answer_letter(opts: list[str], correct: str) -> str | None:
    for i, o in enumerate(opts[:5]):
        if o.strip() == (correct or "").strip():
            return chr(65 + i)
    def norm(s: str) -> str:
        return re.sub(r"\s+", "", s or "").replace("$$", "")
    nc = norm(correct)
    for i, o in enumerate(opts[:5]):
        if norm(o) == nc:
            return chr(65 + i)
    return None


def used_check_qs(book: dict) -> set[str]:
    used = set()
    for u in book.get("units") or []:
        for L in u.get("lessons") or []:
            for c in L.get("cards") or []:
                if c.get("type") == "check" and c.get("q"):
                    used.add(c["q"].strip())
    return used


def add_checks(unit: dict, chapter: dict, ids: set[str], used_q: set[str], max_per_unit: int = 4) -> int:
    pool = [
        q
        for q in (chapter.get("review_exercises") or [])
        if q.get("type") == "MC"
        and isinstance(q.get("options"), list)
        and len(q["options"]) >= 2
        and q.get("question", "").strip() not in used_q
    ]
    added = 0
    lessons = unit.get("lessons") or []
    if not lessons or not pool:
        return 0
    # Prefer lessons with fewer checks
    def n_checks(L):
        return sum(1 for c in L.get("cards") or [] if c.get("type") == "check")

    lessons_sorted = sorted(lessons, key=n_checks)
    for L in lessons_sorted:
        if added >= max_per_unit:
            break
        # add up to 2 per unit total already limited; 1 per lesson pass
        if n_checks(L) >= 4:
            continue
        while pool and added < max_per_unit:
            q = pool.pop(0)
            opts = q["options"]
            letter = answer_letter(opts, q.get("correct_answer") or "")
            if not letter:
                continue
            chk_id = next_chk_id(ids, unit["id"])
            why = (q.get("explanation") or "").strip()
            # strip tigrinya explanation if mixed - explanation is English
            if len(why) > 900:
                why = why[:890] + "…"
            check = {
                "id": chk_id,
                "type": "check",
                "title": "Quick check",
                "page": lesson_page(L),
                "src": "study_notes",
                "q": q["question"].strip(),
                "options": letters_options(opts),
                "answer": letter,
                "why": why or "Review the lesson notes and eliminate wrong options.",
            }
            L.setdefault("cards", []).append(check)
            used_q.add(q["question"].strip())
            added += 1
            break  # one per lesson in this pass
    return added


def update_intro(unit: dict, chapter: dict) -> bool:
    intro = (unit.get("intro") or "").strip()
    if len(intro) >= 200:
        return False
    content = chapter.get("content_en") or ""
    # first bold definition sentence
    m = re.search(r"\*\*([^*]{40,400})\*\*", content)
    if m:
        unit["intro"] = m.group(1).strip()
        return True
    # first paragraph
    secs = split_sections(content)
    if secs:
        paras = md_to_paragraphs("## x\n" + secs[0][1][:800])
        if paras:
            unit["intro"] = paras[0][:500]
            return True
    return False


def expand_unit_from_study(
    book: dict,
    unit: dict,
    chapter: dict,
    ids: set[str],
    prefs: set[str],
    used_q: set[str],
    stats: dict,
) -> None:
    sections = split_sections(chapter.get("content_en") or "")
    added_cards = 0
    for sec_title, body in sections:
        cards = split_subcards(sec_title, body)
        lessons = map_section_to_lessons(unit, sec_title)
        # If one Study Notes section produced many cards, spread across nearby lessons
        if len(cards) >= 3 and len(lessons) == 1:
            all_lessons = unit.get("lessons") or []
            idx = next((i for i, L in enumerate(all_lessons) if L["id"] == lessons[0]["id"]), 0)
            # take this lesson and following ones up to card count
            span = min(len(all_lessons), max(len(lessons), min(len(cards), len(all_lessons) - idx)))
            lessons = all_lessons[idx: idx + max(1, span)]
            if len(lessons) < 2 and idx > 0:
                lessons = all_lessons[max(0, idx - 1): idx + 2]
        dist = distribute_cards(lessons, cards)
        for L in lessons:
            for title, paras in dist.get(L["id"], []):
                if not paras:
                    continue
                pref = paras[0][:80].strip().lower()
                if pref in prefs:
                    continue
                # also skip if any existing body starts with same 80
                cid = next_tb_id(ids, unit["id"])
                card = {
                    "id": cid,
                    "type": "text",
                    "title": title[:100],
                    "page": lesson_page(L),
                    "src": "study_notes",
                    "enriched": True,
                    "body": paras,
                }
                L.setdefault("cards", []).append(card)
                prefs.add(pref)
                added_cards += 1
    n_chk = add_checks(unit, chapter, ids, used_q, max_per_unit=4)
    intro_upd = update_intro(unit, chapter)
    stats["cards"] = stats.get("cards", 0) + added_cards
    stats["checks"] = stats.get("checks", 0) + n_chk
    stats["intro"] = stats.get("intro", 0) + (1 if intro_upd else 0)


def load_chapters(study: dict, subject: str, grade: str) -> dict[int, dict]:
    out = {}
    for c in study["chapter_notes"]:
        if c.get("subject") == subject and str(c.get("grade")) == str(grade):
            out[int(c["chapter_number"])] = c
    return out


# ---------- Chemistry handcrafted expansions ----------

CHEM9_U1_CARDS = [
    (
        "chem9-u1-l1-2",
        "Intensive vs extensive properties",
        [
            "Properties of matter are often grouped as intensive or extensive. An intensive property does not depend on how much sample you have. An extensive property does depend on the amount of matter.",
            "Intensive examples: density, temperature, colour, melting point, boiling point, hardness, and refractive index. One drop of pure water and a litre of pure water both boil at about $$100^\\circ\\text{C}$$ at the same pressure — the boiling point did not change with amount.",
            "Extensive examples: mass, volume, length, and total heat energy stored in a sample. Two litres of water have twice the mass and twice the volume of one litre. If you double the sample, extensive quantities roughly double.",
            "Density links the two ideas: $$\\rho = \\dfrac{m}{V}$$. Mass and volume are extensive, but their ratio (density) is intensive for a uniform material. That is why chemists use density to identify substances without needing a fixed sample size.",
            "Quick check: temperature is intensive (a cup and a pot of boiling water can both be at $$100^\\circ\\text{C}$$). Total thermal energy is extensive (the pot stores more heat). Mass is extensive; colour is intensive.",
        ],
    ),
    (
        "chem9-u1-l1-4",
        "Separation methods — when to use each",
        [
            "Mixtures can be separated by physical methods because the components keep their own identities. Choose the method that matches the difference between the parts (particle size, boiling point, solubility, magnetism, density).",
            "Filtration: separates an insoluble solid from a liquid (or gas). Example: sand from muddy water. The solid trapped on the filter paper is the residue; the liquid that passes through is the filtrate.",
            "Evaporation: removes a liquid solvent by heating so a dissolved solid is left behind. Example: recovering salt from salt water. Good when you want the solid and do not need the liquid.",
            "Distillation: boils a liquid and condenses the vapour to collect a purified liquid. Simple distillation separates a liquid from a dissolved solid or liquids with very different boiling points. Fractional distillation separates liquids whose boiling points are closer (e.g. components of crude oil).",
            "Decantation: carefully pours off a liquid from a settled solid (or from another immiscible liquid). Example: pouring water off after mud has settled. Faster than filtration for coarse sediments, but less complete.",
            "Magnetism: pulls magnetic materials (like iron filings) out of a non-magnetic mixture (like sulphur powder). Useful when one component is ferromagnetic.",
            "Chromatography: separates dissolved substances that travel at different speeds on paper or another medium with a moving solvent. Example: separating ink dyes. Useful for small amounts and coloured mixtures.",
            "Other common methods: sieving (different particle sizes), separating funnel (immiscible liquids like oil and water), and centrifugation (speeds settling of fine suspensions).",
        ],
    ),
]

CHEM9_U2_CARDS = [
    (
        "chem9-u2-l2-1",
        "Average atomic mass (isotopes)",
        [
            "Most elements exist as isotopes: atoms with the same number of protons (same atomic number $$Z$$) but different numbers of neutrons, so they have different mass numbers $$A$$.",
            "The atomic mass listed on the periodic table is not usually the mass of one single isotope. It is a weighted average of the masses of the naturally occurring isotopes, weighted by how common each isotope is (relative abundance).",
            "Formula idea: $$\\text{average atomic mass} = \\sum (\\text{isotopic mass} \\times \\text{fractional abundance})$$. Percent abundance must first be converted to a fraction (divide by 100).",
            "Worked example: Chlorine has two main isotopes. Suppose $$^{35}\\text{Cl}$$ has mass $$34.97\\text{ u}$$ and abundance $$75.78\\%$$, and $$^{37}\\text{Cl}$$ has mass $$36.97\\text{ u}$$ and abundance $$24.22\\%$$.",
            "Average mass $$= (34.97)(0.7578) + (36.97)(0.2422) = 26.50 + 8.95 = 35.45\\text{ u}$$ (approximately). That matches the periodic-table value for chlorine.",
            "Why it matters: chemical calculations use this average so that a mole of natural chlorine atoms has the correct total mass, even though individual atoms are $$^{35}\\text{Cl}$$ or $$^{37}\\text{Cl}$$.",
        ],
    ),
    (
        "chem9-u2-l2-1",
        "Electron configuration (Grade 9 shells)",
        [
            "Electrons occupy energy levels (shells) around the nucleus. For Grade 9 we use a simple shell model: shell 1 holds up to 2 electrons, shell 2 up to 8, shell 3 up to 8 for the first 20 elements (a useful classroom rule before full subshell capacity is taught).",
            "Write configurations by filling lower shells first (Aufbau idea at shell level). Example: sodium ($$Z=11$$) is $$2,8,1$$. Oxygen ($$Z=8$$) is $$2,6$$. Calcium ($$Z=20$$) is $$2,8,8,2$$.",
            "Valence electrons are the electrons in the outermost shell. They largely decide bonding and chemical behaviour. Sodium has 1 valence electron; oxygen has 6.",
            "Noble-gas configurations are especially stable (helium $$2$$; neon $$2,8$$; argon $$2,8,8$$). Other atoms often gain, lose, or share electrons to reach a similar outer-shell count (octet / duplet ideas).",
            "Link to the periodic table: elements in the same group have the same number of valence electrons (for main-group elements), which is why they show similar chemistry.",
            "Practice: magnesium $$Z=12$$ → $$2,8,2$$ (loses 2 electrons to form $$\\text{Mg}^{2+}$$). Fluorine $$Z=9$$ → $$2,7$$ (gains 1 electron to form $$\\text{F}^{-}$$).",
        ],
    ),
    (
        "chem9-u2-l2-2",
        "Ionic vs covalent bonding (text focus)",
        [
            "Ionic bonding: a metal atom transfers one or more valence electrons to a non-metal atom. The metal becomes a positive ion (cation) and the non-metal a negative ion (anion). Electrostatic attraction holds the ions together. Example: sodium and chlorine form $$\\text{Na}^{+}$$ and $$\\text{Cl}^{-}$$.",
            "Covalent bonding: non-metal atoms share pairs of valence electrons so each atom can approach a stable outer shell. Example: two hydrogen atoms share a pair to make $$\\text{H}_2$$; oxygen and hydrogen share pairs to make water $$\\text{H}_2\\text{O}$$.",
            "Properties (qualitative): ionic compounds often form brittle crystalline solids with high melting points and conduct electricity when molten or dissolved. Many covalent molecular substances have lower melting points and do not conduct as solids.",
            "Electronegativity difference is a helpful guide: a large difference favours electron transfer (ionic character); a small difference favours sharing (covalent character). Real bonds can be partly ionic and partly covalent.",
        ],
    ),
]

CHEM9_U3_CARDS = [
    (
        "chem9-u3-l3-2",
        "Naming binary ionic and covalent compounds",
        [
            "Binary compounds contain two elements. Naming depends on whether the compound is ionic (metal + non-metal) or covalent (two non-metals).",
            "Binary ionic names: name the metal (cation) first as the element name, then the non-metal (anion) with the ending changed to -ide. Examples: $$\\text{NaCl}$$ sodium chloride; $$\\text{MgO}$$ magnesium oxide; $$\\text{CaBr}_2$$ calcium bromide.",
            "If the metal can form more than one ion (many transition metals), show the charge with a Roman numeral: $$\\text{FeCl}_2$$ iron(II) chloride; $$\\text{FeCl}_3$$ iron(III) chloride.",
            "Binary covalent names (two non-metals): use prefixes to show how many atoms of each element — mono-, di-, tri-, tetra-, penta-, hexa-. Usually omit mono- on the first element. The second element ends in -ide. Examples: $$\\text{CO}$$ carbon monoxide; $$\\text{CO}_2$$ carbon dioxide; $$\\text{N}_2\\text{O}_4$$ dinitrogen tetroxide.",
            "Building formulas from ions: write the cation and anion symbols with charges, then balance total positive and negative charge so the formula is neutral. Example: $$\\text{Al}^{3+}$$ and $$\\text{O}^{2-}$$ → cross charges to get $$\\text{Al}_2\\text{O}_3$$.",
            "Polyatomic ions keep their names inside compounds: $$\\text{NaNO}_3$$ sodium nitrate; $$\\text{CaSO}_4$$ calcium sulphate (sulfate); $$\\text{NH}_4\\text{Cl}$$ ammonium chloride.",
        ],
    ),
    (
        "chem9-u3-l3-2",
        "Empirical vs molecular formula",
        [
            "An empirical formula shows the simplest whole-number ratio of atoms of each element in a compound. A molecular formula shows the actual number of atoms of each element in one molecule.",
            "Example: hydrogen peroxide has molecular formula $$\\text{H}_2\\text{O}_2$$. The simplest ratio of H:O is 1:1, so the empirical formula is $$\\text{HO}$$. Glucose has molecular formula $$\\text{C}_6\\text{H}_{12}\\text{O}_6$$ and empirical formula $$\\text{CH}_2\\text{O}$$.",
            "For ionic compounds we usually write the empirical formula (the formula unit), because there is no single molecule — e.g. $$\\text{NaCl}$$, $$\\text{MgCl}_2$$.",
            "Worked example: A compound is $$40.0\\%$$ C, $$6.7\\%$$ H, and $$53.3\\%$$ O by mass. Assume $$100\\text{ g}$$ sample → $$40.0\\text{ g}$$ C, $$6.7\\text{ g}$$ H, $$53.3\\text{ g}$$ O.",
            "Moles: $$n_\\text{C} = 40.0/12.0 = 3.33$$; $$n_\\text{H} = 6.7/1.0 = 6.7$$; $$n_\\text{O} = 53.3/16.0 = 3.33$$. Divide by $$3.33$$ → C:H:O = $$1:2:1$$. Empirical formula = $$\\text{CH}_2\\text{O}$$.",
            "If the molar mass of the compound is $$180\\text{ g/mol}$$ and the empirical formula mass of $$\\text{CH}_2\\text{O}$$ is $$30\\text{ g/mol}$$, then $$n = 180/30 = 6$$. Molecular formula = $$\\text{C}_6\\text{H}_{12}\\text{O}_6$$.",
        ],
    ),
    (
        "chem9-u3-l3-1",
        "Building chemical formulas from ions",
        [
            "To write an ionic formula: (1) write the symbols and charges of the ions; (2) find the smallest whole numbers that make total positive charge equal total negative charge; (3) write those numbers as subscripts (omit 1).",
            "Examples: $$\\text{Na}^{+}$$ + $$\\text{Cl}^{-}$$ → $$\\text{NaCl}$$. $$\\text{Ca}^{2+}$$ + $$\\text{Cl}^{-}$$ → $$\\text{CaCl}_2$$. $$\\text{Al}^{3+}$$ + $$\\text{SO}_4^{2-}$$ → $$\\text{Al}_2(\\text{SO}_4)_3$$ (parentheses keep the polyatomic ion together).",
            "Never write charges in the final formula of a neutral compound. Charges are only tools for balancing.",
            "For covalent molecules, formulas come from how many atoms are bonded in the molecule (often learned from prefixes in the name or from known molecules), not from ion charge balance.",
        ],
    ),
]

CHEM10_U1_CARDS = [
    (
        "chem10-u1-l1-1",
        "Newlands — Law of Octaves",
        [
            "By the 1860s more elements were known, and chemists looked for repeating patterns. In 1864–1865 the English chemist John Newlands arranged known elements in order of increasing atomic mass.",
            "Newlands noticed that every eighth element seemed to show properties similar to the first, like notes repeating every octave in music. He called this the Law of Octaves.",
            "Example idea: if you list Li, Be, B, C, N, O, F, then Na (the 8th after Li in his listing) resembles lithium; K resembles sodium, and so on for the lighter elements.",
            "Limitations: the law worked reasonably only for the lighter elements. It broke down for heavier elements; Newlands sometimes forced dissimilar elements into the same group to keep the octave pattern. New elements being discovered did not fit neatly. Many chemists rejected the musical analogy at first.",
            "Despite its limits, Newlands helped establish that properties of elements repeat periodically when elements are ordered by mass — an important step toward the modern periodic table.",
        ],
    ),
    (
        "chem10-u1-l1-1",
        "Mendeleev’s periodic table",
        [
            "In 1869 the Russian chemist Dmitri Mendeleev arranged elements mainly in order of increasing atomic mass, but he also grouped elements with similar chemical properties into vertical columns (groups).",
            "When the mass order conflicted with chemical similarity, Mendeleev sometimes adjusted positions. Crucially, he left gaps for elements that had not yet been discovered, and he predicted their properties (for example eka-silicon, later germanium; eka-aluminium, later gallium).",
            "When gallium and germanium were discovered, their properties closely matched Mendeleev’s predictions. That success convinced many scientists that the periodic law was real.",
            "Limitations of Mendeleev’s table: a few pairs of elements appeared in the wrong order if sorted strictly by atomic mass (e.g. tellurium and iodine; argon and potassium) because the true ordering principle had not yet been found. He also did not know about noble gases at first, and isotopes were unknown.",
            "Contrast with Moseley: in 1913 Henry Moseley used X-ray spectra to show that nuclear charge (atomic number $$Z$$) increases by one from element to element. The modern periodic law orders elements by atomic number, which fixes the misplaced pairs and matches electron structure.",
            "Summary: Newlands saw a repeating “every 8th” pattern; Mendeleev built a practical table with gaps and predictions based on atomic mass and properties; Moseley replaced mass with atomic number as the fundamental order.",
        ],
    ),
    (
        "chem10-u1-l1-1",
        "Historical development — from triads to atomic number",
        [
            "Döbereiner’s triads (1829): groups of three similar elements where the middle atomic mass was roughly the average of the other two (e.g. Li, Na, K; Cl, Br, I). This was an early hint of regularity, but only a few triads worked.",
            "Newlands’ octaves: ordered by atomic mass; similarity every eighth element; failed for heavier elements.",
            "Mendeleev: ordered by atomic mass with chemical groups, left gaps, predicted undiscovered elements; most successful 19th-century table.",
            "Modern table (after Moseley): ordered by atomic number; periods and groups reflect electron configuration. Atomic mass still appears on the table, but atomic number decides position.",
        ],
    ),
]


def find_lesson(book: dict, lesson_id: str) -> dict | None:
    for u in book.get("units") or []:
        for L in u.get("lessons") or []:
            if L.get("id") == lesson_id:
                return L
    return None


def find_unit(book: dict, unit_id: str) -> dict | None:
    for u in book.get("units") or []:
        if u.get("id") == unit_id:
            return u
    return None


def inject_handcrafted(book: dict, unit_id: str, cardspecs: list, ids: set[str], prefs: set[str], src: str = "study_notes") -> int:
    unit = find_unit(book, unit_id)
    if not unit:
        return 0
    added = 0
    for lesson_id, title, paras in cardspecs:
        L = find_lesson(book, lesson_id)
        if not L:
            # fallback: first lesson of unit
            L = (unit.get("lessons") or [None])[0]
        if not L:
            continue
        pref = paras[0][:80].strip().lower()
        if pref in prefs:
            continue
        cid = next_tb_id(ids, unit_id)
        card = {
            "id": cid,
            "type": "text",
            "title": title,
            "page": lesson_page(L),
            "src": src,
            "enriched": True,
            "body": paras,
        }
        L.setdefault("cards", []).append(card)
        prefs.add(pref)
        added += 1
    return added


def remove_chem9_geometry_cards(book: dict) -> list[str]:
    """Remove V-bent water, tetra methane, ionic lattice 3D cards (+ paired diagrams)."""
    remove_ids = {
        "chem9-u2-c15",  # water bent 3D
        "chem9-u2-c16",  # paired diagram
        "chem9-u2-c17",  # methane tetra 3D
        "chem9-u2-c18",  # paired diagram
        "chem9-u3-c10",  # NaCl lattice 3D
        "chem9-u3-c11",  # paired diagram
    }
    removed = []
    for u in book.get("units") or []:
        for L in u.get("lessons") or []:
            new_cards = []
            for c in L.get("cards") or []:
                cid = c.get("id")
                title = (c.get("title") or "").lower()
                body = c.get("body")
                if isinstance(body, list):
                    btxt = " ".join(str(x) for x in body).lower()
                else:
                    btxt = str(body or "").lower()
                drop = False
                if cid in remove_ids:
                    drop = True
                elif "3d model" in title and any(k in (title + " " + btxt) for k in ["bent", "tetra", "lattice", "methane", "water (offline)", "nacl"]):
                    drop = True
                if drop:
                    removed.append(cid or title)
                else:
                    new_cards.append(c)
            L["cards"] = new_cards
    # Clean bent/methane geometry lines from shells taster card
    for u in book.get("units") or []:
        for L in u.get("lessons") or []:
            for c in L.get("cards") or []:
                if c.get("id") == "chem9-u2-c06" and isinstance(c.get("body"), list):
                    new_body = []
                    for p in c["body"]:
                        pl = str(p).lower()
                        if "water bent" in pl or "methane not a flat" in pl:
                            continue
                        if "drawing water as" in pl and "straight line" in pl:
                            continue
                        new_body.append(p)
                    c["body"] = new_body
                if c.get("id") == "chem9-u3-c08" and isinstance(c.get("body"), list):
                    # Keep CO2 linear note but remove bent-water contrast
                    c["body"] = [
                        "Carbon dioxide is a linear molecule: O=C=O. Carbon shares two pairs of electrons with each oxygen (double bonds).",
                        "This is a covalent molecular picture — useful when counting atoms in formulas — not an ionic lattice model.",
                    ]
                    c["title"] = "CO₂ bonding picture"
                    c["src"] = "study_notes"
                    c["enriched"] = True
    return removed


def save_book(path: Path, book: dict, indent: int) -> None:
    path.write_text(json.dumps(book, indent=indent, ensure_ascii=False) + "\n")


def main() -> None:
    study = json.loads(STUDY.read_text())
    report = {}

    # ---- Physics 10 all units ----
    path = NOTES / "physics_10.json"
    raw = path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    prefs = existing_body_prefixes(book)
    used_q = used_check_qs(book)
    chapters = load_chapters(study, "Physics", "10")
    stats = {"cards": 0, "checks": 0, "intro": 0, "removed": 0}
    for u in book["units"]:
        ch = chapters.get(int(u["number"]))
        if not ch:
            continue
        expand_unit_from_study(book, u, ch, ids, prefs, used_q, stats)
    save_book(path, book, indent)
    report["physics_10"] = stats

    # ---- Physics 11 all units ----
    path = NOTES / "physics_11.json"
    raw = path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    prefs = existing_body_prefixes(book)
    used_q = used_check_qs(book)
    chapters = load_chapters(study, "Physics", "11")
    stats = {"cards": 0, "checks": 0, "intro": 0, "removed": 0}
    for u in book["units"]:
        ch = chapters.get(int(u["number"]))
        if not ch:
            continue
        expand_unit_from_study(book, u, ch, ids, prefs, used_q, stats)
    save_book(path, book, indent)
    report["physics_11"] = stats

    # ---- Business 10 unit 3 ----
    path = NOTES / "business_economics_10.json"
    raw = path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    prefs = existing_body_prefixes(book)
    used_q = used_check_qs(book)
    chapters = load_chapters(study, "Business and Economics", "10")
    stats = {"cards": 0, "checks": 0, "intro": 0, "removed": 0}
    for u in book["units"]:
        if int(u["number"]) != 3:
            continue
        ch = chapters.get(3)
        if not ch:
            continue
        expand_unit_from_study(book, u, ch, ids, prefs, used_q, stats)
    save_book(path, book, indent)
    report["business_10_u3"] = stats

    # ---- Business 11 unit 2 ----
    path = NOTES / "business_economics_11.json"
    raw = path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    prefs = existing_body_prefixes(book)
    used_q = used_check_qs(book)
    chapters = load_chapters(study, "Business and Economics", "11")
    stats = {"cards": 0, "checks": 0, "intro": 0, "removed": 0}
    for u in book["units"]:
        if int(u["number"]) != 2:
            continue
        ch = chapters.get(2)
        if not ch:
            continue
        expand_unit_from_study(book, u, ch, ids, prefs, used_q, stats)
    save_book(path, book, indent)
    report["business_11_u2"] = stats

    # ---- Chemistry 9 ----
    path = NOTES / "chemistry_9.json"
    raw = path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    prefs = existing_body_prefixes(book)
    used_q = used_check_qs(book)
    chapters = load_chapters(study, "Chemistry", "9")
    stats = {"cards": 0, "checks": 0, "intro": 0, "removed": 0}

    removed = remove_chem9_geometry_cards(book)
    stats["removed"] = len(removed)
    stats["removed_ids"] = removed

    # Expand units 1–3 from study notes first
    for u in book["units"]:
        if int(u["number"]) not in (1, 2, 3):
            continue
        ch = chapters.get(int(u["number"]))
        if not ch:
            continue
        expand_unit_from_study(book, u, ch, ids, prefs, used_q, stats)

    # Inject required detailed cards (may skip if duplicate prefixes)
    stats["cards"] += inject_handcrafted(book, "chem9-u1", CHEM9_U1_CARDS, ids, prefs, src="study_notes")
    stats["cards"] += inject_handcrafted(book, "chem9-u2", CHEM9_U2_CARDS, ids, prefs, src="study_notes")
    stats["cards"] += inject_handcrafted(book, "chem9-u3", CHEM9_U3_CARDS, ids, prefs, src="study_notes")

    save_book(path, book, indent)
    report["chemistry_9"] = stats

    # ---- Chemistry 10 unit 1 ----
    path = NOTES / "chemistry_10.json"
    raw = path.read_text()
    indent = detect_indent(raw)
    book = json.loads(raw)
    ids = collect_ids(book)
    prefs = existing_body_prefixes(book)
    used_q = used_check_qs(book)
    chapters = load_chapters(study, "Chemistry", "10")
    stats = {"cards": 0, "checks": 0, "intro": 0, "removed": 0}
    for u in book["units"]:
        if int(u["number"]) != 1:
            continue
        ch = chapters.get(1)
        if ch:
            expand_unit_from_study(book, u, ch, ids, prefs, used_q, stats)
    stats["cards"] += inject_handcrafted(book, "chem10-u1", CHEM10_U1_CARDS, ids, prefs, src="study_notes")
    save_book(path, book, indent)
    report["chemistry_10_u1"] = stats

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
