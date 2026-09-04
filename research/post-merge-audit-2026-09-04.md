# Post-merge repository audit — 2026-09-04

## Purpose

Reconcile the repository after the September 4 research wave, identify genuinely orphaned work, distinguish stale branch names from unmerged durable work, and replace the older ingestion handoff with a current operational checkpoint.

## Main branch status

Current `main` after the recovered Insider Movements/SCIM merge:

- merge commit: `bcfa2364d95d5db4342232d9a57c617826ed7118`
- formal-position validation: passing
- research-data validation: passing
- no known generated-output drift at this checkpoint

## Branch audit

### Durable work already merged

The following research branches are historical branch tips whose durable work is represented on `main` through merged pull requests, usually squash merges. Their apparent divergence from `main` does not indicate unmerged research:

- `research/browser-source-pass-2026-09-04` — PR #1
- `research/institution-normalizer-refactor-2026-09-04` — PR #2
- `research/revoice18-completeness-2026-09-04` — PR #3
- `research/institution-ingest-batch1-2026-09-04` — PR #4
- `research/institution-ingest-batch2-2026-09-04` — PR #5
- `research/ruf-transitions-2026-09-04` — PR #6
- `research/ruf-campus-catalog-2025` — PR #7
- `research/revoice18-program-recovery-2026-09-04` — PR #8
- `research/revoice18-confirmed-participation-2026-09-04` — PR #9
- `research/women-serving-formal-positions-2026-09-04` — PR #11
- `research/formal-position-mining-batch1-2026-09-04` — PR #12
- `research/formal-position-mining-batch2-2026-09-04` — PR #13
- `research/women-worship-formal-position-batch3-2026-09-04` — PR #14
- `research/subscription-fv-batch4-2026-09-04` — PR #15
- `research/insider-movements-recovery-2026-09-04` — PR #16

### Intentionally unmerged disposable workflow branch

`research/revoice18-asset-recovery-2026-09-04` is intentionally not merged. PR #10 existed only to run a temporary read-only Wayback asset-recovery workflow. Its unique repository change is the exploratory workflow itself, not durable normalized evidence. Do not merge this branch.

### Genuine orphan recovered during this audit

`research/insider-movements-formal-position-batch4-2026-09-04` contained completed 2011–2014 SCIM research that had validated successfully but was never carried into a PR. It was recovered onto current `main`, rebuilt against the newer identity resolver, reviewed, and merged through PR #16.

Reviewed person-specific SCIM identity resolutions now preserved on `main`:

- David Garner = David B. Garner
- Guy Waters = Guy Prentiss Waters
- Nabeel Jabbour = Nabeel T. Jabbour

The review-queue generator was also tightened so explicitly reviewed name variants are not re-flagged solely because of initials or expanded middle names.

## Reconciled Work/Chrome checkpoint

The older `research/ingestion-queue-2026-09-03.md` checkpoint is materially stale. The following items are now complete or substantially complete on `main`:

- National Partnership explicit-membership evidence: canonical file contains 151 normalized printed-name members supported by 409 evidence records.
- A Faithful PCA: all 571 numbered signers normalized.
- Warhurst protest roster: normalized.
- 2021 Overture 37 minority/recorded-vote evidence: normalized.
- 2022 Overture 15 named formal-position and recorded-vote evidence: normalized.
- 2022 NAE-withdrawal protest roster: normalized.
- 2016 racial-reconciliation overtures: all 43 accounted for by presbytery/action category.
- PCA agency/institution snapshots: substantial current coverage exists across AC, CDM, Covenant College, Covenant Seminary, MNA, MTW, RUF, RTS, WTS, WSC, GPTS, Geneva Benefits, PCA Foundation, and Ridge Haven.
- Covenant Seminary: 51 current faculty, emeriti, incoming faculty, and trustee-class records.
- RUF: 2026 transition events plus the 2025–26 414-row historical campus catalog are normalized.
- Save the PCA FFO: deterministic matching is encoded; 143 records matched and four intentionally preserved for review at the previous checkpoint.
- AMR: platform inventory, 31 captioned videos, and reviewed participant appearances are normalized.
- Formal-position mining now includes 2001–02 Women in the Military; 2003 subscription; 2007 FV/NPP; 2008–09 women-related minority reports; 2011–14 SCIM; 2016 women-study formal actions; 2017 Women Serving; 2019–23 sexuality/O37/O15.

The old Work/Chrome handoff threshold has therefore been met. Browser-heavy research can now be used selectively for stubborn primary-source gaps rather than as a prerequisite for the next phase.

## Remaining high-value source gaps

These are explicit incompletenesses, not evidence of broken prior merges:

1. **1999 General Assembly named blocks**
   - 61-name MNA vote block
   - 144-name Overture 16 block
   - Protests 3 and 4
   - current repository records the gap but does not invent the names

2. **2000 General Assembly named MNA vote blocks**
   - 16-name block
   - 20-name block

3. **2002 Women in the Military final action**
   - 77 recorded negative votes are known at event level
   - named roster remains unrecovered

4. **2002 subscription action**
   - 127 recorded negative votes are known at event level
   - named roster remains unrecovered

5. **Revoice 2018 original printed program**
   - confirmed fragment layer exists
   - the complete approximately-26-workshop program is not reconstructed
   - first-party session evidence indicates attendees possessed a printed program/program-like packet

6. **AMR source-bounded content extraction**
   - inventories and captions exist
   - highest-priority caption passages still need structured issue-level extraction

7. **Long-tail identity review**
   - continue only with source-supported person-specific resolutions
   - do not loosen matching thresholds or create global nickname/middle-name heuristics

8. **Tier-A ministry/career trajectories**
   - current/historical role reconstruction remains useful after source saturation, especially where people recur across multiple high-value datasets

## Recommended next research order

1. Recover the 1999/2000/2002 named General Assembly vote/protest blocks from primary minutes or page images.
2. Recover the 2002 subscription 127-name negative-vote roster.
3. Continue Revoice 2018 printed-program recovery using scans, photographs, attendee archives, and contemporary social-media images rather than treating the later mixed media gallery as a complete program.
4. Extract bounded claims from the highest-priority AMR captions.
5. Continue identity review only as new source context justifies it.
6. Defer detective-view/UI expansion until another source-gap pass is complete.

## Guardrails

- Preserve printed names and source forms.
- Explicit reviewed identity decisions are person-specific.
- Aggregate vote totals never imply unnamed person-level positions.
- Committee membership, report concurrence, report authorship, floor roles, recorded votes, and institutional service remain analytically distinct.
- Institutional/employment/education edges remain zero-weight unless a separate source establishes a formal issue position.
- Do not merge exploratory network workflows merely because their branch remains ahead of an old base.
