"""Backs assembler.

Takes the 3 Rorschach images (one per act) from `assets/rorschach/` and writes
36 numbered JPGs at DriveThruCards' Euro Poker target resolution (825x1125 CMYK).

The numbering matches the front order: cards 1-12 use Rorschach Act I,
13-24 use Rorschach Act II, 25-36 use Rorschach Act III.

This pairing is invariant: it is the contract that front.py and back.py share,
so the assembled deck always has matching front/back acts.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image

DTC_W = 825
DTC_H = 1125
JPEG_QUALITY = 95

# Cards 1-12 -> Act I, 13-24 -> Act II, 25-36 -> Act III
CARD_TO_ACT = {n: (1 if n <= 12 else 2 if n <= 24 else 3) for n in range(1, 37)}


def _prepare_back(src_path: Path) -> Image.Image:
    """Load a Rorschach source PNG, resize to DTC dimensions, convert to CMYK."""
    img = Image.open(src_path)
    img = img.resize((DTC_W, DTC_H), Image.LANCZOS)
    if img.mode in ("RGBA", "LA"):
        # Flatten transparency on the dark Rorschach background.
        bg = Image.new("RGB", img.size, (45, 45, 50))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    return img.convert("CMYK")


def render_backs(asset_dir: Path, out_dir: Path) -> list[Path]:
    """Generate 36 back JPGs in `out_dir`. Returns list of written paths."""
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load and pre-process the 3 source Rorschach images (one per act).
    sources = {
        1: asset_dir / "back_atto_I.png",
        2: asset_dir / "back_atto_II.png",
        3: asset_dir / "back_atto_III.png",
    }
    for act, p in sources.items():
        if not p.exists():
            raise FileNotFoundError(f"Missing Rorschach asset for Act {act}: {p}")

    processed = {act: _prepare_back(path) for act, path in sources.items()}

    written: list[Path] = []
    for n in range(1, 37):
        act = CARD_TO_ACT[n]
        out_path = out_dir / f"{n:03d}back.jpg"
        processed[act].save(out_path, "JPEG", quality=JPEG_QUALITY)
        written.append(out_path)

    return written
