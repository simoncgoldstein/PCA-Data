#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/sexuality-positions-2026-09-04.json'
data = json.loads(path.read_text())

assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 5
assert all(p['ideological_weight'] == 0 for p in positions)
assert all(p['position_type'] == 'jude3_site_published_content' for p in positions)
assert all(p['attribution_status'] == 'no_named_author_exposed' for p in positions)
assert all('author_as_printed' not in p for p in positions)

by_id = {p['position_id']: p for p in positions}
assert len(by_id) == 5
assert 'acts' in by_id['jude3-site-homosexual-acts-sinful']['summary'].lower()
assert 'attraction' in by_id['jude3-site-homosexual-attraction-sinful']['summary'].lower()
assert 'mortified' in by_id['jude3-site-homosexual-attraction-mortification']['summary'].lower()
assert 'self-identity' in by_id['jude3-site-homosexual-self-identification-rejected']['summary'].lower()
assert 'biological sex' in by_id['jude3-site-sex-gender-created-order']['summary'].lower()

print('Jude 3 sexuality position boundaries validated')
