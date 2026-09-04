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

report = json.loads(report_path.read_text(encoding="utf-8"))
index = json.loads(index_path.read_text(encoding="utf-8"))
receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

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

print(json.dumps({
    "committee_members": len(members),
    "committee_status_counts": dict(counts),
    "report_positions": len(positions),
    "mcgreevy_position_topics": len(actual_topics),
    "indexed_position_sources": len(indexed),
}, indent=2))
