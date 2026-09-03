#!/usr/bin/env python3
"""Normalize the preserved 737-entry A Faithful PCA transcription."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("usage: parse-a-faithful-pca-transcription.py <repo-root> <input.md> <output.json>")

root = Path(sys.argv[1])
input_path = Path(sys.argv[2])
output_path = Path(sys.argv[3])
text = input_path.read_text(encoding="utf-8", errors="replace")

heading = re.compile(r"^\*\*(\d{1,3})\.\s+(.+?)\*\*\s*$", re.M)
matches = list(heading.finditer(text))
people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))


def identity_key(value: str) -> str:
    value = value.replace("’", "'")
    value = re.sub(r"^(?:(?:rev|dr)\.?\s+)+", "", value, flags=re.I)
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    value = re.sub(r"[^a-z0-9 ]+", " ", value.lower())
    tokens = [token for token in value.split() if len(token) > 1]
    return f"{tokens[0]} {tokens[-1]}" if len(tokens) >= 2 else " ".join(tokens)


person_index = {}
for person in people:
    person_index.setdefault(identity_key(person["name"]), []).append(person["id"])

role_terms = re.compile(
    r"\b(?:pastor|minister|director|professor|dean|chaplain|coordinator|president|moderator|teacher|missionary|"
    r"church plant|intern|candidate|retired|clerk|elder|executive|founder|leader|head|officer|staff|honorably)\b",
    re.I,
)
location_re = re.compile(r"^.+,\s*(?:[A-Z]{2}|[A-Za-zÁ-ÿ .'-]+)(?:,\s*[A-Z]{2})?$")

records = []
for i, match in enumerate(matches):
    sequence = int(match.group(1))
    printed_name = match.group(2).strip()
    stop = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    raw_lines = [line.strip() for line in text[match.end():stop].splitlines() if line.strip()]
    presbytery = next((line for line in reversed(raw_lines) if line.endswith("Presbytery")), None)
    remaining = [line for line in raw_lines if line != presbytery]
    location = next((line for line in reversed(remaining) if location_re.match(line)), None)
    details = [line for line in remaining if line != location]
    roles = [line for line in details if role_terms.search(line)]
    institutions = [line for line in details if line not in roles]
    honorific_match = re.match(r"^((?:(?:Rev|Dr)\.?\s+)+)", printed_name, re.I)
    candidates = person_index.get(identity_key(printed_name), [])

    city = region = country = None
    if location:
        parts = [part.strip() for part in location.split(",")]
        city = parts[0] or None
        if len(parts) == 2 and re.fullmatch(r"[A-Z]{2}", parts[1]):
            region = parts[1]
            country = "United States"
        elif len(parts) == 3 and re.fullmatch(r"[A-Z]{2}", parts[-1]):
            region = parts[-1]
            country = "United States"
        elif len(parts) >= 2:
            country = parts[-1]

    records.append(
        {
            "snapshot_date": "2022-03-14",
            "sequence_number": sequence,
            "name_as_printed": printed_name,
            "honorific_as_printed": honorific_match.group(1).strip() if honorific_match else None,
            "role_as_printed": roles or None,
            "church_or_institution_as_printed": institutions or None,
            "location_as_printed": location,
            "city_as_printed": city,
            "state_or_region_as_printed": region,
            "country_as_printed": country,
            "presbytery_as_printed": presbytery,
            "normalized_person_id": candidates[0] if len(candidates) == 1 else None,
            "details_as_printed": details,
            "source_locator": f"signature #{sequence}",
        }
    )

sequences = [row["sequence_number"] for row in records]
missing = [n for n in range(1, 738) if n not in sequences]
duplicates = sorted({n for n in sequences if sequences.count(n) > 1})
result = {
    "metadata": {
        "snapshot_date": "2022-03-14",
        "expected_signers": 737,
        "parsed_signers": len(records),
        "missing_sequences": missing,
        "duplicate_sequences": duplicates,
        "primary_source": "https://web.archive.org/web/20220314223906/https://www.afaithfulpca.net/signatures",
        "raw_transcription": str(input_path),
        "rules": {
            "source_wording_preserved": True,
            "creates_new_person_nodes": False,
            "role_and_institution_split_is_heuristic": True,
            "details_as_printed_is_authoritative": True,
        },
    },
    "signers": records,
}

if len(records) != 737 or missing or duplicates:
    raise SystemExit(f"invalid roster: rows={len(records)} missing={missing} duplicates={duplicates}")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"parsed {len(records)} A Faithful PCA signers")
