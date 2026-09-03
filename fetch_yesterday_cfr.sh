#!/bin/bash
#
# Download yesterday's correction-form submissions from the Cologne server and
# turn them into daily/<YYYYMMDD>/correctionform-<YYYYMMDD>.txt.
#
# H3885: curl now uses -f, so an HTTP error is an error instead of a 404 HTML
# page saved under a .tsv name. A 404 is the normal "nobody submitted anything
# yesterday" case and exits 0; every other failure exits non-zero.

set -euo pipefail

if [[ "$(uname)" == "Darwin" ]]; then
    YESTERDAY=$(date -v-1d +%Y%m%d)
else
    YESTERDAY=$(date -d "yesterday" +%Y%m%d)
fi

DIR="daily/$YESTERDAY"
mkdir -p "$DIR"

URL="https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-corrections/app/correction_response/cfr-${YESTERDAY}.tsv"
OUTPUT="$DIR/cfr-${YESTERDAY}.tsv"

echo "Downloading $URL..."
HTTP_CODE=$(curl -fsS --retry 3 --retry-delay 5 -o "$OUTPUT" -w '%{http_code}' "$URL") && CURL_RC=0 || CURL_RC=$?

if [ "$CURL_RC" -ne 0 ]; then
    rm -f "$OUTPUT"
    if [ "$HTTP_CODE" = "404" ]; then
        echo "No corrections file for $YESTERDAY (HTTP 404) - nobody submitted yesterday. Nothing to do."
        rmdir "$DIR" 2>/dev/null || true
        exit 0
    fi
    echo "ERROR: Failed to download $URL (curl exit $CURL_RC, HTTP ${HTTP_CODE:-none})" >&2
    exit 1
fi

if [ ! -s "$OUTPUT" ]; then
    echo "ERROR: Downloaded file $OUTPUT is empty" >&2
    rm -f "$OUTPUT"
    exit 1
fi

echo "File downloaded successfully, running cfr_adj.py..."
cd "$DIR"
mkdir -p dictionaries
python3 ../../cfr_adj.py "cfr-${YESTERDAY}.tsv" "correctionform-${YESTERDAY}.txt"
