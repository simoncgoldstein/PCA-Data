# Current Project State

Snapshot date: **2026-09-14**

This file is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Repository state

The current data state includes two reviewed canonical-seeding batches for the 2017 Women Serving committee. Eight of the twelve committee identities are now canonical and projected to the app-facing committee event.

The repository is no longer a v0.1 scaffold. It now contains a substantial evidence archive, normalized research datasets, canonical app-facing data, identity-resolution machinery, generated overlap analysis, and focused CI validators.

Major completed or substantially developed areas include:

- National Partnership source normalization and identity work, with exact archival pinning still incomplete for some person-level claims.
- A Faithful PCA / `Looking Forward – Together` signer snapshots and normalized public-statement data.
- Alliance for Mission & Renewal leadership, media, organizational framing, and related source snapshots.
- General Assembly source ingestion and normalized formal-position/action datasets across multiple years, including women/office, subscription, sexuality/Revoice, Overtures 23/37, Overture 15, NAE withdrawal, protests, minority reports, recorded votes, and study committees.
- Save the PCA / Functional Female Officer external-dataset ingestion with source-attribution boundaries.
- Church and presbytery canonical data.
- Institution and RUF role snapshots.
- Person identity crosswalks and reviewed identity receipts.
- Generated overlap analysis under `analysis/overlap/`.
- Public/app-facing events, affiliations, organizations, people, and sources under `data/`.
- Multiple focused validation workflows plus repository-wide research validation.

## 2017 Women Serving committee

The 2017 PCA Ad Interim Committee on Women Serving in the Ministry of the Church is represented in the normalized research layer and app-facing event graph.

Current identity status:

- `leon-brown` — canonically resolved from reviewed identity evidence and projected to the app graph.
- `dan-doriani` — canonically resolved from reviewed identity evidence and projected to the app graph.
- `ligon-duncan` — canonically resolved from reviewed identity evidence and projected to the app graph.
- `irwyn-ince` — canonically resolved and projected to the app graph.
- `mary-beth-mcgreevy` — canonically resolved from reviewed identity evidence and projected to the app graph; her separately modeled first-person evidence also links to this canonical person.
- `bruce-o-neil` — canonically resolved and projected to the app graph.
- `harry-reeder` — canonically resolved from reviewed identity evidence and projected to the app graph.
- `roy-taylor` — canonically resolved from reviewed identity evidence and projected to the app graph.
- William Castro, Jeffrey Choi, Lani Jones, and Kathy Keller remain unresolved in this dataset unless a later commit changes their normalized IDs.

Applied identity receipts:

- `sources/raw/identity/2017-women-serving-identity-evidence-batch1-2026-09-14.json` — Dan Doriani, Ligon Duncan, Roy Taylor.
- `sources/raw/identity/2017-women-serving-identity-evidence-batch2-2026-09-14.json` — Leon Brown, Mary Beth McGreevy, Harry Reeder.

Guardrail: committee service remains zero-weight and does not assign every report-level statement, either internal school of thought, or a broader ideological label to an individual member. Mary Beth McGreevy's first-person position evidence remains separately modeled and zero-weight.

## Immediate next slice

Continue the 2017 Women Serving identity pass with the remaining four names: William Castro, Jeffrey Choi, Lani Jones, and Kathy Keller.

Resolve only identities that can be established deterministically from primary, first-party, or already-normalized corroborating evidence. Prefer another **2–3 person batch** if the evidence quality is uneven rather than forcing all four into one PR.

For each identity resolved, update together:

- the canonical person layer;
- the normalized 2017 report and person-edge dataset;
- any person-specific evidence already present in the normalized source;
- the app-facing committee-service affiliation;
- the focused validator;
- any generated outputs made stale by the canonical change.

Do not fill the remaining roster by name recognition alone. Leave genuinely unresolved identities explicit.

## Work after the 2017 identity pass

Preferred order unless stronger evidence changes the priority:

1. Complete Garris Letter 1 and 2 signer normalization and canonical linkage where still incomplete.
2. Continue exact National Partnership person-level message/page pinning and distinguish membership, recruitment, promoted candidates, and adjacency.
3. Continue General Assembly denominational-action coverage where source-register gaps remain.
4. Expand Tier A career reconstruction only after the event/action layer and identity links are stable enough to make recurrence meaningful.

Do not make broad ideological-position scoring the next project phase. Position claims should remain person-specific and source-attributed.

## Documentation maintenance rule

When a meaningful milestone is merged, update this file if it changes:

- the latest completed data state;
- the immediate next slice;
- a major source-family status;
- a material unresolved identity or evidence boundary.

Keep this file short enough that a fresh agent can read it before inspecting implementation details.
