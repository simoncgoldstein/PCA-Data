#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-kyle-wells-women-ministry.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_kyle_wells_women_ministry":
    raise SystemExit("Kyle Wells AMR evidence: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("Kyle Wells AMR evidence: ideological_weight must remain 0")
if "male governing office" not in meta.get("modeling_rule", ""):
    raise SystemExit("Kyle Wells AMR evidence: office boundary missing")

source = data.get("source", {})
if source.get("author_as_printed") != "Kyle Wells":
    raise SystemExit("Kyle Wells AMR evidence: author drift")

expected = {
    "amr-2026-kyle-wells-male-governing-office": "affirm_male_governing_office",
    "amr-2026-kyle-wells-women-public-prayer-instruction": "affirm_public_instructional_ministry_by_women_outside_elder_authority",
    "amr-2026-kyle-wells-women-authority-leadership": "affirm_real_nonelder_authority_and_leadership_by_women",
    "amr-2026-kyle-wells-structured-womens-diaconal-service": "affirm_structured_recognized_diaconal_service_by_women",
    "amr-2026-kyle-wells-public-recognition-womens-ministry": "favor_visible_public_recognition_of_womens_ministry",
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"Kyle Wells AMR evidence: position set drift: {sorted(by_id)}")

for pid, stance in expected.items():
    row = by_id[pid]
    if row.get("person_name_as_stated") != "Kyle Wells":
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

male_office_summary = by_id["amr-2026-kyle-wells-male-governing-office"]["summary"]
if "qualified men" not in male_office_summary or "governing office" not in male_office_summary:
    raise SystemExit("Kyle Wells AMR evidence: male-office affirmation drift")
if "does not" not in by_id["amr-2026-kyle-wells-structured-womens-diaconal-service"]["important_boundary"]:
    raise SystemExit("Kyle Wells AMR evidence: diaconal-status boundary drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "positions": len(positions),
    "author": source["author_as_printed"],
    "ideological_weight": 0,
}, indent=2))
