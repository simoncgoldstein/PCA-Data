# Methodology

## Purpose

This project maps recurring personnel, organizations, coalitions, public actions, denominational roles, and institutional trajectories in and around the Presbyterian Church in America (PCA).

The central research question is not simply, "Who is progressive?" That label is too elastic to function as raw data. The project instead asks:

- Who is formally involved in the same organizations or networks?
- Who repeatedly signs or organizes the same public actions?
- Who serves in denominational committees, agencies, or leadership roles relevant to the controversies being studied?
- Which personnel relationships persist across time and institutions?
- Where are historically significant participants serving now?

Interpretation is downstream of those facts.

## Core distinction: fact versus classification

The database stores factual claims such as:

- `Founding Executive Board, Alliance for Mission & Renewal`
- `Signer, Garris Letter 1`
- `Initial Signatory, A Call to Prayer & Lament`
- `National Partnership member`
- `Visiting Theologian for Mission, Grace Mosaic`

It should not store unsupported conclusions such as:

- `progressive because he knows X`
- `member of network Y because he attended one event`
- `holds position Z because another signer does`

A person-level analytical category may later be derived from multiple independent facts, but the underlying facts must remain visible.

## Edge types

Connections in the graph should use typed edges. At minimum:

1. **Formal organizational affiliation**
   - founder
   - board member
   - officer
   - confirmed member
   - staff role

2. **Public coalition action**
   - signer
   - author
   - organizer
   - minority-report signer
   - protest signer

3. **Denominational action**
   - committee member
   - committee chair
   - overture author/sponsor
   - SJC/RPR/Overtures Committee role
   - Moderator or stated denominational office

4. **Institutional placement**
   - MNA
   - RUF
   - Covenant Seminary
   - church/presbytery
   - external institution

5. **Collaboration**
   - co-author
   - co-organizer
   - documented project collaboration

6. **Adjacency**
   - conference participant
   - network-supported candidate
   - other established relationship that does not prove membership

Adjacency should never render visually as equivalent to formal membership.

## Confidence levels

### Confirmed
A primary source explicitly establishes the connection. Examples:

- organization roster names the person;
- signed public letter names the person;
- official GA minutes record the person;
- leaked correspondence explicitly says the person is a member;
- current institution lists the person's role.

### Strongly supported
Multiple reliable sources establish the connection, or a primary archive is known to contain the explicit record but the exact page/message pin has not yet been normalized.

### Associated
The relationship is established, but membership or ideological agreement is not. Examples include an organization promoting a candidate, a conference appearance, or a collaboration.

### Unresolved
There is a plausible match or claim requiring further verification. Unresolved edges should be excluded from the default public score and clearly marked.

## Negative findings

Negative evidence can be important. A profile may explicitly preserve findings such as:

- `National Partnership membership: not established`
- `Prayer & Lament initial signer: no`
- `Garris letters: no verified signature`

This is especially important when a person has substantial adjacency but the evidence does not support formal membership.

## Network Involvement Index

The index measures repeated, documented involvement in the source universe being studied. It is not an assessment of Christian character, orthodoxy, confessional subscription, or every theological position a person holds.

Current provisional weights:

| Evidence | Typical weight |
| --- | ---: |
| Founder / principal organizer of a network | 5 |
| Confirmed formal network membership or founding board | 4 |
| Coalition organizer / study committee leadership | 4 |
| Public-letter, protest, or minority-report signer | 3 |
| Continuing network leadership | 2–3 |
| Network-supported candidate / meaningful adjacency | 1–2 |
| Collaboration such as co-authorship | 1 |
| Current institutional role alone | 0 |
| Unresolved claim | 0 |

Weights may change as the dataset matures. Any change should be documented in version control.

### Avoiding double counting

Long-term continuity can be analytically meaningful. A founding-board role and a current-board role may both appear, but current continuity is intentionally weighted lower than the original formal affiliation. Future versions may cap repeated signals within one organization.

## Current positions and trajectory

Each major person's record should include, where verifiable:

- current role;
- current organization;
- current church;
- denominational status;
- current presbytery;
- external networks;
- former key roles;
- date the current role was verified;
- sources.

Current roles outside the PCA are included because institutional migration is historically informative. They do not automatically contribute to the Network Involvement Index.

## Source hierarchy

Preferred order:

1. PCA General Assembly minutes and committee reports
2. Original organization/network correspondence or roster
3. Original public letters/statements
4. Current official church, agency, seminary, or nonprofit biography
5. Contemporaneous reporting reproducing or linking primary material
6. Secondary analysis

Secondary analysis may identify where to look, but disputed person-level membership should normally require primary evidence or strong corroboration.

## National Partnership archive rule

The National Partnership archive is a central source class. Claims should eventually point to:

- year;
- message date;
- sender;
- relevant page or section;
- exact nature of the evidence.

The broad archive index is acceptable during data normalization, but it should not remain the final citation for high-importance membership claims.

## Prayer & Lament data-integrity rule

The public Prayer & Lament page states that a verification step was added after disruptive submissions. Raw form scrapes therefore cannot automatically be treated as a verified membership/signature roster.

For v1:

- **Initial Signatories** displayed by the public site are confirmed.
- Later signers require corroboration from a reliable capture, contemporaneous record, or other verification before being marked confirmed.
- Obvious malformed, duplicate, joke, or identity-conflicted submissions are excluded.

## General Assembly action rule

A GA vote alone is generally weak evidence of network identity.

Higher-value actions include:

- authoring or sponsoring an overture;
- signing a formal protest;
- signing a minority report;
- leading a study committee;
- repeated committee placement explicitly documented by a network;
- repeated action across multiple independent controversies.

Each action should be labeled literally. For example, `2019 Warhurst Protest Signer` is preferable to an interpretive label such as `pro-Revoice` because the protest concerned a specific procedural/rhetorical issue.

## Geographic data

Church and presbytery affiliations are ordinary metadata. No church or presbytery receives special public emphasis merely because it is of private interest to a researcher.

Historical and current affiliations should be date-aware where possible.

## Corrections

Corrections should be welcomed when accompanied by documentary evidence. A correction should update both:

1. the factual record; and
2. the source explaining the correction.

Git history provides an audit trail of changes.
