#!/usr/bin/env python3
"""Normalize Save the PCA's 2026-02-08 FFO workbook without altering it.

Uses only Python's standard library to read the OOXML package. The raw XLSX is
kept as the receipt; this script emits source-faithful JSON extracts for later
church matching. It does not turn observed people in the workbook into person
nodes automatically.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

if len(sys.argv) < 3:
    raise SystemExit("usage: import-ffo-xlsx.py <input.xlsx> <output-dir>")

input_path = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

EXPECTED_SHA256 = "b746fbdd1ccbb6087feeb6ed5abee91b4ac203a3cacc08de167c46a8cf9d0150"
DATASET_DATE = "2026-02-08"
SOURCE_URL = "https://www.savethepca.com/wp-content/uploads/2026/02/ffo_public_dataset_020826.xlsx"
SOURCE_PAGE = "https://www.savethepca.com/downloads/"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

raw_bytes = input_path.read_bytes()
sha256 = hashlib.sha256(raw_bytes).hexdigest()


def excel_date(value: str | None):
    if value in (None, ""):
        return None
    try:
        serial = float(value)
    except (TypeError, ValueError):
        return value
    # Excel 1900 date system, accounting for the historical leap-year bug.
    base = dt.datetime(1899, 12, 30)
    return (base + dt.timedelta(days=serial)).date().isoformat()


def col_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref)
    if not letters:
        return 0
    n = 0
    for ch in letters.group(0):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


with zipfile.ZipFile(input_path) as z:
    workbook = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(f"{{{PKG_REL_NS}}}Relationship")
    }

    shared_strings: list[str] = []
    if "xl/sharedStrings.xml" in z.namelist():
        sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in sst.findall("m:si", NS):
            shared_strings.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))

    sheet_paths: dict[str, str] = {}
    sheets = workbook.find("m:sheets", NS)
    for sheet in sheets or []:
        name = sheet.attrib["name"]
        rid = sheet.attrib[f"{{{REL_NS}}}id"]
        target = relmap[rid].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        sheet_paths[name] = target

    def read_sheet(name: str) -> list[dict[str, str]]:
        target = sheet_paths[name]
        root = ET.fromstring(z.read(target))
        matrix: list[list[str]] = []
        for row in root.findall(".//m:sheetData/m:row", NS):
            values: dict[int, str] = {}
            max_col = -1
            for cell in row.findall("m:c", NS):
                idx = col_index(cell.attrib.get("r", "A1"))
                max_col = max(max_col, idx)
                typ = cell.attrib.get("t")
                value = ""
                if typ == "inlineStr":
                    value = "".join(t.text or "" for t in cell.iter(f"{{{NS['m']}}}t"))
                else:
                    v = cell.find("m:v", NS)
                    if v is not None:
                        raw = v.text or ""
                        if typ == "s" and raw.isdigit():
                            value = shared_strings[int(raw)]
                        else:
                            value = raw
                values[idx] = value.strip() if isinstance(value, str) else value
            if max_col >= 0:
                matrix.append([values.get(i, "") for i in range(max_col + 1)])

        if not matrix:
            return []
        headers = [str(h).strip() for h in matrix[0]]
        records = []
        for excel_row, row in enumerate(matrix[1:], start=2):
            padded = row + [""] * max(0, len(headers) - len(row))
            record = {headers[i]: padded[i] for i in range(len(headers)) if headers[i]}
            record["_source_row"] = excel_row
            if any(str(v).strip() for k, v in record.items() if k != "_source_row"):
                records.append(record)
        return records

    extracted = {name: read_sheet(name) for name in [
        "church_list", "raw_data", "bucketed_data", "ambiguous_data", "presbyteries"
    ]}

# Normalize review dates but preserve the raw serial beside them.
for sheet_name in ["church_list", "raw_data", "bucketed_data", "ambiguous_data"]:
    for row in extracted[sheet_name]:
        if "Review Date" in row:
            row["Review Date Raw"] = row["Review Date"]
            row["Review Date"] = excel_date(row["Review Date"])

# Focused derived tables retain all source-attributed fields.
flagged_churches = []
for row in extracted["church_list"]:
    elder = row.get("Functional Female Elders? (Y/N)", "")
    deacon = row.get("Functional Female Deacons? (Y/N)", "")
    if elder == "Y" or deacon == "Y":
        flagged_churches.append({
            "source_row": row["_source_row"],
            "presbytery": row.get("Presbytery") or None,
            "church": row.get("Church") or None,
            "phone": row.get("Phone") or None,
            "website": row.get("Website") or None,
            "email": row.get("Email") or None,
            "pastor_as_printed": row.get("Pastor") or None,
            "review_date": row.get("Review Date") or None,
            "functional_female_elders": elder or None,
            "functional_female_deacons": deacon or None,
            "elders_on_website": row.get("Elders on Website? (Y/N)") or None,
            "deacons_on_website": row.get("Deacons on Website? (Y/N)") or None,
            "other_staff_on_website": row.get("Other Staff on Website? (Y/N)") or None,
            "website_status": row.get("Website Status") or None,
            "comments": row.get("Comments") or None,
        })

raw_roles = []
for i, raw in enumerate(extracted["raw_data"]):
    bucket = extracted["bucketed_data"][i] if i < len(extracted["bucketed_data"]) else {}
    raw_roles.append({
        "source_row": raw["_source_row"],
        "presbytery": raw.get("Presbytery") or None,
        "church": raw.get("Church") or None,
        "phone": raw.get("Phone") or None,
        "website": raw.get("Website") or None,
        "name_as_printed": raw.get("Name") or None,
        "raw_position": raw.get("Position") or None,
        "bucketed_position": bucket.get("Position") or None,
        "review_date": raw.get("Review Date") or None,
        "archive_link": raw.get("Archive Link") or None,
        "bucketed_archive_link": bucket.get("Archive Link") or None,
    })

ambiguous_roles = []
for raw in extracted["ambiguous_data"]:
    ambiguous_roles.append({
        "source_row": raw["_source_row"],
        "presbytery": raw.get("Presbytery") or None,
        "church": raw.get("Church") or None,
        "phone": raw.get("Phone") or None,
        "website": raw.get("Website") or None,
        "name_as_printed": raw.get("Name") or None,
        "raw_position": raw.get("Position") or None,
        "bucketed_position": raw.get("Bucketed Position") or None,
        "review_date": raw.get("Review Date") or None,
        "archive_link": raw.get("Archive Link") or None,
    })

metadata = {
    "dataset": "Save the PCA Functional Female Officer public dataset",
    "dataset_date": DATASET_DATE,
    "source_page": SOURCE_PAGE,
    "source_url": SOURCE_URL,
    "sha256": sha256,
    "expected_sha256_from_user_supplied_copy": EXPECTED_SHA256,
    "matches_user_supplied_copy": sha256 == EXPECTED_SHA256,
    "sheet_counts": {name: len(rows) for name, rows in extracted.items()},
    "derived_counts": {
        "flagged_churches": len(flagged_churches),
        "raw_role_observations": len(raw_roles),
        "ambiguous_role_observations": len(ambiguous_roles),
    },
    "rules": {
        "creates_person_nodes": False,
        "external_assessment_is_church_level": True,
        "raw_workbook_preserved": True,
        "archive_links_preserved": True,
        "silent_corrections": False,
    },
}

outputs = {
    "import-metadata.json": metadata,
    "church-list.json": extracted["church_list"],
    "flagged-churches.json": flagged_churches,
    "role-observations.json": raw_roles,
    "ambiguous-role-observations.json": ambiguous_roles,
    "presbytery-summary-source.json": extracted["presbyteries"],
}

for filename, payload in outputs.items():
    (output_dir / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(json.dumps(metadata, indent=2))
if sha256 != EXPECTED_SHA256:
    raise SystemExit("Downloaded workbook hash differs from the user-supplied 2026-02-08 copy; manual review required.")
