# Current project state

Snapshot: **2026-09-14**

## Phase

**V1 evidence explorer implemented on the finish-line PR; awaiting review and merge.** This document describes that implementation. The earlier pre-UI audit and finish-line brief remain historical acceptance contracts, not the current architecture.

## Product

The public static application now provides an overview, global entity search, typed person profiles, organization/network profiles, first-class actions and complete source rosters, an interactive detective map, selected NP continuity analysis, source provenance, methodology, and secondary church/presbytery exploration.

The map supports node dragging, canvas panning, zooming, neighborhood tracing, filters, and connection/source inspection. Its canonical and supplemental source layers are visibly distinct. Unresolved identities can appear as labeled source-row nodes without fabricated people.

See `research/v1-architecture.md` for routes, files, projections, scoring semantics, testing, and maintenance instructions.

## Evidence baseline preserved

- Canonical app: 329 people, 21 organizations, 19 events, 167 affiliations; 38 canonical source registrations.
- Church directory: 1,970 church nodes, 88 presbyteries.
- Crosswalk: 4,415 source occurrences across 62 datasets, all available through the presentation projection.
- NP: 151 printed member names, 68 canonical people, 45.03% identity coverage.
- Garris Letter 1: 60 sourced signatures, 25 linked identities, 35 unresolved identities.
- Garris Letter 2: 21 signatures, all linked. Its Jeff White remains distinct from the unresolved Letter 1 Jeff White.
- Confirmed NP overlaps: AFP June 2021 50; AFP March 2022 cumulative snapshot 54; Warhurst 31; Overture 15 negative votes 20; NAE protest 10; Garris Letter 1 10.

No new canonical identities or score-bearing edges were created by this UI run. Supplemental authored positions and source occurrences remain unscored. The source registry's stale claim that the NP archive binary was still awaiting placement was corrected to reflect the existing preserved repository PDF.

## Material issues addressed

1. Fixed confidence-filter score mutation. Canonical scores and score ordering derive from the complete included edge set.
2. Added a reproducible source-occurrence presentation model, independent of identity completeness.
3. Preserved printed rosters, source locators, archived context, reviewed source conflicts, and individual attribution boundaries in navigable profiles.
4. Separated membership, public action, denominational action, authored evidence, committee service, and institutional/family context.
5. Added literal source and action drill-down, including graceful local/archive provenance.
6. Surfaced generated NP overlap with both denominators, lower-bound language, shared people, non-random coverage, and temporal caveats.
7. Added a filterable detective map without causal, ideological-transfer, or proximity-based claims.

## Consciously deferred gaps

| Priority | Gap | Why deferred / trigger |
| --- | --- | --- |
| Material later | Exact archival pins for older strongly-supported NP app edges | Broad archive support remains labeled accurately; improve when a prominent claim needs a precise pin. |
| Material later | Source-specific printed-field adapters for less central crosswalk shapes | Every occurrence remains accessible with normalized context and source locator; add adapters as a dataset becomes a primary research path. |
| Material later | Dated current-role refresh for prominent profiles | Role dates and verification gaps are visible; refresh when a role matters to a conclusion. |
| Nice-to-have | Remaining 83 NP identities and 35 Letter 1 identities | Source rosters are already visible; resolve only with independent corroboration and user-facing value. |
| Nice-to-have | Full AFP church-string normalization and career histories | No complete concentration model or full career claim is presented. |
| Nice-to-have | More historical renewal-network rosters and authored-evidence adapters | Existing normalized records remain in the repository and source directory. |
| Not needed for v1 | Predictive NP-vs-non-NP ratios or causal model | No defensible opportunity-aware comparison cohort; absent NP edges cannot define non-members. |
| Not needed for v1 | Backend/database or full-scale force-graph infrastructure | Static data and a bounded SVG explorer meet the current product need. |

## Maintenance priorities

Keep original source wording and identity decisions separate. Run canonical projectors and analytical builders before `build-explorer.py`; verify deterministic output. Preserve the canonical score/filter and source-roster tests. Do not re-open a broad identity-completion campaign solely to raise coverage percentages. Review and merge the finish-line PR manually after CI acceptance.
