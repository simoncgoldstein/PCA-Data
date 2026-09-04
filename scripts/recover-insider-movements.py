#!/usr/bin/env python3
from pathlib import Path
import json

# 1. Formal-position evidence index
ipath = Path('sources/normalized/general-assembly/formal-position-evidence-index.json')
idx = json.loads(ipath.read_text(encoding='utf-8'))
source_path = 'sources/normalized/general-assembly/2011-2014-insider-movements-formal-position-records.json'
entries = [
    {
        'evidence_id': '2012-scim-part-one-unanimous-report',
        'year': 2012,
        'topic': 'divine_familial_language_in_bible_translation',
        'evidence_class': 'signed_formal_report_or_minority_report',
        'path': source_path,
        'coverage': 'six printed Part One report names; report states SCIM unanimously presented Part One and its five recommendations',
        'important_boundary': 'Guy Waters was appointed for Part Two work but is not printed in the six-name Part One report group; do not back-project him into the Part One signature set.'
    },
    {
        'evidence_id': '2013-scim-committee-report',
        'year': 2013,
        'topic': 'insider_movements',
        'evidence_class': 'signed_formal_report_or_minority_report',
        'path': source_path,
        'coverage': 'five printed Committee Report signatories',
        'important_boundary': 'The 41st GA recommitted the entire matter after aggregate votes; no commissioner-level vote is inferred.'
    },
    {
        'evidence_id': '2013-scim-jabbour-minority-report',
        'year': 2013,
        'topic': 'insider_movements',
        'evidence_class': 'signed_formal_report_or_minority_report',
        'path': source_path,
        'coverage': 'Nabeel T. Jabbour as sole printed Minority Report 2013 signer/author',
        'important_boundary': 'Jabbour explicitly described his paper as concurring with most of the committee report while supplementing it; do not encode it as total rejection of the committee report.'
    },
    {
        'evidence_id': '2014-scim-committee-report',
        'year': 2014,
        'topic': 'insider_movements',
        'evidence_class': 'signed_formal_report_or_minority_report',
        'path': source_path,
        'coverage': 'five printed Committee Report signatories; 42nd GA adopted Committee Recommendations 1-3',
        'important_boundary': 'The PCA Historical Center explicitly cautions that only the three Committee Recommendations were adopted, not the report narrative as a constitutional statement.'
    },
    {
        'evidence_id': '2014-scim-jabbour-seelinger-minority-report',
        'year': 2014,
        'topic': 'insider_movements',
        'evidence_class': 'signed_formal_report_or_minority_report',
        'path': source_path,
        'coverage': 'Nabeel Jabbour and Tom Seelinger as the two printed 2014 minority-report signatories',
        'important_boundary': 'The 2014 minority signers stated that they did not support the 2013 minority report; keep the two minority reports as distinct person-position events.'
    },
]
existing = {row.get('evidence_id') for row in idx.get('normalized_position_sources', [])}
for row in entries:
    if row['evidence_id'] not in existing:
        idx.setdefault('normalized_position_sources', []).append(row)
for item in idx.get('priority_backlog', []):
    target = item.get('target', '')
    if 'Insider Movements' in target:
        item['target'] = target.replace('Insider Movements, ', '').replace(', Insider Movements', '').replace('Insider Movements', '').strip(' ,')
ipath.write_text(json.dumps(idx, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# 2. Identity crosswalk integration
bpath = Path('scripts/build-person-crosswalk.py')
text = bpath.read_text(encoding='utf-8')
marker = '# A Faithful PCA snapshots remain separate datasets but one source family.\n'
block = '''# 2011-2014 Insider Movements study-committee evidence. All report years,\n# majority/minority forms, and committee membership changes are one source\n# family so this longitudinal committee record cannot self-corroborate an\n# identity across its own repeated names.\nrelative = "sources/normalized/general-assembly/2011-2014-insider-movements-formal-position-records.json"\nscim_data = register_json(relative)\nfor event in scim_data.get("formal_positions", []):\n    for row in event.get("signers", []):\n        add_record(\n            dataset=f"formal_position_{event['event_id']}",\n            family="insider_movements_scim_2011_2014",\n            source_path=relative,\n            locator=f"{event['event_id']}:signer:{row['print_order']}",\n            printed_name=row["name_as_printed"],\n            row=row,\n            source_tier="official_primary",\n            completeness="complete_printed_report_signers",\n            evidence_type="formal_report_signature",\n            office=row.get("office_as_printed"),\n            existing_id=row.get("normalized_person_id"),\n        )\nfor index, row in enumerate(scim_data.get("named_report_roles", []), 1):\n    add_record(\n        dataset="insider_movements_named_report_roles_2013_2014",\n        family="insider_movements_scim_2011_2014",\n        source_path=relative,\n        locator=f"named_report_role:{index}:{row['year']}",\n        printed_name=row["name_as_printed"],\n        row=row,\n        source_tier="official_primary",\n        completeness="complete_named_floor_report_roles_in_normalized_family",\n        evidence_type="named_report_role",\n        office=row.get("office_as_printed"),\n        existing_id=row.get("normalized_person_id"),\n    )\nfor index, row in enumerate(scim_data.get("named_membership_changes", []), 1):\n    add_record(\n        dataset="insider_movements_committee_membership_changes_2012",\n        family="insider_movements_scim_2011_2014",\n        source_path=relative,\n        locator=f"membership_change:{index}",\n        printed_name=row["name_as_printed"],\n        row=row,\n        source_tier="official_primary",\n        completeness="complete_named_membership_changes_explicit_in_part_one_history",\n        evidence_type="study_committee_membership_change",\n        office=row.get("office_as_printed"),\n        existing_id=row.get("normalized_person_id"),\n    )\n\n\n'''
if 'relative = "sources/normalized/general-assembly/2011-2014-insider-movements-formal-position-records.json"' not in text:
    if marker not in text:
        raise SystemExit('crosswalk insertion marker missing')
    text = text.replace(marker, block + marker, 1)
bpath.write_text(text, encoding='utf-8')

# 3. Formal-position validator
vpath = Path('scripts/validate-formal-position-evidence.py')
v = vpath.read_text(encoding='utf-8')
load_anchor = 'subscription2002_gap = json.loads(subscription2002_gap_path.read_text(encoding="utf-8"))\n'
load_block = '''scim_path = root / "sources/normalized/general-assembly/2011-2014-insider-movements-formal-position-records.json"\nscim = json.loads(scim_path.read_text(encoding="utf-8"))\n'''
if 'scim_path = root / "sources/normalized/general-assembly/2011-2014-insider-movements-formal-position-records.json"' not in v:
    if load_anchor not in v:
        raise SystemExit('validator load anchor missing')
    v = v.replace(load_anchor, load_anchor + load_block, 1)

hierarchy_anchor = 'hierarchy = {row.get("evidence_class"): row for row in index.get("evidence_hierarchy", [])}\n'
checks = '''# 2011-2014 Insider Movements study-committee report family.\nif scim.get("metadata", {}).get("ideological_weight") != 0:\n    raise SystemExit("Insider Movements: ideological_weight must remain 0")\nif scim.get("metadata", {}).get("source_family") != "insider_movements_scim_2011_2014":\n    raise SystemExit("Insider Movements: source-family guardrail drift")\nscim_positions = {e.get("event_id"): e for e in scim.get("formal_positions", [])}\nexpected_scim = {\n    "2012-scim-part-one-unanimous-report": 6,\n    "2013-scim-committee-report": 5,\n    "2013-scim-jabbour-minority-report": 1,\n    "2014-scim-committee-report": 5,\n    "2014-scim-jabbour-seelinger-minority-report": 2,\n}\nif set(scim_positions) != set(expected_scim):\n    raise SystemExit(f"Insider Movements: formal-position event set drift: {sorted(scim_positions)}")\nfor event_id, count in expected_scim.items():\n    event = scim_positions[event_id]\n    if event.get("signer_count") != count or len(event.get("signers", [])) != count:\n        raise SystemExit(f"{event_id}: signer count drift")\n    if event.get("evidence_class") != "signed_formal_report_or_minority_report" or event.get("ideological_weight") != 0:\n        raise SystemExit(f"{event_id}: evidence semantics drift")\nif {r.get("name_as_printed") for r in scim_positions["2012-scim-part-one-unanimous-report"]["signers"]} != {"David B. Garner", "Robert Berman", "Nabeel T. Jabbour", "Jonathan Mitchell", "Bill Nikides", "Tom Seelinger"}:\n    raise SystemExit("2012 SCIM Part One: printed report group drift")\nif any(r.get("name_as_printed") == "Guy Waters" for r in scim_positions["2012-scim-part-one-unanimous-report"]["signers"]):\n    raise SystemExit("2012 SCIM Part One: do not back-project Guy Waters into the six-name printed Part One group")\nif {r.get("name_as_printed") for r in scim_positions["2013-scim-committee-report"]["signers"]} != {"David B. Garner", "Robert Berman", "Jonathan Mitchell", "Bill Nikides", "Guy Prentiss Waters"}:\n    raise SystemExit("2013 SCIM Committee Report: signer set drift")\nif {r.get("name_as_printed") for r in scim_positions["2013-scim-jabbour-minority-report"]["signers"]} != {"Nabeel T. Jabbour"}:\n    raise SystemExit("2013 SCIM Minority Report: Jabbour sole printed signer drift")\nif scim_positions["2013-scim-committee-report"].get("assembly_disposition", {}).get("minority_substitute_became_main_motion_vote") != {"for": 426, "against": 400}:\n    raise SystemExit("2013 SCIM: minority-substitute aggregate vote drift")\nif scim_positions["2013-scim-committee-report"].get("assembly_disposition", {}).get("recommit_vote") != {"for": 438, "against": 402}:\n    raise SystemExit("2013 SCIM: recommit aggregate vote drift")\nif {r.get("name_as_printed") for r in scim_positions["2014-scim-committee-report"]["signers"]} != {"David B. Garner", "Robert Berman", "Jonathan Mitchell", "Bill Nikides", "Guy Prentiss Waters"}:\n    raise SystemExit("2014 SCIM Committee Report: signer set drift")\nif {r.get("name_as_printed") for r in scim_positions["2014-scim-jabbour-seelinger-minority-report"]["signers"]} != {"Nabeel Jabbour", "Tom Seelinger"}:\n    raise SystemExit("2014 SCIM Minority Report: signer set drift")\nif scim_positions["2014-scim-committee-report"].get("assembly_disposition", {}).get("status") != "committee_recommendations_1_through_3_adopted":\n    raise SystemExit("2014 SCIM: adopted recommendation boundary drift")\nif scim_positions["2014-scim-committee-report"].get("assembly_disposition", {}).get("minority_report_status") != "defeated_as_substitute":\n    raise SystemExit("2014 SCIM: minority disposition drift")\ndiscrepancies = {d.get("issue_id"): d for d in scim.get("source_discrepancies_and_guardrails", [])}\nif "2013-tom-seelinger-role-discrepancy" not in discrepancies or "Do not infer" not in discrepancies["2013-tom-seelinger-role-discrepancy"].get("rule", ""):\n    raise SystemExit("SCIM: 2013 Tom Seelinger source discrepancy guardrail missing")\nchanges = {r.get("name_as_printed"): r for r in scim.get("named_membership_changes", [])}\nif set(changes) != {"Wade Bradshaw", "David Garner", "Guy Waters"}:\n    raise SystemExit("SCIM: 2012 named membership-change set drift")\n\n'''
if '# 2011-2014 Insider Movements study-committee report family.' not in v:
    if hierarchy_anchor not in v:
        raise SystemExit('validator hierarchy anchor missing')
    v = v.replace(hierarchy_anchor, checks + hierarchy_anchor, 1)

required_anchor = '    "2001-wim-consensus-report",\n'
required_ids = ''.join(f'    "{eid}",\n' for eid in [
    '2012-scim-part-one-unanimous-report',
    '2013-scim-committee-report',
    '2013-scim-jabbour-minority-report',
    '2014-scim-committee-report',
    '2014-scim-jabbour-seelinger-minority-report',
])
if '    "2012-scim-part-one-unanimous-report",\n' not in v:
    if required_anchor not in v:
        raise SystemExit('validator required-index anchor missing')
    v = v.replace(required_anchor, required_ids + required_anchor, 1)
vpath.write_text(v, encoding='utf-8')
