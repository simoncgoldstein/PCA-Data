#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/organizational-framing-2026-09-04.json'
data = json.loads(path.read_text(encoding='utf-8'))

meta = data.get('metadata', {})
positions = data.get('positions', [])

if meta.get('organization') != 'Jude 3 & the PCA':
    raise SystemExit('wrong organization')
if meta.get('ideological_weight') != 0:
    raise SystemExit('organizational framing must remain zero-weight')
if len(positions) != 6:
    raise SystemExit(f'expected 6 bounded positions, found {len(positions)}')

ids = {p.get('position_id') for p in positions}
required = {
    'jude3-independent-pca-member-voice-2026',
    'jude3-confessional-accountability-purpose-2026',
    'jude3-resource-aggregation-history-2026',
    'jude3-original-content-priority-2026',
    'jude3-confessional-fidelity-editorial-aim-2026',
    'jude3-westminster-standard-sponsorship-2026',
}
if ids != required:
    raise SystemExit(f'position ID drift: {sorted(ids)}')

for p in positions:
    if p.get('ideological_weight') != 0:
        raise SystemExit(f"nonzero ideological weight: {p.get('position_id')}")
    if p.get('source_url') != 'https://jude3pca.org/about-us/':
        raise SystemExit(f"non-About source in organization layer: {p.get('position_id')}")

by_id = {p['position_id']: p for p in positions}
aggregation = ' '.join(str(by_id['jude3-resource-aggregation-history-2026'].get(k, '')) for k in ('summary', 'boundary')).lower()
if 'not treated as endorsement' not in aggregation:
    raise SystemExit('aggregation/endorsement boundary missing')
if 'confessional accountability' not in by_id['jude3-confessional-accountability-purpose-2026']['summary'].lower():
    raise SystemExit('confessional-accountability purpose missing')
if 'confessional fidelity' not in by_id['jude3-confessional-fidelity-editorial-aim-2026']['summary'].lower():
    raise SystemExit('editorial aim missing')

print('Jude 3 & the PCA organizational-framing boundaries validated')
