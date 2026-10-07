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

## Stage 2: 16:9 encrypted video
**Playback path:** `.4vid` → `FourChunkReader.kt` (javax.crypto AES-GCM, one 256 KiB chunk per read, last chunk cached) →
`FourDataSource` (media3 `BaseDataSource`, honours range position/length) → ExoPlayer → Flutter `SurfaceProducer` texture.
Dart only unwraps the content key (gate-checked) and hands it to native memory: no HTTP server, no temp file, no Dart in the byte path.

Why not loopback HTTP + video_player: bytes would be decrypted in Dart (pure Dart ≈ 9 MB/s on a desktop, far less on a
low-end phone) or bounced through a channel per chunk, plus an open local port. Why not media_kit: libmpv adds ~8–12 MB
per ABI. media3-exoplayer core alone added +0.8 MB to the universal APK (147.0 → 147.8 MB).

**Player** (`lib/resources/video_page.dart`): seek bar (drag/tap, buffered track), 0.5–2× speed, fullscreen = landscape +
immersive (back exits fullscreen), double-tap left/right ∓10 s, tap toggles controls (auto-hide 3 s), FLAG_SECURE,
resume position (saved every 3 s and on close; cleared near the end). Reels open in this player until Stage 3.

**Encryptor:** CLI `--transcode720` (ffmpeg → ≤720p H.264 main + AAC 96k + faststart), duration via ffprobe, thumbnail via
ffmpeg. Mac app: same, transcode checkbox (on by default).

**Tests:** `cd android && ./gradlew :app:testDebugUnitTest` (FourChunkReaderTest: full read, seek = 1 chunk + cache,
DataSource ranges, wrong key, tampered chunk, truncated file, throughput); `dart test` in four_format (pure-Dart benchmark);
`flutter test test/native_video_test.dart`.
