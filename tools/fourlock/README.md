# FourLock — Mac paper locker for 4

**Do not use the old FourLock.dmg.** It was an ISO with no app executable, so double-click did nothing.

Use **FourLock.zip**. Unzip it and double-click `Open FourLock.command`.
A Terminal window must appear. If macOS blocks the file:

```
xattr -cr ~/Downloads/FourLock
chmod +x ~/Downloads/FourLock/"Open FourLock.command"
```

Then right-click → Open.

The tool uses bash + osascript + openssl (already on macOS). Optional: `brew install qpdf` for a normal password-PDF.

4 does not render PDFs on the phone. Unlock on the Mac, then copy exam JSON into `assets/high/exams` / the Model tab.
