#!/usr/bin/env python3
from pathlib import Path

path = Path("scripts/build-person-crosswalk.py")
text = path.read_text(encoding="utf-8")

if '"larry c hoop": {' not in text:
    marker = 'REVIEWED_NAME_VARIANTS = {\n'
    if marker not in text:
        raise SystemExit("REVIEWED_NAME_VARIANTS insertion marker missing")
    block = '''    "larry c hoop": {\n        "canonical_candidate": "larry hoop",\n        "canonical_display_name": "Larry Hoop",\n        "evidence_receipt": "sources/raw/identity/larry-larry-c-hoop-resolution-2026-09-04.json",\n        "note": "User-reviewed identity resolution: Larry C. Hoop and Larry Hoop are the same person. This person-specific decision does not create a general middle-initial matching rule.",\n    },\n'''
    text = text.replace(marker, marker + block, 1)
    path.write_text(text, encoding="utf-8")

Path("scripts/resolve-larry-hoop-identity.py").unlink(missing_ok=True)
