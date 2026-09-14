#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def load(relative: str):
    return json.loads((root / relative).read_text(encoding="utf-8"))


garris = load("sources/normalized/public-statements/garris-letters-2024.json")
receipt = load("sources/raw/identity/2024-garris-letter2-identity-evidence-2026-09-14.json")
people = load("data/people.json")
affiliations = load("data/affiliations.json")
events = load("data/events.json")

people_by_id = {row["id"]: row for row in people}
event_by_id = {row["id"]: row for row in events}

meta = garris.get("metadata", {})
if meta.get("dataset_id") != "garris_letters_2024":
    raise SystemExit("Garris dataset_id drift")
if meta.get("letter_1_signer_count") != 60 or meta.get("letter_2_signer_count") != 21:
    raise SystemExit("Garris declared signer counts drift")
if meta.get("default_app_evidence_kind") != "public_coalition_action" or meta.get("default_app_weight") != 3:
    raise SystemExit("Garris default app semantics drift")

combined_boundary = " ".join(
    str(meta.get(key, ""))
    for key in ("scoring_rule", "identity_rule", "interpretive_boundary", "same_name_warning")
).lower()
for phrase in (
    "specific letter",
    "does not by itself establish national partnership",
    "generic ideological label",
    "same-name matching alone is insufficient",
    "jeff white",
):
    if phrase not in combined_boundary:
        raise SystemExit(f"Garris evidence boundary missing: {phrase}")

letters = {row["letter_id"]: row for row in garris.get("letters", [])}
if set(letters) != {"garris-letter-1", "garris-letter-2"}:
    raise SystemExit(f"Garris letter set drift: {sorted(letters)}")

expected = {
    "garris-letter-1": {
        "count": 60,
        "event_id": "evt-garris-letter-1",
        "source_id": "src-garris-letter-1",
    },
    "garris-letter-2": {
        "count": 21,
        "event_id": "evt-garris-letter-2",
        "source_id": "src-garris-letter-2",
    },
}

resolved_rows = {}
resolved_counts = {}
for letter_id, spec in expected.items():
    letter = letters[letter_id]
    if letter.get("event_id") != spec["event_id"] or letter.get("source_id") != spec["source_id"]:
        raise SystemExit(f"{letter_id}: event/source boundary drift")
    signers = letter.get("signers", [])
    if len(signers) != spec["count"]:
        raise SystemExit(f"{letter_id}: signer count drift: {len(signers)}")
    if [row.get("print_order") for row in signers] != list(range(1, spec["count"] + 1)):
        raise SystemExit(f"{letter_id}: print order must remain complete and contiguous")
    if len({row.get("name_as_printed") for row in signers}) != spec["count"]:
        raise SystemExit(f"{letter_id}: duplicate printed signer name unexpectedly introduced")

    event = event_by_id.get(spec["event_id"])
    if not event:
        raise SystemExit(f"{letter_id}: app event missing")
    note = event.get("notes", "").lower()
    if "specific public action only" not in note or "generic ideological label" not in note:
        raise SystemExit(f"{letter_id}: app event no-inference note missing")

    resolved = [row for row in signers if row.get("normalized_person_id")]
    resolved_counts[letter_id] = len(resolved)
    if letter_id == "garris-letter-1" and len(resolved) < 23:
        raise SystemExit(f"Letter 1 canonical coverage regressed below 23: {len(resolved)}")
    if letter_id == "garris-letter-2" and len(resolved) != 21:
        raise SystemExit(f"Letter 2 must remain fully canonical: {len(resolved)}/21")

    for row in resolved:
        person_id = row["normalized_person_id"]
        if person_id not in people_by_id:
            raise SystemExit(f"{letter_id}:{row['print_order']}: missing canonical person {person_id}")
        key = (person_id, spec["event_id"])
        if key in resolved_rows:
            raise SystemExit(f"duplicate resolved signer/event pair: {key}")
        resolved_rows[key] = (letter_id, row, spec)

# Every resolved signer has exactly one score-bearing public-letter app edge,
# and no app Garris signer edge exists without a resolved source row.
garris_event_ids = {spec["event_id"] for spec in expected.values()}
app_garris = [
    aff for aff in affiliations
    if aff.get("target_type") == "event" and aff.get("target_id") in garris_event_ids
]
app_by_pair = {}
for aff in app_garris:
    key = (aff.get("person_id"), aff.get("target_id"))
    app_by_pair.setdefault(key, []).append(aff)

for key, (letter_id, row, spec) in resolved_rows.items():
    matches = app_by_pair.get(key, [])
    if len(matches) != 1:
        raise SystemExit(f"{letter_id}:{row['print_order']}: expected one app edge, found {len(matches)}")
    aff = matches[0]
    if "Signer" not in aff.get("role", ""):
        raise SystemExit(f"{aff['id']}: signer role drift")
    if aff.get("confidence") != "confirmed":
        raise SystemExit(f"{aff['id']}: signer confidence drift")
    if aff.get("evidence_kind") != "public_coalition_action":
        raise SystemExit(f"{aff['id']}: signer evidence-kind drift")
    if aff.get("weight") != 3 or aff.get("score_included") is not True:
        raise SystemExit(f"{aff['id']}: signer scoring drift")
    if spec["source_id"] not in aff.get("source_ids", []):
        raise SystemExit(f"{aff['id']}: primary letter source missing")

extra_pairs = set(app_by_pair) - set(resolved_rows)
if extra_pairs:
    raise SystemExit(f"Garris app edges without resolved normalized rows: {sorted(extra_pairs)}")

# The two printed Jeff White rows are intentionally not merged by name.
letter1_jeff = next(row for row in letters["garris-letter-1"]["signers"] if row["name_as_printed"] == "Jeff White")
letter2_jeff = next(row for row in letters["garris-letter-2"]["signers"] if row["name_as_printed"] == "Jeff White")
if letter1_jeff.get("normalized_person_id") is not None:
    raise SystemExit("Letter 1 Jeff White must remain unresolved absent independent New City/Rio Grande identity evidence")
if letter2_jeff.get("normalized_person_id") != "jeff-white-redeemer-downtown":
    raise SystemExit("Letter 2 Jeff White reviewed identity drift")
if letter1_jeff.get("institution_as_printed") != "New City Fellowship" or letter1_jeff.get("presbytery_as_printed") != "Rio Grande":
    raise SystemExit("Letter 1 Jeff White printed context drift")
if letter2_jeff.get("institution_as_printed") != "Redeemer Downtown" or letter2_jeff.get("presbytery_as_printed") != "Metro NY":
    raise SystemExit("Letter 2 Jeff White printed context drift")

# Reviewed Letter 2 identity receipt remains identity-only and source-specific.
if receipt.get("receipt_id") != "2024-garris-letter2-identity-evidence-2026-09-14":
    raise SystemExit("Letter 2 identity receipt id drift")
if len(receipt.get("evidence", [])) != 19:
    raise SystemExit("Letter 2 identity receipt should retain 19 targeted corroboration records")
if receipt.get("applied_identity_count") != 7:
    raise SystemExit("Letter 2 reviewed canonical-seed count drift")
for item in receipt.get("evidence", []):
    if not item.get("source_url") or not item.get("evidence_summary") or not item.get("source_kind"):
        raise SystemExit(f"Letter 2 identity evidence incomplete at print order {item.get('letter_print_order')}")
for order in (2, 4, 6, 7, 18, 19, 20):
    item = next(row for row in receipt["evidence"] if row["letter_print_order"] == order)
    if item.get("review_state") != "applied_canonical_seed" or not item.get("applied_canonical_id"):
        raise SystemExit(f"Letter 2 reviewed seed not applied at print order {order}")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "letter_1_total": 60,
    "letter_1_canonical": resolved_counts["garris-letter-1"],
    "letter_2_total": 21,
    "letter_2_canonical": resolved_counts["garris-letter-2"],
    "app_signer_edges": len(app_garris),
    "signer_weight": 3,
    "letter1_jeff_white": "unresolved",
    "letter2_jeff_white": letter2_jeff["normalized_person_id"],
}, indent=2))
