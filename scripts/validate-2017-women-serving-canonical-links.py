#!/usr/bin/env python3
"""Validate canonical person links and app projection for the 2017 Women Serving study committee."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
report_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-report.json"
edges_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-person-edges.json"
people_path = root / "data/people.json"
events_path = root / "data/events.json"
affiliations_path = root / "data/affiliations.json"
sources_path = root / "data/sources.json"

report = json.loads(report_path.read_text(encoding="utf-8"))
edges_data = json.loads(edges_path.read_text(encoding="utf-8"))
people = json.loads(people_path.read_text(encoding="utf-8"))
events = json.loads(events_path.read_text(encoding="utf-8"))
affiliations = json.loads(affiliations_path.read_text(encoding="utf-8"))
sources = json.loads(sources_path.read_text(encoding="utf-8"))
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

# App-facing projection. Only canonical identities are projected into data/affiliations.json.
app_event_id = "evt-women-serving-study-committee-2017"
app_source_id = "src-ga45-women-serving-2017"

matching_events = [row for row in events if row.get("id") == app_event_id]
if len(matching_events) != 1:
    raise SystemExit(f"2017 women app projection: expected one event {app_event_id}, found {len(matching_events)}")
app_event = matching_events[0]
if app_event.get("event_type") != "study_committee" or app_event.get("year") != 2017:
    raise SystemExit("2017 women app projection: event type/year drift")
if app_event.get("source_ids") != [app_source_id]:
    raise SystemExit("2017 women app projection: event source linkage drift")
event_notes = app_event.get("notes", "")
for required_phrase in ("does not establish agreement", "individual positions require separate evidence"):
    if required_phrase not in event_notes:
        raise SystemExit(f"2017 women app projection: missing event guardrail phrase: {required_phrase}")

matching_sources = [row for row in sources if row.get("id") == app_source_id]
if len(matching_sources) != 1:
    raise SystemExit(f"2017 women app projection: expected one source {app_source_id}, found {len(matching_sources)}")
app_source = matching_sources[0]
if app_source.get("url") != report.get("metadata", {}).get("primary_source"):
    raise SystemExit("2017 women app projection: source URL must match normalized report primary source")
if app_source.get("source_type") != "primary_denominational_study_report":
    raise SystemExit("2017 women app projection: source type drift")

expected_app_edges = {
    row["normalized_person_id"]: row
    for row in edges
    if row.get("normalized_person_id") is not None
}
app_edges = [
    row for row in affiliations
    if row.get("target_type") == "event" and row.get("target_id") == app_event_id
]
if len(app_edges) != len(expected_app_edges):
    raise SystemExit(
        "2017 women app projection: every resolved normalized committee identity must have exactly one app edge; "
        f"expected {len(expected_app_edges)}, found {len(app_edges)}"
    )
if len({row.get("person_id") for row in app_edges}) != len(app_edges):
    raise SystemExit("2017 women app projection: duplicate person edge")

actual_app_ids = {row.get("person_id") for row in app_edges}
if actual_app_ids != set(expected_app_edges):
    raise SystemExit(
        "2017 women app projection: person ids must equal the resolved normalized identity set: "
        f"expected {sorted(expected_app_edges)}, found {sorted(actual_app_ids)}"
    )

for app_edge in app_edges:
    person_id = app_edge["person_id"]
    normalized_edge = expected_app_edges[person_id]
    if app_edge.get("role") != normalized_edge.get("role"):
        raise SystemExit(f"{person_id}: app role must match normalized committee role")
    if app_edge.get("confidence") != "confirmed":
        raise SystemExit(f"{person_id}: app committee service confidence drift")
    if app_edge.get("evidence_kind") != "study_committee_service":
        raise SystemExit(f"{person_id}: app evidence kind drift")
    if app_edge.get("weight") != 0 or app_edge.get("score_included") is not False:
        raise SystemExit(f"{person_id}: app committee service must remain unscored")
    if app_edge.get("source_ids") != [app_source_id]:
        raise SystemExit(f"{person_id}: app source linkage drift")
    notes = app_edge.get("notes", "")
    for required_phrase in ("Committee service only", "does not assign"):
        if required_phrase not in notes:
            raise SystemExit(f"{person_id}: missing app edge guardrail phrase: {required_phrase}")

print(
    "2017 women-serving canonical links OK: "
    f"{len(edges)} committee rows, {len(resolved)} resolved canonical identities, "
    f"{len(edges) - len(resolved)} explicitly unresolved identities, "
    f"{len(app_edges)} app-facing canonical edges"
)
