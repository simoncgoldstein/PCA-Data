#!/usr/bin/env python3
from pathlib import Path
import json

path = Path("scripts/build-person-crosswalk.py")
text = path.read_text(encoding="utf-8")

variants = [
    (
        '"paul d richardson"',
        '''    "paul d richardson": {\n        "canonical_candidate": "paul richardson",\n        "canonical_display_name": "Paul Richardson",\n        "evidence_receipt": "sources/raw/identity/reviewed-name-variants-batch4-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Paul D. Richardson and Paul Richardson are the same person. This is a person-specific decision only.",\n    },\n'''
    ),
    (
        '"mark a rowden"',
        '''    "mark a rowden": {\n        "canonical_candidate": "mark rowden",\n        "canonical_display_name": "Mark Rowden",\n        "evidence_receipt": "sources/raw/identity/reviewed-name-variants-batch4-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Mark A. Rowden and Mark Rowden are the same person. This is a person-specific decision only.",\n    },\n'''
    ),
    (
        '"stephen thomas estock"',
        '''    "stephen thomas estock": {\n        "canonical_candidate": "stephen estock",\n        "canonical_display_name": "Stephen Estock",\n        "evidence_receipt": "sources/raw/identity/reviewed-name-variants-batch4-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Stephen Thomas Estock and Stephen Estock are the same person. This is a person-specific decision only.",\n    },\n'''
    ),
]

marker = 'REVIEWED_NAME_VARIANTS = {\n'
if marker not in text:
    raise SystemExit("REVIEWED_NAME_VARIANTS insertion marker missing")

for key, block in reversed(variants):
    if key not in text:
        text = text.replace(marker, marker + block, 1)

path.write_text(text, encoding="utf-8")

receipt_path = Path("sources/raw/identity/reviewed-name-variants-batch4-2026-09-04.json")
receipt_path.parent.mkdir(parents=True, exist_ok=True)
receipt = {
    "reviewed_on": "2026-09-04",
    "status": "user_reviewed_name_variant_links",
    "ideological_weight": 0,
    "identity_links": [
        {
            "canonical_name_form": "Paul Richardson",
            "canonical_id": "paul-richardson",
            "alias_name_form": "Paul D. Richardson",
            "reasoning_boundary": "Explicit user-reviewed equivalence for this person only."
        },
        {
            "canonical_name_form": "Mark Rowden",
            "canonical_id": "mark-rowden",
            "alias_name_form": "Mark A. Rowden",
            "reasoning_boundary": "Explicit user-reviewed equivalence for this person only."
        },
        {
            "canonical_name_form": "Stephen Estock",
            "canonical_id": "stephen-estock",
            "alias_name_form": "Stephen Thomas Estock",
            "reasoning_boundary": "Explicit user-reviewed equivalence for this person only."
        }
    ],
    "review_basis": "User explicitly instructed the repository to match all three previously surfaced name-form pairs on 2026-09-04.",
    "generalization_boundary": "These links do not create a global rule for middle initials, middle names, or omitted middle names. Future cases still require review."
}
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

Path("scripts/resolve-reviewed-name-variants-batch4.py").unlink(missing_ok=True)
