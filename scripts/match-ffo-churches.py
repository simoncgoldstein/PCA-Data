#!/usr/bin/env python3
"""Match Save the PCA's 2026-02-08 church assessments to PCA church entities.

The matcher is intentionally conservative. It auto-matches only when evidence is
strong and unambiguous, and otherwise emits candidates for review. It never
creates person-level claims from a church-level assessment.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

if len(sys.argv) < 4:
    raise SystemExit("usage: match-ffo-churches.py <churches.json> <flagged-churches.json> <output-dir>")

churches_path = Path(sys.argv[1])
ffo_path = Path(sys.argv[2])
outdir = Path(sys.argv[3])
outdir.mkdir(parents=True, exist_ok=True)

churches = json.loads(churches_path.read_text(encoding="utf-8"))
ffo = json.loads(ffo_path.read_text(encoding="utf-8"))


def norm_text(value):
    value = (value or "").lower().replace("&", " and ")
    value = re.sub(r"\bpresbyterian church in america\b", " ", value)
    value = re.sub(r"\bpca\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def norm_name(value):
    return norm_text(value)


def simplified_name(value):
    text = norm_name(value)
    stop = {"presbyterian", "church", "community", "pca"}
    return " ".join(token for token in text.split() if token not in stop)


def norm_phone(value):
    digits = re.sub(r"\D", "", value or "")
    return digits[-10:] if len(digits) >= 10 else digits


def norm_url(value):
    value = (value or "").strip()
    if not value:
        return None
    if not re.match(r"^https?://", value, re.I):
        value = "https://" + value
    try:
        parsed = urlparse(value)
    except ValueError:
        return None
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/+$", "", parsed.path or "")
    return host + path.lower()


def norm_host(value):
    normalized = norm_url(value)
    return normalized.split("/", 1)[0] if normalized else None


def norm_presbytery(value):
    text = norm_text(value)
    text = re.sub(r"\bpresbytery\b", "", text)
    aliases = {
        "metro new york": "metropolitan new york",
        "southern louisiana": "southern louisiana",
        "se louisiana": "southern louisiana",
        "se alabama": "southeast alabama",
        "sw florida": "southwest florida",
        "rocky mtn": "rocky mountain",
        "philadelphia metro west": "philadelphia metro west",
    }
    text = re.sub(r"\s+", " ", text).strip()
    return aliases.get(text, text)


index = {
    "url": defaultdict(list),
    "host": defaultdict(list),
    "phone": defaultdict(list),
    "name_presbytery": defaultdict(list),
    "simple_presbytery": defaultdict(list),
}

for church in churches:
    cid = church["id"]
    if norm_url(church.get("website")):
        index["url"][norm_url(church.get("website"))].append(cid)
        index["host"][norm_host(church.get("website"))].append(cid)
    if norm_phone(church.get("phone")):
        index["phone"][norm_phone(church.get("phone"))].append(cid)
    p = norm_presbytery(church.get("presbytery_as_printed"))
    index["name_presbytery"][(norm_name(church.get("name")), p)].append(cid)
    index["simple_presbytery"][(simplified_name(church.get("name")), p)].append(cid)

church_by_id = {church["id"]: church for church in churches}
results = []

for row in ffo:
    candidates = defaultdict(lambda: {"score": 0, "signals": []})
    source_url = norm_url(row.get("website"))
    source_host = norm_host(row.get("website"))
    source_phone = norm_phone(row.get("phone"))
    source_pres = norm_presbytery(row.get("presbytery"))
    source_name = norm_name(row.get("church"))
    source_simple = simplified_name(row.get("church"))

    def add(ids, score, signal):
        for cid in ids:
            candidates[cid]["score"] += score
            candidates[cid]["signals"].append(signal)

    if source_url:
        add(index["url"].get(source_url, []), 120, "exact_url")
    if source_host:
        add(index["host"].get(source_host, []), 75, "same_website_host")
    if source_phone:
        add(index["phone"].get(source_phone, []), 100, "exact_phone")
    add(index["name_presbytery"].get((source_name, source_pres), []), 90, "exact_name_and_presbytery")
    if source_simple:
        add(index["simple_presbytery"].get((source_simple, source_pres), []), 60, "simplified_name_and_presbytery")

    ranked = sorted(
        (
            {
                "church_id": cid,
                "score": info["score"],
                "signals": sorted(set(info["signals"])),
                "church_name": church_by_id[cid].get("name"),
                "presbytery_as_printed": church_by_id[cid].get("presbytery_as_printed"),
                "duplicate_review_required": church_by_id[cid].get("duplicate_review_required", False),
            }
            for cid, info in candidates.items()
        ),
        key=lambda item: (-item["score"], item["church_name"] or ""),
    )

    status = "unmatched"
    matched_id = None
    confidence = None
    reason = None
    if ranked:
        top = ranked[0]
        tied = len(ranked) > 1 and ranked[1]["score"] == top["score"]
        strong_signal = any(signal in top["signals"] for signal in ["exact_url", "exact_phone", "exact_name_and_presbytery"])
        if top["score"] >= 90 and strong_signal and not tied:
            status = "auto_matched"
            matched_id = top["church_id"]
            confidence = "high"
            reason = "+".join(top["signals"])
        elif top["score"] >= 60:
            status = "review_required"
            confidence = "candidate"
            reason = "ambiguous_or_weaker_match"

    results.append(
        {
            "ffo_source_row": row.get("source_row"),
            "ffo_church_as_printed": row.get("church"),
            "ffo_presbytery_as_printed": row.get("presbytery"),
            "ffo_website": row.get("website"),
            "ffo_phone": row.get("phone"),
            "functional_female_elders": row.get("functional_female_elders"),
            "functional_female_deacons": row.get("functional_female_deacons"),
            "review_date": row.get("review_date"),
            "match_status": status,
            "matched_church_id": matched_id,
            "match_confidence": confidence,
            "match_reason": reason,
            "candidates": ranked[:5],
        }
    )

counts = defaultdict(int)
for result in results:
    counts[result["match_status"]] += 1

assessments = []
for result in results:
    if result["match_status"] != "auto_matched":
        continue
    assessments.append(
        {
            "church_id": result["matched_church_id"],
            "source_dataset": "save-the-pca-ffo-2026-02-08",
            "source_row": result["ffo_source_row"],
            "assessment_date": "2026-02-08",
            "review_date": result["review_date"],
            "functional_female_elders": result["functional_female_elders"],
            "functional_female_deacons": result["functional_female_deacons"],
            "attribution": "Save the PCA Functional Female Officer dataset",
            "match_confidence": result["match_confidence"],
            "match_reason": result["match_reason"],
        }
    )

metadata = {
    "source_dataset": "Save the PCA Functional Female Officer dataset, 2026-02-08",
    "pca_church_snapshot": "2026-08-31 directory / 2026-09-03 KML capture",
    "total_flagged_records": len(results),
    "match_counts": dict(counts),
    "auto_matched_assessments": len(assessments),
    "rules": {
        "person_level_inference": False,
        "unmatched_records_preserved": True,
        "ambiguous_matches_not_forced": True,
        "church_duplicate_flags_respected": True,
    },
}

(outdir / "match-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
(outdir / "ffo-church-crosswalk.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
(outdir / "church-assessments-high-confidence.json").write_text(json.dumps(assessments, indent=2) + "\n", encoding="utf-8")
print(json.dumps(metadata, indent=2))
