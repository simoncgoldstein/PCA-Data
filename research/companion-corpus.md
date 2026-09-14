# Companion Research Corpus

Audit date: **2026-09-14**

The user's private Google Drive folder `PCA Research` is a companion research corpus. It contains two different kinds of material:

1. **Authored synthesis / discussion documents** — useful for research questions, argument structure, and context, but not independent primary evidence.
2. **Source documents** — PDFs or other source material that may support claims in the repository and should be registered or archived according to the source policy.

A fresh agent should not assume that every Drive document is duplicated in this public repository.

## Authored synthesis and discussion documents

The following documents were present in the audited Drive corpus and provide useful context for the broader research program:

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

## Source documents in the Drive corpus

| Drive source | Repository status as of 2026-09-14 | Required handling |
| --- | --- | --- |
| `PCA Study Report on Women in Ministry 2017.pdf` | **Represented.** The official PCA Historical Center report is registered as `src-ga45-women-serving-2017` and normalized under `sources/normalized/general-assembly/`. | Continue using the official PCA URL and normalized report/committee datasets. |
| `The Public Preaching of Women – by R.L. Dabney _ Reformed Theology at A Puritan's Mind.pdf` | **Drive-only / not yet explicitly registered in the repo source register.** | Add source metadata and an authoritative/original publication reference before using it as a repository evidence source. Do not copy the PDF into the public repo unless redistribution is appropriate. |
| `Paul on Women Speaking in Church, by B.B. Warfield (1919).pdf` | **Drive-only / not yet explicitly registered in the repo source register.** | Register bibliographic/source metadata and a stable public edition or archive reference before repository use. |
| `The Deaconess & the Household of God_ A Rejoinder to Dan Barber – Presbyterian Polity.pdf` | **Drive-only / not yet explicitly registered in the repo source register.** | Register the article URL, author/publisher/date, and retrieval metadata if it becomes evidence for a normalized claim. |

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

## Known source-completeness conclusion

As of this audit, **not every source file collected in Google Drive is independently registered or preserved in PCA-Data**. The most obvious gaps are the Dabney, Warfield, and Presbyterian Polity/deaconess source PDFs listed above.

This is a documentation/source-registration gap, not permission to infer claims from those works without citation. Future source-ingestion slices should add metadata and stable source references first, and copy raw binaries only when useful and legally appropriate.

## Maintenance

When a new source is added to the Drive corpus and becomes relevant to PCA-Data:

1. classify it as authored synthesis or evidence source;
2. register the source in `data/sources.json` if it supports app-facing claims;
3. preserve or manifest it under `sources/` when appropriate;
4. add normalized extraction only when needed;
5. update `research/source-register.md` and this file if the corpus/source-coverage picture changes.
