# RUF 2026 transition-event ingestion — 2026-09-04

## Scope

This pass models the two official July 2026 Reformed University Fellowship staff announcements as dated employment/role-transition events. It deliberately does **not** reinterpret the announcements as a complete current RUF roster.

Primary source receipt:
`sources/raw/institutions/ruf/annual-transitions-2026-09-04.md`

Normalized output:
`sources/normalized/institutions/ruf/role-transitions-2026.json`

Deterministic normalizer:
`scripts/normalize-ruf-transitions.py`

## Event coverage

The normalized file contains **213 source events**:

- 129 `started_role`
- 10 `transitioned_role`
- 74 `ended_role`

Source-class counts are retained exactly:

- 11 new Campus Staff
- 20 new Campus Ministers, Directors, and Assistants
- 94 new Interns
- 10 Intern-to-Fellow transitions
- 4 new RUF National Staff
- 21 departing Campus Ministers and Campus Staff
- 53 departing Interns and Fellows

Every event has `ideological_weight: 0`.

## Role and campus fidelity

- New Campus Staff rows retain `Campus Staff` as the role class and preserve the printed campus.
- New Intern rows retain `Intern` and preserve the printed campus.
- The combined `Campus Ministers, Directors, and Assistants` class preserves the campus but leaves `role_as_printed` null because the announcement does not identify which exact role applies to each person.
- National Staff rows preserve the exact printed title.
- Intern-to-Fellow rows retain explicit `from_role_as_printed: Intern` and `to_role_as_printed: Fellow`.
- Departure rows in combined classes preserve only the class and person name. Exact role and campus remain null because the departure announcement does not print them.

No current employment, campus, office, presbytery, destination, or later affiliation is inferred from a departure row.

## Preserved source anomalies

Raw-source anomalies remain visible rather than being silently repaired in normalized identity fields:

- `Tyler Luehrs` appears twice in the official departure text extraction; both source occurrences remain separate events.
- `Niko Fanin` and `Niko Fannin` remain separate printed forms from the July 14 and July 8 announcements.
- `Aiden Tuberville` and `AidenTuberville` remain separate printed forms.
- `Mike Park / Mike S. Park` remains the combined form printed in the new-hire receipt.
- `Matt Terrell` and `Joy Beans` remain separate reconstructed rows as documented in the raw receipt's extraction note.

## Identity integration boundary

The normalized RUF event file itself remains identity-neutral. Canonical identity decisions live in the separate crosswalk layer and do not rewrite the historical event receipt.

The 213 event rows are registered as a distinct identity dataset:
`ruf_staff_transitions_2026`

However, they share the identity **source family** `institution_reformed-university-fellowship` with the existing RUF institutional-role dataset. This is intentional. The transition announcement and the existing RUF selected-hire/current-role evidence are not independent evidence families merely because they are represented by separate normalized datasets.

An initial test that treated the RUF transitions as a separate identity family produced 23 new canonical people through same-RUF corroboration. That result was rejected. After placing both RUF datasets in the same source family:

- identity source rows: **2,952 → 3,165**
- bounded identity datasets: **28 → 29**
- canonical person count remains **207**
- generated crosswalk-profile people remain **190**
- `ruf_staff_transitions_2026` has **213 rows and 0 confirmed canonical people**
- the existing `institution_reformed-university-fellowship` dataset returns to its prior **1 confirmed row/person**

Thus the new RUF event source adds evidence and review candidates without using duplicated RUF-family evidence to manufacture identities.

## Validator changes

`validate-research-imports.py` now enforces:

1. exactly 213 RUF transition events;
2. exact event split of 129 started, 10 transitioned, and 74 ended;
3. unique event IDs;
4. zero ideological weight on all RUF service events;
5. source-fidelity fields on each event;
6. no inferred exact role or campus on ambiguous departure classes;
7. null exact roles plus preserved campuses for the 20 combined minister/director/assistant starts;
8. preservation of duplicate/spelling/combined-name source forms;
9. presence of a 213-row `ruf_staff_transitions_2026` identity dataset;
10. identity dataset count may grow but may not regress below the established 28-dataset baseline, and dataset IDs must remain unique.

The read-only GitHub validation workflow also now regenerates `role-transitions-2026.json` and diffs it against the checked-in normalized file, making the RUF event dataset deterministically reproducible.

## What this pass does not claim

- It does not provide a complete current RUF staff/campus roster.
- A `started_role` announcement establishes a 2026 start/transition fact, not indefinite current employment.
- An `ended_role` event establishes departure from the RUF role class, not the person's later employer, church, denomination, office, or location.
- Apparent spelling variants are not merged in the event source layer.

## Remaining RUF source gap

The current public RUF People directory uses dynamic category/load-more behavior and has not yielded a complete deterministic current roster through the available browser path. If complete current-roster coverage becomes the next priority, the most useful attachment would be a saved HTML/PDF or screenshots of the fully expanded RUF People directory/category pages after all `Load More` results are visible, or an official RUF/PCA directory export if available.