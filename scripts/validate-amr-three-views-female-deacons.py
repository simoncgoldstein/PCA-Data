#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-three-views-female-deacons.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_three_views_female_deacons":
    raise SystemExit("AMR three views: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("AMR three views: ideological_weight must remain 0")
if "multiple views" not in meta.get("modeling_rule", ""):
    raise SystemExit("AMR three views: multi-view guardrail missing")

package = data.get("package_source", {})
if package.get("title") != "Three Views on Female Deacons":
    raise SystemExit("AMR three views: package title drift")
if package.get("authors_as_printed") != ["Geoff Ziegler", "Jared Nelson", "Jeffrey Choi"]:
    raise SystemExit("AMR three views: package author list drift")

expected = {
    "amr-2026-female-deacons-jared-nelson": ("Jared Nelson", "oppose_women_in_ordained_diaconate"),
    "amr-2026-female-deacons-jeffrey-choi": ("Jeffrey Choi", "favor_allowing_women_deacons_under_local_discretion"),
    "amr-2026-female-deacons-geoff-ziegler": ("Geoff Ziegler", "oppose_overture_37_now_while_treating_women_deacons_as_permissible_view"),
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"AMR three views: position set drift: {sorted(by_id)}")

for pid, (person, stance) in expected.items():
    row = by_id[pid]
    if row.get("person_name_as_stated") != person:
        raise SystemExit(f"{pid}: person drift")
    if row.get("stance") != stance:
        raise SystemExit(f"{pid}: stance drift")
    if row.get("evidence_class") != "direct_authored_issue_statement":
        raise SystemExit(f"{pid}: evidence class drift")
    if row.get("position_specificity") != "very_high":
        raise SystemExit(f"{pid}: specificity drift")
    if row.get("related_overture") != "2026 Overture 37":
        raise SystemExit(f"{pid}: overture drift")
    if row.get("normalized_person_id") is not None:
        raise SystemExit(f"{pid}: identity must remain independent of this evidence pass")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{pid}: ideological_weight must remain 0")
    if not row.get("source_url", "").startswith("https://a4mr.substack.com/"):
        raise SystemExit(f"{pid}: source URL drift")
    if not row.get("source_locators") or not row.get("important_boundary"):
        raise SystemExit(f"{pid}: evidence boundary missing")
    if len(row.get("summary", "")) > 900:
        raise SystemExit(f"{pid}: summary unexpectedly long")
    if "quote" in row:
        raise SystemExit(f"{pid}: normalized data should not reproduce article quotes")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "positions": len(positions),
    "authors": sorted(row["person_name_as_stated"] for row in positions),
    "ideological_weight": 0,
}, indent=2))
