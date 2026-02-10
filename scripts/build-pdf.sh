#!/bin/bash
# build-pdf.sh — Genera il PDF completo di AnamnesiA
# Legge i dati da _data/*.yml tramite render_materials.py
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$ROOT_DIR/output"
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

mkdir -p "$OUTPUT_DIR"
echo "📖 Assemblaggio documento completo..."

# === 1. Regole: Markdown → HTML ===
PAGES=(
  index.md pilastri.md come-si-gioca.md il-sistema.md stress-ed-echi.md
  archetipi.md archetipi/il-sopravvissuto.md archetipi/il-testimone.md
  archetipi/il-protettore.md archetipi/il-catalizzatore.md
  sessione-zero.md guida-custode.md avvio-primo-ciclo.md esempio-di-gioco.md
  scenario-incidente.md scenario-tradimento.md
  riferimento-rapido.md varianti.md changelog.md
)
RULES_MD="$TMP_DIR/rules.md"
> "$RULES_MD"
for page in "${PAGES[@]}"; do
  f="$ROOT_DIR/$page"
  [ -f "$f" ] && sed '1{/^---$/!q;};1,/^---$/d' "$f" | sed 's/{:.*}//g' >> "$RULES_MD" && echo -e "\n\n" >> "$RULES_MD"
done
echo "   Markdown → HTML..."
pandoc "$RULES_MD" -f markdown -t html5 --toc --toc-depth=2 --metadata title="" -o "$TMP_DIR/rules-body.html"

# === 2. Render materiali da YAML ===
echo "   YAML → Schede + Carte..."
python3 "$SCRIPT_DIR/render_materials.py" sheets > "$TMP_DIR/sheets.html"
python3 "$SCRIPT_DIR/render_materials.py" cards  > "$TMP_DIR/cards.html"

# === 3. Assembla template ===
echo "   Assemblaggio HTML finale..."
cp "$SCRIPT_DIR/pdf-template.html" "$TMP_DIR/full.html"
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

# Split at each <h1 to create separate <section class="rules"> per chapter
# This ensures page breaks work in WeasyPrint's multi-column layout
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
weasyprint "$TMP_DIR/full.html" "$OUTPUT_DIR/anamnesia-zine.pdf" 2>&1 | grep -v "WARNING" || true

echo "✅ PDF: $OUTPUT_DIR/anamnesia-zine.pdf"
