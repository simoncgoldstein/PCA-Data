# PCA Networks & Institutional Activity

A source-driven research project mapping people, organizations, public actions, denominational roles, and institutional trajectories in and around the Presbyterian Church in America (PCA).

The public site is designed to answer three questions:

1. **Who repeatedly appears across the same networks, coalitions, committees, and public actions?**
2. **How are those people and institutions connected over time?**
3. **What primary or reliable source supports each claimed connection?**

## Methodological rule

The project stores **claims and evidence**, not labels by reputation. A person is not classified on the basis of friendship, church attendance, conference proximity, or a single disputed vote. Each displayed connection has a type, confidence level, date range, and source.

The UI may calculate an analytical **Network Involvement Index**, but the underlying evidence remains visible and independently inspectable. The index measures recurrence and organizational involvement in the networks studied. It is not a claim about every aspect of a person's theology.

## Evidence levels

- **Confirmed**: a primary source explicitly establishes the connection.
- **Strongly supported**: multiple reliable sources establish the connection, but no direct roster or equivalent primary record is available.
- **Associated**: participation or institutional relationship is established, but membership or ideological agreement is not.
- **Unresolved**: a possible identity or connection that requires further verification.

Negative findings such as `National Partnership member: not established` are intentionally preserved where useful.

## Repository structure

```text
PCA-Data/
├─ index.html
├─ styles.css
├─ app.js
├─ data/
│  ├─ people.json
│  ├─ organizations.json
│  ├─ events.json
│  ├─ affiliations.json
│  └─ sources.json
├─ research/
│  ├─ methodology.md
│  ├─ source-register.md
│  └─ unresolved-identities.md
└─ README.md
```

## Initial source universe

The v1 research model includes, among other sources:

- National Partnership correspondence, 2013–2021
- Alliance for Mission & Renewal, founding and current leadership
- Denominational Renewal / earlier renewal efforts
- Mike Khandjian's Fellowship and related networks where independently documented
- General Assembly protests, minority reports, committees, and overture activity
- 2017 Women Serving in Ministry Study Committee
- 2019 Warhurst protest
- 2021 Looking Forward Together and Overture 37 activity
- Garris investigation letters
- A Call to Prayer & Lament
- Current institutional roles in PCA and adjacent organizations

## GitHub Pages

This is a static site: HTML + CSS + JavaScript + JSON. No server or database is required. Once GitHub Pages is enabled for the repository root on `main`, `index.html` is the public application.

## Status

**v0.1 research scaffold.** The first dataset is intentionally conservative and incomplete. Additional people and events will be added as claims are normalized and sourced.
