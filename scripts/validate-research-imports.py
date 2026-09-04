#!/usr/bin/env python3
"""Validate source-saturation imports that live outside the core data schema."""

from __future__ import annotations

import csv
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
    "sources/raw/person-leads/andrew-augenstein/overture-15-negative-vote-page-80-user-supplied.png": "d5d440f334334b4730d163acf760f9c2aa4f28cdd8f432a8a155897ce28c6397",
    "sources/raw/person-leads/andrew-augenstein/lake-nona-leadership-2026-09-03.html": "c9f4dd274a903b8ebbbea2c727abb5896170dc2ea2a76e88531d828409ebb8d1",
    "sources/raw/media/jude3pca/home-2026-09-03.html": "eb5691757fa0dd417edfd2f55c81d3c785f78a101a81d7c63b9c4cefb25e9935",
    "sources/raw/media/pcapolity/home-2026-09-03.html": "307a7070c0830c5dcb31112100be8677fd3108ba51039f4f8dde8d267d281467",
    "sources/raw/media/pcapolity/secret-caucuses-2022-01-28.html": "9d0dad6baf7ab5d4f40bc6349f85c5883b089c52c2a08447c1efb610fa0b576a",
    "sources/raw/publications/co-laborers-co-heirs/screenshots/chapters-01-13.png": "41e211ba3d1abef04a949eae9d8ff44a5e3156279355b4a01d480cf58240900a",
    "sources/raw/publications/co-laborers-co-heirs/screenshots/chapters-14-26.png": "2a86ec913b05efa168c77feb31ec82fc82d137616b7ee35c88e48cb832c9f4b6",
    "sources/raw/publications/heal-us-emmanuel/screenshots/chapters-01-15.png": "673646efee0055faae181d4093049b51f8791d53024de0d056680ebd5afe64ff",
    "sources/raw/publications/heal-us-emmanuel/screenshots/chapters-16-30.png": "ce1283b905040da4cc201413ce838eac4db1822ef4dabb9a29e1cbd0f670d53c",
    "sources/raw/publications/hear-us-emmanuel/screenshots/chapters-01-15.png": "edd6258142dbb5fe8fd02ad22eed79c76674aced9213ec8db4257854406d5eb9",
    "sources/raw/publications/hear-us-emmanuel/screenshots/chapters-16-28.png": "0c3898c327a6febdd10a803bf4bdf3c20ab10f3cbea8dae170511df2f74fe081",
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

substack = load("sources/normalized/amr/substack-index-2023-2026.json")
substack_items = substack.get("items", [])
if len(substack_items) != 133 or len({row.get("stable_item_id") for row in substack_items}) != 133:
    errors.append("AMR Substack index: expected 133 unique archive/feed items")
if len({row.get("url") for row in substack_items}) != len(substack_items):
    errors.append("AMR Substack index: duplicate canonical URL")
if sum(row.get("source_visibility") == "rss_feed_only_podcast_companion" for row in substack_items) != 5:
    errors.append("AMR Substack index: expected five RSS-only podcast companions")
substack_manifest = load("sources/raw/media/amr/substack-2026-09-03/manifest.json")
if substack_manifest.get("item_count") != 133:
    errors.append("AMR Substack manifest: expected 133 normalized items")
for receipt in substack_manifest.get("receipts", []):
    path = root / receipt["local_file"]
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
        errors.append(f"AMR Substack receipt missing or hash mismatch: {receipt.get('local_file')}")

youtube = load("sources/normalized/amr/youtube-index-2023-2026.json")
youtube_items = youtube.get("items", [])
if len(youtube_items) != 31 or len({row.get("video_id") for row in youtube_items}) != 31:
    errors.append("AMR YouTube index: expected 31 unique videos")
if any(row.get("caption_status") != "available_archived" or not row.get("caption_receipts") for row in youtube_items):
    errors.append("AMR YouTube index: every captured video should retain an English caption receipt")
youtube_participants = [
    participant
    for row in youtube_items
    for participant in row.get("participants_as_stated", [])
]
allowed_youtube_roles = {"participant", "panelist", "interviewer", "guest", "featured_speaker"}
if len(youtube_participants) != 83:
    errors.append(f"AMR YouTube index: expected 83 stated participant appearances, found {len(youtube_participants)}")
if len({row.get("name_as_printed") for row in youtube_participants}) != 40:
    errors.append("AMR YouTube index: expected 40 unique stated participant names")
if sum(bool(row.get("participants_as_stated")) for row in youtube_items) != 30:
    errors.append("AMR YouTube index: expected stated participants for 30 of 31 videos")
for index, row in enumerate(youtube_items, 1):
    participants = row.get("participants_as_stated", [])
    if participants and row.get("participant_evidence") != "official title, description, or opening caption passage":
        errors.append(f"AMR YouTube item {index}: missing bounded participant evidence note")
    for participant in participants:
        if not participant.get("name_as_printed"):
            errors.append(f"AMR YouTube item {index}: blank participant name")
        if participant.get("role_in_item") not in allowed_youtube_roles:
            errors.append(f"AMR YouTube item {index}: invalid participant role {participant.get('role_in_item')}")
youtube_manifest = load("sources/raw/media/amr/youtube-2026-09-03/manifest.json")
if youtube_manifest.get("video_count") != 31 or youtube_manifest.get("captioned_video_count") != 31:
    errors.append("AMR YouTube manifest: expected 31 videos with 31 captioned videos")
for receipt in youtube_manifest.get("receipts", []):
    path = root / receipt["local_file"]
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
        errors.append(f"AMR YouTube receipt missing or hash mismatch: {receipt.get('local_file')}")
for row in youtube_items:
    for relative in row.get("caption_receipts", []):
        path = root / relative
        if not path.exists() or not path.read_bytes().startswith(b"WEBVTT"):
            errors.append(f"AMR YouTube caption is missing or not VTT: {relative}")

cross_platform = load("sources/normalized/amr/cross-platform-content-map-2023-2026.json")
groups = cross_platform.get("groups", [])
if len(groups) != 112:
    errors.append(f"AMR cross-platform map: expected 112 exact-title groups, found {len(groups)}")
known_platform_ids = {
    *(row.get("stable_item_id") for row in substack_items),
    *(row.get("stable_item_id") for row in youtube_items),
    *(f"website-{index}" for index in range(1, len(amr_items) + 1)),
}
for group in groups:
    if len(set(group.get("platforms", []))) < 2:
        errors.append(f"AMR cross-platform group is not cross-platform: {group.get('title_key')}")
    for item in group.get("items", []):
        if item.get("stable_item_id") not in known_platform_ids:
            errors.append(f"AMR cross-platform group has unknown item: {item.get('stable_item_id')}")

revoice_manifest = load("sources/raw/issues/revoice/documents/manifest.json")
if len(revoice_manifest.get("documents", [])) != 7:
    errors.append("Revoice/Missouri archive: expected seven preserved PDFs")
for receipt in revoice_manifest.get("documents", []):
    path = root / "sources/raw/issues/revoice/documents" / receipt["file"]
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != receipt["sha256"]:
        errors.append(f"Revoice raw document missing or hash mismatch: {receipt.get('file')}")

augenstein = load("sources/normalized/person-leads/andrew-augenstein-source-assessment-2026-09-03.json")
verified = augenstein.get("verified_records", [])
if len(verified) != 4:
    errors.append(f"Andrew Augenstein assessment: expected 4 verified records, found {len(verified)}")
for excluded_key in ("third_party_claims", "media_recovery", "excluded_marker"):
    if excluded_key in augenstein:
        errors.append(f"Andrew Augenstein assessment: unverified field must be absent: {excluded_key}")

publication_contributors = load("data/publication_contributors.json")
publication_by_id = {row.get("publication_id"): row for row in publication_contributors}
expected_chapters = {
    "heal-us-emmanuel-2016": 30,
    "hear-us-emmanuel-2020": 28,
    "co-laborers-co-heirs-2019": 26,
}
for publication_id, expected in expected_chapters.items():
    chapters = publication_by_id.get(publication_id, {}).get("chapter_contributors", [])
    if len(chapters) != expected or [row.get("chapter") for row in chapters] != list(range(1, expected + 1)):
        errors.append(f"{publication_id}: expected {expected} consecutive screenshot-verified chapters")
heal = publication_by_id.get("heal-us-emmanuel-2016", {})
if "Jonathan Seda" not in heal.get("contributors", []) or "Jonathan Edgar" in heal.get("contributors", []):
    errors.append("Heal Us, Emmanuel: chapter 29 screenshot correction must remain Jonathan Seda")

ruf_transitions = load("sources/normalized/institutions/ruf/role-transitions-2026.json")
ruf_events = ruf_transitions.get("events", [])
if len(ruf_events) != 213 or ruf_transitions.get("metadata", {}).get("record_count") != 213:
    errors.append(f"RUF transitions: expected 213 events, found {len(ruf_events)}")
expected_ruf_event_counts = {"started_role": 129, "transitioned_role": 10, "ended_role": 74}
actual_ruf_event_counts = {key: sum(row.get("event_type") == key for row in ruf_events) for key in expected_ruf_event_counts}
if actual_ruf_event_counts != expected_ruf_event_counts:
    errors.append(f"RUF transitions: unexpected event counts {actual_ruf_event_counts}")
if len({row.get("event_id") for row in ruf_events}) != len(ruf_events):
    errors.append("RUF transitions: event IDs must be unique")
for row in ruf_events:
    if row.get("ideological_weight") != 0:
        errors.append(f"RUF transition {row.get('event_id')}: institutional service must have zero ideological weight")
    if not row.get("name_as_printed") or not row.get("source_line") or not row.get("source_url"):
        errors.append(f"RUF transition {row.get('event_id')}: source fidelity field missing")
    if row.get("source_class_as_printed") in {"2026 departing Campus Ministers and Campus Staff", "2026 departing Interns and Fellows"}:
        if row.get("role_as_printed") is not None or row.get("campus_as_printed") is not None:
            errors.append(f"RUF transition {row.get('event_id')}: departure source must not infer exact role or campus")
cmda = [row for row in ruf_events if row.get("source_class_as_printed") == "2026 new Campus Ministers, Directors, and Assistants"]
if len(cmda) != 20 or any(row.get("role_as_printed") is not None or not row.get("campus_as_printed") for row in cmda):
    errors.append("RUF transitions: combined minister/director/assistant class must preserve campus without inventing exact roles")
if len([row for row in ruf_events if row.get("name_as_printed") == "Tyler Luehrs"]) != 2:
    errors.append("RUF transitions: duplicate Tyler Luehrs source rows must remain preserved")
for required_name in ("Niko Fanin", "Niko Fannin", "Aiden Tuberville", "AidenTuberville", "Mike Park / Mike S. Park", "Matt Terrell", "Joy Beans"):
    if not any(row.get("name_as_printed") == required_name for row in ruf_events):
        errors.append(f"RUF transitions: preserved source form missing: {required_name}")

ruf_catalog = load("sources/normalized/institutions/ruf/campus-role-snapshot-2025-10-01.json")
ruf_catalog_roles = ruf_catalog.get("roles", [])
expected_ruf_catalog_role_counts = {
    "Campus Minister": 151,
    "Interns": 151,
    "Campus Staff": 75,
    "Associate Campus Minister": 10,
    "Campus Associate": 9,
    "Campus Assistant": 6,
    "Fellows": 6,
    "Fellow": 5,
    "Campus Minister Assistant": 1,
}
if len(ruf_catalog_roles) != 414 or ruf_catalog.get("metadata", {}).get("record_count") != 414:
    errors.append(f"RUF campus catalog: expected 414 role rows, found {len(ruf_catalog_roles)}")
if ruf_catalog.get("metadata", {}).get("snapshot_date") != "2025-10-01":
    errors.append("RUF campus catalog: snapshot date must remain 2025-10-01")
if ruf_catalog.get("metadata", {}).get("campus_count") != 162:
    errors.append("RUF campus catalog: expected 162 TOC-linked campus entries")
ruf_catalog_coverage = ruf_catalog.get("coverage", {})
if ruf_catalog_coverage.get("ruf_campus_entries") != 138 or ruf_catalog_coverage.get("ruf_international_entries") != 24:
    errors.append("RUF campus catalog: expected 138 RUF and 24 RUF International campus entries")
actual_ruf_catalog_role_counts = {
    role: sum(row.get("role_as_printed") == role for row in ruf_catalog_roles)
    for role in expected_ruf_catalog_role_counts
}
if actual_ruf_catalog_role_counts != expected_ruf_catalog_role_counts:
    errors.append(f"RUF campus catalog: unexpected role counts {actual_ruf_catalog_role_counts}")
if len({row.get("name_as_printed") for row in ruf_catalog_roles}) != 414:
    errors.append("RUF campus catalog: expected 414 unique printed person names")
for index, row in enumerate(ruf_catalog_roles, 1):
    if row.get("ideological_weight") != 0:
        errors.append(f"RUF campus catalog row {index}: institutional service must have zero ideological weight")
    if not row.get("name_as_printed") or not row.get("campus_as_printed") or not row.get("catalog_page") or not row.get("source_url"):
        errors.append(f"RUF campus catalog row {index}: source fidelity field missing")

ruf_catalog_receipt = load("sources/raw/institutions/ruf/campus-catalog-2025-10-01/receipt.json")
if ruf_catalog_receipt.get("pdf_sha256") != "c9556efc40756f77466f1960437c19933d20f29b044e1082f0d743ff77457509":
    errors.append("RUF campus catalog: official PDF SHA-256 drift")
if ruf_catalog_receipt.get("pdf_pages") != 390 or ruf_catalog_receipt.get("role_row_count") != 414:
    errors.append("RUF campus catalog: receipt page/role counts drift")


identity = load("sources/normalized/identity/person-crosswalk.json")
identity_rows = identity.get("records", [])
allowed_statuses = {"exact_confirmed", "context_confirmed", "probable_requires_review", "ambiguous", "collision", "unmatched"}
if len(identity_rows) < 2700:
    errors.append(f"identity crosswalk unexpectedly sparse: {len(identity_rows)} rows")
seen_crosswalk_ids: set[str] = set()
seen_source_rows: set[tuple[str, str]] = set()
for row in identity_rows:
    crosswalk_id = row.get("crosswalk_id")
    source_key = (row.get("source_dataset"), row.get("source_row_locator"))
    if not crosswalk_id or crosswalk_id in seen_crosswalk_ids:
        errors.append(f"identity crosswalk duplicate/missing ID: {crosswalk_id}")
    seen_crosswalk_ids.add(crosswalk_id)
    if source_key in seen_source_rows:
        errors.append(f"identity crosswalk source row maps more than once: {source_key}")
    seen_source_rows.add(source_key)
    if not row.get("name_as_printed"):
        errors.append(f"identity {crosswalk_id}: printed name lost")
    if row.get("match_status") not in allowed_statuses:
        errors.append(f"identity {crosswalk_id}: unsupported match status")
    person_id = row.get("canonical_person_id")
    if person_id and person_id not in people:
        errors.append(f"identity {crosswalk_id}: nonexistent person ID {person_id}")
    if person_id and row.get("match_status") not in {"exact_confirmed", "context_confirmed"}:
        errors.append(f"identity {crosswalk_id}: unresolved/collision row received person ID")
    if row.get("match_status") in {"ambiguous", "collision"} and person_id:
        errors.append(f"identity {crosswalk_id}: confirmed collision key")
identity_summary = load("sources/normalized/identity/summary.json")
if sum(identity_summary.get("overall_match_status_counts", {}).values()) != len(identity_rows):
    errors.append("identity summary status counts do not equal crosswalk row count")
identity_record_count = identity_summary.get("metadata", {}).get("record_count")
if identity_record_count != len(identity_rows):
    errors.append(f"identity summary record_count mismatch: metadata={identity_record_count} crosswalk={len(identity_rows)}")
if len(identity_rows) < 2799:
    errors.append(f"identity crosswalk regressed below established 2,799-row baseline: {len(identity_rows)} rows")
identity_datasets = identity_summary.get("datasets", [])
if len(identity_datasets) < 28:
    errors.append(f"identity summary regressed below established 28 source-bounded datasets: {len(identity_datasets)}")
if len({row.get("source_dataset") for row in identity_datasets}) != len(identity_datasets):
    errors.append("identity summary contains duplicate source-dataset entries")
ruf_identity_summary = next((row for row in identity_datasets if row.get("source_dataset") == "ruf_staff_transitions_2026"), None)
if not ruf_identity_summary or ruf_identity_summary.get("row_count") != 213:
    errors.append("identity summary: expected 213 RUF 2026 staff-transition rows")
ruf_catalog_identity_summary = next((row for row in identity_datasets if row.get("source_dataset") == "ruf_campus_catalog_2025"), None)
if not ruf_catalog_identity_summary or ruf_catalog_identity_summary.get("row_count") != 414:
    errors.append("identity summary: expected 414 RUF 2025 campus-catalog rows")
amr_youtube_summary = next(
    (row for row in identity_summary.get("datasets", []) if row.get("source_dataset") == "amr_youtube_media_2023_2026"),
    None,
)
if not amr_youtube_summary or amr_youtube_summary.get("row_count") != 83:
    errors.append("identity summary: expected 83 AMR YouTube participant rows")
afp_2022 = load("sources/normalized/public-statements/a-faithful-pca/signers-2022-03-14.json").get("signers", [])
if afp_2022 and (afp_2022[5].get("name_as_printed") != "Rev. Steve Brown" or afp_2022[5].get("normalized_person_id") is not None):
    errors.append("A Faithful PCA signature 6 must not carry Andrew Augenstein's ID")
if len(afp_2022) >= 477 and afp_2022[476].get("normalized_person_id") != "andrew-augenstein":
    errors.append("A Faithful PCA signature 477 should resolve to Andrew Augenstein")

overlap_files = [
    "analysis/overlap/dataset-coverage.json",
    "analysis/overlap/pairwise-overlap.csv",
    "analysis/overlap/pairwise-shared-people.json",
    "analysis/overlap/person-recurrence.csv",
    "analysis/overlap/presbytery-concentration.csv",
    "analysis/overlap/church-concentration.csv",
    "analysis/overlap/institutional-pipelines.json",
    "analysis/overlap/graph-quality.json",
]
for relative in overlap_files:
    if not (root / relative).exists():
        errors.append(f"missing overlap output: {relative}")
pairwise_path = root / "analysis/overlap/pairwise-overlap.csv"
if pairwise_path.exists():
    with pairwise_path.open(encoding="utf-8", newline="") as handle:
        pairwise = list(csv.DictReader(handle))
    dataset_count = len(identity_summary.get("datasets", []))
    if len(pairwise) != dataset_count * (dataset_count - 1) // 2:
        errors.append(f"pairwise overlap: expected all dataset pairs, found {len(pairwise)}")
    for row in pairwise:
        if float(row.get("jaccard_similarity", -1)) < 0 or float(row.get("jaccard_similarity", 2)) > 1:
            errors.append(f"pairwise overlap invalid Jaccard: {row.get('dataset_a')} / {row.get('dataset_b')}")
graph_quality = load("analysis/overlap/graph-quality.json")
if graph_quality.get("quality_gaps", {}).get("unresolved_identity_rows") != sum(
    count for status, count in identity_summary.get("overall_match_status_counts", {}).items()
    if status not in {"exact_confirmed", "context_confirmed"}
):
    errors.append("graph quality unresolved-identity count is inconsistent with identity summary")

if errors:
    print(f"Research import validation failed with {len(errors)} error(s):", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)
print("Validated research imports: P0/P1 source families, publication screenshots, identity crosswalk, and overlap analysis.")
for note in notes:
    print(f"- {note}")
