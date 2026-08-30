# 4 — Highschool offline curriculum + controlled study coach

Flutter. Same security as BEE PLUS. **No Junior track** (G9–G12 only).

## Ingested content (from subject ZIP packs)

| Metric | Count |
|--------|------:|
| Unit notes | **108** |
| Practice MCQs | **9,585** |
| Grades | G9, G10, G11 |
| Subjects | Math, Physics, Chemistry, Biology, English, Geography, History, Agriculture, Business/Economics |

### Full content archive
Google Drive: [bee_plus_four_content_full.tar.gz](https://drive.google.com/file/d/1wgefeor1ZdSNPtjhos9_Z_H-3fq9OAe-/view?usp=drivesdk)

Extract into `assets/content/` then `flutter pub get && flutter build apk`.

Loader reads `practice_index.json` → all `practice_g*_*.json` packs, with `practice_lite.json` fallback.

## Offline Coach bot
Intent keywords only (no network LLM). Answers from practice packs.

## Unlock
HMAC QR, device-bound, single-use. Package: `HIGHSCHOOL`.

## CI
Artifact: `four-release-apk`
