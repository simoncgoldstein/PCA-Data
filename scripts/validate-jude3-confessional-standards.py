#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/confessional-standards-positions-2026-09-04.json'
data = json.loads(path.read_text())
assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 3
assert all(p['position_type'] == 'organizational_position' for p in positions)
assert all(p['ideological_weight'] == 0 for p in positions)
by_id = {p['position_id']: p for p in positions}
assert 'subordinate to scripture' in by_id['jude3-westminster-standards-subordinate-summary']['summary'].lower()
assert 'critical theory' in by_id['jude3-rejects-critical-method-authority-in-doctrine']['summary'].lower()
assert 'firm foundation partnership' in by_id['jude3-rejects-chronological-dismissal-westminster']['boundary'].lower()
print('Jude 3 confessional standards boundaries validated')
