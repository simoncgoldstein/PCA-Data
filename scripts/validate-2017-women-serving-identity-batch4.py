#!/usr/bin/env python3
"""Validate final reviewed identities and complete canonicalization of the 2017 Women Serving committee."""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
receipt_path = root / "sources/raw/identity/2017-women-serving-identity-evidence-batch4-2026-09-14.json"
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
app_by_id = {row["id"]: row for row in affiliations}

expected = {
    "2017-women-serving-committee-02": {
        "name": "William Castro",
        "person_id": "william-castro",
        "role": "Advisory Member",
        "ordination": "Teaching Elder",
        "app_id": "aff-castro-women-serving-2017",
    },
    "2017-women-serving-committee-07": {
        "name": "Lani Jones",
        "person_id": "lani-jones",
        "role": "Advisory Member",
        "ordination": None,
        "app_id": "aff-jones-women-serving-2017",
    },
}
receipt_relative = "sources/raw/identity/2017-women-serving-identity-evidence-batch4-2026-09-14.json"

if receipt.get("status") != "canonical_seed_applied" or receipt.get("resolution_applied") is not True:
    raise SystemExit("batch 4 receipt must record an applied canonical seed decision")
if receipt.get("ideological_weight") != 0:
    raise SystemExit("batch 4 identity evidence must remain ideologically unweighted")
modeling_rule = receipt.get("modeling_rule", "")
for phrase in ("person-identity reconciliation only", "do not assign", "Person-specific theological evidence"):
    if phrase not in modeling_rule:
        raise SystemExit(f"batch 4 receipt missing modeling guardrail: {phrase}")

records = receipt.get("records", [])
if len(records) != 2 or {row.get("committee_edge_id") for row in records} != set(expected):
    raise SystemExit("batch 4 receipt must contain exactly the Castro and Jones identity decisions")

for record in records:
    edge_id = record["committee_edge_id"]
    exp = expected[edge_id]
    name = exp["name"]
    person_id = exp["person_id"]
    edge = edge_by_id[edge_id]
    member = report_by_name[name]
    person = people_by_id.get(person_id)
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
    if member.get("normalized_person_id") != person_id or edge.get("normalized_person_id") != person_id:
        raise SystemExit(f"{edge_id}: normalized canonical id mismatch")
    if edge.get("identity_status") != "resolved_reviewed_canonical_person":
        raise SystemExit(f"{edge_id}: reviewed identity status drift")
    if edge.get("identity_review_status") != "canonical_seed_applied" or edge.get("identity_review_receipt") != receipt_relative:
        raise SystemExit(f"{edge_id}: review provenance drift")
    if edge.get("proposed_canonical_person_id") != person_id:
        raise SystemExit(f"{edge_id}: proposed canonical id drift")
    if edge.get("role") != exp["role"] or edge.get("weight") != 0 or edge.get("score_included") is not False:
        raise SystemExit(f"{edge_id}: committee-service role/scoring drift")

    if app is None or app.get("person_id") != person_id or app.get("role") != exp["role"]:
        raise SystemExit(f"{edge_id}: app-facing committee affiliation missing or mismatched")
    if app.get("target_id") != "evt-women-serving-study-committee-2017" or app.get("target_type") != "event":
        raise SystemExit(f"{edge_id}: app event linkage drift")
    if app.get("evidence_kind") != "study_committee_service" or app.get("weight") != 0 or app.get("score_included") is not False:
        raise SystemExit(f"{edge_id}: app committee-service evidence/scoring drift")

# This final identity batch completes the official 12-member roster.
if len(edges) != 12 or any(row.get("normalized_person_id") is None for row in edges):
    raise SystemExit("2017 women-serving committee must now have all 12 identities canonically resolved")
if len({row.get("normalized_person_id") for row in edges}) != 12:
    raise SystemExit("2017 women-serving committee canonical IDs must be unique across all 12 members")

app_committee_edges = [
    row for row in affiliations
    if row.get("target_type") == "event" and row.get("target_id") == "evt-women-serving-study-committee-2017"
]
if len(app_committee_edges) != 12 or len({row.get("person_id") for row in app_committee_edges}) != 12:
    raise SystemExit("all 12 resolved committee identities must have exactly one app-facing committee edge")

print("2017 women-serving identity batch 4 OK: Castro and Jones applied; all 12 committee identities resolved")
