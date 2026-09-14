# Current Project State

Snapshot date: **2026-09-14**

This file is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Repository state

Latest merged milestone at this snapshot: PR #44, `Add reviewed identity evidence for 2017 committee batch 1`.

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

The 2017 PCA Ad Interim Committee on Women Serving in the Ministry of the Church is now represented in the normalized research layer and app-facing event graph.

Current identity status:

- `irwyn-ince` — canonically resolved and projected to the app graph.
- `bruce-o-neil` — canonically resolved and projected to the app graph.
- Dan Doriani — high-confidence reviewed identity evidence, proposed canonical ID `dan-doriani`, not yet seeded.
- Ligon Duncan — high-confidence reviewed identity evidence, proposed canonical ID `ligon-duncan`, not yet seeded.
- Roy Taylor — high-confidence reviewed identity evidence, proposed canonical ID `roy-taylor`, not yet seeded.
- Leon Brown, William Castro, Jeffrey Choi, Lani Jones, Kathy Keller, Mary Beth McGreevy, and Harry Reeder remain unresolved in this dataset unless a later commit changes their normalized IDs.

Guardrail: committee service remains zero-weight and does not assign every report-level statement, either internal school of thought, or a broader ideological label to an individual member.

## Immediate next slice

The next compact research slice should apply the already-reviewed canonical identity decisions for:

1. Dan Doriani
2. Ligon Duncan
3. Roy Taylor

That slice should:

- create or seed the canonical people conservatively;
- update the 2017 normalized report and person-edge dataset;
- add exactly the corresponding app-facing committee-service edges;
- preserve `weight: 0` and `score_included: false`;
- update focused validation so the canonical and app projections remain synchronized;
- regenerate any derived outputs that become stale;
- avoid unrelated role-history or theological-position expansion.

## Work after that

Preferred order unless stronger evidence changes the priority:

1. Continue resolving the remaining 2017 committee identities in small evidence-backed batches.
2. Complete Garris Letter 1 and 2 signer normalization and canonical linkage where still incomplete.
3. Continue exact National Partnership person-level message/page pinning and distinguish membership, recruitment, promoted candidates, and adjacency.
4. Continue General Assembly denominational-action coverage where source-register gaps remain.
5. Expand Tier A career reconstruction only after the event/action layer and identity links are stable enough to make recurrence meaningful.

Do not make broad ideological-position scoring the next project phase. Position claims should remain person-specific and source-attributed.

## Documentation maintenance rule

When a meaningful milestone is merged, update this file if it changes:

- the latest completed milestone;
- the immediate next slice;
- a major source-family status;
- a material unresolved identity or evidence boundary.

Keep this file short enough that a fresh agent can read it before inspecting implementation details.
