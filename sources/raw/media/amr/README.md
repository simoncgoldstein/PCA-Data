# Alliance for Mission & Renewal media archive

This source family preserves AMR's public website, Substack, and YouTube inventories as dated snapshots. Platform duplication is recorded explicitly so the same content is not counted as multiple independent publications.

## Captures

- `blog-pages-2026-09-03/`: AMR website home and twelve blog pagination pages; 120 normalized items.
- `substack-2026-09-03/`: all public archive API pages plus the RSS feed; 128 archive records and five RSS-only podcast companion records.
- `youtube-2026-09-03/`: the public channel Videos tab, terminal continuation, per-video public player metadata, and 31 English caption tracks.

Each capture directory contains a machine-readable manifest with the URL, local path, byte size, and SHA-256 hash of every receipt. YouTube files ending in `-auto-1.vtt` are explicitly auto-generated English captions, not publisher-edited transcripts.

Normalized outputs live under `sources/normalized/amr/`. Cross-platform links use exact normalized titles or explicit embedded-video IDs; differently titled items are not merged by similarity alone.
