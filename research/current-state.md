# Current Project State

Snapshot date: **2026-09-14**

This is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Phase

**Research foundation mature; pre-UI readiness audit complete; next major step is one comprehensive Astra/Sol finish-line run.**

Do not begin another broad identity-resolution or source-expansion pass unless the heavy audit discovers a concrete material blocker.

Before the finish-line run, read:

- `research/pre-ui-astra-readiness-audit.md` — audit verdict, material gaps, product/data contract, UI findings, and v1 acceptance criteria;
- `research/astra-finish-line-brief.md` — the one-shot heavy-run implementation brief.

## Repository state

The repository is an active source-driven PCA research graph with:

- primary-source/provenance material;
- normalized research datasets;
- conservative person-identity crosswalks and reviewed identity receipts;
- canonical app-facing people, organizations, churches, presbyteries, events, affiliations, and sources;
- generated overlap/continuity/coverage analysis;
- deterministic Garris and National Partnership app projectors;
- topic-specific and repository-wide CI validators;
- a static GitHub Pages UI scaffold that is now materially less capable than the evidence layer beneath it.

Substantially developed source areas include National Partnership, A Faithful PCA, AMR, McGowan Global, 2017 Women Serving, Revoice/Warhurst, Human Sexuality, 2021 Overtures 23/37, 2022 Overture 15 and NAE withdrawal, the two Garris letters, 2026 Overture 37, Prayer & Lament, Save the PCA/FFO, PCA church/presbytery data, institutional/RUF snapshots, and reviewed family/context links.

## National Partnership continuity baseline

Current NP identity/app coverage:

- **151** confirmed printed-name NP members;
- **68** confirmed canonical/app-facing people;
- canonical identity coverage: **45.03%**;
- every canonical NP person has exactly one app-facing NP edge, while richer manually curated roles retain their stronger semantics.

High-value exact-name continuity queues are closed:

- A Faithful PCA June 2021: **50 confirmed NP overlaps / 0 unresolved exact-name possibilities**;
- A Faithful PCA March 2022 cumulative snapshot: **54 / 0**;
- 2019 Warhurst protest: **31 / 0**;
- 2022 Overture 15 negative votes: **20 / 0**;
- 2022 NAE-withdrawal protest: **10 / 0**;
- targeted NP <-> Garris Letter 1 exact-name queue: complete.

Selected interpretation boundaries:

- AFP March 2022 is a cumulative snapshot of the 2021 action, not an independent later action;
- AMR current leadership shares four confirmed people with canonical NP, but personnel overlap is not proof of organizational succession;
- no canonical NP edge means membership not established, not confirmed non-membership;
- the current data does **not** support an NP-vs-non-NP risk ratio, odds ratio, causal claim, or `X times more likely` claim.

The canonical NP subset is incomplete and non-random because recurring/high-profile people are generally easier to resolve. Display canonical-subset percentages together with full-roster lower bounds/coverage context.

## Garris letters

Complete source rosters are normalized in `sources/normalized/public-statements/garris-letters-2024.json`.

- **Letter 1:** 60 printed signers; 25 canonical/app-projected; 35 canonical identities unresolved.
- **Letter 2:** 21 printed signers; 21/21 canonical/app-projected.
- **All 81 printed signatures are preserved as source-level data points.**
- A resolved signature is a confirmed `public_coalition_action`, weight 3, score included.

The remaining 35 Letter 1 rows are deferred identity work, not missing source data. The final UI must be able to display those rows without inventing canonical people.

Critical identity boundary:

- Letter 1 `Jeff White` — New City Fellowship / Rio Grande — remains unresolved;
- Letter 2 `Jeff White` — Redeemer Downtown / Metro NY — is `jeff-white-redeemer-downtown`.

Signing one letter establishes that specific public action only. It does not by itself establish NP/AMR membership or a generic ideological label.

## Key evidence-model guardrails

Preserve throughout the UI and any new presentation projection:

- facts/claims before interpretive labels;
- same-name is insufficient for identity merging;
- committee service does not transfer every report statement to each member;
- church/employment/education/current-role context normally has zero ideological/network weight;
- family links are reciprocal factual context, weight 0, and never transfer theology/actions/membership;
- co-signature does not transfer unrelated positions or network membership;
- personnel overlap does not prove organizational successor/front/equivalence;
- source wording and historical conflicts remain visible rather than silently harmonized;
- unresolved source rows are not canonical people;
- absence from a roster is not opposition.

## Pre-UI audit conclusion

See `research/pre-ui-astra-readiness-audit.md` for detail.

**Verdict: GO.** No additional broad normal-chat research slice is required before the heavy run.

The important remaining issues are presentation/model-projection issues:

1. Current `app.js` loads only people, organizations, events, affiliations, and sources; it does not surface the full church/presbytery graph, unresolved source occurrences, or generated analysis.
2. Only person profiles have meaningful drill-down. Organizations/events/actions are shallow display objects.
3. Evidence kinds are flattened into one weight-sorted list, obscuring distinctions among membership, leadership, public action, vote, committee, authored position, institutional context, collaboration, and family/context.
4. The current people table recomputes the displayed Network Involvement Index from confidence-filtered evidence, so a display filter can mutate the apparent canonical score. This must be fixed.
5. The score is more prominent than its evidence breakdown and provisional analytical status warrants.
6. Garris unresolved source rows need a first-class app representation distinct from canonical people.
7. Generated NP continuity/overlap and coverage outputs are valuable but currently absent from the product.
8. Registered local/archive source records need graceful provenance display rather than broken/empty links.
9. Church/presbytery data can enrich the product, but full church-string canonicalization is not a v1 blocker.

## Material gaps that do not block v1

Do not stop the finish-line run merely to complete:

- all 151 NP identities;
- all 35 remaining Garris Letter 1 identities;
- every historical GA roster identity;
- every AFP church-string match;
- every person's current-role/career history;
- every historical renewal-network roster;
- a predictive NP-vs-non-NP model without a defensible comparison cohort.

Investigate further only if the heavy audit finds a contradiction that materially changes a prominent profile, major network/action conclusion, source attribution, or required UI feature.

## Required heavy-run stress tests

At minimum inspect end-to-end behavior for:

- Mike Khandjian — NP membership/recruitment, independent Fellowship distinction, AMR, Garris 1, current role;
- David Cassidy — AMR/McGowan/Garris recurrence with no inferred NP membership;
- Jeffrey Choi — 2017 authored evidence versus 2026 advocacy/dissent and Pacific Presbytery sponsorship boundary;
- Kathy Keller / Tim Keller — spouse context without evidence/score transfer;
- Hansoo Jin — canonical identity while preserving source-specific `Korean Capitol` wording;
- James Kessler — richer founder/principal-organizer NP edge retained over generic member semantics;
- Garris Letter 1 — 60/60 source rows visible, 25 linked, 35 unresolved, Jeff White distinction preserved;
- Garris Letter 2 — 21/21 linked;
- NP continuity — 68/151 coverage and denominator/lower-bound caveats visible;
- at least one zero-weight committee/family/current-role/church edge visible but excluded from score.

## Next step

Run the comprehensive heavy agent using `research/astra-finish-line-brief.md` as the implementation contract.

The run should:

1. audit the repository end to end on a risk basis;
2. correct only material research/model problems discovered;
3. redesign the information architecture and UI with broad discretion;
4. add a clean app-facing source-occurrence/roster-row model so unresolved source participants remain visible;
5. expose selected generated analysis responsibly;
6. fix index/filter correctness and improve score transparency;
7. validate representative inference boundaries;
8. update final documentation;
9. run full CI;
10. open one merge-ready finish-line PR and **do not merge it**.

No additional normal-chat cleanup PR should be inserted before that run unless this readiness documentation itself reveals a factual error.

## Documentation maintenance rule

After the heavy run, replace this handoff with the actual v1 state, final architecture, known deferred gaps, and maintenance priorities. Do not leave `pre-UI` as the stated project phase after the final UI PR merges.
