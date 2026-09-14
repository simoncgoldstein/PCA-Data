#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


expected = {
    'Ben Lyon': {'id': 'ben-lyon', 'o15': 118, 'nae': 114},
    "Bruce O'Neil": {'id': 'bruce-o-neil', 'o15': 130},
    'Bruce Terrell': {'id': 'bruce-terrell', 'o15': 178},
    'Jeremy Fair': {'id': 'jeremy-fair', 'o15': 50, 'nae': 47},
    'Justin Edgar': {'id': 'justin-edgar', 'o15': 46},
    'Luke Evans': {'id': 'luke-evans', 'o15': 49},
    'Omar Ortiz': {'id': 'omar-ortiz', 'o15': 131, 'nae': 126},
    'Peter Rowan': {'id': 'peter-rowan', 'o15': 149, 'nae': 148},
    'Rob Wootton': {'id': 'rob-wootton', 'o15': 196},
    'Tim LeCroy': {'id': 'tim-lecroy', 'o15': 103},
    'Nate Conrad': {'id': 'nate-conrad', 'nae': 33},
}

receipt = load('sources/raw/identity/np-postarchive-identity-evidence-batch1-2026-09-14.json')
if receipt.get('status') != 'reviewed_canonical_identity_evidence':
    raise SystemExit('unexpected receipt status')
if receipt.get('approved_identity_count') != len(expected):
    raise SystemExit('approved identity count drift')
records = {row['name_as_printed']: row for row in receipt.get('evidence', [])}
if set(records) != set(expected):
    raise SystemExit('receipt person set drift')
for name, spec in expected.items():
    row = records[name]
    if row.get('canonical_person_id') != spec['id']:
        raise SystemExit(f'receipt canonical id mismatch: {name}')
    if row.get('review_state') != 'approved_for_canonical_application':
        raise SystemExit(f'receipt review state mismatch: {name}')
    if not row.get('identity_reasoning'):
        raise SystemExit(f'missing identity reasoning: {name}')
    if not row.get('independent_sources'):
        raise SystemExit(f'missing independent evidence: {name}')

# Preserve the two nonstandard/conflicting archival-context boundaries.
if records['Jeremy Fair']['np_context']['presbytery_as_printed'] != 'North Texas':
    raise SystemExit('Jeremy Fair NP archival label must remain as printed')
if 'does not certify' not in records['Jeremy Fair']['identity_reasoning'] and 'stale' not in records['Jeremy Fair']['identity_reasoning']:
    raise SystemExit('Jeremy Fair source-label caveat missing')
if records['Justin Edgar']['np_context']['presbytery_as_printed'] != 'Build That Wall Presbytery':
    raise SystemExit('Justin Edgar NP archival wording must remain verbatim')
if 'does not validate' not in records['Justin Edgar']['identity_reasoning']:
    raise SystemExit('Justin Edgar source-label caveat missing')

people = {row['id']: row for row in load('data/people.json')}
for name, spec in expected.items():
    person = people.get(spec['id'])
    if not person:
        raise SystemExit(f'missing canonical person: {name}')
    if person.get('profile_status') != 'source_assessed':
        raise SystemExit(f'reviewed person must be durable source_assessed seed: {name}')

np_data = load('sources/normalized/national-partnership/confirmed-memberships-canonical.json')
np_rows = {row['normalized_name_key']: row for row in np_data['confirmed_members']}
for name, spec in expected.items():
    key = name.lower().replace("'", ' ').replace('’', ' ')
    key = ' '.join(key.split())
    row = np_rows.get(key)
    if not row or row.get('normalized_person_id') != spec['id']:
        raise SystemExit(f'NP canonical link missing: {name}')

# Validate the exact official 2022 action rows that were reviewed.
o15 = load('sources/normalized/revoice/overture-15-negative-votes-2022.json')
o15_by_order = {row['print_order']: row for row in o15['negative_votes']}
nae = load('sources/normalized/nae/withdrawal-protest-signers-2022.json')
nae_by_order = {row['print_order']: row for row in nae['signers']}
for name, spec in expected.items():
    if 'o15' in spec:
        row = o15_by_order[spec['o15']]
        if row.get('normalized_person_id') != spec['id']:
            raise SystemExit(f'O15 canonical link missing: {name}')
    if 'nae' in spec:
        row = nae_by_order[spec['nae']]
        if row.get('normalized_person_id') != spec['id']:
            raise SystemExit(f'NAE canonical link missing: {name}')

continuity = load('analysis/national-partnership/continuity-summary.json')
cohort = continuity['national_partnership_cohort']
if cohort.get('printed_confirmed_member_name_count') != 151:
    raise SystemExit('NP roster denominator drift')
# This validator protects the batch-1 floor, not a permanent global ceiling.
# Later reviewed identity batches may legitimately increase canonical coverage.
if cohort.get('confirmed_canonical_person_count', 0) < 54:
    raise SystemExit(f"canonical NP coverage regressed below batch-1 floor: {cohort.get('confirmed_canonical_person_count')}")
if cohort.get('identity_resolution_rate_pct', 0) < 35.76:
    raise SystemExit('NP identity-resolution rate regressed below batch-1 floor')
tracked = {row['dataset']: row for row in continuity['tracked_datasets']}
o15_signal = tracked['overture_15_negative_votes_2022']
nae_signal = tracked['nae_withdrawal_protest_2022']
for label, row, minimum_overlap in [
    ('O15', o15_signal, 20),
    ('NAE', nae_signal, 10),
]:
    if row.get('confirmed_overlap_count', 0) < minimum_overlap:
        raise SystemExit(f'{label} confirmed overlap regressed below batch-1 floor')
    if row.get('unresolved_exact_name_possible_overlap_count') != 0:
        raise SystemExit(f'{label} targeted exact-name queue should remain exhausted')

if o15_signal.get('confirmed_lower_bound_share_of_target_printed_roster_pct', 0) < 10.0:
    raise SystemExit('O15 full-roster lower bound regressed')
if nae_signal.get('confirmed_lower_bound_share_of_target_printed_roster_pct', 0) < 4.93:
    raise SystemExit('NAE full-roster lower bound regressed')

# The analysis must retain its no-risk-ratio guardrail after coverage improves.
readiness = continuity['predictive_validity_readiness']
if readiness.get('status') != 'not_ready_for_risk_ratio_odds_ratio_or_causal_claim':
    raise SystemExit('predictive-validity guardrail regressed')
if 'Do not calculate' not in readiness.get('forbidden_shortcut', ''):
    raise SystemExit('forbidden shortcut guardrail missing')

print(json.dumps({
    'status': 'ok',
    'reviewed_identities': len(expected),
    'np_canonical_people': cohort['confirmed_canonical_person_count'],
    'o15_confirmed_np_overlap': o15_signal['confirmed_overlap_count'],
    'nae_confirmed_np_overlap': nae_signal['confirmed_overlap_count'],
    'o15_possible_exact_name_queue': o15_signal['unresolved_exact_name_possible_overlap_count'],
    'nae_possible_exact_name_queue': nae_signal['unresolved_exact_name_possible_overlap_count'],
}, indent=2))
