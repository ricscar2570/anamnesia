#!/usr/bin/env bash
# Build the Italian AnamnesiA card deck for DriveThruCards.
#
# Usage (run from the repo root):
#   bash cards/scripts/build_it.sh

set -euo pipefail
cd "$(dirname "$0")/../.."  # repo root

python -m cards.builders.deck --lang it
