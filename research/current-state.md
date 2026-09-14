# Current Project State

Snapshot date: **2026-09-14**

This is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Repository state

The repository is an active source-driven PCA research graph, not a scaffold. It contains primary-source and provenance material, normalized research datasets, conservative person-identity crosswalks, canonical app-facing people/organizations/events/affiliations, generated overlap analysis, and focused CI validators.

Substantially developed areas now include:

- National Partnership correspondence and membership/action normalization, with exact person-level identity resolution focused on high-value recurrence rather than 151/151 completion;
- bounded National Partnership continuity/recurrence analysis across later PCA action and leadership datasets;
- A Faithful PCA / `Looking Forward – Together` signer data;
- Alliance for Mission & Renewal leadership, media, organizational framing, and issue-specific material;
- McGowan Global Institute roster evidence with independent NP-overlap boundaries;
- General Assembly formal actions across women/office, subscription, sexuality/Revoice, Overtures 23/37, Overture 15, NAE withdrawal, protests, minority reports, votes, and study committees;
- the complete 2017 Women Serving committee identity roster plus separate person-specific evidence for Jeffrey Choi, Kathy Keller, William Castro, and Mary Beth McGreevy;
- the 2026 women-deacons Overture 37 case with institutional/person attribution boundaries;
- Garris Letter 1 and Letter 2 complete printed signer rosters, canonical signer links, app projection, and overlap analysis;
- Save the PCA / Functional Female Officer external data;
- canonical PCA church/presbytery data and institution/RUF snapshots;
- zero-weight family/context edges such as Tim Keller ↔ Kathy Keller.

## Garris letters — current operational state

Primary sources are registered as `src-garris-letter-1` and `src-garris-letter-2`. Complete rosters are normalized in `sources/normalized/public-statements/garris-letters-2024.json`.

Current coverage:

- **Letter 1:** 60 printed signers; **25 canonical** and app-projected.
- **Letter 2:** 21 printed signers; **21/21 canonical** and app-projected.
- Every resolved signature is a confirmed `public_coalition_action` with weight **3** and `score_included: true` under the ordinary public-letter methodology.

Targeted receipts include:

- `sources/raw/identity/2024-garris-letter2-identity-evidence-2026-09-14.json`;
- `sources/raw/identity/np-garris-continuity-identity-evidence-batch1-2026-09-14.json` for David Lindberg and David Richmon.

Critical same-name boundary: Letter 1 `Jeff White` — New City Fellowship / Rio Grande — remains unresolved and must not be merged with Letter 2 `jeff-white-redeemer-downtown` from Redeemer Downtown / Metro NY.

Signing a Garris letter is a meaningful score-bearing public action. It does not by itself establish NP/AMR membership, agreement on unrelated controversies, or a generic ideological label.

## National Partnership continuity / recurrence analysis

Generated analysis lives under `analysis/national-partnership/`. Builder: `scripts/build-national-partnership-continuity-analysis.py`.

The analysis is descriptive rather than causal. It distinguishes confirmed canonical overlap, conservative full-roster lower bounds, and unresolved exact-name screening possibilities.

Current NP identity coverage:

- **151** confirmed printed-name NP members;
- **54** confirmed canonical person identities;
- canonical identity coverage: **35.76%**.

The canonical subset is not assumed to be random; recurring/high-profile people are generally easier to resolve. Percentages inside the canonical subset must therefore be paired with full-roster lower bounds.

Current descriptive signals include:

- **AMR current leadership:** 4 of 6 leaders are confirmed NP members — David Richter, Geoff Ziegler, Joel St. Clair, and Sean Lucas (**66.67%**). This is strong personnel-continuity evidence, not proof of formal organizational succession.
- **A Faithful PCA, June 2021:** **40** confirmed NP overlaps; **74.07%** of the 54-person canonical NP subset and a **26.49% lower bound** against all 151 confirmed printed NP names; **10** exact-name possibilities remain unresolved.
- **A Faithful PCA, March 2022 cumulative snapshot:** **43** confirmed overlaps; **11** unresolved exact-name possibilities. This is a cumulative snapshot of the 2021 action, not an independent later event.
- **2019 Warhurst protest:** **22** confirmed NP overlaps plus **9** unresolved exact-name possibilities.
- **2022 Overture 15 negative votes:** **20 confirmed NP overlaps**, **0 unresolved exact-name possibilities**. Against all 200 recorded negative votes, confirmed overlap is a **10.0% lower bound**; against the full 151-name NP roster, **13.25%** are confirmed in this action.
- **2022 NAE-withdrawal protest:** **10 confirmed NP overlaps**, **0 unresolved exact-name possibilities**. Against all 203 protest signers, confirmed overlap is a **4.93% lower bound**; against the full 151-name NP roster, **6.62%** are confirmed in this action.
- **Garris Letter 1:** **10 confirmed NP overlaps among 25 resolved signers**; **40.0%** of resolved signers and a **16.67% lower bound** across the complete 60-name roster.
- **Garris Letter 2:** 0 confirmed NP overlaps and 0 unresolved exact-name NP overlaps.

The O15/NAE reviewed identity receipt is:

`sources/raw/identity/np-postarchive-identity-evidence-batch1-2026-09-14.json`

It resolves 11 people: Ben Lyon, Bruce O'Neil, Bruce Terrell, Jeremy Fair, Justin Edgar, Luke Evans, Omar Ortiz, Peter Rowan, Rob Wootton, Tim LeCroy, and Nate Conrad. Historical presbytery changes and anomalous source labels are preserved rather than normalized away. In particular, Jeremy Fair's NP presbytery label conflicts with later/official context, and Justin Edgar's NP source contains a nonstandard presbytery label; the identity decisions do not validate those printed labels as accurate official presbytery names.

Predictive-validity boundary: the repository is **not yet ready for an `X times more likely` NP-vs-non-NP claim**. No canonical NP edge means membership is not established in the current graph, not that the person is a confirmed non-member. A defensible predictive estimate would still require a genuinely opportunity-aware comparison cohort, better bounded NP status in that comparison universe, separation of within-archive recurrence from post-archive outcomes, and treatment of correlated actions as related rather than independent trials.

## McGowan Global Institute / National Partnership overlap

`sources/normalized/institutions/mcgowan-global-team-2026.json` tracks Bruce O'Neil, Mike Khandjian, David Cassidy, Ray Cortese, and Bob Flayhart as McGowan Global Institute `Consultant, Coach` roles. These institutional roles are weight 0.

Independent NP evidence exists for O'Neil, Khandjian, Cortese, and Flayhart. No canonical NP membership evidence is currently present for Cassidy; his AMR/Garris/McGowan connections are not a substitute for NP evidence. Personnel recurrence does not by itself establish McGowan as a successor, front, continuation, or ideological equivalent of NP or AMR.

## Family relationships

`sources/normalized/identity/family-relationships-2026.json` includes Tim Keller ↔ Kathy Keller as confirmed spouses. Family edges are reciprocal, weight 0, and score-excluded; they never transfer theology, membership, actions, or score.

## 2017 Women Serving / women-office evidence

All 12 official committee identities are canonical and app-projected. Committee service remains weight 0 and must not be treated as blanket agreement with every report statement or internal school.

Separate attributable evidence is normalized for Jeffrey Choi, Kathy Keller, William Castro, and Mary Beth McGreevy. Choi's 2017 local-session-discretion argument remains distinct from his 2026 Overture 37 advocacy and formal dissent.

## 2026 Overture 37

Pacific Presbytery is the formal submitting body. Jeffrey Choi is separately documented as a public advocate, floor speaker in support, and one of the later formal dissent's four named submitters. Current primary evidence does not establish him as sole author, drafter, sponsor, or orchestrator of the overture itself.

## Immediate next slice

Do **one targeted National Partnership residual identity/pinning pass**, not broad identity cleanup.

Priority order:

1. Review the highest-value remaining NP ↔ A Faithful PCA / Warhurst exact-name possibilities, prioritizing people who recur in multiple independent datasets or materially change person/network profiles.
2. Normalize any still-missing exact NP archive page/message pins for already important canonical people where that improves app-facing evidence quality.
3. Do **not** chase 151/151 NP identity completion or resolve long-tail names solely to improve a percentage.
4. After that residual pass, perform a compact **pre-UI research-gap/readiness audit**: identify only source/model gaps that would materially change the intended app, decide whether any opportunity-aware comparison cohort is defensible, and freeze the analytical boundaries the UI must display.
5. Only add another normal-chat cleanup slice if that audit identifies a material gap. Otherwise move to the heavy Sol/Astra gap-audit/UI/end-to-end phase.

Garris Letter 1 identity resolution can continue opportunistically when it improves another high-value cross-source question; there is no need to complete all 35 unresolved Letter 1 names.

## Documentation maintenance rule

Update this file when a meaningful merge changes the latest completed data state, immediate next slice, major source-family status, or a material unresolved identity/evidence boundary. Keep it concise enough that a fresh agent can orient before inspecting implementation details.
