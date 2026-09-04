#!/usr/bin/env python3
"""Validate the bounded Revoice18 Wayback/media recovery without inventing a full 2018 program."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
receipt = json.loads((root / "sources/raw/issues/revoice/revoice18-wayback-recovery-2026-09-04.json").read_text(encoding="utf-8"))
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

records = media.get("records", [])
if media.get("metadata", {}).get("record_count") != 12 or len(records) != 12:
    raise SystemExit(f"Revoice18 recovered media: expected 12 records, found {len(records)}")
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
    "media_records": len(records),
    "section_counts": dict(Counter(row["page_section"] for row in records)),
    "year_status_counts": dict(Counter(row["year_status"] for row in records)),
}, indent=2))
