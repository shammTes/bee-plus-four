#!/bin/bash
# FourLock 1.1 — lock / unlock papers for the 4 app.
# Uses only bash + osascript + openssl (all built into macOS).
# Do not use "set -e": a failed dialog must not exit with a blank screen.

export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin:$PATH"
LOG="$HOME/Library/Logs/FourLock.log"
mkdir -p "$(dirname "$LOG")" 2>/dev/null || true
say_log() { printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG" 2>/dev/null || true; }
say_log "start pwd=$(pwd) script=$0"

alert() {
  local msg="$1"
  /usr/bin/osascript -e "display dialog \"$msg\" buttons {\"OK\"} default button \"OK\" with title \"FourLock\"" >/dev/null 2>>"$LOG" || true
}

die() {
  say_log "error: $*"
  alert "FourLock could not finish.\\n\\n$*\\n\\nA log is at:\\n$LOG"
  echo "ERROR: $*" >&2
  exit 1
}

echo
echo "  FourLock  —  papers for the 4 app"
echo "  Log: $LOG"
echo

/usr/bin/osascript -e 'display dialog "FourLock is ready.\n\nNext you will pick Lock, Unlock or Pack." buttons {"Continue"} default button "Continue" with title "FourLock"' >/dev/null 2>>"$LOG" || {
  echo "  (dialog blocked — using this Terminal window instead)"
}

choice="$(/usr/bin/osascript <<'EOF' 2>>"$LOG"
set theChoice to choose from list {"Lock a PDF", "Unlock a PDF / .fourpdf / .fourpack", "Pack exam JSON as .fourpack"} with prompt "What do you want to do?" with title "FourLock" default items {"Lock a PDF"}
if theChoice is false then return "cancel"
return item 1 of theChoice
EOF
)"
choice="$(printf '%s' "$choice" | tr -d '\r')"
say_log "choice=$choice"
if [ -z "$choice" ] || [ "$choice" = "cancel" ]; then
  echo "  1  Lock a PDF"
  echo "  2  Unlock a PDF / .fourpdf / .fourpack"
  echo "  3  Pack exam JSON as .fourpack"
  echo "  4  Cancel"
  printf "  Choose 1-4: "
  read -r n || n=4
  case "$n" in
    1) choice="Lock a PDF" ;;
    2) choice="Unlock" ;;
    3) choice="Pack" ;;
    *) echo "Cancelled."; exit 0 ;;
  esac
fi

file="$(/usr/bin/osascript <<'EOF' 2>>"$LOG"
set theFile to choose file with prompt "Pick the file"
return POSIX path of theFile
EOF
)" || true
file="$(printf '%s' "$file" | tr -d '\r')"
file="${file%"${file##*[![:space:]]}"}"
if [ -z "$file" ] || [ ! -f "$file" ]; then
  printf "  Path to the file: "
  read -r file || true
  file="${file%\"}"; file="${file#\"}"
  file="${file/#\~/$HOME}"
fi
say_log "file=$file"
[ -n "$file" ] && [ -f "$file" ] || die "No file was picked."

pass="$(/usr/bin/osascript <<'EOF' 2>>"$LOG"
set thePass to display dialog "Password for this paper" default answer "" with hidden answer buttons {"Cancel", "OK"} default button "OK" with title "FourLock"
if button returned of thePass is "Cancel" then return ""
return text returned of thePass
EOF
)" || true
pass="$(printf '%s' "$pass" | tr -d '\r')"
if [ -z "$pass" ]; then
  printf "  Password: "
  read -r pass || true
fi
[ -n "$pass" ] || die "No password typed."

cmd="lock"
case "$choice" in
  Unlock*) cmd="unlock" ;;
  Pack*)   cmd="pack" ;;
esac

dir="$(dirname "$file")"
base="$(basename "$file")"
stem="${base%.*}"
tmp="$(/usr/bin/mktemp -t fourlock)"
out=""

run_openssl() {
  local mode="-e"
  [ "$3" = "dec" ] && mode="-d"
  /usr/bin/openssl enc $mode -aes-256-cbc -pbkdf2 -iter 200000 -salt \
    -in "$1" -out "$2" -pass "pass:$pass"
}

if [ "$cmd" = "lock" ]; then
  if command -v qpdf >/dev/null 2>&1; then
    out="$dir/${stem}.locked.pdf"
    qpdf --encrypt "$pass" "$pass" 256 -- "$file" "$out" || die "qpdf failed."
    msg="Locked with qpdf AES-256:\\n$out"
  else
    out="$dir/${base}.fourpdf"
    run_openssl "$file" "$tmp" enc || die "openssl encrypt failed."
    { printf 'FOURPDF1'; cat "$tmp"; } > "$out" || die "could not write $out"
    msg="Locked as .fourpdf (openssl AES-256):\\n$out\\n\\nTip: brew install qpdf  for a normal password-PDF next time."
  fi
elif [ "$cmd" = "pack" ]; then
  case "$base" in
    *.json|*.JSON) ;;
    *) die "Pack needs a 4 exam JSON file." ;;
  esac
  out="$dir/${stem}.fourpack"
  run_openssl "$file" "$tmp" enc || die "openssl encrypt failed."
  { printf 'FOURPACK'; cat "$tmp"; } > "$out" || die "could not write $out"
  msg="Packed:\\n$out\\n\\nUnlock on this Mac, then copy the JSON into 4 (assets/high/exams / Model tab)."
else
  head8="$(/usr/bin/dd if="$file" bs=8 count=1 2>/dev/null)"
  if [ "$head8" = "FOURPDF1" ] || [ "$head8" = "FOURPACK" ]; then
    /usr/bin/dd if="$file" bs=8 skip=1 of="$tmp.enc" 2>/dev/null || die "could not read wrapper"
    if [ "$head8" = "FOURPACK" ]; then
      out="$dir/${stem}.unlocked.json"
    else
      out="$dir/${stem}.unlocked.pdf"
    fi
    run_openssl "$tmp.enc" "$out" dec || die "Wrong password, or the file is damaged."
    rm -f "$tmp.enc"
    msg="Unlocked:\\n$out"
  else
    command -v qpdf >/dev/null 2>&1 || die "This looks like a normal PDF. Install qpdf:\\n\\nbrew install qpdf"
    out="$dir/${stem}.unlocked.pdf"
    qpdf --password="$pass" --decrypt "$file" "$out" || die "qpdf could not decrypt (wrong password?)."
    msg="Unlocked with qpdf:\\n$out"
  fi
fi

rm -f "$tmp" "$tmp.enc"
say_log "ok $out"
echo
echo "  Done."
echo "  $out"
echo
alert "Done.\\n\\n$msg"
if [ -t 0 ]; then
  echo "  Press Return to close."
  read -r _ || true
fi
exit 0
