#!/usr/bin/env python3
"""Normalize the official 2026 RUF staff-transition receipt as dated events."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit("usage: normalize-ruf-transitions.py <repo-root> <output.json>")

root, output = Path(sys.argv[1]), Path(sys.argv[2])
raw_relative = "sources/raw/institutions/ruf/annual-transitions-2026-09-04.md"
lines = (root / raw_relative).read_text(encoding="utf-8").splitlines()

NEW_HIRE_URL = "https://ruf.org/media/welcome-new-hires/"
DEPARTURE_URL = "https://ruf.org/media/saying-goodbye-departing-staff/"
