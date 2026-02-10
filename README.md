# AnamnesiA

**Un gioco di ruolo narrativo di horror psicologico**

*«Cosa resta quando anche le bugie svaniscono?»*

---

AnamnesiA è un gioco di ruolo narrativo di horror psicologico per 2–4 giocatori. Non c'è un Master tradizionale: tutti collaborano per ricostruire una verità sepolta.

📖 **Leggi le regole online:** [https://TUOUSERNAME.github.io/anamnesia/](https://TUOUSERNAME.github.io/anamnesia/)

📥 **Scarica il PDF:** Disponibile nella sezione [Releases](https://github.com/TUOUSERNAME/anamnesia/releases/latest)

## Come funziona questa repository

Questa repository contiene i sorgenti del Quickstart di AnamnesiA. Il contenuto è scritto in Markdown e viene trasformato automaticamente in:

- **Un sito web** navigabile, tramite [Jekyll](https://jekyllrb.com/) e [GitHub Pages](https://pages.github.com/)
- **Un PDF** scaricabile, generato automaticamente ad ogni release tramite [GitHub Actions](https://github.com/features/actions)

## Struttura

```
anamnesia/
├── _config.yml              # Configurazione Jekyll
├── _data/
│   ├── archetipi.yml        # ★ Sorgente unica: 4 archetipi
│   └── carte_frammento.yml  # ★ Sorgente unica: 24 carte + dati generatore
├── _sass/
│   ├── color_schemes/
│   │   └── anamnesia.scss   # Tema colori
│   └── custom/
│       └── custom.scss      # Stili personalizzati
├── archetipi/               # Pagine dei 4 Archetipi
├── index.md                 # Homepage
├── pilastri.md              # I Quattro Pilastri
├── come-si-gioca.md         # Come Si Gioca
├── il-sistema.md            # Il Sistema: Frammenti e Dadi
├── stress-ed-echi.md        # Stress ed Echi
├── archetipi.md             # Panoramica Archetipi
├── sessione-zero.md         # Sessione Zero Express
├── avvio-primo-ciclo.md     # Avvio del Primo Ciclo
├── esempio-di-gioco.md      # Esempio di Gioco
├── scenario-incidente.md    # Scenario: L'Incidente
├── riferimento-rapido.md    # Tabella di Riferimento Rapido
├── changelog.md             # Changelog & E Poi?
├── materiali.md             # Hub materiali di gioco
├── generatore.html          # ⚄ Generatore (Liquid → _data)
├── scheda-personaggio.html  # 📋 Schede PG (Liquid → _data)
├── carte-frammento.html     # 🃏 Carte Frammento (Liquid → _data)
├── scripts/
│   ├── build-pdf.sh         # Script generazione PDF
│   ├── render_materials.py  # Renderer Python (YAML → HTML per PDF)
│   ├── pdf-template.html    # Template struttura PDF
│   └── pdf-style.css        # Stile A5 per il PDF
└── .github/
    └── workflows/
        ├── pages.yml        # Deploy sito su GitHub Pages
        └── pdf.yml          # GitHub Action per PDF automatico
```

### Architettura dati unificata

I dati di gioco vivono in un'unica posizione (`_data/*.yml`) e vengono consumati da due pipeline:

- **Sito web:** Jekyll legge `_data/` e i template Liquid negli `.html` generano le pagine
- **PDF:** `render_materials.py` legge gli stessi YAML e genera HTML iniettato nel template PDF

Modificare un archetipo, una carta o un dato del generatore in `_data/` aggiorna automaticamente sia il sito che il PDF.

## Build locale

```bash
# Sito web
gem install bundler
bundle install
bundle exec jekyll serve
# → http://localhost:4000

# PDF (richiede pandoc, weasyprint, pyyaml)
pip install weasyprint pyyaml
bash scripts/build-pdf.sh
```

## Licenza

Game Design e Testi: **Riccardo Scaringi**

YouTube: ilgiocointavolo

© 2026 Riccardo Scaringi. Tutti i diritti riservati. Versione Quickstart 1.3
