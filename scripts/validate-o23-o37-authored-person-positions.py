#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
path = root / 'sources/normalized/general-assembly/2021-o23-o37-authored-person-positions.json'
data = json.loads(path.read_text())

assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 4
assert all(p['ideological_weight'] == 0 for p in positions)
assert all(p['evidence_type'] == 'direct_authored_position' for p in positions)
assert all(p['normalized_person_id'] is None for p in positions)

by_id = {p['position_id']: p for p in positions}
assert set(by_id) == {
    'jon-payne-o23-support-2021',
    'jon-payne-o37-support-2021',
    'david-coffin-o23-oppose-2021',
    'david-coffin-o37-oppose-2021',
}

assert by_id['jon-payne-o23-support-2021']['stance'] == 'support'
assert by_id['jon-payne-o37-support-2021']['stance'] == 'support'
assert by_id['david-coffin-o23-oppose-2021']['stance'] == 'oppose'
assert by_id['david-coffin-o37-oppose-2021']['stance'] == 'oppose'

assert by_id['jon-payne-o23-support-2021']['name_as_printed'] == 'Jon D. Payne'
assert by_id['david-coffin-o23-oppose-2021']['name_as_printed'] == 'David Coffin'

assert all('byfaithonline.com' in p['source'] for p in positions)
print('O23/O37 authored person-position validation passed')
