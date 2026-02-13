#!/usr/bin/env python3
"""
render_materials.py — Genera gli HTML di schede e carte dal YAML centralizzato.
Usato dallo script build-pdf.sh per popolare il template PDF.
"""
import yaml
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, '_data')


def load_yaml(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def render_sheets(archetipi):
    """Genera l'HTML delle 4 schede personaggio per il PDF."""
    html = []
    for a in archetipi:
        abilities_html = '\n'.join(
            f'  <div class="cs-ability-box"><strong>{ab["nome"]}:</strong> {ab["desc"]}</div>'
            for ab in a['abilita']
        )
        approaches_html = '\n'.join(
            f'  <div class="cs-approach"><span class="cs-approach-cost">{ap["costo"]}</span>'
            f'<strong>{ap["nome"]}</strong> — <span class="desc">{ap["desc"]}</span></div>'
            for ap in a['approcci']
        )
        vuln = a['vulnerabilita']

        html.append(f'''<div class="char-sheet">
  <div class="cs-header">
    <div><div class="cs-archetype-name">{a["nome"]}</div><div class="cs-archetype-label">Archetipo</div></div>
    <div class="cs-pool-badge">Pool Base: {a["pool"]}</div>
  </div>
  <div class="cs-fields"><div class="cs-field"><div class="cs-field-label">Nome</div></div><div class="cs-field"><div class="cs-field-label">Scenario</div></div><div class="cs-field"><div class="cs-field-label">Ancora</div></div></div>
  <div class="cs-quote">{a["citazione"]}</div>
  <div class="cs-section-head">Approcci</div>
{approaches_html}
{abilities_html}
  <div class="cs-vuln-box"><strong>Vulnerabilità:</strong> {vuln["trigger"]} {vuln["effetto"]}<em>{vuln["domanda"]}</em></div>
  <div class="cs-trackers">
    <div class="cs-tracker-box"><div class="cs-tracker-title">Stress</div><div class="cs-circles">{"".join(f'<span class="cs-circle">{i}</span>' for i in range(1,6))}</div><div class="cs-tracker-note">4 = Breakdown Parziale · 5 = Breakdown Finale</div></div>
    <div class="cs-tracker-box"><div class="cs-tracker-title">Echi Traumatici</div><div class="cs-circles">{"".join(f'<span class="cs-circle">{i}</span>' for i in range(1,10))}<span class="cs-circle">+</span></div><div class="cs-tracker-note">0–2: 0 · 3–5: −1d · 6–8: −3d · 9+: fuori gioco</div></div>
  </div>
  <div class="cs-pool-calc"><strong>Pool Attuale =</strong> {a["pool"]} − Stress − Penalità Echi (min 1) · Ciclo: ①  ②  ③  ④  ⑤</div>
  <div class="cs-pool-calc"><strong>Ancora usata:</strong> ☐ · <strong>Ultimo Ricordo usato:</strong> ☐</div>
  <div class="cs-notes"><div class="cs-section-head">Ricordi e Note</div></div>
  <div class="cs-footer">Anamn<span class="mr">e</span>siA · v2.0 · © 2026 Riccardo Scaringi</div>
</div>''')
    return '\n\n'.join(html)


def render_cards(carte_data):
    """Genera l'HTML delle 24 carte frammento per il PDF."""
    html = []
    for atto in carte_data['atti']:
        act_id = atto['colore']
        html.append(f'<div class="act-header {act_id}">{atto["nome"]} — {atto["tema"]}</div>')
        html.append('<div class="card-grid">')
        for c in atto['carte']:
            html.append(f'''<div class="fcard {act_id}"><div class="fc-badge">{atto["nome"]} · {atto["tema"]}</div><div class="fc-title">{c["titolo"]}</div><div class="fc-flavor">{c["flavor"]}</div><div class="fc-body">{c["corpo"]}</div><div class="fc-footer"><span class="fc-cost">{c["costo"]}</span><span class="fc-type">{c["tipo"]}</span></div></div>''')
        html.append('</div>')
    return '\n'.join(html)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 render_materials.py [sheets|cards|both]", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    archetipi = load_yaml('archetipi.yml')
    carte = load_yaml('carte_frammento.yml')

    if mode in ('sheets', 'both'):
        print('<!-- SHEETS_START -->')
        print(render_sheets(archetipi))
        print('<!-- SHEETS_END -->')

    if mode in ('cards', 'both'):
        print('<!-- CARDS_START -->')
        print(render_cards(carte))
        print('<!-- CARDS_END -->')
