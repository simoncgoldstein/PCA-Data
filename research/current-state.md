# Current Project State

Snapshot date: **2026-09-14**

This is the dated handoff for a fresh research or coding agent. Read it after `AGENTS.md` and `README.md`.

## Repository state

The repository is an active source-driven PCA research graph, not a scaffold. It contains primary-source and provenance material, normalized research datasets, conservative person-identity crosswalks, canonical app-facing people/organizations/events/affiliations, generated overlap analysis, and focused CI validators.

Substantially developed areas now include:

- National Partnership correspondence and membership/action normalization, with some exact person-level archival pinning still incomplete;
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

- **Letter 1:** 60 printed signers; **24 currently canonical** and app-projected.
- **Letter 2:** 21 printed signers; **21/21 canonical** and app-projected.
- Every resolved signature is a confirmed `public_coalition_action` with the methodology's ordinary public-letter weight **3** and `score_included: true`.
- The score records documented participation in this tracked public action. It is not itself a judgment of orthodoxy, Christian character, or every theological position of the signer.

Letter 2 required a reviewed identity pass for Metro New York and adjacent signers. The provenance receipt is:

`sources/raw/identity/2024-garris-letter2-identity-evidence-2026-09-14.json`

Nineteen Letter 2 rows received targeted independent identity corroboration; seven identities that remained blocked by generic resolver collision/context safeguards were applied as person-specific canonical seeds. The global identity threshold was not weakened.

Critical same-name boundary:

- Letter 1 `Jeff White` — New City Fellowship / Rio Grande — **remains unresolved**.
- Letter 2 `Jeff White` — Redeemer Downtown / Metro NY — resolved as `jeff-white-redeemer-downtown`.
- Never merge those two rows merely because the printed name is identical.

Interpretive boundary: signing one of the Garris letters is a meaningful, score-bearing public denominational action and is appropriate for downstream coalition/trajectory analysis. It does **not by itself** establish National Partnership membership, AMR membership, agreement on unrelated controversies, or a generic ideological label such as `big tent`. Such interpretation should arise downstream from multiple independently sourced actions/relationships.

Reproducibility:

- `scripts/build-person-crosswalk.py` ingests Letter 1 and Letter 2 as separate source families.
- `scripts/project-garris-signers.py` deterministically projects all resolved signer rows to app affiliations.
- repository-wide generated-output validation reruns the person crosswalk, the Garris signer projection, and overlap analysis before requiring a clean git diff.
- `scripts/validate-garris-letter-signers.py` protects roster completeness, scoring semantics, app linkage, Letter 2 completeness, and the Jeff White identity boundary.

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

Continue **Garris Letter 1 identity resolution in compact reviewed batches**, prioritizing signers who recur elsewhere in the repository or whose printed church/presbytery context can be independently corroborated without ambiguity.

For that work:

1. Start from the 36 unresolved Letter 1 rows in `garris-letters-2024.json` / the generated review queue.
2. Prefer already recurring/high-value graph people and exact first-party/official ministry context.
3. Record reviewed identity evidence in a receipt rather than relaxing global name-matching rules.
4. Preserve the distinct Letter 1 Jeff White unless independent New City Fellowship / Rio Grande evidence resolves him.
5. Rerun crosswalk → Garris projection → overlap analysis and keep the focused validator forward-compatible as Letter 1 coverage increases.

After one or two efficient Letter 1 batches, the next broad operational priority should be exact National Partnership person-level message/page pinning and remaining high-value GA action/source gaps. Do not make broad ideological-position scoring the next data-ingestion phase; let the eventual UI/analysis layer synthesize independently sourced actions.

## Documentation maintenance rule

Update this file when a meaningful merge changes the latest completed data state, immediate next slice, major source-family status, or a material unresolved identity/evidence boundary. Keep it concise enough that a fresh agent can orient before inspecting implementation details.
