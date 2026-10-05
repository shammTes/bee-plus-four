# High / bee-plus-four — progress (`fix/high-continue-7`)

Updated: 2026-10-05 ~16:40 (Africa/Asmera, UTC+3)

Branched from upstream main after PR #6 merge.

## 1. Thin-unit enrichment
More worked / check / table / match for:
BE 10–12, math 10–12, physics 9/11/12, chem 11–12, agri 12, bio 12, geo 11.
Fixed MC answer parsing for `C. Kelvin`-style and math `Multiple Choice` full-text answers.
**History teacher text unchanged.**

## 2. Commons diagrams (+ credits.json)
New webps + credits + `commons_extra.json` placements:
- `math_parabola` (PD) → math9 quadratic
- `bio_mitosis_stages` (PD) → bio9 cell
- `phy_lens_ray` (CC BY-SA 3.0) → phys10 optics

(Rock-cycle download hit Commons rate-limit / missing file; skipped.)

## 3. Matric lazy
Expanded `min_lazy_year` **2017 → 2014** so **all 136 Drive papers** are in subject lazy packs (~8.4 MB source). Eager banks still load at startup; lazy packs merge on subject open with exam-id dedupe. Raw 20 MB JSON still not shipped.

## Build
```bash
git fetch origin && git checkout fix/high-continue-7
flutter pub get && flutter analyze
flutter build apk --release
```

## Left
- More geo Commons (rock cycle) when API allows
- Device QA QR unlock on release APK
