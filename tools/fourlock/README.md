# FourLock — Mac paper locker for 4

Encrypt a paper PDF or wrap a 4 exam JSON so it can travel safely, then unlock it on the same Mac.

## Get the disk image

After CI runs, download **FourLock.dmg** (or FourLock.zip) from the Actions artifact `fourlock-mac`.

Or build it here:

```
python3 tools/make_fourlock_dmg.py
# writes dist/FourLock.dmg and dist/FourLock.zip
```

On a Mac: open the `.dmg` (or unzip), drag **FourLock.app** to Applications, double-click.

Needs Python 3 (already on macOS). For a normal password-PDF also run `brew install qpdf`.

## What it makes

| Action | Output | Open in 4? |
| --- | --- | --- |
| Lock PDF | `.locked.pdf` via qpdf AES-256, else `.fourpdf` wrapper | No — 4 does not render PDFs |
| Pack JSON | `.fourpack` (AES-256 exam wrap) | Unlock on the Mac, copy JSON into `assets/high/exams` / Model tab |
| Unlock | original PDF or JSON | — |

CLI (same engine):

```
python3 tools/encrypt_pdf_mac.py lock  Physics_2024.pdf --password sawa
python3 tools/encrypt_pdf_mac.py pack  physics_2024_matric.json --password sawa
python3 tools/encrypt_pdf_mac.py unlock Physics_2024.pdf.fourpdf --password sawa
```
