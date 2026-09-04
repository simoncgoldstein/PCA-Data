#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/national-partnership/organizing-actions-and-member-recommendations-v1.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "national_partnership_organizing_actions_v1":
    raise SystemExit("NP organizing actions: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("NP organizing actions: ideological_weight must remain 0")
if "individual member recommendations" not in meta.get("modeling_rule", ""):
    raise SystemExit("NP organizing actions: scope boundary missing")

records = data.get("records", [])
expected = {
    "np-2015-2016-racial-reconciliation-organizing": "np_organizing_action",
    "np-2016-women-ministry-study-committee-organizing": "np_organizing_action",
    "np-2019-unordained-board-agency-voting-goal": "individual_member_recommendation_presented_as_assembly_goal",
    "np-2019-nashville-study-committee-recommendation": "individual_member_recommendation",
    "np-2019-nae-withdrawal-organizing-goal": "np_organizing_action",
    "np-2014-mercy-community-transformation-seminar": "np_recommended_programming",
}
by_id = {row.get("record_id"): row for row in records}
if set(by_id) != set(expected):
    raise SystemExit(f"NP organizing actions: record set drift: {sorted(by_id)}")

for record_id, scope in expected.items():
    row = by_id[record_id]
    if row.get("evidence_scope") != scope:
        raise SystemExit(f"{record_id}: evidence scope drift")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{record_id}: ideological_weight must remain 0")
    if not row.get("source_pages"):
        raise SystemExit(f"{record_id}: source pages missing")
    if not row.get("important_boundary"):
        raise SystemExit(f"{record_id}: boundary missing")
    if len(row.get("summary", "")) > 1000:
        raise SystemExit(f"{record_id}: summary unexpectedly long")

if "not proof of unanimous NP agreement" not in by_id["np-2019-unordained-board-agency-voting-goal"]["important_boundary"]:
    raise SystemExit("NP organizing actions: individual-goal boundary drift")
if "not modeled as unanimous NP agreement" not in by_id["np-2019-nashville-study-committee-recommendation"]["important_boundary"]:
    raise SystemExit("NP organizing actions: Kessler recommendation boundary drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "records": len(records),
    "np_organizing_actions": sum(1 for row in records if row.get("evidence_scope") == "np_organizing_action"),
    "individual_member_records": sum(1 for row in records if row.get("evidence_scope", "").startswith("individual_member")),
    "ideological_weight": 0,
}, indent=2))
