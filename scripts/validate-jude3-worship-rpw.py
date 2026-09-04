#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/worship-rpw-positions-2026-09-04.json'
data = json.loads(path.read_text())
assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 3
assert all(p['position_type'] == 'jude3_site_published_content' for p in positions)
assert all(p['attribution_status'] == 'no_named_author_exposed' for p in positions)
assert all(p['ideological_weight'] == 0 for p in positions)
by_id = {p['position_id']: p for p in positions}
assert 'second commandment' in by_id['jude3-rpw-second-commandment-regulates-worship']['summary'].lower()
assert 'positively' in by_id['jude3-rpw-positive-negative-form']['summary'].lower()
assert 'westminster confession of faith 21.1' in by_id['jude3-rpw-westminster-confessional-basis']['summary'].lower()
print('Jude 3 RPW position boundaries validated')
