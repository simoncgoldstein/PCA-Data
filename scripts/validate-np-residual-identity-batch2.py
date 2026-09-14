#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def norm_name(value: str) -> str:
    value = (value or '').lower().replace('’', "'")
    words = re.findall(r'[a-z0-9]+', value)
    while words and words[0] in {'rev', 'reverend', 'dr', 'doctor', 'te', 're'}:
        words.pop(0)
    return ' '.join(words)


receipt = load('sources/raw/identity/np-residual-identity-evidence-batch2-2026-09-14.json')
if receipt.get('status') != 'reviewed_canonical_identity_evidence':
    raise SystemExit('unexpected residual identity receipt status')
if receipt.get('approved_identity_count') != 18:
    raise SystemExit('expected 18 reviewed residual identity decisions')
if receipt.get('canonical_np_links_added_count') != 14:
    raise SystemExit('expected 14 new canonical NP links in residual batch')

records = receipt.get('evidence', [])
if len(records) != 18:
    raise SystemExit('residual evidence row count drift')
by_key = {norm_name(row['name_as_printed']): row for row in records}
if len(by_key) != 18:
    raise SystemExit('duplicate normalized names in residual receipt')
for key, row in by_key.items():
    if row.get('review_state') != 'approved_for_canonical_application':
        raise SystemExit(f'unapproved residual identity: {key}')
    if not row.get('canonical_person_id'):
        raise SystemExit(f'missing canonical id in residual receipt: {key}')

people = {row['id']: row for row in load('data/people.json')}
for key, row in by_key.items():
    person_id = row['canonical_person_id']
    if person_id not in people:
        raise SystemExit(f'reviewed person missing from data/people.json: {person_id}')

np_rows = load('sources/normalized/national-partnership/confirmed-memberships-canonical.json')['confirmed_members']
np_by_key = {row['normalized_name_key']: row for row in np_rows}
for key, row in by_key.items():
    expected_id = row['canonical_person_id']
    np_row = np_by_key.get(key)
    if not np_row or np_row.get('normalized_person_id') != expected_id:
        raise SystemExit(f'canonical NP link missing or wrong: {key}')

# Confirm the three target source families use the reviewed identities where the
# receipt says they recur. Printed source context must remain untouched.
target_paths = {
    'a_faithful_pca_2021-06-11': ('sources/normalized/public-statements/a-faithful-pca/signers-2021-06-11.json', 'signers'),
    'a_faithful_pca_2022-03-14': ('sources/normalized/public-statements/a-faithful-pca/signers-2022-03-14.json', 'signers'),
    'warhurst_protest_2019': ('sources/normalized/revoice/warhurst-protest-signers-2019.json', 'signers'),
}
loaded_targets = {dataset: load(path)[row_key] for dataset, (path, row_key) in target_paths.items()}
for row in records:
    expected_id = row['canonical_person_id']
    key = norm_name(row['name_as_printed'])
    for context in row.get('target_contexts', []):
        dataset = context.get('dataset')
        if dataset not in loaded_targets:
            continue
        matches = [r for r in loaded_targets[dataset] if norm_name(r.get('name_as_printed', '')) == key]
        if not matches:
            raise SystemExit(f'missing target source row for {key} in {dataset}')
        if not any(r.get('normalized_person_id') == expected_id for r in matches):
            raise SystemExit(f'target source row not canonicalized for {key} in {dataset}')

# Hansoo Jin is the final Warhurst residual closed by this batch. Preserve the
# source's "Korean Capitol" spelling while linking the person to hansoo-jin.
warhurst = loaded_targets['warhurst_protest_2019']
hansoo = [row for row in warhurst if row.get('name_as_printed') == 'Hansoo Jin']
if len(hansoo) != 1:
    raise SystemExit('expected exactly one Hansoo Jin Warhurst row')
if hansoo[0].get('normalized_person_id') != 'hansoo-jin':
    raise SystemExit('Hansoo Jin Warhurst row not canonicalized')
if hansoo[0].get('presbytery_as_printed') != 'Korean Capitol':
    raise SystemExit('Hansoo Jin printed presbytery spelling was rewritten')

# Preserve reviewed source conflicts instead of harmonizing them away.
tag_tuck = by_key.get('tag tuck')
if not tag_tuck or 'conflict' not in (tag_tuck.get('boundary') or '').lower() and 'conflict' not in json.dumps(tag_tuck).lower():
    raise SystemExit('Tag Tuck TE/RE source-conflict guardrail missing')
ridenhour = by_key.get('david ridenhour')
if not ridenhour or 'does not certify' not in (ridenhour.get('boundary') or '').lower():
    raise SystemExit('David Ridenhour source-label boundary missing')

continuity = load('analysis/national-partnership/continuity-summary.json')
cohort = continuity['national_partnership_cohort']
if cohort.get('printed_confirmed_member_name_count') != 151:
    raise SystemExit('NP printed roster denominator drift')
if cohort.get('confirmed_canonical_person_count', 0) < 68:
    raise SystemExit('NP canonical coverage regressed below residual-batch floor')

tracked = {row['dataset']: row for row in continuity['tracked_datasets']}
expectations = {
    'a_faithful_pca_2021-06-11': (50, 0),
    'a_faithful_pca_2022-03-14': (54, 0),
    'warhurst_protest_2019': (31, 0),
}
for dataset, (minimum_overlap, expected_possible) in expectations.items():
    row = tracked.get(dataset)
    if not row:
        raise SystemExit(f'missing tracked continuity row: {dataset}')
    if row.get('confirmed_overlap_count', 0) < minimum_overlap:
        raise SystemExit(f'confirmed overlap regressed for {dataset}')
    if row.get('unresolved_exact_name_possible_overlap_count') != expected_possible:
        raise SystemExit(f'exact-name residual queue not closed for {dataset}')

# Every canonical NP member must be represented exactly once in the app graph.
affiliations = load('data/affiliations.json')
canonical_np_ids = {row['normalized_person_id'] for row in np_rows if row.get('normalized_person_id')}
app_np_edges: dict[str, list[dict]] = {}
for edge in affiliations:
    if edge.get('target_type') == 'organization' and edge.get('target_id') == 'national-partnership':
        app_np_edges.setdefault(edge.get('person_id'), []).append(edge)
missing = sorted(canonical_np_ids - set(app_np_edges))
duplicates = sorted(pid for pid in canonical_np_ids if len(app_np_edges.get(pid, [])) != 1)
if missing or duplicates:
    raise SystemExit(f'NP app projection mismatch: missing={missing}, duplicates={duplicates}')
for pid in canonical_np_ids:
    edge = app_np_edges[pid][0]
    if edge.get('confidence') != 'confirmed' or edge.get('weight') != 4 or edge.get('score_included') is not True:
        raise SystemExit(f'NP app membership semantics drift: {pid}')

# Pairwise CSV must agree with the continuity closure for the three reviewed targets.
with (ROOT / 'analysis/overlap/pairwise-overlap.csv').open(newline='', encoding='utf-8') as handle:
    pair_rows = list(csv.DictReader(handle))
for dataset, (minimum_overlap, expected_possible) in expectations.items():
    pair = next((row for row in pair_rows if {row['dataset_a'], row['dataset_b']} == {'national_partnership_confirmed_members', dataset}), None)
    if not pair:
        raise SystemExit(f'missing pairwise row for {dataset}')
    if int(pair['confirmed_intersection_count']) < minimum_overlap:
        raise SystemExit(f'pairwise confirmed overlap regressed for {dataset}')
    if int(pair['unresolved_possible_overlap_count']) != expected_possible:
        raise SystemExit(f'pairwise residual queue not closed for {dataset}')

print(json.dumps({
    'status': 'ok',
    'reviewed_identity_decisions': len(records),
    'canonical_np_people': len(canonical_np_ids),
    'afp_2021_np_overlap': tracked['a_faithful_pca_2021-06-11']['confirmed_overlap_count'],
    'afp_2022_np_overlap': tracked['a_faithful_pca_2022-03-14']['confirmed_overlap_count'],
    'warhurst_np_overlap': tracked['warhurst_protest_2019']['confirmed_overlap_count'],
    'closed_exact_name_queues': 3,
}, indent=2))
