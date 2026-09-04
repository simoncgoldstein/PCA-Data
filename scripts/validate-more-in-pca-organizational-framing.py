#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
path = root / 'sources/normalized/public-statements/more-in-pca/organizational-framing-2026-09-04.json'
data = json.loads(path.read_text())

meta = data.get('metadata', {})
if meta.get('organization') != 'MORE in the PCA':
    raise SystemExit('unexpected organization')
if meta.get('ideological_weight') != 0:
    raise SystemExit('metadata ideological_weight must remain 0')
if 'distinct grassroots movement' not in meta.get('modeling_rule', ''):
    raise SystemExit('missing MORE/Jude 3 organizational boundary')

positions = data.get('positions', [])
expected = {
    'more-ruling-elder-participation-2026',
    'more-bco-8-3-general-oversight-2026',
    'more-2017-te-re-imbalance-2026',
    'more-financial-support-re-attendance-2026',
}
ids = {p.get('position_id') for p in positions}
if ids != expected:
    raise SystemExit(f'unexpected MORE position ids: {ids!r}')
for p in positions:
    if p.get('ideological_weight') != 0:
        raise SystemExit(f"nonzero ideological weight: {p.get('position_id')}")
    if not p.get('summary'):
        raise SystemExit(f"missing summary: {p.get('position_id')}")

imbalance = next(p for p in positions if p['position_id'] == 'more-2017-te-re-imbalance-2026')
if 'MORE' not in imbalance.get('boundary', '') or 'independently adjudicated' not in imbalance.get('boundary', ''):
    raise SystemExit('2017 imbalance claim must remain source-attributed')

receipt = root / meta['raw_receipt']
if not receipt.exists():
    raise SystemExit('MORE raw receipt missing')

print('MORE in the PCA organizational framing validation passed')
