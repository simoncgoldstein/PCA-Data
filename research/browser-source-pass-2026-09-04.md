# Browser-heavy source saturation pass — 2026-09-04

## Scope

Continuation of `research/ingestion-queue-2026-09-03.md`, focused on browser/archive gaps that were poorly suited to deterministic import workflows.

This pass is deliberately **source-first**. It archives stronger current/historical receipts without changing normalized institutional outputs, identity mappings, scoring, UI, or the four manually disabled network-fetch/import workflows.

## Completed / materially advanced

### Covenant College

New receipt:
`sources/raw/institutions/covenant-college/leadership-snapshot-2026-09-04.md`

Coverage:
- 9 Senior Administration
- 4 Board Officers
- 23 Trustees
- 12 Trustee Advisors
- **48 current governance/administration records**

Result: the prior `president only; senior administration and trustees remain blocked` limitation is no longer true for the raw source layer.

### Mission to North America

New receipt:
`sources/raw/institutions/mna/team-snapshot-2026-09-04.md`

Coverage:
- **95 current visible MNA team cards**
- exact title and department where printed
- blank-title / blank-department states preserved rather than inferred
- Sarah Kalichman resolved from current card email plus older official MNA source
- Carlos Dimas / Cory Dimas preserved as distinct current records

Result: this supersedes the earlier high-signal partial raw roster.

### Mission to the World

New receipt:
`sources/raw/institutions/mtw/leadership-snapshot-2026-09-04.md`

Current core directly confirmed:
- Lloyd Kim — Coordinator
- Mark Bates — Senior Director of Missions Engagement
- David Stoddard — International Director for Europe; Managing Director of Field Operations
- Jonathan I. — International Director, Asia Pacific
- Neal W. — International Director, Global Muslim Ministries
- Victor Nakah — International Director, Africa / sub-Saharan Africa

Additional current public-facing senior/program roles preserved:
- Sam Kang
- Dale Hollenbeck
- Jerry Gibson
- Robin Lee

Important source reconciliation:
- Mark Bates's Q3 2024 `Senior Director of US Operations` title is superseded by repeated 2026 `Senior Director of Missions Engagement` biographies.
- David Stoddard now has Managing Director of Field Operations responsibility; Cartee Bales's present status remains unresolved.
- Steve Robertson left MTW for Geneva Benefits in 2025. A still-live MTW conference page calling him Americas International Director is stale. Current Americas successor remains unresolved.
- John Tubbesing's 2024 CAO role is retained historically; current MTW estate page lists only `Ambassadors Program`, insufficient to establish current executive status or an end date.

Historical baseline:
- official Q3 2024 directory preserved as a dated staff/leadership source, not mislabeled as current 2026.

### Reformed University Fellowship

New receipt:
`sources/raw/institutions/ruf/annual-transitions-2026-09-04.md`

Official July 2026 transition coverage:
- 11 new Campus Staff
- 20 new Campus Ministers/Directors/Assistants
- 94 new Interns
- 10 Intern-to-Fellow transitions
- 4 new National Staff
- **139 dated new/transition records** before deduplication

Departure coverage:
- 21 reconstructed Campus Minister / Campus Staff rows
- 53 printed Intern / Fellow departure rows

Raw-source anomalies preserved explicitly:
- `Matt TerrellJoy Beans` extraction boundary documented and reconstructed as two people
- `Tyler Luehrs` duplicated in official extraction and preserved as such
- `Niko Fannin` / `Niko Fanin` spelling variant preserved
- `AidenTuberville` / `Aiden Tuberville` source-form difference preserved

Remaining limitation: this is not yet a complete current RUF campus/national roster. It is a complete 2026 official transition receipt for the captured classes.

### Reformed Theological Seminary

New receipt:
`sources/raw/institutions/reformed-theological-seminary/residential-faculty-snapshot-2026-09-04.md`

Coverage:
- **46 unique names classified by current RTS sources in the residential-faculty universe**
- campus-specific roles and titles preserved
- S. Donald Fortson III retained with exact `Emeritus` title despite current-site placement under a Residential Faculty heading
- Sean Michael Lucas preserved as institution-wide residential-directory record while campus pages also expose him as visiting faculty

Current promotion corrections:
- Zachary J. Cole — Professor of New Testament effective June 1, 2026
- D. Blair Smith — Professor of Systematic Theology effective June 1, 2026
- Guy M. Richard — Professor of Systematic Theology effective June 1, 2026

Remaining limitation: adjunct/visiting/lecturer classes are intentionally separate from the residential count.

### Westminster Theological Seminary

New receipt:
`sources/raw/institutions/westminster-theological-seminary/faculty-snapshot-2026-09-04.md`

Coverage:
- 17 primary Faculty
- 3 Affiliate Faculty
- 9 CCEF Counseling Faculty
- 3 Center for Theological Writing records
- **32 current instructional/academic-support records**

Source discrepancy preserved:
- Westminster Media's `current faculty` index includes names, including Sinclair Ferguson, that are not on the live academic faculty page's current teaching categories. The live academic page controls current-role normalization; the media index remains secondary/historical evidence.

### Revoice 2018

New receipt:
`sources/raw/issues/revoice/revoice18-archive-map-2026-09-04.md`

Located:
- original event/program endpoint: `https://revoice.us/events/revoice18/`
- Wayback root snapshots at 2018-06-29 and 2018-08-28
- contemporaneous / official-linked program fragments for general sessions, breakouts, panel, and pre-conference

Confirmed fragments include:
- dates and Memorial Presbyterian venue
- Eve Tushnet General Session 1 appearance
- General Session 2 `Lament`, Ray Low + Nate Collins
- Wesley Hill General Session 3, `Hope` theme corroborated by contemporaneous source
- Grant Hartley, `Redeeming Queer Culture: An Adventure`
- Greg Johnson breakout and exact title `Making the Church a Haven for Sexual Minorities`, supported by the 2020 Missouri Presbytery investigative report quoting Johnson's own description of his Revoice 2018 talk and footnoting the recording
- `Race, Sexuality, and Intersectionality` panel participants and moderator

Remaining limitation: **the archived body of `/events/revoice18/` has not yet been preserved**, so the project must not claim a complete Revoice 2018 program.

## What this pass intentionally did not change

- `sources/normalized/institutions/current-role-snapshots-2026-09-03.json`
- `scripts/normalize-institution-snapshots.py`
- `data/people.json`
- any identity mapping or ideological score
- UI/application files
- FFO crosswalk outputs
- AMR outputs
- Andrew Augenstein records
- disabled network-fetch/import workflow state

## Validation posture

This branch is a raw-source archive batch. Existing repository validation should therefore remain deterministic and should not require generated normalized-output changes.

Before merging:
1. compare branch against `main` and confirm only intended source/research files changed;
2. open a PR so the repository-controlled `Validate research data` workflow executes against the branch;
3. inspect the validation result;
4. merge only if checks pass and the branch remains based cleanly on `main`.

## Next normalization pass

After this source batch is safely merged, the next code/data pass should:

1. refactor `scripts/normalize-institution-snapshots.py` so each source configuration can carry its own snapshot date/path rather than assuming every institution is a 2026-09-03 receipt;
2. point Covenant College, MNA, RTS, MTW, and WTS at the new 2026-09-04 receipts where the new receipt is genuinely more complete;
3. decide whether RUF annual transitions belong in `current-role-snapshots` or a separate transition/event normalized dataset; separate event semantics are preferable;
4. regenerate normalized institutional output deterministically;
5. run identity resolution under the existing conservative unique-match rule;
6. update validation expectations only where the new deterministic output justifies it.

## Remaining browser-heavy queue after this pass

Highest-value unresolved items:

1. retrieve the actual archived Revoice 2018 `/events/revoice18/` program body;
2. complete a current RUF national/campus roster rather than only the 2026 transition classes;
3. locate a current MTW executive roster / annual report that resolves Cartee Bales, John Tubbesing, and the Americas International Director succession;
4. capture RTS adjunct/visiting/lecturer classes only where needed for broader PCA graph overlap;
5. backfill dated historical leadership only after current-source normalization is complete.