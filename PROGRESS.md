# High / bee-plus-four — progress (`fix/high-matric-notes-more`)

Updated: 2026-10-05 ~14:20 (Africa/Asmera, UTC+3)

Follow-up to merged PR #2. Branch targets PR #3.

## 1. Matric_Questions.json — size tradeoff

| Approach | Size | Status |
|---|---|---|
| Ship full Drive JSON | ~20 MB | **Not shipped** (APK bloat) |
| Existing eager exams | ~24 MB | Unchanged |
| Missing papers → eager banks | ~0.4 MB | **Shipped** (English Language 2017/18/20/23/24 + Algebra 2023) |
| Slim 2024+ by subject (lazy) | ~2.2 MB source | **Shipped** under `assets/high/exams/matric_lazy/` |

- Catalog: `assets/high/exams/matric_lazy/catalog.json`
- Loader: `ExamRepo.ensureLazySubject` (isolate decode); kicked from `ExamSubjectPage` on open
- Docs: `tool/matric_lazy/README.md`

## 2. Study Notes → notes JSON

- Enriched geo/physics/chem/bio/math/agri (18 books) with worked / check / table / match from Drive `Study_Notes.json` (History **not** rewritten)
- English 11: +8 grammar units (u9–u16) from Drive chapters 2–4,6–7,12–13,15
- Chemistry 9: added unit 4 (lab / cumulative review)

## 3. Enrich / images

- Step-by-step + games on remaining thin science/geo units (above)
- No new raster images this round (existing Commons assets + `credits.json` unchanged)

## 4. Perf

- Unit notes: `SliverList` + `cacheExtent` ~0.4× height; `addAutomaticKeepAlives: false`
- `MediaLib` credits load deferred until first notes book open
- Matric subject packs lazy (not in startup exam batch)

## Build APK

```bash
git fetch origin && git checkout fix/high-matric-notes-more
flutter pub get && flutter analyze && flutter test
flutter build apk --release
```

## Left

- Pre-2024 Drive papers still only via existing eager banks (not dual-shipped as lazy)
- Remaining English Study Notes chapters 16–24
- True per-card lazy build inside unit notes (widgets still assembled before SliverList)
- Optional Commons diagrams for thin units + credits.json entries
- Full Matric CSV / OCR textbook when `user-Google-drive` signed in
