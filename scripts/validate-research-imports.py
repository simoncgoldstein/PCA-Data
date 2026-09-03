#!/usr/bin/env python3
"""Validate source-saturation imports that live outside the core data schema."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
errors: list[str] = []
notes: list[str] = []


def load(relative: str):
    path = root / relative
    if not path.exists():
        errors.append(f"missing file: {relative}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {relative}: {exc}")
        return {}


people = {p["id"] for p in load("data/people.json")}
presbyteries = {p["id"] for p in load("data/presbyteries.json")}
churches = {p["id"] for p in load("data/churches.json")}


def validate_roster(relative: str, row_key: str, count: int, order_key: str) -> None:
    data = load(relative)
    rows = data.get(row_key, [])
    if len(rows) != count:
        errors.append(f"{relative}: expected {count} rows, found {len(rows)}")
    orders = [row.get(order_key) for row in rows]
    if orders != list(range(1, count + 1)):
        errors.append(f"{relative}: {order_key} is not consecutive 1..{count}")
    for order, row in enumerate(rows, 1):
        person_id = row.get("normalized_person_id")
        if person_id and person_id not in people:
            errors.append(f"{relative}:{order}: unknown normalized_person_id {person_id}")
        if "presbytery_as_printed" in row and not row.get("presbytery_as_printed"):
            errors.append(f"{relative}:{order}: blank presbytery_as_printed")
    source = data.get("metadata", {}).get("primary_source")
    if source and not source.startswith("https://"):
        errors.append(f"{relative}: primary_source must use https")


validate_roster("sources/normalized/revoice/warhurst-protest-signers-2019.json", "signers", 203, "print_order")
validate_roster("sources/normalized/revoice/overture-15-minority-report-signers-2022.json", "signers", 46, "print_order")
validate_roster("sources/normalized/revoice/overture-15-negative-votes-2022.json", "negative_votes", 199, "print_order")
validate_roster("sources/normalized/nae/withdrawal-protest-signers-2022.json", "signers", 203, "print_order")
validate_roster("sources/normalized/general-assembly/2021-overture-37-minority-report-signers.json", "signers", 28, "print_order")
validate_roster("sources/normalized/public-statements/a-faithful-pca/signers-2022-03-14.json", "signers", 737, "sequence_number")
validate_roster("sources/normalized/public-statements/a-faithful-pca/signers-2021-06-11.json", "signers", 571, "sequence")

ratification = load("sources/normalized/revoice/overture-15-presbytery-ratification-2023.json")
votes = ratification.get("presbytery_votes", [])
if len(votes) != 88 or [r.get("print_order") for r in votes] != list(range(1, 89)):
    errors.append("overture-15-presbytery-ratification-2023: expected 88 consecutive rows")
if sum(r.get("reported") is True for r in votes) != 68:
    errors.append("overture-15-presbytery-ratification-2023: expected 68 reporting rows")
if sum(r.get("passed") is True for r in votes) != 39 or sum(r.get("not_passed") is True for r in votes) != 29:
    errors.append("overture-15-presbytery-ratification-2023: official result mismatch")
for row in votes:
    if row.get("presbytery_id") and row["presbytery_id"] not in presbyteries:
        errors.append(f"ratification:{row.get('print_order')}: unknown presbytery_id {row['presbytery_id']}")

comparison = load("sources/normalized/public-statements/a-faithful-pca/snapshot-comparison-2021-06-11-to-2022-03-14.json")
cm = comparison.get("metadata", {})
if (cm.get("snapshot_a_rows"), cm.get("snapshot_b_rows")) != (571, 737):
    errors.append("A Faithful PCA comparison: snapshot counts changed")
notes.append(f"A Faithful PCA comparison: {cm.get('shared_identity_keys')} shared keys, {cm.get('added_identity_keys')} added keys, {cm.get('removed_identity_keys')} removed keys, {cm.get('collision_keys_requiring_review')} collision keys")

np_data = load("sources/normalized/national-partnership/combined-archive-extraction-v1.json")
if len(np_data.get("addition_snapshots", [])) != 31:
    errors.append("National Partnership: expected 31 genuine Additions headings in preserved archive")
if len(np_data.get("priority_issue_action_excerpts", [])) < 600:
    errors.append("National Partnership: priority issue/action extraction unexpectedly sparse")
members = load("sources/normalized/national-partnership/confirmed-memberships-canonical.json").get("confirmed_members", [])
if len(members) != 151:
    errors.append(f"National Partnership: expected 151 canonical printed-name memberships, found {len(members)}")

church_meta = load("sources/normalized/church-directory/canonicalization-metadata.json")
if not church_meta:
    church_meta = load("sources/normalized/church-directory/import-metadata.json")
if len(churches) != 1970:
    errors.append(f"church backbone: expected 1970 canonical churches, found {len(churches)}")
ffo = load("sources/normalized/crosswalks/save-the-pca-ffo-2026-02-08/match-metadata.json")
if ffo.get("match_counts") != {"auto_matched": 143, "unmatched": 4}:
    errors.append(f"FFO crosswalk counts changed: {ffo.get('match_counts')}")
crosswalk = load("sources/normalized/crosswalks/save-the-pca-ffo-2026-02-08/ffo-church-crosswalk.json")
for row in crosswalk:
    if row.get("matched_church_id") and row["matched_church_id"] not in churches:
        errors.append(f"FFO row {row.get('ffo_source_row')}: unknown matched_church_id {row['matched_church_id']}")

hashes = {
    "sources/raw/national-partnership/NPP_Emails_2013_2021.pdf": "d1558fb3b4be92aa2d43b4537ee198ab4feea0036d0b6c09f6470047600d53cd",
    "sources/raw/national-partnership/NPP_Emails_2013_2021.txt": "653d5e9ebae4ee48ce0011125883a25c3c2f7d3e5ce14c360dca583cc0998f24",
    "sources/raw/external-datasets/save-the-pca-ffo/ffo_public_dataset_020826.xlsx": "b746fbdd1ccbb6087feeb6ed5abee91b4ac203a3cacc08de167c46a8cf9d0150",
}
for relative, expected in hashes.items():
    path = root / relative
    if not path.exists():
        errors.append(f"missing raw source: {relative}")
        continue
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        errors.append(f"raw source hash mismatch: {relative}: {actual}")

institutions = load("sources/normalized/institutions/current-role-snapshots-2026-09-03.json")
roles = institutions.get("roles", [])
coverage = institutions.get("coverage", [])
if len(coverage) != 14:
    errors.append(f"institution snapshots: expected 14 organizations, found {len(coverage)}")
if len(roles) < 350:
    errors.append(f"institution snapshots: expected at least 350 neutral role records, found {len(roles)}")
for index, row in enumerate(roles, 1):
    if row.get("ideological_weight") != 0:
        errors.append(f"institution role {index}: ideological_weight must be zero")
    if not str(row.get("source_url", "")).startswith("https://"):
        errors.append(f"institution role {index}: invalid source URL")
    person_id = row.get("normalized_person_id")
    if person_id and person_id not in people:
        errors.append(f"institution role {index}: unknown normalized_person_id {person_id}")

amr = load("sources/normalized/amr/blog-index-2023-2026.json")
amr_items = amr.get("items", [])
if len(amr_items) != 120 or len({row.get("url") for row in amr_items}) != 120:
    errors.append("AMR blog index: expected 120 unique website items")
amr_manifest = load("sources/raw/media/amr/blog-pages-2026-09-03/manifest.json")
if len(amr_manifest.get("pages", [])) != 13:
    errors.append("AMR raw archive: expected home plus 12 preserved pagination pages")
for receipt in amr_manifest.get("pages", []):
    path = root / receipt["local_file"]
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
        errors.append(f"AMR raw page missing or hash mismatch: {receipt.get('local_file')}")

revoice_manifest = load("sources/raw/issues/revoice/documents/manifest.json")
if len(revoice_manifest.get("documents", [])) != 7:
    errors.append("Revoice/Missouri archive: expected seven preserved PDFs")
for receipt in revoice_manifest.get("documents", []):
    path = root / "sources/raw/issues/revoice/documents" / receipt["file"]
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
        errors.append(f"Revoice raw document missing or hash mismatch: {receipt.get('file')}")

if errors:
    print(f"Research import validation failed with {len(errors)} error(s):", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Validated research imports: P0 rosters and source families plus P1 institution roles, AMR blog archive, and Revoice/Missouri documents.")
for note in notes:
    print(f"- {note}")
