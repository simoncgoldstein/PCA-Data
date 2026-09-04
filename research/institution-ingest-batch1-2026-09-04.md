# Institution normalized ingest — batch 1 — 2026-09-04

## Scope

This batch promotes three browser-verified 2026-09-04 receipts into the deterministic institutional-role dataset while preserving institutional service as a neutral, zero-weight graph edge.

### Covenant College

Source receipt:
`sources/raw/institutions/covenant-college/leadership-snapshot-2026-09-04.md`

Normalized coverage:
- 9 Senior Administration records
- 4 Board Officer records
- 23 Trustee records
- 12 Trustee Advisor records
- **48 total current leadership/governance records**

Nested officer/church biography notes are intentionally excluded from the current-role parser and remain available in the raw receipt for later trajectory modeling.

### Mission to North America

Source receipt:
`sources/raw/institutions/mna/team-snapshot-2026-09-04.md`

Normalized coverage:
- **95 current visible team records**
- exact title retained where printed
- department/ministry retained separately as `department_as_printed`
- `Hansoo Jin` and `Will Stockdale` retain null titles because the current source does not print one
- `Mark Casson` retains a null department because the current card extraction does not print one

No title or department is manufactured from older profiles.

### Westminster Theological Seminary

Source receipt:
`sources/raw/institutions/westminster-theological-seminary/faculty-snapshot-2026-09-04.md`

Normalized coverage:
- 17 primary Faculty
- 3 Affiliate Faculty
- 9 CCEF Counseling Faculty
- 3 Center for Theological Writing records
- **32 total current instructional/academic-support records**

The live academic faculty page controls current-role ingestion. The separate Westminster Media index remains secondary evidence where it disagrees with the live academic categories.

## Dataset effect

The institutional current-role dataset grows from **351 to 457 role records**, a net increase of **106**, while remaining at 14 institutional datasets.

The downstream identity crosswalk grows from the established 2,799-row baseline to **2,905 source rows** after deterministic rebuild. Matching remains conservative: unresolved or collision rows do not receive canonical person IDs merely from name similarity.

## Validator hardening

The prior research validator hard-coded identity summary `record_count == 2799`, which made any legitimate new source ingestion fail even when the crosswalk and summary were internally consistent.

This batch replaces that brittle equality with two invariants:

1. identity-summary metadata must exactly equal the actual crosswalk row count;
2. the crosswalk may not regress below the established **2,799-row** baseline.

This permits source growth while still catching lost rows or stale metadata.

## Deliberately deferred

- **RUF:** the 2026 receipt is primarily start/transition/departure event data and should be normalized as a separate transition dataset rather than flattened into current roles.
- **RTS:** the 2026 residential-faculty receipt is person-centered under H3 headings and needs a specialized one-person-per-heading parser with campus/listing metadata separated from role titles.
- **MTW:** ten current leadership/program roles are available, but the batch remains separate so historical reconciliation and unresolved executive succession are not mixed into this three-source ingestion.

## Validation requirement

Merge only after the normal read-only PR workflow passes on the exact final branch head, including:
- application syntax
- structured-data validation
- research-import validation
- institution normalizer reproduction
- identity crosswalk rebuild
- overlap-analysis rebuild
- clean generated-output diff
