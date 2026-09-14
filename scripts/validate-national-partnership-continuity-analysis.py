#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SUMMARY_PATH = ROOT / "analysis/national-partnership/continuity-summary.json"
CSV_PATH = ROOT / "analysis/national-partnership/action-overlap.csv"

summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
with CSV_PATH.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

expected_datasets = {
    "warhurst_protest_2019",
    "a_faithful_pca_2021-06-11",
    "overture_37_negative_votes_2021",
    "a_faithful_pca_2022-03-14",
    "overture_15_negative_votes_2022",
    "nae_withdrawal_protest_2022",
    "garris_letter_1",
    "garris_letter_2",
    "amr_leadership_current",
}

metadata = summary.get("metadata", {})
if metadata.get("analysis_id") != "national_partnership_continuity_2026-09-14":
    raise SystemExit("unexpected NP continuity analysis id")
if metadata.get("source_dataset") != "national_partnership_confirmed_members":
    raise SystemExit("unexpected NP continuity source dataset")

cohort = summary.get("national_partnership_cohort", {})
if cohort.get("printed_confirmed_member_name_count") != 151:
    raise SystemExit("NP printed confirmed-member roster drift")
canonical_count = cohort.get("confirmed_canonical_person_count")
if not isinstance(canonical_count, int) or not (0 < canonical_count <= 151):
    raise SystemExit("invalid NP canonical-person count")
if cohort.get("identity_resolution_rate_pct") != round(100 * canonical_count / 151, 2):
    raise SystemExit("NP identity-resolution rate mismatch")
if "not assumed to be a random sample" not in cohort.get("coverage_warning", ""):
    raise SystemExit("missing NP non-random-resolution warning")

readiness = summary.get("predictive_validity_readiness", {})
if readiness.get("status") != "not_ready_for_risk_ratio_odds_ratio_or_causal_claim":
    raise SystemExit("predictive-validity readiness boundary drift")
if "confirmed non-member" not in readiness.get("absence_semantics", ""):
    raise SystemExit("missing NP absence-semantics guardrail")
if "Do not calculate an NP-vs-non-NP risk ratio" not in readiness.get("forbidden_shortcut", ""):
    raise SystemExit("missing NP comparison-cohort guardrail")
if len(readiness.get("reasons", [])) < 5:
    raise SystemExit("predictive-validity limitations are incomplete")
if len(readiness.get("required_before_x_times_predictive_claim", [])) < 4:
    raise SystemExit("predictive-validity next requirements are incomplete")

if summary.get("tracked_dataset_count") != len(expected_datasets):
    raise SystemExit("tracked dataset count drift")
summary_rows = summary.get("tracked_datasets", [])
if {row.get("dataset") for row in summary_rows} != expected_datasets:
    raise SystemExit("tracked dataset set drift in summary")
if {row.get("dataset") for row in rows} != expected_datasets:
    raise SystemExit("tracked dataset set drift in CSV")


def walk_keys(value: Any):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from walk_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk_keys(item)


for forbidden_key in {"risk_ratio", "odds_ratio", "causal_effect", "non_np_count"}:
    if forbidden_key in set(walk_keys(summary)):
        raise SystemExit(f"forbidden premature metric present: {forbidden_key}")

summary_by_dataset = {row["dataset"]: row for row in summary_rows}
for dataset, row in summary_by_dataset.items():
    target_roster = row["target_printed_roster_count"]
    target_confirmed = row["target_confirmed_canonical_count"]
    overlap = row["confirmed_overlap_count"]
    possible = row["unresolved_exact_name_possible_overlap_count"]
    if target_roster <= 0 or target_confirmed < 0 or target_confirmed > target_roster:
        raise SystemExit(f"invalid target coverage: {dataset}")
    if overlap < 0 or overlap > min(canonical_count, target_confirmed):
        raise SystemExit(f"invalid confirmed overlap: {dataset}")
    if possible < 0:
        raise SystemExit(f"invalid possible overlap: {dataset}")
    if len(row.get("confirmed_shared_people", [])) != overlap:
        raise SystemExit(f"shared-person list/count mismatch: {dataset}")
    if row["same_name_screening_ceiling_share_of_target_printed_roster_pct"] < row["confirmed_lower_bound_share_of_target_printed_roster_pct"]:
        raise SystemExit(f"screening ceiling below confirmed lower bound: {dataset}")

amr = summary_by_dataset["amr_leadership_current"]
if amr["target_printed_roster_count"] != 6 or amr["target_confirmed_canonical_count"] != 6:
    raise SystemExit("AMR current-leadership snapshot denominator drift")
if amr["confirmed_overlap_count"] < 4:
    raise SystemExit("known NP/AMR personnel continuity regressed")

if summary_by_dataset["garris_letter_1"]["target_printed_roster_count"] != 60:
    raise SystemExit("Garris Letter 1 roster drift")
if summary_by_dataset["garris_letter_2"]["target_printed_roster_count"] != 21:
    raise SystemExit("Garris Letter 2 roster drift")
if summary_by_dataset["a_faithful_pca_2021-06-11"]["confirmed_overlap_count"] < 35:
    raise SystemExit("known NP / A Faithful PCA confirmed overlap regressed")

headline = summary.get("headline_descriptive_signals", {})
if "does not by itself establish" not in headline.get("amr_personnel_continuity", {}).get("boundary", ""):
    raise SystemExit("AMR organizational-succession guardrail missing")

print(json.dumps({
    "status": "ok",
    "np_printed_members": 151,
    "np_canonical_people": canonical_count,
    "tracked_datasets": len(expected_datasets),
    "amr_confirmed_np_overlap": amr["confirmed_overlap_count"],
    "predictive_validity": readiness["status"],
}, indent=2))
