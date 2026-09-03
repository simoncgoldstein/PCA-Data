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

- pastors and officers;
- denomination/presbytery over time;
- church plants/campuses/mergers;
- public statements;
- local-practice controversies;
- source-attributed datasets such as Save the PCA's Functional Female Officer dataset;
- Revoice hosting/participation where documented;
- predecessor/successor congregations;
- departure to another denomination where applicable.

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

## Next extraction

1. Export the full PCA text-only church directory into `data/churches.json` with canonical IDs.
2. Preserve the 2026-08-31 directory snapshot as raw CSV/JSON when browser/Work access can extract the form results reliably.
3. Match every Save the PCA FFO workbook church to the canonical PCA church ID.
4. Match every public-letter signer to their contemporaneous church and presbytery.
5. Backfill historical pastor/church/presbytery relationships for Tier-A people.
6. Preserve later directory snapshots instead of overwriting 2026 data.
