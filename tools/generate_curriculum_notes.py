#!/usr/bin/env python3
"""Generate G9–G12 unit notes + illustrated slides + practice into assets/content/."""
from __future__ import annotations
import json
from pathlib import Path

CURRICULUM = {
  "G9": {
    "MATH": [(1,"Set Theory"),(2,"Foundation of Functions"),(3,"Linear Functions"),(4,"Quadratic Functions"),(5,"Exponential and Logarithmic Expressions"),(6,"Right Angled Triangles and Trigonometric Ratios"),(7,"Business Mathematics"),(8,"Polynomials")],
    "PHYSICS": [(1,"Physical Quantities and Measurement"),(2,"Motion in a Straight Line"),(3,"Forces and Newton's Laws"),(4,"Work, Energy and Power"),(5,"Heat and Temperature"),(6,"Light and Optical Instruments"),(7,"Static Electricity"),(8,"Current Electricity")],
    "CHEMISTRY": [(1,"Chemistry: The Study of Matter"),(2,"Atomic Structure"),(3,"Chemical Symbols, Formulas and Equations"),(4,"The Periodic Table"),(5,"Chemical Bonding"),(6,"Acids, Bases and Salts")],
    "BIOLOGY": [(1,"The Cell"),(2,"Cell Division"),(3,"Tissues and Organs"),(4,"Nutrition in Plants and Animals"),(5,"Transport in Plants and Animals"),(6,"Respiration"),(7,"Excretion"),(8,"Coordination and Response")],
    "GEOGRAPHY": [(1,"Introduction to Geography"),(2,"Earth–Sun Relation"),(3,"Maps and Map Reading"),(4,"Concept of Region"),(5,"Weather and Climate"),(6,"Natural Resources of Eritrea")],
    "ENGLISH": [(1,"Parts of Speech Review"),(2,"Tenses and Aspect"),(3,"Sentence Structure"),(4,"Active and Passive Voice"),(5,"Direct and Indirect Speech"),(6,"Paragraph Writing")],
  },
  "G10": {
    "MATH": [(1,"Foundations for Functions"),(2,"Geometric Structure"),(3,"Geometric Patterns"),(4,"Dimensionality and Geometry of Location"),(5,"Congruency and the Geometry of Size"),(6,"Similarity"),(7,"Circle Geometry"),(8,"Trigonometry of Oblique Triangles")],
    "PHYSICS": [(1,"Vectors"),(2,"Motion in Two Dimensions"),(3,"Momentum and Collisions"),(4,"Circular Motion"),(5,"Gravitation"),(6,"Waves and Sound"),(7,"Electromagnetic Induction"),(8,"Modern Physics Introduction")],
    "CHEMISTRY": [(1,"Stoichiometry"),(2,"Chemical Bonding and Forces of Attraction"),(3,"States of Matter"),(4,"Acids, Bases and Salts"),(5,"Oxidation–Reduction"),(6,"Organic Chemistry Basics")],
    "BIOLOGY": [(1,"Food and Digestion"),(2,"Breathing and Gas Exchange"),(3,"Blood and Circulation"),(4,"Immunity"),(5,"Reproduction"),(6,"Genetics Introduction"),(7,"Ecology Basics")],
    "GEOGRAPHY": [(1,"Population Geography"),(2,"Settlement"),(3,"Economic Activities"),(4,"Concept of Development"),(5,"Eritrea: Location and Physical Features"),(6,"Natural Vegetation and Soils")],
    "BUSINESS_ECONOMICS": [(1,"Basic Economics Concepts"),(2,"Demand and Supply"),(3,"Bookkeeping for a Service Business"),(4,"Business Organization"),(5,"Money and Banking")],
    "ENGLISH": [(1,"Complex Sentences"),(2,"Conditionals"),(3,"Modals"),(4,"Essay Structure"),(5,"Summary Writing"),(6,"Reading Comprehension Strategies")],
  },
  "G11": {
    "MATH": [(1,"Relations and Functions"),(2,"Square Root Functions"),(3,"Rational Functions"),(4,"Exponential and Logarithmic Functions"),(5,"Trigonometric Functions"),(6,"Sequences and Series Introduction"),(7,"Statistics"),(8,"Probability")],
    "PHYSICS": [(1,"Kinematics Review"),(2,"Dynamics"),(3,"Rotational Motion"),(4,"Simple Harmonic Motion"),(5,"Fluid Mechanics"),(6,"Thermodynamics"),(7,"Electrostatics"),(8,"Electric Circuits")],
    "CHEMISTRY": [(1,"Chemical Equilibrium"),(2,"Chemical Kinetics"),(3,"Chemistry of Nonmetals"),(4,"Chemistry of Metals"),(5,"Behavior of Gases"),(6,"Thermochemistry")],
    "BIOLOGY": [(1,"Endocrine System"),(2,"Nervous System"),(3,"Homeostasis"),(4,"Plant Physiology"),(5,"Microbiology"),(6,"Biotechnology Introduction")],
    "GEOGRAPHY": [(1,"Tectonic Forces"),(2,"Gradation by Rivers and Winds"),(3,"Gradation by the Action of Waves"),(4,"Human Settlement"),(5,"Cultural Impact on the Natural Environment"),(6,"Geographic Position, Shape and Size of Eritrea"),(7,"Relief and Drainage Systems in Eritrea"),(8,"Map Work – Landforms on Contour Maps")],
    "BUSINESS_ECONOMICS": [(1,"National Income"),(2,"Fiscal and Monetary Policy"),(3,"International Trade"),(4,"Accounting for Merchandising"),(5,"Entrepreneurship")],
    "ENGLISH": [(1,"Advanced Grammar Review"),(2,"Argumentative Writing"),(3,"Literary Devices"),(4,"Report Writing"),(5,"Oral Communication Skills")],
  },
  "G12": {
    "MATH": [(1,"Sequence and Series"),(2,"Limits and Continuity"),(3,"Differentiation"),(4,"Applications of Derivatives"),(5,"Integration"),(6,"Applications of Integration"),(7,"Vectors in Space"),(8,"Probability Distributions")],
    "PHYSICS": [(1,"Electric Fields and Potential"),(2,"Capacitance"),(3,"Magnetic Fields"),(4,"Electromagnetic Waves"),(5,"Wave Optics"),(6,"Atomic Models"),(7,"Nuclear Physics"),(8,"Semiconductor Basics")],
    "CHEMISTRY": [(1,"Atomic Structure Advanced"),(2,"Periodic Properties"),(3,"Chemical Bonding Advanced"),(4,"Electrochemistry"),(5,"Organic Functional Groups"),(6,"Polymers and Biomolecules")],
    "BIOLOGY": [(1,"Molecular Genetics"),(2,"Evolution"),(3,"Human Health and Disease"),(4,"Ecology and Conservation"),(5,"Reproduction and Development"),(6,"Biotechnology Applications")],
    "GEOGRAPHY": [(1,"World Climate Systems"),(2,"Natural Hazards"),(3,"Resources and Sustainable Development"),(4,"Eritrea: Economy and Society"),(5,"Regional Geography of Africa"),(6,"Geographic Information and Fieldwork")],
    "BUSINESS_ECONOMICS": [(1,"Market Structures"),(2,"Business Finance"),(3,"Marketing Principles"),(4,"Business Law Basics"),(5,"Development Economics")],
    "ENGLISH": [(1,"Grammar for Academic Writing"),(2,"Critical Reading"),(3,"Research Skills"),(4,"Presentation Skills"),(5,"Exam Writing Strategies")],
  },
}

def note_for(grade, subject, num, title):
    subj = subject.lower().replace('_', ' ')
    is_math = subject == "MATH"
    is_eng = subject == "ENGLISH"
    terms = [w.lower() for w in title.replace('–', ' ').replace('-', ' ').split() if len(w) > 3][:6] or [title.lower()]
    sections = [
        {"heading": "Overview", "explanation": f"This unit covers {title} in {grade} {subj}. Students learn core definitions, relationships, and methods from the Eritrean national curriculum. Mastery supports later units and matric preparation."},
        {"heading": "Key ideas", "explanation": f"1) Define terms for {title}. 2) State governing rules/principles. 3) Apply to worked examples. 4) Solve practice problems. 5) Connect to related units."},
        {"heading": "Study method", "explanation": "Read summary and key terms. Attempt examples before viewing solutions. Timed practice. Rewrite methods for weak items."},
    ]
    if is_math:
        examples = [
            {"id": f"{grade}_{subject}_U{num}_EX1", "prompt": f"State the main definition in {title} and give one numerical illustration.", "solution": "Identify knowns → choose formula/rule → substitute → simplify → state answer with units if needed."},
            {"id": f"{grade}_{subject}_U{num}_EX2", "prompt": f"Solve an exam-style problem on {title}.", "solution": "Translate to symbols, apply the unit rule, verify domain and edge cases."},
            {"id": f"{grade}_{subject}_U{num}_EX3", "prompt": f"Compare two cases under {title}.", "solution": "Select the matching theorem for each case, compute, interpret the difference."},
        ]
        exercises = [
            {"id": f"{grade}_{subject}_U{num}_Q1", "type": "mcq", "prompt": f"Which statement best matches {title}?", "answer": "The correct curriculum definition", "explanation": "Reject distractors that misuse related ideas."},
            {"id": f"{grade}_{subject}_U{num}_Q2", "type": "practice", "prompt": f"Solve a standard problem on {title} with full steps.", "answer": "Full worked solution", "explanation": "Knowns, formula, substitution, simplification, final answer."},
            {"id": f"{grade}_{subject}_U{num}_Q3", "type": "practice", "prompt": f"Write and solve one similar problem on {title}.", "answer": "Original problem + solution", "explanation": "Changing numbers tests real understanding."},
            {"id": f"{grade}_{subject}_U{num}_Q4", "type": "practice", "prompt": f"Name a common mistake in {title} and how to avoid it.", "answer": "Mistake + fix", "explanation": "Wrong formula, domain errors, sign errors, unit mix-ups."},
        ]
    elif is_eng:
        examples = [
            {"id": f"{grade}_{subject}_U{num}_EX1", "prompt": f"Correct a sentence focusing on {title}.", "solution": "Show error → state rule → corrected sentence."},
            {"id": f"{grade}_{subject}_U{num}_EX2", "prompt": f"Write two sentences using structures from {title}.", "solution": "Each sentence clearly shows the target structure."},
        ]
        exercises = [
            {"id": f"{grade}_{subject}_U{num}_Q1", "type": "practice", "prompt": f"Rewrite five sentences applying {title}.", "answer": "Five correct rewrites", "explanation": "Mark changes and name the rule."},
            {"id": f"{grade}_{subject}_U{num}_Q2", "type": "practice", "prompt": f"Explain {title} with examples (4–6 sentences).", "answer": "Clear paragraph", "explanation": "Definition → rule → example → common error."},
            {"id": f"{grade}_{subject}_U{num}_Q3", "type": "mcq", "prompt": f"Which sentence correctly applies {title}?", "answer": "Grammatically correct option", "explanation": "Eliminate agreement/tense/clause errors."},
        ]
    else:
        examples = [
            {"id": f"{grade}_{subject}_U{num}_EX1", "prompt": f"Explain {title} with a real-world or lab example.", "solution": "Define → example → link to principle."},
            {"id": f"{grade}_{subject}_U{num}_EX2", "prompt": f"Compare two related ideas in {title}.", "solution": "Features, conditions, outcomes for each idea."},
        ]
        exercises = [
            {"id": f"{grade}_{subject}_U{num}_Q1", "type": "practice", "prompt": f"Define three key terms from {title}.", "answer": "Three accurate definitions", "explanation": "Use precise curriculum wording."},
            {"id": f"{grade}_{subject}_U{num}_Q2", "type": "practice", "prompt": f"Answer a structured model-exam style question on {title}.", "answer": "Labeled points response", "explanation": "Use (a)(b)(c) where useful."},
            {"id": f"{grade}_{subject}_U{num}_Q3", "type": "mcq", "prompt": f"Which statement about {title} is correct?", "answer": "Scientifically accurate statement", "explanation": "Reject absolute claims and mixed cause/effect."},
        ]
    return {
        "grade": grade, "subject": subject, "unit_number": num, "title": title,
        "summary": f"{title}: core {grade} {subj} unit — definitions, relationships, worked examples, and practice for the national curriculum.",
        "key_terms": terms,
        "key_ideas": [
            f"{title} is a core {grade} {subj} syllabus unit.",
            "Learn definitions and methods before exam drills.",
            "Practice varied problems and check every answer.",
            "Link to related earlier and later units.",
        ],
        "sections": sections, "examples": examples, "exercises": exercises,
    }

def slides_for(grade, subject, num, title):
    key = f"{grade}|{subject}|{num}"
    bodies = [
        ("Title", f"{grade} {subject.replace('_',' ').title()} — Unit {num}: {title}"),
        ("Goals", f"Explain and apply {title}."),
        ("Key terms", " · ".join([w for w in title.replace('–',' ').split() if len(w)>2][:8]) or title),
        ("Core idea", f"Build from definitions and standard methods for {title}."),
        ("Worked method", "Knowns → rule → substitute → simplify → check."),
        ("Mistakes", f"Avoid wrong formulas and skipped verification in {title}."),
        ("Practice", f"Do 5+ problems on {title}; review errors same day."),
        ("Exams", f"Model/matric items often test {title} in multi-step form."),
    ]
    return key, [{"index": i, "title": t, "body": b, "image": None} for i,(t,b) in enumerate(bodies)]

def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "assets" / "content"
    out.mkdir(parents=True, exist_ok=True)
    notes, slides, practice = [], {}, []
    for grade, subjects in CURRICULUM.items():
        for subject, units in subjects.items():
            for num, title in units:
                n = note_for(grade, subject, num, title)
                notes.append(n)
                k, s = slides_for(grade, subject, num, title)
                slides[k] = s
                for i, ex in enumerate(n["exercises"]):
                    if ex.get("type") == "mcq" or i == 0:
                        practice.append({
                            "id": ex["id"], "grade": grade, "subject": subject, "unit_number": num,
                            "prompt": ex["prompt"],
                            "options": [ex.get("answer") or "Option A", "Common misconception", "Unrelated idea", "Incomplete statement"],
                            "correct_index": 0, "explanation": ex.get("explanation") or "",
                        })
    notes.sort(key=lambda n: (n["grade"], n["subject"], n["unit_number"]))
    (out / "unit_notes.json").write_text(json.dumps(notes, ensure_ascii=False), encoding="utf-8")
    for g in ["G9", "G10", "G11", "G12"]:
        subset = [n for n in notes if n["grade"] == g]
        (out / f"unit_notes_{g.lower()}.json").write_text(json.dumps(subset, ensure_ascii=False), encoding="utf-8")
    (out / "illustrated_slides.json").write_text(json.dumps(slides, ensure_ascii=False), encoding="utf-8")
    (out / "practice_from_notes.json").write_text(json.dumps(practice, ensure_ascii=False), encoding="utf-8")
    (out / "practice_index.json").write_text(json.dumps({
        "files": ["practice_from_notes.json", "practice_questions.json", "practice_lite.json"],
        "lite": "practice_lite.json",
    }), encoding="utf-8")
    inv = {
        "notes": len(notes), "unit_notes_count": len(notes),
        "illustrated_slide_decks": len(slides), "practice_from_notes_mcq": len(practice),
        "notes_version": "v3_systematic_g9_g12_generator",
        "grades": ["G9", "G10", "G11", "G12"],
        "note": "Generated at build time from tools/generate_curriculum_notes.py — full G9–G12 unit map.",
    }
    (out / "content_inventory.json").write_text(json.dumps(inv, indent=2), encoding="utf-8")
    print(f"Generated {len(notes)} notes, {len(slides)} slide decks, {len(practice)} practice → {out}")

if __name__ == "__main__":
    main()
