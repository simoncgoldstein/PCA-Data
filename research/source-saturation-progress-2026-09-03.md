# Source-saturation progress — 2026-09-03

## P0 completed

- Preserved official 47th, 48th, 49th, and 50th General Assembly PDFs, text derivatives, URLs, and SHA-256 receipts.
- Extracted 203 Warhurst protest signers, 46 Overture 15 minority-report signers, 199 recorded Overture 15 negative votes, and 203 NAE-withdrawal protest signers in print order.
- Verified and replaced the existing 28-name Overture 37 roster from the official 2021 minutes while preserving source wording and canonical presbytery IDs separately.
- Preserved the official 2023 Overture 15 ratification table: 88 presbyteries, 68 reporting, 39 passing, 29 not passing, and 59 approvals required. This corrects the earlier provisional metadata.
- Preserved and normalized both A Faithful PCA snapshots: 571 signers on 2021-06-11 and 737 signers on 2022-03-14. The March 2022 Wayback page is the authoritative citation for the 737 roster.
- Preserved the 444-page National Partnership archive and its layout text derivative. Extracted all 31 genuine `Additions` headings present in the archive, 74 named addition entries, explicit membership and committee-list evidence, and 640 issue/action excerpts. Built a strict canonical membership evidence table with 151 normalized printed-name keys and 409 evidence records.
- Re-ran the official PCA KML import: 1,977 placemarks, 1,970 canonical church entities, six exact duplicate groups, and no unresolved current presbytery names.
- Re-ran the Save the PCA FFO workbook import and exact-hash check: 1,964 church-list rows, 802 raw observations, 180 ambiguous observations, and 147 flagged churches. The conservative crosswalk auto-matched 143 and retained four for review.

## Known discrepancies and review queues

- The A Faithful PCA snapshots differ by 166 rows, but first/last-name identity-key comparison does not yield exactly 166 new people. It yields 560 shared keys, 175 added keys, one old-only key (`Hans Madueme`), and 11 collision keys. Ten duplicate-row identity keys in the earlier snapshot explain why row arithmetic cannot be reported as a clean added-person count. No identities were forced through these collisions.
- The National Partnership PDF contains 31 genuine `Additions` headings, not the 41 stated in the handoff. Ten of the 31 headings name no additions. The parser rejects a false heading-like total line and preserves all 74 named entries.
- `Columbus Metro` appears in the official 2023 ratification table but is absent from the repository's 2026 current-presbytery backbone. It remains an unresolved historical presbytery name rather than being silently mapped.
- Four FFO churches have no candidate in the current PCA KML snapshot: Hope MontCo (Eastern Pennsylvania), City Light Church (Pacific), Renewal Presbyterian Church (Philadelphia), and Grace and Peace Presbyterian Church (Pittsburgh). Their original rows and URLs remain in the review queue.
- Rhett Dodson was listed in the handoff as a possible NAE debate role. The relevant official journal passages establish roles for Roy Taylor, Walter Kim, Kenneth McHeard, and Carl Robbins, but do not establish a formal presenter/author role for Dodson. No such edge was created.

## Validation

Run both:

```sh
node scripts/validate-data.mjs
python3 scripts/validate-research-imports.py .
```

The research validator checks expected roster counts and order, resolved-person and presbytery references, the official ratification totals, archive hashes, National Partnership extraction density, the 1,970-church backbone, and the 143/4 FFO crosswalk split.

## P1 completed in this pass

- Normalized **more than 350 neutral dated institution-role records** from 14 official-source snapshot families: AC/byFaith, CDM/Women's Ministry, Covenant College, Covenant Seminary, Geneva Benefits, MNA, MTW, PCA Foundation, RUF, Ridge Haven, RTS, WSC, WTS, and GPTS. Every record retains its raw receipt, source line, exact printed role, source URL, and zero ideological weight. Coverage labels distinguish complete visible rosters from high-signal subsets.
- Added the previously missing Geneva Benefits official team snapshot with seven leadership roles, 23 staff roles, and 16 board names.
- Preserved the AMR home page and all 12 website blog pagination pages as raw HTML and built a deduplicated **120-item website index** spanning 2023–2026. The index includes date, title, contributor string, archive categories, topic tags, URL, and explicit `not_assessed` transcript/caption state.
- Preserved seven core Missouri/Revoice primary PDFs and text derivatives: the 2019 investigative report, 2020 Affirmations and Denials, Human Sexuality AIC report, SJC Cases 2020-05 and 2020-12, SJC Case 2022-12, and the 49th GA volume 2. Added normalized committee, complainant, presbytery-petition, departure, and ministerial-roll actions without collapsing distinct evidence types.

## P1 blocked or incomplete sources

- **AMR Substack and YouTube:** the website archive is complete, but a distinct Substack post export and a complete YouTube channel item/caption export were not available from the website pagination. Missing: stable item lists with video IDs and official caption tracks. Website items with embedded media remain `not_assessed` rather than being labeled transcript-free.
- **Publication screenshots:** the three requested chapter-table image files for *Heal Us, Emmanuel*, *Hear Us, Emmanuel*, and *Co-Laborers, Co-Heirs* are not present in the repository and could not be identified reliably among generically named prior image files. Missing: the actual PNG/JPG files or stable file references tying each image to a title. The existing normalized lists and `https://x.com/dokimazete` attribution receipts remain, but no substitute image was guessed.
- **Covenant College:** the official receipt establishes the president, but does not contain the full senior-administration and trustee roster. Missing: a preserved current page/export listing those names and titles.
- **MNA:** current leadership and 44 high-signal ministry roles are normalized. Missing: names/titles for the complete Disaster Response, Metanoia, and other large regional teams not enumerated in the receipt.
- **MTW:** Lloyd Kim's coordinator role is normalized. Missing: a public complete executive/senior-leadership roster; privacy-sensitive rank-and-file missionary ingestion remains intentionally out of scope.
- **RTS and RUF:** current high-overlap faculty and coordinator/new-hire records are normalized. Missing: a stable complete RTS multi-campus export and the full RUF campus/staff directory with individual profile URLs and presbytery fields.
- **WTS:** 21 current faculty names are normalized. Missing: exact current titles and opened official biography details.
- **Archived Revoice 2018 program:** missing a preserved original program that establishes the complete speaker/workshop roster. The Jay Sklar identification remains `strongly supported`, not upgraded to primary-source confirmed.
