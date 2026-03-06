# AnamnesiA — Digital Extras Pack: Build System

Sistema di generazione automatica dei **30 PDF** del Digital Extras Pack di AnamnesiA (6 documenti × 5 lingue).

---

## Struttura

```
build/
├── assets/
│   ├── fonts/                  # Font Lora statici (generati automaticamente)
│   ├── rorschach_1.png
│   ├── rorschach_2.png
│   ├── rorschach_3.png
│   ├── rorschach_4.png
│   └── rorschach_cthulhu.png
├── builders/
│   ├── shared.py               # Stili, font, helper condivisi
│   ├── build_01.py             # Generatori di Complicazioni
│   ├── build_02.py             # Scheda del Custode
│   ├── build_03.py             # Riferimento Rapido
│   ├── build_04.py             # Schede Personaggio (4 archetipi)
│   ├── build_05.py             # Note di Design
│   ├── build_06.py             # The Lethe Infection
│   └── build_all.py            # Batch builder (tutte le lingue)
├── content/
│   ├── it/  01.yaml … 06.yaml  # Italiano
│   ├── en/  01.yaml … 06.yaml  # English
│   ├── de/  01.yaml … 06.yaml  # Deutsch
│   ├── fr/  01.yaml … 06.yaml  # Français
│   └── es/  01.yaml … 06.yaml  # Español
├── output/
│   ├── it/  *.pdf              # Output generati
│   ├── en/  *.pdf
│   ├── de/  *.pdf
│   ├── fr/  *.pdf
│   └── es/  *.pdf
└── .github/
    └── workflows/
        └── build-pdfs.yml      # CI/CD GitHub Actions
```

---

## Requisiti

```
Python 3.10+
reportlab
PyYAML
fonttools
```

Installazione:

```bash
pip install reportlab PyYAML fonttools
```

---

## Primo avvio: generazione dei font

I font Lora (Google Fonts) vengono estratti come istanze statiche da un variable font. Questo passaggio va fatto una sola volta, oppure viene eseguito automaticamente dalla CI.

```bash
python3 - << 'EOF'
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import os

configs = [
    ('/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf',
     [400, 700], ['LoraRegular', 'LoraBold']),
    ('/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf',
     [400, 700], ['LoraItalic', 'LoraBoldItalic']),
]
os.makedirs('build/assets/fonts', exist_ok=True)
for src, weights, names in configs:
    for w, name in zip(weights, names):
        f = TTFont(src)
        inst = instantiateVariableFont(f, {'wght': w})
        dest = f'build/assets/fonts/{name}.ttf'
        inst.save(dest)
        print(f'Saved {dest}')
EOF
```

Se il sistema non ha i font Lora preinstallati, scaricali prima:

```bash
# Ubuntu / Debian
sudo apt-get install fonts-google-noto

# oppure scarica manualmente
curl -L "https://github.com/google/fonts/raw/main/ofl/lora/Lora%5Bwght%5D.ttf" \
  -o /usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf
curl -L "https://github.com/google/fonts/raw/main/ofl/lora/Lora-Italic%5Bwght%5D.ttf" \
  -o /usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf
```

---

## Generazione PDF

**Tutte le lingue (30 PDF):**

```bash
cd build
python builders/build_all.py
```

**Lingue specifiche:**

```bash
python builders/build_all.py it en
python builders/build_all.py de
```

**Documento singolo:**

```bash
python builders/build_01.py it
python builders/build_06.py en
```

---

## Documenti inclusi

| # | Nome | Contenuto |
|---|------|-----------|
| 01 | Complication Generators | Tabelle d6 per 3 fasi: Nebbia, Connessioni, Rivelazioni |
| 02 | Memory Keeper Reference | Struttura ciclo, fasi, domande per fase, tracking sessione |
| 03 | Quick Reference Card | Formula tiro, esiti, Pool/Stress, meccaniche speciali v2.0 |
| 04 | Character Sheets | 4 archetipi: Sopravvissuto, Testimone, Protettore, Catalizzatore |
| 05 | Design Notes | 9 sezioni: origine, Regola d'Oro, changelog v1.0→v2.0 |
| 06 | The Lethe Infection | Meccanica parasitaria per Mörk Borg, OSE/OSR, Call of Cthulhu 7e |

---

## Aggiornare i contenuti

Ogni documento è definito da un file YAML in `content/<lingua>/0N.yaml`. La struttura è documentata dai commenti nei file stessi. Per aggiornare un testo:

1. Modifica il file YAML corrispondente.
2. Rigenera con `python builders/build_0N.py <lang>`.
3. Controlla il PDF in `output/<lang>/`.

Per aggiungere una nuova lingua:
1. Crea la directory `content/<lingua>/`.
2. Copia e traduci i 6 file YAML.
3. Aggiungi la lingua a `LANGS` in `build_all.py`.
4. Aggiungi la lingua al workflow GitHub Actions.

---

## CI/CD

Il workflow `.github/workflows/build-pdfs.yml` si attiva:

- **Su push** a `main` quando vengono modificati file in `build/content/`, `build/builders/` o `build/assets/`.
- **Manualmente** via `workflow_dispatch` con parametro `lang` opzionale.
- **Su tag** `v*`: genera i PDF e li allega automaticamente alla release GitHub.

L'artifact `anamnesia-digital-extras-pack` viene conservato per 30 giorni ad ogni build.

---

## Crediti

Game Design e Testi: Riccardo Scaringi
YouTube: ilgiocointavolo · Rivista: ioGioco

© 2026 Riccardo Scaringi. Tutti i diritti riservati.
