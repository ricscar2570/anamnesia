#!/bin/bash
# build-all.sh — Build all 4 AnamnesiA PDFs (IT + EN × Zine + Quickstart)
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
echo "🇩🇪 [5/6] Zine Deutsch..."
LANG=de bash "$SCRIPT_DIR/build-pdf.sh"

echo ""
echo "🇩🇪 [6/6] Quickstart Deutsch..."
LANG=de bash "$SCRIPT_DIR/build-quickstart.sh"

echo ""
echo "================================================"
echo "  ✅ All PDFs generated:"
ls -la "$(dirname "$SCRIPT_DIR")/output/"*.pdf
echo "================================================"
