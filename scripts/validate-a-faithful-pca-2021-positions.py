#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/public-statements/a-faithful-pca/looking-forward-together-2021-positions.json"
data = json.loads(path.read_text(encoding="utf-8"))

meta = data.get("metadata", {})
if meta.get("dataset_id") != "a_faithful_pca_looking_forward_together_2021_positions":
    raise SystemExit("A Faithful PCA positions: dataset_id drift")
if meta.get("evidence_scope") != "signed_public_statement":
    raise SystemExit("A Faithful PCA positions: evidence scope drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("A Faithful PCA positions: ideological_weight must remain 0")
if "not automatically" not in meta.get("modeling_rule", ""):
    raise SystemExit("A Faithful PCA positions: coalition scope boundary missing")

expected = {
    "afpca-2021-confessional-good-faith-subscription": "affirm_good_faith_system_subscription",
    "afpca-2021-worship-contextual-latitude": "affirm_contextual_worship_variation_within_scripture_and_polity",
    "afpca-2021-sexual-ethics-and-celibate-ssa": "affirm_traditional_sexual_ethics_and_purity_for_ministry",
    "afpca-2021-racial-refugee-women-mercy-priorities": "affirm_biblical_attention_to_racial_reconciliation_refugee_care_women_and_mercy",
    "afpca-2021-trust-church-courts-over-online-accusation": "favor_personal_and_ecclesiastical_process_over_unproven_online_accusation",
    "afpca-2021-unity-mission-and-nonextreme-rhetoric": "favor_confessional_unity_charitable_dialogue_and_missional_cooperation",
}
positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"A Faithful PCA positions: position set drift: {sorted(by_id)}")

for pid, stance in expected.items():
    row = by_id[pid]
    if row.get("stance") != stance:
        raise SystemExit(f"{pid}: stance drift")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{pid}: ideological_weight must remain 0")
    if not row.get("source_locators") or not row.get("important_boundary"):
        raise SystemExit(f"{pid}: evidence boundary missing")
    if len(row.get("summary", "")) > 1000:
        raise SystemExit(f"{pid}: summary unexpectedly long")

if "same-sex attraction" not in by_id["afpca-2021-sexual-ethics-and-celibate-ssa"]["summary"]:
    raise SystemExit("A Faithful PCA positions: attraction/practice distinction drift")
if "Good Faith Subscription" not in by_id["afpca-2021-confessional-good-faith-subscription"]["summary"]:
    raise SystemExit("A Faithful PCA positions: subscription summary drift")
if "sessions, presbyteries, and judicial processes" not in by_id["afpca-2021-trust-church-courts-over-online-accusation"]["summary"]:
    raise SystemExit("A Faithful PCA positions: polity-process boundary drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "positions": len(positions),
    "scope": meta["evidence_scope"],
    "ideological_weight": 0,
}, indent=2))
