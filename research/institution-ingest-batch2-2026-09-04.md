# Institution normalized ingest — batch 2 — 2026-09-04

## Scope

This batch promotes the 2026-09-04 Reformed Theological Seminary residential-faculty receipt and the conservatively reconciled Mission to the World leadership receipt into the deterministic institutional-role dataset.

All records remain neutral institutional edges with `ideological_weight: 0`.

## Reformed Theological Seminary

Source receipt:
`sources/raw/institutions/reformed-theological-seminary/residential-faculty-snapshot-2026-09-04.md`

The prior normalized dataset contained only an 8-person high-overlap RTS subset. This batch replaces it with the **46 unique identities classified by current RTS sources in the residential-faculty universe**.

Because the receipt is person-centered rather than list-row-centered, RTS receives a dedicated parser:

- each H3 person heading becomes exactly one normalized person-role row;
- actual academic/administrative title bullets are combined into `role_as_printed`;
- campus, Global, visiting, promotion, and current-site classification evidence is retained separately in `listing_evidence_as_printed`;
- source order and H3 source line are preserved;
- no campus/listing sentence is silently converted into a job title.

### Important preserved cases

- **S. Donald Fortson III** remains `Professor of Church History and Pastoral Theology Emeritus`; current-site placement under a Residential Faculty heading does not erase the explicit emeritus title.
- **Sean Michael Lucas** remains one person with role `Chancellor's Professor of Church History`; current institution-wide residential-directory evidence and Atlanta/Orlando visiting-faculty appearances remain separate listing evidence rather than duplicate identities.
- **Zachary J. Cole, D. Blair Smith, and Guy M. Richard** retain current post-promotion titles, while the 2026 promotion evidence remains source evidence rather than a second role row.
- Printed-name punctuation is preserved, including `Richard P. Belcher, Jr.` and `James R. Newheiser, Jr.`.

Normalized RTS coverage: **46 rows**.

## Mission to the World

Source receipt:
`sources/raw/institutions/mtw/leadership-snapshot-2026-09-04.md`

The prior normalized dataset contained only the coordinator. This batch promotes the ten current roles that are conservatively corroborated by 2026/current official sources:

- Lloyd Kim — Coordinator
- Mark Bates — Senior Director of Missions Engagement
- David Stoddard — International Director for Europe; Managing Director of Field Operations
- Jonathan I. — International Director, Asia Pacific
- Neal W. — International Director, Global Muslim Ministries
- Victor Nakah — International Director, Africa / sub-Saharan Africa
- Sam Kang — Director of Diversity Mobilization; Regional Director of East Africa
- Dale Hollenbeck — Director, MTW Mid-America Hub
- Jerry Gibson — MTW Director of Mobilization & Western Hub
- Robin Lee — MTW West Coast Regional Director

Printed protected forms such as `Jonathan I.` and `Neal W.` remain exactly as printed.

### Deliberately excluded from current-role normalization

- Steve Robertson is not treated as current because MTW's dated official profile states that he left MTW for Geneva Benefits in 2025, despite a stale conference page still carrying his former title.
- The current Americas International Director remains unresolved.
- Cartee Bales's and John Tubbesing's current executive status remains unresolved.

Normalized MTW coverage: **10 rows**.

## Dataset effect

Institutional current-role records grow from **457 to 504**, a net increase of **47**:

- RTS: 8 → 46, net +38
- MTW: 1 → 10, net +9

The deterministic identity crosswalk grows from **2,905 to 2,952 source rows** while retaining the same 28 source-bounded datasets.

The batch-2 identity summary remains conservative:

- 312 ambiguous
- 10 collision
- 555 context-confirmed
- 119 exact-confirmed
- 263 probable-requires-review
- 1,693 unmatched

No probable, ambiguous, collision, or unmatched row receives a canonical person ID merely from name similarity.

## Validation requirement

Merge only after the normal read-only PR workflow passes on the exact final branch head, including:

- application syntax
- structured-data validation
- research-import validation
- institution normalizer reproduction
- deterministic identity rebuild
- deterministic overlap-analysis rebuild
- clean generated-output diff

## Next institution work

RUF remains separate from current-role normalization. Its 2026 official source primarily records dated starts, role transitions, and departures, so it should be modeled as a dedicated transition/event dataset rather than flattened into a current roster.