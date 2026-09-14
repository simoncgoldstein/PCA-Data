# Source Archive

This directory is the evidentiary archive for PCA-Data.

The public site is generated from canonical data under `/data`, while material claims should ultimately resolve to source records and evidence preserved or registered here.

## Structure

- `raw/` — original or near-original evidence files, public snapshots, PDFs, exported text, letters, reports, receipts, identity-review records, and other provenance material.
- `normalized/` — structured machine-readable datasets derived from source material, including rosters, formal positions, public statements, institutional snapshots, identity layers, church-directory data, and source-specific normalized records.
- `extracts/` — human-readable or machine-readable extracts used where a source-specific extraction layer is useful.
- `manifests/` — provenance records describing source title, publisher, original/archive URL, retrieval date, local path, checksum where useful, and redistribution limitations.

`data/sources.json` is the app-facing machine source registry; it is not a complete directory listing of every raw/normalized research artifact.

## Current major collections

As of 2026-09-14, source work includes substantial material for:

- National Partnership correspondence;
- PCA General Assembly minutes and formal actions;
- 2017 Women Serving in the Ministry of the Church;
- Revoice-related denominational records;
- Overtures 23/37 and Overture 15;
- NAE withdrawal/protest material;
- A Faithful PCA / public statements;
- Alliance for Mission & Renewal;
- Save the PCA / Functional Female Officer external datasets;
- racial-reconciliation/publication datasets;
- institutional and RUF snapshots;
- church-directory/canonicalization work;
- person identity crosswalks and reviewed identity receipts.

See `research/source-register.md` for source-family status and `research/companion-corpus.md` for the private Google Drive corpus that is not fully duplicated here.

## Evidentiary rules

1. Prefer primary sources over commentary when the primary source is reasonably available.
2. Do not edit a raw file to make a point. Corrections, annotations, transcription fixes, classifications, and normalized tables belong in a derived/normalized layer.
3. If a source cannot appropriately be redistributed, store provenance metadata, source/archive links, and extraction notes rather than copying the full work into the public repository.
4. Each material app-facing affiliation/event should cite one or more source IDs that can be traced back to evidence or a reproducible public source.
5. Same-name matches are never enough to merge identities without corroborating information or a reviewed identity decision.
6. Network membership, event participation, committee service, institutional employment, public-letter signatures, authored positions, and ideological interpretation remain distinct evidence categories.
7. Committee/report-level claims must not be silently promoted to individual positions.
8. A reviewed identity receipt marked `ready_for_canonical_seed` is evidence preparation, not proof that canonical seeding has already happened.
9. Generated normalized/analysis outputs should be rebuilt through their scripts rather than manually edited when generation is available.

## Raw-file policy

A raw binary is useful when it improves reproducibility and redistribution is appropriate, but the project does not require copying every external PDF into GitHub. A stable original/archive URL plus provenance metadata and normalized evidence may be the correct archival form.

This distinction matters for the private Google Drive `PCA Research` corpus. Some collected theological PDFs are documented in `research/companion-corpus.md` but are not yet registered or copied here.

## Agent workflow

A fresh agent should read `AGENTS.md` and `research/current-state.md` before proposing new ingestion. The source trees are much more developed than the original v0.1 planning documents implied, so do not assume a source family is missing merely because an old research note calls it planned.
