# AnamnesiA

**Horror Psicologico · Gioco di Ruolo Narrativo**  
**Psychological Horror · Narrative Tabletop RPG**  
**Horror Psicológico · Juego de Rol Narrativo**

> *"Cosa resta quando anche le bugie svaniscono?"*  
> *"What remains when even the lies fade away?"*  
> *"¿Qué queda cuando incluso las mentiras se desvanecen?"*

A GM-less narrative RPG for 2–4 players. ZineQuest 2026.

---

## Repository Structure

```
content/
  it/          ← Italian markdown (rules, scenarios, archetypes)
  en/          ← English markdown
  es/          ← Spanish markdown
_data/
  it/          ← Italian YAML (character sheets, fragment cards)
  en/          ← English YAML
  es/          ← Spanish YAML
scripts/
  templates/
    it/        ← Italian HTML templates (cover, colophon)
    en/        ← English HTML templates
    es/        ← Spanish HTML templates
  build-pdf.sh          ← Build zine (LANG=it|en|es)
  build-quickstart.sh   ← Build quickstart (LANG=it|en|es)
  build-all.sh          ← Build all 6 PDFs
  render_materials.py   ← YAML → HTML renderer (trilingual labels)
  pdf-style.css         ← Shared stylesheet
assets/                 ← Images, fonts (shared by all languages)
output/                 ← Generated PDFs
```

## Building PDFs

### All 6 PDFs at once
```bash
bash scripts/build-all.sh
```

### Single PDF
```bash
LANG=it bash scripts/build-pdf.sh        # Zine Italiano
LANG=it bash scripts/build-quickstart.sh  # Quickstart Italiano
LANG=en bash scripts/build-pdf.sh        # Zine English
LANG=en bash scripts/build-quickstart.sh  # Quickstart English
LANG=es bash scripts/build-pdf.sh        # Zine Español
LANG=es bash scripts/build-quickstart.sh  # Quickstart Español
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
| `anamnesia-zine-es.pdf` | 🇪🇸 Spanish | Complete edition |
| `anamnesia-quickstart-es.pdf` | 🇪🇸 Spanish | Free quickstart |

---

Game Design & Writing: **Riccardo Scaringi**  
YouTube: ilgiocointavolo · Magazine: ioGioco  
© 2026 Riccardo Scaringi. All rights reserved.
