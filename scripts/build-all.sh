#!/bin/bash
# build-all.sh — Build all AnamnesiA PDFs (IT + EN + DE + ES + FR × Zine + Quickstart)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "================================================"
echo "  AnamnesiA — Building all PDFs"
echo "================================================"
echo ""

echo "🇮🇹 [1/10] Zine Italiano..."
LANG=it bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇮🇹 [2/10] Quickstart Italiano..."
LANG=it bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇬🇧 [3/10] Zine English..."
LANG=en bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇬🇧 [4/10] Quickstart English..."
LANG=en bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇩🇪 [5/10] Zine Deutsch..."
LANG=de bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇩🇪 [6/10] Quickstart Deutsch..."
LANG=de bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇪🇸 [7/10] Zine Español..."
LANG=es bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇪🇸 [8/10] Quickstart Español..."
LANG=es bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇫🇷 [9/10] Zine Français..."
LANG=fr bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇫🇷 [10/10] Quickstart Français..."
LANG=fr bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "================================================"
echo "  ✅ All PDFs generated:"
ls -la "$(dirname "$SCRIPT_DIR")/output/"*.pdf
echo "================================================"
