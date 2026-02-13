#!/usr/bin/env python3
"""
render_materials.py — Generate HTML for character sheets and fragment cards from YAML.
Supports bilingual output via environment variables:
  ANAMNESIA_DATA_DIR  — path to _data/it or _data/en
  ANAMNESIA_LANG      — 'it' or 'en' (affects labels on sheets)

Usage:
  python3 render_materials.py sheets archetypes.yml
  python3 render_materials.py cards fragment_cards.yml
  python3 render_materials.py both archetypes.yml fragment_cards.yml
"""
import yaml
import sys
import os

DATA_DIR = os.environ.get('ANAMNESIA_DATA_DIR',
                          os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_data', 'it'))
LANG = os.environ.get('ANAMNESIA_LANG', 'it')

# Bilingual labels for character sheets
LABELS = {
    'it': {
        'archetype': 'Archetipo',
        'name': 'Nome',
        'scenario': 'Scenario',
        'anchor': 'Ancora',
        'approaches': 'Approcci',
        'vulnerability': 'Vulnerabilità',
        'stress': 'Stress',
        'echoes': 'Echi Traumatici',
        'pool_calc': 'Pool Attuale',
        'pool_note': 'Penalità Echi (min 1)',
        'cycle': 'Ciclo',
        'anchor_used': 'Ancora usata',
        'last_memory': 'Ultimo Ricordo usato',
        'notes': 'Ricordi e Note',
        'echo_note': '0–2: 0 · 3–5: −1d · 6–8: −3d · 9+: fuori gioco',
        'breakdown_note': '4 = Breakdown Parziale · 5 = Breakdown Finale',
        'copyright': '© 2026 Riccardo Scaringi',
    },
    'en': {
        'archetype': 'Archetype',
        'name': 'Name',
        'scenario': 'Scenario',
        'anchor': 'Anchor',
        'approaches': 'Approaches',
        'vulnerability': 'Vulnerability',
        'stress': 'Stress',
        'echoes': 'Traumatic Echoes',
        'pool_calc': 'Current Pool',
        'pool_note': 'Echo Penalty (min 1)',
        'cycle': 'Cycle',
        'anchor_used': 'Anchor used',
        'last_memory': 'Last Memory used',
        'notes': 'Memories & Notes',
        'echo_note': '0–2: 0 · 3–5: −1d · 6–8: −3d · 9+: out of play',
        'breakdown_note': '4 = Partial Breakdown · 5 = Final Breakdown',
        'copyright': '© 2026 Riccardo Scaringi',
    }
}


def load_yaml(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def render_sheets(archetipi):
    """Generate HTML for the 4 character sheets."""
    L = LABELS[LANG]
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
    <div><div class="cs-archetype-name">{a["nome"]}</div><div class="cs-archetype-label">{L["archetype"]}</div></div>
    <div class="cs-pool-badge">Base Pool: {a["pool"]}</div>
  </div>
  <div class="cs-fields"><div class="cs-field"><div class="cs-field-label">{L["name"]}</div></div><div class="cs-field"><div class="cs-field-label">{L["scenario"]}</div></div><div class="cs-field"><div class="cs-field-label">{L["anchor"]}</div></div></div>
  <div class="cs-quote">{a["citazione"]}</div>
  <div class="cs-section-head">{L["approaches"]}</div>
{approaches_html}
{abilities_html}
  <div class="cs-vuln-box"><strong>{L["vulnerability"]}:</strong> {vuln["trigger"]} {vuln["effetto"]}<em>{vuln["domanda"]}</em></div>
  <div class="cs-trackers">
    <div class="cs-tracker-box"><div class="cs-tracker-title">{L["stress"]}</div><div class="cs-circles">{"".join(f'<span class="cs-circle">{i}</span>' for i in range(1,6))}</div><div class="cs-tracker-note">{L["breakdown_note"]}</div></div>
    <div class="cs-tracker-box"><div class="cs-tracker-title">{L["echoes"]}</div><div class="cs-circles">{"".join(f'<span class="cs-circle">{i}</span>' for i in range(1,10))}<span class="cs-circle">+</span></div><div class="cs-tracker-note">{L["echo_note"]}</div></div>
  </div>
  <div class="cs-pool-calc"><strong>{L["pool_calc"]} =</strong> {a["pool"]} − {L["stress"]} − {L["pool_note"]} · {L["cycle"]}: ①  ②  ③  ④  ⑤</div>
  <div class="cs-pool-calc"><strong>{L["anchor_used"]}:</strong> ☐ · <strong>{L["last_memory"]}:</strong> ☐</div>
  <div class="cs-notes"><div class="cs-section-head">{L["notes"]}</div></div>
  <div class="cs-footer">Anamn<span class="mr">e</span>siA · v2.0 · {L["copyright"]}</div>
</div>''')
    return '\n\n'.join(html)


def render_cards(carte_data):
    """Generate HTML for the 24 fragment cards."""
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
    if len(sys.argv) < 3:
        print("Usage: python3 render_materials.py [sheets|cards|both] <yaml_filename> [<yaml_filename2>]", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    arch_file = sys.argv[2] if len(sys.argv) > 2 else None
    cards_file = sys.argv[3] if len(sys.argv) > 3 else (sys.argv[2] if mode == 'cards' else None)

    if mode in ('sheets', 'both'):
        archetipi = load_yaml(arch_file)
        print('<!-- SHEETS_START -->')
        print(render_sheets(archetipi))
        print('<!-- SHEETS_END -->')

    if mode in ('cards', 'both'):
        carte = load_yaml(cards_file if mode == 'both' else arch_file)
        print('<!-- CARDS_START -->')
        print(render_cards(carte))
        print('<!-- CARDS_END -->')
