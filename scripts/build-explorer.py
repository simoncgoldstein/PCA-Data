#!/usr/bin/env python3
"""Deterministic presentation projection. Never creates identities or score edges."""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
def load(path):
    return json.loads((ROOT / path).read_text())
def write(path, data):
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

# Explicit presentation associations, not inferred memberships or new actions.
LINKS = {
    'national_partnership_confirmed_members': ('National Partnership confirmed membership', 'organization', 'national-partnership', ['src-np-local-archive', 'src-np-index']),
    'amr_leadership_current': ('AMR current core leadership', 'organization', 'amr', ['src-amr-team-2026']),
    'garris_letter_1': ('Garris Letter 1 · 2024', 'event', 'evt-garris-letter-1', ['src-garris-letter-1']),
    'garris_letter_2': ('Garris Letter 2 · 2024', 'event', 'evt-garris-letter-2', ['src-garris-letter-2']),
    'a_faithful_pca_2021-06-11': ('A Faithful PCA · June 2021 snapshot', 'event', 'evt-a-faithful-pca-2021', ['src-a-faithful-pca-letter-2021']),
    'a_faithful_pca_2022-03-14': ('A Faithful PCA · March 2022 cumulative snapshot', 'event', 'evt-a-faithful-pca-2021', ['src-a-faithful-pca-signers-wayback']),
    'warhurst_protest_2019': ('Warhurst protest · 2019', 'event', 'evt-warhurst-protest-2019', ['src-ga47-2019']),
    'nae_withdrawal_protest_2022': ('NAE withdrawal protest · 2022', 'event', 'evt-nae-withdrawal-protest-2022', ['src-ga49-vol1-nae']),
    'overture_15_negative_votes_2022': ('Overture 15 · recorded negative votes, 2022', 'event', 'evt-overture15-2022', ['src-ga49-2022']),
    'overture_15_minority_2022': ('Overture 15 · minority report, 2022', 'event', 'evt-overture15-2022', ['src-ga49-2022']),
    'overture_37_negative_votes_2021': ('Overture 37 · recorded negative votes, 2021', 'event', 'evt-overture37-2021', ['src-ga48-2021']),
    'overture_37_minority_2021': ('Overture 37 · minority report, 2021', 'event', 'evt-overture37-2021', ['src-ga48-2021']),
    'human_sexuality_aic_2019_2021': ('Human Sexuality study committee · 2019–2021', 'event', 'evt-human-sexuality-aic', ['src-ga48-2021']),
}
people = {p['id'] for p in load('data/people.json')}
records = load('sources/normalized/identity/person-crosswalk.json')['records']
coverage = {d['source_dataset']: d for d in load('analysis/overlap/dataset-coverage.json')['datasets']}
by_dataset = defaultdict(list)
cache = {}
letters = {f"garris_letter_{i}": letter for i, letter in enumerate(load('sources/normalized/public-statements/garris-letters-2024.json')['letters'], 1)}

def original_row(r):
    """Recover exact printed fields for supported source shapes, never fuzzy-match."""
    path = r['source_path']
    if path not in cache:
        cache[path] = load(path)
    data = cache[path]
    if r['source_dataset'] in letters:
        rows = letters[r['source_dataset']]['signers']
    elif r['source_dataset'] == 'national_partnership_confirmed_members':
        return next(x for x in data['confirmed_members'] if x['canonical_name'] == r['name_as_printed'])
    else:
        rows = data.get('signers', data.get('voters', [])) if isinstance(data, dict) else data
    # Match a source sequence AND printed name. No identity inference occurs here.
    loc = r['source_row_locator'].split(':')
    for row in rows:
        if not isinstance(row, dict):
            continue
        n = row.get('print_order', row.get('sequence'))
        if str(n) in loc and row.get('name_as_printed') == r['name_as_printed']:
            return row
    return None

for r in records:
    dataset = r['source_dataset']
    pid = r['canonical_person_id'] if r['match_status'] in {'exact_confirmed', 'context_confirmed'} else None
    assert pid is None or pid in people
    original = original_row(r)
    entry = {
        'id': r['crosswalk_id'], 'dataset_id': dataset,
        'event_id': LINKS[dataset][2] if dataset in LINKS and LINKS[dataset][1] == 'event' else None,
        'source_ids': LINKS.get(dataset, (None, None, None, []))[3],
        'name_as_printed': r['name_as_printed'], 'person_id': pid,
        'identity_status': 'resolved' if pid else 'unresolved',
        'identity_review_status': r['match_status'],
        'source_path': r['source_path'], 'source_locator': r['source_row_locator'],
        'evidence_kind': r['evidence_type'],
        'context_normalized': {'office': r.get('office'), 'institutions': r.get('institutions', []), 'presbyteries': r.get('presbyteries', [])},
        'identity_notes': r.get('reviewer_note'), 'conflicts': r.get('conflicting_fields', []),
    }
    if original:
        # Retain source-specific fields and archival receipts; omit only resolver fields.
        entry['printed_record'] = {k:v for k,v in original.items() if k not in {'normalized_person_id','normalized_name_candidate','normalized_name_key'}}
        entry['print_order'] = original.get('print_order', original.get('sequence'))
    by_dataset[dataset].append(entry)

datasets = []
for key, rows in sorted(by_dataset.items()):
    rows.sort(key=lambda r: (r.get('print_order') or 0, r['source_locator']))
    label, target_type, target_id, source_ids = LINKS.get(key, (key.replace('_',' ').replace('-', ' ').title(), None, None, []))
    c = coverage[key]
    datasets.append({'id':key, 'label':label, 'target_type':target_type, 'target_id':target_id, 'source_ids':source_ids,
        'row_count':len(rows), 'resolved_rows':sum(bool(r['person_id']) for r in rows),
        'canonical_people':len({r['person_id'] for r in rows if r['person_id']}),
        'unique_printed_names':c['unique_printed_name_count'], 'completeness':c['completeness_status'],
        'source_paths':sorted({r['source_path'] for r in rows}),
        'boundary': ('Cumulative snapshot of the 2021 action. These two snapshots are not independent actions.' if key.startswith('a_faithful_pca') else
          'Identity-verification receipt, not an additional signature or action.' if key == 'garris_letter_2_identity_verification' else
          'This is the source scope represented in the identity crosswalk, not necessarily a complete institutional or historical population.')})

# Separately attributable positions, preserved as unscored presentation records.
path = 'sources/normalized/general-assembly/2012-2019-women-serving-member-authored-positions.json'
authored = load(path)
extra_sources = []
for s in authored['sources']:
    extra_sources.append({'id':'authored-'+s['source_id'], 'title':s['title'], 'source_type':s['source_type'],
        'url':s.get('url',s.get('primary_first_party_republication_url')), 'publisher':s.get('publisher',s.get('author_as_printed')),
        'date':s.get('original_publication_date',s.get('published_on',s.get('excerpt_published_on'))),
        'notes':s.get('notes'), 'provenance_path':path})
positions = [{**p, 'id':p['position_id'], 'person_id':p['normalized_person_id'], 'source_ids':['authored-'+p['source_id']],
    'evidence_kind':'attributable_position', 'score_included':False, 'weight':0, 'source_path':path,
    'attribution_basis':p['evidence_class']} for p in authored['positions']]
# Public advocacy is distinct from the separately scored dissent and floor report.
path = 'sources/normalized/general-assembly/2026-overture-37-women-deacons-formal-actions.json'
o37 = load(path)
adv = o37['jeffrey_choi_actions'][0]
extra_sources.append({'id':'explorer-choi-advocacy-2026','title':'Polity Matters: Polity Nerds Stick Together','url':adv['source_url'],'date':adv['source_date'],'source_type':'first_person_public_advocacy','provenance_path':path})
positions.append({'id':adv['action_id'],'person_id':adv['normalized_person_id'],'topic':adv['role'],'summary':adv['fact'],
    'important_boundary':o37['overture']['important_boundary'],'source_ids':['explorer-choi-advocacy-2026'],
    'source_locators':['Episode 122'], 'evidence_kind':'attributable_position','score_included':False,'weight':0,
    'source_path':path, 'attribution_basis':'Documented public advocacy', 'confidence':adv['confidence']})
identity_reviews = []
for receipt_path in [
    'sources/raw/identity/np-residual-identity-evidence-batch2-2026-09-14.json',
    'sources/raw/identity/np-postarchive-identity-evidence-batch1-2026-09-14.json',
]:
    receipt = load(receipt_path)
    for row in receipt.get('evidence', []):
        if row.get('canonical_person_id') in people and row.get('boundary'):
            identity_reviews.append({'person_id':row['canonical_person_id'], 'boundary':row['boundary'],
                'reasoning':row.get('identity_reasoning'), 'source_path':receipt_path})
write('data/explorer.json', {'schema_version':1,'identity_reviews':identity_reviews,'datasets':datasets,'positions':positions,'sources':extra_sources,
    'contract':'Source occurrences are not canonical affiliations. They never change the Network Involvement Index.'})
write('data/source-occurrences.json', {'schema_version':1,'datasets':by_dataset})
print(f'Projected {len(datasets)} datasets, {len(records)} source occurrences, {len(positions)} attributable positions; no canonical mutations.')
