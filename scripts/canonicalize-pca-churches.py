#!/usr/bin/env python3
"""Convert source-faithful PCA KML placemarks into canonical congregation entities.

The raw KML import remains untouched under sources/normalized/church-directory/.
This script groups only the exact strong duplicate keys already identified by the
importer: same normalized name, website, presbytery, and pastor. Distinct churches
with the same generic name are never merged merely by name.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

if len(sys.argv) < 4:
    raise SystemExit(
        "usage: canonicalize-pca-churches.py <raw.json> <possible-duplicates.json> <churches.json>"
    )

raw_path = Path(sys.argv[1])
duplicates_path = Path(sys.argv[2])
out_path = Path(sys.argv[3])

records = json.loads(raw_path.read_text(encoding="utf-8"))
duplicate_groups = json.loads(duplicates_path.read_text(encoding="utf-8"))
record_by_source = {r["source_record_id"]: r for r in records}


def norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def host(value: str | None) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if not re.match(r"^https?://", value, re.I):
        value = "https://" + value
    try:
        parsed = urlparse(value)
    except ValueError:
        return norm(value)
    hostname = (parsed.hostname or "").lower()
    return hostname[4:] if hostname.startswith("www.") else hostname


def canonical_key(record: dict) -> str:
    return "|".join(
        [
            norm(record.get("name")),
            host(record.get("website")),
            norm(record.get("presbytery_as_printed")),
            norm(record.get("pastor_as_printed")),
        ]
    )

# Map each source record in an explicit duplicate group to one shared group key.
duplicate_membership = {}
for group in duplicate_groups:
    ids = group.get("source_record_ids", [])
    if len(ids) < 2:
        continue
    group_key = group["key"]
    for source_id in ids:
        duplicate_membership[source_id] = group_key

buckets: dict[str, list[dict]] = defaultdict(list)
for record in records:
    source_id = record["source_record_id"]
    if source_id in duplicate_membership:
        bucket_key = "duplicate:" + duplicate_membership[source_id]
    else:
        bucket_key = "single:" + source_id
    buckets[bucket_key].append(record)

canonical = []
for bucket_key, group_records in buckets.items():
    first = group_records[0]
    identity_basis = canonical_key(first) if bucket_key.startswith("duplicate:") else first["source_record_id"]
    digest = hashlib.sha1(identity_basis.encode("utf-8")).hexdigest()[:10]
    name_slug = re.sub(r"[^a-z0-9]+", "-", (first.get("name") or "church").lower()).strip("-")[:60]
    church_id = f"{name_slug}-{digest[:6]}"

    locations = []
    for r in group_records:
        locations.append(
            {
                "source_record_id": r.get("source_record_id"),
                "address_full": r.get("address_full"),
                "address_2": r.get("address_2"),
                "latitude": r.get("latitude"),
                "longitude": r.get("longitude"),
            }
        )

    canonical.append(
        {
            "id": church_id,
            "name": first.get("name"),
            "type": first.get("type_org") or "Church",
            "status": "current_directory_2026_08_31",
            "presbytery_id": first.get("presbytery_id"),
            "presbytery_as_printed": first.get("presbytery_as_printed"),
            "phone": first.get("phone"),
            "email": first.get("email"),
            "website": first.get("website"),
            "pastor_as_printed": first.get("pastor_as_printed"),
            "country_as_printed": first.get("country_as_printed"),
            "locations": locations,
            "source_record_ids": [r["source_record_id"] for r in group_records],
            "source_snapshot": "pca-batchgeo-kml-2026-09-03",
            "canonical_status": "canonical_exact_group" if len(group_records) > 1 else "canonical_single",
            "source_placemark_count": len(group_records),
        }
    )

canonical.sort(key=lambda c: (c["name"] or "", c["presbytery_as_printed"] or "", c["id"]))
out_path.write_text(json.dumps(canonical, indent=2) + "\n", encoding="utf-8")

metadata = {
    "raw_placemarks": len(records),
    "canonical_church_entities": len(canonical),
    "exact_duplicate_groups_collapsed": len(duplicate_groups),
    "source_placemarks_collapsed_into_existing_entities": len(records) - len(canonical),
    "rules": {
        "merge_requires_importer_exact_duplicate_group": True,
        "same_name_alone_never_merges": True,
        "all_locations_and_source_ids_preserved": True,
        "pastor_field_creates_person_node": False,
    },
}
meta_path = raw_path.parent / "canonicalization-metadata.json"
meta_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
print(json.dumps(metadata, indent=2))
