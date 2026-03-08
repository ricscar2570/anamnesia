"""
build_02.py — Scheda del Custode / Memory Keeper Reference Sheet
Uso: python build_02.py <lang>
"""

import sys, os, yaml
sys.path.insert(0, os.path.dirname(__file__))
from shared import *
from reportlab.lib.units import mm
from reportlab.platypus import TableStyle

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '02.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

def build(lang):
    d    = load(lang)
    meta = d['meta']
    out  = os.path.join(OUTPUT_DIR, lang, '02_keeper_reference.pdf')
    S    = make_styles()
    doc  = make_doc(out, meta['header'], meta['footer'], S)

    story = []

    # ── Titolo ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(meta['title'],    S['doc_title']))
    story.append(Paragraph(meta['subtitle'], S['doc_subtitle']))
    story.append(hr_accent())
    story.append(Spacer(1, 2*mm))

    # ── Struttura del ciclo ───────────────────────────────────────────────────
    cyc = d['cycle_section']
    story.append(Paragraph(cyc['title'], S['section']))
    cw = [28*mm, 18*mm, INNER_W - 46*mm]
    story.append(simple_table(cyc['col_headers'], cyc['rows'], cw, S))
    story.append(Spacer(1, 3*mm))

    # ── Fasi di gioco ─────────────────────────────────────────────────────────
    ph = d['phases_section']
    story.append(Paragraph(ph['title'], S['section']))
    cw2 = [24*mm, 16*mm, 24*mm, INNER_W - 64*mm]
    story.append(simple_table(ph['col_headers'], ph['rows'], cw2, S))
    story.append(Spacer(1, 3*mm))

    # ── Domande per fase ──────────────────────────────────────────────────────
    qs = d['questions_section']
    story.append(Paragraph(qs['title'], S['section']))

    for phase_block in qs['phases']:
        story.append(Paragraph(phase_block['label'], S['subsection']))
        for q in phase_block['questions']:
            story.append(Paragraph(f'• {q}', S['bullet']))
        story.append(Spacer(1, 1*mm))

    story.append(Spacer(1, 2*mm))

    # ── Tracking sessione ─────────────────────────────────────────────────────
    story.append(PageBreak())
    tr = d['tracking_section']
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(tr['title'], S['section']))
    story.append(Spacer(1, 1*mm))

    # Riga scenario / data / giocatori
    info_style = S['body_sm']
    for lbl in [tr['scenario_label'], tr['date_label'], tr['players_label']]:
        story.append(Paragraph(
            f'<b>{lbl}</b>  ___________________________',
            info_style,
        ))
    story.append(Spacer(1, 2*mm))

    # Tabella giocatori (4 righe vuote)
    hdrs  = tr['col_headers']
    n_col = len(hdrs)
    empty_w = INNER_W / n_col
    cw3   = [empty_w] * n_col
    empty_rows = [['', '', '', '', ''][:n_col] for _ in range(4)]
    story.append(simple_table(hdrs, empty_rows, cw3, S))
    story.append(Spacer(1, 3*mm))

    # Cicli
    story.append(Paragraph(f'<b>{tr["cycles_label"]}</b>', S['label']))
    cycle_line = '   '.join(c + ' ■' for c in tr['cycles'])
    story.append(Paragraph(cycle_line, S['body_sm']))
    story.append(Spacer(1, 2*mm))

    # Safety tools
    story.append(Paragraph(f'<b>{tr["tools_label"]}</b>', S['label']))
    tools_line = '   '.join(t + ' ■' for t in tr['tools'])
    story.append(Paragraph(tools_line, S['body_sm']))
    story.append(Spacer(1, 2*mm))

    # Connessioni / Verità / Note
    for lbl in [tr['connections_label'], tr['truths_label'], tr['notes_label']]:
        story.append(Paragraph(f'<b>{lbl}</b>', S['label']))
        story.append(Paragraph('_' * 60, S['body_sm']))
        story.append(Paragraph('_' * 60, S['body_sm']))
        story.append(Spacer(1, 1*mm))

    doc.build(story)
    print(f'  [02] {lang} -> {out}')

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    build(lang)
