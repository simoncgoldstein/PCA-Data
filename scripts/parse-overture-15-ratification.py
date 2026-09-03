#!/usr/bin/env python3
"""Extract the 2023 presbytery ratification table for 2022 Overture 15."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: parse-overture-15-ratification.py <repo-root> <output.json>")

root = Path(sys.argv[1])
output = Path(sys.argv[2])
text_path = root / "sources/raw/general-assembly/2023/50th_pcaga_2023.txt"
lines = text_path.read_text(encoding="utf-8", errors="replace").splitlines()

start = next(i for i, line in enumerate(lines) if "1 Arizona" in line and "45 Mississippi Valley" in line)
table_lines = lines[start : start + 44]

presbyteries = json.loads((root / "data/presbyteries.json").read_text(encoding="utf-8"))
name_to_id = {p["name"].lower(): p["id"] for p in presbyteries}
aliases = {
    "korean southwest o.c.": "korean-southwest-orange-county",
    "lowcountry": "lowcountry",
    "north t exas": "north-texas",
    "peedee": "pee-dee",
    "philadelphia metro w.": "philadelphia-metro-west",
    "piedmont t riad": "piedmont-triad",
    "south t exas": "south-texas",
    "t ennessee valley": "tennessee-valley",
    "t idewater": "tidewater",
}


def number(value: str) -> int | None:
    value = value.strip()
    return int(value) if value else None


def parse_half(line: str, offset: int) -> dict:
    if offset == 0:
        head, vote_slices = line[0:27], ((27, 34), (34, 44), (44, 54), (54, 63), (63, 72))
    else:
        head, vote_slices = line[76:100], ((100, 107), (107, 116), (116, 126), (126, 134), (134, 143))
    match = re.match(r"\s*(\d+)\s+(.+?)\s*$", head)
    if not match:
        raise ValueError(f"could not parse table half: {line!r}")
    sequence, printed_name = int(match.group(1)), match.group(2)
    values = [number(line[a:b]) for a, b in vote_slices]
    canonical_key = aliases.get(printed_name.lower()) or name_to_id.get(printed_name.lower())
    return {
        "print_order": sequence,
        "presbytery_as_printed": printed_name,
        "presbytery_id": canonical_key,
        "for": values[0],
        "against": values[1],
        "abstain": values[2],
        "passed": values[3] == 1 if values[3] is not None else None,
        "not_passed": values[4] == 1 if values[4] is not None else None,
        "reported": any(value is not None for value in values),
        "pdf_page": 136,
        "printed_page": 134,
    }


rows = []
for line in table_lines:
    rows.append(parse_half(line, 0))
    rows.append(parse_half(line, 76))
rows.sort(key=lambda row: row["print_order"])

assert [row["print_order"] for row in rows] == list(range(1, 89))
assert sum(row["reported"] for row in rows) == 68
assert sum(row["passed"] is True for row in rows) == 39
assert sum(row["not_passed"] is True for row in rows) == 29
unresolved = [row["presbytery_as_printed"] for row in rows if not row["presbytery_id"]]
assert unresolved == ["Columbus Metro"]

result = {
    "metadata": {
        "event": "50th General Assembly — Overture 15 / BCO 7-4 Presbytery Ratification",
        "action_date": "2023",
        "primary_source": "https://www.pcahistory.org/pca/ga/50th_pcaga_2023.pdf",
        "local_pdf": "sources/raw/general-assembly/2023/50th_pcaga_2023.pdf",
        "local_pdf_text": "sources/raw/general-assembly/2023/50th_pcaga_2023.txt",
        "official_totals": {"for": 39, "against": 29, "presbyteries": 88, "reporting": 68, "two_thirds_needed": 59},
        "result": "not_ratified",
        "scope_note": "These are presbytery-level actions and must not be attributed to every minister or member in a presbytery.",
        "transcription_note": "Spacing artifacts in North Texas, Piedmont Triad, South Texas, Tennessee Valley, and Tidewater are preserved in presbytery_as_printed and mapped explicitly to canonical IDs.",
        "unresolved_presbyteries": unresolved,
        "unresolved_note": "Columbus Metro appears in the 2023 official table but is absent from the repository's 2026 current-presbytery backbone; it remains unresolved rather than being silently mapped to a successor.",
    },
    "presbytery_votes": rows,
}

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("overture-15-ratification-2023: parsed 88 presbyteries; 68 reporting; 39 passed; 29 did not pass")
