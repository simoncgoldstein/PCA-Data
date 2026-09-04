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
wim_path = root / "sources/normalized/general-assembly/2001-2002-women-military-formal-position-records.json"
wim = json.loads(wim_path.read_text(encoding="utf-8"))
women2016_path = root / "sources/normalized/general-assembly/2016-women-study-committee-formal-actions.json"
women2016 = json.loads(women2016_path.read_text(encoding="utf-8"))
batch2_chronology_path = root / "sources/normalized/general-assembly/2019-2023-sexuality-formal-position-chronology.json"
aic_path = root / "sources/normalized/general-assembly/2019-2021-human-sexuality-aic.json"
o37_votes_path = root / "sources/normalized/general-assembly/2021-overture-37-negative-votes.json"
o15_votes_path = root / "sources/normalized/revoice/overture-15-negative-votes-2022.json"
formal_roles_path = root / "sources/normalized/general-assembly/2021-2022-sexuality-named-formal-roles.json"
batch2_chronology = json.loads(batch2_chronology_path.read_text(encoding="utf-8"))
aic = json.loads(aic_path.read_text(encoding="utf-8"))
o37_votes = json.loads(o37_votes_path.read_text(encoding="utf-8"))
o15_votes = json.loads(o15_votes_path.read_text(encoding="utf-8"))
formal_roles = json.loads(formal_roles_path.read_text(encoding="utf-8"))

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

# Batch 2: Human Sexuality / O37 / O15.
if len(aic.get("members", [])) != 7 or aic.get("member_count") != 7:
    raise SystemExit("Human Sexuality AIC: expected 7 members")
if aic.get("collective_position_count") != 12 or len(aic.get("collective_report_positions", [])) != 12:
    raise SystemExit("Human Sexuality AIC: expected 12 collective positions")
if aic.get("metadata", {}).get("formal_recommendations") is not False:
    raise SystemExit("Human Sexuality AIC: report must remain recorded as having no formal recommendations")
if aic.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("Human Sexuality AIC: ideological_weight must remain 0")

if o37_votes.get("metadata", {}).get("parsed_rows") != 207 or len(o37_votes.get("negative_votes", [])) != 207:
    raise SystemExit("Overture 37: expected 207 official recorded negative votes")
if "1349-443" not in o37_votes.get("metadata", {}).get("procedural_vote_guardrail", ""):
    raise SystemExit("Overture 37: close-debate vote guardrail missing")
if o37_votes.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("Overture 37 votes: ideological_weight must remain 0")

if o15_votes.get("metadata", {}).get("parsed_rows") != 200 or len(o15_votes.get("negative_votes", [])) != 200:
    raise SystemExit("Overture 15: expected corrected total of 200 recorded negative votes")
danny = [r for r in o15_votes.get("negative_votes", []) if r.get("name_as_printed") == "Danny Morgan"]
if len(danny) != 1 or danny[0].get("presbytery_as_printed") != "South Coast":
    raise SystemExit("Overture 15: 51st GA Danny Morgan correction missing")

chron = {e.get("event_id"): e for e in batch2_chronology.get("events", [])}
if chron["2021-overture-37-overtures-committee-majority"].get("committee_vote") != {"for": 82, "against": 43, "abstain": 1}:
    raise SystemExit("Overture 37: committee vote drift")
if chron["2021-overture-37-assembly-action"].get("minority_substitute_vote") != {"for": 617, "against": 1209}:
    raise SystemExit("Overture 37: minority substitute vote drift")
if chron["2021-overture-37-assembly-action"].get("final_affirmative_vote") != {"for": 1130, "against": 692}:
    raise SystemExit("Overture 37: final adoption tally drift")
if chron["2022-overture-29-overtures-committee-and-ga"].get("assembly_vote") != {"for": 1922, "against": 200}:
    raise SystemExit("Overture 29: Assembly vote drift")
if chron["2022-overture-15-overtures-committee-majority"].get("committee_vote") != {"for": 80, "against": 47}:
    raise SystemExit("Overture 15: committee majority vote drift")
if chron["2022-overture-15-assembly-action"].get("minority_becomes_main_motion_vote") != {"for": 1094, "against": 1044}:
    raise SystemExit("Overture 15: minority-becomes-main-motion tally drift")
if chron["2022-overture-15-assembly-action"].get("final_affirmative_vote") != {"for": 1167, "against": 978}:
    raise SystemExit("Overture 15: final adoption tally drift")
lifecycle = chron["2023-overture-15-presbytery-disposition"]
if lifecycle.get("official_corrected_presbytery_tally") != {"for": 48, "against": 32}:
    raise SystemExit("Overture 15: corrected presbytery tally must be 48-32")
if lifecycle.get("number_reporting") != 80 or lifecycle.get("two_thirds_approval_threshold") != 59:
    raise SystemExit("Overture 15: corrected presbytery reporting/threshold drift")
if lifecycle.get("superseded_50th_ga_printed_tally") != {"for": 39, "against": 29, "number_reporting": 68}:
    raise SystemExit("Overture 15: superseded 50th GA tally guardrail missing")

roles_by_name = {r.get("name_as_printed"): r for r in formal_roles.get("roles", [])}
for name, role in {"Trevor Laurence":"principal_author_and_presenter", "Derek Radney":"substantial_editorial_contributor", "Matthew D. Fender":"minority_report_presenter", "Joe Cristman":"drafting_committee_member"}.items():
    if roles_by_name.get(name, {}).get("role") != role:
        raise SystemExit(f"formal roles: missing {name} / {role}")
if formal_roles.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("formal roles: ideological_weight must remain 0")

# 2016 women-serving study-committee formal actions.
if women2016.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("2016 women formal actions: ideological_weight must remain 0")
proc2016 = women2016.get("procedural_point_of_order_registration", {})
if proc2016.get("registered_commissioner_count") != 173 or len(proc2016.get("commissioners", [])) != 173:
    raise SystemExit("2016 women procedural registration: expected 173 named commissioners")
if proc2016.get("evidence_class") != "recorded_procedural_position":
    raise SystemExit("2016 women procedural registration: evidence class drift")
if "procedural registration only" not in proc2016.get("important_boundary", ""):
    raise SystemExit("2016 women procedural registration: merits guardrail missing")
if proc2016.get("commissioners", [])[70].get("name_as_printed") != "David T. Irving" or proc2016.get("commissioners", [])[70].get("office_as_printed") is not None:
    raise SystemExit("2016 women procedural registration: preserve David T. Irving office omission as printed")
protest2016 = women2016.get("pipa_protest_against_study_committee", {})
if protest2016.get("added_signer_count") != 28 or len(protest2016.get("added_signers", [])) != 28:
    raise SystemExit("2016 Pipa protest: expected exactly 28 commissioners explicitly listed as adding names")
if protest2016.get("author_presenter", {}).get("name_as_printed") != "Joseph Pipa":
    raise SystemExit("2016 Pipa protest: Joseph Pipa author/presenter record missing")
if any(r.get("name_as_printed") == "Joseph Pipa" for r in protest2016.get("added_signers", [])):
    raise SystemExit("2016 Pipa protest: do not collapse author/presenter into the 28-name added-signers list")
if women2016.get("assembly_disposition", {}).get("permanent_committee_recommendation_to_form_study_committee") != {"for": 767, "against": 375, "abstain": 12}:
    raise SystemExit("2016 women study committee: final Assembly tally drift")

# 2001-2002 Women in the Military report family.
if wim.get("metadata", {}).get("ideological_weight") != 0:
    raise SystemExit("Women in the Military: ideological_weight must remain 0")
committee = wim.get("committee_roster", {})
if committee.get("member_count") != 10 or len(committee.get("members", [])) != 10:
    raise SystemExit("Women in the Military: expected complete 10-member committee roster")
committee_names = {r.get("name_as_printed") for r in committee.get("members", [])}
if committee_names != {"Stephen Leonard", "Stephen Clark", "Ron Swafford", "Beryl Hubbard", "Bentley Rayburn", "Peter Lillback", "Tim Bayly", "Charlie Morrison", "Keith Stoeber", "Don Weyburn"}:
    raise SystemExit("Women in the Military: committee roster drift")
positions = {e.get("event_id"): e for e in wim.get("formal_positions", [])}
expected_wim = {
    "2001-wim-majority-mans-duty-to-protect-woman": 5,
    "2001-wim-minority-wise-counsel": 4,
    "2002-wim-majority-final-recommendations": 6,
    "2002-wim-minority-pastoral-counsel": 4,
}
if set(positions) != set(expected_wim):
    raise SystemExit(f"Women in the Military: formal-position event set drift: {sorted(positions)}")
for event_id, count in expected_wim.items():
    e=positions[event_id]
    if e.get("signer_count") != count or len(e.get("signers", [])) != count:
        raise SystemExit(f"{event_id}: signer count drift")
    if e.get("evidence_class") != "signed_formal_report_or_minority_report" or e.get("ideological_weight") != 0:
        raise SystemExit(f"{event_id}: evidence semantics drift")
if {r.get("name_as_printed") for r in positions["2001-wim-majority-mans-duty-to-protect-woman"]["signers"]} != {"Timothy B. Bayly", "Bentley B. Rayburn", "Donald B. Weyburn", "Stephen W. Leonard", "Keith Stoeber"}:
    raise SystemExit("2001 WIM majority: signer set drift")
if {r.get("name_as_printed") for r in positions["2001-wim-minority-wise-counsel"]["signers"]} != {"Stephen Clark", "Charles Morrison", "Beryl Hubbard", "Ronald Swafford"}:
    raise SystemExit("2001 WIM minority: signer set drift")
if any(r.get("name_as_printed") == "Peter Lillback" for e in positions.values() if e.get("year") == 2001 for r in e.get("signers", [])):
    raise SystemExit("2001 WIM: do not infer Peter Lillback into either published 2001 signature block")
if {r.get("name_as_printed") for r in positions["2002-wim-majority-final-recommendations"]["signers"]} != {"Steve Leonard", "Bentley Rayburn", "Tim Bayly", "Keith Stoeber", "Peter Lillback", "Don Weyburn"}:
    raise SystemExit("2002 WIM majority: signer set drift")
if {r.get("name_as_printed") for r in positions["2002-wim-minority-pastoral-counsel"]["signers"]} != {"Steven Clark", "Beryl Hubbard", "Charles Morrison", "Ronald Swafford"}:
    raise SystemExit("2002 WIM minority: signer set drift")
actions = {a.get("year"): a for a in wim.get("assembly_actions", [])}
if actions.get(2002, {}).get("recorded_negative_vote_count") != 77 or actions.get(2002, {}).get("person_level_evidence_for_77") is not False:
    raise SystemExit("2002 WIM: preserve 77-vote count without inventing a named roster")

hierarchy = {row.get("evidence_class"): row for row in index.get("evidence_hierarchy", [])}
for required in (
    "signed_formal_report_or_minority_report",
    "recorded_vote_or_formal_protest_signature",
    "first_person_issue_statement",
    "study_committee_consensus_participation",
    "committee_membership_only",
    "conference_or_network_participation",
    "recorded_procedural_position",
):
    if required not in hierarchy:
        raise SystemExit(f"formal position index: missing evidence class {required}")

indexed = {row.get("evidence_id"): row for row in index.get("normalized_position_sources", [])}
for required in (
    "2001-wim-consensus-report",
    "2001-wim-majority-duty-report",
    "2001-wim-minority-wise-counsel-report",
    "2002-wim-majority-final-recommendations",
    "2002-wim-minority-pastoral-counsel",
    "2008-overture-9-deaconess-study-minority-report",
    "2008-rpr-women-scripture-reading-minority-report",
    "2009-overture-10-women-roles-study-minority-report",
    "2016-women-study-committee-point-of-order-registration",
    "2016-pipa-protest-women-study-committee",
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
