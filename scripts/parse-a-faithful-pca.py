#!/usr/bin/env python3
"""Parse the preserved 2021 A Faithful PCA signer page into roster records.

Input is text produced by `pdftotext -layout` from the 149-page Wayback PDF.
The parser deliberately preserves raw block lines. It extracts only high-confidence
fields automatically; identity resolution and current-role lookup happen later.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) < 4:
    raise SystemExit("usage: parse-a-faithful-pca.py <repo-root> <input.txt> <output.json>")

root = Path(sys.argv[1])
input_path = Path(sys.argv[2])
output_path = Path(sys.argv[3])
text = input_path.read_text(encoding="utf-8", errors="replace")
people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))


def identity_key(value: str) -> str:
    value = re.sub(r"^(?:(?:rev|dr)\.?\s+)+", "", value, flags=re.I)
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    value = re.sub(r"[^a-z0-9 ]+", " ", value.lower())
    parts = value.split()
    return f"{parts[0]} {parts[-1]}" if len(parts) >= 2 else " ".join(parts)


person_index = {}
for person in people:
    person_index.setdefault(identity_key(person["name"]), []).append(person["id"])

# Preserve page numbers from form-feed boundaries.
pages = text.split("\f")
lines = []
for page_index, page in enumerate(pages, start=1):
    for raw in page.splitlines():
        line = raw.strip()
        if not line:
            continue
        # Drop recurring browser/PDF capture chrome.
        if line.startswith("https://web.archive.org/"):
            continue
        if re.match(r"^\d+/\d+/\d+, .*Signatures — A Faithful PCA$", line):
            continue
        if line in {"Signatures", "A letter to our brothers and friends in the", "Presbyterian Church in America"}:
            continue
        if "Any PCA pastor or elder who wishes to sign this letter" in line:
            continue
        if line.startswith("The Wayback Machine"):
            continue
        if line.startswith("A Faithful PCA Open Letter"):
            continue
        lines.append((page_index, line))

start_re = re.compile(r"^(\d{1,3})\.\s+(.+)$")
starts = []
for i, (page, line) in enumerate(lines):
    m = start_re.match(line)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 571:
            starts.append((i, page, n, m.group(2).strip()))

records = []
for pos, (line_index, page, sequence, name_as_printed) in enumerate(starts):
    next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
    block = lines[line_index + 1 : next_index]
    raw_lines = [line for _, line in block]
    block_pages = sorted(set([page] + [p for p, _ in block]))

    # Last clear presbytery line in the block.
    presbytery = None
    for line in reversed(raw_lines):
        if re.search(r"\bPresbytery$", line):
            presbytery = line
            break

    # First clear US/Canada-style city/state line. Keep as printed.
    location = None
    for line in raw_lines:
        if re.search(r",\s*(?:[A-Z]{2}|ON|BC|AB|SK|MB|QC|NB|NS|PE|NL)\b", line):
            location = line
            break

    # Strip obvious honorifics for a normalized-name candidate only; do not resolve identities here.
    normalized_name_candidate = re.sub(
        r"^(?:Rev\.?\s+Dr\.?|Rev\.?|Dr\.?|TE|RE)\s+", "", name_as_printed, flags=re.I
    ).strip()
    candidates = person_index.get(identity_key(name_as_printed), [])

    records.append(
        {
            "sequence": sequence,
            "name_as_printed": name_as_printed,
            "normalized_name_candidate": normalized_name_candidate,
            "normalized_person_id": candidates[0] if len(candidates) == 1 else None,
            "pdf_pages": block_pages,
            "presbytery_as_printed": presbytery,
            "location_as_printed": location,
            "raw_lines": raw_lines,
            "source": {
                "title": "A Faithful PCA Signatures — Wayback capture",
                "captured_page": "https://web.archive.org/web/20210611152829/https://www.afaithfulpca.net/signatures",
                "preserved_pdf": "https://warhornmedia.com/wp-content/uploads/2022/09/Signatures-%E2%80%94-A-Faithful-PCA.pdf",
                "snapshot_date": "2021-06-11",
            },
        }
    )

# Structural validation.
sequences = [r["sequence"] for r in records]
expected = list(range(1, 572))
missing = [n for n in expected if n not in sequences]
duplicates = sorted({n for n in sequences if sequences.count(n) > 1})

result = {
    "metadata": {
        "expected_signers": 571,
        "snapshot_date": "2021-06-11",
        "primary_source": "https://web.archive.org/web/20210611152829/https://www.afaithfulpca.net/signatures",
        "local_pdf": "sources/raw/public-statements/a-faithful-pca/signatures-2021-06-11.pdf",
        "parsed_signers": len(records),
        "missing_sequences": missing,
        "duplicate_sequences": duplicates,
        "rules": {
            "creates_person_nodes": False,
            "historical_snapshot_only": True,
            "current_role_inference": False,
            "raw_block_preserved": True,
        },
    },
    "signers": records,
}

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Parsed {len(records)} signer records; missing={missing}; duplicates={duplicates}")

if len(records) != 571 or missing or duplicates:
    raise SystemExit(2)
