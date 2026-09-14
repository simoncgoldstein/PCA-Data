# V1 evidence explorer architecture

Implementation date: 2026-09-14. Static GitHub Pages application; no backend, bundler, external font, analytics, or runtime dependency.

## Public information architecture

- Overview: research purpose, global entity search, source-universe metrics, and suggested evidence paths. No default leaderboard.
- People: paginated searchable directory and deep-linked profiles. Canonical typed ledger, role sources and dates, preserved identity-review conflicts, separate authored evidence, complete source occurrences, and an expandable full score ledger.
- Networks / organizations: literal framing, people grouped by relationship, related actions, sources, and links to relevant rosters / continuity analysis.
- Actions / timeline: dated event profiles with complete projected source rosters where available, identity coverage, canonical participant evidence, and selected overlap.
- Detective map: SVG relational explorer with node dragging, background panning, wheel/pinch/button/keyboard zoom, neighborhood depth, source scope, evidence layer, confidence, category, context, and unresolved-row filters. Select a node or line to inspect its source and treatment. Profiles link to their two-step neighborhoods.
- Overlap / continuity: selected generated NP comparisons, shared-person lists, canonical-subset and full printed-name denominators, and lower-bound / non-random-coverage cautions.
- Sources / methodology: searchable source profiles, claim backlinks, local/archive provenance, definitions, and inference boundaries.
- Source datasets: all 62 crosswalk datasets and all 4,415 preserved occurrences, independently navigable even without canonical people.
- Institutions: secondary directory of 1,970 churches and 88 presbyteries; explicit snapshot and incomplete-match boundaries.

Hash routes support GitHub Pages subpaths and browser history. Examples: `#person/jeffrey-choi`, `#event/evt-garris-letter-1`, `#dataset/garris_letter_1`, `#map?focus=person:mike-khandjian&depth=2`, `#analysis?dataset=warhurst_protest_2019`. Legacy `#person=...` links continue to work. Directory filters and pagination are encoded in the URL. Major controls use native links, forms, buttons, and details elements.

## Files and data flow

- `index.html`: accessible static application shell.
- `styles.css`: responsive visual system and map styling.
- `app.js`: routes, entity views, lazy data loading, and rendering.
- `ui/model.mjs`: pure score, filter, grouping, safe URL, and route helpers.
- `ui/graph.mjs`: pure graph construction plus SVG layout / interactions. Layout distance is not a metric or evidence of proximity.
- `scripts/build-explorer.py`: deterministic presentation projection, run after canonical projectors and overlap builders.
- `data/explorer.json`: dataset coverage / associations, separately attributable positions and their source registrations, and reviewed identity-boundary notes.
- `data/source-occurrences.json`: every crosswalk occurrence, grouped by dataset; lazily loaded for profiles, actions, rosters, and the map.

The home page does not load the occurrence archive or full church directory. The archive is fetched once and cached for subsequent exploration. The directory is loaded only for views needing institutional names. Source rosters render all matching rows, including all 60 Garris Letter 1 signers. Large directories use pagination. An excessively broad map (>700 matching nodes, typically from enabling all unresolved source rows) asks for a narrower neighborhood rather than silently dropping records or freezing the browser.

## Presentation contract

Source occurrence is not canonical identity and is not a canonical affiliation. Each projected occurrence retains its crosswalk ID, dataset, printed name, source path and locator, reviewed identity status, optional canonical person ID, normalized context, conflicts, and identity note. Explicitly mapped action datasets also retain event and source IDs.

Supported original signer/voter shapes and NP membership records retain their original printed fields and archival evidence in `printed_record`. Garris retains order, office, institution, presbytery, and source linkage exactly. Other source shapes retain explicitly labeled normalized context and a link to the full normalized record. No normalized context is labeled verbatim source text.

The projection trusts only `exact_confirmed` / `context_confirmed` crosswalk IDs. It does not run an additional name matcher, create canonical people, modify affiliations, or assign new scores. Original-row recovery requires a source sequence and printed name; NP recovery uses the exact normalized roster's canonical printed name. The existing source pipeline remains authoritative.

The named women-serving authors' positions and Choi's public advocacy are explicitly attributable supplemental records, all excluded from the index. Existing committee, floor-speech, and dissent edges retain their independent semantics. Unscored supplemental positions do not mean uncertain attribution; their source-specific attribution basis is shown without inventing a confidence field absent from the normalized source.

## Scoring and graph semantics

The canonical index is always the sum of explicitly included canonical affiliations, excluding unresolved confidence even if an invalid record accidentally marks inclusion true. Directory and profile visibility filters never change it. Each profile shows included/excluded treatment and actual weights for all canonical edges.

Source rows never add points. They can repeat snapshots, receipts, and the same person's appearance within a dataset. The graph deduplicates person-to-dataset display lines but leaves all source rows intact in the roster. A source line carries its original occurrence, not an inferred canonical membership or an independent-action count. Canonical event ownership lines are structural context. Family lines remain zero-weight. Unresolved graph nodes use source-occurrence IDs and are explicitly labeled, never assigned a canonical person ID.

A Faithful PCA June 2021 and March 2022 remain snapshots of one action. Analysis denominators distinguish source rows, distinct printed names, linked rows, and distinct canonical people. NP's 68/151 coverage is not a random sample. No predictive or causal comparison is implemented.

## Validation and maintenance

Run focused checks while editing:

```sh
python3 scripts/build-explorer.py .
python3 scripts/validate-explorer.py .
node --test tests/model.test.mjs
node --check app.js
node --check ui/graph.mjs
```

The main research workflow rebuilds the projection after canonical and analytical builders and requires a clean diff. `validate-explorer.yml` additionally runs every topic/repository Python validator, schema validation, deterministic projection checks, model tests, and Playwright browser acceptance. Browser screenshots and the acceptance result are retained as CI artifacts. Playwright is a pinned CI-only dependency, not shipped to site visitors.

Browser acceptance covers all ten finish-line representative cases, confidence-score invariance, Garris 60/25/35 and 21/21, the Jeff White distinction, navigation/history, desktop/mobile overflow, map zoom/pan/node dragging, line inspection, and explicit empty states.

When sources or crosswalks change, regenerate rather than hand-edit either presentation JSON. Add explicit dataset associations only where an action or organization relationship is supported. Update source adapter and projection tests together when a normalized input shape changes. Do not convert supplemental occurrences into canonical scoring edges just to increase a displayed score.
