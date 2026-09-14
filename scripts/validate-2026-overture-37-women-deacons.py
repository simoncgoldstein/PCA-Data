#!/usr/bin/env python3
"""Validate 2026 Overture 37 women-deacons formal actions and Jeffrey Choi attribution boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
normalized_path = root / "sources/normalized/general-assembly/2026-overture-37-women-deacons-formal-actions.json"
people_path = root / "data/people.json"
events_path = root / "data/events.json"
affiliations_path = root / "data/affiliations.json"
sources_path = root / "data/sources.json"

data = json.loads(normalized_path.read_text(encoding="utf-8"))
people = json.loads(people_path.read_text(encoding="utf-8"))
events = json.loads(events_path.read_text(encoding="utf-8"))
affiliations = json.loads(affiliations_path.read_text(encoding="utf-8"))
sources = json.loads(sources_path.read_text(encoding="utf-8"))

people_by_id = {row["id"]: row for row in people}
events_by_id = {row["id"]: row for row in events}
affiliations_by_id = {row["id"]: row for row in affiliations}
sources_by_id = {row["id"]: row for row in sources}

meta = data.get("metadata", {})
if meta.get("dataset_id") != "2026_overture_37_women_deacons_formal_actions":
    raise SystemExit("O37 dataset id drift")
if meta.get("year") != 2026 or meta.get("assembly") != "53rd General Assembly":
    raise SystemExit("O37 year/assembly drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("O37 normalized metadata must remain ideologically unweighted")
modeling_rule = meta.get("modeling_rule", "")
for phrase in ("Pacific Presbytery", "formal submission", "does not establish Choi as the sole author"):
    if phrase not in modeling_rule:
        raise SystemExit(f"O37 attribution boundary missing: {phrase}")

overture = data["overture"]
if overture.get("overture_number") != 37 or overture.get("submitting_body") != "Pacific Presbytery":
    raise SystemExit("O37 formal submitting body/number drift")
if overture.get("title_as_published") != "Amend BCO 9-3 to Allow Women to Serve as Ordained Deacons":
    raise SystemExit("O37 published title drift")
if overture.get("formal_personal_authorship") != "not_established":
    raise SystemExit("O37 must not invent a named personal author")
if "does not name Jeffrey Choi as author or drafter" not in overture.get("important_boundary", ""):
    raise SystemExit("O37 personal-authorship guardrail missing")

assembly = data["assembly_action"]
if assembly.get("overtures_committee_recommendation") != "answer_in_the_negative":
    raise SystemExit("O37 committee recommendation drift")
if assembly.get("overtures_committee_vote") != {
    "for_negative_recommendation": 115,
    "against_negative_recommendation": 14,
    "abstain": 1,
}:
    raise SystemExit("O37 115-14-1 committee vote drift")
if "answered in the negative" not in assembly.get("general_assembly_outcome", ""):
    raise SystemExit("O37 Assembly outcome drift")

actions = {row["action_id"]: row for row in data.get("jeffrey_choi_actions", [])}
expected_actions = {
    "2026-o37-choi-public-advocacy",
    "2026-o37-choi-floor-speech",
    "2026-o37-choi-formal-dissent",
}
if set(actions) != expected_actions:
    raise SystemExit(f"O37 Choi action set drift: {sorted(actions)}")
for action in actions.values():
    if action.get("person_name") != "Jeffrey Choi" or action.get("normalized_person_id") != "jeffrey-choi":
        raise SystemExit("O37 Choi canonical identity linkage drift")
if "jeffrey-choi" not in people_by_id:
    raise SystemExit("O37 requires canonical person jeffrey-choi")

public_advocacy = actions["2026-o37-choi-public-advocacy"]
if public_advocacy.get("weight") != 0 or public_advocacy.get("score_included") is not False:
    raise SystemExit("O37 public advocacy must remain unscored")
floor = actions["2026-o37-choi-floor-speech"]
if floor.get("role") != "Floor speaker in support of Overture 37" or floor.get("confidence") != "strongly_supported":
    raise SystemExit("O37 Choi floor-speech attribution drift")
if floor.get("weight") != 0 or floor.get("score_included") is not False:
    raise SystemExit("O37 floor speech must remain unscored to avoid double-counting")
if "not sole authorship" not in floor.get("important_boundary", ""):
    raise SystemExit("O37 floor-speech authorship boundary missing")

dissent = actions["2026-o37-choi-formal-dissent"]
expected_authors = ["Aaron Baker", "Jeffrey Choi", "Walter Henegar", "Eric Kapur"]
if dissent.get("role") != "Co-author and submitter of formal dissent":
    raise SystemExit("O37 Choi dissent role drift")
if dissent.get("confidence") != "confirmed" or dissent.get("coauthors_as_printed") != expected_authors:
    raise SystemExit("O37 dissent author list/confidence drift")
if dissent.get("weight") != 3 or dissent.get("score_included") is not True:
    raise SystemExit("O37 formal dissent author should retain weight 3 and be score-included")

formal_dissent = data["formal_dissent"]
if formal_dissent.get("authors_as_printed") != expected_authors:
    raise SystemExit("O37 formal dissent author list drift")
if "does not by itself establish authorship of Overture 37" not in formal_dissent.get("important_boundary", ""):
    raise SystemExit("O37 dissent/overture authorship boundary missing")

# App-facing source records.
expected_sources = {
    "src-ga53-overture37-2026": (
        "https://pcaga.org/wp-content/uploads/2026/02/Overture-37_Pacific_9-3.pdf",
        "primary_denominational_overture",
    ),
    "src-ga53-overture37-dissent-2026": (
        "https://byfaithonline.com/wp-content/uploads/2026/09/Sufficiency_dissent_v3.pdf",
        "primary_denominational_dissent",
    ),
    "src-reformeddeacon-overture37-2026": (
        "https://reformeddeacon.com/blog/women-deacons-at-the-2026-pca-general-assembly/",
        "contemporaneous_secondary_report",
    ),
    "src-byfaith-overture37-dissent-response-2026": (
        "https://byfaithonline.com/general-assembly-responds-to-dissent-regarding-overture-37/",
        "denominational_news",
    ),
}
for source_id, (url, source_type) in expected_sources.items():
    source = sources_by_id.get(source_id)
    if source is None or source.get("url") != url or source.get("source_type") != source_type:
        raise SystemExit(f"O37 source record drift: {source_id}")

# App events preserve overture and dissent as distinct denominational actions.
overture_event = events_by_id.get("evt-overture37-women-deacons-2026")
dissent_event = events_by_id.get("evt-overture37-dissent-2026")
if overture_event is None or overture_event.get("event_type") != "general_assembly_overture":
    raise SystemExit("O37 app overture event missing or mistyped")
if dissent_event is None or dissent_event.get("event_type") != "general_assembly_dissent":
    raise SystemExit("O37 app dissent event missing or mistyped")
if "Pacific Presbytery formally submitted" not in overture_event.get("notes", ""):
    raise SystemExit("O37 app event must preserve formal presbytery sponsorship")
if "not as the formal sponsor or sole author" not in overture_event.get("notes", ""):
    raise SystemExit("O37 app event must preserve Choi authorship boundary")

floor_edge = affiliations_by_id.get("aff-choi-overture37-floor-2026")
dissent_edge = affiliations_by_id.get("aff-choi-overture37-dissent-2026")
if floor_edge is None or floor_edge.get("person_id") != "jeffrey-choi":
    raise SystemExit("O37 Choi app floor edge missing")
if floor_edge.get("target_id") != "evt-overture37-women-deacons-2026" or floor_edge.get("confidence") != "strongly_supported":
    raise SystemExit("O37 Choi app floor edge linkage/confidence drift")
if floor_edge.get("weight") != 0 or floor_edge.get("score_included") is not False:
    raise SystemExit("O37 app floor edge must remain unscored")
if dissent_edge is None or dissent_edge.get("person_id") != "jeffrey-choi":
    raise SystemExit("O37 Choi app dissent edge missing")
if dissent_edge.get("target_id") != "evt-overture37-dissent-2026" or dissent_edge.get("confidence") != "confirmed":
    raise SystemExit("O37 Choi app dissent edge linkage/confidence drift")
if dissent_edge.get("evidence_kind") != "formal_dissent_author" or dissent_edge.get("weight") != 3 or dissent_edge.get("score_included") is not True:
    raise SystemExit("O37 Choi app dissent evidence/scoring drift")

print("2026 Overture 37 OK: Pacific sponsorship preserved; Choi advocacy/floor speech and formal dissent modeled distinctly")
