"""
build_01.py — Generatori di Complicazioni / Complication Generators
Uso: python build_01.py <lang>
"""

import sys, os, yaml
sys.path.insert(0, os.path.dirname(__file__))
from shared import *
from reportlab.lib.units import mm

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '01.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

def build(lang):
    d = load(lang)
    meta = d['meta']
    out  = os.path.join(OUTPUT_DIR, lang, '01_complication_generators.pdf')
    S    = make_styles()
    doc  = make_doc(out, meta['header'], meta['footer'], S)

    story = []

    # ── Titolo copertina ──────────────────────────────────────────────────────
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(meta['title'],    S['doc_title']))
    story.append(Paragraph(meta['subtitle'], S['doc_subtitle']))
    story.append(hr_accent())
    story.append(Spacer(1, 2*mm))

    # ── Introduzione ──────────────────────────────────────────────────────────
    story.append(Paragraph(d['intro'].strip(), S['body']))
    story.append(Spacer(1, 3*mm))

    # ── Immagine Rorschach centrata ───────────────────────────────────────────
    story.append(rorschach_img('rorschach_1.png', width_mm=52))
    story.append(Spacer(1, 4*mm))

    # ── Tre fasi ──────────────────────────────────────────────────────────────
    for i, phase in enumerate(d['phases']):
        if i > 0:
            story.append(PageBreak())

        story.append(Paragraph(phase['title'], S['section']))
        story.append(Paragraph(phase['subtitle'], S['subsection']))
        story.append(Spacer(1, 1*mm))

        col_w = [8*mm, INNER_W - 8*mm]
        rows  = phase['rows']
        story.append(simple_table(
            ['d6', phase['col_header']],
            rows,
            col_w, S,
        ))
        story.append(Spacer(1, 4*mm))

    # ── Quote finale ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 4*mm))
    story.append(hr(LIGHT_GRAY))
    story.append(Paragraph(d['closing_quote'], S['quote']))

    doc.build(story)
    print(f'  [01] {lang} -> {out}')

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    build(lang)
