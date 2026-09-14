# Companion Research Corpus

Audit date: **2026-09-14**

The user's private Google Drive folder `PCA Research` is a companion research corpus. The direct folder audit found **14 items: 11 authored research documents and 3 source PDFs**.

It contains two different kinds of material:

1. **Authored synthesis / discussion documents** — useful for research questions, argument structure, and context, but not independent primary evidence.
2. **Source documents** — PDFs or other source material that may support claims in the repository and should be registered or archived according to the source policy.

A fresh agent should not assume that every Drive document is duplicated in this public repository.

## Authored synthesis and discussion documents

The following 11 documents were direct children of the audited `PCA Research` folder and provide useful context for the broader research program:

- `PCA Research Documents - Master Guide`
- `PCA Present Concerns - One-Page Summary`
- `Pastoral Vision for a Confessional Presbyterian Church`
- `Confessional Subscription in Presbyterianism - What Does It Mean to Receive and Adopt the Westminster Standards?`
- `Asymmetric Confessional Vigilance in the PCA - Short Case File`
- `Women in Public Worship and Sacramental Service in the PCA`
- `The Zachary Garris Letters and the PCA`
- `A Letter Concerning the Women’s Council (long version)`
- `Pastoral Conversation Guide - Trinity Presbyterian Church`
- `Covered Before God: 1 Corinthians 11, Head Coverings, and the Reformed Tradition`
- `From the Beginning of the World Until Yesterday`

These documents may contain useful citations and research leads, but their prose should not be imported into `data/` as though it were primary-source evidence. Trace material claims back to the cited primary or reliable source whenever possible.

This audit inventories the folder and its direct source files. It does **not** claim that every external work cited inside all 11 authored documents has already been independently inventoried and registered in PCA-Data.

## Direct source documents in the Drive folder

The following three PDFs were direct children of the audited folder:

| Drive source | Repository status as of 2026-09-14 | Required handling |
| --- | --- | --- |
| `The Public Preaching of Women – by R.L. Dabney _ Reformed Theology at A Puritan's Mind.pdf` | **Metadata registered.** See `sources/manifests/companion-theological-sources-2026-09-14.json`; raw Drive PDF is not copied into the public repo and no app-facing source ID exists yet. | Use the registered public-source URL/bibliographic metadata. Promote to `data/sources.json` only if it supports an app-facing claim. |
| `Paul on Women Speaking in Church, by B.B. Warfield (1919).pdf` | **Metadata registered.** See the companion theological-source manifest; raw Drive PDF is not copied into the public repo and no app-facing source ID exists yet. | Use the PCA Historical Center public edition registered in the manifest. |
| `The Deaconess & the Household of God_ A Rejoinder to Dan Barber – Presbyterian Polity.pdf` | **Metadata registered.** See the companion theological-source manifest; raw Drive PDF is not copied into the public repo and no app-facing source ID exists yet. | Treat as attributable secondary theological/polity analysis unless a future normalized claim specifically needs it. |

A broader Drive search also surfaced a `PCA Study Report on Women in Ministry 2017.pdf`, but it was **not a direct child of the audited `PCA Research` folder**. Independently of that Drive copy, the repository already represents the official PCA Historical Center version as `src-ga45-women-serving-2017` and normalizes it under `sources/normalized/general-assembly/`.

## Sources discussed in Drive synthesis that are already represented in the repo

The companion corpus discusses several source families that the repository already tracks independently, including:

- the 2017 Women Serving study report;
- PCA General Assembly minutes and formal actions;
- the two public Zachary Garris letters;
- A Faithful PCA / `Looking Forward – Together`;
- National Partnership correspondence;
- Alliance for Mission & Renewal material;
- Prayer & Lament material;
- current institutional and church-role sources.

For these, the repository's primary source records, normalized datasets, and provenance receipts take precedence over citations embedded only in a Drive synthesis document.

## Source-completeness conclusion

As of this audit, **all three direct source PDFs in the audited `PCA Research` folder are discoverable from this repository through registered source metadata**. That does **not** mean every Drive PDF binary is copied into GitHub, nor should it be.

It also does **not** mean every underlying source cited inside the 11 authored synthesis documents has been independently registered. Those documents can contain citations and research leads that should continue to be traced back to primary or reliable sources as claims are normalized.

The current distinction is:

- **represented/normalized source families** — e.g. the official 2017 PCA study report, GA records, Garris letters, National Partnership, AMR, and other source families documented in `research/source-register.md`;
- **metadata registered only** — the three direct Drive source PDFs listed above;
- **authored synthesis only** — user-authored Drive documents whose cited claims must still be traced to underlying evidence.

If additional source files are later added to Drive, they are not automatically part of PCA-Data until this audit/manifest layer is updated.

## Maintenance

When a new source is added to the Drive corpus and becomes relevant to PCA-Data:

1. classify it as authored synthesis or evidence source;
2. register source/provenance metadata under `sources/manifests/` when appropriate;
3. register it in `data/sources.json` if it supports app-facing claims;
4. preserve a raw copy only when useful and legally appropriate;
5. add normalized extraction only when needed;
6. update `research/source-register.md` and this file if the corpus/source-coverage picture changes.
