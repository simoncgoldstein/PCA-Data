#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/pca-trajectory-positions-2026-09-04.json'
data = json.loads(path.read_text())

assert data['metadata']['attribution'] == 'jude3_site_published_content'
assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 3
assert all(p.get('ideological_weight') == 0 for p in positions)

by_id = {p['position_id']: p for p in positions}
assert 'unchanging Gospel' in by_id['jude3-unchanging-gospel-cultural-pressure-2026']['summary']
assert 'Jude 3 states' in by_id['jude3-pcus-pattern-replicated-in-pca-2026']['summary']
assert 'not as an independently adjudicated conclusion' in by_id['jude3-pcus-pattern-replicated-in-pca-2026']['boundary']
assert 'Gospel Reformation Network' in by_id['jude3-change-pca-trajectory-actions-2026']['summary']
assert 'MORE in the PCA' in by_id['jude3-change-pca-trajectory-actions-2026']['summary']

print('Jude 3 PCA trajectory evidence validated')
