# Work / browser handoff — full PCA church import

## Goal

Create the complete current PCA church backbone without auto-importing every pastor as a person.

## Source

PCA Administrative Committee Church Directory:
https://www.pcaac.org/church-directory/

Embedded BatchGeo map:
https://batchgeo.com/map/fed353c376144b1fed2f5e29150c2531

Bulk KML export:
https://batchgeo.com/map/kml/fed353c376144b1fed2f5e29150c2531

Text-only directory for validation:
https://presbyteryportal.pcanet.org/ac/directory

The text-only directory reported `Database Updated: Aug 31, 2026` on 2026-09-03.

## Steps

1. Download the KML unchanged.
2. Save the binary/text source to:
   `sources/raw/institutions/pca-church-directory/pca-churches-2026-09-03.kml`
3. Compute SHA-256 and record it in the source README or a manifest.
4. Run:
   `node scripts/import-pca-church-kml.mjs sources/raw/institutions/pca-church-directory/pca-churches-2026-09-03.kml`
5. Review `possible-duplicates.json` rather than auto-merging.
6. Resolve all KML presbytery names against `data/presbyteries.json`.
7. Produce canonical `data/churches.json`.
8. Compare counts/spot checks against the text-only PCA directory and the official map.
9. Preserve `pastor_as_printed` on the church, but do not create every pastor as a person.
10. Import/resolve the Save the PCA FFO workbook against canonical church IDs.

## Person policy

Follow `research/entity-inclusion-policy.md`.

A pastor printed in the directory becomes a normalized person only if that individual independently appears in a notable source/action/institutional role being tracked.

## Required QA

- no duplicate church IDs;
- every current church has a valid current presbytery unless genuinely unresolved;
- duplicate marker candidates remain auditable;
- no KML raw row is silently discarded;
- every Save the PCA match retains its raw workbook row and source version;
- current church directory metadata never overwrites historical church/presbytery relationships;
- church-level FFO assessment never silently becomes a person-level position.
