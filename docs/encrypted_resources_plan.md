# 4 — Encrypted Add-on Resources (PDF / Video / Reels) — Design Plan

## What exists today (inspected)
- Repo `shammTes/bee-plus-four` (pubspec name `high`, Flutter >=3.44, deps: shared_preferences, crypto, qr_flutter, flutter_svg, flutter_math_fork). No PDF/video/file-picker deps yet.
- Unlock: `lib/licensing/` — native Android ZXing/ML Kit scanner via platform channel (`lock_screen.dart`), parsing in `qr_payload.dart`, state in `unlock_store.dart`.
- QR formats: `BEE1|HIGHSCHOOL|<deviceId>|<nonce>|<hmac-sha256-hex>` (key from `--dart-define BEE_HMAC_KEY`, with a hard-coded default) and Kotlin Seller `BEE1|<deviceId>|<pkg>|<nonce>|<ts>|<hmac12>` (key hard-coded in source).
- Unlock state = SharedPreferences bool `four_highschool_unlocked`; device id = random 12-char `four_device_id_v1`; used nonces list `four_used_nonces`. **Weakness:** a rooted user can flip the bool; nothing secret is stored after unlock.
- `shammTes/bee-plus-ecosystem`: not accessible to the authed account (skipped).

## 1. File format (`.4pdf`, `.4vid`, `.4reel`)
```
magic "4RES" | version u8 | flags u8 | headerLen u32
header (JSON, AES-GCM encrypted with content key, own nonce):
  {id, title, subject, grade, unit, type: pdf|video|reel, mime, durationMs?, pages?,
   size, chunkSize, chunkCount, batchId, createdAt}
thumbnail (JPEG ≤40 KB, AES-GCM encrypted, separate nonce)
keyBlock: batchId + wrappedContentKey (AES-KW or AES-GCM under batch key)
chunks[]: each = ciphertext(chunkSize) + 16-byte GCM tag; nonce = noncePrefix(8) || chunkIndex(u32)
footer: HMAC/GCM tag over header+chunk table (anti-truncation/reorder)
```
- AES-256-GCM, chunk 256 KB (video) / whole-file-in-chunks for PDF. Random-access: offset → chunk index → decrypt one chunk (≈constant cost per seek). Chunk index in nonce + AAD (fileId, index, isLast) prevents swaps/truncation.
- Plain-ish public fields kept minimal: only magic/version/batchId so the app can tell "needs batch X" without decrypting.

## 2. Key scheme (tied to unlock)
- **Master key (MK)**: 32 bytes, embedded in the app obfuscated (split + XOR, ideally in native code via NDK) **and** combined with a secret the app only gets from a valid unlock.
- Recommended: extend unlock so a fresh code yields `unlockSecret = HMAC(sellerKey, "RES"|deviceId|nonce)`; app derives `deviceKEK = HKDF(MK, unlockSecret||deviceId)` and stores the batch keys re-wrapped under it in Android Keystore–backed storage (`flutter_secure_storage`). The bool flag alone never decrypts anything.
- **Batch keys**: Mac tool creates a per-batch key BK, wrapped under MK (`batch_<id>.4key` inside each file's keyBlock). Content key per file wrapped by BK. Lets you revoke/rotate future batches (new MK version) without re-encrypting old ones.
- **Honesty:** this is offline DRM; the key ultimately lives on the phone. A determined attacker with root + reverse engineering can extract MK or decrypted frames/screen-record. Goal is: copied files are useless on non-unlocked phones / casual sharing via SHAREit. Mitigations: FLAG_SECURE on players, keys never written to disk in plain, R8/obfuscation, rotate HMAC keys (current defaults in source should be replaced via dart-define before release).

## 3. Android import flow
1. Resources → "Choose folder" (once): SAF `ACTION_OPEN_DOCUMENT_TREE`, persist URI permission (`takePersistableUriPermission`). No storage permission needed (works API 21–35, scoped storage safe).
2. "Refresh": list folder for `*.4pdf|*.4vid|*.4reel`, read header magic + id; skip already-imported ids.
3. Copy (streamed, still encrypted) into app private dir `files/resources/<id>.bin`; decrypt header+thumb only to build a local index (JSON or sqlite).
4. Optional: offer to delete originals (user confirms). Show progress, handle low space.
- Locked phones may import but every tile shows a lock and opens the unlock screen.

## 4. Where it appears in UI
- **Notes unit pages**: "Extra resources" strip (thumbnails) filtered by subject+grade+unit from header.
- **Resources section** (new tab/home tile): filters Subject/Grade/Type, Refresh button, folder settings; Reels entry opens vertical feed.

## 5. Players (native only, no WebView)
- **PDF**: decrypt to memory (PDFs are small) → `pdfrx` `PdfViewer.data` (PDFium, smooth, zoom/search). Large PDFs: pdfrx custom read-function from the chunk reader.
- **16:9 video**: `media_kit` + `media_kit_video` (hardware decoding via libmpv). Feed it `http://127.0.0.1:<port>/<token>` from an in-app loopback server (dart:io `HttpServer`, bound to loopback, random token, supports HTTP Range → decrypts only needed chunks). Controls: seek bar, 0.5–2× speed, fullscreen/landscape lock, double-tap ±10 s.
- Alternative for `video_player` (ExoPlayer): same loopback server works; a custom ExoPlayer DataSource is faster but needs Kotlin code—consider for Stage 2b if loopback is CPU-heavy.
- **Reels**: `PageView` vertical, keep only 3 players alive (prev/current/next), preload next's first chunk, tap = pause, double-tap = skip forward, thin seek bar. Recommend reels encoded 720p H.264 ≤2 Mbps.

## 6. Packages (verify exact latest on pub.dev against Flutter 3.47.6 before adding)
- `pdfrx` (PDF), `media_kit`, `media_kit_video`, `media_kit_libs_android_video` (only video libs, not audio-full), `cryptography` + `cryptography_flutter` (native AES-GCM via platform crypto – much faster than pure-Dart `pointycastle` on low-end), `flutter_secure_storage`, SAF: `saf_stream`/`shared_storage` or a small Kotlin channel (preferred — the app already uses channels for the scanner). Mac: `desktop_drop`, `file_picker`, `cryptography`, `ffmpeg` CLI for thumbnails.
- Note: I did not run a live pub.dev compatibility check; pin versions after `flutter pub add` on 3.47.6.

## 7. Mac encryptor app (Flutter macOS)
- Drag-drop files/folders → table with metadata form (title, subject, grade, unit, type auto-detected, thumbnail auto from PDF page 1 / video frame, editable). Batch apply subject/grade/unit.
- "Encrypt batch" → writes `.4pdf/.4vid/.4reel` to output folder, progress per file, isolate-based streaming encryption (no full-file RAM).
- Holds MK in macOS Keychain; batch keys log. Optional pre-transcode via ffmpeg to 720p.
- Shares a pure-Dart `four_format` package with the app (format + reader/writer) → Windows build reuses ~100% (only drag-drop/keychain plugin swaps).

## 8. APK size & performance
- pdfrx (PDFium): ~+4–6 MB per ABI; media_kit video libs: ~+8–12 MB per ABI. Use `--split-per-abi`/App Bundle; arm64+armeabi-v7a only. Total ≈ +12–18 MB per-ABI APK.
- AES-GCM native: ~100–300 MB/s on low-end ARM with AES instructions; 2 Mbps video needs <1 MB/s → negligible. Avoid pure-Dart crypto in the hot path. Lazy-load players (deferred init) so app start time is unchanged.

## 9. Staged rollout
- **Stage 1**: format spec + `four_format` package + tests, key scheme & unlock extension, Mac tool, SAF import, Resources section, PDF viewer.
- **Stage 2**: 16:9 video (loopback Range server + media_kit), unit-page strips.
- **Stage 3**: Reels feed, preloading, perf tuning on a 2 GB RAM device.

## 10. Risks & open questions
- Offline keys are extractable by experts; accept or add per-device online activation?
- Phones already unlocked with old codes have no `unlockSecret` — fall back to MK-only (weaker) or require a re-scan?
- Hard-coded HMAC/seller keys in source → rotate & move to dart-define/native before relying on them.
- SHAREit may rename extensions/strip files; detect by magic bytes, not just extension.
- Low-end devices without AES hardware (some old ARMv7) — test speed; maybe lower bitrates.
- Storage: duplicated files (shared folder + private copy) — offer cleanup.
- Is ecosystem/Bee Seller repo to be updated to issue resource-capable codes? (not accessible to inspect).
- Revocation/expiry of batches? Per-grade bundles priced separately?
