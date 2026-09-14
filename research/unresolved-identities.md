# Unresolved / Pending Verification

Audit date: **2026-09-14**

These items are deliberately kept outside confirmed public claims until further sourcing or canonicalization is completed.

## Garris Letter 1 signer identities

The Garris source-ingestion layer is complete, but Letter 1 still has **35 unresolved signer rows** after conservative cross-source matching. Letter 2 is complete at 21/21 canonical identities.

Policy for the remaining Letter 1 queue:

- resolve in small reviewed batches using independent church, ministry, presbytery, or official denominational context;
- prioritize people who recur elsewhere in the graph or materially improve overlap analysis;
- do not relax the global same-name resolver merely to raise completion percentage;
- preserve printed office/church/presbytery context and the original source row;
- keep Letter 1 `Jeff White` (New City Fellowship / Rio Grande) unresolved unless independent evidence establishes that specific identity. It is not the reviewed Letter 2 `Jeff White` from Redeemer Downtown / Metro NY.

A resolved signature is weight 3 as a public-letter action, but identity resolution does not add unrelated network memberships or issue positions. Every printed signer remains preserved as a source-level data point whether or not canonical identity is resolved.

The targeted NP ↔ Garris Letter 1 exact-name queue is complete: David Lindberg and David Richmon are reviewed canonical matches.

## 2017 Women Serving committee

**Identity resolution is complete.** All 12 official committee members are canonically linked and projected to the app-facing committee event. Committee service remains zero-weight and does not establish agreement with every report statement; person-specific authored material is normalized separately.

Reviewed canonical IDs:

- Leon Brown — `leon-brown`
- William Castro — `william-castro`
- Jeffrey Choi — `jeffrey-choi`
- Dan Doriani — `dan-doriani`
- Ligon Duncan — `ligon-duncan`
- Irwyn Ince — `irwyn-ince`
- Lani Jones — `lani-jones`
- Kathy Keller — `kathy-keller`
- Mary Beth McGreevy — `mary-beth-mcgreevy`
- Bruce O'Neil — `bruce-o-neil`
- Harry Reeder — `harry-reeder`
- Roy Taylor — `roy-taylor`

## 2026 Overture 37 attribution boundary

Current evidence establishes Pacific Presbytery as the formal submitting body for Overture 37. Jeffrey Choi is documented as a public advocate, floor speaker in support, and one of four co-authors/submitters of the later formal dissent.

**Not established:** that Choi was the sole author, drafter, sponsor, or orchestrator of the overture itself. Preserve that distinction unless additional primary evidence is found.

## National Partnership identity coverage and archival pins

The normalized NP source layer contains **151 confirmed printed-name members**, and **68** now have confirmed canonical person identities. That **45.03%** canonical coverage remains incomplete and plausibly non-random because people who recur elsewhere are easier to identity-resolve.

Consequences:

- no current canonical NP edge means **membership not established in the current canonical graph**, not confirmed non-membership;
- do not calculate NP-vs-non-NP risk ratios by assigning everyone without a canonical NP edge to a non-member comparison group;
- unresolved exact-name overlaps are research leads only, not confirmed identity matches;
- canonical NP membership is deterministically projected to the app graph, one edge per canonical member, while richer manually curated NP edges take precedence.

Completed targeted continuity queues:

1. **NP ↔ Garris Letter 1:** exact-name queue complete; 10 confirmed overlaps, 25/60 Letter 1 signers canonical.
2. **NP ↔ 2022 Overture 15 negative votes:** exact-name queue complete; **20 confirmed overlaps, 0 unresolved exact-name possibilities**.
3. **NP ↔ 2022 NAE-withdrawal protest:** exact-name queue complete; **10 confirmed overlaps, 0 unresolved exact-name possibilities**.
4. **NP ↔ A Faithful PCA June 2021:** residual exact-name queue complete; **50 confirmed overlaps, 0 unresolved exact-name possibilities**.
5. **NP ↔ A Faithful PCA March 2022 cumulative snapshot:** residual exact-name queue complete; **54 confirmed overlaps, 0 unresolved exact-name possibilities**.
6. **NP ↔ 2019 Warhurst protest:** residual exact-name queue complete; **31 confirmed overlaps, 0 unresolved exact-name possibilities**.

Reviewed receipts:

- `sources/raw/identity/np-postarchive-identity-evidence-batch1-2026-09-14.json` — O15/NAE identity review;
- `sources/raw/identity/np-residual-identity-evidence-batch2-2026-09-14.json` — 18 reviewed AFP/Warhurst identity decisions.

Preserve reviewed source-boundary caveats:

- Jeremy Fair's NP presbytery label conflicts with later/official denominational context; the identity resolution does not validate the NP printed label as accurate.
- Justin Edgar's NP archive row contains a nonstandard presbytery label; preserve it as source text rather than normalizing it into an official presbytery claim.
- David Ridenhour's NP archival presbytery wording conflicts with official 2018–2019 North Texas evidence; resolving the person does not certify the NP label.
- Tag Tuck has a source-level TE/RE conflict; do not harmonize the office classification without separate evidence.
- Hansoo Jin is canonically resolved across NP / Warhurst / A Faithful PCA while the Warhurst source spelling `Korean Capitol` remains preserved verbatim; NP/AFP print `Korean Capital`.

At this point, **do not begin another general NP identity batch**. The remaining long tail can be resolved opportunistically when it materially affects a prominent profile, source claim, or future UI feature. Do not pursue full 151/151 identity completion merely to improve coverage.

Generated continuity analysis:

`analysis/national-partnership/continuity-summary.json`

## Prayer & Lament later commitment list

The public page exposes the initial signatories but does not establish the full later commitment list as a clean verified roster. A raw scrape supplied during research includes duplicates, malformed entries, and apparent disruptive submissions.

Policy:

- do not bulk-import the raw scrape as confirmed people;
- independently corroborate later signers;
- preserve original rows only as research provenance until verified.

## Current-role normalization

Current roles still require refresh or careful dated treatment for a number of people. A 2024 source may establish a role at that date without proving that the role is still current in 2026.

## Denominational status

For people now serving primarily in adjacent institutions, distinguish current PCA Teaching Elder / Ruling Elder status, former PCA minister, minister out of bounds, current presbytery, and status not established. Do not infer current ecclesiastical status from an old biography.

## Historical renewal networks

The following areas remain candidates for later reconstruction but are not prerequisites for the immediate UI phase unless the gap audit shows they materially affect the intended product:

- 2006 Presbyterians and Presbyterians Together roster and role taxonomy;
- 2008 Denominational Renewal organizers versus speakers versus respondents;
- Common Grounds participant categories;
- Beautiful Orthodoxy organizers and speakers;
- Semper Ref leadership and participation;
- Khandjian Fellowship roster over time.

## Identity collisions

Common names require institutional, office, presbytery, location, or other contextual evidence before merging records. A same-name match is not sufficient evidence.

Reviewed aliases and name variants are person-specific decisions. Do not generalize one reviewed nickname, middle-initial, spelling equivalence, or historical-move decision into a global matching rule.

## Maintenance

When an unresolved item is resolved, update this file or remove the stale entry in the same milestone if practical. `research/current-state.md` should summarize only unresolved items that materially affect the immediate next slice; this file can retain the broader queue.
