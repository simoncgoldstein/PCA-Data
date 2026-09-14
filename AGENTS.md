# PCA-Data Agent Guide

This repository is a source-driven research project about people, organizations, public actions, denominational roles, institutional trajectories, and recurring networks in and around the Presbyterian Church in America (PCA).

## Read this first

Before changing research data or interpreting the project, read these files in order:

1. `README.md` — project purpose and repository map.
2. `research/current-state.md` — dated snapshot of what is already complete and what should happen next.
3. `research/methodology.md` — evidence model, edge types, confidence levels, scoring boundaries, and research rules.
4. `research/source-register.md` — source-family status and known source gaps.
5. `research/companion-corpus.md` — the private Google Drive research corpus and which items are or are not represented in this repository.
6. `research/unresolved-identities.md` — claims and identities that must remain unresolved until further evidence is added.
7. `sources/README.md` — raw/normalized/manifests archive conventions.

Do not rely on prior chat history as project state. The repository should be treated as the source of truth.

## Core research rules

- Store claims and evidence, not reputation labels.
- Interpretation is downstream of facts.
- Prefer primary sources over secondary commentary.
- Preserve exact source wording, printed names, offices, dates, presbyteries, and source locators wherever practical.
- Same-name matches are not enough to merge identities. Identity resolution requires corroborating context or a reviewed identity decision.
- Do not infer an individual's theological position from committee membership, institutional employment, church membership, conference proximity, co-signers, or another person's position.
- Committee/report-level statements stay report-level unless separate first-person, signed, authored, or otherwise individually attributable evidence exists.
- Institutional employment, education, ordinary church roles, and current-role snapshots are normally zero-weight for the Network Involvement Index.
- Unresolved claims remain excluded from scoring and public certainty.
- Negative findings can be preserved when useful, but absence from a roster is not evidence of opposition.

## Data flow

The intended evidence pipeline is:

`source -> raw/provenance receipt -> normalized dataset -> canonical identity/edge -> app-facing data -> generated analysis`

Important locations:

- `sources/raw/` — preserved primary files, receipts, snapshots, and provenance material.
- `sources/normalized/` — structured datasets derived from sources.
- `data/` — app-facing canonical entities, events, affiliations, and source records.
- `analysis/` — generated analytical outputs; do not hand-edit generated files unless the generating workflow explicitly requires it.
- `research/` — methodology, current state, source register, gap tracking, and research notes.
- `scripts/` — import, normalization, crosswalk, analysis, and validation code.

## 2017 Women Serving committee guardrail

The 2017 Ad Interim Committee on Women Serving in the Ministry of the Church is modeled as committee service, not as a blanket individual theological position.

- Committee service is `weight: 0` and `score_included: false`.
- The report itself records internal diversity on subsidiary questions.
- Do not assign either internal school of thought, every report sentence, or a broader ideological label to a committee member without separate person-specific evidence.
- Irwyn Ince, Bruce O'Neil, Dan Doriani, Ligon Duncan, and Roy Taylor are canonically resolved and projected to the app-facing committee event. The other seven committee identities remain unresolved until separately evidenced.

## Source handling

`data/sources.json` is the machine-facing source registry. `research/source-register.md` is its human-readable companion, but not every useful research document belongs in `data/sources.json`.

A private Google Drive folder named `PCA Research` contains authored synthesis documents and several source PDFs. Its audited relationship to the repository is documented in `research/companion-corpus.md`. Do not treat user-authored synthesis documents as independent primary evidence. Where redistribution rights are unclear, store metadata, URLs, archive references, or extraction receipts rather than copying a full work into the public repository.

## Validation and change discipline

Prefer small, reviewable slices. For research changes:

1. Inspect the relevant normalized source and canonical entities first.
2. Change the smallest coherent set of files.
3. Add or extend a focused validator when a new evidence boundary or invariant matters.
4. Run the relevant focused validation plus the repository-wide research validation through CI.
5. Regenerate derived outputs when the generating script says they are stale.
6. Stop at a clean PR boundary rather than combining unrelated research topics.

The repository's GitHub Actions workflows under `.github/workflows/` are authoritative for CI expectations.

## Current next step

See `research/current-state.md`. Do not infer a new priority from old PR descriptions or chat history if that file says otherwise.
