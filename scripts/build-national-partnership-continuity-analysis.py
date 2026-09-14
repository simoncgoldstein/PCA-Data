#!/usr/bin/env python3
"""Build bounded National Partnership continuity/recurrence analysis.

This analysis is deliberately descriptive. It reports confirmed canonical overlap,
full-roster lower bounds, and exact-name screening ceilings. It does not treat the
absence of a confirmed NP identity as proof of non-membership and therefore does
not produce risk ratios, odds ratios, or causal/predictive-effect estimates.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


if len(sys.argv) not in (1, 2):
    raise SystemExit("usage: build-national-partnership-continuity-analysis.py [repo-root]")

ROOT = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
OVERLAP_DIR = ROOT / "analysis/overlap"
OUT = ROOT / "analysis/national-partnership"
OUT.mkdir(parents=True, exist_ok=True)
GENERATED_ON = "2026-09-14"
NP_DATASET = "national_partnership_confirmed_members"

TARGETS = [
    {
        "dataset": "warhurst_protest_2019",
        "label": "2019 Warhurst protest",
        "period": "2019",
        "temporal_relation": "within_np_archive_window",
        "evidence_scope": "formal_public_action",
    },
    {
        "dataset": "a_faithful_pca_2021-06-11",
        "label": "A Faithful PCA / Looking Forward – Together (June 2021)",
        "period": "2021-06-11",
        "temporal_relation": "within_np_archive_window",
        "evidence_scope": "public_coalition_action",
    },
    {
        "dataset": "overture_37_negative_votes_2021",
        "label": "2021 Overture 37 negative recorded votes",
        "period": "2021",
        "temporal_relation": "within_np_archive_window",
        "evidence_scope": "recorded_general_assembly_vote",
    },
    {
        "dataset": "a_faithful_pca_2022-03-14",
        "label": "A Faithful PCA cumulative signer snapshot (March 2022)",
        "period": "2022-03-14",
        "temporal_relation": "post_archive_snapshot_of_2021_action",
        "evidence_scope": "cumulative_public_statement_snapshot",
    },
    {
        "dataset": "overture_15_negative_votes_2022",
        "label": "2022 Overture 15 negative recorded votes",
        "period": "2022",
        "temporal_relation": "post_np_archive",
        "evidence_scope": "recorded_general_assembly_vote",
    },
    {
        "dataset": "nae_withdrawal_protest_2022",
        "label": "2022 NAE-withdrawal protest",
        "period": "2022",
        "temporal_relation": "post_np_archive",
        "evidence_scope": "formal_public_action",
    },
    {
        "dataset": "garris_letter_1",
        "label": "Garris Letter 1",
        "period": "2024",
        "temporal_relation": "post_np_archive",
        "evidence_scope": "public_coalition_action",
    },
    {
        "dataset": "garris_letter_2",
        "label": "Garris Letter 2",
        "period": "2024",
        "temporal_relation": "post_np_archive",
        "evidence_scope": "public_coalition_action",
    },
    {
        "dataset": "amr_leadership_current",
        "label": "Alliance for Mission & Renewal current leadership",
        "period": "2026",
        "temporal_relation": "post_np_archive",
        "evidence_scope": "current_network_leadership",
    },
]


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def pct(numerator: int, denominator: int) -> float:
    return round(100 * numerator / denominator, 2) if denominator else 0.0


def ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


with (OVERLAP_DIR / "pairwise-overlap.csv").open(newline="", encoding="utf-8") as handle:
    pairwise_rows = list(csv.DictReader(handle))

coverage = load_json("analysis/overlap/dataset-coverage.json")
coverage_by_dataset = {row["source_dataset"]: row for row in coverage["datasets"]}
shared_payload = load_json("analysis/overlap/pairwise-shared-people.json")
shared_by_pair = {
    frozenset((row["dataset_a"], row["dataset_b"])): row
    for row in shared_payload["pairs_with_confirmed_or_possible_overlap"]
}

if NP_DATASET not in coverage_by_dataset:
    raise SystemExit(f"missing NP dataset coverage: {NP_DATASET}")

np_coverage = coverage_by_dataset[NP_DATASET]
np_roster_count = int(np_coverage["unique_printed_name_count"])
np_confirmed_count = int(np_coverage["confirmed_canonical_person_count"])


def pair_for(left: str, right: str) -> dict[str, str]:
    for row in pairwise_rows:
        if {row["dataset_a"], row["dataset_b"]} == {left, right}:
            return row
    raise SystemExit(f"missing pairwise overlap row: {left} / {right}")


def side_counts(row: dict[str, str], dataset: str) -> tuple[int, int]:
    if row["dataset_a"] == dataset:
        return int(row["roster_a_unique_printed_names"]), int(row["confirmed_subset_a_count"])
    if row["dataset_b"] == dataset:
        return int(row["roster_b_unique_printed_names"]), int(row["confirmed_subset_b_count"])
    raise SystemExit(f"dataset {dataset} is not in pair row")


rows: list[dict[str, Any]] = []
for target in TARGETS:
    dataset = target["dataset"]
    if dataset not in coverage_by_dataset:
        raise SystemExit(f"missing target dataset coverage: {dataset}")

    pair = pair_for(NP_DATASET, dataset)
    target_roster_count, target_confirmed_count = side_counts(pair, dataset)
    pair_np_roster_count, pair_np_confirmed_count = side_counts(pair, NP_DATASET)
    if (pair_np_roster_count, pair_np_confirmed_count) != (np_roster_count, np_confirmed_count):
        raise SystemExit(f"NP denominator drift in pair: {dataset}")

    confirmed_overlap = int(pair["confirmed_intersection_count"])
    possible_same_name = int(pair["unresolved_possible_overlap_count"])
    screening_overlap = confirmed_overlap + possible_same_name
    shared = shared_by_pair.get(frozenset((NP_DATASET, dataset)), {})
    shared_people = shared.get("confirmed_shared_people", [])

    rows.append({
        **target,
        "np_printed_roster_count": np_roster_count,
        "np_confirmed_canonical_count": np_confirmed_count,
        "np_identity_resolution_rate_pct": pct(np_confirmed_count, np_roster_count),
        "target_printed_roster_count": target_roster_count,
        "target_confirmed_canonical_count": target_confirmed_count,
        "target_identity_resolution_rate_pct": pct(target_confirmed_count, target_roster_count),
        "confirmed_overlap_count": confirmed_overlap,
        "unresolved_exact_name_possible_overlap_count": possible_same_name,
        "confirmed_np_share_of_target_confirmed_pct": pct(confirmed_overlap, target_confirmed_count),
        "confirmed_target_share_of_np_confirmed_pct": pct(confirmed_overlap, np_confirmed_count),
        "confirmed_lower_bound_share_of_target_printed_roster_pct": pct(confirmed_overlap, target_roster_count),
        "confirmed_lower_bound_share_of_np_printed_roster_pct": pct(confirmed_overlap, np_roster_count),
        "same_name_screening_ceiling_share_of_target_printed_roster_pct": pct(screening_overlap, target_roster_count),
        "same_name_screening_ceiling_share_of_np_printed_roster_pct": pct(screening_overlap, np_roster_count),
        "confirmed_shared_people": [
            {"canonical_person_id": person["canonical_person_id"], "name": person["name"]}
            for person in shared_people
        ],
    })

# These rankings are descriptive only. NP identity canonicalization is incomplete and
# likely non-random because recurring people are easier to resolve.
strongest_target_share = max(rows, key=lambda row: row["confirmed_np_share_of_target_confirmed_pct"])
strongest_np_recurrence = max(rows, key=lambda row: row["confirmed_target_share_of_np_confirmed_pct"])
amr_row = next(row for row in rows if row["dataset"] == "amr_leadership_current")
garris1_row = next(row for row in rows if row["dataset"] == "garris_letter_1")
afp2021_row = next(row for row in rows if row["dataset"] == "a_faithful_pca_2021-06-11")

summary = {
    "metadata": {
        "generated_on": GENERATED_ON,
        "analysis_id": "national_partnership_continuity_2026-09-14",
        "source_dataset": NP_DATASET,
        "source_inputs": [
            "analysis/overlap/dataset-coverage.json",
            "analysis/overlap/pairwise-overlap.csv",
            "analysis/overlap/pairwise-shared-people.json",
        ],
        "analysis_rule": (
            "Descriptive continuity/recurrence analysis only. Confirmed overlap uses shared canonical person IDs. "
            "Full-roster lower bounds divide confirmed overlap by printed-roster denominators. Same-name screening "
            "ceilings add unresolved exact normalized-name overlaps and are not confirmed identity matches."
        ),
    },
    "national_partnership_cohort": {
        "printed_confirmed_member_name_count": np_roster_count,
        "confirmed_canonical_person_count": np_confirmed_count,
        "identity_resolution_rate_pct": pct(np_confirmed_count, np_roster_count),
        "coverage_warning": (
            "The canonical NP subset is incomplete and is not assumed to be a random sample of the full confirmed "
            "printed-name membership roster. Recurring people may be easier to identity-resolve, which can inflate "
            "recurrence percentages calculated only within the canonical subset."
        ),
    },
    "headline_descriptive_signals": {
        "amr_personnel_continuity": {
            "confirmed_np_overlap": amr_row["confirmed_overlap_count"],
            "amr_confirmed_leaders": amr_row["target_confirmed_canonical_count"],
            "confirmed_np_share_of_amr_leadership_pct": amr_row["confirmed_np_share_of_target_confirmed_pct"],
            "shared_people": amr_row["confirmed_shared_people"],
            "boundary": (
                "This is strong personnel-continuity evidence. It does not by itself establish that AMR is a legal, "
                "organizational, or formal successor to the National Partnership."
            ),
        },
        "a_faithful_pca_recurrence": {
            "confirmed_overlap": afp2021_row["confirmed_overlap_count"],
            "canonical_np_denominator": np_confirmed_count,
            "pct_of_canonical_np_subset": afp2021_row["confirmed_target_share_of_np_confirmed_pct"],
            "full_np_roster_lower_bound_pct": afp2021_row["confirmed_lower_bound_share_of_np_printed_roster_pct"],
            "boundary": "The canonical-subset percentage is descriptive and potentially resolution-biased; use the full-roster lower bound for a conservative population statement.",
        },
        "garris_letter_1_recurrence": {
            "confirmed_overlap": garris1_row["confirmed_overlap_count"],
            "garris1_confirmed_people": garris1_row["target_confirmed_canonical_count"],
            "confirmed_np_share_of_resolved_garris1_pct": garris1_row["confirmed_np_share_of_target_confirmed_pct"],
            "garris1_full_roster_lower_bound_pct": garris1_row["confirmed_lower_bound_share_of_target_printed_roster_pct"],
            "boundary": "Letter 1 identity resolution is incomplete, so the resolved-signer percentage is not treated as a full-roster estimate.",
        },
        "strongest_target_share_among_tracked_rows": {
            "dataset": strongest_target_share["dataset"],
            "pct": strongest_target_share["confirmed_np_share_of_target_confirmed_pct"],
            "boundary": "Ranking is among the selected tracked datasets only and is not a population ranking.",
        },
        "strongest_recurrence_of_canonical_np_subset": {
            "dataset": strongest_np_recurrence["dataset"],
            "pct": strongest_np_recurrence["confirmed_target_share_of_np_confirmed_pct"],
            "boundary": "This ranking inherits the incomplete/non-random NP identity-resolution limitation.",
        },
    },
    "predictive_validity_readiness": {
        "status": "not_ready_for_risk_ratio_odds_ratio_or_causal_claim",
        "reasons": [
            "Only part of the 151-name confirmed NP membership roster is canonically resolved, and resolution is plausibly recurrence-biased.",
            "Absence of a confirmed NP canonical identity is not proof that a tracked person was not an NP member.",
            "Most later datasets are selected action rosters, not complete opportunity denominators for the relevant PCA population.",
            "Several tracked actions occur inside the 2013-2021 NP archive window, so they are recurrence evidence rather than strictly prospective outcomes.",
            "The tracked actions are correlated with one another; they are not independent repeated trials.",
        ],
        "required_before_x_times_predictive_claim": [
            "Resolve or otherwise bound NP identity status for people in the selected comparison/action universe, prioritizing exact-name possible overlaps.",
            "Define an opportunity-aware comparison cohort whose members could reasonably have taken each action.",
            "Separate within-archive recurrence from post-archive outcomes.",
            "Predefine how repeated/correlated public actions will be grouped so one coalition episode is not counted as many independent outcomes.",
        ],
        "absence_semantics": "No confirmed NP link in the current graph means 'not established in the current canonical data,' not 'confirmed non-member.'",
        "forbidden_shortcut": "Do not calculate an NP-vs-non-NP risk ratio by treating every person without a canonical NP edge as a non-member.",
    },
    "tracked_dataset_count": len(rows),
    "tracked_datasets": rows,
}

(OUT / "continuity-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

csv_fields = [
    "dataset",
    "label",
    "period",
    "temporal_relation",
    "evidence_scope",
    "np_printed_roster_count",
    "np_confirmed_canonical_count",
    "np_identity_resolution_rate_pct",
    "target_printed_roster_count",
    "target_confirmed_canonical_count",
    "target_identity_resolution_rate_pct",
    "confirmed_overlap_count",
    "unresolved_exact_name_possible_overlap_count",
    "confirmed_np_share_of_target_confirmed_pct",
    "confirmed_target_share_of_np_confirmed_pct",
    "confirmed_lower_bound_share_of_target_printed_roster_pct",
    "confirmed_lower_bound_share_of_np_printed_roster_pct",
    "same_name_screening_ceiling_share_of_target_printed_roster_pct",
    "same_name_screening_ceiling_share_of_np_printed_roster_pct",
]
with (OUT / "action-overlap.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=csv_fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row[field] for field in csv_fields})

print(json.dumps({
    "analysis": summary["metadata"]["analysis_id"],
    "np_roster_names": np_roster_count,
    "np_canonical_people": np_confirmed_count,
    "np_resolution_rate_pct": pct(np_confirmed_count, np_roster_count),
    "tracked_datasets": len(rows),
    "amr_np_overlap": amr_row["confirmed_overlap_count"],
    "amr_leaders": amr_row["target_confirmed_canonical_count"],
    "predictive_validity_status": summary["predictive_validity_readiness"]["status"],
}, indent=2))
