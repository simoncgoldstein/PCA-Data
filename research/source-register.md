# Source Register

Audit date: **2026-09-14**

This is the human-readable companion to `data/sources.json` and the evidence archive under `sources/`.

Source layers:

- `data/sources.json` — machine-facing source IDs used by app entities and affiliations;
- `sources/raw/` — primary files, snapshots, receipts, and provenance material;
- `sources/normalized/` — structured datasets derived from sources;
- `sources/manifests/` — provenance / redistribution metadata;
- `research/companion-corpus.md` — relationship to the private Google Drive research corpus.

## National Partnership correspondence, 2013–2021

Archive index: https://jude3pca.org/national-partnership-emails/

Status: **substantially ingested; some exact person-level archival pinning remains incomplete**.

The repository has canonical membership/action normalization, addition/committee rosters, and identity work. Continue to distinguish explicit membership from recruitment, promoted candidates, committee-placement recommendations, and adjacency.

Recent exact app-facing pins include:

- Bruce O'Neil — 2018 NP-guys committee rosters, archive pp. 264–265;
- Mike Khandjian — explicit NP-member language in 2014 plus Partnership-men roster evidence; his independently created Fellowship remains distinct despite high overlap;
- Ray Cortese — March 11, 2013 additions record, archive p. 17;
- Bob Flayhart — February 11, 2013 additions record, archive p. 3.

David Cassidy is not in the current canonical NP membership dataset. His AMR/McGowan/Garris connections are not a substitute for NP evidence.

## Garris letters, 2024

Status: **complete printed rosters normalized; Letter 2 fully canonical; Letter 1 partially canonical and queued for reviewed identity batches**.

Primary machine-facing sources:

- `src-garris-letter-1` — `Report Concerning the Christian Character of TE Zachary Garris`;
- `src-garris-letter-2` — `Letter to Rio Grande Presbytery Concerning TE Zachary Garris`, dated June 6, 2024.

Normalized complete rosters:

`sources/normalized/public-statements/garris-letters-2024.json`

Current coverage:

- Letter 1: **60** printed signers; **24** canonical/app-projected;
- Letter 2: **21** printed signers; **21/21** canonical/app-projected;
- confirmed signatures are `public_coalition_action`, weight **3**, and score-included under the ordinary public-letter/protest methodology.

Letter 2 identity provenance:

`sources/raw/identity/2024-garris-letter2-identity-evidence-2026-09-14.json`

That receipt preserves targeted independent church/ministry/official corroboration for 19 Letter 2 rows. Seven identities that remained blocked by generic collision/context safeguards were applied as person-specific reviewed canonical seeds; the global identity threshold was not weakened.

Critical same-name boundary:

- Letter 1 `Jeff White` — New City Fellowship / Rio Grande — unresolved;
- Letter 2 `Jeff White` — Redeemer Downtown / Metro NY — `jeff-white-redeemer-downtown`.

Do not merge those rows from name alone.

A signature establishes participation in that specific letter and its request for presbytery investigation. It is a meaningful formal action for recurrence/coalition analysis, but it does not by itself establish National Partnership or AMR membership, agreement on unrelated controversies, or a generic ideological label.

Reproducibility path:

`build-person-crosswalk.py -> project-garris-signers.py -> build-overlap-analysis.py`

Repository-wide CI reruns that path and requires a clean diff. `scripts/validate-garris-letter-signers.py` separately protects roster completeness, weight/scoring semantics, app linkage, Letter 2 completeness, and the Jeff White boundary.

## McGowan Global Institute

Status: **current first-party roster normalized with bounded overlap analysis**.

Machine-facing source: `src-mcgowan-global-team-2026` (`Who We Are`).

Normalized record:

`sources/normalized/institutions/mcgowan-global-team-2026.json`

The tracked roster includes Bruce O'Neil, Mike Khandjian, David P. Cassidy, Ray Cortese, and Bob Flayhart as `Consultant, Coach`. McGowan roles are app-visible but weight 0 / score-excluded.

O'Neil, Khandjian, Cortese, and Flayhart independently overlap the canonical NP dataset. Cassidy does not currently have an NP membership record. Personnel recurrence does not establish McGowan as a successor, front, continuation, or ideological equivalent of NP, the Khandjian Fellowship, or AMR.

## PCA General Assembly records

Status: **substantial normalized coverage**.

Coverage includes, among other areas:

- women/office and women-in-ministry records;
- confessional-subscription / Federal Vision formal records;
- 2016–17 Women Serving committee/report material;
- 2019 Warhurst protest material;
- Human Sexuality Ad Interim Committee material;
- 2021 Overtures 23/37 and related minority-report / recorded-vote evidence;
- 2022 Overture 15 and NAE-withdrawal material;
- 2026 Overture 37 on ordained women deacons, including Pacific Presbytery sponsorship, Assembly disposition, Jeffrey Choi advocacy/floor activity, and the later formal dissent.

Remaining work includes systematic long-tail protest/minority-report coverage, overture authorship/presbytery sponsorship where not yet normalized, and exact person-level normalization for some rosters.

## 2017 Women Serving in the Ministry of the Church

Status: **complete at the committee identity layer with separate person-specific evidence**.

Primary source: `src-ga45-women-serving-2017`.

All 12 committee identities and voting/advisory roles are canonical and app-projected. Committee-service edges remain weight 0; they do not transfer every report statement or internal school of thought to every member.

Separate authored/person-specific evidence is normalized for Jeffrey Choi, Kathy Keller, William Castro, and Mary Beth McGreevy. Choi's 2017 position is kept separate from his 2026 Overture 37 actions.

## 2026 Overture 37 — women serving as ordained deacons

Status: **normalized as a distinct formal-action case with attribution guardrails**.

Key machine-facing sources include the official Pacific Presbytery overture, the primary formal dissent naming Aaron Baker / Jeffrey Choi / Walter Henegar / Eric Kapur, byFaith denominational reporting, and contemporaneous reporting used for Choi's floor-speech attribution.

Pacific Presbytery is the formal submitting body. Current evidence does not establish Choi as sole author, drafter, sponsor, or orchestrator of the overture itself.

## Alliance for Mission & Renewal

Status: **substantial first-party coverage**.

Founding-board material, current leadership, organizational framing, blog/Substack/YouTube snapshots, and multiple issue-specific evidence datasets are present. Media participation remains distinct from formal membership or blanket agreement with everything said in the same venue.

## A Faithful PCA / Looking Forward – Together

Status: **normalized letter and historical signer snapshots available**.

Identity matching remains conservative, especially for common names and records lacking institutional context.

## A Call to Prayer & Lament

Status: **initial-signatory/source material registered with verification guardrails**.

The public site itself reports that verification was added after disruptive submissions. Do not bulk-promote a raw later-submission scrape into a verified roster without corroboration.

## Save the PCA / Functional Female Officer datasets

Status: **ingested as source-attributed external assessment data**.

Church classifications stay at the institutional/source layer and do not automatically transfer to every pastor, officer, employee, or member.

## Church, presbytery, institutional, and RUF sources

Status: **first-class canonical church/presbytery data plus multiple dated institutional/RUF snapshots**.

Historical roles and current roles must remain dated. Institutional employment, education, ordinary church roles, and current-role snapshots normally contribute zero ideological/network weight by themselves.

## Identity and family evidence

The reproducible person crosswalk and reviewed identity receipts live under `sources/normalized/identity/` and `sources/raw/identity/`.

Rules:

- exact same-name matching alone is insufficient;
- reviewed aliases/name variants are person-specific, not global nickname rules;
- reviewed-but-unapplied evidence is not the same as a completed canonical seed;
- ambiguous rows remain unresolved until context is sufficient.

Family relationships are separately normalized in `sources/normalized/identity/family-relationships-2026.json`. Tim Keller ↔ Kathy Keller is currently app-visible as reciprocal spouse context. Family edges are weight 0 and never transfer theology, membership, actions, or scores.

## Secondary and theological-context sources

Secondary sources are roadmaps, corroboration, or context; they should not be the sole basis for disputed membership when primary evidence is reasonably available.

The companion theological manifest currently metadata-registers R. L. Dabney's `The Public Preaching of Women`, B. B. Warfield's `Paul on Women Speaking in Church`, and Rich Leino's `The Deaconess & the Household of God: A Rejoinder to Dan Barber` without unnecessarily copying private Drive binaries.

## Private Google Drive companion corpus

The private `PCA Research` folder contains authored synthesis and source PDFs. It is not fully duplicated in the public repo. User-authored synthesis is context/research product, not independent primary evidence; material claims should trace back to underlying sources. See `research/companion-corpus.md`.

## Archival and maintenance rule

Where redistribution rights are unclear, preserve metadata, extraction notes, provenance receipts, and stable source/archive URLs rather than republishing entire works.

Update this register when a major source family changes status, a new source family becomes app-facing, or a material evidence gap is closed. A fresh agent should be able to tell what is already done before proposing duplicate ingestion work.
