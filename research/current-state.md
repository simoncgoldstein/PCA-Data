# Current Project State

Snapshot date: **2026-09-14**

This is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Repository state

The repository is an active source-driven PCA research graph, not a scaffold. It contains primary-source and provenance material, normalized research datasets, conservative person-identity crosswalks, canonical app-facing people/organizations/events/affiliations, generated overlap analysis, and focused CI validators.

Substantially developed areas now include:

- National Partnership correspondence and membership/action normalization, with some exact person-level archival pinning and identity resolution still incomplete;
- a bounded National Partnership continuity/recurrence analysis across later PCA action and leadership datasets;
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

Primary sources are registered as:

- `src-garris-letter-1` — `Report Concerning the Christian Character of TE Zachary Garris`;
- `src-garris-letter-2` — `Letter to Rio Grande Presbytery Concerning TE Zachary Garris`, dated June 6, 2024.

Normalized complete rosters:

`sources/normalized/public-statements/garris-letters-2024.json`

Current coverage:

- **Letter 1:** 60 printed signers; **25 currently canonical** and app-projected.
- **Letter 2:** 21 printed signers; **21/21 canonical** and app-projected.
- Every resolved signature is a confirmed `public_coalition_action` with the methodology's ordinary public-letter weight **3** and `score_included: true`.
- The score records documented participation in this tracked public action. It is not itself a judgment of orthodoxy, Christian character, or every theological position of the signer.

Letter 2 required a reviewed identity pass for Metro New York and adjacent signers. The provenance receipt is:

`sources/raw/identity/2024-garris-letter2-identity-evidence-2026-09-14.json`

The targeted NP-continuity review also resolved David Lindberg and David Richmon in Letter 1. Its receipt is:

`sources/raw/identity/np-garris-continuity-identity-evidence-batch1-2026-09-14.json`

Richmon is tied deterministically through Pacific Northwest and the Green Lake → Trinity Seattle church history. Lindberg is a reviewed historical-continuity decision: NP evidence places him in Metro Atlanta in 2018, contemporaneous sources identify the same PCA minister at ChristChurch Atlanta, byFaith records his later move to Covenant Presbyterian in Cherry Hill, and 2024 official/first-party sources place TE David Lindberg at Christ the King / North Texas. Preserve those presbytery changes as dated facts rather than rewriting them into a same-context match.

Critical same-name boundary:

- Letter 1 `Jeff White` — New City Fellowship / Rio Grande — **remains unresolved**.
- Letter 2 `Jeff White` — Redeemer Downtown / Metro NY — resolved as `jeff-white-redeemer-downtown`.
- Never merge those two rows merely because the printed name is identical.

Interpretive boundary: signing one of the Garris letters is a meaningful, score-bearing public denominational action and is appropriate for downstream coalition/trajectory analysis. It does **not by itself** establish National Partnership membership, AMR membership, agreement on unrelated controversies, or a generic ideological label such as `big tent`. Such interpretation should arise downstream from multiple independently sourced actions/relationships.

Reproducibility:

- `scripts/build-person-crosswalk.py` ingests Letter 1 and Letter 2 as separate source families.
- `scripts/project-garris-signers.py` deterministically reconciles resolved signer rows to app affiliations, including removal of stale signer edges after an identity correction.
- repository-wide generated-output validation reruns the person crosswalk, the Garris signer projection, overlap analysis, and the National Partnership continuity analysis before requiring a clean git diff.
- `scripts/validate-garris-letter-signers.py` protects roster completeness, scoring semantics, app linkage, Letter 2 completeness, and the Jeff White identity boundary.
- `scripts/validate-np-garris-identity-batch1.py` protects the reviewed Lindberg/Richmon identity decisions and their continuity-analysis impact.

## National Partnership continuity / recurrence analysis

Generated analysis lives under:

`analysis/national-partnership/`

Builder:

`scripts/build-national-partnership-continuity-analysis.py`

The analysis is intentionally descriptive rather than causal. It distinguishes confirmed canonical overlap, conservative full-roster lower bounds, and unresolved exact-name screening possibilities.

Current NP identity coverage:

- **151** confirmed printed-name NP members in the normalized source roster;
- **45** currently have confirmed canonical person identities;
- canonical identity coverage is therefore **29.8%**.

Because recurring people are generally easier to identity-resolve, the 45-person canonical subset is not assumed to be an unbiased random sample of all 151 confirmed printed-name NP members. Percentages calculated only inside the canonical subset can therefore overstate recurrence and must be paired with full-roster lower bounds.

Current descriptive signals include:

- **AMR current leadership:** 4 of 6 confirmed leaders are also confirmed canonical NP members — David Richter, Geoff Ziegler, Joel St. Clair, and Sean Lucas. This is strong personnel-continuity evidence, but not by itself proof that AMR is a formal/legal/organizational successor to NP.
- **A Faithful PCA, June 2021:** 36 confirmed overlaps. That is 80.0% of the currently canonical NP subset, with a **23.84% confirmed lower bound** against the full 151-name NP roster; 14 additional exact-name overlaps remain unresolved.
- **A Faithful PCA, March 2022 cumulative snapshot:** 37 confirmed overlaps plus 17 unresolved exact-name possibilities.
- **Garris Letter 1:** **10 confirmed NP overlaps among 25 resolved signers**; the targeted exact-name NP/Garris queue is now exhausted. Against the full 60-name Letter 1 roster, the confirmed NP overlap is a **16.67% lower bound**.
- **Garris Letter 2:** 0 confirmed NP overlaps and 0 unresolved exact-name NP overlaps.
- **2022 Overture 15 negative votes:** 10 confirmed NP overlaps plus 10 unresolved exact-name possibilities.
- **2022 NAE-withdrawal protest:** 5 confirmed NP overlaps plus 5 unresolved exact-name possibilities.

Predictive-validity boundary:

The repository is **not yet ready for an `X times more likely` NP-vs-non-NP claim**. Do not treat a person with no current canonical NP edge as a confirmed non-member. A defensible predictive estimate first requires materially better NP identity coverage, an opportunity-aware comparison cohort, separation of within-archive recurrence from truly post-archive outcomes, and treatment of correlated actions as related rather than independent trials.

The analysis and validator explicitly prohibit the shortcut of calculating risk/odds ratios by treating all people without canonical NP membership as non-members.

## McGowan Global Institute / National Partnership overlap

`sources/normalized/institutions/mcgowan-global-team-2026.json` tracks Bruce O'Neil, Mike Khandjian, David Cassidy, Ray Cortese, and Bob Flayhart as McGowan Global Institute `Consultant, Coach` roles. Those institutional roles are weight 0.

Independent NP evidence exists for O'Neil, Khandjian, Cortese, and Flayhart. No canonical NP membership evidence is currently present for Cassidy; his AMR/Garris/McGowan connections must not be converted into NP membership without independent evidence. Personnel recurrence is analytically useful but does not by itself establish that McGowan is an NP/AMR successor, front, or ideological equivalent.

## Family relationships

`sources/normalized/identity/family-relationships-2026.json` currently includes Tim Keller ↔ Kathy Keller as confirmed spouses. Family edges are reciprocal, `weight: 0`, and `score_included: false`; they never transfer theology, committee service, network membership, public actions, or score between people.

## 2017 Women Serving / women-office evidence

All 12 official committee identities are canonical and app-projected. Committee service remains weight 0 and must not be treated as blanket agreement with every report statement or internal school.

Separate attributable evidence is normalized for Jeffrey Choi, Kathy Keller, William Castro, and Mary Beth McGreevy. Choi's 2017 local-session-discretion argument is kept distinct from his 2026 Overture 37 advocacy and formal dissent. Kathy Keller's male authoritative-teaching/elder boundary is kept alongside her broad stated support for other ministry by women. Castro's stricter ordinary-public-worship speech position is person-specific rather than inferred from committee service.

## 2026 Overture 37

Pacific Presbytery is the formal submitting body for Overture 37. Jeffrey Choi is separately documented as a public advocate, floor speaker in support, and one of the later formal dissent's four named submitters. Current primary evidence does not establish Choi as the sole author, drafter, sponsor, or orchestrator of the overture itself.

## Immediate next slice

Continue **targeted National Partnership identity resolution for post-archive continuity analysis**, not broad identity cleanup for its own sake.

Priority order:

1. Review the **10** unresolved exact-name NP possibilities in the 2022 Overture 15 negative-vote dataset.
2. Review the **5** unresolved exact-name NP possibilities in the 2022 NAE-withdrawal protest dataset. Combine with the O15 batch if the evidence is straightforward; split only if collision/history review makes the PR unwieldy.
3. Then do one targeted pass over the highest-value remaining NP ↔ A Faithful PCA / Warhurst exact-name possibilities and any important NP archival pins that materially affect recurrent-person profiles. Do not chase full 151/151 NP identity completion for its own sake.
4. After those identity passes, perform a compact pre-UI research-gap audit: decide whether an opportunity-aware comparison cohort is actually defensible with current data and identify only source gaps that materially affect the intended UI/analysis.

Only after identity coverage materially improves should the project construct an opportunity-aware comparison cohort for a formal predictive-validity estimate. Do **not** add risk ratios or odds ratios before that denominator problem is solved.

Garris Letter 1 identity resolution can continue opportunistically when it improves another high-value cross-source question; there is no need to complete all 35 unresolved Letter 1 names before moving to higher-information work.

## Documentation maintenance rule

Update this file when a meaningful merge changes the latest completed data state, immediate next slice, major source-family status, or a material unresolved identity/evidence boundary. Keep it concise enough that a fresh agent can orient before inspecting implementation details.
