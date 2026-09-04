#!/usr/bin/env python3
"""Validate bounded, speaker-specific AMR issue-position evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-overtures-roundtable-issue-positions.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_overtures_roundtable_issue_positions":
    raise SystemExit("AMR issue evidence: dataset_id drift")
if meta.get("source_family") != "amr_2026_overtures_roundtable_part2":
    raise SystemExit("AMR issue evidence: source_family drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("AMR issue evidence: ideological_weight must remain 0")
if "Panel participation" not in meta.get("modeling_rule", ""):
    raise SystemExit("AMR issue evidence: panel-participation guardrail missing")

source = data.get("source", {})
if source.get("video_id") != "JpsstSfx40U":
    raise SystemExit("AMR issue evidence: source video drift")
caption_path = root / source.get("caption_path", "")
if not caption_path.exists():
    raise SystemExit(f"AMR issue evidence: archived caption missing: {caption_path}")
if source.get("participants_as_stated") != [
    "Derek Radney", "Steve Tipton", "David Coffin", "Howie Donahoe"
]:
    raise SystemExit("AMR issue evidence: participant metadata drift")

positions = data.get("positions", [])
expected = {
    "amr-2026-o37-steve-tipton": ("Steve Tipton", "2026 Overture 37", "oppose"),
    "amr-2026-o37-david-coffin": ("David Coffin", "2026 Overture 37", "oppose"),
    "amr-2026-o37-howie-donahoe": ("Howie Donahoe", "2026 Overture 37", "oppose"),
    "amr-2026-o61-howie-donahoe-danvers": ("Howie Donahoe", "2026 Overture 61", "critical_of_proposed_declaration"),
}
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"AMR issue evidence: position set drift: {sorted(by_id)}")

for position_id, (person, overture, stance) in expected.items():
    row = by_id[position_id]
    if row.get("person_name_as_stated") != person:
        raise SystemExit(f"{position_id}: person drift")
    if row.get("overture") != overture or row.get("stance") != stance:
        raise SystemExit(f"{position_id}: overture/stance drift")
    if row.get("evidence_class") != "direct_first_person_issue_statement":
        raise SystemExit(f"{position_id}: evidence class drift")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{position_id}: ideological_weight must remain 0")
    if row.get("normalized_person_id") is not None:
        raise SystemExit(f"{position_id}: identity must remain independent of this evidence pass")
    locators = row.get("source_locators", [])
    if len(locators) < 1 or any(not locator.startswith("00:") for locator in locators):
        raise SystemExit(f"{position_id}: timestamp locators missing or malformed")
    if not row.get("speaker_attribution_basis") or not row.get("important_boundary"):
        raise SystemExit(f"{position_id}: attribution/boundary guardrail missing")
    if len(row.get("summary", "")) > 700:
        raise SystemExit(f"{position_id}: normalized summary unexpectedly long")
    if "quote" in row:
        raise SystemExit(f"{position_id}: normalized data should not reproduce transcript quotes")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "source_video": source["video_id"],
    "positions": len(positions),
    "speakers": sorted({row["person_name_as_stated"] for row in positions}),
    "ideological_weight": 0,
}, indent=2))
