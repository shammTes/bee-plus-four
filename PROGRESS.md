# High / bee-plus-four — progress (`fix/high-drive-english-perf`)

Updated: 2026-10-05 ~14:00 (Africa/Asmera, UTC+3)

Follow-up to merged PR #1 (`fix/high-qr-content-sync`).

## 1. Drive sync (matric / model / notes)

Source: https://drive.google.com/drive/folders/1k0yjHIKkeIlE_7QMhs5ph1XOF9FDGgjV  
Downloaded via public `uc?export=download` (MCP `user-Google-drive` DownloadFile still unsigned-in).

**In app:**
- `assets/high/exercises/drive_chapters/chem_g10_c1.json`, `history_g10_c1.json`
- `assets/high/exercises/drive_meta/Matric_Questions_index.json`, `Practice_Questions.json`
- `assets/high/exams/drive_matric_index.json` (same matric index)
- MC items from chapter packs + Practice bank merged into exercise JSON / `exercises/index.json`
  - chem10 +1 drive MC; history10 chapter MC; practice → agri/bio banks (+20)
- Tooling: `tool/drive_sync/convert_chapter.py`, README

**Left:** Full 20 MB `Matric_Questions.json` not bundled (size). Study_Notes_markdown bulk (173 chapters) not yet converted into notes JSON — English G11 used 8 key chapters. Need signed Drive connector for private/large blobs if export URLs change.

## 2. English Grade 11

Textbook PDF `1D5r-Nl3_…` still image-scanned (MCP extract fails).  
**Rebuilt** `assets/high/notes/notes/english_11.json` from Drive Study Notes markdown:

`Study_Notes_markdown/English/Grade_11-12/` Ch01, Ch05, Ch08–11, Ch14, Ch20  
→ 8 units, **80** practice questions (S-V-O, agreement, modals, passive, reported speech, conditionals/wish, gerunds, cohesion).  
Sources cached under `tool/english/study_notes_md/`. Index + `english_index.json` updated.

## 3. Enrich thin notes

Added study-step cards, multi-step `why`, and match games where missing for:  
`business_economics_11/12`, `physics_12`, `agriculture_11`, `chemistry_12`.  
**History teacher text not rewritten.**

## 4. Matric UI

- Model answer accordion **opens by default**
- Acc `clipBehavior: Clip.none` (from prior PR) kept
- Long stems: scroll + “Show full question”

## 5. Performance

- Exam JSON batches decode in **Isolate** when `useIsolate: true` (default in `High.init`)
- `ScreenList` `cacheExtent` reduced (~0.35× height)
- `Deco.litePuffyShadows` + `card(lite: …)` for lighter list paint
- Figure `Image.asset` uses `cacheWidth` / low–medium filter quality
- `_HighScreenState.dispose` stops study ticker + disposes notes `AppState`

## Build APK

```bash
git fetch origin && git checkout fix/high-drive-english-perf
flutter pub get && flutter analyze && flutter test
flutter build apk --release
# build/app/outputs/flutter-apk/app-release.apk
```

## Push / PR

Branch pushed to **fork** `stesfalem06-crypto/bee-plus-four`; PR opened into `shammTes/bee-plus-four`.
