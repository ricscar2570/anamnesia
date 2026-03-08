"""
build_03.py — Riferimento Rapido / Quick Reference Card
Uso: python build_03.py <lang>
"""

import sys, os, yaml
sys.path.insert(0, os.path.dirname(__file__))
from shared import *
from reportlab.lib.units import mm

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '03.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

def build(lang):
    d    = load(lang)
    meta = d['meta']
    out  = os.path.join(OUTPUT_DIR, lang, '03_quick_reference.pdf')
    S    = make_styles()
    doc  = make_doc(out, meta['header'], meta['footer'], S)

    story = []
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(meta['title'],    S['doc_title']))
    story.append(Paragraph(meta['subtitle'], S['doc_subtitle']))
    story.append(hr_accent())
    story.append(Spacer(1, 2*mm))

    # ── Formula del tiro ──────────────────────────────────────────────────────
    rs = d['roll_section']
    story.append(Paragraph(rs['title'], S['section']))
    for step in rs['steps']:
        story.append(Paragraph(step, S['body_sm']))
    story.append(Spacer(1, 1*mm))

    cw_dice = [12*mm, 26*mm, INNER_W - 38*mm]
    story.append(simple_table(rs['dice_col_headers'], rs['dice_rows'], cw_dice, S))
    story.append(Spacer(1, 3*mm))

    # ── Esiti ─────────────────────────────────────────────────────────────────
    os_ = d['outcomes_section']
    story.append(Paragraph(os_['title'], S['section']))
    cw_out = [12*mm, 32*mm, INNER_W - 44*mm]
    story.append(simple_table(os_['col_headers'], os_['rows'], cw_out, S))
    story.append(Spacer(1, 3*mm))

    # ── Pool e Stress ─────────────────────────────────────────────────────────
    ps = d['pool_section']
    story.append(Paragraph(ps['title'], S['section']))
    story.append(box_paragraph(ps['formula'], S, 'body_sm'))
    story.append(Spacer(1, 1.5*mm))

    # Tabella Echi (compatta, 2 colonne)
    story.append(Paragraph(f'<b>{ps["echi_label"]}</b>', S['label']))
    cw_ech = [16*mm, INNER_W - 16*mm]
    story.append(simple_table(['', ''], ps['echi_rows'], cw_ech, S))
    story.append(Spacer(1, 1.5*mm))

    cw_st = [16*mm, INNER_W - 16*mm]
    story.append(simple_table(ps['stress_col_headers'], ps['stress_rows'], cw_st, S))
    story.append(Spacer(1, 3*mm))

    # ── Meccaniche speciali ────────────────────────────────────────────────────
    story.append(PageBreak())
    sp = d['special_section']
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(sp['title'], S['section']))
    for mec in sp['mechanics']:
        story.append(Paragraph(f'<b>{mec["name"]}</b>', S['label']))
        story.append(Paragraph(mec['text'], S['body_sm']))
        story.append(Spacer(1, 1*mm))
    story.append(Spacer(1, 2*mm))

    # ── Recupero Stress ───────────────────────────────────────────────────────
    rec = d['recovery_section']
    story.append(Paragraph(rec['title'], S['section']))
    for item in rec['items']:
        story.append(Paragraph(f'• {item}', S['bullet']))
    story.append(Spacer(1, 3*mm))

    # ── Generatore sensoriale ─────────────────────────────────────────────────
    sen = d['sensory_section']
    story.append(Paragraph(sen['title'], S['section']))
    cw_sen = [9*mm, 22*mm, INNER_W - 31*mm]
    story.append(simple_table(sen['col_headers'], sen['rows'], cw_sen, S))
    story.append(Spacer(1, 3*mm))

    # ── Quote finale ──────────────────────────────────────────────────────────
    story.append(hr(LIGHT_GRAY))
    story.append(Paragraph(d['closing_quote'], S['quote']))

    doc.build(story)
    print(f'  [03] {lang} -> {out}')

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    build(lang)
