#!/usr/bin/env python3
"""Validate high-specificity formal denominational position evidence."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
report_path = root / "sources/normalized/general-assembly/2017-women-serving-ministry-report.json"
index_path = root / "sources/normalized/general-assembly/formal-position-evidence-index.json"
receipt_path = root / "sources/raw/issues/women-serving-ministry/mcgreevy-video-transcript-receipt-2026-09-04.json"
batch1_path = root / "sources/normalized/general-assembly/2008-2009-women-formal-position-records.json"

report = json.loads(report_path.read_text(encoding="utf-8"))
index = json.loads(index_path.read_text(encoding="utf-8"))
receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
batch1 = json.loads(batch1_path.read_text(encoding="utf-8"))

meta = report["metadata"]
if meta.get("report_form") != "committee consensus report":
    raise SystemExit("2017 women report: report form drift")
if meta.get("consensus_wording_as_printed") != "overwhelming consensus":
    raise SystemExit("2017 women report: consensus wording drift")
if meta.get("minority_report_in_published_final_report") is not False:
    raise SystemExit("2017 women report: do not invent a published minority report")
if meta.get("ideological_weight") != 0:
    raise SystemExit("2017 women report: committee/report evidence must remain ideological_weight 0")

members = report.get("committee_members", [])
if len(members) != 12:
    raise SystemExit(f"2017 women report: expected 12 listed committee members, found {len(members)}")
counts = Counter(row.get("committee_status") for row in members)
if counts != {"Voting Member": 7, "Advisory Member": 5}:
    raise SystemExit(f"2017 women report: committee status counts drift: {dict(counts)}")
if not any(row.get("name") == "Mary Beth McGreevy" and row.get("committee_status") == "Voting Member" for row in members):
    raise SystemExit("2017 women report: Mary Beth McGreevy voting-member record missing")

positions = {row.get("position_id"): row for row in report.get("report_level_positions", [])}
required_report_positions = {
    "male-only-eldership",
    "no-bco-change-recommended",
    "two-schools-women-teaching-men",
    "public-worship-prayer-and-scripture-suggestions",
}
if set(positions) != required_report_positions:
    raise SystemExit(f"2017 women report: report-level position set drift: {sorted(positions)}")
if "do not assign either school" not in positions["two-schools-women-teaching-men"].get("scope", ""):
    raise SystemExit("2017 women report: internal teaching-view ambiguity guardrail missing")

first_person = report.get("first_person_position_evidence", [])
if len(first_person) != 1:
    raise SystemExit("2017 women report: expected exactly one normalized first-person statement")
mcgreevy = first_person[0]
if mcgreevy.get("person_name") != "Mary Beth McGreevy":
    raise SystemExit("McGreevy evidence: speaker drift")
if mcgreevy.get("source_url") != "https://www.youtube.com/watch?v=KzjCJIitP9A":
    raise SystemExit("McGreevy evidence: source URL drift")
if mcgreevy.get("user_supplied_transcript_sha256") != "9b55b81f355a6ecc22140eaf7f973cece41b2db50f150cbee04a656e6f9b0eb1":
    raise SystemExit("McGreevy evidence: transcript hash drift")
if mcgreevy.get("user_supplied_transcript_line_count") != 857:
    raise SystemExit("McGreevy evidence: transcript line-count drift")
if mcgreevy.get("ideological_weight") != 0:
    raise SystemExit("McGreevy evidence: first-person evidence must remain ideological_weight 0")
required_topics = {
    "complementarianism_and_headship",
    "support_for_2017_report_direction",
    "authoritative_pulpit_and_sacraments",
    "teaching_and_mixed_groups",
    "paid_ministry_roles",
    "session_meeting_consultation",
}
actual_topics = {row.get("topic") for row in mcgreevy.get("positions", [])}
if actual_topics != required_topics:
    raise SystemExit(f"McGreevy evidence: position-topic set drift: {sorted(actual_topics)}")

if receipt.get("transcript_sha256") != mcgreevy.get("user_supplied_transcript_sha256"):
    raise SystemExit("McGreevy evidence: raw receipt / normalized hash mismatch")
if receipt.get("transcript_line_count") != mcgreevy.get("user_supplied_transcript_line_count"):
    raise SystemExit("McGreevy evidence: raw receipt / normalized line-count mismatch")
if receipt.get("full_transcript_committed") is not False:
    raise SystemExit("McGreevy evidence: full third-party transcript should not be committed")

# 2008-2009 formal-position batch.
if batch1.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("2008-2009 women batch: metadata ideological_weight must remain 0")
events = {row.get("event_id"): row for row in batch1.get("events", [])}
expected_event_counts = {
    "2008-overture-9-deaconess-study-minority-report": 27,
    "2008-rpr-women-scripture-reading-minority-report": 8,
    "2009-overture-10-women-roles-study-minority-report": 34,
}
if set(events) != set(expected_event_counts):
    raise SystemExit(f"2008-2009 women batch: event set drift: {sorted(events)}")
for event_id, expected_signers in expected_event_counts.items():
    event = events[event_id]
    if event.get("evidence_class") != "signed_formal_report_or_minority_report":
        raise SystemExit(f"{event_id}: evidence class drift")
    if event.get("ideological_weight") != 0:
        raise SystemExit(f"{event_id}: ideological_weight must remain 0")
    signers = event.get("signers", [])
    if event.get("signer_count") != expected_signers or len(signers) != expected_signers:
        raise SystemExit(f"{event_id}: expected {expected_signers} signers, found {len(signers)}")
    printed = [row.get("name_as_printed") for row in signers]
    if any(not value for value in printed) or len(printed) != len(set(printed)):
        raise SystemExit(f"{event_id}: signer names must be nonblank and unique within event")

if "wide variety of positions and practices" not in events["2008-overture-9-deaconess-study-minority-report"].get("important_boundary", ""):
    raise SystemExit("2008 Overture 9: do not turn study-committee signership into a female-ordination claim")
if events["2008-overture-9-deaconess-study-minority-report"].get("named_presenter", {}).get("name") != "Bryan Chapell":
    raise SystemExit("2008 Overture 9: Bryan Chapell presenter record missing")

worship = events["2008-rpr-women-scripture-reading-minority-report"]
required_worship_signers = {
    "TE K. Hugh Acton", "RE Gene Friedline", "TE John Carroll", "RE David Marshall",
    "TE Lane Keister", "RE David O'Steen", "TE Bob Peterson", "TE Richard Wheeler",
}
if {row.get("name_as_printed") for row in worship.get("signers", [])} != required_worship_signers:
    raise SystemExit("2008 RPR worship minority: signer set drift")
if "reading Scripture or exhorting" not in worship.get("position_summary", ""):
    raise SystemExit("2008 RPR worship minority: position summary drift")

women2009 = events["2009-overture-10-women-roles-study-minority-report"]
if women2009.get("assembly_outcome") != "Minority report defeated 427-446; Recommendation 8 answering Overture 10 in the negative was adopted.":
    raise SystemExit("2009 Overture 10: aggregate Assembly outcome drift")
if women2009.get("named_presenter", {}).get("name") != "David Coffin":
    raise SystemExit("2009 Overture 10: David Coffin presenter record missing")
if women2009.get("named_floor_supporter", {}).get("name") != "E. J. Nusbaum":
    raise SystemExit("2009 Overture 10: E. J. Nusbaum floor-support record missing")

hierarchy = {row.get("evidence_class"): row for row in index.get("evidence_hierarchy", [])}
for required in (
    "signed_formal_report_or_minority_report",
    "recorded_vote_or_formal_protest_signature",
    "first_person_issue_statement",
    "study_committee_consensus_participation",
    "committee_membership_only",
    "conference_or_network_participation",
):
    if required not in hierarchy:
        raise SystemExit(f"formal position index: missing evidence class {required}")

indexed = {row.get("evidence_id"): row for row in index.get("normalized_position_sources", [])}
for required in (
    "2008-overture-9-deaconess-study-minority-report",
    "2008-rpr-women-scripture-reading-minority-report",
    "2009-overture-10-women-roles-study-minority-report",
    "2017-women-serving-ministry-consensus-report",
    "2017-mary-beth-mcgreevy-first-person-women-ministry",
    "2019-2021-human-sexuality-aic",
    "2021-overture-37-minority-report",
    "2022-overture-15-minority-report",
    "2022-overture-15-recorded-negative-votes",
):
    if required not in indexed:
        raise SystemExit(f"formal position index: missing normalized source {required}")
    path = root / indexed[required]["path"]
    if not path.exists():
        raise SystemExit(f"formal position index: referenced path does not exist: {path}")

if index.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("formal position index: evidence framework must remain ideological_weight 0")
if "Aggregate votes are event-level evidence" not in index.get("metadata", {}).get("modeling_rule", ""):
    raise SystemExit("formal position index: aggregate-vote guardrail missing")

print(json.dumps({
    "committee_members": len(members),
    "committee_status_counts": dict(counts),
    "report_positions": len(positions),
    "mcgreevy_position_topics": len(actual_topics),
    "batch1_events": len(events),
    "batch1_signers": sum(len(row.get("signers", [])) for row in events.values()),
    "indexed_position_sources": len(indexed),
}, indent=2))
