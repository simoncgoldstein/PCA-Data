#!/usr/bin/env python3
"""Calculate conservative person-roster overlaps from confirmed identities only."""

from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


if len(sys.argv) not in (1, 2):
    raise SystemExit("usage: build-overlap-analysis.py [repo-root]")

ROOT = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
OUT = ROOT / "analysis/overlap"
OUT.mkdir(parents=True, exist_ok=True)
GENERATED_ON = "2026-09-04"


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def write_json(name: str, value: Any) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(name: str, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with (OUT / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


crosswalk = load("sources/normalized/identity/person-crosswalk.json")
identity_summary = load("sources/normalized/identity/summary.json")
people = {p["id"]: p for p in load("data/people.json")}
records = crosswalk["records"]
confirmed_statuses = {"exact_confirmed", "context_confirmed"}

by_dataset: dict[str, list[dict[str, Any]]] = defaultdict(list)
by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
for row in records:
    by_dataset[row["source_dataset"]].append(row)
    if row["canonical_person_id"] and row["match_status"] in confirmed_statuses:
        by_person[row["canonical_person_id"]].append(row)

datasets = sorted(by_dataset)
confirmed_sets = {
    dataset: {r["canonical_person_id"] for r in rows if r["canonical_person_id"] and r["match_status"] in confirmed_statuses}
    for dataset, rows in by_dataset.items()
}


# Dataset coverage.
coverage_rows = []
for item in identity_summary["datasets"]:
    counts = item["match_status_counts"]
    coverage_rows.append({
        "source_dataset": item["source_dataset"],
        "row_count": item["row_count"],
        "unique_printed_name_count": item["unique_printed_name_count"],
        "confirmed_canonical_person_count": item["confirmed_canonical_person_count"],
        "unmatched_count": counts["unmatched"],
        "probable_requires_review_count": counts["probable_requires_review"],
        "ambiguous_or_collision_count": counts["ambiguous"] + counts["collision"],
        "percentage_resolved": item["percent_rows_resolved"],
        "source_tier": item["source_tier"],
        "completeness_status": item["completeness_status"],
    })
write_json("dataset-coverage.json", {
    "metadata": {
        "generated_on": GENERATED_ON,
        "measurement": "Resolution coverage for the exact source rows included in the identity crosswalk; percentages are row-resolution rates, not population estimates.",
    },
    "datasets": coverage_rows,
})
coverage_by_dataset = {row["source_dataset"]: row for row in coverage_rows}


# Pairwise confirmed overlap plus exact-name possible overlaps kept separate.
pairwise_rows: list[dict[str, Any]] = []
pairwise_shared: list[dict[str, Any]] = []
for left_index, left in enumerate(datasets):
    for right in datasets[left_index + 1:]:
        left_ids, right_ids = confirmed_sets[left], confirmed_sets[right]
        shared = sorted(left_ids & right_ids)
        union = left_ids | right_ids
        left_keys = {r["normalized_candidate"] for r in by_dataset[left]}
        right_keys = {r["normalized_candidate"] for r in by_dataset[right]}
        unresolved_keys = []
        for key in sorted(left_keys & right_keys):
            left_key_ids = {r["canonical_person_id"] for r in by_dataset[left] if r["normalized_candidate"] == key and r["canonical_person_id"]}
            right_key_ids = {r["canonical_person_id"] for r in by_dataset[right] if r["normalized_candidate"] == key and r["canonical_person_id"]}
            if not (left_key_ids & right_key_ids):
                unresolved_keys.append(key)
        pairwise_rows.append({
            "dataset_a": left,
            "dataset_b": right,
            "roster_a_unique_printed_names": coverage_by_dataset[left]["unique_printed_name_count"],
            "roster_b_unique_printed_names": coverage_by_dataset[right]["unique_printed_name_count"],
            "confirmed_subset_a_count": len(left_ids),
            "confirmed_subset_b_count": len(right_ids),
            "confirmed_intersection_count": len(shared),
            "confirmed_union_count": len(union),
            "jaccard_similarity": f"{(len(shared) / len(union) if union else 0):.6f}",
            "percent_of_confirmed_subset_a_in_b": f"{(100 * len(shared) / len(left_ids) if left_ids else 0):.2f}",
            "percent_of_confirmed_subset_b_in_a": f"{(100 * len(shared) / len(right_ids) if right_ids else 0):.2f}",
            "confirmed_lower_bound_percent_of_roster_a_in_b": f"{(100 * len(shared) / coverage_by_dataset[left]['unique_printed_name_count'] if coverage_by_dataset[left]['unique_printed_name_count'] else 0):.2f}",
            "confirmed_lower_bound_percent_of_roster_b_in_a": f"{(100 * len(shared) / coverage_by_dataset[right]['unique_printed_name_count'] if coverage_by_dataset[right]['unique_printed_name_count'] else 0):.2f}",
            "unresolved_possible_overlap_count": len(unresolved_keys),
        })
        if shared or unresolved_keys:
            shared_people = []
            for person_id in shared:
                shared_people.append({
                    "canonical_person_id": person_id,
                    "name": people[person_id]["name"],
                    "dataset_a_locators": [r["source_row_locator"] for r in by_dataset[left] if r["canonical_person_id"] == person_id],
                    "dataset_b_locators": [r["source_row_locator"] for r in by_dataset[right] if r["canonical_person_id"] == person_id],
                })
            pairwise_shared.append({
                "dataset_a": left,
                "dataset_b": right,
                "confirmed_shared_people": shared_people,
                "unresolved_exact_name_keys": unresolved_keys,
            })

write_csv(
    "pairwise-overlap.csv",
    ["dataset_a", "dataset_b", "roster_a_unique_printed_names", "roster_b_unique_printed_names", "confirmed_subset_a_count", "confirmed_subset_b_count", "confirmed_intersection_count", "confirmed_union_count", "jaccard_similarity", "percent_of_confirmed_subset_a_in_b", "percent_of_confirmed_subset_b_in_a", "confirmed_lower_bound_percent_of_roster_a_in_b", "confirmed_lower_bound_percent_of_roster_b_in_a", "unresolved_possible_overlap_count"],
    pairwise_rows,
)
write_json("pairwise-shared-people.json", {
    "metadata": {
        "generated_on": GENERATED_ON,
        "confirmed_rule": "Only shared canonical_person_id values with exact_confirmed/context_confirmed status are counted.",
        "possible_overlap_rule": "Exact normalized printed-name overlaps without a shared confirmed ID are listed separately and excluded from all confirmed metrics.",
    },
    "pairs_with_confirmed_or_possible_overlap": pairwise_shared,
})


# Multi-roster recurrence.
recurrence_rows = []
for person_id, person_rows in sorted(by_person.items(), key=lambda item: (people[item[0]]["name"], item[0])):
    person_datasets = sorted({r["source_dataset"] for r in person_rows})
    person_families = sorted({r["source_family"] for r in person_rows})
    if len(person_families) < 2:
        continue
    evidence_types = sorted({r["evidence_type"] for r in person_rows})
    source_locators = [f"{r['source_dataset']}::{r['source_row_locator']}" for r in sorted(person_rows, key=lambda r: (r["source_dataset"], r["source_row_locator"]))]
    recurrence_rows.append({
        "canonical_person_id": person_id,
        "name": people[person_id]["name"],
        "dataset_count": len(person_datasets),
        "independent_source_family_count": len(person_families),
        "datasets": "; ".join(person_datasets),
        "source_families": "; ".join(person_families),
        "evidence_types": "; ".join(evidence_types),
        "source_locators": "; ".join(source_locators),
    })
recurrence_rows.sort(key=lambda r: (-int(r["dataset_count"]), r["name"], r["canonical_person_id"]))
write_csv("person-recurrence.csv", ["canonical_person_id", "name", "dataset_count", "independent_source_family_count", "datasets", "source_families", "evidence_types", "source_locators"], recurrence_rows)
recurring_ids = {r["canonical_person_id"] for r in recurrence_rows}


# Presbytery concentration: dataset-level observed denominators and an aggregate.
presbytery_entities = load("data/presbyteries.json")
presbytery_id_by_name = {norm(row["name"]): row["id"] for row in presbytery_entities}
presbytery_aliases = {
    "iliana": "illiana",
    "korean capitol": "korean-capital",
    "metro new york": "metropolitan-new-york",
    "new york metro": "metropolitan-new-york",
    "of northern illinois": "northern-illinois",
    "pnw": "pacific-northwest",
    "rocky mtn": "rocky-mountain",
    "s new england": "southern-new-england",
    "se alabama": "southeast-alabama",
    "se louisiana": "southern-louisiana",
    "siouxland": "siouxlands",
    "sothern new england": "southern-new-england",
    "southcoast": "south-coast",
    "suncoast": "suncoast-florida",
    "susquehanna": "susquehanna-valley",
    "tvp": "tennessee-valley",
}
presbytery_rows = []
for dataset in datasets + ["ALL_TRACKED_DATASETS"]:
    subset = records if dataset == "ALL_TRACKED_DATASETS" else by_dataset[dataset]
    presbyteries = sorted({p for r in subset for p in r["presbyteries"]})
    for presbytery in presbyteries:
        local = [r for r in subset if presbytery in r["presbyteries"]]
        printed_keys = {r["normalized_candidate"] for r in local}
        confirmed_ids = {r["canonical_person_id"] for r in local if r["canonical_person_id"] and r["match_status"] in confirmed_statuses}
        recurrent = confirmed_ids & recurring_ids
        presbytery_id = presbytery_id_by_name.get(presbytery) or presbytery_aliases.get(presbytery)
        canonicalization_status = "current_exact" if presbytery in presbytery_id_by_name else ("known_alias" if presbytery in presbytery_aliases else "unresolved_historical_or_noncanonical")
        presbytery_rows.append({
            "source_dataset": dataset,
            "presbytery_normalized": presbytery,
            "presbytery_id": presbytery_id or "",
            "canonicalization_status": canonicalization_status,
            "observed_roster_rows": len(local),
            "unique_printed_name_denominator": len(printed_keys),
            "confirmed_person_count": len(confirmed_ids),
            "confirmed_resolution_rate": f"{(100 * len(confirmed_ids) / len(printed_keys) if printed_keys else 0):.2f}",
            "multi_roster_person_count": len(recurrent),
            "multi_roster_rate_among_confirmed": f"{(100 * len(recurrent) / len(confirmed_ids) if confirmed_ids else 0):.2f}",
        })
write_csv(
    "presbytery-concentration.csv",
    ["source_dataset", "presbytery_normalized", "presbytery_id", "canonicalization_status", "observed_roster_rows", "unique_printed_name_denominator", "confirmed_person_count", "confirmed_resolution_rate", "multi_roster_person_count", "multi_roster_rate_among_confirmed"],
    presbytery_rows,
)


# Exact current-directory church matching for the structured 2022 AFP snapshot.
churches = load("data/churches.json")
church_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
for church in churches:
    church_index[norm(church["name"])].append(church)
afp_2022 = load("sources/normalized/public-statements/a-faithful-pca/signers-2022-03-14.json")["signers"]
afp_crosswalk = {
    r["source_row_locator"]: r
    for r in by_dataset["a_faithful_pca_2022-03-14"]
}
church_observations: dict[str, list[dict[str, Any]]] = defaultdict(list)
unmatched_church_strings = Counter()
ambiguous_church_strings = Counter()
for signer in afp_2022:
    cross = afp_crosswalk[f"signature:{signer['sequence_number']}"]
    for printed_org in signer.get("church_or_institution_as_printed") or []:
        candidates = church_index.get(norm(printed_org), [])
        printed_presbytery = norm(signer.get("presbytery_as_printed") or "").replace(" presbytery", "")
        if len(candidates) > 1 and printed_presbytery:
            filtered = [c for c in candidates if norm(c.get("presbytery_as_printed") or "") == printed_presbytery]
            if filtered:
                candidates = filtered
        if len(candidates) == 1:
            church_observations[candidates[0]["id"]].append({"signer": signer, "crosswalk": cross})
        elif candidates:
            ambiguous_church_strings[printed_org] += 1
        else:
            unmatched_church_strings[printed_org] += 1

church_rows = []
church_by_id = {c["id"]: c for c in churches}
for church_id, observations in sorted(church_observations.items()):
    church = church_by_id[church_id]
    printed_keys = {o["crosswalk"]["normalized_candidate"] for o in observations}
    confirmed_ids = {o["crosswalk"]["canonical_person_id"] for o in observations if o["crosswalk"]["canonical_person_id"]}
    recurrent = confirmed_ids & recurring_ids
    church_rows.append({
        "church_id": church_id,
        "church_name": church["name"],
        "presbytery_id": church.get("presbytery_id") or "",
        "source_dataset": "a_faithful_pca_2022-03-14",
        "observed_roster_rows": len(observations),
        "unique_printed_name_denominator": len(printed_keys),
        "confirmed_person_count": len(confirmed_ids),
        "confirmed_resolution_rate": f"{(100 * len(confirmed_ids) / len(printed_keys) if printed_keys else 0):.2f}",
        "multi_roster_person_count": len(recurrent),
        "multi_roster_rate_among_confirmed": f"{(100 * len(recurrent) / len(confirmed_ids) if confirmed_ids else 0):.2f}",
    })
church_rows.sort(key=lambda r: (-int(r["multi_roster_person_count"]), -int(r["confirmed_person_count"]), r["church_name"]))
write_csv(
    "church-concentration.csv",
    ["church_id", "church_name", "presbytery_id", "source_dataset", "observed_roster_rows", "unique_printed_name_denominator", "confirmed_person_count", "confirmed_resolution_rate", "multi_roster_person_count", "multi_roster_rate_among_confirmed"],
    church_rows,
)


# Dated institutional role pipelines into/out of other documented action types.
event_years = {
    "warhurst_protest_2019": 2019,
    "overture_37_minority_2021": 2021,
    "overture_15_minority_2022": 2022,
    "overture_15_negative_votes_2022": 2022,
    "nae_withdrawal_protest_2022": 2022,
    "a_faithful_pca_2021-06-11": 2021,
    "a_faithful_pca_2022-03-14": 2022,
    "publication_heal-us-emmanuel-2016": 2016,
    "publication_co-laborers-co-heirs-2019": 2019,
    "publication_hear-us-emmanuel-2020": 2020,
    "amr_leadership_current": 2026,
    "amr_website_media_2023_2026": None,
    "national_partnership_confirmed_members": None,
}
pipeline_people = []
sequence_counts: Counter[tuple[str, str]] = Counter()
for person_id, person_rows in sorted(by_person.items()):
    institutional = [r for r in person_rows if r["evidence_type"] == "institutional_role"]
    other = [r for r in person_rows if r["evidence_type"] != "institutional_role"]
    if not institutional or not other:
        continue
    role_edges = []
    for row in sorted(institutional, key=lambda r: (r["source_dataset"], r["source_row_locator"])):
        organization = row["source_dataset"].removeprefix("institution_")
        role_edges.append({
            "organization": organization,
            "snapshot_date": "2026-09-03",
            "source_path": row["source_path"],
            "source_locator": row["source_row_locator"],
            "relationship_type": "institutional_role",
        })
        for action in other:
            sequence_counts[(organization, action["source_dataset"])] += 1
    pipeline_people.append({
        "canonical_person_id": person_id,
        "name": people[person_id]["name"],
        "dated_institutional_role_edges": role_edges,
        "other_documented_edges": [
            {
                "dataset": row["source_dataset"],
                "year": event_years.get(row["source_dataset"]),
                "relationship_type": row["evidence_type"],
                "source_path": row["source_path"],
                "source_locator": row["source_row_locator"],
            }
            for row in sorted(other, key=lambda r: (r["source_dataset"], r["source_row_locator"]))
        ],
    })
write_json("institutional-pipelines.json", {
    "metadata": {
        "generated_on": GENERATED_ON,
        "measurement": "Confirmed people with a dated 2026-09-03 institutional role snapshot and at least one separately documented action, membership, publication, leadership, or media edge.",
        "causation_warning": "Sequences and co-occurrences are descriptive. They do not establish recruitment, influence, agreement, or causation.",
    },
    "people": pipeline_people,
    "common_role_to_dataset_cooccurrences": [
        {"institution": institution, "other_dataset": dataset, "confirmed_person_count": count}
        for (institution, dataset), count in sorted(sequence_counts.items(), key=lambda item: (-item[1], item[0]))
    ],
})


# Bipartite identity graph quality.
person_nodes = set(people)
dataset_nodes = {f"dataset:{dataset}" for dataset in datasets}
adjacency: dict[str, set[str]] = defaultdict(set)
edge_type_counts = Counter()
evidence_tier_counts = Counter()
source_paths = set()
missing_date_edges = 0
for row in records:
    if not row["canonical_person_id"] or row["match_status"] not in confirmed_statuses:
        continue
    person_node = f"person:{row['canonical_person_id']}"
    dataset_node = f"dataset:{row['source_dataset']}"
    adjacency[person_node].add(dataset_node)
    adjacency[dataset_node].add(person_node)
    edge_type_counts[row["evidence_type"]] += 1
    evidence_tier_counts[row["source_tier"]] += 1
    source_paths.add(row["source_path"])
    if event_years.get(row["source_dataset"]) is None and not row["source_dataset"].startswith("institution_"):
        missing_date_edges += 1

all_graph_nodes = {f"person:{person_id}" for person_id in person_nodes} | dataset_nodes
seen = set()
component_sizes = []
for node in sorted(all_graph_nodes):
    if node in seen:
        continue
    queue = deque([node])
    seen.add(node)
    size = 0
    while queue:
        current = queue.popleft()
        size += 1
        for neighbor in adjacency[current]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    component_sizes.append(size)
edge_count = sum(edge_type_counts.values())
possible_bipartite_edges = len(person_nodes) * len(dataset_nodes)
unresolved_counts = Counter(r["match_status"] for r in records if not r["canonical_person_id"])
non_primary_datasets = sorted({
    dataset for dataset, rows in by_dataset.items()
    if not any(r["source_tier"] in {"official_primary", "primary_archive", "first_party", "first_party_archive", "official_institutional"} for r in rows)
})
write_json("graph-quality.json", {
    "metadata": {
        "generated_on": GENERATED_ON,
        "graph_scope": "Confirmed identity-to-dataset bipartite graph plus counts of repository core node classes.",
    },
    "nodes": {
        "person_nodes": len(person_nodes),
        "dataset_nodes": len(dataset_nodes),
        "organization_nodes": len(load("data/organizations.json")),
        "church_nodes": len(churches),
        "presbytery_nodes": len(presbytery_entities),
        "event_nodes": len(load("data/events.json")),
    },
    "edges": {
        "confirmed_identity_dataset_edges": edge_count,
        "by_evidence_type": dict(sorted(edge_type_counts.items())),
        "by_source_tier": dict(sorted(evidence_tier_counts.items())),
        "distinct_source_paths": len(source_paths),
    },
    "density": {
        "definition": "confirmed identity-dataset edges / (person nodes × dataset nodes)",
        "value": round(edge_count / possible_bipartite_edges, 8) if possible_bipartite_edges else 0,
    },
    "components": {
        "count": len(component_sizes),
        "largest_component_nodes": max(component_sizes) if component_sizes else 0,
        "isolated_person_nodes": sum(1 for person_id in person_nodes if not adjacency[f"person:{person_id}"]),
    },
    "quality_gaps": {
        "unresolved_identity_rows": sum(unresolved_counts.values()),
        "unresolved_by_status": dict(sorted(unresolved_counts.items())),
        "confirmed_edges_missing_specific_event_year": missing_date_edges,
        "datasets_without_primary_or_official_tier": non_primary_datasets,
        "unmatched_structured_church_strings_2022_afp": sum(unmatched_church_strings.values()),
        "ambiguous_structured_church_strings_2022_afp": sum(ambiguous_church_strings.values()),
        "unresolved_historical_or_noncanonical_presbytery_names": sorted({
            row["presbytery_normalized"] for row in presbytery_rows
            if row["canonicalization_status"] == "unresolved_historical_or_noncanonical"
        }),
    },
    "claims_excluded_from_scoring": [
        "probable, ambiguous, collision, and unmatched identity rows",
        "institutional employment, education, governance, and ordinary church roles",
        "publication participation as proof of agreement with every argument",
        "absence from a roster as evidence of opposition",
        "source-audit screenshot highlighting as independent proof of National Partnership membership",
        "third-party sensitive-personal claims",
    ],
})

print(json.dumps({
    "datasets": len(datasets),
    "pairwise_rows": len(pairwise_rows),
    "recurring_people": len(recurrence_rows),
    "presbytery_rows": len(presbytery_rows),
    "matched_churches": len(church_rows),
    "pipeline_people": len(pipeline_people),
    "confirmed_graph_edges": edge_count,
}, indent=2))
