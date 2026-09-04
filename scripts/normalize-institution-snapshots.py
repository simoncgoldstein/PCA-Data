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
    ("mission-to-the-world", "sources/raw/institutions/mtw/leadership-snapshot-2026-09-04.md", "2026-09-04", "https://mtw.org/about/", ["Current leadership confirmed by 2026/current official sources"], True, "10 currently corroborated leadership and senior/program roles; unresolved executive succession remains excluded"),
    ("pca-administrative-committee", "sources/raw/institutions/pca-administrative-committee/staff-snapshot-2026-09-03.md", "2026-09-03", "https://www.pcaac.org/staff/", ["Current staff listed by the Administrative Committee"], True, "complete visible current staff roster"),
    ("pca-foundation", "sources/raw/institutions/pca-foundation/team-board-2026-09-03.md", "2026-09-03", "https://pcafoundation.com/about/", ["Current team visible in official sources", "Board of Directors listed in 2025 Annual Report"], True, "current staff plus 2025 annual-report board"),
    ("reformed-theological-seminary", "sources/raw/institutions/reformed-theological-seminary/residential-faculty-snapshot-2026-09-04.md", "2026-09-04", "https://rts.edu/people/", ["Current residential-faculty union"], True, "46 unique current-site residential-faculty identities, including one explicitly emeritus classification"),
    ("ridge-haven", "sources/raw/institutions/ridge-haven/staff-snapshot-2026-09-03.md", "2026-09-03", "https://www.ridgehaven.org/staff", ["Current leadership and notable staff"], True, "current visible staff, including Ridge Haven Cono"),
    ("reformed-university-fellowship", "sources/raw/institutions/ruf/roster-and-pipeline-snapshot-2026-09-03.md", "2026-09-03", "https://ruf.org/about/", ["Current national leadership / historical coordinator line", "Current/visible national staff examples", "2026 new Campus Ministers / Directors / Assistants"], True, "coordinator history and selected 2026 hires; complete campus roster remains incomplete"),
    ("westminster-seminary-california", "sources/raw/institutions/westminster-seminary-california/faculty-snapshot-2026-09-03.md", "2026-09-03", "https://www.wscal.edu/faculty/", ["Current faculty", "Faculty emeriti", "2025–2026 visiting/adjunct/lecturer examples listed by official faculty page"], True, "current faculty, emeriti, and visible visiting/adjunct examples"),
    ("westminster-theological-seminary", "sources/raw/institutions/westminster-theological-seminary/faculty-snapshot-2026-09-04.md", "2026-09-04", "https://www.wts.edu/academic-study/faculty", ["Current Faculty", "Current Affiliate Faculty", "Current CCEF Counseling Faculty listed by Westminster", "Center for Theological Writing"], False, "current faculty, affiliate faculty, counseling faculty, and theological-writing staff with exact titles"),
]

DEPARTMENT_SPLIT_ORGS = {"mission-to-north-america"}
MTW_ORG = "mission-to-the-world"
RTS_ORG = "reformed-theological-seminary"
RTS_SECTION = "Current residential-faculty union"
RTS_EVIDENCE_PREFIXES = (
    "Current residential listing:",
    "Current residential listings:",
    "Current site classification:",
    "Current institution-wide residential directory listing",
    "Current campus pages also expose",
    "RTS announced promotion",
    "Treat the exact emeritus title",
)

people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))


def strip_markup(value: str) -> str:
    return re.sub(r"[*_`]", "", value).strip()


def clean(value: str) -> str:
    return strip_markup(value).rstrip(".")


def key(value: str) -> str:
    value = re.sub(r"^(?:(?:rev|dr|prof|mr|mrs|ms|pastor)\.?\s+)+", "", clean(value), flags=re.I)
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    parts = re.sub(r"[^a-z0-9 ]+", " ", value.lower()).split()
    return f"{parts[0]} {parts[-1]}" if len(parts) >= 2 else " ".join(parts)


person_index = {}
for person in people:
    person_index.setdefault(key(person["name"]), []).append(person["id"])


def resolve_person(printed_name: str) -> str | None:
    if printed_name.startswith("Sarah [surname not exposed"):
        return None
    candidates = person_index.get(key(printed_name), [])
    return candidates[0] if len(candidates) == 1 else None


def parse_rts(
    lines: list[str],
    organization_id: str,
    relative: str,
    snapshot_date: str,
    source_url: str,
) -> list[dict]:
    """Parse the person-centered RTS receipt into one neutral role row per H3 person."""
    parsed: list[dict] = []
    in_section = False
    current_name: str | None = None
    current_line: int | None = None
    role_lines: list[str] = []
    evidence_lines: list[str] = []

    def flush() -> None:
        nonlocal current_name, current_line, role_lines, evidence_lines
        if not current_name:
            return
        if not role_lines:
            raise SystemExit(f"RTS receipt has no role title for {current_name}")
        parsed.append({
            "organization_id": organization_id,
            "snapshot_date": snapshot_date,
            "section_as_printed": RTS_SECTION,
            "name_as_printed": current_name,
            "role_as_printed": "; ".join(role_lines),
            "listing_evidence_as_printed": evidence_lines,
            "normalized_person_id": resolve_person(current_name),
            "source_url": source_url,
            "raw_receipt": relative,
            "source_line": current_line,
            "ideological_weight": 0,
        })
        current_name = None
        current_line = None
        role_lines = []
        evidence_lines = []

    for line_number, line in enumerate(lines, 1):
        if line.startswith("## "):
            if in_section:
                flush()
            in_section = line[3:].strip() == RTS_SECTION
            continue
        if not in_section:
            continue
        if line.startswith("### "):
            flush()
            current_name = strip_markup(line[4:].strip())
            current_line = line_number
            continue
        match = re.match(r"^- (.+)$", line)
        if not match or not current_name:
            continue
        value = strip_markup(match.group(1))
        if value.startswith(RTS_EVIDENCE_PREFIXES):
            evidence_lines.append(value)
        else:
            role_lines.append(value)
    if in_section:
        flush()
    return parsed


records = []
coverage = []
snapshot_dates = sorted({config[2] for config in CONFIG})

for organization_id, relative, snapshot_date, source_url, allowed_h2, include_h3, status in CONFIG:
    lines = (root / relative).read_text(encoding="utf-8").splitlines()
    count_before = len(records)

    if organization_id == RTS_ORG:
        records.extend(parse_rts(lines, organization_id, relative, snapshot_date, source_url))
        coverage.append({"organization_id": organization_id, "records": len(records) - count_before, "coverage_status": status, "source_url": source_url, "raw_receipt": relative})
        continue

    h2 = h3 = None
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
        printed_name = strip_markup(printed_name) if organization_id == MTW_ORG else clean(printed_name)
        role = clean(role)

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
        record = {
            "organization_id": organization_id,
            "snapshot_date": snapshot_date,
            "section_as_printed": h3 or h2,
            "name_as_printed": printed_name,
            "role_as_printed": role,
            "normalized_person_id": resolve_person(printed_name),
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
