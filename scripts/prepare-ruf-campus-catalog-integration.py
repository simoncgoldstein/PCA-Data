#!/usr/bin/env python3
"""One-time helper for wiring the RUF 2025 catalog into identity and validation."""

from pathlib import Path

crosswalk = Path("scripts/build-person-crosswalk.py")
text = crosswalk.read_text(encoding="utf-8")
anchor = "\n\n# Publication chapter rosters, now backed by archived screenshots.\n"
if 'dataset="ruf_campus_catalog_2025"' not in text:
    block = '''

# Dated RUF 2025-2026 Internship Campus Catalog. This remains a separate
# historical dataset but shares the RUF source family so RUF cannot corroborate
# itself when the identity layer creates canonical people.
relative = "sources/normalized/institutions/ruf/campus-role-snapshot-2025-10-01.json"
ruf_catalog_data = load(relative)
for index, row in enumerate(ruf_catalog_data.get("roles", []), 1):
    institutions = ["reformed-university-fellowship", row.get("campus_as_printed")]
    add_record(
        dataset="ruf_campus_catalog_2025",
        family="institution_reformed-university-fellowship",
        source_path=relative,
        locator=f"catalog-role:{index}:page:{row.get('catalog_page')}",
        printed_name=row["name_as_printed"],
        row=None,
        source_tier="official_institutional",
        completeness="complete_catalog_listed_campus_roles_2025_10_01",
        evidence_type="ruf_campus_role_snapshot",
        institutions=[value for value in institutions if value],
        location=row.get("location_as_printed"),
        backfill=False,
    )
'''
    if anchor not in text:
        raise SystemExit("crosswalk insertion anchor missing")
    crosswalk.write_text(text.replace(anchor, block + anchor, 1), encoding="utf-8")

validator = Path("scripts/validate-research-imports.py")
text = validator.read_text(encoding="utf-8")
anchor = '\n\nidentity = load("sources/normalized/identity/person-crosswalk.json")\n'
if "RUF campus catalog: expected 414 role rows" not in text:
    block = '''

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
'''
    if anchor not in text:
        raise SystemExit("validator insertion anchor missing")
    text = text.replace(anchor, block + anchor, 1)

identity_anchor = '''if not ruf_identity_summary or ruf_identity_summary.get("row_count") != 213:
    errors.append("identity summary: expected 213 RUF 2026 staff-transition rows")
'''
identity_add = identity_anchor + '''ruf_catalog_identity_summary = next((row for row in identity_datasets if row.get("source_dataset") == "ruf_campus_catalog_2025"), None)
if not ruf_catalog_identity_summary or ruf_catalog_identity_summary.get("row_count") != 414:
    errors.append("identity summary: expected 414 RUF 2025 campus-catalog rows")
'''
if "identity summary: expected 414 RUF 2025 campus-catalog rows" not in text:
    if identity_anchor not in text:
        raise SystemExit("identity validator insertion anchor missing")
    text = text.replace(identity_anchor, identity_add, 1)
validator.write_text(text, encoding="utf-8")
