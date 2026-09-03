#!/usr/bin/env python3
"""Verify and source-faithfully normalize the 2021 Overture 37 roster."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: verify-overture-37-roster.py <repo-root> <output.json>")
root, output = Path(sys.argv[1]), Path(sys.argv[2])
text = (root / "sources/raw/general-assembly/2021/48th_pcaga_2021.txt").read_text(encoding="utf-8", errors="replace")
start = text.index("Minority Report Signers\nTE Robert Binion")
end = text.index("\n\n\nMinority Report Overture 37", start)
source_lines = text[start:end].splitlines()[1:]

people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))
presbyteries = json.loads((root / "data/presbyteries.json").read_text(encoding="utf-8"))


def person_key(value: str) -> str:
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    value = re.sub(r"[^a-z0-9 ]", " ", value.lower())
    parts = value.split()
    return f"{parts[0]} {parts[-1]}"


person_index = {}
for person in people:
    person_index.setdefault(person_key(person["name"]), []).append(person["id"])
presbytery_index = {p["name"].lower(): p["id"] for p in presbyteries}
presbytery_aliases = {
    "susquehanna": "susquehanna-valley",
    "new york metro": "metropolitan-new-york",
    "presbytery of northern illinois": "northern-illinois",
}

rows = []
for sequence, line in enumerate(source_lines, 1):
    if line == "TE Tag Tuck Blue, Ridge Presbytery":
        office, name, printed_presbytery = "TE", "Tag Tuck", "Blue, Ridge Presbytery"
        canonical_name = "Blue Ridge"
    else:
        match = re.match(r"^(TE|RE) (.+?), (.+)$", line)
        if not match:
            raise ValueError(f"unparsed roster line: {line!r}")
        office, name, printed_presbytery = match.groups()
        canonical_name = re.sub(r" Presbytery$", "", printed_presbytery)
    candidates = person_index.get(person_key(name), [])
    presbytery_id = presbytery_aliases.get(canonical_name.lower()) or presbytery_index.get(canonical_name.lower())
    rows.append({
        "print_order": sequence,
        "office_as_printed": office,
        "name_as_printed": name,
        "presbytery_as_printed": printed_presbytery,
        "presbytery_id": presbytery_id,
        "normalized_person_id": candidates[0] if len(candidates) == 1 else None,
        "pdf_page": 135,
        "printed_appendix_page": 10,
    })

assert len(rows) == 28
assert all(row["presbytery_id"] for row in rows)
result = {
    "metadata": {
        "event": "48th General Assembly — Overture 37 Minority Report",
        "year": 2021,
        "primary_source": "https://www.pcahistory.org/pca/ga/48th_pcaga_2021.pdf",
        "local_pdf": "sources/raw/general-assembly/2021/48th_pcaga_2021.pdf",
        "status": "verified against official primary-source roster",
        "method_note": "This records formal minority-report signership only. It should not be collapsed into a generic ideological label.",
        "source_oddity_note": "The extracted official text reads 'TE Tag Tuck Blue, Ridge Presbytery'; that wording is preserved while the canonical presbytery mapping is Blue Ridge.",
        "parsed_rows": 28,
    },
    "signers": rows,
}
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("overture-37-minority-2021: verified 28 signers")
