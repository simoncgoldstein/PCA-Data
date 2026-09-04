# Identity-resolution audit — 2026-09-04

## Result

The first reproducible identity layer covers 2,716 printed-name rows across 27 dated or source-bounded datasets. It confirms 660 row-to-person mappings representing 206 canonical people. The builder added 189 recurring public-person nodes to the 18 previously reviewed core records; one existing core person does not occur in the current crosswalk inputs.

No probable, ambiguous, collision, or unmatched row receives a canonical ID.

## Match summary

| Status | Rows | Meaning |
|---|---:|---|
| `exact_confirmed` | 108 | The row already carried a reviewed seed-person ID whose printed name matched the seed or a documented alias. |
| `context_confirmed` | 552 | The exact normalized name was supported across independent source families by a matching presbytery, institution, or location, or by one of two documented seed-name aliases. |
| `probable_requires_review` | 226 | The exact name recurs, but the row itself lacks a shared disambiguator. |
| `ambiguous` | 276 | A duplicate, middle-name/initial variant, or common first-name variant cannot be safely collapsed. |
| `collision` | 10 | Conflicting offices, identifiers, or other explicit collision evidence prevents a match. |
| `unmatched` | 1,544 | No confirming cross-source context was found. |

The review queue contains 763 rows. It includes unresolved statuses plus initials-only and first/last variant keys, so its count is intentionally broader than the ambiguous/collision count.

## Inputs

The builder ingests both A Faithful PCA snapshots; confirmed National Partnership memberships; the 2019 Warhurst protest; the 2021 Overture 37 minority report; the 2022 Overture 15 minority report and recorded negative votes; the 2022 NAE-withdrawal protest; 14 institutional snapshot families; current AMR leadership; the 120-item AMR website index's bylines; and the three screenshot-backed publication chapter rosters.

The publication images are preserved under each publication's `screenshots/` directory. During image-to-data verification, chapter 29 of *Heal Us, Emmanuel* was corrected from `Jonathan Edgar` to the visible `Jonathan Seda`.

## Matching rules

The normalization layer handles honorifics, suffixes, punctuation, Unicode diacritics, curly apostrophes, initials, common spacing variations, and common first-name variants as collision keys. It retains each source's original printed name. A nickname/full-name pair such as `Tim`/`Timothy` is queued rather than merged automatically.

A new ID requires:

1. the same exact normalized full name in at least two independent source families; and
2. a shared presbytery, institution/church, or location; and
3. no Teaching Elder/Ruling Elder conflict, duplicate-within-dataset blocker, or unresolved first/last-name variant collision.

Even after a group is confirmed, a context-free row is not assigned that ID merely because its printed name is identical. The row remains `probable_requires_review` unless it independently shares a disambiguator or carries an explicit reviewed mapping.

Two explicit seed aliases are documented in the builder: `Sean Michael Lucas` → `sean-lucas` and `Duke L. Kwon` → `duke-kwon`. No fuzzy similarity match creates an ID.

## Corrected pre-existing identity error

The 2022 A Faithful PCA row `signature:6`, printed as `Rev. Steve Brown`, previously carried `andrew-augenstein`. The builder rejects that name/ID mismatch, clears the ID, and retains the correction in the reproducible collision audit. Andrew Augenstein is now linked to the correct 2022 row, `signature:477`, through matching Lake Nona/Central Florida evidence and confirmed official-action rows.

## Outputs

- `sources/normalized/identity/person-crosswalk.json` — full source-row crosswalk with match method, supporting/conflicting fields, confidence, and reviewer note.
- `sources/normalized/identity/review-queue.json` — unresolved collisions, duplicates, initials, and name variants.
- `sources/normalized/identity/summary.json` — per-dataset coverage and status totals.
- `scripts/build-person-crosswalk.py` — deterministic builder and conservative backfill.

The builder was run twice after generation with byte-identical results.

## Remaining identity work

The largest gains will come from opening individual institutional bios, completing RUF/RTS/MNA/MTW rosters with profile URLs, and adding dated church/presbytery context to publication and AMR media participants. The 226 probable rows are the fastest review set because their names already recur; the 276 ambiguous and 10 collision rows require stronger context rather than looser matching.
