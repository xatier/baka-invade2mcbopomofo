#!/usr/bin/env bash

set -euo pipefail

DICT="/usr/share/fcitx5/data/mcbopomofo-data.txt"

while IFS= read -r line; do
    # for exact match
    ag " $line " "$DICT" || :
done <1.txt
