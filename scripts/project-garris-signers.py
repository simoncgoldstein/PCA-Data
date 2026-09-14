#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write(relative: str, value) -> None:
    (ROOT / relative).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


relative = "sources/normalized/public-statements/garris-letters-2024.json"
data = load(relative)
affiliations = load("data/affiliations.json")
events = load("data/events.json")
people = {row["id"]: row for row in load("data/people.json")}

by_pair = {}
for aff in affiliations:
    if aff.get("target_type") == "event":
        by_pair.setdefault((aff.get("person_id"), aff.get("target_id")), []).append(aff)

created = 0
existing = 0
unresolved = 0
resolved_by_letter = {}

for letter in data["letters"]:
    event_id = letter["event_id"]
    source_id = letter["source_id"]
    resolved_count = 0
    for row in letter["signers"]:
        person_id = row.get("normalized_person_id")
        if not person_id:
            unresolved += 1
            continue
        if person_id not in people:
            raise SystemExit(f"{letter['letter_id']}:{row['print_order']}: unknown normalized_person_id {person_id}")
        resolved_count += 1
        key = (person_id, event_id)
        matches = by_pair.get(key, [])
        if len(matches) > 1:
            raise SystemExit(f"duplicate app affiliations for {person_id} -> {event_id}")
        if matches:
            aff = matches[0]
            if aff.get("role", "").split(";")[0] != "Signer":
                raise SystemExit(f"existing Garris edge has unexpected role: {aff['id']}")
            if aff.get("confidence") != "confirmed" or aff.get("weight") != 3 or aff.get("score_included") is not True:
                raise SystemExit(f"existing Garris edge has scoring/confidence drift: {aff['id']}")
            if source_id not in aff.get("source_ids", []):
                raise SystemExit(f"existing Garris edge missing source: {aff['id']}")
            existing += 1
            continue

        aff_id = f"aff-{slug(letter['letter_id'])}-{person_id}"
        if any(a.get("id") == aff_id for a in affiliations):
            raise SystemExit(f"affiliation id collision: {aff_id}")
        context = ", ".join(
            value for value in [row.get("office_as_printed"), row.get("institution_as_printed"), row.get("presbytery_as_printed")]
            if value
        )
        aff = {
            "id": aff_id,
            "person_id": person_id,
            "target_type": "event",
            "target_id": event_id,
            "role": "Signer",
            "confidence": "confirmed",
            "evidence_kind": "public_coalition_action",
            "weight": 3,
            "score_included": True,
            "source_ids": [source_id],
            "notes": f"Printed signer context: {context}. Signature establishes participation in this specific public letter; it does not by itself establish unrelated network membership or positions on other controversies.",
        }
        affiliations.append(aff)
        by_pair[key] = [aff]
        created += 1
    resolved_by_letter[letter["letter_id"]] = resolved_count

# Keep event descriptions literal and source-bounded.
event_by_id = {row["id"]: row for row in events}
for letter in data["letters"]:
    event = event_by_id.get(letter["event_id"])
    if not event:
        raise SystemExit(f"missing app event: {letter['event_id']}")
    event["notes"] = (
        letter["signed_action_summary"]
        + " Signer edges record this specific public action only; co-signature is not treated as proof of other network membership or a generic ideological label."
    )

write("data/affiliations.json", affiliations)
write("data/events.json", events)

print(json.dumps({
    "dataset": data["metadata"]["dataset_id"],
    "resolved_by_letter": resolved_by_letter,
    "created_affiliations": created,
    "existing_affiliations": existing,
    "unresolved_signer_rows": unresolved,
}, indent=2))
