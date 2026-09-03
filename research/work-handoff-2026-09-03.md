# PCA-Data — Work / Chrome source-saturation handoff

Prepared: 2026-09-03

## Objective

Continue the source-first construction of a time-aware PCA institutional/network knowledge graph. This is a **research ingestion pass**, not primarily a frontend redesign pass.

The repository already contains methodology, source dossiers, partial normalized datasets, a static site shell, validators, and institutional schemas. The goal of this Work pass is to complete the large/browsing-heavy source families that are inefficient or error-prone to transcribe manually.

## Non-negotiable research rules

1. **Keep the receipts.** Every normalized row must trace to a raw source, archived page, official PDF, screenshot, transcript, or source manifest with URL/date.
2. Prefer PCA official minutes, original organization material, archived public pages, and official institutional bios over commentary.
3. Commentary/social media may identify leads but does not establish disputed person-level claims by itself.
4. Preserve source wording and historical role/presbytery/church as printed. Do not silently replace historical affiliations with current ones.
5. Resolve identities cautiously. Same name does not equal same person without supporting context.
6. Every church and presbytery can be canonicalized. **Do not ingest every person in every church.** Create person nodes only when a person enters the research graph through a notable public source, role, action, publication, network, agency/faculty role, or controversy.
7. A church-level external assessment does not automatically become a person-level doctrinal claim.
8. Education, faculty employment, RUF/MNA/MTW work, and ordinary church employment are institutional edges and normally score zero ideologically.
9. Preserve distinct evidence types. Examples:
   - `2019 Warhurst Protest Signer`, not `pro-Revoice`.
   - `O15 Minority Report Signer`, not generic `anti-gay`/`sexuality position`.
   - `National Partnership confirmed member`, only when the archive explicitly establishes membership.
10. Run/repair validation after each bulk import.

---

# P0 — Bulk primary roster imports

## 1. A Faithful PCA / Looking Forward – Together

### Primary letter
Historical site / statement: `Looking Forward – Together`, 2021-06-02.
Existing repo dossier:
`sources/raw/public-statements/a-faithful-pca/README.md`

### Two legitimate signer snapshots

#### Snapshot A — 2021-06-11 — 571 signers
Static PDF:
https://warhornmedia.com/wp-content/uploads/2022/09/Signatures-%E2%80%94-A-Faithful-PCA.pdf

Wayback origin recorded by PDF:
https://web.archive.org/web/20210611152829/https://www.afaithfulpca.net/signatures

The repo already has signers #1–94 normalized in three chunks. Verify rather than re-key them if possible.

#### Snapshot B — 2022-03-14 — 737 signers
Wayback:
https://web.archive.org/web/20220314223906/https://www.afaithfulpca.net/signatures

A full user-supplied transcription exists in the source ChatGPT conversation as:
`Pasted markdown(20260903-164744).md`

It runs consecutively from:
- #1 Rev. Charles E. McGowan
through
- #737 Rev. Brad A. Anderson

### Tasks

1. Preserve/copy the **raw 737-entry transcription** into:
   `sources/raw/public-statements/a-faithful-pca/signatures-2022-03-14-transcription.md`
   and record its Wayback URL as provenance.
2. If possible, also save HTML/PDF/screenshots from the Wayback page itself.
3. Normalize all 737 entries into a structured file, preserving:
   - snapshot_date
   - sequence_number
   - name_as_printed
   - honorific/title as printed
   - role_as_printed
   - church_or_institution_as_printed
   - city/state/country as printed
   - presbytery_as_printed
   - normalized_person_id only when resolved
   - source locator
4. Preserve the 571 snapshot separately. Do not overwrite it with the later roster.
5. Calculate:
   - which names are in both snapshots;
   - which 166 entries were added between snapshots;
   - possible removed/changed entries;
   - role/presbytery changes only as historical source changes, not automatically as career changes.

Important correction: the 737 A Faithful PCA roster is **not** the contaminated Prayer & Lament form data. An earlier repo warning was corrected.

---

## 2. 2019 Warhurst protest / Revoice-era GA action

Primary source:
https://www.pcahistory.org/pca/ga/47th_pcaga_2019.pdf

Useful navigation/secondary index:
https://pcapolity.com/case-studies/protest-case-study/protest-of-the-minority-report/

Existing metadata:
`sources/normalized/revoice/warhurst-protest-2019-metadata.json`

Known:
- Formal protest offered by Kevin Twit.
- Official Minutes preserve **203 signers**.
- Protest is around Minutes pp. 80–85.
- Overture 28 minority report context is preserved elsewhere in the same Minutes.

### Tasks

Extract all 203 signers with:
- print order
- name_as_printed
- TE/RE
- presbytery_as_printed
- normalized_person_id when resolved
- PDF page

Store as:
`sources/normalized/revoice/warhurst-protest-signers-2019.json`

Do NOT label the cohort generically `pro-Revoice`.

---

## 3. Overture 15 — 49th GA, 2022

Primary source:
https://www.pcahistory.org/pca/ga/49th_pcaga_2022.pdf

Existing metadata:
`sources/normalized/revoice/overture-15-2022-metadata.json`

Known:
- O15 was adopted as amended 1167–978.
- Minority Report supported the O15 formulation.
- Minority Report had **46 signers**, 24 RE + 22 TE, from 31 presbyteries.
- RE Matthew Fender presented it.
- Official Minutes also preserve a separate **negative-vote roster** representing opposition to O15.

### Tasks

Create two separate datasets:

`sources/normalized/revoice/overture-15-minority-report-signers-2022.json`

and

`sources/normalized/revoice/overture-15-negative-votes-2022.json`

Never merge the two.

For each row preserve name, TE/RE, presbytery, print order/page, normalized person ID.

Also preserve the official presbytery-ratification results if a reliable official record can be captured; presbytery voting is a presbytery-level action, not an inferred vote by every minister in that presbytery.

---

## 4. NAE withdrawal protest — 49th GA, 2022

Primary source:
https://pcahistory.org/pca/ga/49th_pcaga_2022_vol01.pdf

Existing dossier:
`sources/raw/denominational-actions/nae-withdrawal-2022/README.md`

Existing source receipt records the protest location.

Known:
- PCA withdrew from NAE in 2022, final controlling vote 1059–681.
- TE L. Roy Taylor offered a formal protest.
- Official Minutes pp. approximately 27–31 preserve a **200+ named commissioner roster**.

### Tasks

Extract entire protest roster:
`sources/normalized/nae/withdrawal-protest-signers-2022.json`

Fields:
- print_order
- name_as_printed
- TE/RE
- presbytery_as_printed
- normalized_person_id
- PDF page

Also preserve named roles in the debate separately:
- L. Roy Taylor
- Walter Kim
- Kenneth McHeard
- Carl Robbins
- Rhett Dodson
- other formal presenters/authors from official minutes

---

## 5. Overture 37 minority report — verify existing import

Primary source:
https://www.pcahistory.org/pca/ga/48th_pcaga_2021.pdf

The repo already contains the complete 28-name roster. Verify it against the official PDF and fix any spelling/presbytery normalization errors. Do not recreate if correct.

---

# P0 — National Partnership source completion

## Combined primary archive

Project source file:
`NPP_Emails_2013_2021.pdf`
444 pages.

Existing normalized files:
- `sources/normalized/national-partnership/confirmed-memberships-and-actions-v1.json`
- `sources/normalized/national-partnership/confirmed-memberships-additional-v2.json`
- `sources/normalized/national-partnership/confirmed-memberships-additional-v3.json`
- `sources/normalized/national-partnership/issue-actions-v1.json`

### Membership rule

Confirmed NP membership requires one of:
- explicit `Additions` entry;
- `NP member X` wording;
- a list explicitly headed as NP members;
- an explicit roster such as `Here are the NP members I currently have on the committee`;
- equivalent unambiguous archive wording.

Do NOT turn these into confirmed membership by themselves:
- NP-supported candidate;
- person praised by Kessler;
- person nominated by a committee containing NP members;
- conference attendee;
- someone merely copied or discussed.

### Tasks

1. Complete all **41 `Additions` snapshots** across the archive.
2. Extract every explicit `NP member` reference.
3. Extract every named list of `NP guys/Partnership men/NP members` on:
   - Nominating Committee
   - Review of Presbytery Records
   - Overtures Committee
   - Administrative Committee
   - Interchurch Relations
   - MNA
   - MTW
   - RUF/RUM
   - Covenant College/CTS boards/committees where applicable
   - SJC-related ballots/nominees when explicitly called NP members
4. Deduplicate to a canonical confirmed-membership table while preserving every historical evidence record.
5. Keep a separate table of:
   - NP-supported candidates
   - NP-preferred nominees
   - positively discussed leaders
   - organizations/events considered adjacent but distinct

### Special archive relationships to preserve

- Mike Khandjian: explicitly NP member + organizer of Fellowship; archive says Fellowship organizationally distinct but high overlap.
- Sean Lucas: explicitly `NP member Sean Lucas`.
- Irwyn Ince: explicit addition + later `NP member and chairman` of Women Serving committee.
- Tag Tuck: explicitly listed as NP Overtures member, Blue Ridge, 2019.
- Rob Wootton: explicit NP Overtures member, James River, 2019.
- Andy Wood: explicit 2018 `NP guys on committees` RPR listing, Blue Ridge.
- Bryan Chapell and George Robertson: explicitly included in 2014 list headed `NP members who have been nominated...`.
- Greg Thompson: NP-supported/celebrated SJC nominee, but **membership not established** unless another explicit record is found.

### Issue/action extraction priorities

Preserve exact messages/pages concerning:
- 2015/2016 racial reconciliation organizing;
- Women Serving in Ministry study committee;
- Revoice / Nashville Statement / Human Sexuality AIC;
- Overtures 23/37;
- NAE withdrawal;
- unordained persons/women on PCA boards/agencies;
- Good Faith Subscription;
- Beautiful Orthodoxy;
- Fellowship;
- A Faithful PCA;
- denominational committee strategy.

---

# P0 — Complete PCA church backbone

## Official PCA sources

Directory page:
https://www.pcaac.org/church-directory/

Text directory:
https://presbyteryportal.pcanet.org/ac/directory

The text directory reported `Database Updated: Aug 31, 2026` during this research pass.

The PCA page embeds a BatchGeo map whose KML export contains bulk nationwide church records.

Existing importer:
`scripts/import-pca-church-kml.mjs`

### Tasks

1. Download/save the official KML into:
   `sources/raw/institutions/pca-church-directory/`
2. Run the importer.
3. Preserve the raw parsed placemark output.
4. Resolve duplicates conservatively.
5. Populate `data/churches.json` with canonical current church/mission IDs.
6. Preserve:
   - church name
   - type / mission status
   - address
   - city/state/country
   - website
   - contact fields if public
   - pastor_as_printed (raw field only; do not create person automatically)
   - presbytery_id
   - coordinates
   - source snapshot date
7. Cross-check anomalies against the official text directory.

Do **not** ingest all pastors as people. The directory's pastor field is an attribute/lead until that person appears elsewhere in a notable source.

---

# P0 — Save the PCA FFO workbook

Project source workbook supplied by user:
`ffo_public_dataset_020826(2).xlsx` / equivalent exact mounted filename.

Version date: 2026-02-08.

Existing source/analysis notes identify sheets including:
- church_list
- raw_data
- bucketed_data
- ambiguous_data
- presbyteries

### Tasks

1. Save exact workbook binary under:
   `sources/raw/external-datasets/save-the-pca/`
2. Hash it.
3. Preserve raw rows losslessly in a machine-readable normalized extract.
4. Match each church against canonical PCA church IDs after church import.
5. Preserve source dataset's own classifications and raw evidence URLs.
6. Keep ambiguous rows separate.
7. Do not assign a church classification directly to every pastor/staff member.

Desired graph:
`Save the PCA dataset/version → assessment → Church`

and separately:
`Person → dated role → Church`

---

# P1 — Institutional rosters and career graph

Complete dated current snapshots for:

## PCA institutions/agencies
- Administrative Committee / byFaith
- CDM, especially Women's Ministry
- Covenant College
- Covenant Theological Seminary
- PCA Foundation
- MNA
- MTW
- RUF
- PCA Retirement & Benefits
- Ridge Haven

Prioritize complete leadership/staff/faculty rosters where publicly exposed.

## Seminaries
High priority:
- Covenant Theological Seminary
- Reformed Theological Seminary (campus-specific where possible)
- Westminster Theological Seminary
- Westminster Seminary California
- Greenville Presbyterian Theological Seminary

Add others when they arise in notable-person biographies.

### Education rule
Seminary attendance/alumni status is a zero-weight institutional edge. Faculty/administrative role is a dated employment edge, also normally zero ideological weight.

## Career reconstruction

For Tier-A/high-overlap people reconstruct public ministry history from seminary onward as far as reliable sources allow:
- education
- RUF
- local pastorates
- church planting
- MNA/MTW/CDM
- faculty/administration
- presbytery transitions
- denominational transfers/departures
- current role

Do not over-research one-off roster signers until overlap makes them important.

---

# P1 — AMR media archive

Official sources:
- https://a4mr.org/blog/
- https://a4mr.substack.com/
- https://www.youtube.com/@AllianceforMissionandRenewal

Existing repo contains a priority media inventory.

### Tasks

Create a complete item index with:
- date
- title
- author/host
- guests
- current/historical role as stated
- topic tags
- URL
- transcript/caption availability

Archive official captions/transcripts where available.

Transcript priority:
1. GA overture roundtables / post-GA analysis
2. female deacons / women in ministry
3. confessional subscription / theological vision
4. Revoice / Side-B / sexuality
5. race / immigration / mercy / public theology
6. AMR self-description and network history

Do not infer organizational unanimity from one guest/article unless AMR itself adopts the statement.

---

# P1 — Publication screenshot receipts

User supplied screenshots of chapter tables for:
- *Heal Us, Emmanuel*
- *Hear Us, Emmanuel*
- *Co-Laborers, Co-Heirs*

Source attribution requested by user for those screenshots:
https://x.com/dokimazete

Tasks:
- save the actual PNG/JPG screenshots into each publication's `screenshots/` subfolder where conversation/browser access permits;
- preserve source-attribution README;
- verify the normalized chapter lists against the screenshots;
- do not treat the X account's commentary as evidence of the contributors' theology beyond what the visual receipts show.

---

# P1 — Revoice/Missouri/SJC deepening

Existing dossier:
`sources/raw/issues/revoice/README.md`

Need browser-heavy capture of:
- Missouri Presbytery investigative material;
- Affirmations & Denials;
- complaints and SJC case documents;
- Memorial statements and departure material;
- Greg Johnson's career/transfer/departure trajectory;
- preserved Revoice 2018 speaker/board material where publicly archived;
- exact identities of relevant PCA participants.

Keep conference participation, hosting, presbytery investigation, protest signing, minority reports and SJC actions as distinct edge types.

---

# Quality control / output requirements

After each major import:

1. Run repository data validator.
2. Check for:
   - duplicate person IDs;
   - orphan source IDs;
   - unresolved presbytery spellings;
   - same-name collisions;
   - historical/current role overwrites;
   - church duplicates;
   - invalid source URLs.
3. Update a progress file summarizing:
   - rows imported;
   - rows unresolved;
   - duplicate candidates;
   - sources still inaccessible;
   - suggested next source family.
4. Commit source receipts and normalized data together when practical.
5. Do not redesign the public UI substantially in this pass. Source saturation comes first.

## End-of-pass deliverable

The Work session should leave `PCA-Data` with enough source density to support reliable derived overlap queries such as:

- Garris Letter 1 ∩ confirmed NP members
- Garris Letter 1 ∩ AMR
- Garris Letter 1 ∩ A Faithful PCA
- Garris Letter 1 ∩ churches classified in FFO dataset
- Warhurst protest ∩ NP ∩ A Faithful PCA
- O15 negative voters ∩ A Faithful PCA
- AMR leadership ∩ NP
- PCA agency staff ∩ public coalitions
- seminary faculty/alumni ∩ public-action cohorts
- presbytery concentrations of each cohort

Every derived count must drill down to the underlying people and source-backed paths.
