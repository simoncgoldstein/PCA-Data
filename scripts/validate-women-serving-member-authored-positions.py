#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
path = root / "sources/normalized/general-assembly/2012-2019-women-serving-member-authored-positions.json"
people_path = root / "data/people.json"
committee_edges_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-person-edges.json"

data = json.loads(path.read_text(encoding="utf-8"))
people = json.loads(people_path.read_text(encoding="utf-8"))
committee_edges = json.loads(committee_edges_path.read_text(encoding="utf-8"))["edges"]

meta = data.get("metadata", {})
if meta.get("dataset_id") != "women_serving_member_authored_positions_2012_2019":
    raise SystemExit("women-serving authored positions: dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("women-serving authored positions: ideological_weight must remain 0")
for phrase in (
    "individually attributable",
    "Do not infer",
    "ordained office",
    "public worship speech",
    "local-session discretion",
):
    if phrase not in meta.get("modeling_rule", ""):
        raise SystemExit(f"women-serving authored positions: missing modeling guardrail {phrase!r}")
if "must not be read backward" not in meta.get("trajectory_rule", ""):
    raise SystemExit("women-serving authored positions: trajectory guardrail missing")

sources = data.get("sources", [])
source_by_id = {row.get("source_id"): row for row in sources}
expected_sources = {
    "choi-2017-wim-dissent",
    "keller-2012-jesus-justice-paul-excerpt",
    "keller-2012-jesus-justice-justice-excerpt",
    "castro-2019-1cor14-public-worship",
}
if set(source_by_id) != expected_sources:
    raise SystemExit(f"women-serving authored positions: source set drift: {sorted(source_by_id)}")

expected = {
    "choi-2017-local-session-diaconate-discretion": (
        "jeffrey-choi",
        "favor_local_session_discretion_due_exegetical_uncertainty",
    ),
    "choi-2017-phoebe-official-role": (
        "jeffrey-choi",
        "argue_phoebe_likely_held_recognized_official_church_role",
    ),
    "choi-2017-1tim3-diaconate-uncertainty": (
        "jeffrey-choi",
        "reject_confident_inclusion_or_exclusion_from_1timothy_3_alone",
    ),
    "keller-2012-authoritative-teaching-elder-restriction": (
        "kathy-keller",
        "restrict_authoritative_teaching_elder_role_to_men",
    ),
    "keller-2012-broad-women-public-ministry": (
        "kathy-keller",
        "favor_broad_women_public_ministry_outside_authoritative_elder_role",
    ),
    "keller-2012-gender-texts-transcultural": (
        "kathy-keller",
        "affirm_continuing_authority_of_1cor14_and_1tim2_gender_commands",
    ),
    "keller-2012-ordination-vs-marginalization-justice": (
        "kathy-keller",
        "reject_ordination_as_justice_claim_but_condemn_extrabiblical_marginalization",
    ),
    "castro-2019-public-worship-speaking-restriction": (
        "william-castro",
        "favor_traditional_restriction_on_women_individual_public_speech_in_ordinary_worship",
    ),
    "castro-2019-reject-judging-prophecies-solution": (
        "william-castro",
        "reject_judging_of_prophecies_only_interpretation_as_novel",
    ),
    "castro-2019-cultural-pressure-hermeneutics": (
        "william-castro",
        "warn_against_cultural_adaptation_driving_reinterpretation",
    ),
}

positions = data.get("positions", [])
by_id = {row.get("position_id"): row for row in positions}
if set(by_id) != set(expected):
    raise SystemExit(f"women-serving authored positions: position set drift: {sorted(by_id)}")

people_by_id = {row.get("id"): row for row in people}
for person_id, expected_name in {
    "jeffrey-choi": "Jeffrey Choi",
    "kathy-keller": "Kathy Keller",
    "william-castro": "William Castro",
}.items():
    person = people_by_id.get(person_id)
    if person is None or person.get("name") != expected_name:
        raise SystemExit(f"women-serving authored positions: canonical person missing/drifted: {person_id}")

for pid, (person_id, stance) in expected.items():
    row = by_id[pid]
    if row.get("normalized_person_id") != person_id:
        raise SystemExit(f"{pid}: canonical person linkage drift")
    if row.get("stance") != stance:
        raise SystemExit(f"{pid}: stance drift")
    if row.get("source_id") not in expected_sources:
        raise SystemExit(f"{pid}: source linkage drift")
    if row.get("ideological_weight") != 0:
        raise SystemExit(f"{pid}: ideological_weight must remain 0")
    if row.get("position_specificity") not in {"high", "very_high"}:
        raise SystemExit(f"{pid}: position specificity drift")
    if not row.get("summary") or len(row["summary"]) > 900:
        raise SystemExit(f"{pid}: summary missing or unexpectedly long")
    if not row.get("source_locators") or not row.get("important_boundary"):
        raise SystemExit(f"{pid}: evidence boundary missing")
    if "quote" in row:
        raise SystemExit(f"{pid}: normalized dataset must not reproduce source quotations")

# Choi: protect 2017 local-discretion evidence from being rewritten by the later 2026 action.
choi_local = by_id["choi-2017-local-session-diaconate-discretion"]
for phrase in ("local-session discretion", "not an unqualified 2017 endorsement", "2026"):
    if phrase not in choi_local["important_boundary"]:
        raise SystemExit(f"Choi 2017 trajectory boundary missing: {phrase}")
if "denomination-wide rule either including or excluding" not in choi_local["summary"]:
    raise SystemExit("Choi 2017 local-session summary drift")

# Keller: broad ministry permissions and male authoritative-teaching boundary must coexist.
keller_restriction = by_id["keller-2012-authoritative-teaching-elder-restriction"]
keller_broad = by_id["keller-2012-broad-women-public-ministry"]
if "authoritative teaching role" not in keller_restriction["summary"]:
    raise SystemExit("Keller authoritative-teaching boundary drift")
if "outside that authority" not in keller_broad["summary"]:
    raise SystemExit("Keller broad-ministry boundary drift")
if "women as elders" not in keller_broad["important_boundary"]:
    raise SystemExit("Keller eldership guardrail missing")

# Castro: preserve the distinction between individual official speech and congregational participation.
castro_worship = by_id["castro-2019-public-worship-speaking-restriction"]
if "congregational" not in castro_worship["important_boundary"]:
    raise SystemExit("Castro congregational-response boundary missing")
if "extraordinary" not in castro_worship["important_boundary"]:
    raise SystemExit("Castro extraordinary-case boundary missing")

# Committee service must remain a separate, zero-weight evidence type for these three people.
committee_by_person = {row.get("normalized_person_id"): row for row in committee_edges}
for person_id in ("jeffrey-choi", "kathy-keller", "william-castro"):
    edge = committee_by_person.get(person_id)
    if edge is None:
        raise SystemExit(f"{person_id}: 2017 committee edge missing")
    if edge.get("evidence_kind") != "study_committee_service":
        raise SystemExit(f"{person_id}: committee evidence-kind drift")
    if edge.get("weight") != 0 or edge.get("score_included") is not False:
        raise SystemExit(f"{person_id}: committee service must remain unscored")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "sources": len(sources),
    "positions": len(positions),
    "people": ["jeffrey-choi", "kathy-keller", "william-castro"],
    "ideological_weight": 0,
}, indent=2))
