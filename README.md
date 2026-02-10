# AnamnesiA

**Repository privata** — Gioco di ruolo narrativo di horror psicologico per 2–4 giocatori.

## Struttura

```
*.md                   ← contenuti Markdown (18 file)
_data/                 ← sorgente unica YAML
  archetipi.yml            4 Archetipi (Pool, Approcci, abilità)
  carte_frammento.yml      24 carte (Nebbia/Connessioni/Rivelazioni)
scripts/               ← pipeline di build
  build-pdf.sh             → anamnesia-zine.pdf (50 pag)
  build-quickstart.sh      → anamnesia-quickstart-free.pdf (28 pag)
  pdf-template.html        template Zine
  pdf-template-quickstart.html  template Quickstart
  pdf-style.css            stile condiviso (Cinzel + Alegreya)
  render_materials.py      YAML → schede + carte HTML
assets/                ← immagini e font
  cover-skull.png          copertina
  rorschach.png            pagina interna
  fonts/                   Cinzel, Alegreya, Alegreya SC (woff2)
```

## Build

Richiede: `pandoc`, `python3`, `weasyprint`, `pyyaml`

```bash
bash scripts/build-pdf.sh          # Zine completa (50 pag)
bash scripts/build-quickstart.sh   # Quickstart gratuito (28 pag)
```

## Automazione

```bash
git tag v1.5 && git push --tags
```

→ GitHub Actions builda entrambi i PDF → Release su GitHub → Quickstart su itch.io

### Setup itch.io (una tantum)

Settings → Secrets: `BUTLER_API_KEY` · Settings → Variables: `ITCHIO_USER`

## Due prodotti, una sorgente

| | Quickstart | Zine |
|:--|:--|:--|
| Pagine | 28 | 50 |
| Dove | itch.io (gratis) | Kickstarter (a pagamento) |
| Contenuto | Sistema, Archetipi, 1 scenario, carte, schede | + Sessione Zero, Guida Custode, 2° scenario, Varianti |

## Licenza

© 2026 Riccardo Cangini. Tutti i diritti riservati.
