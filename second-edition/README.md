# AnamnesiA — Second Edition development

This directory contains the active development line for **AnamnesiA Second Edition**.

The published first edition remains untouched in the repository root. Second Edition work is isolated here until the Human Alpha and G2 gates are passed.

## Current milestone

**Human Alpha 1 — A0.3**

Status:

- Design Constitution: PASS
- Core A0.3: frozen for Human Alpha 1
- *L'Incidente* A0.3: frozen for Human Alpha 1
- Structural / Monte Carlo stress test: completed
- Human Alpha 1 kit and field protocol: ready
- Kickstarter backer recruitment copy: ready
- Human Alpha 1 sessions A1–A6: **to be executed with real players**
- G2: pending real human playtest evidence
- *Il Tradimento* 2E and further content: blocked until G2

## Core design direction

The Second Edition keeps the original identity of AnamnesiA while tightening its procedures:

- five Cycles remain the backbone of play;
- Nebbia → Connessioni → Rivelazioni remains unchanged;
- the Regola d'Oro remains central;
- Stress, Echi, Breakdown and Ultimo Ricordo remain core dramatic pressures;
- scenarios now distinguish **Fatti Fissi**, **Domande Aperte** and **Vincoli di Rivelazione**;
- memory contradictions are tracked without turning corroboration into objective truth;
- **Corroborato non significa vero** is a core epistemic rule;
- the Second Edition must remain light enough that procedures disappear into the fiction.

## Repository layout

- `alpha-a0.3/core/` — current Core Alpha source
- `alpha-a0.3/scenarios/` — scenario and card sources
- `alpha-a0.3/audit/` — technical / structural validation notes
- `alpha-a0.3/playtest/` — Human Alpha 1 operational documents

## Freeze rule

A0.3 is frozen for the six-session Human Alpha 1 campaign. Rules should not change between sessions except for a safety-critical issue or a P0 defect that prevents play. If the same severe problem appears in two independent sessions, the campaign stops and A0.4 remediation begins.

## Remaining roadmap

### 1. Human Alpha 1 — next mandatory gate
Run sessions A1–A6 with 2, 3 and 4 players, including:
- narrative-focused players;
- low/medium-experience players;
- traditional RPG players;
- First Edition veterans;
- at least one true blind group that learns the game only from the Alpha kit.

Collect:
- session length;
- roll distribution;
- Stress/Echi/Breakdown data;
- use of Approaches and Forzare il Ricordo;
- contradiction count and resolution;
- time spent on the Memory Register;
- perceived agency and clarity of the Regola d'Oro;
- finale satisfaction;
- whether the session still feels recognizably like AnamnesiA.

### 2. Human Alpha report / A0.4 remediation
After A1–A6:
- classify issues P0/P1/P2/P3;
- decide which experimental rules survive;
- produce A0.4 only where evidence requires remediation;
- run targeted re-tests if needed.

Primary open questions:
- is the two-memory-roll cap useful or artificial?
- do +2 Approaches become inaccessible too early?
- is the Echi 6–8 penalty of −2 correct?
- does Identità Fratturata create useful fiction or excess contradictions?
- does the Memory Register remain lightweight?
- are Ombre del Trauma inspirational rather than prescriptive?
- are the 12 scenario cards useful without an extra cost?
- can the Regola d'Oro be learned without author explanation?
- can Cycle 5 close the story without a predetermined solution?

### 3. G2 — Scenario/Core gate
G2 may pass only if Human Alpha evidence shows that:
- the Regola d'Oro no longer creates recurring authority conflicts;
- the Memory Register remains operationally light;
- contradictions are playable rather than administrative;
- the finale works without Keeper fiat;
- no Approach or Archetype is structurally dominated;
- the game still feels like AnamnesiA.

### 4. Content expansion — blocked until G2
Once G2 passes:
1. Convert **Il Tradimento** to the 2E scenario template.
2. Design and test the advanced Archetypes **Il Negatore** and **L'Assente**.
3. Write and test the new scenarios **La Trasmissione** and **La Casa Sommersa**.
4. Build the **36 Universal Fragment Cards**: 12 Nebbia, 12 Connessioni, 12 Rivelazioni.
5. Complete 12 scenario-specific cards for each of the four core scenarios.
6. Build the scenario generator.
7. Expand the Memory Keeper guide using real playtest failure modes.
8. Add complete examples: one roll, one contradiction, one Breakdown, Cycle 5, condensed session.

### 5. Campaign module — after one-shot freeze
Design **Palinsesto** only after the one-shot core is stable. If it requires substantial additional machinery, publish it as a separate supplement rather than burdening the core rules.

### 6. Blind Beta
Run at least 6–8 groups that learn and play without author intervention. Validate teachability, scenario prep, safety procedures, final truth construction and repeatability.

### 7. Rules freeze and editorial production
After Beta:
- freeze rules and terminology;
- assemble the full manual;
- complete editing and cross-reference QA;
- rebuild indexes and reference materials;
- produce digital, print and printer-friendly editions;
- keep play materials in a separate PDF;
- perform final accessibility and print QA.

### 8. GitHub release strategy
- keep First Edition stable on `main` while 2E remains experimental;
- preserve Alpha/Beta development in dedicated branches / PRs;
- merge the Second Edition only after the appropriate release gate;
- tag the final release separately from the published First Edition history.

## Publication status

Nothing in this directory should be treated as rules-locked or publication-ready until Human Alpha 1, G2, the subsequent content-development gates and blind Beta are complete.

### Current readiness estimate

- core game design: **~75–80%**
- planned Second Edition content: **~40%**
- editorial / commercial readiness: **~25–30%**

The immediate bottleneck is no longer design work. It is **real Human Alpha evidence**.

© 2026 Riccardo Scaringi.