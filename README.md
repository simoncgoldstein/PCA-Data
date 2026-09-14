# PCA Networks & Institutional Activity

A source-driven research project mapping people, organizations, public actions, denominational roles, institutional trajectories, and recurring networks in and around the Presbyterian Church in America (PCA).

The public site is designed to answer three questions:

1. **Who repeatedly appears across the same networks, coalitions, committees, and public actions?**
2. **How are those people and institutions connected over time?**
3. **What primary or reliable source supports each claimed connection?**

## Fresh-agent onboarding

If you are opening this repository without prior chat/project context, start with:

1. [`AGENTS.md`](AGENTS.md)
2. [`research/current-state.md`](research/current-state.md)
3. [`research/methodology.md`](research/methodology.md)
4. [`research/source-register.md`](research/source-register.md)
5. [`research/companion-corpus.md`](research/companion-corpus.md)
6. [`research/unresolved-identities.md`](research/unresolved-identities.md)

Those files are intended to make the repository self-contained enough that a new AI agent does not need old chat history to understand the evidence model, current status, source coverage, and next research slice.

## Methodological rule

The project stores **claims and evidence**, not labels by reputation. A person is not classified on the basis of friendship, church attendance, conference proximity, institutional employment, committee membership alone, or a single disputed vote. Each material connection should retain a type, confidence level, date or period where available, and source.

The UI may calculate an analytical **Network Involvement Index**, but the underlying evidence remains independently inspectable. The index measures recurrence and documented organizational/public-action involvement in the source universe studied. It is not a claim about every aspect of a person's theology, orthodoxy, or Christian character.

## Evidence levels

- **Confirmed**: a primary source explicitly establishes the connection.
- **Strongly supported**: multiple reliable sources establish the connection, but a direct roster or exact source pin is still incomplete.
- **Associated**: participation or institutional relationship is established, but membership or ideological agreement is not.
- **Unresolved**: a possible identity or connection that requires further verification.

Negative findings such as `National Partnership member: not established` are intentionally preserved where useful. Absence from a roster is not treated as evidence of opposition.

## Repository structure

```text
PCA-Data/
├─ AGENTS.md                     # Fresh-agent operating guide
├─ README.md
├─ index.html / app.js / styles.css
├─ data/                         # App-facing canonical entities and claims
│  ├─ people.json
│  ├─ organizations.json
│  ├─ events.json
│  ├─ affiliations.json
│  ├─ sources.json
│  ├─ churches.json
│  └─ presbyteries.json
├─ sources/
│  ├─ raw/                       # Primary files, snapshots, receipts, provenance
│  ├─ normalized/                # Structured datasets derived from sources
│  ├─ extracts/
│  └─ manifests/
├─ analysis/                     # Generated analytical outputs
├─ research/
│  ├─ current-state.md
│  ├─ methodology.md
│  ├─ source-register.md
│  ├─ companion-corpus.md
│  ├─ unresolved-identities.md
│  └─ additional audit/planning notes
└─ scripts/                      # Import, normalization, analysis, validation
```

## Current source universe

The repository now contains or registers substantial material from, among other source families:

- National Partnership correspondence, 2013–2021;
- A Faithful PCA / `Looking Forward – Together` and historical signer snapshots;
- Alliance for Mission & Renewal founding, leadership, media, and organizational material;
- PCA General Assembly minutes, study reports, protests, minority reports, recorded votes, overtures, and committee actions across multiple years;
- 2017 Women Serving in the Ministry of the Church study committee/report;
- 2019 Warhurst protest;
- 2021 Overtures 23/37 and related actions;
- 2022 Overture 15 and NAE-withdrawal actions;
- Human Sexuality Ad Interim Committee material;
- Garris investigation letters;
- A Call to Prayer & Lament;
- Save the PCA / Functional Female Officer external datasets;
- church/presbytery data;
- current institutional and RUF role snapshots;
- person identity crosswalks and reviewed identity receipts.

The private Google Drive `PCA Research` corpus also contains authored synthesis and several source PDFs that are **not all duplicated or registered here**. See [`research/companion-corpus.md`](research/companion-corpus.md) for the audited boundary.

## Validation

Research invariants are enforced by repository-wide and topic-specific GitHub Actions workflows under `.github/workflows/`. Generated research outputs should be rebuilt rather than manually edited when their generating scripts change or source data makes them stale.

## GitHub Pages

This is a static site: HTML + CSS + JavaScript + JSON. No server or database is required. Once GitHub Pages is enabled for the repository root on `main`, `index.html` is the public application.

## Status

**Active research build, beyond the original v0.1 scaffold.**

As of **2026-09-14**, the project has a substantial normalized evidence layer, identity-resolution system, generated overlap analysis, and app-facing graph. The dated handoff and immediate next slice live in [`research/current-state.md`](research/current-state.md). Update that file when a merged milestone materially changes the project state.
