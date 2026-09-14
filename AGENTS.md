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
- Do not infer an individual's theological position from committee membership, institutional employment, church membership, conference proximity, co-signers, family relationships, or another person's position.
- Committee/report-level statements stay report-level unless separate first-person, signed, authored, or otherwise individually attributable evidence exists.
- Institutional employment, education, ordinary church roles, current-role snapshots, and family relationships are normally zero-weight for the Network Involvement Index.
- Personnel overlap between organizations is evidence of overlap only. Do not infer that one organization is a successor, front, continuation, or ideological equivalent of another without separate organizational evidence.
- Spouse/family links are factual context edges only. They must never transfer theology, organizational membership, actions, or score from one person to another.
- Unresolved claims remain excluded from scoring and public certainty.
- Negative findings can be preserved when useful, but absence from a roster is not evidence of opposition or proof of nonparticipation in all related activity.

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

## Garris letters guardrail

The two 2024 public letters concerning TE Zachary Garris are modeled as **separate formal public actions** from their primary PDFs.

- `sources/normalized/public-statements/garris-letters-2024.json` preserves the complete printed rosters: 60 signers for Letter 1 and 21 for Letter 2.
- A confirmed signature is `public_coalition_action`, weight `3`, and score-included under the existing public-letter/protest methodology.
- Weight 3 means documented involvement in a tracked formal action. It is not itself a judgment of orthodoxy, Christian character, or every theological position of the signer.
- Signing establishes participation in that specific letter and its request for presbytery investigation. It does **not by itself** establish National Partnership membership, AMR membership, agreement on unrelated controversies, or a generic ideological label such as `big tent`.
- Letter 2 is fully canonically resolved. Letter 1 remains partially resolved; do not force common-name or weak-context matches for completeness.
- The two printed `Jeff White` rows are not one identity by default. Letter 1 prints New City Fellowship / Rio Grande and remains unresolved; Letter 2 prints Redeemer Downtown / Metro NY and is reviewed as `jeff-white-redeemer-downtown`.
- `scripts/project-garris-signers.py` is part of generated-output reconstruction and must run after the person crosswalk and before overlap analysis.

## 2017 Women Serving committee guardrail

The 2017 Ad Interim Committee on Women Serving in the Ministry of the Church is modeled as committee service, not as a blanket individual theological position.

- Committee service is `weight: 0` and `score_included: false`.
- The report itself records internal diversity on subsidiary questions.
- Do not assign either internal school of thought, every report sentence, or a broader ideological label to a committee member without separate person-specific evidence.
- All 12 official committee identities are now canonically resolved and projected to the app-facing committee event.
- Reviewed identity decisions are preserved in four receipts under `sources/raw/identity/2017-women-serving-identity-evidence-batch*-2026-09-14.json`.
- Person-specific evidence remains distinct. Mary Beth McGreevy's reviewed first-person evidence is normalized separately. Jeffrey Choi, Kathy Keller, and William Castro now have separately normalized authored positions in `sources/normalized/general-assembly/2012-2019-women-serving-member-authored-positions.json`.
- The authored-position dataset remains `ideological_weight: 0`. Preserve its internal distinctions: Choi's 2017 local-session discretion is not the same claim as his later 2026 Overture 37 action; Keller combines a male authoritative-teaching/elder boundary with broad non-elder ministry by women; Castro argues for a stricter ordinary-public-worship speech boundary while preserving congregational and extraordinary-case qualifications.

## 2026 Overture 37 attribution guardrail

The 53rd General Assembly Overture 37 record must distinguish institutional sponsorship from individual advocacy.

- **Pacific Presbytery** is the formal submitting body named by the official overture.
- Current evidence supports Jeffrey Choi as a public advocate, a floor speaker in support, and one of four named co-authors/submitters of the later formal dissent.
- Do **not** label Choi the sole author, drafter, sponsor, or orchestrator of Overture 37 unless additional primary evidence establishes that role.
- Choi's floor advocacy is unscored; his confirmed co-authorship of the formal dissent is modeled as a distinct formal denominational action.

## McGowan Global / National Partnership overlap guardrail

The current McGowan Global Institute roster is represented as a zero-weight institutional source. Independent National Partnership evidence is joined person-by-person rather than inferred from McGowan service.

- Bruce O'Neil, Mike Khandjian, Ray Cortese, and Bob Flayhart have independently documented National Partnership membership/participation in the canonical NP dataset.
- David Cassidy is a McGowan consultant and separately an AMR leader, but the current canonical NP dataset does **not** establish him as an NP member. Do not infer NP membership from organizational overlap.
- Mike Khandjian's Fellowship is documented as independent from the National Partnership despite substantial personnel overlap. Preserve that distinction.
- McGowan Global Institute itself is not modeled as an NP successor, front, continuation, or ideological equivalent absent separate organizational evidence.

## Family relationship guardrail

Person-to-person family edges are supported by the app graph but remain contextual only.

- `sources/normalized/identity/family-relationships-2026.json` contains reviewed family relationships.
- Tim Keller and Kathy Keller are modeled as spouses with reciprocal `target_type: person` edges.
- Family edges use `weight: 0` and `score_included: false`.
- Never use marriage or kinship to transfer a spouse's committee service, authored positions, network memberships, public actions, or Network Involvement Index score.

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
