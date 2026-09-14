# Pre-UI / Astra Readiness Audit

Audit date: **2026-09-14**

Purpose: determine whether PCA-Data is ready for one comprehensive heavy run that audits the information, closes only material gaps, redesigns the user experience, and brings the public site to a credible v1 finish line.

## Verdict

**GO for the heavy Astra/Sol run.**

The repository is no longer research-blocked. The core evidence architecture, source provenance, identity guardrails, app-facing graph, generated overlap analysis, and topic-specific validators are mature enough that another broad normal-chat research phase would have diminishing returns.

The remaining important problems are chiefly **product/data-presentation problems**, not missing-research problems:

1. the current UI exposes only a narrow subset of the repository;
2. unresolved source-level roster rows are not first-class app objects;
3. generated analytical outputs are not surfaced;
4. evidence kinds, scoring boundaries, confidence, source provenance, and source conflicts are too compressed in the current profile UI;
5. organization/event/source drill-down is shallow;
6. the full church/presbytery graph exists but is largely absent from the site;
7. the Network Involvement Index is currently presented more prominently and less transparently than the evidence model warrants.

These are appropriate for a single end-state implementation run.

## What is sufficiently mature

### Source/evidence pipeline

The intended pipeline is established and repeatedly validated:

`source -> raw/provenance -> normalized dataset -> canonical identity/edge -> app-facing data -> generated analysis`

The heavy run should preserve that architecture rather than bypass it with hand-authored UI conclusions.

### Major source families

The repository has substantial normalized or registered evidence for the high-value source families that motivated the project, including:

- National Partnership correspondence and confirmed membership evidence;
- A Faithful PCA / Looking Forward – Together;
- Alliance for Mission & Renewal founding/current leadership/media;
- 2017 Women Serving study committee and person-specific authored evidence;
- Revoice-related denominational records and the 2019 Warhurst protest;
- Human Sexuality Ad Interim Committee material;
- 2021 Overtures 23/37 and related minority reports/votes;
- 2022 Overture 15 and NAE-withdrawal actions;
- the two 2024 Zachary Garris public letters;
- 2026 women-deacons Overture 37 and dissent;
- A Call to Prayer & Lament;
- McGowan Global Institute current roster evidence;
- Save the PCA / Functional Female Officer external church assessment data;
- PCA church/presbytery data and selected institutional/RUF snapshots;
- reviewed family/context links such as Tim Keller <-> Kathy Keller.

The private Drive companion corpus is inventoried separately. Its authored synthesis is not treated as independent evidence, and its direct source PDFs are discoverable through repository metadata.

### National Partnership continuity work

The confirmed printed NP roster is 151 names. **68 are canonical/app-facing (45.03%)** after targeted identity work.

The high-value exact-name overlap queues are now closed:

- A Faithful PCA June 2021: **50 confirmed NP overlaps / 0 exact-name possibilities**;
- A Faithful PCA March 2022 cumulative snapshot: **54 / 0**;
- 2019 Warhurst protest: **31 / 0**;
- 2022 Overture 15 negative votes: **20 / 0**;
- 2022 NAE-withdrawal protest: **10 / 0**;
- targeted NP <-> Garris Letter 1 exact-name queue: closed.

This is enough for descriptive recurrence displays. It is **not** enough for an NP-vs-non-NP causal or predictive risk ratio, because the unresolved NP population cannot be treated as confirmed non-members and the action cohorts are not opportunity-normalized.

### Garris letters

The source layer is complete:

- Letter 1: **60 printed signers**, 25 canonical;
- Letter 2: **21 printed signers**, 21 canonical;
- total: **81 source-level signature rows**.

The remaining 35 Letter 1 identities are not a data-loss problem. Their names, offices, institutions, presbyteries, print order, source, and action are already preserved. They should be visible as unresolved source-level participants in the final UI rather than hidden until canonicalized.

## Current UI audit

The present static site is a useful scaffold, but it no longer matches the depth of the repository.

### What the current application loads

`app.js` loads only:

- `data/people.json`;
- `data/organizations.json`;
- `data/events.json`;
- `data/affiliations.json`;
- `data/sources.json`.

It does **not** load the full church/presbytery graph, normalized unresolved roster rows, or generated analysis outputs.

### Current views

The site currently provides:

- People table;
- simple organization/network cards;
- chronological event list;
- flat source list;
- person modal.

Only people have meaningful drill-down. Networks and events are not first-class navigable profiles.

### Material UI correctness issue: filtered score mutation

`renderPeople()` filters affiliations by the selected confidence filter and then calls `scoreFor(person.id, evidence)`. Therefore changing the evidence-confidence filter can change the displayed Network Involvement Index and sorting order.

That is conceptually misleading. The canonical index should be calculated from the canonical score-included edge set. A visibility filter may change which evidence is shown or which people match, but it should not silently redefine the person's canonical score. If the final UI offers a filtered subtotal, it must be labeled as such rather than replacing the canonical index.

### Evidence-type flattening

The current person modal renders every affiliation in one weight-sorted list. It does not visibly distinguish enough between:

- formal network membership / founding / leadership;
- public coalition action;
- denominational vote/action;
- committee service;
- authored or first-person position;
- ordinary institutional/current role;
- church/presbytery relationship;
- collaboration;
- family/context edge.

This is the central UI risk. The repository intentionally treats those relationships differently; the interface should make those distinctions more visible, not less.

### Score transparency

The current interface shows a single numeric index but does not show a sufficiently clear breakdown of:

- which edges contribute;
- which edges are zero-weight;
- which edges are excluded;
- what each evidence kind means;
- why current-role/family/committee/context edges may appear without contributing score.

The index should become secondary to the evidence ledger, with a transparent breakdown available when shown.

### Source provenance limitations

A person's edge shows source links, but the site does not provide a robust evidence drill-down showing claim -> edge type -> confidence -> source(s) -> source locator/context -> score treatment.

Some registered sources are local/archive provenance records without a public URL. The UI must not render an empty/broken link for such sources; it should show an appropriate provenance label.

### Generated analysis is invisible

The repository already generates:

- NP continuity summaries;
- pairwise overlap tables;
- shared-person lists;
- person recurrence;
- institutional pipeline summaries;
- church/presbytery concentration;
- dataset coverage and graph-quality diagnostics.

None of this is meaningfully surfaced in the current product. The final UI should selectively expose high-value analysis while avoiding an indiscriminate dump of all pairwise combinations.

### Organizations and events are under-modeled in the UI

`data/organizations.json` and `data/events.json` contain important literal framing and interpretive boundaries, but current network cards/timeline items are mostly display-only.

The final product should support organization/network and event/action profiles with participant rosters, edge kinds, sources, related actions, and bounded overlap analysis.

### Full institutional graph is not used

`data/churches.json` and `data/presbyteries.json` are validated first-class graph entities, but the current app does not load them. The analysis layer contains **1,970 church nodes and 88 presbytery nodes**.

This does not mean the launch UI must expose all 1,970 churches equally. Astra should decide the best level of discoverability. Canonically matched churches/presbyteries can enrich person/event/network profiles; unresolved church-string cleanup should not become a launch blocker.

## Material remaining source/model gaps

These are real, but none requires another broad research phase before UI work.

### 1. Unresolved Garris source rows need an app representation

**Material and must be solved in the heavy run.**

Canonical `data/people.json` cannot represent an unresolved printed signer without inventing a person identity. The final application therefore needs a first-class concept such as `source occurrence`, `roster entry`, or equivalent.

Required properties for a Garris roster row include at least:

- action/event ID;
- print order;
- name as printed;
- office as printed;
- institution as printed;
- presbytery as printed;
- canonical person ID when resolved, otherwise null;
- identity status;
- source ID.

Astra may generalize this beyond Garris if useful. The important invariant is: **source occurrence is not canonical person identity**.

### 2. Some important NP app edges still rely on broad archive source IDs

Several older manually curated NP edges remain `strongly_supported` because an exact archive page/message has not been normalized into that app edge, even though the broader archive establishes the relationship.

This is worth displaying accurately but is not a UI blocker. The heavy run should not spend substantial time chasing exact archival pins unless a missing pin materially affects a prominent public claim or is needed to resolve an inconsistency discovered during the audit.

### 3. Long-tail source datasets remain poorly canonicalized

Dataset coverage intentionally remains uneven. Some older formal-action rosters have very low or zero canonical identity resolution.

The final UI should distinguish:

- source roster completeness;
- canonical identity resolution coverage;
- app-facing canonical participants.

It should not hide a complete primary roster merely because canonical identity resolution is incomplete, and it should not present unresolved rows as canonical people.

### 4. Church-string normalization is incomplete

Generated quality diagnostics still report many unmatched/ambiguous structured church strings in large AFP rosters. This affects complete church-level concentration analysis more than it affects the core person/network/action product.

Do not make full church-string normalization a launch blocker. Display coverage limitations wherever a church-level metric depends on incomplete matches.

### 5. Current-role/career completeness is uneven

Some people have rich current-role sources; many generated/roster-only people correctly have sparse profiles. This is consistent with the Tier A/B/C methodology.

The UI must not make sparse profile data look like a negative finding. Use explicit states such as `current role not normalized` or omit low-value empty panels.

## Analytical contract for v1

### Safe to expose

The final product may expose, with clear denominators and coverage notes:

- literal membership/action/role evidence;
- recurrence counts;
- shared-person counts;
- confirmed overlap between named datasets;
- proportion of the currently canonical NP subset appearing in a tracked action;
- conservative confirmed lower bounds against complete printed rosters;
- identity-resolution coverage;
- source-level roster sizes;
- score breakdown from explicitly score-included canonical edges;
- timelines of dated evidence;
- network/organization personnel continuity, explicitly labeled as personnel overlap.

### Do not expose as established findings

Do **not** present:

- `X times more likely` NP-vs-non-NP claims;
- odds ratios built by treating people without NP edges as non-members;
- causal claims that NP membership caused later actions;
- AMR or McGowan as an NP successor/front/equivalent solely from personnel recurrence;
- generic ideological labels as raw evidence;
- theology transferred through co-signature, family, church, committee, employment, education, or conference proximity;
- source absence as opposition.

### A Faithful PCA temporal caveat

The March 2022 AFP signer page is a cumulative snapshot of the 2021 public action, not an independent 2022 action. Do not count both snapshots as independent repeated behavior.

## Recommended product information architecture

Astra has design discretion, but the evidence model strongly supports the following user tasks.

### 1. Overview / research home

Should answer quickly:

- What is this project?
- What kinds of evidence are tracked?
- What is the current source universe?
- What are a few high-confidence descriptive findings?
- How do I search a person, organization, event, or source?

Avoid leading with a leaderboard.

### 2. People

Searchable/browsable directory with profile pages or deep-linked detail views.

A strong person profile should distinguish:

- current snapshot/status;
- evidence timeline;
- formal network membership/leadership;
- public actions;
- denominational actions;
- authored/first-person positions where normalized;
- institutional/career context;
- family/collaboration context;
- sources;
- score breakdown and zero-weight/excluded evidence;
- unresolved/uncertain claims clearly separated.

### 3. Networks / organizations

Profiles for important organizations/networks with:

- literal description/status;
- dated events;
- people by relationship type;
- sources;
- overlap with selected other actions/networks;
- explicit interpretive boundary where personnel overlap is not organizational succession.

### 4. Actions / events

This should become a first-class view.

Each event/action profile should show:

- what happened;
- date/year;
- source(s);
- literal action summary;
- complete source roster when available;
- canonical/resolved count;
- unresolved source-level rows;
- participant evidence kind;
- selected overlap/recurrence context.

The Garris letters are the required stress test for this architecture.

### 5. Analysis / overlap

Expose selected generated analysis, not raw noise.

Recommended modules:

- NP continuity dashboard with identity-coverage warning;
- selected dataset overlap explorer;
- recurring-person explorer;
- coverage/quality notes.

Every percentage must display its denominator and whether it is a resolved-subset statistic or full-roster lower bound.

### 6. Timeline

Cross-cutting timeline linking people, organizations, and actions. It should help the user distinguish historical sequence from asserted causation.

### 7. Sources / methodology

Searchable source register and concise methodology/definitions. Evidence should be reachable from claims in one or two interactions.

### 8. Institutions (optional/secondary)

Church/presbytery exploration can be included if it improves the product without overwhelming the run. It is lower priority than people/networks/actions/evidence/analysis.

## Visual/product direction

Astra has broad discretion to redesign the site. The target should feel like a serious research index / investigative archive, not a campaign page and not a raw admin table.

Design principles:

- evidence-first;
- dense but calm;
- explicit hierarchy between fact and analysis;
- neutral visual language for relationship types;
- strong typography and readable long-form evidence;
- mobile responsive;
- keyboard accessible;
- deep-linkable;
- performant as a static GitHub Pages site;
- no visual convention that implies zero-weight contextual edges are equivalent to formal membership/action edges.

The current earth/green visual language may be retained, refined, or replaced. Visual redesign is not constrained by the existing markup/CSS.

## Technical contract

### Static deployment

The public site should remain deployable on GitHub Pages without a server/database unless Astra identifies an overwhelming reason otherwise. Architectural refactoring of the static front end is permitted.

### Generated data

Astra may add generated app-facing JSON or scripts where useful. Prefer generating a clean presentation contract from normalized/canonical sources over teaching UI code to understand every research file shape independently.

### Existing validators

Do not weaken research guardrails to make the UI easier. Existing source/research validators remain authoritative. If a new app-facing projection is added, add an appropriate focused validator or extend repository validation.

### Testing cadence

During implementation, use targeted checks for coherent slices. Run the full repository/CI gates at the milestone/end rather than after every cosmetic edit.

## Representative end-to-end acceptance tests

The final heavy run should manually/automatically inspect at least these cases:

1. **Mike Khandjian** — NP membership/recruitment, distinct Khandjian Fellowship, AMR founding role, Garris Letter 1, current church role. The UI must not collapse the Fellowship into NP.
2. **David Cassidy** — AMR/McGowan/Garris recurrence but no canonical NP membership. The UI must not infer NP membership.
3. **Jeffrey Choi** — 2017 women/office authored evidence, 2026 Overture 37 advocacy, formal dissent, and institutional attribution boundary. The UI must not call him sole author/sponsor of the overture.
4. **Kathy Keller / Tim Keller** — reciprocal spouse context with no theology/score transfer.
5. **Hansoo Jin** — identity continuity while preserving the Warhurst printed spelling `Korean Capitol` rather than silently rewriting source text.
6. **Garris Letter 1** — all 60 printed rows visible, 25 linked to canonical profiles, 35 visibly unresolved without fabricated person identities; Letter 1 Jeff White remains distinct from Letter 2 Jeff White.
7. **Garris Letter 2** — all 21 rows canonically linked.
8. **National Partnership continuity** — show 68/151 identity coverage, selected overlap metrics, lower-bound language, and no predictive-ratio shortcut.
9. **James Kessler** — richer founder/principal-organizer NP edge remains distinct from ordinary generated member edges and retains weight 5.
10. **A zero-weight institutional/family/committee edge** — visible as context but clearly excluded from the index.

## Finish-line definition

The heavy run can be considered successful when:

- the product no longer depends on a people-table-first mental model;
- people, organizations/networks, events/actions, and sources are navigable first-class objects;
- complete source rosters can be displayed independently of canonical identity resolution;
- evidence kinds and scoring treatment are visible and understandable;
- source provenance is one or two interactions from every material claim;
- generated overlap/continuity analysis is selectively surfaced with denominators and caveats;
- the canonical index no longer mutates merely because the user changes a display confidence filter;
- representative profiles pass the inference guardrails above;
- no major research validator is weakened;
- the static site is polished on desktop and mobile;
- repository docs explain the final architecture and any consciously deferred gaps;
- final CI is green;
- the work ends in one reviewable PR and is not merged automatically.

## Deferred work that should not block v1

Unless the heavy audit discovers a material contradiction, defer:

- resolving all 151 NP identities;
- resolving all 35 remaining Garris Letter 1 identities;
- canonicalizing every historical GA roster;
- matching every AFP church string;
- reconstructing every historical renewal-network roster;
- completing every person's full career history;
- constructing an NP-vs-non-NP predictive model without a defensible comparison cohort.

Those are future enrichment tasks, not prerequisites for a credible evidence-driven v1.
