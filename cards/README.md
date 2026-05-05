# AnamnesiA Card Deck Builder

This subproject generates the **Fragment Card Deck** for AnamnesiA in print-ready
form for **DriveThruCards** (Euro Poker Premium, double-sided, 36 cards).

It is a standalone build pipeline within the AnamnesiA repository: data-driven,
reproducible, and language-agnostic. To regenerate either the Italian or
English deck, edit a YAML file and run a single script.

## Project layout

```
cards/
├── data/
│   ├── theme.yaml           Visual theme (CMYK colours, fonts, layout)
│   ├── deck_it.yaml         36 Italian cards
│   └── deck_en.yaml         36 English cards
├── assets/
│   └── rorschach/           3 Rorschach images for card backs
│       ├── back_atto_I.png
│       ├── back_atto_II.png
│       └── back_atto_III.png
├── builders/
│   ├── theme.py             YAML theme loader
│   ├── icons.py             Per-category PNG icon generator
│   ├── front.py             Card-front renderer
│   ├── back.py              Card-backs assembler
│   └── deck.py              Pipeline orchestrator (CLI entry)
├── scripts/
│   ├── build_it.sh          Build Italian deck
│   ├── build_en.sh          Build English deck
│   └── build_all.sh         Build both
├── output/                  Generated artifacts (gitignored)
└── requirements.txt
```

## How to build a deck

### 1. Install dependencies

```bash
pip install -r cards/requirements.txt
```

`pdftoppm` (from `poppler-utils`) is required for PDF rasterisation:

```bash
# Debian/Ubuntu
sudo apt-get install poppler-utils

# macOS (Homebrew)
brew install poppler
```

### 2. Run a build

From the repository root:

```bash
bash cards/scripts/build_it.sh    # Italian only
bash cards/scripts/build_en.sh    # English only
bash cards/scripts/build_all.sh   # both
```

Or call the orchestrator module directly:

```bash
python -m cards.builders.deck --lang it
python -m cards.builders.deck --lang en
```

### 3. Outputs

Each build writes to `cards/output/<lang>/`:

- `deck_<lang>.pdf` - 36-page master PDF (one card per page, full bleed CMYK)
- `jpgs/NNNfront.jpg` - 36 individual front JPGs (825x1125 CMYK)
- `jpgs/NNNback.jpg` - 36 individual back JPGs (825x1125 CMYK)
- `jpgs/deck_<lang>_dtc.zip` - all 72 JPGs zipped, ready to upload to DTC

## How to edit content

### Change a card text or category

Open `cards/data/deck_it.yaml` (or `deck_en.yaml`) and edit the entry. Each card
is a single YAML object:

```yaml
- { number: 7,  act: 1, title: "Specchio Incrinato",
    quote: "Qualcuno l'ha colpito con forza.",
    cost_label: "FRAM.",  cost_value: "1", category: "SENSORIALE" }
```

Rules to keep the build valid:

- `number` must equal the position of the card in the list (1..36).
- `act` 1, 2, or 3 must follow the act partition: cards 1-12 must be Act 1,
  cards 13-24 must be Act 2, cards 25-36 must be Act 3. The pipeline aborts if
  this is violated, because the card backs are paired by act.
- `category` must be one of the keys defined in `theme.yaml` (Italian set for
  `deck_it.yaml`, English set for `deck_en.yaml`).
- `cost_label` is one of `FRAM.` / `LIBERA` / `TUTTI` (Italian) or
  `FRAG.` / `FREE` / `ALL` (English).

Then run `bash cards/scripts/build_<lang>.sh`.

### Change colours, fonts, or layout

Open `cards/data/theme.yaml`. Every visual parameter is there: act colours,
category icon colours, font sizes, badge spacing, paper background. Changes
apply to both languages because both decks share the same theme.

### Replace a card-back image

Drop a new file into `cards/assets/rorschach/` keeping the filename
(`back_atto_I.png`, `back_atto_II.png`, `back_atto_III.png`). The image will be
resized to 825x1125 and converted to CMYK at build time.

## How to add a new language

1. Copy `data/deck_en.yaml` to `data/deck_xx.yaml` (e.g. `deck_es.yaml`).
2. Translate every card's `title`, `quote`, and (where present) `instruction`.
3. Add `xx:` UI strings to `theme.yaml` under `ui_strings:` (scenario label,
   cost labels, copyright).
4. Add `xx` to the `acts:` labels in `theme.yaml` (`label_xx:`).
5. Edit `builders/front.py` to handle the new language code (currently
   `it` and `en` are hard-coded in the act-label lookup).
6. Either copy `scripts/build_en.sh` to `scripts/build_xx.sh` or just call
   `python -m cards.builders.deck --lang xx`.

## Front/back pairing on DriveThruCards

The pipeline produces JPGs named `NNNfront.jpg` and `NNNback.jpg` so DTC can
auto-pair them by sequence. **DTC pairs by upload order, not by filename.**
Always upload fronts in numerical order, then backs in numerical order, then
verify pairings on the **Step 5 - Assemble My Deck** screen before ordering
the proof.

The pipeline guarantees that fronts and backs of the same card number share
the same act (Act I for cards 1-12, Act II for 13-24, Act III for 25-36), so
the only thing that can go wrong is the upload order.

## Continuous integration

Every push that touches `cards/**` triggers `.github/workflows/build-cards.yml`,
which builds both decks in parallel and uploads `deck_it.pdf`, `deck_en.pdf`,
and the two DTC ZIPs as workflow artifacts. Download them from the run page
on GitHub Actions when the build is green.

## Specifications

- **Format**: DriveThruCards Euro Poker Premium, double-sided, low-gloss UV
- **Dimensions**: 69.4 x 94.4 mm including 3.2 mm bleed on each edge
- **Resolution**: 300 DPI (825 x 1125 px raster output)
- **Colour space**: CMYK
- **Page count**: 36 cards per deck
