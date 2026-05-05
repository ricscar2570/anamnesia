"""Deck orchestrator: full pipeline from YAML input to DTC-ready ZIP.

Usage from CLI:
    python -m cards.builders.deck --lang it
    python -m cards.builders.deck --lang en
    python -m cards.builders.deck --lang it --no-zip       # skip ZIP step
    python -m cards.builders.deck --lang en --output-dir custom/path
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import yaml
from PIL import Image
from reportlab.pdfgen.canvas import Canvas

from .theme import Theme
from .icons import render_all_icons
from .front import draw_card_front
from .back import render_backs


def _project_root() -> Path:
    """Return the absolute path of the `cards/` directory."""
    return Path(__file__).resolve().parent.parent


def _load_deck(yaml_path: Path) -> list[dict]:
    """Load and validate the deck YAML. Cards are returned in deck order."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cards = data["cards"]

    if len(cards) != 36:
        raise ValueError(f"Expected 36 cards, found {len(cards)} in {yaml_path}")
    for i, card in enumerate(cards, start=1):
        if int(card["number"]) != i:
            raise ValueError(
                f"Card at position {i} has number={card['number']!r} "
                f"(must equal its position to keep front/back pairing intact)"
            )
    return cards


def _render_pdf(
    cards: list[dict],
    theme: Theme,
    lang: str,
    icon_paths: dict[str, Path],
    pdf_path: Path,
) -> None:
    """Render all 36 fronts to a single multi-page PDF."""
    page_size = (theme.card_w_pt, theme.card_h_pt)
    c = Canvas(str(pdf_path), pagesize=page_size)
    title = "AnamnesiA - Carte Frammento" if lang == "it" else "AnamnesiA - Fragment Cards"
    c.setTitle(f"{title} ({lang.upper()})")
    c.setAuthor("Riccardo Scaringi / Temple Games")
    c.setSubject("Print-ready card fronts for DriveThruCards Euro Poker Premium")

    for card in cards:
        draw_card_front(c, card, theme, lang, icon_paths)
        c.showPage()
    c.save()


def _rasterise_pdf_to_jpgs(pdf_path: Path, jpg_dir: Path) -> list[Path]:
    """Rasterise each PDF page to an 825x1125 CMYK JPG named NNNfront.jpg.

    Requires `pdftoppm` (poppler-utils) on PATH.
    """
    jpg_dir.mkdir(parents=True, exist_ok=True)

    # Clean up previous renders so we don't keep stale files.
    for old in jpg_dir.glob("*.jpg"):
        old.unlink()

    written: list[Path] = []
    for i in range(1, 37):
        prefix = jpg_dir / f"raw_{i:03d}"
        subprocess.run(
            ["pdftoppm", "-jpeg", "-r", "300",
             "-f", str(i), "-l", str(i),
             str(pdf_path), str(prefix)],
            check=True,
        )
        raw_files = sorted(jpg_dir.glob(f"raw_{i:03d}-*.jpg"))
        if not raw_files:
            raise RuntimeError(f"pdftoppm produced no output for page {i}")
        img = Image.open(raw_files[0])
        out = jpg_dir / f"{i:03d}front.jpg"
        img.resize((825, 1125), Image.LANCZOS).convert("CMYK").save(
            out, "JPEG", quality=95
        )
        raw_files[0].unlink()
        written.append(out)
    return written


def _build_zip(deck_dir: Path, lang: str) -> Path:
    """Zip the JPG fronts + backs together for upload to DTC's DECKBUILDER."""
    zip_path = deck_dir / f"deck_{lang}_dtc.zip"
    if zip_path.exists():
        zip_path.unlink()

    files = sorted(list(deck_dir.glob("*front.jpg")) + list(deck_dir.glob("*back.jpg")))
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=f.name)
    return zip_path


def build_deck(lang: str, output_dir: Path | None = None, do_zip: bool = True) -> dict:
    """Run the full pipeline. Returns a dict of paths produced."""
    if lang not in ("it", "en"):
        raise ValueError(f"Unsupported language: {lang!r} (use 'it' or 'en')")

    root = _project_root()
    if output_dir is None:
        output_dir = root / "output" / lang
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== Building {lang.upper()} deck ===")
    print(f"Output directory: {output_dir}")

    # Load theme + deck data
    theme = Theme.load(root / "data" / "theme.yaml")
    cards = _load_deck(root / "data" / f"deck_{lang}.yaml")
    print(f"  Loaded {len(cards)} cards")

    # Render category icons (cached per build)
    icons_dir = output_dir / "_icons"
    icon_paths = render_all_icons(theme, icons_dir)
    print(f"  Generated {len(icon_paths)} icons")

    # Render fronts -> PDF
    pdf_path = output_dir / f"deck_{lang}.pdf"
    _render_pdf(cards, theme, lang, icon_paths, pdf_path)
    print(f"  Wrote PDF: {pdf_path.name}")

    # Rasterise PDF pages -> 36 JPG fronts
    jpgs_dir = output_dir / "jpgs"
    front_paths = _rasterise_pdf_to_jpgs(pdf_path, jpgs_dir)
    print(f"  Rasterised {len(front_paths)} fronts")

    # Render 36 backs from the Rorschach assets
    asset_dir = root / "assets" / "rorschach"
    back_paths = render_backs(asset_dir, jpgs_dir)
    print(f"  Generated {len(back_paths)} backs")

    # Verify pairing invariant: card N front should be in the same act as card N back.
    # (Backs are produced by act lookup, fronts by YAML order; both must agree.)
    for n in range(1, 37):
        expected_act = 1 if n <= 12 else 2 if n <= 24 else 3
        front_act = int(cards[n - 1]["act"])
        if front_act != expected_act:
            raise RuntimeError(
                f"Card {n:03d} front is in Act {front_act} but back will be Act "
                f"{expected_act}. Check {lang} YAML deck order."
            )

    result = {"pdf": pdf_path, "jpgs_dir": jpgs_dir, "fronts": front_paths, "backs": back_paths}

    if do_zip:
        zip_path = _build_zip(jpgs_dir, lang)
        print(f"  Bundled: {zip_path.relative_to(output_dir)}")
        result["zip"] = zip_path

    print("=== Done ===\n")
    return result


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Build AnamnesiA card deck for DTC.")
    parser.add_argument("--lang", required=True, choices=["it", "en"], help="Deck language")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Override output directory (default: cards/output/<lang>)")
    parser.add_argument("--no-zip", action="store_true", help="Skip the DTC ZIP step")
    args = parser.parse_args()

    try:
        build_deck(lang=args.lang, output_dir=args.output_dir, do_zip=not args.no_zip)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
