#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
path = root / 'sources/normalized/public-statements/jude3-pca/women-office-positions-2026-09-04.json'
data = json.loads(path.read_text())

assert data['metadata']['ideological_weight'] == 0
positions = data['positions']
assert len(positions) == 6
assert all(p['ideological_weight'] == 0 for p in positions)

by_id = {p['position_id']: p for p in positions}
assert len(by_id) == len(positions)

site_ids = {
    'jude3-site-male-only-pca-diaconate-bco',
    'jude3-site-disagreement-submit-amend-or-leave',
    'jude3-site-nonoffice-womens-ministry-titles-legitimate',
    'jude3-site-scripture-over-cultural-office-expectations',
}
for position_id in site_ids:
    p = by_id[position_id]
    assert p['position_type'] == 'jude3_site_published_content'
    assert p['attribution_status'] == 'no_named_author_exposed'
    assert 'author_as_printed' not in p

for position_id in {
    'ryan-biese-2026-ga-preview-women-officer-titles',
    'ryan-biese-2026-ga-preview-women-deacons-prediction',
}:
    p = by_id[position_id]
    assert p['position_type'] == 'author_publication'
    assert p['author_as_printed'] == 'Ryan Biese'
    assert p['published'] == '2026-06-18'

assert 'submit' in by_id['jude3-site-disagreement-submit-amend-or-leave']['summary'].lower()
assert 'women\'s ministry coordinator' in by_id['jude3-site-nonoffice-womens-ministry-titles-legitimate']['summary'].lower()
assert 'forecast' in by_id['ryan-biese-2026-ga-preview-women-deacons-prediction']['boundary'].lower()

print('Jude 3 women/office position boundaries validated')
