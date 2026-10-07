# FourEncryptor (Flutter macOS / Windows)

Encrypts PDFs (Stage 1) and videos (Stage 2/3) into `.4pdf` / `.4vid` / `.4reel` files that only phones which
unlocked 4 can open. Format + crypto: `packages/four_format` (shared with the phone app). Spec: `docs/encrypted_resources.md`.

## Build & run (on the Mac)
```
cd tools/four_encryptor
flutter pub get
flutter run -d macos          # or: flutter build macos  → build/macos/Build/Products/Release/four_encryptor.app
```
Windows: same source, `flutter run -d windows` (the master key goes to Windows Credential Manager).

## Use
1. Drag PDFs (or a folder) onto the window. A thumbnail is made from page 1 (click it to choose another image).
   Videos need `ffmpeg`/`ffprobe` on PATH (`brew install ffmpeg`) for thumbnail, duration and the optional
   **transcode to 720p** (H.264 main + AAC 96k, faststart — recommended for low-end phones; on by default).
2. Set title / subject / grade / unit per row, or set them in the top bar and **Apply to selected**.
3. **Encrypt selected** → choose an output folder. Each file is encrypted in a background isolate, chunk by chunk.
4. Copy the output files to the phone (cable or SHAREit), then in 4: Home → Extra resources → Refresh.

## Master key
- Default is the **DEV key**, which matches debug builds and release builds made without `FOUR_MK`.
- For real distribution: key button → Generate new → Save to Keychain, and build 4 with
  `flutter build apk --release --dart-define=FOUR_MK=<that base64 key>`. Files made with one key only open in apps built with it.
- macOS sandbox entitlements already include user-selected file access and Keychain.

No-GUI alternative (any OS, handy for testing): `dart run four_format:four_encrypt --help` from `packages/four_format`.
