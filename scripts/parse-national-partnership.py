#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

if len(sys.argv) < 3:
    raise SystemExit("usage: parse-national-partnership.py <np.txt> <output.json> [pdf-path]")

text_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
pdf_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
text = text_path.read_text(encoding="utf-8", errors="replace")
pages = text.split("\f")

DATE_RE = re.compile(r"([A-Z][a-z]{2} \d{1,2}, 20\d{2}, [0-9:]+ [AP]M)")
SECTION_RE = re.compile(
    r"^\s*\d+[\.)]?\s*(?:News|Updates|Action items|To Do|Calendar|Prayer|Discussion|General Assembly|GA\b)",
    re.I,
)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def context_for(page_no: int, line_no: int) -> dict:
    for pno in range(page_no, max(0, page_no - 5), -1):
        lines = pages[pno - 1].splitlines()
        upto = line_no - 1 if pno == page_no else len(lines)
        for idx in range(upto - 1, -1, -1):
            match = DATE_RE.search(lines[idx])
            if not match:
                continue
            sender = None
            for k in range(idx - 1, max(-1, idx - 8), -1):
                candidate = clean(lines[k])
                if (
                    candidate
                    and not candidate.startswith("<")
                    and "@" not in candidate
                    and "unread" not in candidate.lower()
                    and not re.match(r"^\d+ views?$", candidate)
                ):
                    sender = candidate
                    break
            return {"date": match.group(1), "context_page": pno, "sender_as_printed": sender}
    return {"date": None, "context_page": None, "sender_as_printed": None}


def excerpt(page_no: int, line_no: int, before: int = 2, after: int = 5) -> list[str]:
    lines = pages[page_no - 1].splitlines()
    start = max(0, line_no - 1 - before)
    end = min(len(lines), line_no + after)
    return [clean(line) for line in lines[start:end] if clean(line)]


def parse_inline_people(value: str) -> list[dict]:
    people = []
    pattern = re.compile(
        r"(?:(TE|RE)\s+)?([A-Z][A-Za-z0-9\.\'’\- ]*?[A-Za-z\.\'’\-])\s*\(([^)]+)\)"
    )
    for match in pattern.finditer(value):
        name = clean(match.group(2))
        presbytery = clean(match.group(3))
        if name and len(name) < 80:
            people.append(
                {
                    "name": name,
                    "title": match.group(1),
                    "presbytery_as_printed": presbytery,
                    "raw": clean(match.group(0)),
                }
            )
    return people


# Explicit Additions snapshots.
additions = []
for page_no, page in enumerate(pages, 1):
    lines = page.splitlines()
    for i, line in enumerate(lines):
        if not re.match(r"^\s*(?:\d+[\.)]?\s*)?Additions\b", line, re.I):
            continue
        people = []
        for j in range(i + 1, min(i + 40, len(lines))):
            value = clean(lines[j])
            if SECTION_RE.match(value) or re.match(
                r"^\s*\d+[\.)]?\s*(?:News|Updates|Action items)", value, re.I
            ):
                break
            match = re.match(r"^(TE|RE)\s+(.+?)\s+\(([^)]+)\)\s*$", value)
            if match:
                people.append(
                    {
                        "name": clean(match.group(2)),
                        "title": match.group(1),
                        "presbytery_as_printed": clean(match.group(3)),
                        "raw": value,
                    }
                )
        if not people:
            continue
        ctx = context_for(page_no, i + 1)
        totals = re.search(r"(\d+)\s*(?:elders?)?\s*in\s*(\d+)\s*presbyter", line, re.I)
        additions.append(
            {
                "page": page_no,
                "line": i + 1,
                "date": ctx["date"],
                "sender_as_printed": ctx["sender_as_printed"],
                "heading": clean(line),
                "reported_members_or_elders": int(totals.group(1)) if totals else None,
                "reported_presbyteries": int(totals.group(2)) if totals else None,
                "people": people,
                "evidence_type": "explicit_additions_roster",
            }
        )


# Direct named references using the exact phrase "NP member."
explicit = []
explicit_patterns = [
    (re.compile(r"NP member Sean Lucas", re.I), "Sean Lucas"),
    (re.compile(r"Mike Khandjian, NP member", re.I), "Mike Khandjian"),
    (re.compile(r"Pastor Kevin Labby, NP member", re.I), "Kevin Labby"),
    (re.compile(r"Irwyn Ince, NP member", re.I), "Irwyn Ince"),
]
seen = set()
for page_no, page in enumerate(pages, 1):
    for line_no, line in enumerate(page.splitlines(), 1):
        for pattern, name in explicit_patterns:
            if not pattern.search(line):
                continue
            ctx = context_for(page_no, line_no)
            key = (name, ctx["date"])
            if key in seen:
                continue
            seen.add(key)
            explicit.append(
                {
                    "name": name,
                    "evidence_type": "explicit_member_reference",
                    "page": page_no,
                    "line": line_no,
                    "date": ctx["date"],
                    "sender_as_printed": ctx["sender_as_printed"],
                    "excerpt": excerpt(page_no, line_no, 2, 4),
                }
            )


# Lists expressly introduced as "NP members who have been nominated."
nominee_lists = []
for page_no, page in enumerate(pages, 1):
    lines = page.splitlines()
    for i, line in enumerate(lines):
        if "list of NP members who have been nominated for permanent or special committees" not in line:
            continue
        people = []
        for j in range(i + 1, min(i + 25, len(lines))):
            value = clean(lines[j])
            if not value:
                continue
            match = re.match(r"^(TE|RE)\s+(.+?)\s+\(([^)]+)\)\s*$", value)
            if match:
                people.append(
                    {
                        "name": clean(match.group(2)),
                        "title": match.group(1),
                        "nomination_as_printed": clean(match.group(3)),
                        "raw": value,
                    }
                )
            elif people:
                break
        if people:
            ctx = context_for(page_no, i + 1)
            nominee_lists.append(
                {
                    "page": page_no,
                    "line": i + 1,
                    "date": ctx["date"],
                    "sender_as_printed": ctx["sender_as_printed"],
                    "evidence_type": "explicit_np_member_nominee_list",
                    "people": people,
                }
            )

unique_nominee_lists = []
seen = set()
for record in nominee_lists:
    key = (
        record["date"],
        tuple((person["name"], person["nomination_as_printed"]) for person in record["people"]),
    )
    if key not in seen:
        seen.add(key)
        unique_nominee_lists.append(record)
nominee_lists = unique_nominee_lists


# 2015 rosters literally headed "Partnership men ..."
partnership_blocks = []
committee_labels = {
    "serving on rpr": "Review of Presbytery Records",
    "on nominating committee": "Nominating Committee",
    "on the overtures committee": "Overtures Committee",
}
for page_no, page in enumerate(pages, 1):
    lines = page.splitlines()
    for i, line in enumerate(lines):
        value = clean(line)
        match = re.match(
            r"^Partnership men (serving on RPR|on Nominating committee|on the Overtures Committee)\s*:?(.*)$",
            value,
            re.I,
        )
        if not match:
            continue
        committee = committee_labels[match.group(1).lower()]
        collected = match.group(2).strip()
        for j in range(i + 1, min(i + 8, len(lines))):
            nxt = clean(lines[j])
            if not nxt:
                break
            if re.match(
                r"^(Here are|GA COMMITTEE|Please let me|Partnership men|\d+\.|National Partnership)",
                nxt,
                re.I,
            ):
                break
            collected += " " + nxt
        people = parse_inline_people(collected)
        if people:
            ctx = context_for(page_no, i + 1)
            partnership_blocks.append(
                {
                    "page": page_no,
                    "line": i + 1,
                    "date": ctx["date"],
                    "sender_as_printed": ctx["sender_as_printed"],
                    "committee": committee,
                    "evidence_type": "explicit_partnership_men_committee_roster",
                    "people": people,
                    "raw_text": clean(collected),
                }
            )


# 2018 "NP guys on committees" snapshots spanning page boundaries.
np_guys = []
for page_no, page in enumerate(pages, 1):
    lines = page.splitlines()
    for i, line in enumerate(lines):
        if "NP guys on committees" not in line:
            continue
        ctx = context_for(page_no, i + 1)
        chunks = []
        stop = False
        for qno in range(page_no, min(len(pages), page_no + 3) + 1):
            qlines = pages[qno - 1].splitlines()
            start = i + 1 if qno == page_no else 0
            for j in range(start, len(qlines)):
                value = clean(qlines[j])
                if (qno != page_no or j > i) and DATE_RE.search(value):
                    stop = True
                    break
                if re.match(r"^(Thanks all|JK)$", value):
                    stop = True
                    break
                chunks.append((qno, j + 1, value))
            if stop:
                break

        current = None
        people_by = {}
        for _qno, _line_no, value in chunks:
            if not value:
                continue
            if re.fullmatch(r"Nominating Committee", value, re.I):
                current = "Nominating Committee"
                people_by.setdefault(current, [])
                continue
            if re.fullmatch(r"RPR", value, re.I):
                current = "Review of Presbytery Records"
                people_by.setdefault(current, [])
                continue
            if re.fullmatch(r"Overtures", value, re.I):
                current = "Overtures Committee"
                people_by.setdefault(current, [])
                continue
            if not current:
                continue
            dash_match = re.match(r"^(.+?)\s+-\s*(.*)$", value)
            if dash_match:
                people_by[current].append(
                    {
                        "name": clean(dash_match.group(1)),
                        "presbytery_as_printed": clean(dash_match.group(2)) or None,
                        "raw": value,
                    }
                )
            elif current == "Overtures Committee" and not re.match(r"^(Brothers|What this means|\d+\.)", value):
                tokens = value.split()
                if 2 <= len(tokens) <= 7:
                    people_by[current].append(
                        {
                            "name": None,
                            "presbytery_as_printed": None,
                            "raw": value,
                            "parse_status": "unresolved_name_presbytery_boundary",
                        }
                    )
        if any(people_by.values()):
            np_guys.append(
                {
                    "page": page_no,
                    "line": i + 1,
                    "date": ctx["date"],
                    "sender_as_printed": ctx["sender_as_printed"],
                    "evidence_type": "explicit_np_guys_committee_roster",
                    "committees": people_by,
                }
            )

seen = set()
unique_np_guys = []
for record in np_guys:
    if record["date"] not in seen:
        seen.add(record["date"])
        unique_np_guys.append(record)
np_guys = unique_np_guys


# 2019 roster introduced across a wrapped two-line sentence as current NP members on Overtures.
current_committee = []
for page_no, page in enumerate(pages, 1):
    lines = page.splitlines()
    for i, line in enumerate(lines):
        window = " ".join(clean(value) for value in lines[i : min(len(lines), i + 2)])
        if "Here are the NP members" not in window or "committee" not in window:
            continue
        nearby = " ".join(clean(value) for value in lines[max(0, i - 5) : min(len(lines), i + 2)])
        if "Overtures" not in nearby and "current list" not in nearby and "membership update" not in nearby:
            continue
        people = []
        for j in range(i + 1, min(i + 25, len(lines))):
            value = clean(lines[j])
            match = re.match(r"^(TE|RE)\s+(.+?)\s+\(([^)]+)\)\s*$", value)
            if match:
                people.append(
                    {
                        "name": clean(match.group(2)),
                        "title": match.group(1),
                        "presbytery_as_printed": clean(match.group(3)),
                        "raw": value,
                    }
                )
            elif people:
                break
        if people:
            ctx = context_for(page_no, i + 1)
            current_committee.append(
                {
                    "page": page_no,
                    "line": i + 1,
                    "date": ctx["date"],
                    "sender_as_printed": ctx["sender_as_printed"],
                    "committee": "Overtures Committee",
                    "evidence_type": "explicit_np_members_current_committee_roster",
                    "people": people,
                }
            )


# Named agency/committee service following 2015 Partnership rosters.
agency_rosters = []
for page_no in [176, 178, 180]:
    if page_no > len(pages):
        continue
    lines = pages[page_no - 1].splitlines()
    ctx = context_for(page_no, len(lines))
    people = []
    for line_no, line in enumerate(lines, 1):
        value = clean(line)
        match = re.match(
            r"^(Admin|Covenant College|Covenant Sem|Discipleship min|IRC|MNA|MTW|RUM)\s*[–-]\s*(.+)$",
            value,
            re.I,
        )
        if not match:
            continue
        for person in parse_inline_people(match.group(2)):
            people.append(
                {
                    "organization_as_printed": match.group(1),
                    **person,
                    "page": page_no,
                    "line": line_no,
                }
            )
    if people:
        agency_rosters.append(
            {
                "page": page_no,
                "date": ctx["date"],
                "sender_as_printed": ctx["sender_as_printed"],
                "evidence_type": "np_roster_current_committee_or_agency_service",
                "people": people,
            }
        )


# Membership/committee count statements for historical scale.
count_snapshots = []
count_patterns = [
    re.compile(r"(\d+)\s+Partnership members? on (?:the )?committee", re.I),
    re.compile(r"(\d+)\s+NP members? serving on the Nominating Committee", re.I),
    re.compile(r"(\d+)\s+NP members? serving on RPR", re.I),
    re.compile(r"counting\s+(\d+)\s+NP men on the Overtures committee", re.I),
]
for page_no, page in enumerate(pages, 1):
    for line_no, line in enumerate(page.splitlines(), 1):
        for pattern in count_patterns:
            match = pattern.search(line)
            if match:
                ctx = context_for(page_no, line_no)
                count_snapshots.append(
                    {
                        "page": page_no,
                        "line": line_no,
                        "date": ctx["date"],
                        "reported_count": int(match.group(1)),
                        "raw": clean(line),
                    }
                )
                break


# Generic evidence excerpts for all network-membership keywords so source material
# overlooked by the structured parsers remains discoverable for later review.
keyword_excerpts = []
for page_no, page in enumerate(pages, 1):
    for line_no, line in enumerate(page.splitlines(), 1):
        if re.search(r"\b(?:NP members?|NP guys|Partnership men|Partnership members?)\b", line, re.I):
            ctx = context_for(page_no, line_no)
            keyword_excerpts.append(
                {
                    "page": page_no,
                    "line": line_no,
                    "date": ctx["date"],
                    "sender_as_printed": ctx["sender_as_printed"],
                    "matched_line": clean(line),
                    "excerpt": excerpt(page_no, line_no, 2, 3),
                }
            )


# Derived evidence index. Name strings are intentionally not silently canonicalized.
evidence = []


def add_evidence(name, kind, page, date, detail, presbytery=None, title=None):
    evidence.append(
        {
            "name": name,
            "evidence_type": kind,
            "page": page,
            "date": date,
            "detail": detail,
            "presbytery_as_printed": presbytery,
            "title": title,
        }
    )


for snapshot in additions:
    for person in snapshot["people"]:
        add_evidence(
            person["name"],
            "addition",
            snapshot["page"],
            snapshot["date"],
            snapshot["heading"],
            person["presbytery_as_printed"],
            person["title"],
        )
for record in explicit:
    add_evidence(
        record["name"],
        "explicit_reference",
        record["page"],
        record["date"],
        " / ".join(record["excerpt"]),
    )
for snapshot in nominee_lists:
    for person in snapshot["people"]:
        add_evidence(
            person["name"],
            "explicit_np_member_nominee_list",
            snapshot["page"],
            snapshot["date"],
            person["nomination_as_printed"],
            title=person["title"],
        )
for snapshot in partnership_blocks:
    for person in snapshot["people"]:
        add_evidence(
            person["name"],
            "partnership_men_roster",
            snapshot["page"],
            snapshot["date"],
            snapshot["committee"],
            person["presbytery_as_printed"],
            person["title"],
        )
for snapshot in np_guys:
    for committee, people in snapshot["committees"].items():
        for person in people:
            if person.get("name"):
                add_evidence(
                    person["name"],
                    "np_guys_committee_roster",
                    snapshot["page"],
                    snapshot["date"],
                    committee,
                    person.get("presbytery_as_printed"),
                )
for snapshot in current_committee:
    for person in snapshot["people"]:
        add_evidence(
            person["name"],
            "explicit_np_members_committee_roster",
            snapshot["page"],
            snapshot["date"],
            snapshot["committee"],
            person["presbytery_as_printed"],
            person["title"],
        )

by_name = {}
for record in evidence:
    by_name.setdefault(record["name"].strip(), []).append(record)

confirmed_member_name_evidence_index = [
    {
        "name": name,
        "evidence_count": len(records),
        "first_date": next((record["date"] for record in records if record["date"]), None),
        "evidence": records,
    }
    for name, records in sorted(by_name.items())
]

result = {
    "metadata": {
        "source_title": "National Partnership Emails, 2013–2021 — combined archive",
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest()
        if pdf_path and pdf_path.exists()
        else None,
        "page_count_text_split": len(pages),
        "method_note": "The confirmed-name evidence index includes only explicit Additions rosters, explicit NP-member references, lists explicitly called NP members, Partnership-men committee rosters, NP-guys committee rosters, and rosters explicitly introduced as NP members. Supported nominees or praised leaders are not included merely because they were favored by NP.",
        "warnings": [
            "Internal names/presbytery labels are preserved as printed; jokes, abbreviations, misspellings, and historical presbytery names are not silently corrected.",
            "Repeated additions/rosters are preserved as dated evidence.",
            "NP-guys committee language is treated as explicit network-roster evidence but retains the source wording.",
            "The derived count is a count of distinct printed name strings, not a final identity-resolved person count. Variants such as EJ/E.J., Dave/David, and source misspellings require later identity resolution.",
        ],
    },
    "counts": {
        "addition_snapshots": len(additions),
        "addition_entries": sum(len(record["people"]) for record in additions),
        "explicit_named_member_references": len(explicit),
        "np_member_nominee_lists": len(nominee_lists),
        "partnership_men_committee_snapshots": len(partnership_blocks),
        "np_guys_committee_snapshots": len(np_guys),
        "explicit_np_current_committee_snapshots": len(current_committee),
        "derived_distinct_confirmed_member_name_strings": len(confirmed_member_name_evidence_index),
        "keyword_evidence_excerpts": len(keyword_excerpts),
    },
    "addition_snapshots": additions,
    "explicit_named_member_references": explicit,
    "np_member_nominee_lists": nominee_lists,
    "partnership_men_committee_rosters": partnership_blocks,
    "np_guys_committee_rosters": np_guys,
    "explicit_np_current_committee_rosters": current_committee,
    "np_current_agency_or_committee_rosters": agency_rosters,
    "membership_count_snapshots": count_snapshots,
    "confirmed_member_name_evidence_index": confirmed_member_name_evidence_index,
    "membership_keyword_excerpts": keyword_excerpts,
}

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(result["counts"], indent=2))
