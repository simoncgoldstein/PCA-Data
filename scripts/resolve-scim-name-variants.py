#!/usr/bin/env python3
from pathlib import Path
import json

receipt_path = Path('sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json')
receipt_path.parent.mkdir(parents=True, exist_ok=True)
receipt = {
  "captured_on": "2026-09-04",
  "status": "reviewed_confirmed_identity",
  "subject": "Reviewed Insider Movements name-form equivalences",
  "decisions": [
    {
      "canonical_display_name": "David B. Garner",
      "canonical_id": "david-b-garner",
      "aliases": ["David Garner"],
      "decision": "User confirmed David Garner and David B. Garner are the same person."
    },
    {
      "canonical_display_name": "Guy Prentiss Waters",
      "canonical_id": "guy-prentiss-waters",
      "aliases": ["Guy Waters"],
      "decision": "User confirmed Guy Waters and Guy Prentiss Waters are the same person."
    },
    {
      "canonical_display_name": "Nabeel T. Jabbour",
      "canonical_id": "nabeel-t-jabbour",
      "aliases": ["Nabeel Jabbour"],
      "decision": "User confirmed Nabeel Jabbour and Nabeel T. Jabbour are the same person."
    }
  ],
  "scope": "These are person-specific reviewed identity decisions only. They do not create a general rule that missing middle names, initials, or expanded middle names imply identity.",
  "ideological_weight": 0
}
receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

path = Path('scripts/build-person-crosswalk.py')
text = path.read_text(encoding='utf-8')
anchor = 'REVIEWED_NAME_VARIANTS = {\n'
if anchor not in text:
    raise SystemExit('reviewed variants anchor missing')
block = '''REVIEWED_NAME_VARIANTS = {\n    "david b garner": {\n        "canonical_candidate": "david b garner",\n        "canonical_display_name": "David B. Garner",\n        "evidence_receipt": "sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json",\n        "note": "User-reviewed identity resolution: David Garner and David B. Garner are the same person. This is a person-specific decision only.",\n    },\n    "david garner": {\n        "canonical_candidate": "david b garner",\n        "canonical_display_name": "David B. Garner",\n        "evidence_receipt": "sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json",\n        "note": "User-reviewed identity resolution: David Garner and David B. Garner are the same person. This is a person-specific decision only.",\n    },\n    "guy prentiss waters": {\n        "canonical_candidate": "guy prentiss waters",\n        "canonical_display_name": "Guy Prentiss Waters",\n        "evidence_receipt": "sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Guy Waters and Guy Prentiss Waters are the same person. This is a person-specific decision only.",\n    },\n    "guy waters": {\n        "canonical_candidate": "guy prentiss waters",\n        "canonical_display_name": "Guy Prentiss Waters",\n        "evidence_receipt": "sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Guy Waters and Guy Prentiss Waters are the same person. This is a person-specific decision only.",\n    },\n    "nabeel t jabbour": {\n        "canonical_candidate": "nabeel t jabbour",\n        "canonical_display_name": "Nabeel T. Jabbour",\n        "evidence_receipt": "sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Nabeel Jabbour and Nabeel T. Jabbour are the same person. This is a person-specific decision only.",\n    },\n    "nabeel jabbour": {\n        "canonical_candidate": "nabeel t jabbour",\n        "canonical_display_name": "Nabeel T. Jabbour",\n        "evidence_receipt": "sources/raw/identity/reviewed-scim-name-variants-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Nabeel Jabbour and Nabeel T. Jabbour are the same person. This is a person-specific decision only.",\n    },\n'''
if '"david b garner": {' not in text:
    text = text.replace(anchor, block, 1)
path.write_text(text, encoding='utf-8')
