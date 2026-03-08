#!/usr/bin/env python3
"""
build_all.py — Genera tutti i 30 PDF del Digital Extras Pack.
Uso: python build_all.py [lang1 lang2 ...]
     python build_all.py          # tutte e 5 le lingue
     python build_all.py it en    # solo italiano e inglese

Output: build/output/<lang>/0N_nome.pdf  (6 file × 5 lingue = 30 PDF)
"""

import sys, os, time
sys.path.insert(0, os.path.dirname(__file__))

from build_01 import build as b01
from build_02 import build as b02
from build_03 import build as b03
from build_04 import build as b04
from build_05 import build as b05
from build_06 import build as b06

BUILDERS = [b01, b02, b03, b04, b05, b06]
LANGS    = ['it', 'en', 'de', 'fr', 'es']

LANG_NAMES = {
    'it': 'Italiano',
    'en': 'English',
    'de': 'Deutsch',
    'fr': 'Français',
    'es': 'Español',
}

if __name__ == '__main__':
    langs = sys.argv[1:] if len(sys.argv) > 1 else LANGS

    invalid = [l for l in langs if l not in LANGS]
    if invalid:
        print(f'Lingue non valide: {invalid}. Disponibili: {LANGS}')
        sys.exit(1)

    total = len(langs) * len(BUILDERS)
    done  = 0
    errors = []

    t0 = time.time()
    print(f'\nAnamnesiA Digital Extras Pack — Build\n{"─" * 44}')

    for lang in langs:
        print(f'\n▶  {LANG_NAMES[lang]} [{lang}]')
        # Crea directory output se non esiste
        out_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'output', lang,
        )
        os.makedirs(out_dir, exist_ok=True)

        for builder in BUILDERS:
            try:
                builder(lang)
                done += 1
            except Exception as e:
                errors.append((lang, builder.__module__, str(e)))
                print(f'  ERROR [{builder.__module__}] {lang}: {e}')

    elapsed = time.time() - t0
    print(f'\n{"─" * 44}')
    print(f'Completati: {done}/{total} PDF in {elapsed:.1f}s')

    if errors:
        print(f'\nErrori ({len(errors)}):')
        for lang, mod, err in errors:
            print(f'  [{lang}] {mod}: {err}')
        sys.exit(1)
    else:
        print('Tutti i PDF generati senza errori.')
