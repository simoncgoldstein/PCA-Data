#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/save-the-pca/organizational-framing-2026-09-04.json'
data = json.loads(path.read_text(encoding='utf-8'))

meta = data.get('metadata', {})
positions = data.get('positions', [])

if meta.get('organization') != 'Save the PCA':
    raise SystemExit('wrong organization')
if meta.get('ideological_weight') != 0:
    raise SystemExit('organization framing must remain zero-weight')
if len(positions) != 7:
    raise SystemExit(f'expected 7 bounded positions, found {len(positions)}')

ids = {p.get('position_id') for p in positions}
required = {
    'save-the-pca-organizational-purpose-2026',
    'save-the-pca-functional-female-officer-definition-2025',
    'save-the-pca-ffo-assistant-exclusions-2025',
    'save-the-pca-public-worship-governance-concern-2025',
    'save-the-pca-female-eldership-trajectory-2025',
    'save-the-pca-verification-awareness-method-2025',
    'save-the-pca-row-vs-classification-boundary-2025',
}
if ids != required:
    raise SystemExit(f'position ID drift: {sorted(ids)}')

for p in positions:
    if p.get('ideological_weight') != 0:
        raise SystemExit(f"nonzero ideological weight: {p.get('position_id')}")
    if not p.get('source_url', '').startswith('https://www.savethepca.com/'):
        raise SystemExit(f"non-first-party source: {p.get('position_id')}")

by_id = {p['position_id']: p for p in positions}

def text(pid: str) -> str:
    p = by_id[pid]
    return ' '.join(str(p.get(k, '')) for k in ('summary', 'boundary')).lower()

if 'analytical category' not in text('save-the-pca-functional-female-officer-definition-2025'):
    raise SystemExit('FFO definition must remain source-attributed analytical category')
if 'not an independently established' not in text('save-the-pca-female-eldership-trajectory-2025'):
    raise SystemExit('trajectory claim must retain non-adjudication boundary')
if 'row' not in text('save-the-pca-row-vs-classification-boundary-2025') or 'alone does not establish' not in text('save-the-pca-row-vs-classification-boundary-2025'):
    raise SystemExit('raw-row/classification distinction was weakened')
if 'assistants to the diaconate' not in text('save-the-pca-ffo-assistant-exclusions-2025'):
    raise SystemExit('assistant exclusion missing')

print('Save the PCA organizational-framing boundaries validated')
