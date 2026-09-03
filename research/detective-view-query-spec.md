# Detective view and cohort-analysis specification

## Goal

The public application should support both individual investigation and cohort analysis. A user should be able to open a roster/event such as **Garris Letter 1** and immediately see documented overlap with other networks, institutions, churches, presbyteries, publications, and actions.

The interface must compute these results from source-backed typed relationships rather than hand-written narrative labels.

## Core entity types

- Person
- Church
- Presbytery
- Seminary / College
- PCA Agency / Committee
- External Institution
- Network / Coalition
- Publication
- Public Letter
- General Assembly Event
- Overture
- Protest / Minority Report
- Study / Ad Interim Committee
- SJC / church-court case
- External versioned church assessment

## Example: Garris Letter cohort page

Header metrics might show:

- total verified signers;
- current PCA / former PCA / unresolved status;
- number and percentage with confirmed National Partnership membership;
- number and percentage with AMR founding/current involvement;
- number and percentage signing A Faithful PCA;
- number and percentage signing Prayer & Lament;
- number and percentage signing the 2019 Warhurst protest;
- number and percentage appearing in Heal Us / Hear Us / Co-Laborers;
- number and percentage with current or former RUF, MNA, MTW, CDM, Covenant Seminary, Covenant College, or other PCA-agency roles;
- seminary alumni/faculty distributions;
- current-presbytery distribution;
- historical-presbytery distribution at the time of signature;
- current-church distribution;
- number serving at churches carrying a source-attributed Save the PCA FFO classification;
- number whose churches later departed the PCA;
- number with documented Revoice-related actions;
- number with NAE-withdrawal protest/leadership involvement;
- number participating in racial-reconciliation overtures/study committees/publications.

Every metric should be clickable to reveal the exact people and source-backed paths behind the count.

## Example path display

A cohort member could show:

`Mike Khandjian`

`Garris Letter 1 signer`

→ `National Partnership — confirmed member`

→ `Fellowship — organizer`

→ `Heal Us, Emmanuel — contributor`

→ `AMR — founding board`

→ `Chapelgate Presbyterian Church — Senior Pastor`

→ `Chesapeake Presbytery`

Each edge opens its receipt.

## Church-level overlay

Church profile should show:

- current PCA directory record;
- current presbytery;
- current pastor(s)/officers where public;
- historical pastors relevant to the graph;
- people in tracked public rosters currently/formerly associated with the church;
- public controversies or actions directly involving the church;
- external source-attributed practice assessments, including Save the PCA FFO versions;
- departure/merger/plant relationships;
- publications/conferences hosted where documented.

### Example external assessment rendering

`Save the PCA Functional Female Officer Dataset — 2026-02-08`

`Classification: [raw category from workbook]`

`Evidence: [original church-page / archived source link]`

This appears on the **church**, not automatically on every associated person.

## Presbytery profile

Each presbytery should show:

- current canonical PCA status;
- stated clerk and official website from a dated snapshot;
- current churches;
- tracked Teaching/Ruling Elders;
- National Partnership representation by year;
- GA overtures originated;
- formal protests/minority reports involving members;
- study/ad-interim committee personnel;
- SJC cases involving the presbytery;
- constitutional-amendment vote history where official totals are available;
- 2016 racial-reconciliation overture participation;
- Revoice/sexuality-related actions;
- current and historical church-practice assessment counts;
- departures/transfers of churches or ministers where relevant.

The presbytery page should distinguish **collective presbytery action** from actions of individual members.

## Seminary / institutional pipeline view

Queries should support:

- `Covenant Seminary alumni ∩ National Partnership members`
- `RTS faculty ∩ A Faithful PCA signers`
- `former RUF staff ∩ AMR leadership`
- `RUF → pastorate → MNA/MTW leadership` career paths
- `Covenant Seminary faculty/administration ∩ racial-reconciliation publications`
- `current agency staff ∩ public-letter cohorts`

Education itself has no ideological score; these are pipeline/proximity analyses.

## Presbytery-level issue overlays

Store issue data as source-specific events rather than a permanent left/right rating.

Examples:

- submitted a 2016 racial-reconciliation overture;
- voted X/Y on a constitutional amendment;
- sent an overture concerning women/deacons;
- formally investigated/acted in a Revoice-related case;
- produced a protest/dissent;
- hosted a tracked church/person.

A later UI may summarize recurring patterns, but the source events remain visible underneath.

## Cohort comparison

Allow two cohorts to be compared, for example:

`Garris Letter 1` vs `Garris Letter 2`

or

`Warhurst protest` vs `A Faithful PCA`

or

`NP confirmed members` vs `AMR leadership`

Compare:

- exact person overlap;
- Jaccard overlap;
- presbytery concentration;
- church concentration;
- seminary education;
- denominational-agency service;
- publication participation;
- subsequent current roles;
- source-attributed church-practice overlays.

## Evidence drill-down requirement

No derived count should be a dead-end number.

For example:

`14 of 60 Garris Letter 1 signers are confirmed NP members`

must expand to a table containing:

- person;
- Garris source;
- NP membership source/date/page;
- confidence;
- historical church/presbytery at each event;
- current role verification date.

This requirement is central to the project's credibility.

## Time slider

Long-term objective: allow a user to select a year and see the graph as it existed then.

Example:

`2015` — NP membership, current churches and institutions at that date.

`2019` — Revoice/Warhurst/committee network.

`2021` — A Faithful PCA + O23/O37 + Human Sexuality.

`2026` — AMR + Prayer & Lament + current institutional positions.

Historical edges therefore need start/end dates wherever reliable.

## Priority before UI implementation

1. Normalize the large primary rosters.
2. Import canonical PCA churches and presbyteries.
3. Match Save the PCA FFO dataset to canonical church IDs.
4. Normalize current PCA agency/seminary rosters.
5. Reconstruct Tier-A careers.
6. Calculate cohort-overlap tables in data scripts.
7. Only then build the interactive detective UI.
