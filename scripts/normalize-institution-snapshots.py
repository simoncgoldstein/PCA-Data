#!/usr/bin/env python3
"""Normalize curated, dated official institution-roster receipts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: normalize-institution-snapshots.py <repo-root> <output.json>")
root, output = Path(sys.argv[1]), Path(sys.argv[2])

# Configuration fields:
#   organization_id, raw_receipt, snapshot_date, source_url,
#   allowed_h2, include_h3, coverage_status
#
# `include_h3=False` means only list rows directly under an allowed H2 are
# normalized. This is useful when an otherwise valid H2 contains nested notes
# or evidence sections that should not become role rows.
CONFIG = [
    ("cdm", "sources/raw/institutions/cdm/staff-and-womens-ministry-2026-09-03.md", "2026-09-03", "https://pcacdm.org/about-cdm/cdm-staff/", ["Current CDM program staff", "Administrative staff / consultant", "Current Women's Ministry national leadership", "Additional Women's Ministry advisor roles visible on current page"], True, "substantial current staff and Women's Ministry leadership snapshot"),
    ("covenant-college", "sources/raw/institutions/covenant-college/leadership-snapshot-2026-09-04.md", "2026-09-04", "https://covenant.edu/about/who/leadership/", ["Current Senior Administration", "Current Board Officers", "Current Trustees", "Current Trustee Advisors"], False, "complete visible current senior administration, board officers, trustees, and trustee advisors"),
    ("covenant-theological-seminary", "sources/raw/institutions/covenant-theological-seminary/faculty-trustees-2026-09-03.md", "2026-09-03", "https://www.covenantseminary.edu/faculty", ["Current president", "Full-time faculty visible on the current faculty page", "Incoming / recently appointed", "Emeritus faculty visible on current page", "Board of Trustees listed on current About page"], True, "current faculty, emeriti, incoming faculty, and trustee classes"),
    ("geneva-benefits", "sources/raw/institutions/geneva-benefits/team-board-2026-09-03.md", "2026-09-03", "https://genevabenefits.org/about-us/", ["Current leadership", "Current staff", "Current board"], True, "current official leadership, staff, and board"),
    ("greenville-presbyterian-theological-seminary", "sources/raw/institutions/greenville-presbyterian-theological-seminary/faculty-snapshot-2026-09-03.md", "2026-09-03", "https://www.gpts.edu/faculty", ["Resident faculty", "Visiting / adjunct faculty", "Current staff visible on official page"], True, "current faculty and staff"),
    ("mission-to-north-america", "sources/raw/institutions/mna/team-snapshot-2026-09-04.md", "2026-09-04", "https://www.pcamna.org/about", ["Current MNA Team"], False, "complete visible current MNA team roster with title and department where printed"),
    ("mission-to-the-world", "sources/raw/institutions/mtw/leadership-and-strategy-2026-09-03.md", "2026-09-03", "https://mtw.org/about/", ["Current coordinator"], False, "coordinator only; no public executive roster captured"),
    ("pca-administrative-committee", "sources/raw/institutions/pca-administrative-committee/staff-snapshot-2026-09-03.md", "2026-09-03", "https://www.pcaac.org/staff/", ["Current staff listed by the Administrative Committee"], True, "complete visible current staff roster"),
    ("pca-foundation", "sources/raw/institutions/pca-foundation/team-board-2026-09-03.md", "2026-09-03", "https://pcafoundation.com/about/", ["Current team visible in official sources", "Board of Directors listed in 2025 Annual Report"], True, "current staff plus 2025 annual-report board"),
    ("reformed-theological-seminary", "sources/raw/institutions/reformed-theological-seminary/faculty-snapshot-2026-09-03.md", "2026-09-03", "https://rts.edu/people/", ["Current high-value overlaps already in the PCA research universe"], True, "high-overlap subset only; campus-wide roster remains incomplete"),
    ("ridge-haven", "sources/raw/institutions/ridge-haven/staff-snapshot-2026-09-03.md", "2026-09-03", "https://www.ridgehaven.org/staff", ["Current leadership and notable staff"], True, "current visible staff, including Ridge Haven Cono"),
    ("reformed-university-fellowship", "sources/raw/institutions/ruf/roster-and-pipeline-snapshot-2026-09-03.md", "2026-09-03", "https://ruf.org/about/", ["Current national leadership / historical coordinator line", "Current/visible national staff examples", "2026 new Campus Ministers / Directors / Assistants"], True, "coordinator history and selected 2026 hires; complete campus roster remains incomplete"),
    ("westminster-seminary-california", "sources/raw/institutions/westminster-seminary-california/faculty-snapshot-2026-09-03.md", "2026-09-03", "https://www.wscal.edu/faculty/", ["Current faculty", "Faculty emeriti", "2025–2026 visiting/adjunct/lecturer examples listed by official faculty page"], True, "current faculty, emeriti, and visible visiting/adjunct examples"),
    ("westminster-theological-seminary", "sources/raw/institutions/westminster-theological-seminary/faculty-snapshot-2026-09-04.md", "2026-09-04", "https://www.wts.edu/academic-study/faculty", ["Current Faculty", "Current Affiliate Faculty", "Current CCEF Counseling Faculty listed by Westminster", "Center for Theological Writing"], False, "current faculty, affiliate faculty, counseling faculty, and theological-writing staff with exact titles"),
]

DEPARTMENT_SPLIT_ORGS = {"mission-to-north-america"}

people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))


def clean(value: str) -> str:
    return re.sub(r"[*_`]", "", value).strip().rstrip(".")


def key(value: str) -> str:
    value = re.sub(r"^(?:(?:rev|dr|prof|mr|mrs|ms|pastor)\.?\s+)+", "", clean(value), flags=re.I)
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    parts = re.sub(r"[^a-z0-9 ]+", " ", value.lower()).split()
    return f"{parts[0]} {parts[-1]}" if len(parts) >= 2 else " ".join(parts)


person_index = {}
for person in people:
    person_index.setdefault(key(person["name"]), []).append(person["id"])

records = []
coverage = []
snapshot_dates = sorted({config[2] for config in CONFIG})

for organization_id, relative, snapshot_date, source_url, allowed_h2, include_h3, status in CONFIG:
    lines = (root / relative).read_text(encoding="utf-8").splitlines()
    h2 = h3 = None
    count_before = len(records)
    for line_number, line in enumerate(lines, 1):
        if line.startswith("## "):
            h2, h3 = line[3:].strip(), None
            continue
        if line.startswith("### "):
            h3 = line[4:].strip()
            continue
        if h2 not in allowed_h2:
            continue
        if h3 and not include_h3:
            continue
        match = re.match(r"^(?:- |\d+\. )(.+)$", line)
        if not match:
            continue
        raw = match.group(1).strip()
        has_delimiter = " — " in raw
        if has_delimiter:
            printed_name, role = raw.split(" — ", 1)
        else:
            printed_name, role = raw, h3 or h2
        printed_name, role = clean(printed_name), clean(role)

        department = None
        if organization_id in DEPARTMENT_SPLIT_ORGS:
            role_part, separator, department_part = role.partition(" — ")
            role = clean(role_part)
            if role.lower() == "title not printed":
                role = None
            if separator:
                department = clean(department_part)
                if department.lower().startswith("department not printed"):
                    department = None

        if re.match(r"^(?:B\.A|M\.A|M\.Div|M\.S(?:\.Ed)?|Ed\.D|Ph\.D)(?:[., ]|$)", printed_name) or printed_name.startswith(("doctorate", "former ", "RTS role")):
            continue
        if not has_delimiter and printed_name[:1].islower():
            continue
        if printed_name.startswith("Sarah [surname not exposed"):
            resolved = None
        else:
            candidates = person_index.get(key(printed_name), [])
            resolved = candidates[0] if len(candidates) == 1 else None
        record = {
            "organization_id": organization_id,
            "snapshot_date": snapshot_date,
            "section_as_printed": h3 or h2,
            "name_as_printed": printed_name,
            "role_as_printed": role,
            "normalized_person_id": resolved,
            "source_url": source_url,
            "raw_receipt": relative,
            "source_line": line_number,
            "ideological_weight": 0,
        }
        if organization_id in DEPARTMENT_SPLIT_ORGS:
            record["department_as_printed"] = department
        records.append(record)
    coverage.append({"organization_id": organization_id, "records": len(records) - count_before, "coverage_status": status, "source_url": source_url, "raw_receipt": relative})

metadata = {
    "snapshot_date": snapshot_dates[-1],
    "record_count": len(records),
    "identity_rule": "Only unique first/last matches to existing data/people.json are resolved. No new person nodes are created.",
    "modeling_rule": "Employment, governance, education, and ordinary institutional service are neutral graph edges with zero ideological weight.",
}
if len(snapshot_dates) > 1:
    metadata["snapshot_dates"] = snapshot_dates

result = {
    "metadata": metadata,
    "coverage": coverage,
    "roles": records,
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"records": len(records), "organizations": len(coverage), "by_organization": {x['organization_id']: x['records'] for x in coverage}}, indent=2))
