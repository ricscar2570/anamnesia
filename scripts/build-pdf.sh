#!/bin/bash
# build-pdf.sh — Build the complete AnamnesiA PDF (Zine edition)
# Usage: LANG=en ./build-pdf.sh   or   LANG=it ./build-pdf.sh (default: it)
set -e

LANG_CODE="${LANG:-it}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$ROOT_DIR/output"
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

mkdir -p "$OUTPUT_DIR"

# === Language configuration ===
CONTENT_DIR="$ROOT_DIR/content/$LANG_CODE"
DATA_DIR="$ROOT_DIR/_data/$LANG_CODE"
TEMPLATE_DIR="$SCRIPT_DIR/templates/$LANG_CODE"

if [ ! -d "$CONTENT_DIR" ]; then
  echo "❌ Content directory not found: $CONTENT_DIR"; exit 1
fi

if [ "$LANG_CODE" = "en" ]; then
  echo "📖 Assembling Complete Edition (English)..."
  PAGES=(
    index.md pillars.md how-to-play.md the-system.md stress-and-echoes.md
    archetypes.md archetypes/the-survivor.md archetypes/the-witness.md
    archetypes/the-protector.md archetypes/the-catalyst.md
    session-zero.md memory-keeper-guide.md starting-first-cycle.md gameplay-example.md
    scenario-the-incident.md scenario-the-betrayal.md
    universal-fragments.md quick-reference.md variants.md changelog.md
  )
  YAML_ARCH="archetypes.yml"
  YAML_CARDS="fragment_cards.yml"
  OUTPUT_FILE="anamnesia-zine-en.pdf"
elif [ "$LANG_CODE" = "de" ]; then
  echo "📖 Zusammenstellung Vollständige Ausgabe (Deutsch)..."
  PAGES=(
    index.md saeulen.md spielablauf.md das-system.md stress-und-echos.md
    archetypen.md archetypen/der-ueberlebende.md archetypen/der-zeuge.md
    archetypen/der-beschuetzer.md archetypen/der-katalysator.md
    session-zero.md hueter-leitfaden.md start-erster-zyklus.md spielbeispiel.md
    szenario-der-vorfall.md szenario-der-verrat.md
    universelle-fragmente.md kurzuebersicht.md varianten.md changelog.md
  )
  YAML_ARCH="archetypen.yml"
  YAML_CARDS="fragmentkarten.yml"
  OUTPUT_FILE="anamnesia-zine-de.pdf"
elif [ "$LANG_CODE" = "es" ]; then
  echo "📖 Ensamblando Edición Completa (Español)..."
  PAGES=(
    index.md pilares.md como-se-juega.md el-sistema.md estres-y-ecos.md
    arquetipos.md arquetipos/el-superviviente.md arquetipos/el-testigo.md
    arquetipos/el-protector.md arquetipos/el-catalizador.md
    sesion-cero.md guia-del-guardian.md inicio-primer-ciclo.md ejemplo-de-juego.md
    escenario-el-incidente.md escenario-la-traicion.md
    fragmentos-universales.md referencia-rapida.md variantes.md changelog.md
  )
  YAML_ARCH="arquetipos.yml"
  YAML_CARDS="cartas_fragmento.yml"
  OUTPUT_FILE="anamnesia-zine-es.pdf"
elif [ "$LANG_CODE" = "fr" ]; then
  echo "📖 Assemblage Édition Complète (Français)..."
  PAGES=(
    index.md piliers.md comment-jouer.md le-systeme.md stress-et-echos.md
    archetypes.md archetypes/le-survivant.md archetypes/le-temoin.md
    archetypes/le-protecteur.md archetypes/le-catalyseur.md
    session-zero.md guide-du-gardien.md debut-premier-cycle.md exemple-de-jeu.md
    scenario-incident.md scenario-trahison.md
    fragments-universels.md reference-rapide.md variantes.md changelog.md
  )
  YAML_ARCH="archetypes.yml"
  YAML_CARDS="cartes_fragment.yml"
  OUTPUT_FILE="anamnesia-zine-fr.pdf"
else
  echo "📖 Assemblaggio Edizione Completa (Italiano)..."
  PAGES=(
    index.md pilastri.md come-si-gioca.md il-sistema.md stress-ed-echi.md
    archetipi.md archetipi/il-sopravvissuto.md archetipi/il-testimone.md
    archetipi/il-protettore.md archetipi/il-catalizzatore.md
    sessione-zero.md guida-custode.md avvio-primo-ciclo.md esempio-di-gioco.md
    scenario-incidente.md scenario-tradimento.md
    frammenti-universali.md riferimento-rapido.md varianti.md changelog.md
  )
  YAML_ARCH="archetipi.yml"
  YAML_CARDS="carte_frammento.yml"
  OUTPUT_FILE="anamnesia-zine-it.pdf"
fi

# === 1. Rules: Markdown → HTML ===
RULES_MD="$TMP_DIR/rules.md"
> "$RULES_MD"
for page in "${PAGES[@]}"; do
  f="$CONTENT_DIR/$page"
  [ -f "$f" ] && sed '1{/^---$/!q;};1,/^---$/d' "$f" | sed 's/{:.*}//g' >> "$RULES_MD" && echo -e "\n\n" >> "$RULES_MD"
done
echo "   Markdown → HTML..."
pandoc "$RULES_MD" -f markdown -t html5 --toc --toc-depth=2 --metadata title="" -o "$TMP_DIR/rules-body.html"

# === 2. Render materials from YAML ===
echo "   YAML → Sheets + Cards..."
ANAMNESIA_DATA_DIR="$DATA_DIR" ANAMNESIA_LANG="$LANG_CODE" \
  python3 "$SCRIPT_DIR/render_materials.py" sheets "$YAML_ARCH" > "$TMP_DIR/sheets.html"
ANAMNESIA_DATA_DIR="$DATA_DIR" ANAMNESIA_LANG="$LANG_CODE" \
  python3 "$SCRIPT_DIR/render_materials.py" cards "$YAML_CARDS" > "$TMP_DIR/cards.html"

# === 3. Assemble template ===
echo "   Assembling final HTML..."
cp "$TEMPLATE_DIR/zine.html" "$TMP_DIR/full.html"
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

parts = re.split(r'(?=<h1[ >])', rules_html)
sections = []
for i, part in enumerate(parts):
    part = part.strip()
    if not part:
        continue
    sections.append(f'<section class="rules">\n{part}\n</section>')
rules_final = '\n\n'.join(sections)

# Wrap tables in column-spanning divs (WeasyPrint needs wrapper for column-span on tables)
rules_final = re.sub(r'(<table\b.*?</table>)', r'<div class="table-span">\1</div>', rules_final, flags=re.DOTALL)

html = html.replace('<!-- TOC_PLACEHOLDER -->', toc_html)
html = html.replace('<!-- RULES_PLACEHOLDER -->', rules_final)
html = html.replace('<!-- SHEETS_PLACEHOLDER -->', sheets)
html = html.replace('<!-- CARDS_PLACEHOLDER -->', cards)
html = html.replace('CSSPATH', "$TMP_DIR/pdf-style.css")

pathlib.Path("$TMP_DIR/full.html").write_text(html)
PYEOF

# === 4. PDF ===
echo "🎨 WeasyPrint..."
weasyprint "$TMP_DIR/full.html" "$OUTPUT_DIR/$OUTPUT_FILE" 2>&1 | grep -v "WARNING" || true

echo "✅ PDF: $OUTPUT_DIR/$OUTPUT_FILE"
