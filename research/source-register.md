# Source Register

Audit date: **2026-09-14**

This document is the human-readable companion to `data/sources.json` and the evidentiary archive under `sources/`.

Use the source layers this way:

- `data/sources.json` — machine-facing source IDs used by app-facing events/affiliations.
- `sources/raw/` — preserved primary files, snapshots, receipts, and provenance material.
- `sources/normalized/` — structured datasets derived from source material.
- `sources/manifests/` and source-specific receipts — provenance and redistribution metadata.
- this file — source-family status and known gaps.
- `research/companion-corpus.md` — relationship between the private Google Drive research corpus and this repository.

## Highest-priority source families

### National Partnership correspondence, 2013–2021

Archive index: https://jude3pca.org/national-partnership-emails/

Status: **substantially ingested but person-level archival pinning remains incomplete**.

The repository includes National Partnership normalization, identity work, and archival/source records. Remaining work includes:

- add exact sender/date/year/page or message locators for person-level membership and organizing claims where still missing;
- distinguish explicit members from promoted candidates, recruited prospects, committee-placement recommendations, and adjacent figures;
- avoid upgrading `strongly_supported` claims to `confirmed` until the exact archival evidence is pinned.

### PCA General Assembly records

Status: **substantial normalized coverage; no longer merely planned**.

The repository contains official GA PDFs/text for key modern years plus normalized formal-position/action datasets across multiple controversies and periods. Current normalized work includes, among other items:

- women/office and women-in-ministry records from earlier GA periods;
- confessional subscription and Federal Vision-related formal records;
- 2016 creation/actions connected to the women-serving study committee;
- the 2017 Women Serving in the Ministry of the Church report and committee roster;
- 2019 Warhurst protest material;
- Human Sexuality Ad Interim Committee material;
- 2021 Overtures 23/37, minority-report and recorded-vote evidence;
- 2022 Overture 15 and NAE-withdrawal protest/vote evidence;
- later GA chronology/source material used by current validators.

Still incomplete:

- systematic coverage of all relevant protests/minority reports through the target period;
- overture authorship/presbytery sponsorship where not yet normalized;
- broader committee/agency placement history where analytically relevant;
- exact person-level normalization for some long-tail rosters.

### 2017 Women Serving in the Ministry of the Church

Status: **normalized, app-event represented, and partially canonically linked**.

The official PCA study report is registered as `src-ga45-women-serving-2017`. The normalized layer includes:

- all 12 committee members;
- voting/advisory status;
- report-level position summaries with explicit non-attribution guardrails;
- Mary Beth McGreevy first-person evidence preserved separately;
- canonical committee links and app-facing zero-weight service edges for Dan Doriani, Ligon Duncan, Irwyn Ince, Bruce O'Neil, and Roy Taylor;
- an applied reviewed-identity receipt for Doriani, Duncan, and Taylor.

Still unresolved in this committee dataset: Leon Brown, William Castro, Jeffrey Choi, Lani Jones, Kathy Keller, Mary Beth McGreevy, and Harry Reeder.

Committee service remains zero-weight and does not establish individual agreement with every report statement or internal school of thought.

### Alliance for Mission & Renewal

Status: **substantial first-party coverage**.

The repository includes founding-board material, current leadership, organizational framing, website/blog material, Substack/media snapshots, YouTube/video participation data, and topic-specific evidence boundaries. Media appearance remains distinct from formal membership or agreement with every statement made in the same venue.

### A Faithful PCA / Looking Forward – Together

Status: **normalized public-letter and signer snapshots available**.

Historical signer snapshots are preserved separately from the letter text. Identity resolution remains conservative, especially for common names and rows with incomplete institutional context.

### Garris letters

Status: **registered primary sources; signer normalization remains a priority**.

Both publicly circulated letters are registered in `data/sources.json`. They should be normalized person-by-person from the source PDFs. Do not convert co-signature into agreement with unrelated positions or broader network membership.

### A Call to Prayer & Lament

Status: **initial signatory/source material registered with verification guardrails**.

The public statement and initial signatories are tracked. The site itself reports that verification was added after disruptive submissions, so a downstream raw/form scrape must not be treated as a verified complete roster without corroboration.

### Save the PCA / Functional Female Officer datasets

Status: **ingested as source-attributed external assessment data**.

External church classifications belong to the institution/source layer. They do not automatically transfer to every pastor, officer, employee, or member associated with the church.

### Church and presbytery data

Status: **first-class canonical graph entities with broad directory coverage**.

Church/presbytery identity is used for institutional matching and concentration analysis. Historical names and unresolved aliases should remain explicit rather than silently normalized when confidence is low.

### Current institutional / RUF role sources

Status: **multiple dated snapshots normalized**.

Official institutional biographies and rosters are preferred. Current-role snapshots are dated because personnel move. A historical role source does not establish that a person still holds the role in 2026.

Institutional employment, education, ordinary church roles, and current-role snapshots normally contribute zero ideological/network weight by themselves.

## Identity evidence

The repository contains a reproducible person crosswalk plus reviewed identity receipts under `sources/raw/identity/`.

Rules:

- exact same-name matching alone is insufficient for common or ambiguous names;
- reviewed name-form equivalences are person-specific and do not create universal nickname/middle-initial rules;
- a `ready_for_canonical_seed` review state is not the same thing as a completed canonical mutation;
- an applied identity receipt should identify the canonical ID actually seeded and remain linked from the normalized evidence row;
- canonical IDs should be added only when the evidence and validator state support the change.

## Secondary and theological-context sources

Secondary sources are used as roadmaps, corroboration, historical/theological context, or source discovery. They should not be the sole basis for a disputed formal-membership claim when a primary source is reasonably obtainable.

The private Drive corpus contains several theological/polity sources that are now metadata-registered in:

`sources/manifests/companion-theological-sources-2026-09-14.json`

That manifest records stable public-source metadata for:

- R. L. Dabney, `The Public Preaching of Women` — public transcription at A Puritan's Mind, originally published in *The Southern Presbyterian Review* (October 1879);
- B. B. Warfield, `Paul on Women Speaking in Church` — PCA Historical Center edition identifying the original *The Presbyterian* publication of October 30, 1919;
- Rich Leino, `The Deaconess & the Household of God: A Rejoinder to Dan Barber` — Presbyterian Polity, September 1, 2026.

These are not currently app-facing source IDs and their Drive PDF binaries are not copied into the public repo. Metadata registration is sufficient for discoverability until a normalized/app-facing claim needs more.

## Private Google Drive companion corpus

The private `PCA Research` Drive folder contains authored synthesis documents and source PDFs. It is **not fully duplicated as raw binaries in this repository**, nor should it necessarily be.

See `research/companion-corpus.md` for the audited list and boundary. As of this audit, the known direct source PDFs in that corpus are discoverable from PCA-Data either through normalized/source records or the companion theological-source manifest.

User-authored synthesis documents in Drive remain context/research products, not independent primary evidence. Trace their material claims back to underlying sources.

## Archival policy

Where redistribution rights are unclear, store metadata, extraction notes, provenance receipts, and stable original/archive URLs rather than republishing the entire source file.

A source can be adequately represented without copying its binary if the repository preserves enough information to locate, verify, and cite it reproducibly.

## Maintenance rule

Update this file when:

- a major source family moves from planned to substantially normalized;
- a new source family becomes important to app-facing claims;
- a companion-corpus source is registered or archived;
- a known evidence gap is closed or materially changes.

Do not let this human register fall behind the actual normalized/source trees again; a fresh agent should be able to tell what is already done before proposing duplicate ingestion work.
