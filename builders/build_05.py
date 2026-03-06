"""
build_05.py — Note di Design / Design Notes
Uso: python build_05.py <lang>
"""

import sys, os, yaml
sys.path.insert(0, os.path.dirname(__file__))
from shared import *
from reportlab.lib.units import mm

def load(lang):
    p = os.path.join(BUILD_DIR, 'content', lang, '05.yaml')
    with open(p, encoding='utf-8') as f:
        return yaml.safe_load(f)

def build(lang):
    d    = load(lang)
    meta = d['meta']
    out  = os.path.join(OUTPUT_DIR, lang, '05_design_notes.pdf')
    S    = make_styles()
    doc  = make_doc(out, meta['header'], meta['footer'], S)

    story = []

    # ── Copertina ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(meta['title'],    S['doc_title']))
    story.append(Paragraph(meta['subtitle'], S['doc_subtitle']))
    story.append(hr_accent())
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph(d['opening_quote'], S['quote']))
    story.append(Spacer(1, 1*mm))
    story.append(Paragraph(d['intro'].strip(), S['body_sm']))
    story.append(Spacer(1, 3*mm))

    # ── Sezioni ───────────────────────────────────────────────────────────────
    for sec in d['sections']:
        story.append(KeepTogether([
            section_header(sec['num'], sec['title'], S),
        ]))

        # Sezione con sottosezioni (es. sezione 8 ZineQuest)
        if 'subsections' in sec:
            for sub in sec['subsections']:
                story.append(Paragraph(sub['subtitle'], S['subsection']))
                for para in sub['paragraphs']:
                    story.append(Paragraph(para.strip(), S['body']))
                story.append(Spacer(1, 1*mm))

        # Sezione con bullet list (es. sezione 9 Lezioni apprese)
        elif 'bullets' in sec:
            for b in sec['bullets']:
                story.append(Paragraph(f'• {b}', S['bullet']))
                story.append(Spacer(1, 0.5*mm))

        # Sezione standard: paragrafi
        else:
            for para in sec.get('paragraphs', []):
                story.append(Paragraph(para.strip(), S['body']))

        story.append(Spacer(1, 2*mm))

    # ── Chiusura ──────────────────────────────────────────────────────────────
    story.append(hr(LIGHT_GRAY))
    story.append(Paragraph(d['closing_quote'], S['quote']))
    story.append(Paragraph(d['closing_credit'], S['footer']))

    doc.build(story)
    print(f'  [05] {lang} -> {out}')

if __name__ == '__main__':
    lang = sys.argv[1] if len(sys.argv) > 1 else 'it'
    build(lang)
