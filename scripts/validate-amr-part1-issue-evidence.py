#!/usr/bin/env python3
"""Validate bounded AMR 2026 overtures roundtable Part 1 issue-position evidence."""

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-overtures-roundtable-part1-issue-positions.json"
data = json.loads(path.read_text(encoding="utf-8"))
meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_overtures_roundtable_part1_issue_positions":
    raise SystemExit("AMR Part 1 issue evidence: dataset_id drift")
if meta.get("source_family") != "amr_2026_overtures_roundtable_part1":
    raise SystemExit("AMR Part 1 issue evidence: source_family drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("AMR Part 1 issue evidence: ideological_weight must remain 0")
if "Panel participation" not in meta.get("modeling_rule", ""):
    raise SystemExit("AMR Part 1 issue evidence: panel-participation guardrail missing")
source = data.get("source", {})
if source.get("video_id") != "xezEYJN8aiM":
    raise SystemExit("AMR Part 1 issue evidence: source video drift")
if not (root / source.get("caption_path", "")).exists():
    raise SystemExit("AMR Part 1 issue evidence: archived caption missing")
expected = {
    "amr-2026-o7-howie-donahoe": ("Howie Donahoe", "2026 Overture 7", "favor"),
    "amr-2026-o27-howie-donahoe": ("Howie Donahoe", "2026 Westminster Overture 27 as stated in the video", "oppose_as_written_support_if_materially_amended"),
    "amr-2026-o50-david-coffin": ("David Coffin", "2026 Overture 50", "favorable"),
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"AMR Part 1 issue evidence: position set drift: {sorted(by_id)}")
for position_id, (person, overture, stance) in expected.items():
    row = by_id[position_id]
    if (row.get("person_name_as_stated"), row.get("overture"), row.get("stance")) != (person, overture, stance):
        raise SystemExit(f"{position_id}: person/overture/stance drift")
    if row.get("evidence_class") != "direct_first_person_issue_statement":
        raise SystemExit(f"{position_id}: evidence class drift")
    if row.get("ideological_weight") != 0 or row.get("normalized_person_id") is not None:
        raise SystemExit(f"{position_id}: weighting/identity boundary drift")
    if not row.get("source_locators") or not row.get("speaker_attribution_basis") or not row.get("important_boundary"):
        raise SystemExit(f"{position_id}: locator/attribution/boundary missing")
    if len(row.get("summary", "")) > 700 or "quote" in row:
        raise SystemExit(f"{position_id}: transcript-reproduction boundary violated")
print(json.dumps({"dataset": meta["dataset_id"], "positions": len(positions), "ideological_weight": 0}, indent=2))
