#!/bin/bash
# build-quickstart.sh — Genera il PDF Quickstart (gratuito, 12-16 pagine)
# Estrae un sottoinsieme dalla stessa repository del manuale completo
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$ROOT_DIR/output"
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

mkdir -p "$OUTPUT_DIR"
echo "📖 Assemblaggio Quickstart..."

# === 1. Solo le pagine essenziali ===
PAGES=(
  index.md
  il-sistema.md
  stress-ed-echi.md
  archetipi.md
  archetipi/il-sopravvissuto.md
  archetipi/il-testimone.md
  archetipi/il-protettore.md
  archetipi/il-catalizzatore.md
  scenario-incidente.md
  riferimento-rapido.md
)
RULES_MD="$TMP_DIR/rules.md"
> "$RULES_MD"
for page in "${PAGES[@]}"; do
  f="$ROOT_DIR/$page"
  [ -f "$f" ] && sed '1{/^---$/!q;};1,/^---$/d' "$f" | sed 's/{:.*}//g' >> "$RULES_MD" && echo -e "\n\n" >> "$RULES_MD"
done
echo "   Markdown → HTML..."
pandoc "$RULES_MD" -f markdown -t html5 --toc --toc-depth=2 --metadata title="" -o "$TMP_DIR/rules-body.html"

# === 2. Render materiali da YAML (schede + carte) ===
echo "   YAML → Schede + Carte..."
python3 "$SCRIPT_DIR/render_materials.py" sheets > "$TMP_DIR/sheets.html"
python3 "$SCRIPT_DIR/render_materials.py" cards  > "$TMP_DIR/cards.html"

# === 3. Assembla template quickstart ===
echo "   Assemblaggio HTML finale..."
cp "$SCRIPT_DIR/pdf-template-quickstart.html" "$TMP_DIR/full.html"
cp "$SCRIPT_DIR/pdf-style.css" "$TMP_DIR/pdf-style.css"
cp -r "$ROOT_DIR/assets" "$TMP_DIR/assets" 2>/dev/null || true

python3 << PYEOF
import re, pathlib

html = pathlib.Path("$TMP_DIR/full.html").read_text()
rules_raw = pathlib.Path("$TMP_DIR/rules-body.html").read_text()
sheets = pathlib.Path("$TMP_DIR/sheets.html").read_text()
cards = pathlib.Path("$TMP_DIR/cards.html").read_text()

toc = re.search(r'<nav[^>]*id="TOC".*?</nav>', rules_raw, re.DOTALL)
toc_html = toc.group(0) if toc else ''
rules_html = re.sub(r'<nav[^>]*id="TOC".*?</nav>', '', rules_raw, flags=re.DOTALL)

# Split at each <h1 for page breaks
parts = re.split(r'(?=<h1[ >])', rules_html)
sections = []
for i, part in enumerate(parts):
    part = part.strip()
    if not part:
        continue
    sections.append(f'<section class="rules">\n{part}\n</section>')
rules_final = '\n\n'.join(sections)

html = html.replace('<!-- TOC_PLACEHOLDER -->', toc_html)
html = html.replace('<!-- RULES_PLACEHOLDER -->', rules_final)
html = html.replace('<!-- SHEETS_PLACEHOLDER -->', sheets)
html = html.replace('<!-- CARDS_PLACEHOLDER -->', cards)
html = html.replace('CSSPATH', "$TMP_DIR/pdf-style.css")

pathlib.Path("$TMP_DIR/full.html").write_text(html)
PYEOF

# === 4. PDF ===
echo "🎨 WeasyPrint..."
weasyprint "$TMP_DIR/full.html" "$OUTPUT_DIR/anamnesia-quickstart-free.pdf" 2>&1 | grep -v "WARNING" || true

echo "✅ Quickstart: $OUTPUT_DIR/anamnesia-quickstart-free.pdf"
