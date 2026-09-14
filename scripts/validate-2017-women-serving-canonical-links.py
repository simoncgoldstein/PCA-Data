#!/usr/bin/env python3
"""Validate canonical person links for the 2017 Women Serving study committee."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
report_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-report.json"
edges_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-person-edges.json"
people_path = root / "data/people.json"

report = json.loads(report_path.read_text(encoding="utf-8"))
edges_data = json.loads(edges_path.read_text(encoding="utf-8"))
people = json.loads(people_path.read_text(encoding="utf-8"))
people_by_id = {row["id"]: row for row in people}

expected_roster = [
    ("TE Leon Brown", "Leon Brown", "TE", "Advisory Member"),
    ("TE William Castro", "William Castro", "TE", "Advisory Member"),
    ("TE Jeffrey Choi", "Jeffrey Choi", "TE", "Voting Member"),
    ("TE Dan Doriani", "Dan Doriani", "TE", "Advisory Member"),
    ("TE Ligon Duncan", "Ligon Duncan", "TE", "Voting Member"),
    ("TE Irwyn Ince", "Irwyn Ince", "TE", "Voting Member"),
    ("Mrs. Lani Jones", "Lani Jones", None, "Advisory Member"),
    ("Mrs. Kathy Keller", "Kathy Keller", None, "Voting Member"),
    ("Mrs. Mary Beth McGreevy", "Mary Beth McGreevy", None, "Voting Member"),
    ("TE Bruce O’Neil", "Bruce O’Neil", "TE", "Voting Member"),
    ("TE Harry Reeder", "Harry Reeder", "TE", "Voting Member"),
    ("TE Roy Taylor", "Roy Taylor", "TE", "Advisory Member"),
]

meta = edges_data.get("metadata", {})
if meta.get("dataset_id") != "2017_women_serving_ministry_person_edges":
    raise SystemExit("2017 women committee edges: dataset id drift")
if meta.get("event_id") != "2017-women-serving-ministry-study-committee":
    raise SystemExit("2017 women committee edges: event id drift")
if meta.get("event_type") != "study_committee":
    raise SystemExit("2017 women committee edges: event type drift")
if meta.get("source_family") != "ga_2017_women_serving_ministry":
    raise SystemExit("2017 women committee edges: source family drift")
if meta.get("primary_source") != report.get("metadata", {}).get("primary_source"):
    raise SystemExit("2017 women committee edges: primary source must match normalized report")
if meta.get("committee_member_count") != 12:
    raise SystemExit("2017 women committee edges: expected committee_member_count 12")
if meta.get("ideological_weight") != 0 or meta.get("score_included") is not False:
    raise SystemExit("2017 women committee edges: committee service must remain unscored")
modeling_rule = meta.get("modeling_rule", "")
for required_phrase in ("service on the 2017 study committee only", "does not assign", "separate first-person or signed evidence"):
    if required_phrase not in modeling_rule:
        raise SystemExit(f"2017 women committee edges: missing modeling guardrail phrase: {required_phrase}")

report_members = report.get("committee_members", [])
if len(report_members) != 12:
    raise SystemExit(f"2017 women report: expected 12 committee members, found {len(report_members)}")
actual_report_roster = [
    (row.get("name_as_printed"), row.get("name"), row.get("office_as_printed"), row.get("committee_status"))
    for row in report_members
]
if actual_report_roster != expected_roster:
    raise SystemExit("2017 women report: committee roster/order drift")

edges = edges_data.get("edges", [])
if len(edges) != 12:
    raise SystemExit(f"2017 women committee edges: expected 12 rows, found {len(edges)}")
if len({row.get("edge_id") for row in edges}) != 12:
    raise SystemExit("2017 women committee edges: edge ids must be unique")

actual_edge_roster = [
    (row.get("name_as_printed"), row.get("person_name"), row.get("office_as_printed"), row.get("role"))
    for row in edges
]
if actual_edge_roster != expected_roster:
    raise SystemExit("2017 women committee edges: roster must mirror the normalized report exactly")

status_counts = Counter(row.get("role") for row in edges)
if status_counts != {"Voting Member": 7, "Advisory Member": 5}:
    raise SystemExit(f"2017 women committee edges: role counts drift: {dict(status_counts)}")

for report_row, edge in zip(report_members, edges, strict=True):
    if edge.get("normalized_person_id") != report_row.get("normalized_person_id"):
        raise SystemExit(f"{edge.get('person_name')}: report/edge canonical id mismatch")
    if edge.get("evidence_kind") != "study_committee_service":
        raise SystemExit(f"{edge.get('person_name')}: evidence kind drift")
    if edge.get("confidence") != "confirmed":
        raise SystemExit(f"{edge.get('person_name')}: official committee service should remain confirmed")
    if edge.get("weight") != 0 or edge.get("score_included") is not False:
        raise SystemExit(f"{edge.get('person_name')}: committee service must remain unscored")
    forbidden_keys = {"position_id", "position", "position_summary", "report_level_positions"}
    if forbidden_keys.intersection(edge):
        raise SystemExit(f"{edge.get('person_name')}: report-level position leaked into person edge")

    person_id = edge.get("normalized_person_id")
    if person_id is None:
        if edge.get("identity_status") != "unresolved":
            raise SystemExit(f"{edge.get('person_name')}: null person id must remain explicitly unresolved")
        continue

    if edge.get("identity_status") != "resolved_existing_canonical_person":
        raise SystemExit(f"{edge.get('person_name')}: resolved id must have resolved identity status")
    if person_id not in people_by_id:
        raise SystemExit(f"{edge.get('person_name')}: canonical id {person_id!r} is absent from data/people.json")
    if people_by_id[person_id].get("name") != edge.get("person_name"):
        raise SystemExit(
            f"{edge.get('person_name')}: canonical name mismatch for {person_id}: "
            f"{people_by_id[person_id].get('name')!r}"
        )

resolved = {
    row["person_name"]: row["normalized_person_id"]
    for row in edges
    if row.get("normalized_person_id") is not None
}
required_resolved = {
    "Irwyn Ince": "irwyn-ince",
    "Bruce O’Neil": "bruce-o-neil",
}
for name, person_id in required_resolved.items():
    if resolved.get(name) != person_id:
        raise SystemExit(f"2017 women committee edges: required canonical link missing: {name} -> {person_id}")

print(
    "2017 women-serving canonical links OK: "
    f"{len(edges)} committee rows, {len(resolved)} resolved canonical identities, "
    f"{len(edges) - len(resolved)} explicitly unresolved identities"
)
