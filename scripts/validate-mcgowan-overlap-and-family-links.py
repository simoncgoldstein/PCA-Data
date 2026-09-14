#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

mcgowan = json.loads((root / "sources/normalized/institutions/mcgowan-global-team-2026.json").read_text(encoding="utf-8"))
family = json.loads((root / "sources/normalized/identity/family-relationships-2026.json").read_text(encoding="utf-8"))
people = json.loads((root / "data/people.json").read_text(encoding="utf-8"))
organizations = json.loads((root / "data/organizations.json").read_text(encoding="utf-8"))
affiliations = json.loads((root / "data/affiliations.json").read_text(encoding="utf-8"))
sources = json.loads((root / "data/sources.json").read_text(encoding="utf-8"))

people_by_id = {row["id"]: row for row in people}
org_by_id = {row["id"]: row for row in organizations}
aff_by_id = {row["id"]: row for row in affiliations}
source_by_id = {row["id"]: row for row in sources}

# McGowan dataset and organizational boundary.
meta = mcgowan.get("metadata", {})
if meta.get("dataset_id") != "mcgowan_global_team_2026":
    raise SystemExit("McGowan dataset_id drift")
if meta.get("ideological_weight") != 0:
    raise SystemExit("McGowan institutional roster must remain ideological_weight 0")
for phrase in ("not evidence", "National Partnership status", "overlap"):
    if phrase not in meta.get("modeling_rule", "") + " " + meta.get("overlap_rule", ""):
        raise SystemExit(f"McGowan modeling boundary missing: {phrase}")

org = org_by_id.get("mcgowan-global-institute")
if not org or org.get("name") != "McGowan Global Institute" or org.get("type") != "external_nonprofit":
    raise SystemExit("McGowan app organization missing or drifted")

expected_roster = {
    "bruce-o-neil": "confirmed_in_canonical_np_membership_dataset",
    "mike-khandjian": "confirmed_in_canonical_np_membership_dataset",
    "david-cassidy": "not_found_in_current_canonical_np_membership_dataset",
    "ray-cortese": "confirmed_in_canonical_np_membership_dataset",
    "bob-flayhart": "confirmed_in_canonical_np_membership_dataset",
}
roster = mcgowan.get("tracked_roster", [])
roster_by_id = {row.get("normalized_person_id"): row for row in roster}
if set(roster_by_id) != set(expected_roster):
    raise SystemExit(f"McGowan tracked roster drift: {sorted(roster_by_id)}")

for person_id, np_status in expected_roster.items():
    row = roster_by_id[person_id]
    if row.get("mcgowan_role") != "Consultant, Coach":
        raise SystemExit(f"{person_id}: McGowan role drift")
    if row.get("np_status") != np_status:
        raise SystemExit(f"{person_id}: NP status drift")
    if not row.get("important_boundary"):
        raise SystemExit(f"{person_id}: missing overlap boundary")
    if person_id not in people_by_id:
        raise SystemExit(f"{person_id}: canonical person missing")

# MGI is a current institutional role only: five edges, all zero-weight.
expected_mgi_edges = {
    "bruce-o-neil": "aff-oneil-mcgowan-2026",
    "mike-khandjian": "aff-khandjian-mcgowan-2026",
    "david-cassidy": "aff-cassidy-mcgowan-2026",
    "ray-cortese": "aff-cortese-mcgowan-2026",
    "bob-flayhart": "aff-flayhart-mcgowan-2026",
}
for person_id, aff_id in expected_mgi_edges.items():
    aff = aff_by_id.get(aff_id)
    if not aff:
        raise SystemExit(f"{aff_id}: missing")
    if aff.get("person_id") != person_id or aff.get("target_type") != "organization" or aff.get("target_id") != "mcgowan-global-institute":
        raise SystemExit(f"{aff_id}: target/person drift")
    if aff.get("role") != "Consultant, Coach" or aff.get("confidence") != "confirmed":
        raise SystemExit(f"{aff_id}: role/confidence drift")
    if aff.get("evidence_kind") != "current_external_role":
        raise SystemExit(f"{aff_id}: evidence kind drift")
    if aff.get("weight") != 0 or aff.get("score_included") is not False:
        raise SystemExit(f"{aff_id}: McGowan role must remain unscored")
    if aff.get("source_ids") != ["src-mcgowan-global-team-2026"]:
        raise SystemExit(f"{aff_id}: source linkage drift")

# Four independently evidenced NP memberships are app-visible and score-bearing.
expected_np_edges = {
    "bruce-o-neil": "aff-oneil-np",
    "mike-khandjian": "aff-khandjian-np",
    "ray-cortese": "aff-cortese-np",
    "bob-flayhart": "aff-flayhart-np",
}
for person_id, aff_id in expected_np_edges.items():
    aff = aff_by_id.get(aff_id)
    if not aff:
        raise SystemExit(f"{aff_id}: missing")
    if aff.get("person_id") != person_id or aff.get("target_id") != "national-partnership":
        raise SystemExit(f"{aff_id}: NP target/person drift")
    if aff.get("confidence") != "confirmed":
        raise SystemExit(f"{aff_id}: NP evidence should remain confirmed")
    if aff.get("evidence_kind") != "network_membership":
        raise SystemExit(f"{aff_id}: NP evidence-kind drift")
    if aff.get("weight") != 4 or aff.get("score_included") is not True:
        raise SystemExit(f"{aff_id}: NP scoring drift")

# David Cassidy's separate AMR/MGI history must not silently become NP membership.
cassidy_np = [
    aff for aff in affiliations
    if aff.get("person_id") == "david-cassidy" and aff.get("target_id") == "national-partnership"
]
if cassidy_np:
    raise SystemExit("David Cassidy must not have an NP affiliation without new independent NP evidence")
if "not proof" not in roster_by_id["david-cassidy"]["important_boundary"].lower() and "do not label" not in roster_by_id["david-cassidy"]["important_boundary"].lower():
    raise SystemExit("Cassidy negative-finding boundary missing")

# Source registrations.
for source_id in ("src-mcgowan-global-team-2026", "src-pca-bookstore-keller-marriage"):
    if source_id not in source_by_id:
        raise SystemExit(f"source missing: {source_id}")
if source_by_id["src-mcgowan-global-team-2026"].get("url") != "https://mcgowanglobal.com/who-we-are/":
    raise SystemExit("McGowan source URL drift")

# Tim/Kathy family relation is factual context, reciprocal, and always unscored.
family_meta = family.get("metadata", {})
if family_meta.get("dataset_id") != "family_relationships_2026" or family_meta.get("ideological_weight") != 0:
    raise SystemExit("family relationship metadata drift")
for phrase in ("never evidence", "weight 0", "score_included false"):
    combined = family_meta.get("modeling_rule", "") + " " + family_meta.get("app_projection_rule", "")
    if phrase not in combined:
        raise SystemExit(f"family guardrail missing: {phrase}")

if people_by_id.get("tim-keller", {}).get("name") != "Tim Keller":
    raise SystemExit("Tim Keller canonical seed missing")
if people_by_id.get("kathy-keller", {}).get("name") != "Kathy Keller":
    raise SystemExit("Kathy Keller canonical person missing")

relationships = family.get("relationships", [])
if len(relationships) != 1 or relationships[0].get("relationship_id") != "family-tim-kathy-keller":
    raise SystemExit("Tim/Kathy normalized family relationship drift")
rel = relationships[0]
if rel.get("relationship_type") != "spouse" or rel.get("confidence") != "confirmed":
    raise SystemExit("Tim/Kathy normalized spouse relationship drift")
if "must not transfer" not in rel.get("important_boundary", ""):
    raise SystemExit("Tim/Kathy no-transfer boundary missing")

for aff_id, person_id, target_id in (
    ("aff-tim-keller-kathy-spouse", "tim-keller", "kathy-keller"),
    ("aff-kathy-keller-tim-spouse", "kathy-keller", "tim-keller"),
):
    aff = aff_by_id.get(aff_id)
    if not aff:
        raise SystemExit(f"{aff_id}: missing")
    if aff.get("person_id") != person_id or aff.get("target_type") != "person" or aff.get("target_id") != target_id:
        raise SystemExit(f"{aff_id}: reciprocal family target drift")
    if aff.get("role") != "Spouse" or aff.get("evidence_kind") != "family_relationship" or aff.get("confidence") != "confirmed":
        raise SystemExit(f"{aff_id}: family semantics drift")
    if aff.get("weight") != 0 or aff.get("score_included") is not False:
        raise SystemExit(f"{aff_id}: family relationship must remain unscored")
    if aff.get("source_ids") != ["src-pca-bookstore-keller-marriage"]:
        raise SystemExit(f"{aff_id}: family source drift")

print(json.dumps({
    "dataset": meta["dataset_id"],
    "mcgowan_roster": len(roster),
    "independently_confirmed_np_overlap": sorted(expected_np_edges),
    "cassidy_np_edge": False,
    "family_relationship": "tim-keller <-> kathy-keller",
    "family_weight": 0,
}, indent=2))
