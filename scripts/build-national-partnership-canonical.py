#!/usr/bin/env python3
"""Build canonical confirmed NP membership and separate adjacent evidence."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: build-national-partnership-canonical.py <repo-root> <output-dir>")

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)
archive_path = root / "sources/normalized/national-partnership/combined-archive-extraction-v1.json"
archive = json.loads(archive_path.read_text(encoding="utf-8"))
people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))


def key(value: str) -> str:
    value = value.replace("’", "'")
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    value = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    value = re.sub(r"\be j\b", "ej", value)
    return value


def person_key(value: str) -> str:
    tokens = [token for token in key(value).split() if len(token) > 1]
    return f"{tokens[0]} {tokens[-1]}" if len(tokens) >= 2 else " ".join(tokens)


person_index = defaultdict(list)
for person in people:
    person_index[person_key(person["name"])].append(person["id"])

evidence = []
for item in archive["confirmed_member_name_evidence_index"]:
    for record in item["evidence"]:
        evidence.append(
            {
                "name_as_printed": item["name"],
                "evidence_type": record["evidence_type"],
                "date": record.get("date"),
                "archive_page": record.get("page"),
                "presbytery_as_printed": record.get("presbytery_as_printed"),
                "office_as_printed": record.get("title"),
                "detail": record.get("detail"),
                "source": "NPP_Emails_2013_2021.pdf",
            }
        )

# Add source-faithful hand-curated extracts not yet covered by the generic PDF parser.
csv_rules = {
    "2013-additions.csv": {"explicit_addition"},
    "2013-other-membership-evidence.csv": {"explicit_member", "explicit_representative", "network_leader"},
    "2014-additions.csv": {"explicit_addition"},
    "2014-committee-roster.csv": {"named_np_committee_roster"},
    "2014-other-membership-evidence.csv": {"explicit_member", "explicit_addition"},
    "2015-additions.csv": {"explicit_addition"},
    "2015-committee-roster.csv": {"named_partnership_man"},
    "2016-committee-roster.csv": {"named_np_committee_participant"},
}
extract_dir = root / "sources/extracts/national-partnership"
for filename, allowed in csv_rules.items():
    with (extract_dir / filename).open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("evidence_type") not in allowed or row.get("confidence") != "confirmed":
                continue
            evidence.append(
                {
                    "name_as_printed": row.get("name"),
                    "evidence_type": row.get("evidence_type"),
                    "date": row.get("evidence_date") or row.get("evidence_period"),
                    "archive_page": int(row["archive_page"]) if row.get("archive_page", "").isdigit() else None,
                    "presbytery_as_printed": row.get("presbytery"),
                    "office_as_printed": row.get("office"),
                    "detail": row.get("evidence_summary") or row.get("notes") or row.get("committee_or_agency"),
                    "source": filename,
                }
            )

# Explicitly named membership/continuation statements in issue-action extracts.
for filename in ["2017-issue-actions.csv", "2021-issue-actions.csv"]:
    with (extract_dir / filename).open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("action_type") not in {"explicit_np_member", "explicit_np_continuation"}:
                continue
            evidence.append(
                {
                    "name_as_printed": row.get("subject_or_person"),
                    "evidence_type": row.get("action_type"),
                    "date": row.get("evidence_date"),
                    "archive_page": int(row["archive_page"]) if row.get("archive_page", "").isdigit() else None,
                    "presbytery_as_printed": None,
                    "office_as_printed": None,
                    "detail": row.get("evidence_summary"),
                    "source": filename,
                }
            )

# Deduplicate identical evidence rows while retaining every distinct historical receipt.
unique = []
seen = set()
for row in evidence:
    marker = tuple(str(row.get(field) or "") for field in [
        "name_as_printed", "evidence_type", "date", "archive_page", "presbytery_as_printed", "detail"
    ])
    if marker not in seen:
        seen.add(marker)
        unique.append(row)

by_name = defaultdict(list)
for row in unique:
    by_name[key(row["name_as_printed"])].append(row)

members = []
for normalized_name_key, records in sorted(by_name.items()):
    variants = Counter(row["name_as_printed"] for row in records)
    display_name = variants.most_common(1)[0][0]
    candidates = person_index.get(person_key(display_name), [])
    dates = sorted(row["date"] for row in records if row.get("date") and re.match(r"\d{4}-\d{2}-\d{2}", row["date"]))
    members.append(
        {
            "canonical_name": display_name,
            "normalized_name_key": normalized_name_key,
            "name_variants_as_printed": sorted(variants),
            "normalized_person_id": candidates[0] if len(candidates) == 1 else None,
            "first_evidence_date": dates[0] if dates else None,
            "evidence_count": len(records),
            "evidence": records,
        }
    )

membership = {
    "metadata": {
        "source": "National Partnership Emails, 2013–2021 — combined archive",
        "confirmed_member_count_by_normalized_printed_name": len(members),
        "evidence_record_count": sum(member["evidence_count"] for member in members),
        "rule": "Only explicit additions, explicit member language, explicitly headed NP/Partnership rosters, and unambiguous leadership/continuation statements are included.",
        "caution": "Name normalization merges punctuation and suffix variants only. Nicknames and source misspellings remain separate unless already preserved in the same evidence chain.",
    },
    "confirmed_members": members,
}
(outdir / "confirmed-memberships-canonical.json").write_text(
    json.dumps(membership, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
)

adjacent = []
with (extract_dir / "2016-candidate-support.csv").open(encoding="utf-8", newline="") as handle:
    for row in csv.DictReader(handle):
        adjacent.append({**row, "source": "2016-candidate-support.csv", "membership_established_by_record": False})
with (extract_dir / "2017-issue-actions.csv").open(encoding="utf-8", newline="") as handle:
    for row in csv.DictReader(handle):
        if "candidate_support" in (row.get("action_type") or ""):
            adjacent.append({**row, "source": "2017-issue-actions.csv", "membership_established_by_record": False})
adjacent.append(
    {
        "candidate": "Greg Thompson",
        "evidence_type": "np_supported_sjc_nominee",
        "evidence_summary": "NP correspondence supports and celebrates Thompson as an SJC nominee; this record does not establish NP membership.",
        "membership_established_by_record": False,
        "source": "confirmed-memberships-and-actions-v1.json",
    }
)
(outdir / "supported-candidates-and-adjacent-leaders.json").write_text(
    json.dumps(
        {
            "metadata": {
                "record_count": len(adjacent),
                "rule": "Support, preference, praise, or adjacency is stored separately and never establishes membership by itself.",
            },
            "records": adjacent,
        },
        indent=2,
        ensure_ascii=False,
    )
    + "\n",
    encoding="utf-8",
)
print(json.dumps(membership["metadata"], indent=2))
