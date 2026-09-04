#!/usr/bin/env python3
from pathlib import Path

path = Path('scripts/build-person-crosswalk.py')
text = path.read_text(encoding='utf-8')
old = '''    row["variant_collision_key"] = first_last if first_last in variant_review_keys else None\n    row["initials_only_name"] = any(len(word) == 1 for word in words)\n'''
new = '''    row["variant_collision_key"] = None if row.get("reviewed_name_variant") else (first_last if first_last in variant_review_keys else None)\n    printed_words = row["normalized_name_as_printed"].split()\n    row["initials_only_name"] = any(len(word) == 1 for word in printed_words)\n'''
if old not in text:
    raise SystemExit('variant review block not found')
text = text.replace(old, new, 1)
old2 = '''    if r["match_status"] in {"probable_requires_review", "ambiguous", "collision"}\n    or r["variant_collision_key"]\n    or r["initials_only_name"]\n]\n'''
new2 = '''    if r["match_status"] in {"probable_requires_review", "ambiguous", "collision"}\n    or r["variant_collision_key"]\n    or (r["initials_only_name"] and not r.get("reviewed_name_variant"))\n]\n'''
if old2 not in text:
    raise SystemExit('review queue predicate block not found')
text = text.replace(old2, new2, 1)
path.write_text(text, encoding='utf-8')
