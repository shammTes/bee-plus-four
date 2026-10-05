# High / bee-plus-four — progress (`fix/high-continue-10`)

Updated: 2026-10-05 ~17:00 (Africa/Asmera, UTC+3)

## QR (user testing)
Upstream main includes PR #9 (embedded MobileScanner only). User is testing on device.

## This branch
### Thin-unit enrich (History untouched)
- Tool: `tool/enrich/from_study_notes.py` — maps Study_Notes review MCQs → `check` + `worked` cards on lessons missing both.
- Skips History and English (English has its own pipeline).
- Cap ~24 new checks/book; touched STEM + Agriculture + Business & Economics across grades 9–12.

### Commons diagrams + credits
| id | lesson | notes |
|---|---|---|
| `geo_rockcycle` | geo9-u5-l5-1 | Rock cycle (PNG → webp) |
| `chem_phscale` | chem10-u4-l4-1 | pH scale |
| `bio_nitrogen` | bio12-u3-l3-1 | Nitrogen cycle |
| `math_venn` | math9-u1-l1-1 | Three-set Venn |

Placements in `assets/high/media/commons_extra.json`; attribution in `credits.json`.

## Verify
```bash
# History must be unchanged
git diff -- assets/high/notes/notes/history_*.json
adb logcat -s HighSecure   # QR testing (separate)
```
