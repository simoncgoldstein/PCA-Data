#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/amr/2026-organizational-theological-vision.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "amr_2026_organizational_theological_vision":
    raise SystemExit("AMR organizational vision: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("AMR organizational vision: ideological_weight must remain 0")
if "not inferred positions of every AMR member" not in meta.get("modeling_rule", ""):
    raise SystemExit("AMR organizational vision: organization/member boundary missing")

sources = {row.get("source_id"): row for row in data.get("sources", [])}
expected_sources = {
    "amr-board-confessional-missional-center-2026-04-14",
    "amr-board-theological-vision-2026-04-29",
}
if set(sources) != expected_sources:
    raise SystemExit("AMR organizational vision: source set drift")
if any(row.get("author_as_printed") != "The Board of AMR" for row in sources.values()):
    raise SystemExit("AMR organizational vision: board attribution drift")

expected = {
    "amr-org-2026-biblical-authority": "affirm_inerrant_scripture_and_oppose_extra_biblical_constraints",
    "amr-org-2026-reformed-subscription": "affirm_system_subscription_between_substance_and_strict_subscription",
    "amr-org-2026-presbyterian-process": "affirm_constitutional_presbyterian_process_and_oppose_mob_adjudication",
    "amr-org-2026-elders-and-whole-body-ministry": "affirm_male_eldership_and_gifts_of_all_members",
    "amr-org-2026-regulated-adapted-worship": "affirm_regulated_worship_with_contextual_adaptation_and_scriptural_freedom",
    "amr-org-2026-confessional-missional-big-tent": "favor_confessional_missional_big_tent_and_resist_unnecessary_narrowing",
    "amr-org-2026-political-tribalism-christian-nationalism": "critical_of_political_tribalism_and_forms_of_christian_nationalism",
    "amr-org-2026-women-minorities-trust-concerns": "call_for_attention_to_women_and_minority_concerns_and_rebuilding_trust",
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"AMR organizational vision: position set drift: {sorted(by_id)}")

for pid, stance in expected.items():
    row = by_id[pid]
    if row.get("organization_id") != "amr":
        raise SystemExit(f"{pid}: organization drift")
    if row.get("stance") != stance:
        raise SystemExit(f"{pid}: stance drift")
    if row.get("evidence_class") != "direct_organizational_board_statement":
        raise SystemExit(f"{pid}: evidence class drift")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{pid}: ideological_weight must remain 0")
    if not row.get("source_ids") or any(src not in expected_sources for src in row["source_ids"]):
        raise SystemExit(f"{pid}: source linkage drift")
    if not row.get("source_locators") or not row.get("important_boundary"):
        raise SystemExit(f"{pid}: evidence boundary missing")
    if len(row.get("summary", "")) > 1000:
        raise SystemExit(f"{pid}: summary unexpectedly long")

elders = by_id["amr-org-2026-elders-and-whole-body-ministry"]["summary"]
if "godly men" not in elders or "all members" not in elders:
    raise SystemExit("AMR organizational vision: elders/ministry boundary drift")
worship = by_id["amr-org-2026-regulated-adapted-worship"]["summary"]
if "Word, sacrament, and prayer" not in worship or "officer authority" not in worship:
    raise SystemExit("AMR organizational vision: worship boundary drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "sources": len(sources),
    "positions": len(positions),
    "organization": meta["organization"],
    "ideological_weight": 0,
}, indent=2))
