#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
path = root / 'sources/normalized/public-statements/gospel-reformation-network/organizational-framing-2026-09-04.json'
data = json.loads(path.read_text())

assert data['metadata']['organization'] == 'Gospel Reformation Network'
assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 4
assert all(p['ideological_weight'] == 0 for p in positions)
ids = {p['position_id'] for p in positions}
assert ids == {
    'grn-sanctification-origin-2012',
    'grn-expanded-church-health-mission',
    'grn-biblical-confessional-distinctive',
    'grn-progressive-trajectory-concerns',
}
trajectory = next(p for p in positions if p['position_id'] == 'grn-progressive-trajectory-concerns')
assert "GRN's diagnosis" in trajectory['boundary']
assert 'independently adjudicated' in trajectory['boundary']
assert all('ideological_weight' in p for p in positions)
print('GRN organizational framing validation passed')
