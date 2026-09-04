#!/usr/bin/env python3
"""Build a conservative, reproducible cross-dataset person identity layer.

The builder preserves every printed name, trusts only pre-existing reviewed seed
IDs, and creates new canonical IDs only when independent source families share
an exact normalized name plus a contextual disambiguator. Name similarity alone
never produces a confirmed ID.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


if len(sys.argv) not in (1, 2):
    raise SystemExit("usage: build-person-crosswalk.py [repo-root]")

ROOT = Path(sys.argv[1] if len(sys.argv) == 2 else ".").resolve()
TODAY = "2026-09-04"


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write(relative: str, value: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


HONORIFICS = {
    "rev", "reverend", "dr", "doctor", "prof", "professor", "pastor",
    "elder", "mr", "mrs", "ms", "te", "re",
}
SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}
FIRST_NAME_VARIANTS = {
    "andy": "andrew",
    "ben": "benjamin",
    "bill": "william",
    "bob": "robert",
    "bobby": "robert",
    "chris": "christopher",
    "dan": "daniel",
    "dave": "david",
    "geoff": "geoffrey",
    "greg": "gregory",
    "jeff": "jeffrey",
    "jen": "jennifer",
    "jim": "james",
    "jimmy": "james",
    "joe": "joseph",
    "jon": "jonathan",
    "ken": "kenneth",
    "matt": "matthew",
    "mike": "michael",
    "rob": "robert",
    "ron": "ronald",
    "steve": "stephen",
    "tim": "timothy",
    "tony": "anthony",
    "will": "william",
    "zack": "zachary",
}


def ascii_words(value: str) -> list[str]:
    value = value.replace("’", "'").replace("“", "").replace("”", "")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.findall(r"[a-z0-9]+", value.lower())


def normalize_name(value: str) -> str:
    words = ascii_words(value)
    while words and words[0] in HONORIFICS:
        words.pop(0)
    while words and words[-1] in SUFFIXES:
        words.pop()
    return " ".join(words)


def display_name(value: str) -> str:
    value = re.sub(
        r"^(?:(?:rev(?:erend)?|dr|doctor|prof(?:essor)?|pastor|elder|mr|mrs|ms|te|re)\.?\s*,?\s*)+",
        "",
        value.strip(),
        flags=re.I,
    )
    value = re.sub(r",?\s+(?:Jr|Sr|II|III|IV|V)\.?$", "", value, flags=re.I)
    return value.strip(" ,")


def normalize_presbytery(value: str | None) -> str | None:
    if not value:
        return None
    words = [w for w in ascii_words(value) if w != "presbytery"]
    return " ".join(words) or None


def normalize_context(value: str | None) -> str | None:
    if not value:
        return None
    words = ascii_words(value)
    return " ".join(words) or None


def normalize_office(value: str | None) -> str | None:
    if not value:
        return None
    key = normalize_context(value)
    if key in {"te", "teaching elder"}:
        return "teaching_elder"
    if key in {"re", "ruling elder"}:
        return "ruling_elder"
    return None


def slug(value: str) -> str:
    result = normalize_name(value).replace(" ", "-")
    return result or "unnamed-person"


people_all = load("data/people.json")
# IDs created by this builder are deliberately removed and regenerated so the
# process remains idempotent even after source rows have been backfilled.
seed_people = [p for p in people_all if p.get("profile_status") != "identity_crosswalk"]
seed_ids = {p["id"] for p in seed_people}
seed_by_id = {p["id"]: p for p in seed_people}

MANUAL_SEED_ALIASES = {
    "sean michael lucas": {
        "person_id": "sean-lucas",
        "note": "Full middle-name form is tied to Sean Lucas by the reviewed core profile and source-backed AMR/RTS/Independent Presbyterian Church roles.",
    },
    "duke l kwon": {
        "person_id": "duke-kwon",
        "note": "Middle-initial form is tied to Duke Kwon by matching Potomac Presbytery and Grace Meridian Hill context in official/source-audit records.",
    },
}

# Audited corrections remain in the reproducible review trail even after the
# generated source file has been cleaned, so a second run produces no drift.
REJECTED_SOURCE_ID_OVERRIDES = {
    ("a_faithful_pca_2022-03-14", "signature:6"): "andrew-augenstein",
}

seed_exact: dict[str, list[str]] = defaultdict(list)
for person in seed_people:
    seed_exact[normalize_name(person["name"])].append(person["id"])
for alias, detail in MANUAL_SEED_ALIASES.items():
    if detail["person_id"] not in seed_ids:
        raise SystemExit(f"manual alias points to unknown seed person: {detail}")


records: list[dict[str, Any]] = []
mutable_sources: dict[str, Any] = {}


def add_record(
    *,
    dataset: str,
    family: str,
    source_path: str,
    locator: str,
    printed_name: str,
    row: dict[str, Any] | None,
    source_tier: str,
    completeness: str,
    evidence_type: str,
    presbyteries: list[str] | None = None,
    institutions: list[str] | None = None,
    location: str | None = None,
    office: str | None = None,
    existing_id: str | None = None,
    backfill: bool = True,
) -> None:
    if not printed_name or not normalize_name(printed_name):
        raise ValueError(f"{dataset}:{locator}: missing printable person name")
    candidate = normalize_name(printed_name)
    valid_existing_id = None
    rejected_existing_id = REJECTED_SOURCE_ID_OVERRIDES.get((dataset, locator))
    if existing_id in seed_ids:
        seed_name_matches = candidate == normalize_name(seed_by_id[existing_id]["name"])
        manual_name_matches = MANUAL_SEED_ALIASES.get(candidate, {}).get("person_id") == existing_id
        if seed_name_matches or manual_name_matches:
            valid_existing_id = existing_id
        elif not rejected_existing_id:
            rejected_existing_id = existing_id
    records.append({
        "source_dataset": dataset,
        "source_family": family,
        "source_path": source_path,
        "source_row_locator": locator,
        "name_as_printed": printed_name,
        "normalized_candidate": candidate,
        "source_tier": source_tier,
        "completeness_status": completeness,
        "evidence_type": evidence_type,
        "presbyteries": sorted({p for p in (normalize_presbytery(x) for x in (presbyteries or [])) if p}),
        "institutions": sorted({p for p in (normalize_context(x) for x in (institutions or [])) if p}),
        "location": normalize_context(location),
        "office": normalize_office(office),
        "existing_id": valid_existing_id,
        "rejected_existing_id": rejected_existing_id,
        "_row": row if backfill else None,
    })


def register_json(relative: str) -> Any:
    data = load(relative)
    mutable_sources[relative] = data
    return data


# Official/formal rosters.
roster_specs = [
    ("warhurst_protest_2019", "warhurst_protest_2019", "sources/normalized/revoice/warhurst-protest-signers-2019.json", "signers", "print_order", "formal_protest_signature"),
    ("overture_37_minority_2021", "overture_37_minority_2021", "sources/normalized/general-assembly/2021-overture-37-minority-report-signers.json", "signers", "print_order", "minority_report_signature"),
    ("overture_15_minority_2022", "overture_15_minority_2022", "sources/normalized/revoice/overture-15-minority-report-signers-2022.json", "signers", "print_order", "minority_report_signature"),
    ("overture_15_negative_votes_2022", "overture_15_negative_votes_2022", "sources/normalized/revoice/overture-15-negative-votes-2022.json", "negative_votes", "print_order", "recorded_negative_vote"),
    ("nae_withdrawal_protest_2022", "nae_withdrawal_protest_2022", "sources/normalized/nae/withdrawal-protest-signers-2022.json", "signers", "print_order", "formal_protest_signature"),
]
for dataset, family, relative, row_key, order_key, evidence_type in roster_specs:
    data = register_json(relative)
    for row in data[row_key]:
        add_record(
            dataset=dataset,
            family=family,
            source_path=relative,
            locator=f"{order_key}:{row[order_key]}",
            printed_name=row["name_as_printed"],
            row=row,
            source_tier="official_primary",
            completeness="complete",
            evidence_type=evidence_type,
            presbyteries=[row.get("presbytery_as_printed")],
            office=row.get("office_as_printed"),
            existing_id=row.get("normalized_person_id"),
        )


# A Faithful PCA snapshots remain separate datasets but one source family.
for date, relative, order_key in [
    ("2021-06-11", "sources/normalized/public-statements/a-faithful-pca/signers-2021-06-11.json", "sequence"),
    ("2022-03-14", "sources/normalized/public-statements/a-faithful-pca/signers-2022-03-14.json", "sequence_number"),
]:
    data = register_json(relative)
    for row in data["signers"]:
        institutions = row.get("church_or_institution_as_printed", [])
        if not institutions:
            institutions = row.get("raw_lines", [])
        add_record(
            dataset=f"a_faithful_pca_{date}",
            family="a_faithful_pca",
            source_path=relative,
            locator=f"signature:{row[order_key]}",
            printed_name=row["name_as_printed"],
            row=row,
            source_tier="first_party_archive",
            completeness="complete",
            evidence_type="public_letter_signature",
            presbyteries=[row.get("presbytery_as_printed")],
            institutions=institutions,
            location=row.get("location_as_printed"),
            existing_id=row.get("normalized_person_id"),
        )


# Strict National Partnership membership table.
relative = "sources/normalized/national-partnership/confirmed-memberships-canonical.json"
np_data = register_json(relative)
for index, row in enumerate(np_data["confirmed_members"], 1):
    add_record(
        dataset="national_partnership_confirmed_members",
        family="national_partnership",
        source_path=relative,
        locator=f"confirmed_member:{index}:{row['normalized_name_key']}",
        printed_name=row["canonical_name"],
        row=row,
        source_tier="primary_archive",
        completeness="complete_explicit_membership_extraction",
        evidence_type="formal_organization_membership",
        presbyteries=[e.get("presbytery_as_printed") for e in row.get("evidence", [])],
        office=next((e.get("office_as_printed") for e in row.get("evidence", []) if e.get("office_as_printed")), None),
        existing_id=row.get("normalized_person_id"),
    )


# Current institution roles. Each organization is a separately reported roster.
relative = "sources/normalized/institutions/current-role-snapshots-2026-09-03.json"
institution_data = register_json(relative)
coverage_by_org = {x["organization_id"]: x for x in institution_data["coverage"]}
for index, row in enumerate(institution_data["roles"], 1):
    org = row["organization_id"]
    add_record(
        dataset=f"institution_{org}",
        family=f"institution_{org}",
        source_path=relative,
        locator=f"role:{index}:{org}:line:{row.get('source_line')}",
        printed_name=row["name_as_printed"],
        row=row,
        source_tier="official_institutional",
        completeness=coverage_by_org[org]["coverage_status"],
        evidence_type="institutional_role",
        institutions=[org],
        office=row.get("role_as_printed"),
        existing_id=row.get("normalized_person_id"),
    )


# Dated RUF 2026 staff transitions remain a separate event dataset.
relative = "sources/normalized/institutions/ruf/role-transitions-2026.json"
ruf_transition_data = load(relative)
for row in ruf_transition_data.get("events", []):
    institutions = ["reformed-university-fellowship"]
    if row.get("campus_as_printed"):
        institutions.append(row["campus_as_printed"])
    add_record(
        dataset="ruf_staff_transitions_2026",
        family="ruf_staff_transitions",
        source_path=relative,
        locator=row["event_id"],
        printed_name=row["name_as_printed"],
        row=None,
        source_tier="official_institutional",
        completeness="complete_official_2026_transition_announcements",
        evidence_type=f"ruf_{row['event_type']}",
        institutions=institutions,
        backfill=False,
    )


# Publication chapter rosters, now backed by archived screenshots.
relative = "data/publication_contributors.json"
publication_data = register_json(relative)
for publication in publication_data:
    publication_id = publication["publication_id"]
    for chapter in publication.get("chapter_contributors", []):
        for contributor_index, printed_name in enumerate(chapter.get("contributors", []), 1):
            add_record(
                dataset=f"publication_{publication_id}",
                family=f"publication_{publication_id}",
                source_path=relative,
                locator=f"chapter:{chapter['chapter']}:contributor:{contributor_index}",
                printed_name=printed_name,
                row=None,
                source_tier="user_supplied_visual_receipt",
                completeness="complete_visible_chapter_table",
                evidence_type="publication_contribution",
                institutions=[publication_id],
                existing_id=publication.get("known_person_links", {}).get(printed_name),
                backfill=False,
            )


# Current AMR leadership is already source-backed in the core graph.
affiliations = load("data/affiliations.json")
for row in affiliations:
    if row.get("target_type") != "organization" or row.get("target_id") != "amr":
        continue
    person = seed_by_id.get(row.get("person_id"))
    if not person:
        continue
    add_record(
        dataset="amr_leadership_current",
        family="amr_leadership",
        source_path="data/affiliations.json",
        locator=row["id"],
        printed_name=person["name"],
        row=None,
        source_tier="first_party",
        completeness="complete_current_core_leadership",
        evidence_type="formal_organization_leadership",
        institutions=["amr"],
        office=person.get("ordination"),
        existing_id=person["id"],
        backfill=False,
    )


def parse_amr_byline(value: str) -> list[str]:
    value = value.strip().strip(",")
    if not value or re.match(r"^(?:the board(?: of amr)?|the executive board|editor(?: of amr)?)$", value, re.I):
        return []
    value = re.sub(r"^by\s+", "", value, flags=re.I)
    value = re.sub(r"^reverend,\s*", "", value, flags=re.I)
    parts = re.split(r"\s*,\s*(?:and\s+)?|\s+and\s+", value)
    return [part.strip().strip(",") for part in parts if normalize_name(part)]


relative = "sources/normalized/amr/blog-index-2023-2026.json"
amr_data = load(relative)
for item_index, item in enumerate(amr_data["items"], 1):
    for contributor_index, printed_name in enumerate(parse_amr_byline(item.get("contributor_as_printed", "")), 1):
        add_record(
            dataset="amr_website_media_2023_2026",
            family="amr_media",
            source_path=relative,
            locator=f"item:{item_index}:contributor:{contributor_index}:{item['url']}",
            printed_name=printed_name,
            row=None,
            source_tier="first_party",
            completeness="complete_website_index_byline_field",
            evidence_type="media_authorship_or_participation",
            institutions=["amr"],
            backfill=False,
        )


# YouTube participants are reviewed from official titles/descriptions and, when
# necessary, opening caption passages. Platform duplication remains in the same
# AMR source family so it cannot inflate independent-family recurrence.
relative = "sources/normalized/amr/youtube-index-2023-2026.json"
amr_youtube = load(relative)
for item_index, item in enumerate(amr_youtube["items"], 1):
    for participant_index, participant in enumerate(item.get("participants_as_stated", []), 1):
        add_record(
            dataset="amr_youtube_media_2023_2026",
            family="amr_media",
            source_path=relative,
            locator=f"video:{item['video_id']}:participant:{participant_index}",
            printed_name=participant["name_as_printed"],
            row=None,
            source_tier="first_party",
            completeness="complete_public_channel_participants_where_stated",
            evidence_type="media_participation",
            institutions=["amr"],
            backfill=False,
        )


# Ensure row locators are one-to-one before matching.
locator_counts = Counter((r["source_dataset"], r["source_row_locator"]) for r in records)
duplicate_locators = [key for key, count in locator_counts.items() if count > 1]
if duplicate_locators:
    raise SystemExit(f"duplicate crosswalk locators: {duplicate_locators[:10]}")

groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
for record in records:
    groups[record["normalized_candidate"]].append(record)

first_last_groups: dict[str, set[str]] = defaultdict(set)
for key in groups:
    words = key.split()
    if len(words) >= 2:
        first_last_groups[f"{FIRST_NAME_VARIANTS.get(words[0], words[0])} {words[-1]}"].add(key)


def shared_nonempty(rows: list[dict[str, Any]], field: str) -> set[str]:
    family_values: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        values = row[field] if isinstance(row[field], list) else ([row[field]] if row[field] else [])
        family_values[row["source_family"]].update(v for v in values if v)
    families = list(family_values)
    shared: set[str] = set()
    for i, left in enumerate(families):
        for right in families[i + 1:]:
            shared.update(family_values[left] & family_values[right])
    return shared


def rows_share_context(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Return true only for a contextual match across independent families."""
    if left["source_family"] == right["source_family"]:
        return False
    if set(left["presbyteries"]) & set(right["presbyteries"]):
        return True
    if set(left["institutions"]) & set(right["institutions"]):
        return True
    return bool(left["location"] and left["location"] == right["location"])


def infer_ordination(rows: list[dict[str, Any]]) -> str | None:
    offices = {row["office"] for row in rows if row["office"]}
    if offices == {"teaching_elder"}:
        return "Teaching Elder"
    if offices == {"ruling_elder"}:
        return "Ruling Elder"
    return None


used_ids = {p["id"] for p in seed_people}
generated_people: list[dict[str, Any]] = []

for key in sorted(groups):
    rows = groups[key]
    families = {r["source_family"] for r in rows}
    datasets = {r["source_dataset"] for r in rows}
    existing_ids = {r["existing_id"] for r in rows if r["existing_id"]}
    rejected_existing_ids = {r["rejected_existing_id"] for r in rows if r["rejected_existing_id"]}
    exact_seed_ids = set(seed_exact.get(key, []))
    manual = MANUAL_SEED_ALIASES.get(key)
    if manual:
        exact_seed_ids.add(manual["person_id"])

    presbytery_support = shared_nonempty(rows, "presbyteries")
    institution_support = shared_nonempty(rows, "institutions")
    location_support = shared_nonempty(rows, "location")
    offices = {r["office"] for r in rows if r["office"]}
    office_conflict = offices == {"teaching_elder", "ruling_elder"}
    duplicate_in_dataset = any(count > 1 for count in Counter(r["source_dataset"] for r in rows).values())
    key_words = key.split()
    first_last_key = f"{FIRST_NAME_VARIANTS.get(key_words[0], key_words[0])} {key_words[-1]}" if len(key_words) >= 2 else key
    variant_conflict = len(first_last_groups.get(first_last_key, set())) > 1

    canonical_id: str | None = None
    status = "unmatched"
    method = "no_confirming_context"
    confidence = 0.0
    support: list[str] = []
    conflicts: list[str] = []
    note = "No canonical ID assigned."

    if rejected_existing_ids:
        status, method, confidence = "collision", "preexisting_id_name_mismatch", 0.0
        conflicts.append(f"stored IDs do not match printed name: {', '.join(sorted(rejected_existing_ids))}")
        note = "The mismatched stored ID is cleared and this source row requires manual review."
    elif len(existing_ids) > 1:
        status, method, confidence = "collision", "conflicting_preexisting_ids", 0.0
        conflicts.append("multiple pre-existing canonical IDs on the same normalized name")
        note = "Requires manual review; no ID was propagated."
    elif office_conflict:
        status, method, confidence = "collision", "conflicting_office_types", 0.0
        conflicts.append("both Teaching Elder and Ruling Elder appear for the same normalized name")
        note = "Office conflict prevents automatic identity resolution."
    elif existing_ids:
        canonical_id = next(iter(existing_ids))
        status, method, confidence = "exact_confirmed", "preexisting_verified_id", 1.0
        support.append("a source row already carries a reviewed core person ID")
        note = "Reviewed source-specific identity is retained and propagated only within this exact normalized-name group."
    elif manual:
        canonical_id = manual["person_id"]
        status, method, confidence = "context_confirmed", "documented_manual_alias", 0.98
        support.append("explicit documented name-form alias")
        note = manual["note"]
    elif len(exact_seed_ids) == 1 and len(families) >= 2 and (presbytery_support or institution_support):
        canonical_id = next(iter(exact_seed_ids))
        status, method, confidence = "context_confirmed", "seed_name_plus_shared_context", 0.97
        support.append("exact seed-person name")
        note = "Exact reviewed seed name plus context repeated in independent source families."
    elif len(exact_seed_ids) > 1:
        status, method, confidence = "collision", "duplicate_seed_name", 0.0
        conflicts.append("multiple seed people have the same normalized name")
        note = "Requires manual review; no ID assigned."
    elif variant_conflict:
        status, method, confidence = "ambiguous", "first_last_name_variant_collision", 0.0
        conflicts.append("multiple full-name or initial variants share this first/last-name key")
        note = "No new ID is created until the name variants are reconciled with source context."
    elif len(families) >= 2 and (presbytery_support or institution_support or location_support) and not duplicate_in_dataset:
        # This is the only automatic path that creates a new canonical person.
        preferred = max((display_name(r["name_as_printed"]) for r in rows), key=lambda x: (len(normalize_name(x).split()), len(x), x))
        candidate_id = slug(preferred)
        if candidate_id in used_ids:
            status, method, confidence = "collision", "generated_id_collision", 0.0
            conflicts.append(f"generated ID {candidate_id} is already in use")
            note = "Requires manual review; no ID assigned."
        else:
            canonical_id = candidate_id
            used_ids.add(candidate_id)
            status, method, confidence = "context_confirmed", "exact_name_plus_shared_context", 0.95
            if presbytery_support:
                support.append(f"matching presbytery: {', '.join(sorted(presbytery_support))}")
            if institution_support:
                support.append(f"matching church/institution: {', '.join(sorted(institution_support))}")
            if location_support:
                support.append(f"matching location: {', '.join(sorted(location_support))}")
            note = "Exact normalized name recurs in independent source families with a shared contextual disambiguator."
            generated_people.append({
                "id": canonical_id,
                "name": preferred,
                "ordination": infer_ordination(rows),
                "current_role": None,
                "current_organization": None,
                "denominational_status": "PCA-related role documented in tracked sources; current status not assessed",
                "current_role_source_ids": [],
                "profile_status": "identity_crosswalk",
            })
    elif len(families) >= 2:
        status, method, confidence = "probable_requires_review", "exact_name_without_disambiguator", 0.65
        note = "Exact normalized name recurs, but no shared presbytery, institution, or location is available; no ID assigned."
    elif duplicate_in_dataset:
        status, method, confidence = "ambiguous", "duplicate_name_within_dataset", 0.0
        conflicts.append("same normalized name occurs more than once within a source dataset")
        note = "Possible duplicate signer or same-name collision; no ID assigned."

    if canonical_id and canonical_id not in seed_ids and canonical_id not in {p["id"] for p in generated_people}:
        # A pre-existing source row should never point to an old generated ID;
        # those are filtered above. This guard catches unexpected drift.
        raise SystemExit(f"unaccounted canonical ID: {canonical_id}")

    for row in rows:
        row_id = canonical_id
        row_status = status
        row_method = method
        row_confidence = confidence
        row_note = note

        # A canonical ID supported by one or more anchor records is not spread
        # to a context-free row merely because its printed name is identical.
        # The row itself must either carry the reviewed seed ID, be covered by
        # an explicit manual alias, or share a disambiguator with an independent
        # source-family peer in the same exact-name group.
        if canonical_id and not row.get("existing_id") and not manual:
            if not any(rows_share_context(row, peer) for peer in rows if peer is not row):
                row_id = None
                row_status = "probable_requires_review"
                row_method = "exact_name_without_row_level_disambiguator"
                row_confidence = 0.65
                row_note = "The group has a confirmed identity, but this row lacks its own shared contextual disambiguator; no ID assigned."

        row["canonical_person_id"] = row_id
        row["match_status"] = row_status
        row["match_method"] = row_method
        row["supporting_fields"] = support if row_id else []
        row["conflicting_fields"] = conflicts
        row["confidence"] = row_confidence
        row["reviewer_note"] = row_note
        if row["_row"] is not None:
            row["_row"]["normalized_person_id"] = row_id


# First/last-name variants are review leads only; they never merge identities.
variant_review_keys = {key for key, values in first_last_groups.items() if len(values) > 1}
for row in records:
    words = row["normalized_candidate"].split()
    first_last = f"{FIRST_NAME_VARIANTS.get(words[0], words[0])} {words[-1]}" if len(words) >= 2 else row["normalized_candidate"]
    row["variant_collision_key"] = first_last if first_last in variant_review_keys else None
    row["initials_only_name"] = any(len(word) == 1 for word in words)


public_records = []
for index, row in enumerate(sorted(records, key=lambda r: (r["source_dataset"], r["source_row_locator"])), 1):
    public_records.append({
        "crosswalk_id": f"identity-row-{index:05d}",
        **{k: v for k, v in row.items() if not k.startswith("_") and k not in {"existing_id"}},
    })

status_order = ["exact_confirmed", "context_confirmed", "probable_requires_review", "ambiguous", "collision", "unmatched"]
dataset_summary = []
for dataset in sorted({r["source_dataset"] for r in public_records}):
    subset = [r for r in public_records if r["source_dataset"] == dataset]
    counts = Counter(r["match_status"] for r in subset)
    confirmed = sum(counts[s] for s in ("exact_confirmed", "context_confirmed"))
    dataset_summary.append({
        "source_dataset": dataset,
        "row_count": len(subset),
        "unique_printed_name_count": len({r["name_as_printed"] for r in subset}),
        "confirmed_canonical_person_count": len({r["canonical_person_id"] for r in subset if r["canonical_person_id"]}),
        "confirmed_row_count": confirmed,
        "match_status_counts": {status: counts.get(status, 0) for status in status_order},
        "percent_rows_resolved": round(100 * confirmed / len(subset), 2) if subset else 0.0,
        "source_tier": sorted({r["source_tier"] for r in subset}),
        "completeness_status": sorted({r["completeness_status"] for r in subset}),
    })

review_records = [
    {
        "crosswalk_id": r["crosswalk_id"],
        "source_dataset": r["source_dataset"],
        "source_row_locator": r["source_row_locator"],
        "name_as_printed": r["name_as_printed"],
        "normalized_candidate": r["normalized_candidate"],
        "match_status": r["match_status"],
        "variant_collision_key": r["variant_collision_key"],
        "initials_only_name": r["initials_only_name"],
        "conflicting_fields": r["conflicting_fields"],
        "reviewer_note": r["reviewer_note"],
    }
    for r in public_records
    if r["match_status"] in {"probable_requires_review", "ambiguous", "collision"}
    or r["variant_collision_key"]
    or r["initials_only_name"]
]

crosswalk = {
    "metadata": {
        "generated_on": TODAY,
        "record_count": len(public_records),
        "canonical_person_count": len({r["canonical_person_id"] for r in public_records if r["canonical_person_id"]}),
        "new_person_count": len(generated_people),
        "rules": {
            "name_similarity_alone_confirms_identity": False,
            "new_id_threshold": "exact normalized name in at least two independent source families plus matching presbytery, institution, or location",
            "probable_or_ambiguous_records_receive_ids": False,
            "printed_names_preserved": True,
            "sensitive_attributes_inferred": False,
        },
    },
    "records": public_records,
}
summary = {
    "metadata": crosswalk["metadata"],
    "overall_match_status_counts": dict(sorted(Counter(r["match_status"] for r in public_records).items())),
    "datasets": dataset_summary,
}
review_queue = {
    "metadata": {
        "generated_on": TODAY,
        "record_count": len(review_records),
        "rule": "Rows may appear because of unresolved status, a first/last variant collision key, or initials-only spelling. Review never implies identity.",
    },
    "records": review_records,
}

write("sources/normalized/identity/person-crosswalk.json", crosswalk)
write("sources/normalized/identity/review-queue.json", review_queue)
write("sources/normalized/identity/summary.json", summary)
write("data/people.json", seed_people + sorted(generated_people, key=lambda p: p["id"]))
for relative, data in mutable_sources.items():
    write(relative, data)

print(json.dumps({
    "crosswalk_records": len(public_records),
    "confirmed_canonical_people": crosswalk["metadata"]["canonical_person_count"],
    "new_people": len(generated_people),
    "review_queue_records": len(review_records),
    "status_counts": summary["overall_match_status_counts"],
}, indent=2))
