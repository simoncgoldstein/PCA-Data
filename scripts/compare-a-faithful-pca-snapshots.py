#!/usr/bin/env python3
"""Compare the independently preserved 571- and 737-signer snapshots."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("usage: compare-a-faithful-pca-snapshots.py <571.json> <737.json> <output.json>")

old_path, new_path, output_path = map(Path, sys.argv[1:])
old = json.loads(old_path.read_text(encoding="utf-8"))["signers"]
new = json.loads(new_path.read_text(encoding="utf-8"))["signers"]


def key(value: str) -> str:
    value = value.replace("’", "'")
    value = re.sub(r"^(?:(?:rev|dr)\.?\s+)+", "", value, flags=re.I)
    value = re.sub(r"\b(?:jr|sr|ii|iii|iv)\.?\b", "", value, flags=re.I)
    value = re.sub(r"[^a-z0-9 ]+", " ", value.lower())
    tokens = [t for t in value.split() if len(t) > 1]
    return f"{tokens[0]} {tokens[-1]}" if len(tokens) >= 2 else " ".join(tokens)


old_by = defaultdict(list)
new_by = defaultdict(list)
for row in old:
    old_by[key(row["name_as_printed"])].append(row)
for row in new:
    new_by[key(row["name_as_printed"])].append(row)

shared = sorted(set(old_by) & set(new_by))
added = sorted(set(new_by) - set(old_by))
removed = sorted(set(old_by) - set(new_by))
collisions = sorted(k for k in set(old_by) | set(new_by) if len(old_by[k]) > 1 or len(new_by[k]) > 1)

result = {
    "metadata": {
        "snapshot_a": "2021-06-11",
        "snapshot_b": "2022-03-14",
        "snapshot_a_rows": len(old),
        "snapshot_b_rows": len(new),
        "shared_identity_keys": len(shared),
        "added_identity_keys": len(added),
        "removed_identity_keys": len(removed),
        "collision_keys_requiring_review": len(collisions),
        "comparison_rule": "Honorifics, punctuation, suffixes, and middle initials are ignored; first and last name form the comparison key. Collisions remain review items.",
    },
    "in_both": [
        {"identity_key": k, "snapshot_a": old_by[k], "snapshot_b": new_by[k]} for k in shared
    ],
    "added_in_2022_snapshot": [row for k in added for row in new_by[k]],
    "not_matched_in_2022_snapshot": [row for k in removed for row in old_by[k]],
    "possible_name_collisions": [
        {"identity_key": k, "snapshot_a": old_by[k], "snapshot_b": new_by[k]} for k in collisions
    ],
}
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(result["metadata"], indent=2))
