# Astra Finish-Line Brief

Prepared: **2026-09-14**

This document is the handoff for a single comprehensive heavy run intended to bring PCA-Data from a mature research repository and UI scaffold to a polished, evidence-first v1 product.

## Mission

**Audit the repository end to end, correct only material information/model gaps, redesign the information architecture and public UI as needed, implement the redesign, validate representative evidence paths, run final tests, and open one finish-line PR.**

Do not stop after producing recommendations or wireframes. The expected output is working repository changes plus a concise final audit of what changed and what remains consciously deferred.

You have broad design and architectural discretion. The existing HTML/CSS/JS UI is a scaffold, not a constraint. Preserve the research/evidence guardrails, not the current page layout.

## Required reading order

Before making changes, read:

1. `AGENTS.md`
2. `README.md`
3. `research/current-state.md`
4. `research/pre-ui-astra-readiness-audit.md`
5. `research/methodology.md`
6. `research/source-register.md`
7. `research/companion-corpus.md`
8. `research/unresolved-identities.md`
9. `sources/README.md`

Then inspect the existing front end, canonical `data/` files, relevant normalized source datasets, generated `analysis/` outputs, builders/projectors, and validators before choosing the final architecture.

Treat repository state—not prior chat history—as authoritative.

## Operating mode

This is intended to be the **last major build/audit run before v1**.

Use judgment and finish the product rather than waiting for the user to make routine design decisions. Do not ask for confirmation on ordinary architecture, styling, component, naming, or layout choices. Make the best evidence-driven product decisions you can.

If a real factual/model contradiction is discovered, investigate it. If the issue is merely long-tail incompleteness, represent the limitation honestly and keep moving.

Prefer one coherent implementation branch and one reviewable PR. **Do not merge it.**

## Research audit scope

Perform a risk-based audit, not a row-by-row re-research of the universe.

### Confirm

- primary/reliable source provenance survives into material app claims;
- canonical identity and unresolved source occurrence remain distinct concepts;
- edge kind, confidence, source, notes, score inclusion, and weight are not lost in presentation projections;
- generated overlap metrics still match their source/identity denominators;
- source conflicts/printed variants are preserved where intentionally recorded;
- family, institutional, committee, co-signature, education, and adjacency evidence does not transfer theology or network membership;
- current-role snapshots are not silently presented as timeless facts;
- A Faithful PCA March 2022 remains a cumulative snapshot of the 2021 action, not an independent behavior event;
- McGowan/AMR/NP personnel overlap is not presented as organizational succession without separate evidence;
- the two Garris letters remain distinct actions and the two Jeff White rows remain distinct absent further evidence.

### Research only when material

Only add new factual research if it would materially change:

- a prominent person profile;
- a major organization/network profile;
- a high-value overlap/continuity conclusion;
- an event/action roster;
- a source attribution;
- a planned UI feature;
- a serious factual inconsistency discovered during implementation.

Do not spend the run completing low-value identity percentages.

## Current research baseline to preserve

At handoff:

- confirmed NP printed roster: **151**;
- canonical/app-facing NP identities: **68 (45.03%)**;
- AFP June 2021 confirmed NP overlap: **50**, exact-name possible queue **0**;
- AFP March 2022 cumulative snapshot confirmed NP overlap: **54**, queue **0**;
- Warhurst 2019 confirmed NP overlap: **31**, queue **0**;
- Overture 15 negative-vote confirmed NP overlap: **20**, queue **0**;
- NAE-withdrawal protest confirmed NP overlap: **10**, queue **0**;
- Garris Letter 1: **60 printed rows / 25 canonical / 35 unresolved**;
- Garris Letter 2: **21 printed rows / 21 canonical**.

These values are not immutable if the audit finds a real data error, but do not casually change them through UI reshaping or identity inference.

## Product goal

Build a serious source-driven research interface that lets a reader answer:

1. Who is this person and what is actually documented about them?
2. Which networks, institutions, denominational actions, public letters, committees, collaborations, and family/context relationships connect them?
3. Which connections are formal, which are public actions, and which are merely contextual?
4. What source supports each connection?
5. What happened at a particular event/action, and who is on its complete source roster?
6. Which people recur across selected organizations/actions over time?
7. What can and cannot responsibly be inferred from that recurrence?

The product should feel like a polished research index / evidence explorer, not an activist scorecard and not a database admin console.

## Information architecture expectations

You may redesign these, but the final product should give first-class treatment to the underlying objects and tasks.

### Overview

A useful landing experience with:

- concise project purpose;
- global search or strong discovery path;
- meaningful dataset/source metrics;
- selected high-confidence findings or research modules;
- methodology/inference notice;
- clear paths into people, networks/organizations, actions/events, analysis, and sources.

Do not make a person leaderboard the primary thesis of the site.

### People

Profiles should expose evidence in typed sections rather than one flat weighted list.

Useful categories include:

- network membership/founding/leadership;
- public coalition actions;
- denominational votes/protests/reports/actions;
- authored or attributable positions;
- institutional/career context;
- church/presbytery context;
- collaboration;
- family/context relationships;
- unresolved claims if relevant.

Show sources and evidence boundaries. If the Network Involvement Index remains visible, make it secondary and explain/break down the contributing edges.

### Networks / organizations

Profiles should show:

- description/status/timeframe;
- source basis;
- people grouped by relationship type;
- related events/actions;
- selected overlaps with other networks/actions;
- appropriate boundary language.

### Actions / events

Make actions/events first-class and deep-linkable.

Required capabilities:

- literal action summary;
- date/year;
- source(s);
- complete roster where repository source data is complete;
- resolved/canonical participant count;
- unresolved source-level rows;
- links from resolved rows to canonical profiles;
- overlap context when useful;
- no invented identity for unresolved source rows.

### Analysis

Use the generated analysis selectively.

At minimum, evaluate whether the final product should surface:

- National Partnership continuity/recurrence;
- selected pairwise overlap;
- recurring people;
- source/dataset coverage;
- identity-resolution coverage;
- church/presbytery concentration only where coverage supports it.

Do not make raw 1,891-pair tables the default user experience.

Every displayed percentage must make its denominator/coverage meaning understandable.

### Sources / methodology

Users should be able to inspect source provenance without leaving the context of the claim. The dedicated source area can also provide a searchable register and concise definitions.

Handle local/archive-only source records gracefully rather than rendering empty links.

## Required source-occurrence model

The final v1 must be able to display a complete source roster without requiring every row to be a canonical person.

The Garris letters are the required case:

- all 60 Letter 1 printed signers must be inspectable;
- 25 should link to canonical person profiles;
- 35 should remain visibly unresolved source rows;
- all 21 Letter 2 signers should link to canonical people;
- Letter 1 Jeff White must remain source-level unresolved New City Fellowship / Rio Grande;
- Letter 2 Jeff White must link to `jeff-white-redeemer-downtown`.

Design a clean generic representation—`source occurrence`, `roster entry`, `participant row`, or equivalent—rather than creating fake canonical people.

You may add generated app-facing JSON and projectors/validators to make this clean.

## Network Involvement Index requirements

The index is provisional analytical metadata, not the product's verdict on a person.

### Fix the current filter bug

The existing UI can recompute a person's displayed index from a confidence-filtered subset of affiliations. That means display filtering changes the apparent canonical score.

Fix this. The canonical index should derive from the canonical score-included edge set. If the UI offers a filtered subtotal, label it separately.

### Show enough explanation

When the score is presented, users should be able to understand:

- contributing edge;
- evidence kind;
- weight;
- whether it is included;
- zero-weight contextual evidence;
- why a visible edge may not contribute.

Do not imply that high index = theological verdict.

## Analytical boundaries

### Allowed descriptive analysis

With appropriate caveats, expose:

- confirmed shared people;
- recurrence counts;
- overlap counts;
- canonical-subset percentages;
- complete-roster lower bounds;
- resolution coverage;
- dated personnel continuity;
- score breakdown from score-included edges.

### Forbidden shortcuts

Do not publish as established:

- NP vs non-NP risk ratios/odds ratios based on absent NP edges;
- `X times more likely` claims without a defensible opportunity-aware comparison cohort;
- causal claims from recurrence;
- organizational succession/front/equivalence from shared people alone;
- ideological labels inferred from family, employment, education, committee service, co-signature, conference participation, or church association;
- absence from a roster as opposition.

If you determine a defensible predictive comparison cohort can now be built, justify the cohort and assumptions in detail before implementing it. The default expectation is **defer predictive ratios for v1**.

## UI/visual design freedom

You have free rein to redesign the product.

The current serif/earth-tone static page may be retained, substantially refined, or replaced. Optimize for credibility, legibility, research density, and evidence navigation.

Requirements:

- desktop and mobile responsive;
- accessible keyboard interactions;
- strong color contrast;
- deep-linkable major entities/views;
- clear empty/loading/error states;
- no sensational ideological color coding;
- contextual/zero-weight edges visually distinct from formal membership/action evidence;
- performant on GitHub Pages.

A graph visualization is optional. Use one only if it materially improves exploration and remains legible/evidence-linked. A polished relational table/timeline/overlap interface is preferable to an impressive but unusable hairball graph.

## Technical discretion

The project is currently static HTML/CSS/JS/JSON on GitHub Pages.

You may:

- refactor the front end substantially;
- split JavaScript/CSS into modules;
- add generated presentation JSON;
- add build scripts if they materially improve maintainability and the committed output still deploys reliably to GitHub Pages;
- add lightweight dependencies when justified;
- add focused validation/smoke tests.

Prefer the simplest architecture that can express the product well. Do not introduce server/database complexity solely for architectural fashion.

Never hand-edit generated research analysis when a builder owns it.

## Representative stress tests

Before considering the run complete, inspect the UI/evidence path for all of these:

### Mike Khandjian

Must preserve:

- confirmed NP membership/participation/recruitment;
- his independently created Fellowship as distinct from NP;
- AMR founding role;
- Garris Letter 1 signature;
- current Chapelgate role.

Do not visually collapse the Fellowship and NP.

### David Cassidy

Show:

- AMR founding/current role;
- McGowan role;
- Garris Letter 1;
- current Spanish River role;
- **no canonical NP membership**.

Do not infer NP membership from recurrence.

### Jeffrey Choi

Preserve distinctions among:

- 2017 authored women/office evidence;
- 2026 Overture 37 public advocacy/floor speech;
- Pacific Presbytery as formal overture submitter;
- Choi as one of four later formal dissent submitters.

Do not label him sole overture author/sponsor/orchestrator.

### Kathy Keller / Tim Keller

Show spouse relationship as contextual, reciprocal, zero-weight, with no transfer of Kathy's authored evidence to Tim.

### Hansoo Jin

Show canonical identity while preserving source-specific printed context, including Warhurst's `Korean Capitol` spelling.

### James Kessler

Preserve his richer founder/principal-organizer NP edge and weight 5; do not downgrade it to the generic generated member edge.

### Garris Letter 1

All 60 source rows must be visible. Resolved and unresolved rows must be distinguishable without implying that unresolved = uncertain signature. The signature is sourced; only the canonical identity is unresolved.

### Garris Letter 2

All 21 source rows should resolve to canonical profiles.

### NP continuity

Show identity coverage and denominator caveats alongside any percentage. Do not imply the 68 resolved members are a random sample of the 151.

### Zero-weight edge

Pick a family, committee, current-role, church, or presbytery edge and confirm it is visible but not silently counted as network involvement.

## Validation expectations

During implementation:

- use targeted syntax/data checks after coherent changes;
- do not run the entire suite after every CSS tweak;
- at the milestone/end, run the repository-wide validation and all PR workflows;
- add focused validators for any new generated presentation data or critical inference boundary;
- verify generated outputs are clean/current;
- manually inspect representative desktop/mobile pages if possible.

Do not weaken existing validators merely to make a new UI pass.

## Documentation expectations

At completion update at least:

- `README.md` if the public product/architecture changes materially;
- `research/current-state.md` to record v1 state and genuinely deferred gaps;
- relevant methodology/source docs only if the underlying contract changes;
- any new data-projection documentation required for maintainers.

The final PR body should summarize:

- audit findings;
- architecture/UI changes;
- data projections added;
- representative inference tests;
- deferred research;
- validation results.

## Finish-line criteria

Do not call the run complete until the following are true or explicitly documented as blocked:

1. The UI is substantially redesigned/restructured if needed, not merely cosmetically restyled.
2. People, networks/organizations, actions/events, and sources are genuinely explorable.
3. Complete source rosters can appear even when canonical identity resolution is incomplete.
4. Garris Letter 1 shows 60/60 source rows without fabricating 35 people.
5. Evidence kinds and score treatment are understandable in profiles.
6. The canonical index does not change merely because evidence display filters change.
7. Selected generated continuity/overlap analysis is actually useful in the product.
8. Percentages display enough denominator/coverage context to prevent obvious misreading.
9. Major inference guardrails survive representative end-to-end testing.
10. Source provenance remains directly inspectable.
11. Mobile and desktop experiences are polished.
12. Existing research CI remains green.
13. Any new presentation projection is reproducible/validated.
14. Remaining source gaps are explicitly prioritized as `material later`, `nice-to-have`, or `not needed for v1`.
15. One final PR is opened and **not merged**.

## What not to spend the run on

Do not make these prerequisites unless the audit uncovers a concrete user-facing reason:

- resolving all NP names;
- resolving all remaining Garris Letter 1 identities;
- normalizing every church string;
- filling every person's current job/career history;
- reconstructing every historical renewal group;
- inventing a predictive model to make the analysis sound stronger;
- preserving the current UI merely because it already exists.

## Final instruction

Use the repository's evidence model as the constraint and the current UI as disposable implementation detail.

**Audit first, then build. Resolve material contradictions if found. Otherwise make the best product decisions, implement them fully, validate the evidence paths, and leave the user one merge-ready finish-line PR.**
