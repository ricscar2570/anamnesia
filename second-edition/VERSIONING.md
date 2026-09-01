# AnamnesiA — Versioning convention

This repository contains two distinct version histories:

- the **published First Edition**, preserved on `main`;
- the **Second Edition development line**, currently isolated on `2e-human-alpha-a0.3`.

Because the repository already contains historical tags such as `2.1`, `21`, `v2.1`, `v2.10` … `v2.14` and `v20`, the Second Edition must use a namespaced tag convention to avoid ambiguity.

## Recommended tag scheme

### Published First Edition

Use `1e-` as the namespace for any new archival tags referring to the published edition.

Examples:

- `1e-final-2026`
- `1e-dtrpg-final`

Historical tags should be preserved rather than renamed or deleted unless there is a compelling archival reason.

### Second Edition — development

Use `2e-` as the namespace.

Alpha milestones:

- `2e-a0.1-core-alpha`
- `2e-a0.2-audit-remediation`
- `2e-a0.3-human-alpha`
- `2e-a0.4-human-alpha-remediation`

Beta milestones:

- `2e-b0.1-blind-beta`
- `2e-b0.2-beta-remediation`

Release candidates:

- `2e-rc1`
- `2e-rc2`

Final publication:

- `2e-v1.0.0`
- `2e-v1.0.1` for editorial/errata-only fixes
- `2e-v1.1.0` for backward-compatible additions
- `2e-v2.0.0` only for a future breaking edition-level rules revision

## Current canonical development label

**`2e-a0.3-human-alpha`**

This label identifies the exact rules baseline frozen for Human Alpha 1.

It should point to the current head of branch `2e-human-alpha-a0.3` only after the Human Alpha kit, scenario, audit and field-operation sources are all committed.

## Tagging rules

1. A tag is immutable historical evidence: do not move a published milestone tag after testers have received it.
2. Patch ordinary working commits without creating a tag.
3. Create a tag only when a milestone is intentionally frozen or distributed to testers.
4. Human Alpha sessions A1–A6 must all use the same `2e-a0.3-human-alpha` baseline unless a P0/safety issue forces an A0.4 remediation.
5. Do not merge Second Edition tags into the meaning of the historical `v2.x` tag family. The `1e-` / `2e-` namespace exists specifically to keep those histories distinguishable.
6. GitHub Release titles should mirror the tag and add a readable milestone name, e.g. `AnamnesiA 2E — Human Alpha 1 A0.3`.

## Recommended release progression

`2e-a0.3-human-alpha` → Human Alpha evidence → `2e-a0.4-human-alpha-remediation` if required → G2 → `2e-b0.1-blind-beta` → remediation as needed → `2e-rc1` → `2e-v1.0.0`.

© 2026 Riccardo Scaringi.