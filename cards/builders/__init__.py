"""AnamnesiA card-deck builders package.

Modules:
  theme   - YAML theme loader (colours, fonts, layout)
  icons   - per-category PNG icon generator
  front   - card-front renderer (single page on a Canvas)
  back    - assembles 36 backs from 3 Rorschach asset images
  deck    - full pipeline orchestrator (CLI entry point)

Quick start:
  python -m cards.builders.deck --lang it
  python -m cards.builders.deck --lang en
"""
