#!/bin/bash
# build-all.sh — Build all 6 AnamnesiA PDFs (IT + EN + ES × Zine + Quickstart)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "================================================"
echo "  AnamnesiA — Building all PDFs"
echo "================================================"
echo ""

echo "🇮🇹 [1/6] Zine Italiano..."
LANG=it bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇮🇹 [2/6] Quickstart Italiano..."
LANG=it bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇬🇧 [3/6] Zine English..."
LANG=en bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇬🇧 [4/6] Quickstart English..."
LANG=en bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇪🇸 [5/6] Zine Español..."
LANG=es bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇪🇸 [6/6] Quickstart Español..."
LANG=es bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "================================================"
echo "  ✅ All PDFs generated:"
ls -la "$(dirname "$SCRIPT_DIR")/output/"*.pdf
echo "================================================"
