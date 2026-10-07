# Encrypted add-on resources — Stage 1 (PDFs)

Plan: `docs/encrypted_resources_plan.md`. Stage 1 = format + Mac/CLI encryptor + Android import + PDF viewer.
Videos (Stage 2) and reels (Stage 3) reuse the same format; their files import and list already but open with "next update".

## Pieces
| Path | What |
|---|---|
| `packages/four_format/` | pure-Dart format: writer, reader (chunk seek), keys, CLI `four_encrypt`, unit tests |
| `lib/resources/gate.dart` | who may decrypt: locked / legacy / strong |
| `lib/resources/library.dart` | SAF refresh → app-private copy → sealed index |
| `lib/resources/resources_ui.dart` | Home card, Resources page, unit-page strip, lock → unlock screen |
| `lib/resources/pdf_page.dart` | pdfrx (PDFium) viewer, decrypt to memory only, FLAG_SECURE |
| `android/.../ResourcesChannel.kt` | folder picker (persisted permission), listing by magic bytes, streaming copy, FLAG_SECURE |
| `tools/four_encryptor/` | Flutter macOS/Windows encryptor app |

## File format v1 (big-endian)
```
"4RES" | ver=1 | flags (bit0 thumb) | mkVersion | reserved=0
fileId[16] | batchIdLen u8 | batchId utf8 (≤64)
wrappedBatchKey[60]   = AES-GCM(MK,  BK, aad "4RES-BK|batchId")   (nonce12|ct32|tag16)
wrappedContentKey[60] = AES-GCM(BK,  CK, aad fileId)
noncePrefix[8] | chunkSize u32 | chunkCount u32 | plainSize u64 | headerLen u32 | thumbLen u32
header = AES-GCM(CK, JSON meta, aad preamble|'H')     meta: title, subject, grade, unit, type, mime, pages?, durationMs?, createdAt
thumb  = AES-GCM(CK, JPEG,      aad preamble|'T')     (optional)
chunk i = AES-GCM(CK, nonce prefix|u32 i, aad fileId|u32 i|u8 isLast) → ct + tag16   (256 KiB default)
footer = "4END" | HMAC-SHA256(HKDF(CK,"4RES-footer-v1"), preamble | tag_0 … tag_n-1)
```
- Seek: chunk = offset / chunkSize, file offset = dataStart + i·(chunkSize+16) → one chunk decrypted per seek.
- Tamper/reorder/truncation: preamble is header AAD; chunk index + last flag in AAD; exact total length checked; footer on import.
- Detected by the 4 magic bytes, not the extension (SHAREit may rename).

## Keys and unlock
- MK: `--dart-define=FOUR_MK=<base64>` in release builds; without it the public **DEV key** is used (testing only!).
- Phones unlocked with **old codes** (no proof stored) → **legacy**: MK-only, allowed (weaker).
- A **fresh unlock** stores `HMAC(signingKey, "RES|BEE1|deviceId|nonce")` in Keystore-backed secure storage → **strong**:
  it is re-verified against this phone's id each launch and mixed into the device key that seals the local index.
- Honest limit: offline protection only. MK is inside the APK; root + reverse engineering can extract it, and the
  HMAC signing key in `qr_payload.dart` has an in-source default. Rotate both before relying on this (the seller key too).

## Try it
1. Make a test file (any OS with Flutter/Dart):
   ```
   cd packages/four_format && dart pub get
   dart run four_format:four_encrypt encrypt ~/notes.pdf --title "Cell biology" --subject biology --grade 11 --unit 1
   dart run four_format:four_encrypt info ~/notes.4pdf      # prints metadata, "integrity: OK"
   ```
   (Mac GUI: `tools/four_encryptor`, see its README.) Subject+grade must match a notes book id (`biology_11`) and unit = unit number, for the unit-page strip.
2. Build/install 4 (debug or release without FOUR_MK so it uses the DEV key) and unlock it.
3. Copy `notes.4pdf` to the phone (e.g. `Download/4`). Home → **Extra resources** → Choose folder → Refresh.
4. Tap the file → PDF opens (screenshots blocked). It also shows on Notes → Biology 11 → Unit 1 under "Extra resources".
5. Negative checks: a file encrypted with another `--mk` reports "could not be opened"; a corrupted copy is rejected.

Tests: `cd packages/four_format && dart test` (round-trip, chunk seek, tamper, swap, truncation, wrong key) and
`flutter test test/resources_gate_test.dart` (locked / legacy / strong / forged proof).
