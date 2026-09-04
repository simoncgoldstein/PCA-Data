#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-katie-polski-women-ministry.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_katie_polski_women_ministry":
    raise SystemExit("Katie Polski AMR evidence: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("Katie Polski AMR evidence: ideological_weight must remain 0")
if "male-only ordained elder and deacon offices" not in meta.get("modeling_rule", ""):
    raise SystemExit("Katie Polski AMR evidence: office boundary missing")

source = data.get("source", {})
if source.get("author_as_printed") != "Katie Polski":
    raise SystemExit("Katie Polski AMR evidence: author drift")
if source.get("url") != "https://a4mr.org/1770-2/":
    raise SystemExit("Katie Polski AMR evidence: source URL drift")

expected = {
    "amr-2026-katie-polski-male-ordained-offices": "affirm_male_only_ordained_elder_and_deacon_offices",
    "amr-2026-katie-polski-gift-based-ministry": "affirm_expansive_nonordained_ministry_by_women",
    "amr-2026-katie-polski-worship-and-formation": "favor_women_in_worship_planning_music_leadership_and_formation",
    "amr-2026-katie-polski-visible-leadership-pathways": "favor_visible_training_and_service_pathways_for_women",
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"Katie Polski AMR evidence: position set drift: {sorted(by_id)}")

for pid, stance in expected.items():
    row = by_id[pid]
    if row.get("person_name_as_stated") != "Katie Polski":
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

male_office = by_id["amr-2026-katie-polski-male-ordained-offices"]["summary"]
if "elder and deacon" not in male_office or "qualified men" not in male_office:
    raise SystemExit("Katie Polski AMR evidence: male-office affirmation drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "positions": len(positions),
    "author": source["author_as_printed"],
    "ideological_weight": 0,
}, indent=2))
