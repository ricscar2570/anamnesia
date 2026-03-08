"""
shared.py — stili, colori, header/footer comuni a tutti i builder AnamnesiA.
Importato da ogni build_XX.py.
"""

import os
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak, Image,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ── DIRECTORY ────────────────────────────────────────────────────────────────

BUILD_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BUILD_DIR, 'assets')
OUTPUT_DIR = os.path.join(BUILD_DIR, 'output')
FONTS_DIR  = os.path.join(ASSETS_DIR, 'fonts')

# ── DIMENSIONI PAGINA A5 ──────────────────────────────────────────────────────

W, H = A5          # 148 × 210 mm
M    = 14 * mm     # margine esterno
INNER_W = W - 2 * M

# ── PALETTE ───────────────────────────────────────────────────────────────────

INK        = colors.HexColor('#1a1a1a')
DARK_GRAY  = colors.HexColor('#3a3a3a')
MID_GRAY   = colors.HexColor('#888888')
LIGHT_GRAY = colors.HexColor('#cccccc')
ACCENT     = colors.HexColor('#8b1a1a')   # rosso scuro AnamnesiA
PAPER      = colors.HexColor('#faf8f4')
PAPER_ALT  = colors.HexColor('#f2ede4')
TABLE_DARK = colors.HexColor('#2c2c2c')
TABLE_ALT  = colors.HexColor('#ece8e0')
WHITE      = colors.white

# ── FONT ──────────────────────────────────────────────────────────────────────
# Lora (Google Fonts, estratto da variable font) per tutto il testo serif.
# Registriamo la famiglia completa (Regular/Bold/Italic/BoldItalic) affinché
# reportlab risolva correttamente i tag <b> e <i> nel markup interno.

pdfmetrics.registerFont(TTFont('Lora',   os.path.join(FONTS_DIR, 'LoraRegular.ttf')))
pdfmetrics.registerFont(TTFont('LoraB',  os.path.join(FONTS_DIR, 'LoraBold.ttf')))
pdfmetrics.registerFont(TTFont('LoraI',  os.path.join(FONTS_DIR, 'LoraItalic.ttf')))
pdfmetrics.registerFont(TTFont('LoraBI', os.path.join(FONTS_DIR, 'LoraBoldItalic.ttf')))

registerFontFamily(
    'Lora',
    normal    = 'Lora',
    bold      = 'LoraB',
    italic    = 'LoraI',
    boldItalic= 'LoraBI',
)

SERIF   = 'Lora'
SERIF_B = 'LoraB'
SERIF_I = 'LoraI'

# ── STILI ─────────────────────────────────────────────────────────────────────

def make_styles():
    S = {}

    S['header'] = ParagraphStyle('header',
        fontName=SERIF, fontSize=6.5, textColor=MID_GRAY,
        alignment=TA_CENTER, spaceAfter=0, spaceBefore=0,
        letterSpacing=2.5,
    )
    S['footer'] = ParagraphStyle('footer',
        fontName=SERIF_I, fontSize=6, textColor=MID_GRAY,
        alignment=TA_CENTER, spaceAfter=0, spaceBefore=0,
    )
    S['doc_title'] = ParagraphStyle('doc_title',
        fontName=SERIF_B, fontSize=22, textColor=INK,
        alignment=TA_CENTER, spaceAfter=4*mm, spaceBefore=4*mm,
        leading=26,
    )
    S['doc_subtitle'] = ParagraphStyle('doc_subtitle',
        fontName=SERIF_I, fontSize=10, textColor=DARK_GRAY,
        alignment=TA_CENTER, spaceAfter=3*mm, spaceBefore=0,
    )
    S['quote'] = ParagraphStyle('quote',
        fontName=SERIF_I, fontSize=9.5, textColor=ACCENT,
        alignment=TA_CENTER, spaceAfter=4*mm, spaceBefore=2*mm,
        leading=14, leftIndent=8*mm, rightIndent=8*mm,
    )
    S['section'] = ParagraphStyle('section',
        fontName=SERIF_B, fontSize=12, textColor=ACCENT,
        alignment=TA_LEFT, spaceAfter=2*mm, spaceBefore=4*mm,
        leading=15,
    )
    S['subsection'] = ParagraphStyle('subsection',
        fontName=SERIF_I, fontSize=10, textColor=ACCENT,
        alignment=TA_LEFT, spaceAfter=1.5*mm, spaceBefore=2.5*mm,
    )
    S['body'] = ParagraphStyle('body',
        fontName=SERIF, fontSize=9, textColor=INK,
        alignment=TA_JUSTIFY, spaceAfter=2*mm, spaceBefore=0,
        leading=13,
    )
    S['body_sm'] = ParagraphStyle('body_sm',
        fontName=SERIF, fontSize=8.2, textColor=INK,
        alignment=TA_JUSTIFY, spaceAfter=1.5*mm, spaceBefore=0,
        leading=12,
    )
    S['bullet'] = ParagraphStyle('bullet',
        fontName=SERIF, fontSize=8.5, textColor=INK,
        alignment=TA_LEFT, spaceAfter=1*mm, spaceBefore=0,
        leading=12, leftIndent=4*mm, firstLineIndent=0,
    )
    S['table_hdr'] = ParagraphStyle('table_hdr',
        fontName=SERIF_B, fontSize=8.5, textColor=WHITE,
        alignment=TA_CENTER,
    )
    S['table_hdr_left'] = ParagraphStyle('table_hdr_left',
        fontName=SERIF_B, fontSize=8.5, textColor=WHITE,
        alignment=TA_LEFT,
    )
    S['table_cell'] = ParagraphStyle('table_cell',
        fontName=SERIF, fontSize=8, textColor=INK,
        alignment=TA_LEFT, leading=11,
    )
    S['table_cell_it'] = ParagraphStyle('table_cell_it',
        fontName=SERIF_I, fontSize=8, textColor=INK,
        alignment=TA_LEFT, leading=11,
    )
    S['table_num'] = ParagraphStyle('table_num',
        fontName=SERIF_B, fontSize=9, textColor=WHITE,
        alignment=TA_CENTER,
    )
    S['label'] = ParagraphStyle('label',
        fontName=SERIF_B, fontSize=7.5, textColor=ACCENT,
        alignment=TA_LEFT, spaceAfter=0.5*mm, spaceBefore=1*mm,
        letterSpacing=0.8,
    )
    S['mono'] = ParagraphStyle('mono',
        fontName='Courier', fontSize=7.5, textColor=INK,
        alignment=TA_LEFT, leading=11,
    )
    return S


# ── HEADER / FOOTER ───────────────────────────────────────────────────────────

def make_page_template(doc, header_text, footer_text, S):
    """Restituisce un PageTemplate con header e footer fissi."""

    def on_page(canvas, doc):
        canvas.saveState()
        # header
        canvas.setFont(SERIF, 6.5)
        canvas.setFillColor(MID_GRAY)
        canvas.drawCentredString(W / 2, H - 8*mm, header_text)
        canvas.setStrokeColor(LIGHT_GRAY)
        canvas.setLineWidth(0.4)
        canvas.line(M, H - 9*mm, W - M, H - 9*mm)
        # footer
        canvas.setFont(SERIF_I, 6)
        canvas.drawCentredString(W / 2, 6*mm, footer_text)
        canvas.setLineWidth(0.3)
        canvas.line(M, 8.5*mm, W - M, 8.5*mm)
        canvas.restoreState()

    frame = Frame(M, 11*mm, INNER_W, H - 22*mm, id='main',
                  leftPadding=0, rightPadding=0,
                  topPadding=2*mm, bottomPadding=0)
    return PageTemplate(id='main', frames=[frame], onPage=on_page)


# ── HELPER: LINEA SEPARATORE ──────────────────────────────────────────────────

def hr(color=LIGHT_GRAY, thickness=0.5):
    return HRFlowable(width='100%', thickness=thickness,
                      color=color, spaceAfter=2*mm, spaceBefore=0)

def hr_accent(thickness=1.0):
    return HRFlowable(width='100%', thickness=thickness,
                      color=ACCENT, spaceAfter=2*mm, spaceBefore=0)


# ── HELPER: IMMAGINE RORSCHACH ────────────────────────────────────────────────

def rorschach_img(filename, width_mm=44):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return Spacer(1, 1*mm)
    w_pt = width_mm * mm
    img  = Image(path, width=w_pt, height=w_pt * 0.76)
    img.hAlign = 'CENTER'
    t = Table([[img]], colWidths=[w_pt + 8*mm])
    t.setStyle(TableStyle([
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('BOX',           (0,0), (-1,-1), 0.8, DARK_GRAY),
        ('BACKGROUND',    (0,0), (-1,-1), PAPER_ALT),
    ]))
    t.hAlign = 'CENTER'
    return t


# ── HELPER: TABELLA GENERICA ──────────────────────────────────────────────────

def simple_table(header_row, data_rows, col_widths, S, italic_content=False):
    """
    header_row: lista di stringhe per l'intestazione
    data_rows:  lista di liste di stringhe
    col_widths: lista di larghezze in pt
    """
    cell_style = S['table_cell_it'] if italic_content else S['table_cell']
    data = [[Paragraph(h, S['table_hdr']) for h in header_row]]
    for i, row in enumerate(data_rows):
        bg = TABLE_ALT if i % 2 == 0 else WHITE
        cells = []
        for j, cell in enumerate(row):
            st = S['table_num'] if j == 0 and len(row) > 1 and str(cell).isdigit() else cell_style
            cells.append(Paragraph(str(cell), st))
        data.append(cells)

    ts = TableStyle([
        ('BACKGROUND',    (0, 0), (-1,  0),  TABLE_DARK),
        ('FONTNAME',      (0, 0), (-1,  0),  SERIF_B),
        ('TEXTCOLOR',     (0, 0), (-1,  0),  WHITE),
        ('ALIGN',         (0, 0), (-1, -1),  'LEFT'),
        ('ALIGN',         (0, 0), ( 0, -1),  'CENTER'),
        ('VALIGN',        (0, 0), (-1, -1),  'TOP'),
        ('TOPPADDING',    (0, 0), (-1, -1),  4),
        ('BOTTOMPADDING', (0, 0), (-1, -1),  4),
        ('LEFTPADDING',   (0, 0), (-1, -1),  5),
        ('RIGHTPADDING',  (0, 0), (-1, -1),  5),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1),  [TABLE_ALT, WHITE]),
        ('GRID',          (0, 0), (-1, -1),  0.3, LIGHT_GRAY),
        ('LINEBELOW',     (0, 0), (-1,  0),  1.0, ACCENT),
    ])
    # prima colonna bold + sfondo scuro se è numerica
    for i, row in enumerate(data_rows, 1):
        if len(row) > 1 and str(row[0]).isdigit():
            ts.add('BACKGROUND', (0, i), (0, i), TABLE_DARK)
            ts.add('TEXTCOLOR',  (0, i), (0, i), WHITE)
            ts.add('FONTNAME',   (0, i), (0, i), SERIF_B)
            ts.add('ALIGN',      (0, i), (0, i), 'CENTER')

    t = Table(data, colWidths=col_widths)
    t.setStyle(ts)
    return t


# ── HELPER: BOX EVIDENZIATO ───────────────────────────────────────────────────

def box_paragraph(text, S, style_key='body_sm', bg=PAPER_ALT, border=ACCENT):
    """Paragrafo in un riquadro colorato."""
    p = Paragraph(text, S[style_key])
    t = Table([[p]], colWidths=[INNER_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('BOX',           (0,0), (-1,-1), 0.8, border),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
    ]))
    return t


# ── HELPER: SEZIONE NUMERATA ──────────────────────────────────────────────────

def section_header(num, title, S):
    return Paragraph(f'{num}. {title.upper()}', S['section'])


# ── COSTRUTTORE DOCUMENTO ─────────────────────────────────────────────────────

def make_doc(output_path, header_text, footer_text, S):
    """Crea e restituisce un BaseDocTemplate con PageTemplate già configurato."""
    doc = BaseDocTemplate(
        output_path,
        pagesize=A5,
        leftMargin=M, rightMargin=M,
        topMargin=12*mm, bottomMargin=12*mm,
        title=header_text,
    )
    pt = make_page_template(doc, header_text, footer_text, S)
    doc.addPageTemplates([pt])
    return doc
