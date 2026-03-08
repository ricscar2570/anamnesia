"""
build_06.py — The Lethe Infection
Uso: python build_06.py <lang>
Layout: 4 immagini Rorschach intercalate, tabelle sistemi, tabelle d10.
"""

import sys, os, yaml
sys.path.insert(0, os.path.dirname(__file__))
from shared import *
from reportlab.lib.units import mm
from reportlab.platypus import TableStyle as TS

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '06.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

def two_col_choice_table(choice_data, S):
    """Tabella Accettazione / Rifiuto a due colonne."""
    hdrs = choice_data['col_headers']
    rows_raw = choice_data['rows']
    half = INNER_W / 2

    # header row
    data = [[
        Paragraph(hdrs[0], S['table_hdr']),
        Paragraph(hdrs[1], S['table_hdr']),
    ]]
    # content row
    data.append([
        Paragraph(rows_raw[0].strip(), S['table_cell']),
        Paragraph(rows_raw[1].strip(), S['table_cell']),
    ])

    ts = TS([
        ('BACKGROUND',    (0,0), (-1,0),  TABLE_DARK),
        ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
        ('FONTNAME',      (0,0), (-1,0),  SERIF_B),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
        ('BACKGROUND',    (0,1), (0,1),   TABLE_ALT),
        ('BACKGROUND',    (1,1), (1,1),   WHITE),
        ('GRID',          (0,0), (-1,-1), 0.3, LIGHT_GRAY),
        ('LINEBELOW',     (0,0), (-1,0),  1.0, ACCENT),
        ('LINEBEFORE',    (1,0), (1,-1),  0.5, ACCENT),
    ])
    t = Table(data, colWidths=[half, half])
    t.setStyle(ts)
    return t

def system_table(sys_data, S):
    """Tabella per integrazione sistema: acceptance/denial rows."""
    hdrs = sys_data['col_headers']   # ['', 'Effetto', 'Risultato'] o sim.
    rows = sys_data['rows']
    n    = len(hdrs)
    if n == 3:
        cw = [24*mm, 34*mm, INNER_W - 58*mm]
    else:
        cw = [INNER_W / n] * n
    return simple_table(hdrs, rows, cw, S)

def d10_table(tbl_data, S):
    """Tabella d10 per le spark tables."""
    cw = [9*mm, INNER_W - 9*mm]
    rows = tbl_data['rows']
    return simple_table(['d10', tbl_data['col_header']], rows, cw, S)

# Immagini Rorschach per doc 06 (nell'ordine stabilito)
RORO = ['rorschach_1.png', 'rorschach_3.png', 'rorschach_2.png', 'rorschach_cthulhu.png']

def build(lang):
    d    = load(lang)
    meta = d['meta']
    out  = os.path.join(OUTPUT_DIR, lang, '06_lethe_infection.pdf')
    S    = make_styles()
    doc  = make_doc(out, meta['header'], meta['footer'], S)

    story = []
    roro_idx = 0   # indice immagine corrente

    # ── Copertina ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(meta['title'],    S['doc_title']))
    story.append(Paragraph(meta['subtitle'], S['doc_subtitle']))
    story.append(hr_accent())
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(d['opening_quote'].strip(), S['quote']))
    story.append(Spacer(1, 2*mm))

    # Prima immagine
    story.append(rorschach_img(RORO[roro_idx], width_mm=48))
    roro_idx += 1
    story.append(Spacer(1, 3*mm))

    # Intro
    for para in d['intro']['paragraphs']:
        story.append(Paragraph(para.strip(), S['body']))
    story.append(Spacer(1, 2*mm))

    # ── Sezioni ───────────────────────────────────────────────────────────────
    for i, sec in enumerate(d['sections']):
        story.append(section_header(sec['num'], sec['title'], S))

        # Sezione 1: Vettore (paragrafi + bullets + chiusura)
        if 'bullets' in sec and 'paragraphs' in sec:
            for para in sec['paragraphs']:
                story.append(Paragraph(para.strip(), S['body']))
            for b in sec['bullets']:
                story.append(Paragraph(f'• {b}', S['bullet']))
            if 'closing' in sec:
                story.append(Spacer(1, 1*mm))
                story.append(box_paragraph(sec['closing'].strip(), S, 'body_sm'))

        # Sezione 2: Regola d'Oro (paragrafi + tabella scelta + nota veto)
        elif 'choice_table' in sec:
            for para in sec['paragraphs']:
                story.append(Paragraph(para.strip(), S['body']))
            story.append(Spacer(1, 1*mm))
            story.append(two_col_choice_table(sec['choice_table'], S))
            story.append(Spacer(1, 1*mm))
            story.append(Paragraph(
                f'<i>{sec["veto_note"].strip()}</i>', S['body_sm']
            ))

        # Sezione 3: Integrazioni di sistema
        elif 'systems' in sec:
            # Seconda immagine Rorschach prima delle integrazioni
            story.append(Spacer(1, 2*mm))
            if roro_idx < len(RORO):
                story.append(rorschach_img(RORO[roro_idx], width_mm=44))
                roro_idx += 1
            story.append(Spacer(1, 3*mm))
            story.append(PageBreak())
            story.append(Spacer(1, 3*mm))
            story.append(section_header(sec['num'], sec['title'], S))

            for sys_item in sec['systems']:
                story.append(Paragraph(sys_item['name'], S['subsection']))
                story.append(Paragraph(sys_item['intro'].strip(), S['body_sm']))
                story.append(Spacer(1, 1*mm))
                story.append(system_table(sys_item, S))
                story.append(Spacer(1, 3*mm))
            continue

        # Sezione 4: Tabelle mnemoniche
        elif 'tables' in sec:
            story.append(Paragraph(sec['intro'].strip(), S['body_sm']))
            story.append(Spacer(1, 2*mm))

            for j, tbl in enumerate(sec['tables']):
                # Immagine Rorschach prima di ogni tabella (da 3a in poi)
                if roro_idx < len(RORO):
                    story.append(rorschach_img(RORO[roro_idx], width_mm=40))
                    roro_idx += 1
                    story.append(Spacer(1, 2*mm))

                story.append(Paragraph(tbl['name'], S['subsection']))
                story.append(Paragraph(
                    f'<i>{tbl["context"]}</i>', S['body_sm']
                ))
                story.append(Spacer(1, 1*mm))
                story.append(d10_table(tbl, S))
                if j < len(sec['tables']) - 1:
                    story.append(Spacer(1, 3*mm))

        # Sezione 5: Velo (solo paragrafi)
        else:
            for para in sec.get('paragraphs', []):
                story.append(Paragraph(para.strip(), S['body']))

        story.append(Spacer(1, 2*mm))

    # ── Licenze ───────────────────────────────────────────────────────────────
    story.append(hr(LIGHT_GRAY))
    for lic in d.get('licenses', []):
        story.append(Paragraph(lic.strip(), S['body_sm']))
        story.append(Spacer(1, 1*mm))

    story.append(hr(LIGHT_GRAY))
    story.append(Paragraph(d['closing_quote'], S['quote']))
    story.append(Paragraph(d['closing_credit'], S['footer']))

    doc.build(story)
    print(f'  [06] {lang} -> {out}')

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    build(lang)
