#!/bin/bash
# build-all.sh — Build all AnamnesiA PDFs (IT + EN + ES + FR × Zine + Quickstart)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "================================================"
echo "  AnamnesiA — Building all PDFs"
echo "================================================"
echo ""

echo "🇮🇹 [1/8] Zine Italiano..."
LANG=it bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇮🇹 [2/8] Quickstart Italiano..."
LANG=it bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇬🇧 [3/8] Zine English..."
LANG=en bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇬🇧 [4/8] Quickstart English..."
LANG=en bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇪🇸 [5/8] Zine Español..."
LANG=es bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇪🇸 [6/8] Quickstart Español..."
LANG=es bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "🇫🇷 [7/8] Zine Français..."
LANG=fr bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇫🇷 [8/8] Quickstart Français..."
LANG=fr bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "================================================"
echo "  ✅ All PDFs generated:"
ls -la "$(dirname "$SCRIPT_DIR")/output/"*.pdf
echo "================================================"
