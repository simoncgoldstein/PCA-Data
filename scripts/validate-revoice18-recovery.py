#!/usr/bin/env python3
"""Validate the bounded Revoice18 archive/transcript recovery without inventing a full 2018 program."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
receipt = json.loads((root / "sources/raw/issues/revoice/revoice18-wayback-recovery-2026-09-04.json").read_text(encoding="utf-8"))
transcripts = json.loads((root / "sources/raw/issues/revoice/revoice18-general-session-transcript-receipt-2026-09-04.json").read_text(encoding="utf-8"))
media = json.loads((root / "sources/normalized/revoice/revoice18-recovered-media-2019-07.json").read_text(encoding="utf-8"))

captures = receipt.get("exact_endpoint_captures", [])
if [(row.get("timestamp"), row.get("statuscode")) for row in captures] != [
    ("20190707073156", 200),
    ("20190717044623", 200),
]:
    raise SystemExit("Revoice18 recovery: exact endpoint capture set drift")
if any(row.get("timestamp", "").startswith("2018") for row in captures):
    raise SystemExit("Revoice18 recovery: do not claim an exact 2018 event-path capture")

expected_capture_hashes = {
    "20190707073156": "2072943a8696fd2466d6d17a36505d78a15f97a10feb641d59a866e66afc61f9",
    "20190717044623": "1745446332198aa7e64756807bb581d049cd429691d9b24cbbaf42136c4d0d9f",
}
for row in captures:
    if row.get("recovered_body_sha256") != expected_capture_hashes.get(row.get("timestamp")):
        raise SystemExit(f"Revoice18 recovery: capture hash drift at {row.get('timestamp')}")

probes = receipt.get("known_2018_root_capture_probes", [])
if len(probes) != 2 or any(row.get("returned_body_sha256") != expected_capture_hashes["20190707073156"] for row in probes):
    raise SystemExit("Revoice18 recovery: known 2018 root probes must remain documented as forward-resolved 2019 bodies")

sessions = transcripts.get("sessions", [])
if len(sessions) != 3:
    raise SystemExit(f"Revoice18 transcripts: expected 3 session receipts, found {len(sessions)}")
by_session = {row.get("session_number"): row for row in sessions}
if [by_session[n].get("theme") for n in (1, 2, 3)] != ["Praise", "Lament", "Hope"]:
    raise SystemExit("Revoice18 transcripts: Praise/Lament/Hope sequence drift")
expected_transcript_evidence = {
    1: ("bcdaff28872c598583b8036e36c845050662de08ede0c7efd7eca314c65aafe2", 634, "reviewed_user_supplied_text"),
    2: ("aa70e45f2488043820860323cd8608c5591a67fecbeec03b82fd549dfa5bd0e9", 508, "reviewed_user_supplied_text"),
}
for number, (digest, line_count, status) in expected_transcript_evidence.items():
    row = by_session[number]
    if (row.get("transcript_sha256"), row.get("transcript_line_count"), row.get("transcript_status")) != (digest, line_count, status):
        raise SystemExit(f"Revoice18 transcripts: source evidence drift for session {number}")
if by_session[3].get("transcript_status") != "not_available_in_current_chat":
    raise SystemExit("Revoice18 transcripts: Session 3 must remain marked unavailable until primary transcript evidence is preserved")
if "printed program" not in transcripts.get("program_recovery_implication", ""):
    raise SystemExit("Revoice18 transcripts: physical/distributed program recovery lead missing")

records = media.get("records", [])
if media.get("metadata", {}).get("record_count") != 12 or len(records) != 12:
    raise SystemExit(f"Revoice18 recovered media: expected 12 records, found {len(records)}")
if media.get("metadata", {}).get("general_session_transcript_receipt") != "sources/raw/issues/revoice/revoice18-general-session-transcript-receipt-2026-09-04.json":
    raise SystemExit("Revoice18 recovered media: transcript receipt linkage missing")
if Counter(row.get("page_section") for row in records) != {
    "General Sessions": 3,
    "Workshops": 4,
    "Spiritual Friendship Preconference": 5,
}:
    raise SystemExit("Revoice18 recovered media: section counts drift")

ids = [row.get("youtube_id") for row in records]
if len(ids) != len(set(ids)) or any(not value for value in ids):
    raise SystemExit("Revoice18 recovered media: YouTube IDs must be unique and nonblank")

by_id = {row["youtube_id"]: row for row in records}
for youtube_id in ("xC4u02b9-gk", "SHe2y2SVjIc", "ImESpqDCfhQ", "ijGQEJOHMP8"):
    if by_id[youtube_id].get("year_status") != "confirmed_2018":
        raise SystemExit(f"Revoice18 recovered media: confirmed 2018 status drift for {youtube_id}")

session1 = by_id["xC4u02b9-gk"]
if session1.get("title_as_printed") != "Revoice 2018 – General Session 1: Praise | Eve Tushnet & Amber Carol":
    raise SystemExit("Revoice18 Session 1: preserve first-party printed Amber Carol title spelling")
resolved1 = {(row.get("name"), row.get("role")) for row in session1.get("resolved_participants", [])}
if resolved1 != {("Amber Carroll", "testimony"), ("Eve Tushnet", "message")}:
    raise SystemExit("Revoice18 Session 1: resolved transcript participants drift")
roles1 = {(row.get("name"), row.get("role")) for row in session1.get("additional_named_session_roles", [])}
if roles1 != {("Greg Johnson", "opening_welcome"), ("Chris Gillum", "conference_chaplain_opening_prayer")}:
    raise SystemExit("Revoice18 Session 1: named opening roles drift")

session2 = by_id["SHe2y2SVjIc"]
resolved2 = {(row.get("name"), row.get("role")) for row in session2.get("resolved_participants", [])}
if resolved2 != {("Ray Low", "testimony"), ("Nate Collins", "message")}:
    raise SystemExit("Revoice18 Session 2: resolved participants drift")
if any(row.get("name") == "Ray Lowe" for row in session2.get("resolved_participants", [])):
    raise SystemExit("Revoice18 Session 2: transcript spelling Ray Lowe must not silently become normalized identity")
if "printed program" not in session2.get("program_artifact_evidence", ""):
    raise SystemExit("Revoice18 Session 2: direct program-artifact evidence missing")

session3 = by_id["ImESpqDCfhQ"]
if {(row.get("name"), row.get("role")) for row in session3.get("resolved_participants", [])} != {("Wesley Hill", "message")}:
    raise SystemExit("Revoice18 Session 3: only Wesley Hill may be resolved from current primary evidence")
held = session3.get("held_name_resolution", {})
if (held.get("printed_name"), held.get("candidate")) != ("Bekah", "Bekah Mason"):
    raise SystemExit("Revoice18 Session 3: Bekah Mason candidate must remain explicitly held")

for youtube_id in ("Msbsg1vE-qI", "nEtLYGZB280"):
    if by_id[youtube_id].get("year_status") != "unresolved" or by_id[youtube_id].get("revoice18_graph_status") != "hold":
        raise SystemExit(f"Revoice18 recovered media: unresolved mixed-gallery item promoted without evidence: {youtube_id}")
if by_id["PGOA2P2Xtwc"].get("year_status") != "confirmed_2019" or by_id["PGOA2P2Xtwc"].get("revoice18_graph_status") != "exclude_from_revoice18":
    raise SystemExit("Revoice18 recovered media: known Revoice 2019 workshop must stay excluded from Revoice18")

for youtube_id in ("vqgKUYCbXg4", "K4CGXuJpWXI", "FG0fev-WtQE", "3lcLTpdJAuw"):
    row = by_id[youtube_id]
    if row.get("year_status") != "confirmed_2018_related_preconference" or row.get("revoice18_graph_status") != "related_event_not_main_conference":
        raise SystemExit(f"Revoice18 recovered media: preconference/main-conference boundary drift for {youtube_id}")
if by_id["-upw6WjZGpk"].get("year_status") != "probable_2018_related_preconference" or by_id["-upw6WjZGpk"].get("revoice18_graph_status") != "hold_related_event":
    raise SystemExit("Revoice18 recovered media: panel must remain held pending independent date/participant confirmation")

if "not a reconstruction of the original advertised Revoice 2018 program" not in media.get("metadata", {}).get("modeling_rule", ""):
    raise SystemExit("Revoice18 recovered media: incompleteness boundary missing")

print(json.dumps({
    "captures": len(captures),
    "transcript_receipts": len(sessions),
    "media_records": len(records),
    "section_counts": dict(Counter(row["page_section"] for row in records)),
    "year_status_counts": dict(Counter(row["year_status"] for row in records)),
}, indent=2))
