#!/usr/bin/env python3
"""Validate applied identity evidence for 2017 Women Serving committee batch 2."""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
receipt_path = root / "sources/raw/identity/2017-women-serving-identity-evidence-batch2-2026-09-14.json"
report_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-report.json"
edges_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-person-edges.json"
people_path = root / "data/people.json"
affiliations_path = root / "data/affiliations.json"

receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
report = json.loads(report_path.read_text(encoding="utf-8"))
edges = json.loads(edges_path.read_text(encoding="utf-8"))["edges"]
people = json.loads(people_path.read_text(encoding="utf-8"))
affiliations = json.loads(affiliations_path.read_text(encoding="utf-8"))

people_by_id = {row["id"]: row for row in people}
report_by_name = {row["name"]: row for row in report["committee_members"]}
edge_by_id = {row["edge_id"]: row for row in edges}

expected = {
    "2017-women-serving-committee-01": {
        "name": "Leon Brown",
        "person_id": "leon-brown",
        "role": "Advisory Member",
        "ordination": "Teaching Elder",
        "app_id": "aff-brown-women-serving-2017",
    },
    "2017-women-serving-committee-09": {
        "name": "Mary Beth McGreevy",
        "person_id": "mary-beth-mcgreevy",
        "role": "Voting Member",
        "ordination": None,
        "app_id": "aff-mcgreevy-women-serving-2017",
    },
    "2017-women-serving-committee-11": {
        "name": "Harry Reeder",
        "person_id": "harry-reeder",
        "role": "Voting Member",
        "ordination": "Teaching Elder",
        "app_id": "aff-reeder-women-serving-2017",
    },
}
receipt_relative = "sources/raw/identity/2017-women-serving-identity-evidence-batch2-2026-09-14.json"

if receipt.get("status") != "canonical_seed_applied" or receipt.get("resolution_applied") is not True:
    raise SystemExit("batch 2 receipt must record an applied canonical identity decision")
if receipt.get("applied_on") != "2026-09-14":
    raise SystemExit("batch 2 receipt applied date drift")
if receipt.get("ideological_weight") != 0:
    raise SystemExit("batch 2 identity evidence must remain ideologically unweighted")
modeling_rule = receipt.get("modeling_rule", "")
for phrase in ("person-identity reconciliation only", "do not assign", "broader ideological label"):
    if phrase not in modeling_rule:
        raise SystemExit(f"batch 2 receipt missing modeling guardrail: {phrase}")

records = receipt.get("records", [])
if {row.get("committee_edge_id") for row in records} != set(expected):
    raise SystemExit("batch 2 receipt edge set drift")
if len(records) != len(expected):
    raise SystemExit("batch 2 receipt must contain exactly three reviewed identities")

app_by_id = {row["id"]: row for row in affiliations}
for record in records:
    edge_id = record["committee_edge_id"]
    exp = expected[edge_id]
    name = exp["name"]
    person_id = exp["person_id"]
    edge = edge_by_id[edge_id]
    person = people_by_id.get(person_id)
    member = report_by_name[name]
    app = app_by_id.get(exp["app_id"])

    if record.get("person_name") != name:
        raise SystemExit(f"{edge_id}: receipt name drift")
    if record.get("proposed_canonical_person_id") != person_id or record.get("current_normalized_person_id") != person_id:
        raise SystemExit(f"{edge_id}: receipt canonical id drift")
    if record.get("review_status") != "canonical_seed_applied" or record.get("confidence") != "high":
        raise SystemExit(f"{edge_id}: receipt status/confidence drift")
    if len(record.get("evidence", [])) < 3:
        raise SystemExit(f"{edge_id}: expected at least three identity evidence records")
    if "Identity only" not in record.get("reasoning_boundary", ""):
        raise SystemExit(f"{edge_id}: identity-only reasoning boundary missing")

    if person is None or person.get("name") != name:
        raise SystemExit(f"{edge_id}: canonical person missing or name mismatch")
    if person.get("ordination") != exp["ordination"] or person.get("profile_status") != "seeded":
        raise SystemExit(f"{edge_id}: canonical seed metadata drift")

    if member.get("normalized_person_id") != person_id:
        raise SystemExit(f"{edge_id}: normalized report id mismatch")
    if edge.get("normalized_person_id") != person_id:
        raise SystemExit(f"{edge_id}: normalized edge id mismatch")
    if edge.get("identity_status") != "resolved_reviewed_canonical_person":
        raise SystemExit(f"{edge_id}: reviewed identity status drift")
    if edge.get("identity_review_status") != "canonical_seed_applied":
        raise SystemExit(f"{edge_id}: applied review status drift")
    if edge.get("identity_review_receipt") != receipt_relative:
        raise SystemExit(f"{edge_id}: receipt linkage drift")
    if edge.get("proposed_canonical_person_id") != person_id:
        raise SystemExit(f"{edge_id}: proposed canonical id drift")
    if edge.get("role") != exp["role"] or edge.get("weight") != 0 or edge.get("score_included") is not False:
        raise SystemExit(f"{edge_id}: committee-service role/scoring drift")

    if app is None:
        raise SystemExit(f"{edge_id}: app-facing affiliation missing")
    if app.get("person_id") != person_id or app.get("role") != exp["role"]:
        raise SystemExit(f"{edge_id}: app-facing identity/role mismatch")
    if app.get("target_id") != "evt-women-serving-study-committee-2017" or app.get("target_type") != "event":
        raise SystemExit(f"{edge_id}: app-facing event linkage drift")
    if app.get("evidence_kind") != "study_committee_service" or app.get("confidence") != "confirmed":
        raise SystemExit(f"{edge_id}: app-facing evidence metadata drift")
    if app.get("weight") != 0 or app.get("score_included") is not False:
        raise SystemExit(f"{edge_id}: app-facing committee service must remain unscored")
    if app.get("source_ids") != ["src-ga45-women-serving-2017"]:
        raise SystemExit(f"{edge_id}: app-facing source linkage drift")
    notes = app.get("notes", "")
    if "Committee service only" not in notes or "does not assign" not in notes:
        raise SystemExit(f"{edge_id}: app-facing guardrail text missing")

mcgreevy_evidence = [
    row for row in report.get("first_person_position_evidence", [])
    if row.get("person_name") == "Mary Beth McGreevy"
]
if len(mcgreevy_evidence) != 1 or mcgreevy_evidence[0].get("normalized_person_id") != "mary-beth-mcgreevy":
    raise SystemExit("Mary Beth McGreevy first-person evidence must link to her canonical identity")
if mcgreevy_evidence[0].get("ideological_weight") != 0:
    raise SystemExit("Mary Beth McGreevy first-person evidence must remain unscored")

remaining_unresolved = {
    row["person_name"] for row in edges if row.get("normalized_person_id") is None
}
if {exp["name"] for exp in expected.values()} & remaining_unresolved:
    raise SystemExit("batch 2 identities must remain resolved in all later slices")

print(
    "2017 women-serving identity batch 2 OK: "
    f"3 reviewed identities remain applied; {len(remaining_unresolved)} committee identities currently unresolved"
)
