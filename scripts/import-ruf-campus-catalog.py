#!/usr/bin/env python3
"""Extract bounded staff-role facts from RUF's 2025-2026 Internship Campus Catalog PDF."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import fitz

if len(sys.argv) != 3:
    raise SystemExit("usage: import-ruf-campus-catalog.py <catalog.pdf> <repo-root>")

pdf_path = Path(sys.argv[1])
root = Path(sys.argv[2])
source_url = "https://drive.google.com/file/d/1qAYDUxeK-qcfqBfZdVNSXiK7MTqVCWda/view?usp=sharing"
snapshot_date = "2025-10-01"
raw_dir = root / "sources/raw/institutions/ruf/campus-catalog-2025-10-01"
raw_csv = raw_dir / "role-fields.csv"
raw_receipt = raw_dir / "receipt.json"
normalized_path = root / "sources/normalized/institutions/ruf/campus-role-snapshot-2025-10-01.json"
research_path = root / "research/ruf-campus-catalog-2025-10-01.md"

ROLE_LABELS = [
    "Campus Minister",
    "Associate Campus Minister",
    "Campus Associate",
    "Campus Staff",
    "Campus Assistant",
    "Campus Minister Assistant",
    "Interns",
    "Fellows",
    "Fellow",
]
FIELD_LABELS = set(ROLE_LABELS) | {
    "Location",
    "CM Leadership Style",
    "CA Leadership Style",
    "CS Leadership Style",
    "Leadership Style",
    "Large Group Size",
    "Student Group Description",
    "Campus Description",
    "Church/Churches in the area",
    "Church/churches in the area",
}
CONNECTORS = {"van", "der", "de", "del", "da", "di", "la", "le", "von"}


def name_line(value: str) -> bool:
    base = re.sub(r"\s*\([^)]*\)\s*$", "", value).strip()
    base = re.sub(r"\s+\d(?:st|nd|rd|th)\s*(?:yr|year)?\.?$", "", base, flags=re.I).strip()
    if not base or len(base) > 80 or any(ch in base for ch in ":;?!"):
        return False
    words = base.replace("–", "-").split()
    if not 1 <= len(words) <= 6:
        return False
    for word in words:
        token = word.strip(",")
        if token.lower() in CONNECTORS:
            continue
        if re.fullmatch(r"[A-Z](?:\.[A-Z])?\.?", token):
            continue
        if re.fullmatch(r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’.-]*", token):
            continue
        return False
    return True


def person_name(value: str) -> str:
    value = re.sub(r"\s*\([^)]*\)\s*$", "", value).strip()
    return re.sub(r"\s+\d(?:st|nd|rd|th)\s*(?:yr|year)?\.?$", "", value, flags=re.I).strip()


def tenure_note(value: str) -> str | None:
    match = re.search(r"\(([^)]*(?:yr|year|pt)[^)]*)\)\s*$", value, flags=re.I)
    if match:
        return match.group(1)
    match = re.search(r"(\d(?:st|nd|rd|th)\s*(?:yr|year)\.?)$", value, flags=re.I)
    return match.group(1) if match else None


def fields_on_first_page(page: fitz.Page) -> dict[str, list[str]]:
    left: list[tuple[float, str]] = []
    for block in page.get_text("blocks"):
        x0, y0, _x1, _y1, text, *_ = block
        label = " ".join(text.split())
        if x0 < 250 and label in FIELD_LABELS:
            left.append((y0, label))
    left.sort()

    right_lines: dict[tuple[int, int], list[tuple]] = {}
    for word in page.get_text("words"):
        x0, _y0, _x1, _y1, _text, block_no, line_no, _word_no = word
        if x0 > 250:
            right_lines.setdefault((block_no, line_no), []).append(word)
    right: list[tuple[float, str]] = []
    for words in right_lines.values():
        words.sort(key=lambda item: item[0])
        right.append((min(item[1] for item in words), " ".join(item[4] for item in words)))
    right.sort()

    # Two Canva pages shift the entire left label column down. Infer the offset
    # from the location row, preferring a comma-bearing city/state value.
    offset = 0.0
    location_y = next((y for y, label in left if label == "Location"), None)
    if location_y is not None:
        candidates = [(abs(y - location_y), y) for y, text in right if abs(y - location_y) <= 25 and "," in text]
        if not candidates:
            candidates = [(abs(y - location_y), y) for y, _text in right if abs(y - location_y) <= 25]
        if candidates:
            _distance, right_y = min(candidates)
            offset = right_y - location_y

    result: dict[str, list[str]] = {}
    for index, (left_y, label) in enumerate(left):
        y = left_y + offset
        next_y = left[index + 1][0] + offset if index + 1 < len(left) else y + 80
        values = [text for right_y, text in right if right_y >= y - 2 and right_y < next_y - 2]
        if values:
            result[label] = values
    return result


doc = fitz.open(pdf_path)
links: list[tuple[str, int]] = []
for toc_page in (2, 3, 4):
    page = doc[toc_page]
    for link in page.get_links():
        if link.get("page") is None:
            continue
        campus = " ".join(page.get_textbox(fitz.Rect(link["from"])).split())
        if campus:
            links.append((campus, int(link["page"]) - 1))

if len(links) != 162 or len({name for name, _page in links}) != 162:
    raise SystemExit(f"expected 162 unique catalog campus links, found {len(links)}")

rows: list[dict] = []
rejected: list[dict] = []
for campus, page_index in sorted(links, key=lambda item: item[1]):
    fields = fields_on_first_page(doc[page_index])
    location = " ".join(fields.get("Location", [])) or None
    program = "ruf_international" if campus.startswith("RUF-I ") else "ruf"
    for role in ROLE_LABELS:
        for printed_line in fields.get(role, []):
            if not name_line(printed_line):
                rejected.append({"campus": campus, "page": page_index + 1, "role": role, "text": printed_line})
                continue
            rows.append({
                "organization_id": "reformed-university-fellowship",
                "snapshot_date": snapshot_date,
                "program": program,
                "campus_as_printed": campus,
                "location_as_printed": location,
                "role_as_printed": role,
                "name_as_printed": person_name(printed_line),
                "name_line_as_printed": printed_line,
                "tenure_note_as_printed": tenure_note(printed_line),
                "catalog_page": page_index + 1,
                "source_url": source_url,
                "ideological_weight": 0,
            })

expected_rejection = [{
    "campus": "Baylor University",
    "page": 18,
    "role": "Interns",
    "text": "I try to lead well by casting vision, listening to and",
}]
if rejected not in ([], expected_rejection):
    raise SystemExit(f"unexpected non-name lines in staff fields: {rejected}")
if len(rows) != 414:
    raise SystemExit(f"expected 414 role rows, found {len(rows)}")
if len({row["name_as_printed"] for row in rows}) != 414:
    raise SystemExit("catalog person-role extraction unexpectedly contains duplicate printed names")

raw_dir.mkdir(parents=True, exist_ok=True)
with raw_csv.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=[
        "campus_as_printed", "program", "catalog_page", "location_as_printed", "role_as_printed", "name_line_as_printed"
    ])
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row[key] for key in writer.fieldnames})

role_counts = Counter(row["role_as_printed"] for row in rows)
receipt = {
    "source_title": "CampusCatalog2025-2026.pdf",
    "source_url": source_url,
    "drive_file_id": "1qAYDUxeK-qcfqBfZdVNSXiK7MTqVCWda",
    "snapshot_date": snapshot_date,
    "pdf_metadata_creation_date": doc.metadata.get("creationDate"),
    "pdf_pages": len(doc),
    "pdf_bytes": pdf_path.stat().st_size,
    "pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
    "catalog_campus_count": 162,
    "ruf_campus_entries": sum(1 for name, _page in links if not name.startswith("RUF-I ")),
    "ruf_international_entries": sum(1 for name, _page in links if name.startswith("RUF-I ")),
    "role_row_count": len(rows),
    "role_counts": dict(role_counts),
    "extraction_scope": "TOC-linked campus names plus first-page Location and printed staff-role fields only; narrative ministry answers excluded.",
    "excluded_non_name_lines": rejected,
}
raw_receipt.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

normalized = {
    "metadata": {
        "snapshot_date": snapshot_date,
        "record_count": len(rows),
        "campus_count": 162,
        "source_title": "Campus Catalog 2025-2026",
        "source_url": source_url,
        "modeling_rule": "Dated Oct. 1, 2025 campus-role snapshot. It is not a September 2026 current-roster claim. RUF service is zero-weight institutional evidence.",
    },
    "coverage": {
        "ruf_campus_entries": receipt["ruf_campus_entries"],
        "ruf_international_entries": receipt["ruf_international_entries"],
        "role_counts": dict(role_counts),
    },
    "roles": rows,
}
normalized_path.parent.mkdir(parents=True, exist_ok=True)
normalized_path.write_text(json.dumps(normalized, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

research_path.parent.mkdir(parents=True, exist_ok=True)
research_path.write_text(
    "# RUF 2025-2026 Campus Catalog ingestion\n\n"
    f"- Snapshot date: `{snapshot_date}` (PDF creation metadata)\n"
    "- Source: official RUF Internship Campus Catalog linked from RUF's Intern application page\n"
    f"- PDF SHA-256: `{receipt['pdf_sha256']}`\n"
    f"- PDF pages: {len(doc)}\n"
    f"- TOC-linked campus entries: 162 ({receipt['ruf_campus_entries']} RUF, {receipt['ruf_international_entries']} RUF International)\n"
    f"- Extracted person-role rows: {len(rows)}\n"
    f"- Role counts: {json.dumps(dict(role_counts), sort_keys=True)}\n\n"
    "Only factual first-page roster fields are retained. Narrative answers are intentionally excluded. "
    "This is historical 2025 evidence, not a claim that each person remained in the same role in September 2026. "
    "The later 2026 RUF transition dataset remains separate. Both datasets share the same RUF identity source family so RUF cannot corroborate itself for identity creation.\n",
    encoding="utf-8",
)

print(json.dumps({
    "campuses": 162,
    "roles": len(rows),
    "ruf": receipt["ruf_campus_entries"],
    "ruf_international": receipt["ruf_international_entries"],
    "role_counts": dict(role_counts),
}, indent=2))
