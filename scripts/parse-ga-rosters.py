#!/usr/bin/env python3
"""Extract source-faithful named rosters from PCA General Assembly minutes.

The parser operates only inside explicit start/end markers, preserves every
printed field, and resolves only people already present in data/people.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("usage: parse-ga-rosters.py <repo-root> <roster-key> <output.json>")

root = Path(sys.argv[1])
key = sys.argv[2]
output = Path(sys.argv[3])

CONFIG = {
    "warhurst-2019": {
        "input": "sources/raw/general-assembly/2019/47th_pcaga_2019.txt",
        "start": "The following commissioners registered their protest:",
        "end": "47-44 Report of the Overtures Committee",
        "mode": "name",
        "expected": 203,
        "event": "47th General Assembly — 2019 Warhurst Protest",
        "url": "https://www.pcahistory.org/pca/ga/47th_pcaga_2019.pdf",
    },
    "nae-withdrawal-2022": {
        "input": "sources/raw/general-assembly/2022/49th_pcaga_2022_vol01.txt",
        "start": "Protest Signatories",
        "end": "49-33 PCA Retirement & Benefits",
        "mode": "first_last",
        "expected": 203,
        "event": "49th General Assembly — NAE Withdrawal Protest",
        "url": "https://pcahistory.org/pca/ga/49th_pcaga_2022_vol01.pdf",
    },
    "overture-15-negative-2022": {
        "input": "sources/raw/general-assembly/2022/49th_pcaga_2022_vol01.txt",
        "start": "Overture 15 – Negative Votes",
        "end": "The Chairman resumed his report by moving Recommendation 8",
        "mode": "first_last",
        "expected": None,
        "event": "49th General Assembly — Overture 15 Recorded Negative Votes",
        "url": "https://www.pcahistory.org/pca/ga/49th_pcaga_2022.pdf",
    },
    "overture-15-minority-2022": {
        "input": "sources/raw/general-assembly/2022/49th_pcaga_2022_vol01.txt",
        "start": "MINORITY REPORT\n                             ON OVERTURE 15",
        "row_start": "SIGNED BY:",
        "end": "MINORITY REPORT\n                              ON OVERTURE 26",
        "mode": "name",
        "expected": 46,
        "event": "49th General Assembly — Overture 15 Minority Report",
        "url": "https://www.pcahistory.org/pca/ga/49th_pcaga_2022.pdf",
    },
}

if key not in CONFIG:
    raise SystemExit(f"unknown roster-key: {key}")
cfg = CONFIG[key]
text_path = root / cfg["input"]
text = text_path.read_text(encoding="utf-8", errors="replace")

start = text.find(cfg["start"])
if start < 0:
    raise SystemExit(f"start marker not found for {key}")
if cfg.get("row_start"):
    start = text.find(cfg["row_start"], start)
    if start < 0:
        raise SystemExit(f"row start marker not found for {key}")
end = text.find(cfg["end"], start)
if end < 0:
    raise SystemExit(f"end marker not found for {key}")

# Record PDF page and the printed page label for every source line.
line_meta = {}
global_line = 0
for pdf_page, page in enumerate(text.split("\f"), start=1):
    standalone = [
        int(m.group(1))
        for line in page.splitlines()
        if (m := re.match(r"^\s*(\d{1,4})\s*$", line))
    ]
    printed_page = standalone[-1] if standalone else None
    for _line in page.splitlines(keepends=True):
        global_line += 1
        line_meta[global_line] = (pdf_page, printed_page)

start_line = text[:start].count("\n") + 1
segment = text[start:end]

people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))


def identity_key(value: str) -> str:
    value = value.replace("’", "'")
    value = re.sub(r"^(?:rev\.?|dr\.?|te|re)\s+", "", value, flags=re.I)
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    value = re.sub(r"[^a-z0-9 ]+", " ", value.lower())
    tokens = [token for token in value.split() if len(token) > 1]
    if len(tokens) >= 2:
        return f"{tokens[0]} {tokens[-1]}"
    return " ".join(tokens)


person_index = {}
for person in people:
    person_index.setdefault(identity_key(person["name"]), []).append(person["id"])

rows = []
pending = None
for offset, raw in enumerate(segment.splitlines(), start=0):
    source_line = start_line + offset
    line = raw.rstrip()
    if cfg["mode"] == "first_last":
        match = re.match(r"^\s*(TE|RE)\s{2,}(.+?)\s{2,}(.+?)\s{2,}(.+?)\s*$", line)
        if match:
            office, first, last, presbytery = (part.strip() for part in match.groups())
            name = f"{first} {last}".strip()
            pending = {
                "office_as_printed": office,
                "first_name_as_printed": first,
                "last_name_as_printed": last,
                "name_as_printed": name,
                "presbytery_as_printed": presbytery,
                "source_line": source_line,
            }
            rows.append(pending)
            continue
        # One known PDF extraction wrap splits Won Kwak's presbytery over two lines.
        if pending and pending["name_as_printed"] == "Won Kwak" and "CountyCoast" in line:
            pending["presbytery_as_printed"] = "South Coast"
            pending["raw_wrap_note"] = line.strip()
        continue

    match = re.match(r"^\s*(TE|RE)\s+(.+?)\s{2,}(.+?)\s*$", line)
    if not match:
        continue
    office, name, presbytery = (part.strip() for part in match.groups())
    rows.append(
        {
            "office_as_printed": office,
            "name_as_printed": name,
            "presbytery_as_printed": presbytery,
            "source_line": source_line,
        }
    )

for index, row in enumerate(rows, start=1):
    row["print_order"] = index
    pdf_page, printed_page = line_meta.get(row.pop("source_line"), (None, None))
    row["pdf_page"] = pdf_page
    row["printed_page"] = printed_page
    candidates = person_index.get(identity_key(row["name_as_printed"]), [])
    row["normalized_person_id"] = candidates[0] if len(candidates) == 1 else None

result = {
    "metadata": {
        "event": cfg["event"],
        "primary_source": cfg["url"],
        "local_pdf_text": cfg["input"],
        "extraction_start_marker": cfg["start"],
        "extraction_end_marker": cfg["end"],
        "expected_rows": cfg["expected"],
        "parsed_rows": len(rows),
        "identity_rule": "Only unique matches to existing data/people.json records are resolved; printed names and presbyteries remain unchanged.",
    },
    "signers" if "negative" not in key else "negative_votes": rows,
}

if cfg["expected"] is not None and len(rows) != cfg["expected"]:
    raise SystemExit(f"{key}: parsed {len(rows)} rows, expected {cfg['expected']}")

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"{key}: parsed {len(rows)} rows")
