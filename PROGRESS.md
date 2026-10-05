# High / bee-plus-four — progress (fix/high-qr-content-sync)

Updated: 2026-10-05 afternoon (Africa/Asmera, UTC+3)

## QR camera — root cause + fix

**Package:** `mobile_scanner: ^6.0.2` (+ `qr_flutter`). Unlock gate kept.

**Flow:**
- `lib/main.dart` → `UnlockStore` → if locked, `LockScreen`
- Device shows its ID QR; Bee Seller returns a signed payload (`lib/licensing/qr_payload.dart` / `unlock_store.dart`)
- “Scan seller QR” opens the camera

**Why camera failed on first install (Android):**
1. `LockScreen` mounted bare `MobileScanner()` with **no runtime permission request** and **no `MobileScannerController` lifecycle**.
2. Native Android already had a working path — `MainActivity` MethodChannel `com.warsay.high/secure` with `requestCamera` + Google Play Services **Code Scanner** (`scanQr`) — but **Flutter never called it**.
3. Manifest already had `CAMERA` + `uses-feature`; `minSdk 23` is fine. No iOS target in this repo.

**Fix (Android-primary):**
- `lib/licensing/lock_screen.dart`: request camera via MethodChannel (rationale message first); prefer native `scanQr`; on failure fall back to embedded `MobileScanner` with controller `autoStart: false`, **start after the widget mounts**, stop/dispose on leave / unlock.
- If permission denied: message + **Open Settings** button (`openAppSettings` on the channel).
- `android/.../MainActivity.kt`: added `hasCamera` + `openAppSettings`; kept `requestCamera` / `scanQr`.

Unlock gate is unchanged (still requires a valid Bee Seller code).

## Content sync

### History 9–11 (teacher zip)
- JSON bytes already matched `/workspace/High-history-teacher-update.zip` (left `history_12` alone).
- Replaced `assets/high/media/placements.json` from the zip (39 KB → 325 KB).
- Merged history unit metadata into `notes/index.json` and history keys into `unit_questions.json`.
- Copied `tool/history/` converters.

### English grammar
- Merged zip books: `english_9/10/12.json` (full grammar units).
- Generated **`english_11.json`** (8 units, 64 practice questions) via `tool/english/eng11.py` — Drive textbook `1D5r-Nl3_…` is a **scanned PDF** (MCP text extract failed; `user-Google-drive` DownloadFile not signed in). Regenerate from OCR when available.
- Registered English in `notes/index.json` + `english_index.json` for grades 9–12; `english` already in `kNotesSubjects` / Exercise tab (notes books drive the subject chips).
- `unit_questions.json` gained eng9/10/11/12 mappings from zip + eng11 build.

### Matric / Drive (started)
- Listed folder `1k0yjHIKkeIlE_7QMhs5ph1XOF9FDGgjV`: chapter packs (`chem_g10_c1`, `history_g10_c1`), Matric/Practice/Study_Notes blobs, `Study_Notes_markdown/` (173 chapters).
- Added `tool/drive_sync/` converter + README. Full binary sync needs Drive download auth; text chapters readable via MCP.
- **UI fix:** long stems can scroll + “Show full question”; Accordion `clipBehavior: Clip.none` so explanations/model answers are not clipped.

### Performance (started)
- Reduced clay `puffyShadows` blur/spread in `lib/high/theme/deco.dart` (list cards cheaper to paint).
- Fig thumbnails use `cacheWidth` / low filter quality.
- Scanner controller disposed on close/unlock.

### Enrich notes
- Not bulk-rewritten. History teacher text untouched. English G11 is new grammar notes with steps in `why`. Further enrichment / open images later.

## Files changed (high level)
- `lib/licensing/lock_screen.dart`
- `android/app/src/main/kotlin/com/warsay/high/MainActivity.kt`
- `lib/high/exam/cards.dart`, `lib/high/theme/deco.dart`
- `assets/high/notes/notes/english_{9,10,11,12}.json`, `index.json`, `english_index.json`
- `assets/high/notes/unit_questions.json`, `assets/high/media/placements.json`
- `tool/english/*`, `tool/history/*`, `tool/drive_sync/*`
- `PROGRESS.md`

## Done vs left

| Item | Status |
|------|--------|
| QR camera first-install Android | Done (needs device QA) |
| History 9–11 teacher sync | Done (JSON already current; placements/index/uq refreshed) |
| English 9/10/12 zip merge | Done |
| English 11 from textbook PDF | Provisional (curriculum-faithful generator; OCR pass left) |
| English in Exercise nav | Done via notes index |
| Drive matric/notes full ingest | Started (inventory + converter); bulk left |
| Matric answer overflow | Stem/Acc fix done; more QA left |
| Perf pass | Quick wins only |
| Push to GitHub | **Blocked** — `stesfalem06-crypto` has pull-only on `shammTes/bee-plus-four` |

## Build APK (on a machine with Flutter)

```bash
cd /workspace/bee-plus-four   # or your clone
git checkout fix/high-qr-content-sync
flutter pub get
flutter analyze
flutter test
flutter build apk --release
# APK: build/app/outputs/flutter-apk/app-release.apk
# applicationId: com.four.student
```

To get push access: owner must add write permission for `stesfalem06-crypto`, or open a PR from a fork.

## Branch
`fix/high-qr-content-sync` — committed locally only.
