#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-chuck-colson-lords-supper-distribution.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_chuck_colson_lords_supper_distribution":
    raise SystemExit("Colson Lord's Supper evidence: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("Colson Lord's Supper evidence: ideological_weight must remain 0")
if "administration/consecration" not in meta.get("modeling_rule", ""):
    raise SystemExit("Colson Lord's Supper evidence: administration/distribution boundary missing")

source = data.get("source", {})
if source.get("author_as_printed") != "Chuck Colson":
    raise SystemExit("Colson Lord's Supper evidence: author drift")

expected = {
    "amr-2026-colson-serving-passing-distinction": "oppose_restriction_based_on_serving_passing_distinction",
    "amr-2026-colson-minister-administers-people-distribute": "affirm_ordained_administration_with_distribution_by_communicants",
    "amr-2026-colson-distribution-not-keys": "reject_necessary_connection_between_distribution_details_and_keys",
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"Colson Lord's Supper evidence: position set drift: {sorted(by_id)}")

for pid, stance in expected.items():
    row = by_id[pid]
    if row.get("person_name_as_stated") != "Chuck Colson":
        raise SystemExit(f"{pid}: person drift")
    if row.get("stance") != stance:
        raise SystemExit(f"{pid}: stance drift")
    if row.get("evidence_class") != "direct_authored_issue_statement":
        raise SystemExit(f"{pid}: evidence class drift")
    if row.get("normalized_person_id") is not None:
        raise SystemExit(f"{pid}: identity must remain independent of this evidence pass")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{pid}: ideological_weight must remain 0")
    if not row.get("source_locators") or not row.get("important_boundary"):
        raise SystemExit(f"{pid}: evidence boundary missing")
    if len(row.get("summary", "")) > 900:
        raise SystemExit(f"{pid}: summary unexpectedly long")

admin = by_id["amr-2026-colson-minister-administers-people-distribute"]
if "presiding ordained minister" not in admin["summary"] or "communicants" not in admin["summary"]:
    raise SystemExit("Colson Lord's Supper evidence: minister/communicant distinction drift")
if "not lay consecration" not in admin["important_boundary"]:
    raise SystemExit("Colson Lord's Supper evidence: consecration boundary drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "positions": len(positions),
    "author": source["author_as_printed"],
    "ideological_weight": 0,
}, indent=2))
