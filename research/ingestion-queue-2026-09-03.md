# Research ingestion queue — 2026-09-03

This queue is intentionally source-first. New public-facing person/network claims should not be added merely because a lead appears in commentary, social media, or a secondary article.

## Current phase

**Source saturation plus conservative identity/overlap analysis before detective-view/UI expansion.**

Normal web/files/GitHub tools are still producing useful primary evidence. A ChatGPT Work/Chrome investigation pass should begin **after the checkpoint at the bottom of this file is substantially complete**, because that is when browser/computer access becomes most valuable for stubborn downloads, Wayback pages, YouTube transcripts, old church staff pages, and presbytery records.

## P0 — primary roster normalization

### National Partnership, 2013–2021 — IN PROGRESS
- Continue year-by-year extraction of additions and explicit membership references.
- Extract all named NP men on Nominating, RPR, Overtures, IRC, MNA, MTW, SJC-related ballots, and other committees.
- Separate NP members from NP-supported candidates/nominees.
- Extract internal issue/action records with exact page/date.
- Current normalized work already includes multiple explicit membership/addition records and thematic issue-action records for race, women in ministry, sexuality/Revoice, NAE, and related issues.

### A Faithful PCA / Looking Forward – Together, 2021 — CLEAN SOURCE RECOVERED
- Clean source: 149-page preservation of the June 11, 2021 Wayback signer page.
- Source contains **571 numbered signers**.
- Normalize all 571 with sequence number, 2021 role, church/institution, location, presbytery, and PDF page.
- Resolve duplicates only after identity review.
- Cross-reference with every other formal roster.
- Web extraction is possible; binary/raw-page preservation is better suited to the later Work/browser pass if the PDF cannot be directly committed from the current connector.

### Warhurst protest / Revoice, 2019 — DOSSIER BUILT; ROSTER PENDING
- Comprehensive Revoice source dossier added under `sources/raw/issues/revoice/README.md`.
- Extract every named protest signer from 47th GA Minutes.
- Preserve TE/RE and presbytery.
- Keep marker text precise: signer of protest concerning language in Steven Warhurst's Overture 28 minority-report speech.

### Overture 37 minority report, 2021 — PENDING FULL ROSTER
- Extract all signers/authors and exact proposed wording.

### Overture 15, 2022 — PENDING FULL ROSTER
- User supplied official-Minutes screenshot showing the start of the negative-vote roster, including RE Andrew Augenstein.
- Extract majority/minority report signers, named votes, and formal protests.
- Add presbytery ratification data only from official records; do not infer person-level votes.

### NAE withdrawal protest, 2022 — EVENT/DOSSIER BUILT; ROSTER PENDING
- NAE chronology now covers 2011–12, 2019, and 2022 withdrawal attempts.
- Extract Roy Taylor's full protest roster from the official 49th GA Minutes.
- Preserve event role and presbytery exactly.

## P1 — issue dossiers

### Women in ministry — DOSSIER BUILT / EXPANDING
- 2008 deaconess controversy and SJC case identified.
- 2017 Women Serving committee roster and NP/Ince link documented.
- AMR 2026 `Three Views on Female Deacons` identified as three separate authored positions.
- `Co-Laborers, Co-Heirs` chapter-level roster corrected from user-supplied source-audit screenshots; full 26-chapter structure is now normalized, including the two-contributor chapter and one unidentified contributor.
- Next: normalize 2008 minority/majority actors and later local-practice SJC cases.

### Racial reconciliation / social justice — DOSSIER BUILT / EXPANDING
- 2015 Lucas/Duncan Personal Resolution documented.
- Official 2016 source confirms **43 racial-reconciliation overtures**.
- Overture 4 (Missouri) was a model for many; Overture 43 (Potomac) became the framework adopted by the Assembly; Overture 45 formed the racial-reconciliation/ethnic-diversity study committee.
- Committee roster is documented in the source dossier.
- Heal Us / Hear Us publication rosters are normalized; source-audit screenshots provide current/last affiliation leads.
- Next: normalize all 43 overtures by presbytery and requested action, then 2018 committee recommendations and PCA Unity Fund leadership.

### Immigration / refugee ministry — DOSSIER BUILT / EXPANDING
- MNA Refugee & Immigrant Ministry formation and Pat Hatch/Angela Pacey leadership are documented.
- 2025 MNA webpage/content controversy under Irwyn Ince is registered as a specific event rather than generalized to all MNA immigration work.
- Walter Kim → NAE → Evangelical Immigration Table trajectory identified.
- Next: normalize current RIM team and search PCA-specific EIT signers/participants.

### Homosexuality / Revoice / Side-B — DOSSIER BUILT / HIGH PRIORITY
- Revoice 2018 hosting, Missouri investigation, 2019 GA floor roles, Missouri A&D committee, Human Sexuality AIC, O23/O37, SJC cases, O15, and Memorial departure are now in a single source dossier.
- Next: full Warhurst protest roster, O37 minority report, O15 named actions, Greg Johnson/Memorial trajectory.

### NAE — DOSSIER BUILT / ROSTER PENDING
- 2011–12, 2019, and 2022 withdrawal attempts normalized as one historical family.
- Roy Taylor, Bruce O'Neil, Walter Kim, Kenneth McHeard, Carl Robbins, Rhett Dodson, and NP internal opposition to withdrawal are documented at event-role level.
- Next: full 2022 protest roster and overlap analysis.

## P1 — institutional/career graph

### PCA agencies — SOURCE SNAPSHOTS UNDERWAY
Current source folders now exist for:
- Administrative Committee
- CDM
- Covenant College
- Covenant Theological Seminary
- PCA Foundation
- MNA
- MTW
- RUF
- PCA Retirement & Benefits / related current branding as available
- Ridge Haven
- Great Commission Publications as a partner, not a PCA agency

Next:
- normalize current leadership/staff into dated role edges;
- backfill historical leadership from GA reports and archived bios;
- prioritize RUF/MNA/MTW because they form strong ministry-career pipelines.

### Seminaries — SOURCE SNAPSHOTS UNDERWAY
Current source folders exist for:
- Covenant Theological Seminary
- Reformed Theological Seminary
- Westminster Theological Seminary
- Westminster Seminary California
- Greenville Presbyterian Theological Seminary

RTS current faculty evidence already connects several people in the broader dataset, including Sean Michael Lucas, Irwyn Ince, Geoff Ziegler, Stephen Estock, Ligon Duncan, and others. These are zero-score academic/employment edges.

Next:
- build full current Covenant faculty/trustee snapshot;
- normalize RTS current/visiting/adjunct roles;
- reconstruct education/career history for Tier A figures.

### Save the PCA FFO dataset — WORKBOOK FOUND AND VERIFIED
- Exact conversation upload found: `ffo_public_dataset_020826(2).xlsx`.
- Workbook corresponds to the Save the PCA dataset dated 2026-02-08.
- Source folder contains the source URL, verification/hash/sheet audit, and normalization notes.
- Workbook sheets include church-level, raw-role, bucketed-role, ambiguous, presbytery, and statistics/interactive material.
- Next: finish lossless row-level export, match church identities to the PCA directory, and preserve versioned source-attributed classifications.

## P1 — publications / screenshots

User-supplied source-audit screenshots for Heal Us, Hear Us, and Co-Laborers are attributed to:
https://x.com/dokimazete

**COMPLETED 2026-09-04:** all six PNG files are archived under the corresponding publication `screenshots/` folders with SHA-256 manifests. All 84 chapter rows are normalized. The image audit corrected *Heal Us, Emmanuel* chapter 29 to Jonathan Seda.

Do not rely on the screenshots' color/highlight as proof of NP membership unless the NP archive independently establishes the relationship.

## P1 — identity resolution and overlap analysis

**FIRST PASS COMPLETED 2026-09-04:** the reproducible identity crosswalk covers 2,799 source rows across 28 datasets and confirms 672 row mappings to 206 people. The first overlap outputs include all 378 dataset pairs, typed multi-roster recurrence, presbytery/church concentration, institutional co-occurrence pipelines, and graph-quality diagnostics. Continue with the 252 probable rows first, then the ambiguous/collision queue; do not loosen the contextual matching threshold.

## P1 — AMR media archive

Sources:
- https://a4mr.org/blog/
- https://a4mr.substack.com/
- https://www.youtube.com/@AllianceforMissionandRenewal

For each item preserve title, date, authors/hosts/guests, stated roles, topic tags, GA context, URL, transcript source, and exact claims/recommendations where material.

### Transcript priority
1. General Assembly overture roundtables and post-GA reviews.
2. Female deacons / women in ministry.
3. Confessional-missional-center / theological-vision material.
4. Human sexuality / Revoice / Side-B material.
5. Race, immigration, public theology, mercy, or social-justice content.
6. Network history / AMR self-description.

Official YouTube captions, `.vtt`, `.srt`, or plain transcript exports are all acceptable as research inputs if the video URL/title/date accompany the transcript.

**PLATFORM INVENTORIES COMPLETED 2026-09-04:** the repository now preserves 128 Substack archive records, five RSS-only podcast companion records, 31 YouTube video records, and English caption VTT receipts for all 31 videos. Exact-title cross-posting is normalized separately. Official titles, descriptions, and opening captions establish 83 participant appearances across 30 videos and 40 distinct printed names; one video remains unnamed rather than inferred. Next work should extract source-bounded passages from the highest-priority captions; it should not treat a guest's statement as an AMR-wide position.

## P2 — current-role/trajectory resolution

Once a person appears in two or more high-value datasets, verify:
- current church/institution;
- current denomination/presbytery where public;
- former PCA role(s);
- education/seminary;
- RUF/MNA/MTW or seminary career;
- departure/transfer if applicable;
- current external networks or institutions.

Tier A people receive full public ministry-career reconstruction. Long-tail one-off signers remain roster-only until overlap makes them analytically significant.

## Exclusion / quarantine rules

- Social-media accusations are lead material unless tied to primary evidence.
- Sensitive personal claims that are unnecessary to documented ecclesiastical actions are not part of the dataset.
- Contaminated or spammed signer forms are quarantined and never treated as verified rosters.
- Same-name matches are unresolved until identity is established.
- A current employer, church, seminary, or educational role does not by itself count toward ideological/network scoring.
- Save the PCA church classifications attach to the church and source version, not automatically to each person serving there.

## WORK / CHROME HANDOFF CHECKPOINT

Start the major Work/Chrome investigation wave when most of the following are true:

- [ ] NP explicit membership/addition and committee-placement extraction is substantially complete.
- [ ] All 571 A Faithful PCA signers are normalized.
- [ ] 2019 Warhurst protest roster is normalized.
- [ ] Overture 37 minority-report roster is normalized.
- [ ] Overture 15 named-vote/protest data is normalized.
- [ ] 2022 NAE-withdrawal protest roster is normalized.
- [ ] 43 racial-reconciliation overtures are captured by presbytery/action category.
- [ ] Current PCA agency leadership/staff snapshots are substantially normalized.
- [ ] Current Covenant/RTS faculty and trustee/leadership snapshots are substantially normalized.
- [ ] Save the PCA FFO workbook has a lossless normalized export and church matching is underway.
- [ ] AMR article/video inventory exists, even if transcripts are not yet complete.

At that point Work/Chrome should focus on:
1. missing binaries and screenshots;
2. Wayback-only/dead pages;
3. YouTube/Substack transcript capture;
4. old church staff/biography pages;
5. presbytery minutes and hard-to-index court records;
6. entire-repo source audit and gap discovery;
7. then a separate front-end/detective-view implementation/review wave.
