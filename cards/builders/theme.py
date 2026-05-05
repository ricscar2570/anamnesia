"""Theme loader: parses theme.yaml and exposes typed access to colours, fonts, layout."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml

from reportlab.lib.colors import CMYKColor


def _cmyk(values: list[float]) -> CMYKColor:
    """Convert a [c, m, y, k] list into a ReportLab CMYKColor."""
    return CMYKColor(*values)


@dataclass
class CardSpec:
    width_mm: float
    height_mm: float
    bleed_mm: float


@dataclass
class ActSpec:
    label_it: str
    label_en: str
    color: CMYKColor


@dataclass
class BadgeSpec:
    radius_mm: float
    center_offset_y_pt: float
    cost_label_size: float
    cost_value_size: float
    label_offset_y: float
    value_offset_y: float
    free_label_size: float
    all_top_size: float
    all_bottom_size: float
    all_top_offset_y: float
    all_bottom_offset_y: float


@dataclass
class UIStrings:
    scenario_label: str
    cost_frag: str
    cost_free: str
    cost_all_top: str
    cost_all_bottom: str
    copyright: str


@dataclass
class Theme:
    card: CardSpec
    acts: dict[int, ActSpec]
    colors: dict[str, CMYKColor]
    categories: dict[str, CMYKColor]
    icon_shape_for_category: dict[str, str]
    fonts: dict[str, Any]
    badge: BadgeSpec
    ui: dict[str, UIStrings]

    @classmethod
    def load(cls, path: str | Path) -> "Theme":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        card = CardSpec(**data["card"])

        acts = {
            int(k): ActSpec(
                label_it=v["label_it"],
                label_en=v["label_en"],
                color=_cmyk(v["color_cmyk"]),
            )
            for k, v in data["acts"].items()
        }

        colors = {k: _cmyk(v) for k, v in data["colors"].items()}
        categories = {k: _cmyk(v) for k, v in data["categories"].items()}
        badge = BadgeSpec(**data["badge"])

        ui = {
            lang: UIStrings(**strings)
            for lang, strings in data["ui_strings"].items()
        }

        return cls(
            card=card,
            acts=acts,
            colors=colors,
            categories=categories,
            icon_shape_for_category=data["icon_shape_for_category"],
            fonts=data["fonts"],
            badge=badge,
            ui=ui,
        )

    # ── Convenience accessors ─────────────────────────────────────────────────
    @property
    def card_w_pt(self) -> float:
        return self.card.width_mm * 72.0 / 25.4

    @property
    def card_h_pt(self) -> float:
        return self.card.height_mm * 72.0 / 25.4

    @property
    def bleed_pt(self) -> float:
        return self.card.bleed_mm * 72.0 / 25.4

    def font(self, key: str) -> tuple[str, float]:
        spec = self.fonts[key]
        return spec[0], float(spec[1])
