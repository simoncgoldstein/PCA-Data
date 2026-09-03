# Entity inclusion policy

## Scope decision

The project will aim for **complete institutional coverage** of PCA churches and presbyteries, but **selective person coverage**.

This distinction is deliberate.

### Complete entities

The project should eventually contain every currently listed PCA:

- congregation / mission church in the official PCA church directory;
- presbytery in the official PCA presbytery list.

Historical churches and former presbyteries are added when they appear in a tracked person's career, a formal denominational action, a source-attributed practice dataset, a departure/merger, or another notable event.

### Selective people

A person enters the normalized graph when his or her name appears in a source that is independently relevant to the project, including:

1. formal network membership or leadership;
2. public-letter, protest, minority-report, overture, committee, or church-court participation;
3. current or historical leadership of a major PCA agency/institution;
4. seminary faculty/administration when the institution is being tracked;
5. author/editor/contributor/speaker in a tracked publication or event;
6. pastor/officer/staff role at a church **when that person already appears elsewhere in the graph**;
7. historically important pastor/officer role needed to explain a church or institutional trajectory;
8. named public role in a major controversy or policy action;
9. current external role needed to document the trajectory of an already-tracked person.

A person is **not** added merely because he or she is:

- an ordinary church member;
- the spouse of a tracked person;
- an unconnected ruling elder/deacon;
- a church staff member with no independent notable-source appearance;
- a conference attendee with no meaningful documented role;
- socially or professionally acquainted with a tracked person.

Exceptions are allowed when the person's role itself becomes evidentially important, but the reason for inclusion should be source-backed and explicit.

## Why every church but not every person?

Complete church coverage creates a stable institutional backbone. It lets the project answer questions such as:

- Which tracked people served at the same church?
- Which churches are in the same presbytery?
- Which churches appear in a source-attributed practice dataset?
- Which churches produced multiple signers of a public letter?
- Which churches later departed, merged, or changed presbyteries?

Importing every elder, deacon, spouse, and influential member would create an enormous population of low-signal people, increase identity-resolution risk, and raise privacy/accuracy concerns without materially improving the research questions.

## Person-church relationship rule

A church may contain many people in reality, but the graph stores only the **tracked people** whose relationship to that church is relevant and verifiable.

Example:

`Person A -> Senior Pastor -> Church X`

`Person B -> former RUF intern / member -> Church X`

`Church X -> Presbytery Y`

`Save the PCA dataset 2026-02-08 -> classified -> Church X`

The presence of the church-practice classification does not automatically attach the same position to Person A or Person B.

## Person identity threshold

Before creating a normalized person ID, require enough information to distinguish the person from same-name individuals. Preferred disambiguators:

- TE/RE/member status;
- church or institution;
- presbytery;
- city/state;
- contemporaneous role;
- exact source context.

Unresolved names remain source-level text until identity can be established.

## Historical spouse / family references

A spouse or family member is not automatically a person node. Add one only when that individual independently appears in a tracked publication, ministry role, public action, institution, or other notable source.

Example: Robin Wootton is independently included because she contributed to *Hear Us, Emmanuel*, has her own documented PCA-related writings, and now holds a formal religious-education role. Her inclusion is not simply because she is Robert Wootton's wife.

## Roster ingestion

Large rosters such as A Faithful PCA, Garris letters, Warhurst protest, NAE protest, study committees, and publication contributor lists are legitimate person-entry triggers because the person has affirmatively appeared in a tracked public/formal source.

For each roster participant preserve the contemporaneous role/church/presbytery exactly as printed before current-role research is attempted.

## Institutional staff ingestion

For major PCA institutions, complete current leadership/faculty rosters may be imported where the roster itself is analytically relevant. Ordinary administrative staff may remain source-level records until they intersect another tracked dataset.

Priority:

- executive leadership;
- ministry directors;
- faculty;
- board/trustee roles where public and useful;
- denominational program leadership;
- regional/campus leadership where the institution is a major personnel pipeline.

## Scoring

Being included as a person node does not itself imply any ideological classification. Church membership, education, family relationship, institutional employment, and ordinary pastoral service normally carry zero network-involvement weight unless another explicit action establishes a scored connection.
