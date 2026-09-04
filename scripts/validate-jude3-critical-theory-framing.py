#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/critical-theory-social-justice-positions-2026-09-04.json'
data = json.loads(path.read_text())
assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 4
assert all(p['position_type'] == 'jude3_site_published_content' for p in positions)
assert all(p['ideological_weight'] == 0 for p in positions)
by_id = {p['position_id']: p for p in positions}
assert 'marxism' in by_id['jude3-critical-theory-marxist-revolutionary-framing']['summary'].lower()
assert 'identity-based equality' in by_id['jude3-social-justice-identity-equality-framing']['summary'].lower()
assert 'organizational claim' in by_id['jude3-critical-theory-present-in-pca-claim']['boundary'].lower()
assert 'christian institutions' in by_id['jude3-critical-theory-destabilizes-institutions-claim']['summary'].lower()
print('Jude 3 Critical Theory framing boundaries validated')
