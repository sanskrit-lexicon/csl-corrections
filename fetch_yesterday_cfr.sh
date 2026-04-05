#!/bin/bash

set -e

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
if ! curl -o "$OUTPUT" "$URL"; then
    echo "ERROR: Failed to download $URL" >&2
    exit 1
fi

if [ -s "$OUTPUT" ]; then
    echo "File downloaded successfully, running cfr_adj.py..."
    cd "$DIR"
    mkdir -p dictionaries
    python3 ../../cfr_adj.py "cfr-${YESTERDAY}.tsv" "correctionform-${YESTERDAY}.txt"
else
    echo "WARNING: Downloaded file is empty, skipping cfr_adj.py"
    exit 1
fi