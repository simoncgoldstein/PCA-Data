# Current Project State

Snapshot date: **2026-09-14**

This file is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Repository state

The 2017 Women Serving committee identity pass is complete: all 12 official committee members are canonically resolved and projected to the app-facing committee event. The repository also contains a normalized 2026 Overture 37 record distinguishing Pacific Presbytery's formal submission from Jeffrey Choi's person-specific advocacy, floor speech, and later formal dissent.

A person-specific women/office evidence layer now separately normalizes attributable positions for Jeffrey Choi, Kathy Keller, and William Castro without inferring those positions from committee service.

The repository is no longer a v0.1 scaffold. It contains a substantial evidence archive, normalized research datasets, canonical app-facing data, identity-resolution machinery, generated overlap analysis, and focused CI validators.

Major completed or substantially developed areas include:

- National Partnership source normalization and identity work, with exact archival pinning still incomplete for some person-level claims.
- A Faithful PCA / `Looking Forward – Together` signer snapshots and normalized public-statement data.
- Alliance for Mission & Renewal leadership, media, organizational framing, and related source snapshots.
- General Assembly source ingestion and normalized formal-position/action datasets across multiple years, including women/office, subscription, sexuality/Revoice, Overtures 23/37, Overture 15, NAE withdrawal, protests, minority reports, recorded votes, study committees, and 2026 Overture 37 on ordained women deacons.
- Save the PCA / Functional Female Officer external-dataset ingestion with source-attribution boundaries.
- Church and presbytery canonical data.
- Institution and RUF role snapshots.
- Person identity crosswalks and reviewed identity receipts.
- Generated overlap analysis under `analysis/overlap/`.
- Public/app-facing events, affiliations, organizations, people, and sources under `data/`.
- Multiple focused validation workflows plus repository-wide research validation.

## 2017 Women Serving committee

All 12 official committee identities are canonical:

- `leon-brown`
- `william-castro`
- `jeffrey-choi`
- `dan-doriani`
- `ligon-duncan`
- `irwyn-ince`
- `lani-jones`
- `kathy-keller`
- `mary-beth-mcgreevy`
- `bruce-o-neil`
- `harry-reeder`
- `roy-taylor`

Applied identity receipts:

- `sources/raw/identity/2017-women-serving-identity-evidence-batch1-2026-09-14.json` — Dan Doriani, Ligon Duncan, Roy Taylor.
- `sources/raw/identity/2017-women-serving-identity-evidence-batch2-2026-09-14.json` — Leon Brown, Mary Beth McGreevy, Harry Reeder.
- `sources/raw/identity/2017-women-serving-identity-evidence-batch3-2026-09-14.json` — Jeffrey Choi, Kathy Keller.
- `sources/raw/identity/2017-women-serving-identity-evidence-batch4-2026-09-14.json` — William Castro, Lani Jones.

Guardrail: committee service remains zero-weight and does not assign every report-level statement, either internal school of thought, or a broader ideological label to an individual member.

## Person-specific women/office evidence

Normalized record:

`sources/normalized/general-assembly/2012-2019-women-serving-member-authored-positions.json`

Current factual model:

- **Jeffrey Choi (2017):** argued that the biblical evidence did not justify a denomination-wide rule either including or excluding women from the diaconate and favored local-session discretion; he also argued that Romans 16:1 gives substantial support to Phoebe holding a recognized official role while treating 1 Timothy 3:11 as insufficient by itself to settle the diaconate question. Do not read his later 2026 Overture 37 activity backward into this earlier position.
- **Kathy Keller (2012):** maintained a male-only authoritative-teaching/elder boundary while advocating broad teaching, leadership, speaking, exhortation, prayer, and ministry by women outside that authority; she rejected treating the relevant Pauline commands as culturally obsolete and distinguished ordination from the injustice of imposing extra-biblical restrictions that marginalize women's gifts.
- **William Castro (2019):** defended the traditional restriction on women teaching, preaching, or otherwise speaking individually and officially in ordinary public worship; he rejected the interpretation that 1 Corinthians 14:34 concerns only the judging of prophecies and warned against cultural pressure driving novel exegesis. His argument does not treat congregational singing/responses or every extraordinary historical circumstance as identical to individual official speech.

All of these records remain `ideological_weight: 0`. They are source-attributed issue positions, not a new ideological scoring layer.

Mary Beth McGreevy's previously normalized first-person evidence remains a separate person-specific record.

## 2026 Overture 37: women as ordained deacons

Normalized record: `sources/normalized/general-assembly/2026-overture-37-women-deacons-formal-actions.json`.

Current factual model:

- Overture 37 was formally submitted by **Pacific Presbytery** and proposed amending BCO 9-3 and conforming provisions to permit local sessions to decide whether qualified women may serve as ordained deacons.
- The Overtures Committee recommended answering the overture in the negative by **115-14-1**, and the Assembly adopted the negative recommendation.
- Jeffrey Choi is separately documented as a public advocate for Overture 37 and as a floor speaker in support. Those advocacy edges are unscored.
- A later formal dissent from the Assembly action names TEs Aaron Baker, Jeffrey Choi, Walter Henegar, and Eric Kapur as its submitters. Choi's confirmed co-authorship/submission of that dissent is modeled as a formal person-specific denominational action with weight 3.
- Current primary evidence does **not** name Choi as the sole author, drafter, sponsor, or orchestrator of Overture 37. Preserve that attribution boundary unless stronger primary evidence is added.

## Immediate next slice

Shift back to the broad operational graph and complete **Garris Letter 1 and 2 signer normalization and canonical linkage** where the signer evidence can be resolved deterministically.

For that slice:

- normalize the signer rosters from the registered primary PDFs;
- preserve letter 1 and letter 2 as separate actions;
- link only identities that meet the repository's existing identity standard;
- leave common-name or institutionally ambiguous rows unresolved;
- project confirmed signer edges to the app-facing events using the ordinary public-letter weight already defined by methodology;
- regenerate identity/overlap outputs and add focused validation so co-signature cannot be inflated into unrelated network membership or theological agreement.

## Work after that

Preferred order unless stronger evidence changes the priority:

1. Complete Garris Letter 1 and 2 signer normalization and canonical linkage.
2. Continue exact National Partnership person-level message/page pinning, distinguishing membership, recruitment, promoted candidates, and adjacency.
3. Continue remaining General Assembly denominational-action coverage and source gaps.
4. Expand additional person-specific position evidence only where it materially improves a high-value case study or recurring-person profile.
5. Expand Tier A career reconstruction after the event/action layer and identity links are stable enough to make recurrence meaningful.

Do not make broad ideological-position scoring the next project phase. Position claims should remain person-specific and source-attributed.

## Documentation maintenance rule

When a meaningful milestone is merged, update this file if it changes:

- the latest completed data state;
- the immediate next slice;
- a major source-family status;
- a material unresolved identity or evidence boundary.

Keep this file short enough that a fresh agent can read it before inspecting implementation details.
