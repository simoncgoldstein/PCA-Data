#!/usr/bin/env python3
"""Protect source-row completeness, identity boundaries, and presentation provenance."""
import json
import sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
def load(p):return json.loads((root/p).read_text())
x=load('data/explorer.json'); rows=load('data/source-occurrences.json')['datasets']
people={p['id'] for p in load('data/people.json')}; sources={s['id'] for s in load('data/sources.json')+x['sources']}
records={r['crosswalk_id']:r for r in load('sources/normalized/identity/person-crosswalk.json')['records']}
assert sum(map(len,rows.values()))==len(records)
for d in x['datasets']:
 rs=rows[d['id']]
 assert len(rs)==d['row_count']
 assert sum(bool(r['person_id']) for r in rs)==d['resolved_rows']
 assert len({r['person_id'] for r in rs if r['person_id']})==d['canonical_people']
 assert set(d['source_ids'])<=sources
 for r in rs:
  c=records[r['id']]
  expected=c['canonical_person_id'] if c['match_status'] in {'exact_confirmed','context_confirmed'} else None
  assert r['person_id']==expected and (expected is None or expected in people)
  assert r['name_as_printed']==c['name_as_printed']
  assert r['source_locator']==c['source_row_locator']
  assert (root/r['source_path']).is_file()
  assert 'score_included' not in r and 'weight' not in r
for i,total,resolved in [(1,60,25),(2,21,21)]:
 rs=rows[f'garris_letter_{i}']; assert len(rs)==total
 assert sum(bool(r['person_id']) for r in rs)==resolved
 assert sorted(r['print_order'] for r in rs)==list(range(1,total+1))
 for r in rs:
  assert r['printed_record']['name_as_printed']==r['name_as_printed']
  assert r['event_id']==f'evt-garris-letter-{i}'
  assert r['source_ids']==[f'src-garris-letter-{i}']
a=next(r for r in rows['garris_letter_1'] if r['name_as_printed']=='Jeff White')
b=next(r for r in rows['garris_letter_2'] if r['name_as_printed']=='Jeff White')
assert a['person_id'] is None and a['printed_record']['presbytery_as_printed']=='Rio Grande'
assert b['person_id']=='jeff-white-redeemer-downtown'
h=next(r for r in rows['warhurst_protest_2019'] if r['person_id']=='hansoo-jin')
assert h['printed_record']['presbytery_as_printed']=='Korean Capitol'
np=next(d for d in x['datasets'] if d['id']=='national_partnership_confirmed_members')
assert (np['row_count'],np['canonical_people'])==(151,68)
assert all('not independent' in d['boundary'] for d in x['datasets'] if d['id'].startswith('a_faithful_pca'))
for p in x['positions']:
 assert p['person_id'] in people and p['weight']==0 and p['score_included'] is False
 assert set(p['source_ids'])<=sources and p['important_boundary']
assert any(p['person_id']=='jeffrey-choi' for p in x['positions'])
assert any(p['person_id']=='kathy-keller' for p in x['positions'])
assert not any(p['person_id']=='tim-keller' for p in x['positions'])
assert any(r['person_id']=='tag-tuck' and 'discrepancy' in r['boundary'] for r in x['identity_reviews'])
print(f'Explorer contract validated: {len(records)} source rows, {len(x["datasets"])} datasets, inference boundaries intact.')
