# Church and presbytery graph schema

## Coverage

- `data/presbyteries.json`: complete current PCA presbytery backbone.
- `data/churches.json`: complete current PCA church/mission-church backbone after KML normalization.
- People remain selective under `research/entity-inclusion-policy.md`.

## Church entity

Recommended canonical shape:

```json
{
  "id": "church-stable-id",
  "name": "Church Name",
  "aliases": [],
  "status": "current_pca",
  "address_full": "...",
  "city": "...",
  "state_province": "...",
  "country": "USA",
  "postal_code": "...",
  "phone": "...",
  "email": "...",
  "website": "...",
  "presbytery_id": "chesapeake",
  "pastor_as_printed": "Rev. Example Person",
  "source_record_ids": ["batchgeo-..."],
  "directory_database_date": "2026-08-31",
  "snapshot_date": "2026-09-03"
}
```

`pastor_as_printed` is informational metadata and is not automatically a normalized person relationship.

## Presbytery entity

Recommended shape:

```json
{
  "id": "chesapeake",
  "name": "Chesapeake",
  "status": "current",
  "official_website": null,
  "stated_clerk_as_printed": null,
  "snapshot_date": "2026-09-03"
}
```

Current normalized file initially stores the canonical name/ID set; clerk, website, geography, historical names, and status history can be layered in later.

## Person -> church relationship

Only tracked people receive normalized relationship edges.

```json
{
  "person_id": "example-person",
  "church_id": "example-church",
  "role": "Senior Pastor",
  "start_date": "2021",
  "end_date": null,
  "current": true,
  "source_ids": ["source-id"]
}
```

Possible roles include:

- Senior Pastor
- Pastor
- Associate Pastor
- Assistant Pastor
- Stated Supply
- Church Planter
- Ruling Elder
- Deacon
- Staff
- Member
- Former Pastor
- Visiting Theologian

Use the most literal source language available.

## Church -> presbytery history

The current `presbytery_id` on the church entity is a snapshot relationship. Historical changes should later be represented as dated edges:

```json
{
  "church_id": "memorial-st-louis",
  "presbytery_id": "missouri",
  "start_date": null,
  "end_date": "2022-11-18",
  "relationship": "member_congregation",
  "source_ids": ["source-id"]
}
```

## External church assessment

External research such as Save the PCA must be attributed and versioned:

```json
{
  "church_id": "example-church",
  "dataset": "save-the-pca-ffo",
  "dataset_version": "2026-02-08",
  "assessment_type": "female_deacon",
  "value": true,
  "raw_role": "Deaconess",
  "evidence_urls": ["..."],
  "source_row": 123
}
```

This is a source-attributed church assessment, not a person-level claim.

## Event cohort join

A public-letter/event roster should resolve each participant through:

`event participant -> person -> contemporaneous church -> contemporaneous presbytery`

and separately:

`person -> current church -> current presbytery`

This prevents current affiliation from being substituted for historical affiliation.

## Example Garris cohort query

For every verified signer:

1. resolve person ID;
2. preserve church/presbytery printed in the letter;
3. resolve current church separately;
4. join current church to Save the PCA assessment(s);
5. join person to NP/AMR/A Faithful PCA/Revoice/agency/seminary edges;
6. aggregate only from confirmed/qualified relationships;
7. expose every contributing row beneath each cohort statistic.

## Duplicate church handling

The BatchGeo map contains possible duplicate markers. The import pipeline should use three levels:

1. raw placemark — never deleted;
2. duplicate candidate group — machine-flagged only;
3. canonical church entity — created after conservative resolution.

Factors for resolution:

- same normalized name;
- same website/domain;
- same presbytery;
- same pastor as printed;
- nearly identical address/coordinates;
- PCA text-directory result;
- current church website.

Do not merge merely because names are identical.
