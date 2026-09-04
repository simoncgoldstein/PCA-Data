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

RULES = {
    "2026 new Campus Staff": {
        "date": "2026-07-14", "url": NEW_HIRE_URL, "event": "started_role",
        "role_class": "Campus Staff", "role": "Campus Staff", "right": "campus",
    },
    "2026 new Campus Ministers, Directors, and Assistants": {
        "date": "2026-07-14", "url": NEW_HIRE_URL, "event": "started_role",
        "role_class": "Campus Ministers, Directors, and Assistants", "role": None, "right": "campus",
    },
    "2026 new Interns": {
        "date": "2026-07-14", "url": NEW_HIRE_URL, "event": "started_role",
        "role_class": "Interns", "role": "Intern", "right": "campus",
    },
    "2026 Intern-to-Fellow transitions": {
        "date": "2026-07-14", "url": NEW_HIRE_URL, "event": "transitioned_role",
        "role_class": "Intern-to-Fellow transitions", "role": None, "right": None,
        "from_role": "Intern", "to_role": "Fellow",
    },
    "2026 new RUF National Staff": {
        "date": "2026-07-14", "url": NEW_HIRE_URL, "event": "started_role",
        "role_class": "RUF National Staff", "role": None, "right": "role",
    },
    "2026 departing Campus Ministers and Campus Staff": {
        "date": "2026-07-08", "url": DEPARTURE_URL, "event": "ended_role",
        "role_class": "Campus Ministers and Campus Staff", "role": None, "right": None,
    },
    "2026 departing Interns and Fellows": {
        "date": "2026-07-08", "url": DEPARTURE_URL, "event": "ended_role",
        "role_class": "Interns and Fellows", "role": None, "right": None,
    },
}

EXPECTED = {
    "2026 new Campus Staff": 11,
    "2026 new Campus Ministers, Directors, and Assistants": 20,
    "2026 new Interns": 94,
    "2026 Intern-to-Fellow transitions": 10,
    "2026 new RUF National Staff": 4,
    "2026 departing Campus Ministers and Campus Staff": 21,
    "2026 departing Interns and Fellows": 53,
}


def strip_markup(value: str) -> str:
    return re.sub(r"[*_`]", "", value).strip()


events = []
section = None
section_counts = Counter()
name_occurrences = Counter()

for line_number, line in enumerate(lines, 1):
    if line.startswith("## "):
        heading = line[3:].strip()
        section = heading if heading in RULES else None
        continue
    if not section:
        continue
    match = re.match(r"^- (.+)$", line)
    if not match:
        continue

    raw = strip_markup(match.group(1))
    if " — " in raw:
        name, right_value = raw.split(" — ", 1)
        name = strip_markup(name)
        right_value = strip_markup(right_value)
    else:
        name, right_value = raw, None

    rule = RULES[section]
    section_counts[section] += 1
    name_occurrences[(section, name)] += 1

    event = {
        "event_id": f"ruf-2026-transition-{len(events) + 1:03d}",
        "organization_id": "reformed-university-fellowship",
        "announcement_date": rule["date"],
        "event_type": rule["event"],
        "source_class_as_printed": section,
        "source_row_number_within_class": section_counts[section],
        "source_name_occurrence_within_class": name_occurrences[(section, name)],
        "name_as_printed": name,
        "role_class_as_printed": rule["role_class"],
        "role_as_printed": rule.get("role"),
        "from_role_as_printed": rule.get("from_role"),
        "to_role_as_printed": rule.get("to_role"),
        "campus_as_printed": None,
        "source_url": rule["url"],
        "raw_receipt": raw_relative,
        "source_line": line_number,
        "ideological_weight": 0,
    }

    if rule["right"] == "campus":
        if right_value is None:
            raise SystemExit(f"{section}:{line_number}: expected campus after em dash")
        event["campus_as_printed"] = right_value
    elif rule["right"] == "role":
        if right_value is None:
            raise SystemExit(f"{section}:{line_number}: expected role after em dash")
        event["role_as_printed"] = right_value
    elif right_value is not None:
        raise SystemExit(f"{section}:{line_number}: unexpected right-hand value")

    events.append(event)

for section_name, expected in EXPECTED.items():
    actual = section_counts[section_name]
    if actual != expected:
        raise SystemExit(f"{section_name}: expected {expected}, parsed {actual}")

counts_by_event = Counter(row["event_type"] for row in events)
expected_event_counts = {"started_role": 129, "transitioned_role": 10, "ended_role": 74}
if dict(counts_by_event) != expected_event_counts:
    raise SystemExit(f"unexpected event counts: {dict(counts_by_event)}")
if len(events) != 213:
    raise SystemExit(f"expected 213 events, parsed {len(events)}")

result = {
    "metadata": {
        "snapshot_date": "2026-09-04",
        "organization_id": "reformed-university-fellowship",
        "record_count": 213,
        "counts_by_event_type": expected_event_counts,
        "modeling_rule": "Dated starts, role transitions, and departures are preserved as events and are not treated as a current-roster claim. RUF service has zero ideological weight.",
        "source_anomalies_preserved": [
            "The two Tyler Luehrs departure rows remain separate source occurrences.",
            "Niko Fanin and Niko Fannin remain separate printed forms.",
            "Aiden Tuberville and AidenTuberville remain separate printed forms.",
            "Mike Park / Mike S. Park remains the combined form printed in the new-hire receipt.",
            "Matt Terrell and Joy Beans remain separate reconstructed rows as documented in the raw receipt.",
        ],
    },
    "source_announcements": [
        {"announcement_date": "2026-07-08", "source_url": DEPARTURE_URL, "kind": "departing staff"},
        {"announcement_date": "2026-07-14", "source_url": NEW_HIRE_URL, "kind": "new hires and role transitions"},
    ],
    "coverage": [
        {"source_class_as_printed": name, "records": EXPECTED[name]}
        for name in RULES
    ],
    "events": events,
}

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({
    "records": len(events),
    "counts_by_event_type": expected_event_counts,
    "by_source_class": dict(section_counts),
}, indent=2))
