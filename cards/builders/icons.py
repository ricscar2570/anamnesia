"""Category icon generator. Produces flat-coloured PNG glyphs.

The `Theme` knows which icon shape belongs to each category (eye, person, etc.),
so the renderer in front.py just looks up the glyph and pastes it.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

from .theme import Theme

ICON_SIZE = 256


def _cmyk_to_rgb(c) -> tuple[int, int, int]:
    """Approximate CMYK -> RGB for icon rasterisation only.

    Print fidelity does not depend on this; the final card is composed
    in CMYK by ReportLab. PIL needs RGB to draw the glyph.
    """
    r = int(255 * (1 - c.cyan)    * (1 - c.black))
    g = int(255 * (1 - c.magenta) * (1 - c.black))
    b = int(255 * (1 - c.yellow)  * (1 - c.black))
    return (r, g, b)


def _draw_shape(d: ImageDraw.ImageDraw, shape: str, fill: tuple[int, int, int, int]) -> None:
    s = ICON_SIZE
    if shape == "eye":
        d.ellipse((s*0.18, s*0.34, s*0.82, s*0.66), outline=fill, width=int(s*0.04))
        d.ellipse((s*0.42, s*0.42, s*0.58, s*0.58), fill=fill)
    elif shape == "person":
        d.ellipse((s*0.36, s*0.18, s*0.64, s*0.46), fill=fill)
        d.rounded_rectangle((s*0.24, s*0.50, s*0.76, s*0.86), radius=int(s*0.13), fill=fill)
    elif shape == "frame":
        d.rounded_rectangle((s*0.26, s*0.20, s*0.74, s*0.84), radius=int(s*0.05),
                            outline=fill, width=int(s*0.05))
        d.rectangle((s*0.45, s*0.50, s*0.62, s*0.78), fill=fill)
    elif shape == "document":
        d.polygon([(s*0.30, s*0.18), (s*0.62, s*0.18), (s*0.74, s*0.30),
                   (s*0.74, s*0.84), (s*0.30, s*0.84)], fill=fill)
        d.polygon([(s*0.62, s*0.18), (s*0.74, s*0.30), (s*0.62, s*0.30)],
                  fill=(255, 255, 255, 255))
        for yy in (0.50, 0.60, 0.70):
            d.rectangle((s*0.40, s*yy-2, s*0.66, s*yy+2), fill=(255, 255, 255, 255))
    elif shape == "magnifier":
        r = int(s*0.20)
        d.ellipse((s*0.24, s*0.20, s*0.24+2*r, s*0.20+2*r),
                  outline=fill, width=int(s*0.05))
        d.line((s*0.62, s*0.58, s*0.84, s*0.84), fill=fill, width=int(s*0.07))
        d.ellipse((s*0.40, s*0.36, s*0.52, s*0.48), fill=fill)
    elif shape == "rings":
        r = int(s*0.20)
        d.ellipse((s*0.20, s*0.30, s*0.20+2*r, s*0.30+2*r),
                  outline=fill, width=int(s*0.05))
        d.ellipse((s*0.40, s*0.30, s*0.40+2*r, s*0.30+2*r), fill=fill)
    elif shape == "speech":
        d.rounded_rectangle((s*0.18, s*0.22, s*0.82, s*0.72), radius=int(s*0.08),
                            outline=fill, width=int(s*0.05))
        d.polygon([(s*0.30, s*0.72), (s*0.30, s*0.86), (s*0.46, s*0.72)], fill=fill)
        for yy in (0.36, 0.50):
            d.rectangle((s*0.28, s*yy-2, s*0.72, s*yy+2), fill=fill)
    elif shape == "warning":
        d.polygon([(s*0.50, s*0.18), (s*0.86, s*0.82), (s*0.14, s*0.82)], fill=fill)
        d.rectangle((s*0.47, s*0.36, s*0.53, s*0.62), fill=(255, 255, 255, 255))
        d.ellipse((s*0.47, s*0.66, s*0.53, s*0.74), fill=(255, 255, 255, 255))
    elif shape == "key":
        r = int(s*0.13)
        d.ellipse((s*0.20, s*0.40, s*0.20+2*r, s*0.40+2*r),
                  outline=fill, width=int(s*0.05))
        d.ellipse((s*0.32, s*0.50, s*0.40, s*0.58), fill=fill)
        d.line((s*0.46, s*0.54, s*0.84, s*0.54), fill=fill, width=int(s*0.07))
        d.line((s*0.78, s*0.54, s*0.78, s*0.66), fill=fill, width=int(s*0.07))
    elif shape == "hourglass":
        d.polygon([(s*0.28, s*0.22), (s*0.72, s*0.22), (s*0.50, s*0.50)],
                  outline=fill, width=int(s*0.05))
        d.polygon([(s*0.50, s*0.50), (s*0.28, s*0.78), (s*0.72, s*0.78)], fill=fill)
        d.rectangle((s*0.24, s*0.18, s*0.76, s*0.24), fill=fill)
        d.rectangle((s*0.24, s*0.78, s*0.76, s*0.84), fill=fill)
    else:
        raise ValueError(f"Unknown icon shape: {shape!r}")


def make_icon(category: str, theme: Theme) -> Image.Image:
    """Return an RGBA PIL image (256x256) of the icon for `category`."""
    shape = theme.icon_shape_for_category[category]
    color = theme.categories[category]
    fill = (*_cmyk_to_rgb(color), 255)

    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    _draw_shape(d, shape, fill)
    return img


def render_all_icons(theme: Theme, out_dir: Path) -> dict[str, Path]:
    """Render every category icon as a PNG. Returns {category: path}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for category in theme.categories:
        p = out_dir / f"{category}.png"
        make_icon(category, theme).save(p)
        paths[category] = p
    return paths
