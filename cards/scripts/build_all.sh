#!/usr/bin/env bash
# Build all AnamnesiA card decks (IT + EN) for DriveThruCards.
#
# Usage (run from the repo root):
#   bash cards/scripts/build_all.sh

set -euo pipefail
cd "$(dirname "$0")/../.."  # repo root

bash cards/scripts/build_it.sh
bash cards/scripts/build_en.sh

echo
echo "All decks built. DTC-ready ZIPs:"
echo "  cards/output/it/jpgs/deck_it_dtc.zip"
echo "  cards/output/en/jpgs/deck_en_dtc.zip"
