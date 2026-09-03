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

## P1 status and next sources

Current dated raw snapshots already cover AC, CDM, Covenant College, Covenant Seminary, PCA Foundation, MNA, MTW, RUF, Ridge Haven, and five seminaries. The remaining P1 work is to normalize those snapshots consistently, add a Retirement & Benefits/Geneva Benefits snapshot, complete the AMR item index and caption archive, preserve user-supplied publication screenshots when accessible, and deepen the Missouri/Revoice/SJC document archive.
