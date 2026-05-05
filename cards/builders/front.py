"""Card-front renderer.

Draws a single card front onto a ReportLab canvas page using:
  - card data (dict from YAML)
  - theme (Theme dataclass)
  - language code ('it' or 'en')
  - icon paths (from builders.icons.render_all_icons)
"""
from __future__ import annotations

from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm

from .theme import Theme


def _wrap(c: Canvas, text: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    """Word-wrap `text` to lines that fit within `max_width`."""
    words = text.split()
    lines: list[str] = []
    cur: list[str] = []
    for w in words:
        trial = " ".join(cur + [w])
        if c.stringWidth(trial, font_name, font_size) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_card_front(
    c: Canvas,
    card: dict,
    theme: Theme,
    lang: str,
    icon_paths: dict[str, Path],
) -> None:
    """Render one card front onto the current canvas page (caller does showPage)."""
    act = int(card["act"])
    title = card["title"]
    quote = card["quote"]
    cost_label = card["cost_label"]
    cost_value = str(card["cost_value"])
    category = card["category"]
    instruction = card.get("instruction")

    ui = theme.ui[lang]
    act_label = theme.acts[act].label_it if lang == "it" else theme.acts[act].label_en
    act_color = theme.acts[act].color

    W = theme.card_w_pt
    H = theme.card_h_pt
    BLEED = theme.bleed_pt

    # 1. paper background (full bleed)
    c.setFillColor(theme.colors["paper_cream"])
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # 2. act header band
    band_h = 22 * mm
    band_top = H
    band_bot = band_top - band_h
    c.setFillColor(act_color)
    c.rect(0, band_bot, W, band_h, fill=1, stroke=0)

    # scenario tag (top of band)
    c.setFillColor(theme.colors["header_text"])
    f_name, f_size = theme.font("scenario_tag")
    c.setFont(f_name, f_size)
    c.drawCentredString(W/2, band_top - BLEED - 6, ui.scenario_label)

    # act header label
    f_name, f_size = theme.font("act_header")
    c.setFont(f_name, f_size)
    c.drawCentredString(W/2, band_bot + band_h/2 - 5, act_label)

    # 3. title (auto-shrink if too long)
    title_y = band_bot - 11 * mm
    c.setFillColor(theme.colors["title_dark"])
    f_name, t_size = theme.font("title")
    title_min = float(theme.fonts["title_min"])
    while c.stringWidth(title, f_name, t_size) > W - 14*mm and t_size > title_min:
        t_size -= 0.5
    c.setFont(f_name, t_size)
    c.drawCentredString(W/2, title_y, title)

    # divider under title
    c.setStrokeColor(theme.colors["divider"])
    c.setLineWidth(0.4)
    c.line(8*mm, title_y - 4*mm, W - 8*mm, title_y - 4*mm)

    # 4. quote (italic, sepia, with chevrons)
    quote_top = title_y - 9 * mm
    f_name, q_size = theme.font("quote")
    q_min = float(theme.fonts["quote_min"])
    quote_lines = _wrap(c, quote, f_name, q_size, W - 14*mm)
    if len(quote_lines) >= 3 and q_size > q_min:
        q_size = q_min
        quote_lines = _wrap(c, quote, f_name, q_size, W - 14*mm)
    c.setFont(f_name, q_size)
    c.setFillColor(theme.colors["quote_sepia"])
    line_h = q_size + 3
    for i, ln in enumerate(quote_lines):
        if len(quote_lines) == 1:
            txt = f"\u00ab{ln}\u00bb"
        elif i == 0:
            txt = f"\u00ab{ln}"
        elif i == len(quote_lines) - 1:
            txt = f"{ln}\u00bb"
        else:
            txt = ln
        c.drawCentredString(W/2, quote_top - i * line_h, txt)
    quote_bottom = quote_top - len(quote_lines) * line_h

    # 5. instruction (optional)
    after_quote_y = quote_bottom - 5 * mm
    if instruction:
        c.setStrokeColor(theme.colors["divider"])
        c.setLineWidth(0.2)
        c.line(15*mm, after_quote_y + 2*mm, W - 15*mm, after_quote_y + 2*mm)
        f_name, i_size = theme.font("instruction")
        i_min = float(theme.fonts["instruction_min"])
        inst_lines = _wrap(c, instruction, f_name, i_size, W - 12*mm)
        if len(inst_lines) > 3 and i_size > i_min:
            i_size = i_min
            inst_lines = _wrap(c, instruction, f_name, i_size, W - 12*mm)
        c.setFont(f_name, i_size)
        c.setFillColor(theme.colors["instruction"])
        for i, ln in enumerate(inst_lines):
            c.drawCentredString(W/2, after_quote_y - 4 - i * (i_size + 2.5), ln)
        icon_top = after_quote_y - 4 - len(inst_lines) * (i_size + 2.5) - 4
    else:
        icon_top = after_quote_y - 2

    # 6. category icon
    footer_top = BLEED + 22
    icon_space = icon_top - footer_top
    icon_pt = max(20, min(36, icon_space * 0.65))
    icon_x = W/2 - icon_pt/2
    icon_y = footer_top + (icon_space - icon_pt) / 2
    c.drawImage(str(icon_paths[category]), icon_x, icon_y,
                width=icon_pt, height=icon_pt, mask='auto')

    # 7. footer (category label + copyright)
    c.setFillColor(theme.colors["type_label"])
    f_name, f_size = theme.font("type_label")
    c.setFont(f_name, f_size)
    c.drawString(BLEED + 4, BLEED + 14, category)

    c.setFillColor(theme.colors["copyright"])
    f_name, f_size = theme.font("copyright")
    c.setFont(f_name, f_size)
    c.drawCentredString(W/2, BLEED + 5, ui.copyright)

    # 8. cost badge (bottom-right)
    badge_r = theme.badge.radius_mm * mm
    badge_cx = W - BLEED - badge_r - 3
    badge_cy = BLEED + theme.badge.center_offset_y_pt
    c.setFillColor(act_color)
    c.circle(badge_cx, badge_cy, badge_r, fill=1, stroke=0)
    c.setFillColor(theme.colors["cost_fg"])

    if cost_label in ("ALL", "TUTTI"):
        c.setFont("Helvetica-Bold", theme.badge.all_top_size)
        c.drawCentredString(badge_cx, badge_cy + theme.badge.all_top_offset_y, ui.cost_all_top)
        c.setFont("Helvetica", theme.badge.all_bottom_size)
        c.drawCentredString(badge_cx, badge_cy + theme.badge.all_bottom_offset_y, ui.cost_all_bottom)
    elif cost_label in ("FREE", "LIBERA"):
        c.setFont("Helvetica-Bold", theme.badge.free_label_size)
        c.drawCentredString(badge_cx, badge_cy + theme.badge.label_offset_y, ui.cost_free)
        c.setFont("Helvetica-Bold", theme.badge.cost_value_size)
        c.drawCentredString(badge_cx, badge_cy + theme.badge.value_offset_y, cost_value)
    else:  # FRAG. / FRAM.
        c.setFont("Helvetica", theme.badge.cost_label_size)
        c.drawCentredString(badge_cx, badge_cy + theme.badge.label_offset_y, ui.cost_frag)
        c.setFont("Helvetica-Bold", theme.badge.cost_value_size)
        c.drawCentredString(badge_cx, badge_cy + theme.badge.value_offset_y, cost_value)
