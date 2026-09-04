#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-alex-dean-women-ministry.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_alex_dean_women_ministry":
    raise SystemExit("Alex Dean AMR evidence: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("Alex Dean AMR evidence: ideological_weight must remain 0")
if "non-ordained" not in meta.get("modeling_rule", ""):
    raise SystemExit("Alex Dean AMR evidence: ordained/non-ordained boundary missing")

source = data.get("source", {})
if source.get("author_as_printed") != "Alex Dean":
    raise SystemExit("Alex Dean AMR evidence: author drift")
if source.get("title") != "A Vision for Women in Ministry in the PCA—Recalling the 2017 Ad Interim Report":
    raise SystemExit("Alex Dean AMR evidence: title drift")

expected = {
    "amr-2026-alex-dean-2017-report": "strongly_affirm",
    "amr-2026-alex-dean-lay-worship-leadership": "favor_nonordained_men_and_women_leading_selected_worship_elements",
    "amr-2026-alex-dean-nonordained-deaconess": "favor_nonordained_public_diaconal_role_for_women",
    "amr-2026-alex-dean-womens-leadership-team": "favor_nonordained_women_leadership_roles",
    "amr-2026-alex-dean-catholicity-freedom": "favor_broad_tent_local_freedom_within_confessional_bounds",
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"Alex Dean AMR evidence: position set drift: {sorted(by_id)}")

for pid, stance in expected.items():
    row = by_id[pid]
    if row.get("person_name_as_stated") != "Alex Dean":
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
    if "quote" in row:
        raise SystemExit(f"{pid}: normalized data should not reproduce article quotes")

# Protect the key distinction in this source: support for public/non-ordained roles is not ordination.
if "non-ordained" not in by_id["amr-2026-alex-dean-nonordained-deaconess"]["important_boundary"]:
    raise SystemExit("Alex Dean AMR evidence: deaconess ordination boundary drift")
if "not elders" not in by_id["amr-2026-alex-dean-womens-leadership-team"]["summary"]:
    raise SystemExit("Alex Dean AMR evidence: Women's Leadership Team eldership boundary drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "positions": len(positions),
    "author": source["author_as_printed"],
    "ideological_weight": 0,
}, indent=2))
