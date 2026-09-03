# Institutional, educational, and ministry-career coverage plan

## Objective

Build a longitudinal institutional graph for significant PCA figures rather than a present-day directory. The target end state is a source-driven "detective view" in which a user can start with a person, church, seminary, agency, presbytery, public action, or network and traverse documented relationships through time.

The graph should be comprehensive enough to expose recurring personnel pipelines while remaining literal about what each edge proves.

## Core principle

**Education, employment, ministry service, and church attendance are relationships, not ideological classifications.**

Examples:

- `M.Div., Covenant Theological Seminary, 2008` is an education edge.
- `RUF Campus Minister, University of Virginia, 2019–2025` is a ministry/employment edge.
- `Professor, Covenant Theological Seminary, 2014–2022` is a faculty edge.
- `Pastor, Church X, 2022–present` is a church-role edge.
- `Church X was classified by Save the PCA as functional-female-officer: deacon, dataset version 2026-02-08` is a **source-attributed church assessment**, not a claim about every pastor/member at Church X.

The UI may later derive proximity views from these facts, but raw data must preserve the distinction.

## Person-level longitudinal record

For high-value people, research the full public ministry career where reliable sources permit it.

### Priority fields

- full normalized name;
- ordination status, where applicable;
- denomination(s) and dates;
- presbytery membership and dates;
- current church/institution;
- current formal role(s);
- prior pastoral roles;
- prior assistant/associate pastor roles;
- church-planting roles;
- RUF roles;
- MNA roles;
- MTW roles;
- denominational committee/agency employment;
- seminary/college faculty or administrative roles;
- nonprofit/network roles;
- board memberships;
- chaplaincy;
- major publications/collaborations;
- education/degrees;
- seminary attended;
- degree year where verifiable;
- current-role verification date;
- source for each individual role/degree.

### Career completeness tiers

**Tier A — full career reconstruction**

Use for people with repeated appearances across multiple high-value datasets or important institutional leadership. Attempt to reconstruct all substantial ministry/institutional posts from seminary onward.

**Tier B — major-role history**

Use for people with one or two important appearances. Capture current role plus significant former PCA roles and education.

**Tier C — roster-only**

For long-tail one-off signers/committee members, preserve the role stated in the contemporaneous source. Expand only if later overlaps make the person analytically important.

This prevents the project from spending equal research time on 2,000 low-overlap names while still supporting a comprehensive graph.

## Education and seminary data

### What to track

For every significant person, collect theological and graduate education when publicly stated:

- institution;
- degree;
- field/concentration if relevant;
- graduation year or attendance range;
- completed vs. attended/incomplete where the source distinguishes this;
- faculty mentor/program only when explicitly relevant and sourced.

Undergraduate education may also be stored, but seminary/theological education receives priority because it is more likely to reveal institutional pipelines relevant to PCA ministry.

### Seminary alumni edge weight

Seminary attendance should normally have **zero ideological/network score**. It is useful for graph traversal and institutional-pipeline analysis, not as evidence that alumni share positions.

## Faculty and seminary-affiliation data

Current faculty rosters should be treated as a high-value live dataset.

Track:

- full-time faculty;
- adjunct/visiting faculty when publicly listed;
- president/chancellor/deans;
- board/trustee roles where public;
- faculty dates where historical archives permit;
- courses/department only when relevant;
- PCA ordination/presbytery separately from academic employment.

A person can therefore have distinct edges such as:

`PCA Teaching Elder → Missouri Presbytery`

`Professor → Covenant Theological Seminary`

`Author → public statement/event`

without collapsing those relationships.

## Seminary source universe

### Denominational institution

1. **Covenant Theological Seminary** — highest priority because it is a PCA committee/agency institution and the denomination's seminary.

### Major non-denominational seminaries repeatedly represented in PCA leadership

Add and maintain institutions as they occur in source biographies. Priority starting set:

2. Reformed Theological Seminary, including campus-specific roles where possible.
3. Westminster Theological Seminary.
4. Westminster Seminary California.
5. Greenville Presbyterian Theological Seminary.
6. Other seminaries such as Fuller, Trinity Evangelical Divinity School, Gordon-Conwell, Southern Baptist Theological Seminary, etc., only as people in the dataset create a reason to add them.

The goal is not to rank seminaries. The goal is to preserve educational and faculty pipelines.

## PCA committees and agencies: full live-roster priority

The PCA's own current directory lists the following committees/agencies. These should receive systematic current-roster capture and, over time, historical leadership snapshots:

1. Administrative Committee
2. Committee on Discipleship Ministries (CDM)
3. Covenant College
4. Covenant Theological Seminary
5. PCA Foundation
6. Mission to North America (MNA)
7. Mission to the World (MTW)
8. Reformed University Fellowship (RUF)
9. PCA Retirement & Benefits / successor branding as applicable
10. Ridge Haven

Also track major programs/subministries where personnel overlap makes them analytically important, including:

- PCA Unity Fund;
- MNA African American Ministries;
- MNA Refugee & Immigrant Ministry;
- MNA church planting / church vitality;
- MNA Chaplain Ministries;
- MNA Disaster Response;
- RUF senior leadership and regional staff;
- MTW senior leadership, regional directors, and major strategic initiatives;
- CDM Women's Ministry leadership;
- byFaith/Administrative Committee editorial leadership where relevant;
- Historical Center staff/leadership where relevant;
- Great Commission Publications as a PCA partner, with relationship type clearly marked as partner rather than PCA agency.

## Agency-roster capture strategy

For each agency/institution maintain:

- current official roster snapshot date;
- name;
- title;
- department/team;
- location if public;
- PCA ordination status if stated;
- organization URL;
- individual bio URL;
- former role(s) stated in the bio;
- education stated in the bio;
- archive link if a prior roster is available.

Do not infer presbytery membership from employment unless a source states it.

## Full ministry-career reconstruction

For Tier A people, search in this order:

1. current official institutional bio;
2. current church bio;
3. PCA minister directory / GA minutes / presbytery records;
4. former church staff pages or archived bios;
5. seminary/faculty bio;
6. RUF/MNA/MTW bio archives;
7. conference/speaker bios;
8. reliable denominational reporting;
9. secondary biographies only as leads.

Each role should carry dates with explicit precision:

- exact date when known;
- year when only year is known;
- `before YYYY`, `by YYYY`, or `circa` only if unavoidable and clearly marked.

## Church graph

Eventually every PCA congregation should be a first-class institution record with:

- normalized church name;
- city/state/country;
- presbytery;
- PCA directory identifiers if available;
- current website;
- active/dissolved/departed status;
- current pastors;
- current officers when public;
- historical pastors where important;
- church plants/campus relationships;
- source snapshot dates.

This enables people to connect to controversies through their actual congregational history without attaching a controversy directly to the person when the evidence only concerns the church.

## Save the PCA dataset integration

Save the PCA's **Functional Female Officer Report dataset** is a significant external source for church-level practice data and should be preserved as a versioned, source-attributed dataset.

Primary source page:
https://www.savethepca.com/downloads/

Current downloadable dataset identified by the site as:
`Dataset, Updated February 8th, 2026`

Direct file URL exposed by the source page:
https://www.savethepca.com/wp-content/uploads/2026/02/ffo_public_dataset_020826.xlsx

### Integration rule

Do **not** put `functional female officer church` directly on every person who serves there.

Instead model:

`Person → pastoral/staff/member role → Church`

and independently:

`Save the PCA dataset version 2026-02-08 → source-attributed classification → Church`

The detective view may then display:

`Current church: X`

`External church-practice dataset: Save the PCA classified X as [category], 2026-02-08`

This preserves attribution and avoids converting a church-level external assessment into a person-level theological claim.

### Fields to preserve from Save the PCA

When the workbook is formally ingested, retain as much raw information as possible before any normalization:

- PCA church name as printed;
- presbytery;
- website;
- raw role/title observed;
- bucketed role/title;
- female-elder classification;
- female-deacon classification;
- source/evidence URL(s) if included;
- notes;
- dataset version/date;
- original row identifier if present.

Create a normalized church match only after resolving church identity against the PCA church directory.

### Versioning

Save the PCA states its findings have changed as tips and dataset refinement occurred. Therefore every import must be tied to a dataset date/version. Do not silently overwrite historical classifications.

A later source correction should produce a new assessment record, preserving the earlier source version for auditability.

## Future detective-view queries this enables

Examples:

- Show everyone who attended Covenant Seminary and later served in RUF.
- Show former RUF staff who later became MNA/MTW leaders.
- Show AMR leaders who were also National Partnership members.
- Show A Faithful PCA signers who later held faculty positions at a seminary.
- Show people connected to Revoice-era actions who later moved to another denomination.
- Show all pastors currently serving churches classified in a particular category by a versioned external church dataset.
- Show Blue Ridge Presbytery ministers connected through seminary, RUF, former churches, committees, and public actions.
- Show institutional pipelines into General Assembly committees or study committees.

## Research-stage priority order

1. Preserve primary rosters and event lists.
2. Build complete current rosters for PCA committees/agencies.
3. Build current faculty rosters for Covenant Seminary and other high-overlap seminaries.
4. Reconstruct Tier A ministry careers and education.
5. Build/normalize PCA church directory data.
6. Import and resolve Save the PCA church-level dataset against the church directory.
7. Expand Tier B careers as overlaps become apparent.
8. Build derived detective views only after relationship/source coverage is sufficiently dense.

The current project is intentionally still in stages 1–4. UI sophistication should not outrun source coverage.
