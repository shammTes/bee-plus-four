# 4 Encryptor (Android)

Native Flutter app (no WebView) that turns PDFs, videos and offline web pages into add-on files for 4 or Bee Plus:
`.4pdf`, `.4vid` (16:9), `.4reel` (9:16) and `.4web` (interactive page bundle). Same container and key chain as
`packages/four_format` (master key → batch key → file key, AES-256-GCM, 256 KiB chunks), so the files open in 4
exactly like files from the Mac/CLI tools.

## Use
1. **Add files** (system picker, many at once): PDFs, videos, or a `.zip` of a saved web page.
   ⋮ menu: **Add web page folder…** (a saved page folder with an `index.html`) or **Import LabXchange link…**.
2. Each file gets an auto-detected type (PDF / Video 16:9 / Reel 9:16 by orientation / Web), title,
   optional subject + grade + unit (subject+grade+unit put it on the matching notes unit page in 4).
3. Third-party content: tick *Made by someone else*, pick the licence and fill author + source URL. The credit is
   stored in the file and 4 shows it under the content.
4. **Encrypt**: choose the output folder once (SAF), progress per file + overall, then **Share** (SHAREit, Bluetooth…).

Inputs are read in place through their content URI, one chunk at a time, and outputs are written straight into the
chosen folder, so a 2 GB video needs no extra space and little RAM. AES-GCM runs natively through
`cryptography_flutter` (javax.crypto; hardware AES on ARMv8). Thumbnails, duration and page count come from Android
(`MediaMetadataRetriever`, `PdfRenderer`), so nothing big is bundled. There is no decrypt function in this app.

## Target app: 4 or Bee Plus
The switch at the top (**Files for: 4 | Bee Plus**) picks the app the files are for. Both apps read the same
container (`.4pdf` / `.4vid` / `.4reel`), but each has its **own master key**, so a file made for 4 does not open in
Bee Plus and vice versa:

| Target | Release key define | Without the define |
|---|---|---|
| 4 | `FOUR_MK` (same as 4's `lib/resources/gate.dart`) | 4 DEV key (`FourKeys.devMasterKey`) |
| Bee Plus | `BEE_MK` (same as Bee Plus' `lib/junior/resources/gate.dart`) | Bee Plus DEV key (SHA-256 of `BEE-RES-DEV-MASTER-KEY-v1-CHANGE-IN-RELEASE`) |

The subject and grade lists follow the target (Bee Plus: Grades 6–8 and Junior's subject ids such as `science`,
`mathematics`, `social_studies`), so subject + grade + unit put the file on the matching notes unit page. The key chip
and its fingerprint show the key of the selected target. The choice is not saved: the app starts on 4 every time.
`.4web` pages are not supported by Bee Plus. Release build carrying both keys:

    flutter build apk --release --target-platform android-arm,android-arm64 --dart-define=FOUR_MK=<4 key> --dart-define=BEE_MK=<Bee Plus key>

## Master key
Exactly the same source as the 4 app (`lib/resources/gate.dart`): `--dart-define=FOUR_MK=<base64 32 bytes>`;
without it the public DEV key from four_format. The key chip in the app bar says which one is in the build and shows
a short fingerprint. **When 4 switches to a real release key, rebuild this app with the same `FOUR_MK`**:

    flutter build apk --release --target-platform android-arm,android-arm64 --dart-define=FOUR_MK=<same key as 4>

Files made with the DEV build will then no longer open in release 4 (re-encrypt them). Keep this APK private:
the master key is inside it, like it is inside 4.

## Licence gate (4 is a paid app)
Allowed: CC BY, CC BY-SA, CC0, public domain, CC BY-ND (unmodified files only; web pages count as modified because
references are rewritten). Refused with a message: any NC licence, "all rights reserved", the LabXchange Standard
License (LX1: personal non-commercial use on the site only), and unknown licences. For LabXchange links the licence
is read from the LabXchange API and cannot be changed by hand.

## LabXchange import
Resolves `…/library/items/lb:…` through the public API (`api.www.labxchange.org/api/v1/items/<id>`), checks the
licence, then downloads: documents → PDF; videos → MP4 when LabXchange offers one (YouTube-only videos are refused);
simulations/interactives → an offline mirror of the page (`lib/src/web_mirror.dart`: HTML, scripts, styles, images,
fonts, plus asset paths found in JS), zipped into a `.4web`. Pages that fetch data from servers at run time will
not work offline; test the `.4web` in 4 with Wi-Fi off before sharing.

## Build / test
    flutter pub get && flutter test
    flutter build apk --release --target-platform android-arm,android-arm64
    dart run tool/labx_check.dart /tmp/out <labxchange url>…   # licence + offline mirror check on a PC
