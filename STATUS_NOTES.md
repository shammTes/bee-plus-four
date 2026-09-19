# Unit notes status (v2 polished + MCQ)

## Content
- **133 units** from 29 official MoE textbooks (Drive folder)
- **unit_notes_rich.json** (~3.3MB): sections, examples, exercises
- **unit_notes.json**: flat list for UI
- **practice_from_notes.json**: **1412 scored MCQs** derived from unit terms/exercises

## App wiring
- `UnitNote` model includes sections / examples / exercises / keyIdeas
- `ContentRepository.notes()` prefers `unit_notes_rich.json`
- Notes detail: expandable examples + **UnitExerciseSession**
- Practice screen CTA: **Textbook unit exercises**
- `practice_index.json` loads `practice_from_notes.json` first for scored MCQ practice

## Drive assets (public folder)
Folder: https://drive.google.com/drive/folders/1Qy4TuxVMvlMurxQkdaFa-P-HJOqZFZm3

| File | Link |
|------|------|
| unit_notes_rich.json | https://drive.google.com/file/d/1gv_l5Vay2WWt-NybgA8bb3DwPseMAu0q/view |
| unit_notes_flat_v2.json | https://drive.google.com/file/d/1-lrX7DJp7vMjtEac74F9lJ-bWkKFQA_9/view |
| practice_from_notes.json | https://drive.google.com/file/d/1Le6xHfpnvpRJ7oGiF70_SFzTkIWTJZSY/view |
| notes_ALL_BOOKS_v2_polished.json | https://drive.google.com/file/d/1BPqrDcoC63zyQ1A16VKGtIssBKT1Tcqf/view |

## CI note
Large JSON packs should be downloaded in the workflow into `assets/content/` (or included in the content tarball). Local monorepo already has them under `assets/content/`.

## Polish
- Second pass on 13 thin units: all now have ≥4 key terms
- History G11 unit boundaries fixed
- MCQ distractors built from unit key terms
