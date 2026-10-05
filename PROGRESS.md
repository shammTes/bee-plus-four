# High / bee-plus-four — progress (`fix/high-enrich-images-more`)

Updated: 2026-10-05 ~16:30 (Africa/Asmera, UTC+3)

Branched from upstream main after PR #5 (QR camera) merge.

## 1. Thin-unit enrichment
Added more worked / check / table / match from Drive Study Notes for:
physics 9–10, mathematics 9–10, chemistry 9, biology 9, geography 9–10, agriculture 11.
**History teacher text unchanged.**

## 2. Wikimedia Commons diagrams (+ credits.json)
New webp assets under `assets/high/media/img/` with credits:

| id | topic | licence |
|---|---|---|
| math_pythagoras | Pythagorean theorem | Public domain |
| math_cartesian | Coordinate plane | Public domain |
| phy_circuit | Series circuit | CC BY-SA (Commons metadata) |
| phy_spectrum | EM spectrum | Public domain |
| chem_bohr | Bohr atom model | Public domain |
| bio_leaf_xsec | Leaf anatomy | CC BY-SA 3.0 |

Placements: `assets/high/media/commons_extra.json` (loaded by NotesRepo with other placement packs).

## 3. Matric lazy gaps
Expanded `matric_lazy` from **2020+** to **2017+** (~6.8 MB source across 12 subjects, 110 papers).
Pre-2017 still eager-bank only (keeps APK lean; full Drive JSON still not shipped).
Loader comment + `tool/matric_lazy` docs updated (`min_lazy_year: 2017`).

## Build
```bash
git fetch origin && git checkout fix/high-enrich-images-more
flutter pub get && flutter analyze
flutter build apk --release
```

## Left
- Pre-2017 Drive-only papers (if any gaps vs eager)
- More Commons diagrams (geo/math as needed)
- Device QA of QR PR #5 on release APK
