#!/usr/bin/env python3
"""Archive and normalize AMR's public Substack and YouTube inventories.

The importer is intentionally local/manual: it does not run in GitHub Actions and
does not commit its own output. Raw API/page responses and caption tracks are
preserved so every normalized record remains auditable.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
import time
import unicodedata
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


if len(sys.argv) not in (1, 2, 3):
    raise SystemExit("usage: import-amr-platforms.py [repo-root] [snapshot-date]")

ROOT = Path(sys.argv[1] if len(sys.argv) >= 2 else ".").resolve()
SNAPSHOT = sys.argv[2] if len(sys.argv) == 3 else "2026-09-03"
RAW_ROOT = ROOT / "sources/raw/media/amr"
SUBSTACK_RAW = RAW_ROOT / f"substack-{SNAPSHOT}"
YOUTUBE_RAW = RAW_ROOT / f"youtube-{SNAPSHOT}"
NORMALIZED = ROOT / "sources/normalized/amr"
SUBSTACK_ARCHIVE = "https://a4mr.substack.com/api/v1/archive?sort=new&search=&offset={offset}&limit=12"
SUBSTACK_FEED = "https://a4mr.substack.com/feed"
YOUTUBE_VIDEOS = "https://www.youtube.com/@AllianceforMissionandRenewal/videos"


def fetch(url: str, *, payload: dict[str, Any] | None = None) -> bytes:
    command = [
        "curl", "-L", "--fail", "--silent", "--show-error",
        "--retry", "2", "--max-time", "90",
        "-A", "Mozilla/5.0 (compatible; PCA-Data public-source archiver)",
    ]
    if payload is not None:
        command += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(payload)]
    command.append(url)
    result = subprocess.run(command, check=True, capture_output=True)
    return result.stdout


def write_bytes(path: Path, value: bytes) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)
    return {
        "local_file": str(path.relative_to(ROOT)),
        "size_bytes": len(value),
        "sha256": hashlib.sha256(value).hexdigest(),
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def values(value: Any, key: str):
    if isinstance(value, dict):
        if key in value:
            yield value[key]
        for child in value.values():
            yield from values(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from values(child, key)


def json_after(pattern: str, text: str) -> Any:
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f"marker not found: {pattern}")
    return json.JSONDecoder().raw_decode(text[match.end():])[0]


def title_key(value: str) -> str:
    value = unicodedata.normalize("NFKD", html.unescape(value))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def topic_tags(title: str) -> list[str]:
    rules = [
        (r"overture|general assembly|\bPCA\b|presbyter|BCO", "PCA"),
        (r"women|female|deacon|daughter", "women in ministry"),
        (r"revoice|sexual|celib|homosexual|side b", "sexuality / Revoice"),
        (r"race|racial|ethnic|immigra|refugee", "race / immigration"),
        (r"confession|reformed|subscription|theological vision", "confessional identity"),
        (r"mission|evangeli|church plant", "mission"),
        (r"worship|lord.s supper|sacrament", "worship"),
        (r"RUF|university|campus", "RUF / campus ministry"),
        (r"justice|mercy|poor|public theology", "mercy / public theology"),
    ]
    found = [tag for pattern, tag in rules if re.search(pattern, title, re.I)]
    return found or ["uncategorized"]


def archive_substack() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    receipts: list[dict[str, Any]] = []
    posts: list[dict[str, Any]] = []
    for offset in range(0, 10000, 12):
        url = SUBSTACK_ARCHIVE.format(offset=offset)
        raw = fetch(url)
        page = json.loads(raw)
        if not page:
            break
        receipt = write_bytes(SUBSTACK_RAW / f"archive-offset-{offset:03d}.json", raw)
        receipt.update({"url": url, "offset": offset, "record_count": len(page)})
        receipts.append(receipt)
        posts.extend(page)
        if len(page) < 12:
            break

    feed = fetch(SUBSTACK_FEED)
    feed_receipt = write_bytes(SUBSTACK_RAW / "feed.xml", feed)
    feed_receipt.update({"url": SUBSTACK_FEED, "format": "rss"})
    receipts.append(feed_receipt)

    feed_items = []
    root = ElementTree.fromstring(feed)
    content_key = "{http://purl.org/rss/1.0/modules/content/}encoded"
    for item in root.findall("./channel/item"):
        enclosure = item.find("enclosure")
        body = item.findtext(content_key) or ""
        feed_items.append({
            "title": (item.findtext("title") or "").strip(),
            "description": (item.findtext("description") or "").strip(),
            "canonical_url": item.findtext("link"),
            "published_at": parsedate_to_datetime(item.findtext("pubDate")).isoformat(),
            "enclosure_url": enclosure.get("url") if enclosure is not None else None,
            "enclosure_type": enclosure.get("type") if enclosure is not None else None,
            "embedded_youtube_video_ids": sorted(set(re.findall(r"youtube2-([A-Za-z0-9_-]{11})", body))),
        })

    unique = {int(post["id"]): post for post in posts}
    return [unique[key] for key in sorted(unique)], feed_items, receipts


def extract_lockup(lockup: dict[str, Any]) -> dict[str, Any] | None:
    if lockup.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO":
        return None
    video_id = lockup.get("contentId")
    if not video_id:
        return None
    metadata = lockup.get("metadata", {}).get("lockupMetadataViewModel", {})
    title = metadata.get("title", {}).get("content")
    rows = metadata.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
    parts = [
        part.get("text", {}).get("content")
        for row in rows for part in row.get("metadataParts", [])
        if part.get("text", {}).get("content")
    ]
    duration = None
    for badge in values(lockup.get("contentImage", {}), "thumbnailBadgeViewModel"):
        if re.fullmatch(r"(?:\d+:)?\d{1,2}:\d{2}", badge.get("text", "")):
            duration = badge["text"]
            break
    thumbnails = list(values(lockup.get("contentImage", {}), "sources"))
    flat_thumbnails = [row for group in thumbnails if isinstance(group, list) for row in group]
    return {
        "video_id": video_id,
        "title_from_channel_page": title,
        "channel_page_metadata": parts,
        "duration_as_printed": duration,
        "thumbnail_url": flat_thumbnails[-1].get("url") if flat_thumbnails else None,
    }


def youtube_grid(initial: dict[str, Any]) -> dict[str, Any]:
    grids = list(values(initial, "richGridRenderer"))
    if not grids:
        raise ValueError("YouTube videos grid not found")
    return grids[0]


def archive_youtube() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    receipts: list[dict[str, Any]] = []
    raw_html = fetch(YOUTUBE_VIDEOS)
    receipts.append({**write_bytes(YOUTUBE_RAW / "channel-videos.html", raw_html), "url": YOUTUBE_VIDEOS})
    page = raw_html.decode("utf-8", errors="replace")
    initial = json_after(r"var ytInitialData = ", page)
    config: dict[str, Any] = {}
    for match in re.finditer(r"ytcfg\.set\(", page):
        try:
            candidate = json.JSONDecoder().raw_decode(page[match.end():])[0]
        except (ValueError, json.JSONDecodeError):
            continue
        if isinstance(candidate, dict):
            config.update(candidate)
    api_key = config.get("INNERTUBE_API_KEY")
    web_context = config.get("INNERTUBE_CONTEXT")
    if not api_key or not web_context:
        raise ValueError("YouTube public API context not found in channel page")

    videos: dict[str, dict[str, Any]] = {}
    grid = youtube_grid(initial)
    for lockup in values(grid, "lockupViewModel"):
        parsed = extract_lockup(lockup)
        if parsed:
            videos[parsed["video_id"]] = parsed

    continuation_items = [row["continuationItemRenderer"] for row in grid.get("contents", []) if "continuationItemRenderer" in row]
    for index, item in enumerate(continuation_items, 1):
        token = item.get("continuationEndpoint", {}).get("continuationCommand", {}).get("token")
        if not token:
            continue
        url = f"https://www.youtube.com/youtubei/v1/browse?key={api_key}"
        raw = fetch(url, payload={"context": web_context, "continuation": token})
        receipts.append({
            **write_bytes(YOUTUBE_RAW / f"continuation-{index:02d}.json", raw),
            "url": "https://www.youtube.com/youtubei/v1/browse",
            "response_kind": "channel_videos_continuation",
        })
        response = json.loads(raw)
        for lockup in values(response, "lockupViewModel"):
            parsed = extract_lockup(lockup)
            if parsed:
                videos[parsed["video_id"]] = parsed

    player_dir = YOUTUBE_RAW / "player-metadata"
    caption_dir = YOUTUBE_RAW / "captions"
    android_context = {
        "client": {"clientName": "ANDROID", "clientVersion": "20.10.38", "hl": "en", "gl": "US"}
    }
    for sequence, video_id in enumerate(sorted(videos), 1):
        player_url = f"https://www.youtube.com/youtubei/v1/player?key={api_key}"
        web_raw = fetch(player_url, payload={"context": web_context, "videoId": video_id})
        android_raw = fetch(player_url, payload={"context": android_context, "videoId": video_id})
        web_receipt = write_bytes(player_dir / f"{video_id}-web.json", web_raw)
        android_receipt = write_bytes(player_dir / f"{video_id}-android.json", android_raw)
        receipts += [
            {**web_receipt, "url": "https://www.youtube.com/youtubei/v1/player", "video_id": video_id, "client": "web"},
            {**android_receipt, "url": "https://www.youtube.com/youtubei/v1/player", "video_id": video_id, "client": "android"},
        ]
        web = json.loads(web_raw)
        android = json.loads(android_raw)
        details = web.get("videoDetails") or android.get("videoDetails") or {}
        micro = web.get("microformat", {}).get("playerMicroformatRenderer", {})
        tracks = android.get("captions", {}).get("playerCaptionsTracklistRenderer", {}).get("captionTracks", [])
        caption_receipts = []
        for track_index, track in enumerate(tracks, 1):
            if track.get("languageCode") != "en":
                continue
            caption_url = track.get("baseUrl", "").replace("fmt=srv3", "fmt=vtt")
            if not caption_url:
                continue
            caption_raw = fetch(caption_url)
            kind = "auto" if track.get("kind") == "asr" else "official"
            caption_path = caption_dir / f"{video_id}-en-{kind}-{track_index}.vtt"
            receipt = write_bytes(caption_path, caption_raw)
            receipt.update({
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "video_id": video_id,
                "language": "en",
                "caption_kind": kind,
                "track_name": "".join(run.get("text", "") for run in track.get("name", {}).get("runs", [])),
            })
            receipts.append(receipt)
            caption_receipts.append(receipt)

        videos[video_id].update({
            "title": details.get("title") or videos[video_id].get("title_from_channel_page"),
            "description": details.get("shortDescription"),
            "published_at": micro.get("publishDate"),
            "upload_date": micro.get("uploadDate"),
            "duration_seconds": int(details["lengthSeconds"]) if details.get("lengthSeconds") else None,
            "view_count_at_capture": int(details["viewCount"]) if details.get("viewCount") else None,
            "keywords_as_printed": details.get("keywords", []),
            "category": micro.get("category"),
            "playability_status": android.get("playabilityStatus", {}).get("status") or web.get("playabilityStatus", {}).get("status"),
            "caption_receipts": [row["local_file"] for row in caption_receipts],
            "caption_status": "available_archived" if caption_receipts else "not_exposed_by_public_player_metadata",
            "transcript_status": "caption_track_archived" if caption_receipts else "not_available",
        })
        if sequence < len(videos):
            time.sleep(0.05)

    return [videos[key] for key in sorted(videos)], receipts


def main() -> None:
    website = json.loads((NORMALIZED / "blog-index-2023-2026.json").read_text(encoding="utf-8"))["items"]
    site_by_title = {title_key(row["title"]): row for row in website}
    substack_posts, feed_items, substack_receipts = archive_substack()
    youtube_videos, youtube_receipts = archive_youtube()
    feed_by_url = {row["canonical_url"]: row for row in feed_items}
    youtube_to_feed: dict[str, list[dict[str, Any]]] = {}
    for row in feed_items:
        for video_id in row["embedded_youtube_video_ids"]:
            youtube_to_feed.setdefault(video_id, []).append(row)

    substack_items = []
    for post in sorted(substack_posts, key=lambda row: (row.get("post_date", ""), row.get("id", 0)), reverse=True):
        site = site_by_title.get(title_key(post.get("title", "")))
        feed = feed_by_url.get(post.get("canonical_url"))
        embedded_youtube = feed.get("embedded_youtube_video_ids", []) if feed else []
        if post.get("video_upload_id") or embedded_youtube:
            media_type = "video"
        elif post.get("podcast_url") or (feed and feed.get("enclosure_type") == "audio/mpeg"):
            media_type = "audio_or_podcast"
        else:
            media_type = "article"
        substack_items.append({
            "stable_item_id": f"substack-{post['id']}",
            "substack_post_id": post["id"],
            "title": post.get("title"),
            "subtitle": post.get("subtitle") or post.get("description"),
            "published_at": post.get("post_date"),
            "url": post.get("canonical_url"),
            "author_or_contributor_as_printed": site.get("contributor_as_printed") if site else None,
            "hosts_as_stated": None,
            "guests_as_stated": None,
            "roles_as_stated": None,
            "media_type": media_type,
            "substack_type": post.get("type"),
            "categories": [row.get("name") or row.get("slug") for row in post.get("postTags", [])],
            "topic_tags": topic_tags(post.get("title", "")),
            "audio_url": post.get("podcast_url"),
            "audio_duration_seconds": post.get("podcast_duration"),
            "embedded_youtube_video_ids": embedded_youtube,
            "website_crosspost_url": site.get("url") if site else None,
            "caption_status": "not_applicable" if media_type == "article" else "not_exposed_by_archive_record",
            "transcript_status": "article_body_in_raw_rss" if feed and media_type == "article" else ("excerpt_in_raw_archive" if media_type == "article" else "not_assessed"),
            "source_visibility": "archive_api_and_rss" if feed else "archive_api",
        })

    archive_urls = {row["url"] for row in substack_items}
    for feed in feed_items:
        if feed["canonical_url"] in archive_urls:
            continue
        podcast_match = re.search(r"/podcast/(\d+)/", feed.get("enclosure_url") or "")
        stable_suffix = podcast_match.group(1) if podcast_match else hashlib.sha256(feed["canonical_url"].encode()).hexdigest()[:12]
        site = site_by_title.get(title_key(feed["title"]))
        substack_items.append({
            "stable_item_id": f"substack-feed-{stable_suffix}",
            "substack_post_id": int(stable_suffix) if stable_suffix.isdigit() else None,
            "title": feed["title"],
            "subtitle": feed["description"],
            "published_at": feed["published_at"],
            "url": feed["canonical_url"],
            "author_or_contributor_as_printed": site.get("contributor_as_printed") if site else None,
            "hosts_as_stated": None,
            "guests_as_stated": None,
            "roles_as_stated": None,
            "media_type": "audio_or_podcast" if feed.get("enclosure_type") == "audio/mpeg" else "rss_item",
            "substack_type": "podcast_companion",
            "categories": [],
            "topic_tags": topic_tags(feed["title"]),
            "audio_url": feed.get("enclosure_url"),
            "audio_duration_seconds": None,
            "embedded_youtube_video_ids": feed["embedded_youtube_video_ids"],
            "website_crosspost_url": site.get("url") if site else None,
            "caption_status": "not_exposed_by_rss",
            "transcript_status": "not_exposed_by_rss",
            "source_visibility": "rss_feed_only_podcast_companion",
        })
    substack_items.sort(key=lambda row: (row.get("published_at") or "", row["stable_item_id"]), reverse=True)

    youtube_items = []
    for video in sorted(youtube_videos, key=lambda row: (row.get("published_at") or "", row["video_id"]), reverse=True):
        site = site_by_title.get(title_key(video.get("title", "")))
        feed_matches = youtube_to_feed.get(video["video_id"], [])
        youtube_items.append({
            "stable_item_id": f"youtube-{video['video_id']}",
            "video_id": video["video_id"],
            "title": video.get("title"),
            "published_at": video.get("published_at"),
            "upload_date": video.get("upload_date"),
            "url": f"https://www.youtube.com/watch?v={video['video_id']}",
            "channel_id": "UCTmuCc8VJTYR1_0nDM7yQMA",
            "channel": "Alliance for Mission and Renewal",
            "author_or_contributor_as_printed": site.get("contributor_as_printed") if site else None,
            "hosts_as_stated": None,
            "guests_as_stated": None,
            "roles_as_stated": None,
            "description": video.get("description"),
            "media_type": "video",
            "duration_seconds": video.get("duration_seconds"),
            "category": video.get("category"),
            "topic_tags": topic_tags(video.get("title", "")),
            "website_crosspost_url": site.get("url") if site else None,
            "substack_crosspost_urls": sorted({row["canonical_url"] for row in feed_matches}),
            "substack_description_as_printed": feed_matches[0]["description"] if feed_matches else None,
            "caption_status": video.get("caption_status"),
            "transcript_status": video.get("transcript_status"),
            "caption_receipts": video.get("caption_receipts", []),
            "playability_status_at_capture": video.get("playability_status"),
        })

    all_platform_rows = [
        *(dict(platform="website", stable_item_id=f"website-{index + 1}", **row) for index, row in enumerate(website)),
        *(dict(platform="substack", **row) for row in substack_items),
        *(dict(platform="youtube", **row) for row in youtube_items),
    ]
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in all_platform_rows:
        groups.setdefault(title_key(row["title"]), []).append(row)
    crossposts = []
    for key, rows in sorted(groups.items()):
        platforms = sorted({row["platform"] for row in rows})
        if len(platforms) < 2:
            continue
        crossposts.append({
            "title_key": key,
            "title": rows[0]["title"],
            "platforms": platforms,
            "items": [{"platform": row["platform"], "stable_item_id": row["stable_item_id"], "url": row["url"]} for row in rows],
            "match_method": "exact_normalized_title",
        })

    write_json(NORMALIZED / "substack-index-2023-2026.json", {
        "metadata": {
            "organization": "Alliance for Mission & Renewal",
            "snapshot_date": SNAPSHOT,
            "archive": "https://a4mr.substack.com/",
            "item_count": len(substack_items),
            "coverage": "Complete public Substack archive API pagination at capture time.",
            "field_note": "Contributor data is copied only from an exact-title AMR website crosspost; host, guest, and role fields remain null unless explicitly classified.",
        },
        "items": substack_items,
    })
    write_json(NORMALIZED / "youtube-index-2023-2026.json", {
        "metadata": {
            "organization": "Alliance for Mission & Renewal",
            "snapshot_date": SNAPSHOT,
            "channel": YOUTUBE_VIDEOS,
            "channel_id": "UCTmuCc8VJTYR1_0nDM7yQMA",
            "item_count": len(youtube_items),
            "coverage": "Complete public Videos-tab grid at capture time, including its terminal continuation.",
            "caption_note": "English caption tracks exposed by the public Android player response are archived as VTT; auto-generated tracks are labeled auto in filenames and manifests.",
        },
        "items": youtube_items,
    })
    write_json(NORMALIZED / "cross-platform-content-map-2023-2026.json", {
        "metadata": {
            "snapshot_date": SNAPSHOT,
            "method": "Exact normalized-title matches only; unmatched or differently titled items are not forced together.",
            "cross_platform_group_count": len(crossposts),
        },
        "groups": crossposts,
    })
    write_json(SUBSTACK_RAW / "manifest.json", {
        "captured_on": SNAPSHOT,
        "source": "https://a4mr.substack.com/",
        "item_count": len(substack_items),
        "receipts": substack_receipts,
    })
    write_json(YOUTUBE_RAW / "manifest.json", {
        "captured_on": SNAPSHOT,
        "source": YOUTUBE_VIDEOS,
        "video_count": len(youtube_items),
        "captioned_video_count": sum(row["caption_status"] == "available_archived" for row in youtube_items),
        "receipts": youtube_receipts,
    })
    print(json.dumps({
        "substack_items": len(substack_items),
        "youtube_videos": len(youtube_items),
        "captioned_videos": sum(row["caption_status"] == "available_archived" for row in youtube_items),
        "cross_platform_groups": len(crossposts),
    }, indent=2))


if __name__ == "__main__":
    main()
