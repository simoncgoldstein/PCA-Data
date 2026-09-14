#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


expected = {
    'David Lindberg': {
        'id': 'david-lindberg',
        'garris_order': 32,
        'np_presbytery': 'Metro Atlanta',
        'garris_presbytery': 'North Texas',
    },
    'David Richmon': {
        'id': 'david-richmon',
        'garris_order': 39,
        'np_presbytery': 'PNW',
        'garris_presbytery': 'Pacific NW',
    },
}

receipt = load('sources/raw/identity/np-garris-continuity-identity-evidence-batch1-2026-09-14.json')
if receipt.get('status') != 'reviewed_canonical_identity_evidence':
    raise SystemExit('unexpected identity receipt status')
if receipt.get('approved_identity_count') != 2:
    raise SystemExit('reviewed identity count drift')
records = {row['name_as_printed']: row for row in receipt.get('evidence', [])}
if set(records) != set(expected):
    raise SystemExit('identity receipt person set drift')
for name, spec in expected.items():
    row = records[name]
    if row.get('canonical_person_id') != spec['id']:
        raise SystemExit(f'receipt canonical id mismatch: {name}')
    if row.get('review_state') != 'approved_for_canonical_application':
        raise SystemExit(f'receipt review state mismatch: {name}')
    if row.get('np_context', {}).get('presbytery_as_printed') != spec['np_presbytery']:
        raise SystemExit(f'NP historical context drift: {name}')
    if row.get('garris_letter_1', {}).get('presbytery_as_printed') != spec['garris_presbytery']:
        raise SystemExit(f'Garris context drift: {name}')
    if len(row.get('independent_sources', [])) < 3:
        raise SystemExit(f'insufficient independent identity evidence recorded: {name}')

# Lindberg's presbytery change must remain explicit rather than rewritten as a
# same-context match.
lindberg_reasoning = records['David Lindberg'].get('identity_reasoning', '').lower()
if 'presbytery change' not in lindberg_reasoning:
    raise SystemExit('Lindberg historical-presbytery boundary missing')

people = {row['id']: row for row in load('data/people.json')}
for name, spec in expected.items():
    person = people.get(spec['id'])
    if not person or person.get('name') != name:
        raise SystemExit(f'missing canonical person seed: {name}')
    if person.get('profile_status') != 'source_assessed':
        raise SystemExit(f'reviewed person must be durable source_assessed seed: {name}')

np_data = load('sources/normalized/national-partnership/confirmed-memberships-canonical.json')
np_rows = {row['canonical_name']: row for row in np_data['confirmed_members']}
for name, spec in expected.items():
    row = np_rows.get(name)
    if not row or row.get('normalized_person_id') != spec['id']:
        raise SystemExit(f'NP canonical link missing: {name}')
    evidence = row.get('evidence', [])
    if not any(item.get('presbytery_as_printed') == spec['np_presbytery'] for item in evidence):
        raise SystemExit(f'NP source context missing: {name}')

garris = load('sources/normalized/public-statements/garris-letters-2024.json')
letter1 = next(row for row in garris['letters'] if row['letter_id'] == 'garris-letter-1')
garris_by_order = {row['print_order']: row for row in letter1['signers']}
for name, spec in expected.items():
    row = garris_by_order[spec['garris_order']]
    if row.get('name_as_printed') != name or row.get('normalized_person_id') != spec['id']:
        raise SystemExit(f'Garris canonical link missing: {name}')

# Existing critical same-name safeguard must remain intact.
letter1_jeff = next(row for row in letter1['signers'] if row['name_as_printed'] == 'Jeff White')
if letter1_jeff.get('normalized_person_id') is not None:
    raise SystemExit('Letter 1 Jeff White boundary regressed')

app_affiliations = load('data/affiliations.json')
for name, spec in expected.items():
    matches = [
        row for row in app_affiliations
        if row.get('person_id') == spec['id'] and row.get('target_id') == 'evt-garris-letter-1'
    ]
    if len(matches) != 1:
        raise SystemExit(f'expected exactly one Garris app edge: {name}')
    edge = matches[0]
    if edge.get('evidence_kind') != 'public_coalition_action' or edge.get('weight') != 3 or edge.get('score_included') is not True:
        raise SystemExit(f'Garris scoring semantics drift: {name}')

continuity = load('analysis/national-partnership/continuity-summary.json')
cohort = continuity['national_partnership_cohort']
if cohort.get('printed_confirmed_member_name_count') != 151:
    raise SystemExit('NP printed roster denominator drift')
if cohort.get('confirmed_canonical_person_count') != 45:
    raise SystemExit('NP canonical coverage expected 45 after reviewed batch')
if cohort.get('identity_resolution_rate_pct') != 29.8:
    raise SystemExit('NP canonical resolution rate drift')
garris_signal = continuity['headline_descriptive_signals']['garris_letter_1_recurrence']
expected_signal = {
    'confirmed_overlap': 10,
    'garris1_confirmed_people': 25,
    'confirmed_np_share_of_resolved_garris1_pct': 40.0,
    'garris1_full_roster_lower_bound_pct': 16.67,
}
for key, value in expected_signal.items():
    if garris_signal.get(key) != value:
        raise SystemExit(f'NP/Garris continuity metric drift: {key} expected={value} actual={garris_signal.get(key)}')

tracked = {row['dataset']: row for row in continuity['tracked_datasets']}
np_garris = tracked['garris_letter_1']
if np_garris.get('unresolved_exact_name_possible_overlap_count') != 0:
    raise SystemExit('targeted NP/Garris exact-name queue should be exhausted after reviewed batch')
shared_ids = {row['canonical_person_id'] for row in np_garris.get('confirmed_shared_people', [])}
for spec in expected.values():
    if spec['id'] not in shared_ids:
        raise SystemExit(f'continuity shared-person list missing {spec["id"]}')

print(json.dumps({
    'status': 'ok',
    'reviewed_identities': 2,
    'np_canonical_people': cohort['confirmed_canonical_person_count'],
    'garris1_canonical_people': garris_signal['garris1_confirmed_people'],
    'np_garris1_confirmed_overlap': garris_signal['confirmed_overlap'],
    'np_garris1_full_roster_lower_bound_pct': garris_signal['garris1_full_roster_lower_bound_pct'],
}, indent=2))
