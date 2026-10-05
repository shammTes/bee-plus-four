# High / bee-plus-four — progress (`fix/high-more-english-matric-enrich`)

Updated: 2026-10-05 ~16:15 (Africa/Asmera, UTC+3)

Follow-up to merged PR #3. Branch targets PR #4.

## Sync
- Branched from upstream `main` after PR #2/#3 merges (`94bb196`).

## 1. Lazy Matric — more pre-2024 (APK lean)

| Pack | Years | Source size |
|---|---|---|
| Prior (PR #3) | 2024+ | ~2.2 MB |
| **This PR** | **2020+** | **~4.8 MB** across 12 subject files |

- Still **not** shipping full Drive JSON (~20 MB) or pre-2020 Drive duplicates (eager banks cover those).
- Same loader: `ExamRepo.ensureLazySubject` on Matric subject open; exam-id dedupe.
- Docs: `tool/matric_lazy/README.md`, `matric_lazy/catalog.json` (`min_lazy_year: 2020`).

## 2. English Study Notes ch.16–24

- Added eng11 units **u17–u24** (phrasals, prepositions, collocations, synonyms, conversation, pronunciation, reading, L1 mistakes).
- Ch.20 (cohesion) already present as unit 8 — skipped duplicate.
- Each unit: grammar/text cards, worked + check, match game, **10 MCQs with answers/explanations**.

## 3. Enrich

- More steps/tables/games: math 11–12, BE 10–12, physics 12, chem 12, english 9/10/12.
- **History teacher text unchanged.**
- No new Commons rasters this round (`credits.json` unchanged).

## 4. Per-card lazy notes

- Unit page `_contentBuilders` returns `List<Widget Function()>`.
- Each lesson head / note card / quiz item is its own SliverList entry; widgets build when the list asks (`items[i]()`).
- `addAutomaticKeepAlives: false` retained.

## Build

```bash
git fetch origin && git checkout fix/high-more-english-matric-enrich
flutter pub get && flutter analyze && flutter test
flutter build apk --release
```

## Left
- Pre-2020 Drive-only papers (if any gaps vs eager banks)
- English thematic G12 textbook units (still topic books, not grammar ch.16–24)
- Optional Commons diagrams + credits.json
- Further APK trim (gzip already helps; could drop workout stems from lazy packs)
