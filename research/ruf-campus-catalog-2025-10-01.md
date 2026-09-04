# RUF 2025-2026 Campus Catalog ingestion

- Snapshot date: `2025-10-01` (PDF creation metadata)
- Source: official RUF Internship Campus Catalog linked from RUF's Intern application page
- PDF SHA-256: `c9556efc40756f77466f1960437c19933d20f29b044e1082f0d743ff77457509`
- PDF pages: 390
- TOC-linked campus entries: 162 (138 RUF, 24 RUF International)
- Extracted person-role rows: 414
- Role counts: {"Associate Campus Minister": 10, "Campus Assistant": 6, "Campus Associate": 9, "Campus Minister": 151, "Campus Minister Assistant": 1, "Campus Staff": 75, "Fellow": 5, "Fellows": 6, "Interns": 151}

Only factual first-page roster fields are retained. Narrative answers are intentionally excluded. This is historical 2025 evidence, not a claim that each person remained in the same role in September 2026. The later 2026 RUF transition dataset remains separate. All RUF datasets share the same RUF identity source family so RUF cannot corroborate itself for identity creation.

## Identity audit

Adding the catalog increases the bounded identity source universe from 3,165 to 3,579 rows and from 29 to 30 source datasets. It creates six new canonical identities, all from independent non-RUF corroboration in the Faithful PCA signer records. In each case the full name, RUF Campus Minister role, and campus agree:

- `ben-coppedge`: Ben Coppedge, University of Georgia
- `george-hamm`: George Hamm, Emory University
- `john-craft`: John Craft, Rhodes College
- `matthew-trexler`: Matthew Trexler, University of California Los Angeles
- `nathan-dicks`: Nathan Dicks, Boston University
- `sammy-rhodes`: Sammy Rhodes, University of South Carolina

The canonical-person count therefore rises from 207 to 213, and identity-crosswalk-created profiles rise from 190 to 196. No identity is created merely from agreement among RUF datasets.

The review queue gains one office collision for `Andrew Terrell`. The catalog supplies an RUF role, while other tracked evidence under the same normalized name contains both Teaching Elder and Ruling Elder office labels. The identity builder correctly leaves this row unresolved with no canonical person ID.

## Reproducibility

The PDF coordinate extraction is pinned to PyMuPDF 1.26.7, the version under which the 414-row extraction was derived and inspected. A newer PyMuPDF geometry implementation produced a materially different coordinate parse and was rejected by the exact 414-row invariant rather than accepted as source drift. The committed normalized output is additionally checked by fixed row, campus, role-count, source-hash, page-count, and zero-weight validation rules.
