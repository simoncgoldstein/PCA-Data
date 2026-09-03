#!/usr/bin/env python3
"""Build a complete AMR website blog index from preserved pagination HTML."""

from __future__ import annotations

import hashlib
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

if len(sys.argv) != 4:
    raise SystemExit("usage: parse-amr-blog-index.py <raw-page-dir> <output.json> <manifest.json>")
raw_dir, output, manifest_path = map(Path, sys.argv[1:])


def text(value: str) -> str:
    return html.unescape(re.sub(r"<.*?>", "", value, flags=re.S)).strip()


def topics(title: str) -> list[str]:
    rules = [
        (r"overture|general assembly|\bPCA\b|presbyter", "PCA"),
        (r"women|female|deacon", "women in ministry"),
        (r"revoice|sexual|celib", "sexuality / Revoice"),
        (r"race|racial|ethnic|immigra|refugee", "race / immigration"),
        (r"confession|reformed|subscription", "confessional identity"),
        (r"mission|evangeli|church plant", "mission"),
        (r"worship|Lord.s Supper|sacrament", "worship"),
        (r"RUF|university", "RUF / campus ministry"),
        (r"theological vision", "AMR theological vision"),
        (r"justice|mercy|poor", "mercy / public theology"),
    ]
    found = [tag for pattern, tag in rules if re.search(pattern, title, re.I)]
    return found or ["uncategorized"]


items_by_url = {}
page_receipts = []
page_paths = [raw_dir / "home.html"] + sorted(raw_dir.glob("page-*.html"), key=lambda p: int(p.stem.split("-")[-1]))
for page_path in page_paths:
    raw_bytes = page_path.read_bytes()
    body = raw_bytes.decode("utf-8", errors="replace")
    page_number = "home" if page_path.name == "home.html" else int(page_path.stem.split("-")[-1])
    page_url = "https://a4mr.org/" if page_number == "home" else ("https://a4mr.org/blog/" if page_number == 1 else f"https://a4mr.org/blog/page/{page_number}/")
    page_receipts.append({"page": page_number, "url": page_url, "local_file": str(page_path), "size_bytes": len(raw_bytes), "sha256": hashlib.sha256(raw_bytes).hexdigest()})
    for block in re.findall(r"<article\b.*?</article>", body, flags=re.S):
        heading = re.search(r'<h5 class="entry-title"><a href="([^"]+)"[^>]*>(.*?)</a>', block, flags=re.S)
        published = re.search(r'<span class="published">(.*?)</span>', block, flags=re.S)
        author = re.search(r'dp-dfg-cf-author.*?dp-dfg-custom-field-value">(.*?)</span>', block, flags=re.S)
        if not heading or not published:
            continue
        url, title = html.unescape(heading.group(1)), text(heading.group(2))
        date_as_printed = text(published.group(1))
        contributor = text(author.group(1)) if author else None
        date = datetime.strptime(date_as_printed, "%B %d, %Y").date().isoformat()
        category_match = re.search(r'<article[^>]+class="([^"]+)"', block)
        categories = sorted(set(re.findall(r"category-([a-z0-9-]+)", category_match.group(1) if category_match else "")))
        items_by_url[url] = {
            "date": date,
            "date_as_printed": date_as_printed,
            "title": title,
            "contributor_as_printed": contributor,
            "role_as_stated": None,
            "guests_as_stated": None,
            "site_categories": categories,
            "topic_tags": topics(title),
            "url": url,
            "item_format": "article_or_embedded_media_not_yet_opened",
            "transcript_or_caption_availability": "not_assessed",
            "archive_page": page_number,
        }

items = sorted(items_by_url.values(), key=lambda row: (row["date"], row["title"]), reverse=True)
result = {
    "metadata": {
        "organization": "Alliance for Mission & Renewal",
        "snapshot_date": "2026-09-03",
        "archive": "https://a4mr.org/blog/",
        "item_count": len(items),
        "coverage": "complete website home-feature and blog pagination pages 1-12 at capture time; Substack and YouTube require separate enumeration",
        "field_note": "Contributor strings and categories are preserved from archive cards. Role, guest, format, and transcript fields remain null/not_assessed until each item is opened; no organizational unanimity is inferred from contributor appearance.",
    },
    "items": items,
}
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
manifest_path.write_text(json.dumps({"captured_on": "2026-09-03", "method": "curl -L", "pages": page_receipts}, indent=2) + "\n", encoding="utf-8")
print(f"AMR blog index: {len(items)} unique items across {len(page_receipts)} preserved pages")
