#!/usr/bin/env bash
# Runs Bee Seller 1.2.0's own parser (bee-plus-ecosystem, Android) on codes made by this app.
#   SELLER_REPO=/path/to/bee-plus-ecosystem tool/bee_seller_compat.sh
set -euo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
: "${SELLER_REPO:?set SELLER_REPO to a bee-plus-ecosystem checkout}"
: "${GRADLE:=gradle}"
(cd "$here" && flutter test test/grant_test.dart --plain-name 'write compatibility vectors')
work=$(mktemp -d)
(cd "$SELLER_REPO" && tar --exclude=build --exclude=.gradle --exclude=.git -cf - .) | tar -xf - -C "$work"
# Only the modules Bee Seller needs (other apps may be missing from a partial checkout).
sed -i -E '/":app-bee-(plus|master)",?/d' "$work/settings.gradle.kts"
cp "$here/tool/BeeSellerCompatTest.kt" "$work/app-bee-seller/src/test/java/com/beeplus/seller/"
SHAMM_VECTORS="$here/build/compat_vectors.tsv" "$GRADLE" -p "$work" ${GRADLE_OFFLINE:-} :app-bee-seller:testDebugUnitTest \
  --tests 'com.beeplus.seller.BeeSellerCompatTest' --tests 'com.beeplus.seller.ShammMasterCodeTest' -i | grep -E 'BeeSellerCompat|PASSED|FAILED|BUILD' || true
echo "report: $work/app-bee-seller/build/test-results"
