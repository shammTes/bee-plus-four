#!/usr/bin/env bash
set -euo pipefail
mkdir -p assets/fonts \
  assets/content/phet \
  assets/content/vendor/katex/fonts \
  assets/content/examprep_preview \
  assets/content/interactive_notes \
  assets/content/illustrated_pdf \
  assets/content/textbooks
curl -sL -o assets/fonts/NotoSansEthiopic-Regular.ttf \
  "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansEthiopic/NotoSansEthiopic-Regular.ttf"
curl -sL -o assets/fonts/NotoSans-Regular.ttf \
  "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf"
curl -sL -o assets/fonts/Nunito-VariableFont_wght.ttf \
  "https://github.com/google/fonts/raw/main/ofl/nunito/Nunito%5Bwght%5D.ttf" || \
curl -sL -o assets/fonts/Nunito-VariableFont_wght.ttf \
  "https://github.com/googlefonts/nunito/raw/main/fonts/variable/Nunito%5Bwght%5D.ttf"
test -s assets/fonts/NotoSansEthiopic-Regular.ttf
test -s assets/fonts/NotoSans-Regular.ttf
test -s assets/fonts/Nunito-VariableFont_wght.ttf
touch assets/content/phet/.keep assets/content/vendor/katex/.keep assets/content/vendor/katex/fonts/.keep
ls -lh assets/fonts
