# Network-overlap audit — 2026-09-04

## 1. What is measured

This first overlap pass measures shared **confirmed canonical people** across 27 source-bounded rosters and role/media datasets. It does not measure ideology, agreement with every co-participant, or the unobserved PCA population.

The analysis contains 351 pairwise comparisons, 204 people recurring across at least two independent source families, 559 dataset/presbytery concentration rows, 208 exactly matched current-directory churches from the structured 2022 A Faithful PCA fields, six confirmed institution-to-action pipeline people, and 660 confirmed identity-to-dataset graph edges.

Every pairwise result reports two percentage types:

- `percent_of_confirmed_subset_*` uses only the resolved canonical subset as its denominator.
- `confirmed_lower_bound_percent_of_roster_*` divides the confirmed intersection by all unique printed names in that roster. It is a defensible lower bound while identity resolution remains incomplete.

## 2. Strongest observed overlaps

The strongest large-roster confirmed overlaps, excluding the two snapshots of the same A Faithful PCA source family, are:

| Roster pair | Confirmed shared people | Jaccard on confirmed subsets | Lower bound of roster A | Lower bound of roster B | Unresolved exact-name possibilities |
|---|---:|---:|---:|---:|---:|
| 2022 A Faithful PCA × 2019 Warhurst protest | 78 | 0.464286 | 10.60% | 38.42% | 9 |
| 2022 NAE-withdrawal protest × 2022 Overture 15 negative votes | 53 | 0.417323 | 26.11% | 26.63% | 15 |
| 2022 A Faithful PCA × 2022 Overture 15 negative votes | 59 | 0.301020 | 8.02% | 29.65% | 12 |
| 2022 A Faithful PCA × confirmed National Partnership members | 35 | 0.221519 | 4.76% | 23.18% | 19 |
| Confirmed National Partnership members × 2019 Warhurst protest | 17 | 0.149123 | 11.26% | 8.37% | 14 |

The most recurrent confirmed people in the present source universe include David Richter, Geoff Ziegler, and Irwyn Ince in seven datasets each; David Cassidy, Owen Lee, Peter Rowan, Scott Sauls, and Sean Lucas in six each. These are counts of distinct documented appearances, with evidence types preserved separately.

## 3. Denominator and identity limits

Resolution remains incomplete: 2,056 of 2,716 crosswalk rows do not have a confirmed ID. The key large-roster resolved-person coverage is 154 of 737 rows for the 2022 A Faithful PCA snapshot, 101 of 199 for the Overture 15 negative-vote roster, 92 of 203 for the Warhurst protest, 79 of 203 for the NAE-withdrawal protest, and 39 of 151 for confirmed National Partnership printed-name records.

Accordingly, confirmed-subset percentages can be much higher than whole-roster lower bounds and must never be presented as full-roster rates. Unresolved exact-name possibilities are displayed separately and excluded from all confirmed intersections, unions, recurrence counts, concentration counts, and graph edges.

Presbytery and church rates use observed roster names as denominators. They are not rates among all PCA ministers, elders, churches, or members. Presbytery rows distinguish current exact names, documented aliases, and unresolved historical/noncanonical source labels; none is silently coerced. Current institutional snapshots are dated neutral role observations, and the current-directory church match excludes non-unique or non-exact strings.

## 4. Source families that would most improve the graph

1. Complete official RUF, RTS, MNA, MTW, Covenant College, and WTS profiles with exact roles, locations, and profile URLs.
2. Distinct AMR Substack and YouTube inventories with stable item/video IDs, participants, and official captions.
3. An original or reconstructed primary-source Revoice 2018 program.
4. Primary church/presbytery context for the 226 probable identity rows and stronger disambiguation for 276 ambiguous rows.
5. Current and historical church crosswalks for organization strings that do not exactly match the 2026 PCA directory.

## 5. Findings safe for a future interface

The interface can safely show exact roster membership/action labels, confirmed shared-person lists with source locators, resolved-subset Jaccard values, whole-roster confirmed lower bounds, recurrence by typed evidence, and dated zero-weight institutional role edges. It can also expose unresolved possible overlaps as a visibly separate review layer.

Drill-down should retain the printed name, exact source dataset, source row/page or URL locator, match status, match method, and supporting context. Pairwise views should show both denominator types together.

## 6. Findings that must remain qualified or excluded

- Do not describe the Warhurst protest roster as generically pro-Revoice.
- Do not treat a negative vote, protest signature, minority-report signature, publication contribution, or media appearance as interchangeable.
- Do not interpret absence from any roster as opposition.
- Do not turn institutional employment, education, ordinary church service, or source-attributed church classifications into person-level ideology.
- Do not treat screenshot highlighting as independent proof of National Partnership membership.
- Do not count probable, ambiguous, collision, initials-only, or unmatched names as shared people.
- Do not infer causation or recruitment from institutional pipeline co-occurrence.

## Outputs

- `analysis/overlap/dataset-coverage.json`
- `analysis/overlap/pairwise-overlap.csv`
- `analysis/overlap/pairwise-shared-people.json`
- `analysis/overlap/person-recurrence.csv`
- `analysis/overlap/presbytery-concentration.csv`
- `analysis/overlap/church-concentration.csv`
- `analysis/overlap/institutional-pipelines.json`
- `analysis/overlap/graph-quality.json`
- `scripts/build-overlap-analysis.py`

Both builders were rerun after generation and produced no diff.
