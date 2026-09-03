# PCA church and presbytery directory source family

Snapshot date: **2026-09-03**

## Canonical current church directory

PCA Administrative Committee Church Directory:
https://www.pcaac.org/church-directory/

Text-only directory:
https://presbyteryportal.pcanet.org/ac/directory

The text-only directory reported on 2026-09-03:

> Database Updated: Aug 31, 2026

Its visible fields are:

- Church Name
- City
- State
- Phone
- Email
- Website
- Presbytery
- Pastor

The directory is the preferred canonical source for current PCA congregation identity and current presbytery assignment. Church websites remain necessary for officer/staff details and local-practice verification.

## Bulk church source discovered

The PCA Administrative Committee church-directory page embeds a public BatchGeo map titled `PCA Churches`:

https://batchgeo.com/map/fed353c376144b1fed2f5e29150c2531

BatchGeo documents that a public map may be exported as KML by inserting `/kml/` after `/map/`. The resulting PCA bulk endpoint is:

https://batchgeo.com/map/kml/fed353c376144b1fed2f5e29150c2531

The KML is currently accessible publicly and contains nationwide `<Placemark>` records with fields including:

- church name;
- full address;
- phone;
- email;
- website;
- pastor as printed;
- presbytery;
- `Type Org`;
- coordinates;
- occasional extra fields such as `Address 2` or `Country`.

This is now the preferred **bulk ingestion source** for the current church backbone because it originates from the PCA Administrative Committee's embedded map and exposes the nationwide dataset in a machine-readable format.

### Important KML caveat

The map may contain duplicate/place-marker variants. Example observed on 2026-09-03: Alexandria Presbyterian Church appeared twice with the same website, pastor and presbytery but slightly different street-address text. Therefore KML rows must be normalized and deduplicated conservatively rather than assumed to be one-row-per-congregation.

The importer should preserve all raw records and separately produce canonical church entities.

## Canonical current presbytery list

PCA Administrative Committee Presbytery List:
https://www.pcaac.org/resources/presbyteries/presbytery-list/

The list contained **88 current presbyteries** on the 2026-09-03 snapshot and included stated-clerk and website fields where available. The normalized names are stored in `data/presbyteries.json`.

## Graph model

The core hierarchy is:

`Person → dated role → Church → dated membership → Presbytery → PCA`

Presbytery is also connected independently to:

- overtures;
- formal protests/dissents;
- General Assembly commissioners;
- study/ad-interim committee participants;
- SJC cases;
- National Partnership representation;
- presbytery-level votes on constitutional amendments;
- formal statements/minority reports;
- current officers/stated clerk;
- historical boundary/name changes when relevant.

Church is independently connected to:

- tracked pastors/officers/staff whose names enter the graph through notable evidence;
- denomination/presbytery over time;
- church plants/campuses/mergers;
- public statements;
- local-practice controversies;
- source-attributed datasets such as Save the PCA's Functional Female Officer dataset;
- Revoice hosting/participation where documented;
- predecessor/successor congregations;
- departure to another denomination where applicable.

## Person inclusion rule for the church import

The current directory's `Pastor` field is church metadata. **Do not automatically create a person node for every pastor in the nationwide directory.** Preserve the text as `pastor_as_printed` on the church record.

Create/resolve a normalized person only when that individual independently enters the project through a notable source or role under `research/entity-inclusion-policy.md`.

This keeps church/presbytery coverage complete while person coverage remains evidence-driven.

## Time-awareness rule

Do not overwrite historical affiliation with current affiliation.

Example:

`Person X → Church A → 2019` and `Person X → Church B → 2026`

must remain separate edges.

Likewise:

`Church A → Missouri Presbytery → through 2022`

and

`Church A → departed PCA → 2022`

should both remain queryable.

## Church practice / external assessment rule

A church-level assessment must never silently become a person-level theological claim.

Correct graph:

`Save the PCA FFO dataset (2026-02-08) → female-deacon/female-elder classification → Church X`

and separately:

`Pastor Y → serves at → Church X`

A query may show the overlap, but Pastor Y only receives a direct doctrinal/practice edge if separate evidence establishes his own action or position.

## Extraction sequence

1. Preserve/download the complete KML as a raw source receipt.
2. Parse every placemark into a raw normalized extract without dropping duplicates.
3. Resolve presbytery names against `data/presbyteries.json`.
4. Produce canonical/deduplicated church entities in `data/churches.json`.
5. Compare the resulting set against the text-only directory for omissions or stale map records.
6. Match every Save the PCA FFO workbook church to the canonical PCA church ID.
7. Match every public-letter signer to their contemporaneous church and presbytery.
8. Backfill historical pastor/church/presbytery relationships for Tier-A people.
9. Preserve later directory/map snapshots instead of overwriting 2026 data.

A parser scaffold is maintained in `scripts/import-pca-church-kml.mjs` so a future Work/Chrome pass or user-supplied KML download can be ingested reproducibly.
