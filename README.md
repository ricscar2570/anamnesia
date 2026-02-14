# AnamnesiA

**Horror Psicologico · Gioco di Ruolo Narrativo**  
**Psychological Horror · Narrative Tabletop RPG**

> *"Cosa resta quando anche le bugie svaniscono?"*  
> *"What remains when even the lies fade away?"*

A GM-less narrative RPG for 2–4 players. ZineQuest 2026.

---

## Repository Structure

```
content/
  it/          ← Italian markdown (rules, scenarios, archetypes)
  en/          ← English markdown
_data/
  it/          ← Italian YAML (character sheets, fragment cards)
  en/          ← English YAML
scripts/
  templates/
    it/        ← Italian HTML templates (cover, colophon)
    en/        ← English HTML templates
  build-pdf.sh          ← Build zine (LANG=it|en)
  build-quickstart.sh   ← Build quickstart (LANG=it|en)
  build-all.sh          ← Build all 4 PDFs
  render_materials.py   ← YAML → HTML renderer
  pdf-style.css         ← Shared stylesheet
assets/                 ← Images, fonts (shared by both languages)
output/                 ← Generated PDFs
```

## Building PDFs

### All 4 PDFs at once
```bash
bash scripts/build-all.sh
```

### Single PDF
```bash
LANG=it bash scripts/build-pdf.sh        # Zine Italiano
LANG=it bash scripts/build-quickstart.sh  # Quickstart Italiano
LANG=en bash scripts/build-pdf.sh        # Zine English
LANG=en bash scripts/build-quickstart.sh  # Quickstart English
```

### Dependencies
- `pandoc` (markdown → HTML)
- `weasyprint` (HTML → PDF)
- `pyyaml` (YAML parsing)

### GitHub Actions
Push a tag (`git tag v2.1 && git push origin v2.1`) to auto-build all PDFs and create a GitHub Release. Manual trigger also available via Actions → "Build PDFs" → Run workflow.

## Output

| File | Language | Content |
|------|----------|---------|
| `anamnesia-zine.pdf` | 🇮🇹 Italian | Complete edition (2 scenarios, keeper guide, variants) |
| `anamnesia-quickstart-it.pdf` | 🇮🇹 Italian | Free quickstart (1 scenario, full rules) |
| `anamnesia-zine-en.pdf` | 🇬🇧 English | Complete edition |
| `anamnesia-quickstart-en.pdf` | 🇬🇧 English | Free quickstart |

---

Game Design & Writing: **Riccardo Scaringi**  
YouTube: ilgiocointavolo · Magazine: ioGioco  
© 2026 Riccardo Scaringi. All rights reserved.
