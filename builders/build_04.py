"""
build_04.py — Schede Personaggio / Character Sheets
Uso: python build_04.py <lang>
Genera una pagina per ogni Archetipo (4 pagine totali).
"""

import sys, os, yaml
sys.path.insert(0, os.path.dirname(__file__))
from shared import *
from reportlab.lib.units import mm
from reportlab.platypus import TableStyle

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '04.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

def _field(label, S, line_len=45):
    """Riga campo compilabile: LABEL  _______"""
    return Paragraph(
        f'<b>{label}</b>  {"_" * line_len}',
        S['body_sm'],
    )

def _checkbox_row(items, S):
    """Riga di checkbox: ■ item1   ■ item2 ..."""
    txt = '   '.join(f'■  {it}' for it in items)
    return Paragraph(txt, S['body_sm'])

def _track_row(label, boxes, S):
    """Riga tracciamento: LABEL  ■ 1  ■ 2  ■ 3 ..."""
    box_str = '   '.join(f'■ {b}' for b in boxes)
    return Paragraph(f'<b>{label}</b>   {box_str}', S['body_sm'])

def archetype_page(arch, lbl, S):
    """Restituisce una lista di flowable per una scheda archetipo."""
    elems = []

    # Intestazione archetipo
    elems.append(Spacer(1, 2*mm))
    elems.append(Paragraph(arch['name'], S['doc_title']))
    elems.append(Paragraph(arch['quote'], S['quote']))
    elems.append(hr_accent())
    elems.append(Spacer(1, 1*mm))

    # Campi nome / scenario / ancora
    elems.append(_field(lbl['name'],     S, 30))
    elems.append(_field(lbl['scenario'], S, 28))
    elems.append(_field(lbl['anchor'],   S, 30))
    elems.append(Spacer(1, 1*mm))
    elems.append(hr())

    # Biografia
    if arch.get('bio'):
        elems.append(Paragraph(arch['bio'].strip(), S['body_sm']))
        elems.append(Spacer(1, 1*mm))

    # Approcci
    elems.append(Paragraph(lbl['approaches'], S['label']))
    cw_ap = [18*mm, INNER_W - 18*mm]
    ap_rows = [
        [f'{a["cost"]}', a['name'] + ' — ' + a['desc']]
        for a in arch['approaches']
    ]
    elems.append(simple_table(
        [lbl['approach_cost_col'], lbl['approach_name_col']],
        ap_rows, cw_ap, S,
    ))
    elems.append(Spacer(1, 2*mm))

    # Abilità principale
    elems.append(Paragraph(arch['ability_name'], S['label']))
    elems.append(box_paragraph(arch['ability_text'].strip(), S, 'body_sm'))
    elems.append(Spacer(1, 1*mm))

    # Abilità speciale (solo Catalizzatore)
    if arch.get('special_ability_name'):
        elems.append(Paragraph(arch['special_ability_name'], S['label']))
        elems.append(box_paragraph(arch['special_ability_text'].strip(), S, 'body_sm'))
        elems.append(Spacer(1, 1*mm))

    # Vulnerabilità
    elems.append(Paragraph(lbl['vulnerability'], S['label']))
    elems.append(Paragraph(
        f'<i>{arch["vulnerability"]}</i>  →  {arch["vulnerability_reward"]}',
        S['body_sm'],
    ))
    elems.append(Spacer(1, 1*mm))
    elems.append(hr())

    # Domanda chiave
    elems.append(Paragraph(arch['key_question'], S['quote']))
    elems.append(hr())

    # Tracciamento
    elems.append(Paragraph(lbl['tracking'], S['label']))

    pool_str = lbl['pool_formula'].format(pool=str(arch['pool']))
    elems.append(Paragraph(pool_str, S['body_sm']))
    elems.append(Spacer(1, 0.5*mm))

    # Stress track
    stress_boxes = ['1', '2', '3', '4 ●', '5 ●']
    elems.append(_track_row('STRESS', stress_boxes, S))
    # Echo track
    echo_boxes = ['1','2','3','4','5','6','7','8','9+']
    elems.append(_track_row('ECHO', echo_boxes, S))
    elems.append(Spacer(1, 0.5*mm))

    # Ciclo
    cycle_boxes = ['①','②','③','④','⑤']
    elems.append(_track_row('CYCLE', cycle_boxes, S))
    elems.append(Spacer(1, 0.5*mm))

    # Checkbox speciali (Ancora, Ultimo Ricordo, Senso di Colpa)
    cb_labels = [lbl['anchor_used'], lbl['last_memory']]
    if 'guilt_used' in arch.get('special_checkboxes', []):
        cb_labels.append(lbl['guilt_used'])
    elems.append(_checkbox_row(cb_labels, S))
    elems.append(Spacer(1, 1*mm))

    # Note
    elems.append(Paragraph(f'<b>{lbl["notes"]}</b>', S['label']))
    for _ in range(3):
        elems.append(Paragraph('_' * 62, S['body_sm']))

    return elems

def build(lang):
    d    = load(lang)
    meta = d['meta']
    lbl  = d['labels']
    out  = os.path.join(OUTPUT_DIR, lang, '04_character_sheets.pdf')
    S    = make_styles()
    doc  = make_doc(out, meta['header'], meta['footer'], S)

    story = []
    for i, arch in enumerate(d['archetypes']):
        if i > 0:
            story.append(PageBreak())
        story.extend(archetype_page(arch, lbl, S))

    doc.build(story)
    print(f'  [04] {lang} -> {out}')

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    build(lang)
