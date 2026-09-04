# Source access gap ledger

Last reviewed: 2026-09-04

## Purpose

This file is the durable backlog for sources that are known to exist or are strongly evidenced, but that the current research environment could not fully retrieve, inspect, or evaluate. These are not treated as negative evidence, and missing person-level data must not be reconstructed from aggregate counts or secondary summaries.

When a future research pass encounters another known-but-inaccessible source, add it here with: source identity, what is missing, current blocker, evidence already preserved, and the concrete recovery path.

## Active gaps

### 1. 1999 PCA General Assembly minutes, 27th General Assembly

**Primary source:** `https://www.pcahistory.org/pca/ga/27th_pcaga_1999.pdf`

**Current blocker:** The official PDF is an unusually large scanned file, approximately 219 MB in the 2026-09-04 retrieval attempt. The web PDF retriever would not open it, and the local runtime could not directly fetch the host. The source is identified, but the relevant page images could not be inspected in the current environment.

**Still needed:**

- pp. 117-118, 27-31: the 61 commissioners who recorded negative votes on the MNA recommendation concerning MNA staff and women speaking/teaching
- p. 170, 27-44, III.10: the 144 commissioners who recorded affirmative votes on the substitute answering Western Carolina Presbytery Overture 16 affirmatively
- pp. 211-212, 27-57: Protests 3 and 4 related to the women teaching/preaching controversy

**Already preserved:** Event-level counts/actions are represented in the women/deacons/worship chronology, and `research/batch3-source-gaps.md` records the same roster gaps.

**Recovery path:** Obtain the official PDF outside the restricted retriever, extract only the cited pages as smaller PDF/image files, then transcribe and normalize the names from those page images against the primary source.

### 2. 2000 PCA General Assembly minutes, 28th General Assembly

**Primary source:** `https://www.pcahistory.org/pca/ga/28th_pcaga_2000.pdf`

**Current blocker:** The official PDF is an unusually large scanned file, approximately 319 MB in the 2026-09-04 retrieval attempt. The web PDF retriever would not open it, and the local runtime could not directly fetch the host.

**Still needed:**

- p. 101, 28-31, III.9: the 16 commissioners who registered affirmative votes on the defeated amendment to MNA Recommendation 9
- p. 101, 28-31, III.9: the 20 commissioners who registered negative votes on adoption of Recommendation 9

**Already preserved:** Event-level counts/actions are represented in the women/deacons/worship chronology, and `research/batch3-source-gaps.md` records the same roster gaps.

**Recovery path:** Download the official minutes outside the restricted retriever, isolate p. 101, and ingest the primary page image/text.

### 3. 2002 Women in the Military final-action recorded-vote roster

**Known primary-source family:** `https://www.pcahistory.org/pca/studies/aiscwim.html` plus the official 30th General Assembly minutes.

**Current blocker:** The PCA Historical Center HTML confirms the final action and that 77 commissioners requested their negative votes be recorded, but the accessible HTML does not expose the 77 names. The full named roll must therefore be recovered from the official 2002 General Assembly minutes or equivalent primary page images.

**Still needed:** The complete 77-name negative-vote roster.

**Already preserved:** The event-level action and aggregate count are retained; no names have been inferred.

**Recovery path:** Locate the exact 30th GA minutes pages containing the recorded votes, acquire those pages as images/PDF, and normalize only the names actually printed there.

### 4. 2002 subscription action recorded-vote roster

**Known source:** 2002 PCA General Assembly subscription action documented in the repository's formal-position research and post-merge audit.

**Current blocker:** The event-level record establishes 127 recorded negative votes, but the complete named roster has not been recovered from the primary General Assembly minutes in the current research environment.

**Still needed:** The complete 127-name negative-vote roster.

**Already preserved:** The event-level count/action is retained without manufacturing person-level positions.

**Recovery path:** Identify the exact 30th GA minutes pages for the subscription action, recover the primary page images, and ingest the printed names.

### 5. Revoice 2018 original printed program / complete workshop schedule

**Known source class:** Original Revoice 2018 attendee program, program packet, or equivalent first-party schedule artifact.

**Current blocker:** Repository recovery work established first-party fragments and evidence that attendees possessed a printed program/program-like packet, but the complete original approximately 26-workshop program has not been recovered. Later mixed media galleries and surviving web fragments are not sufficient to reconstruct the whole program without inference.

**Still needed:** A complete primary copy or sufficiently complete sequence of scans/photos showing the original workshop/session schedule and named participants.

**Already preserved:** Confirmed fragments, bounded participation evidence, and the distinction between confirmed material and unrecovered program content. The exploratory Wayback asset-recovery workflow branch was intentionally not merged because it produced no durable additional primary evidence.

**Recovery path:** Search attendee archives, scans, photographs, contemporary social-media images, archived attachments/assets, and personal copies. If a complete copy surfaces, preserve the original artifact before normalization.

### 6. PCA “A Call to Prayer & Lament” original statement and signer page

**Known primary source:** `https://www.pcaprayerandlament.com/`

**Current blocker:** The original site was not retrievable in the 2026-09-04 research environment. Search results expose secondary critiques, reports, and descriptions of the statement, but those sources are not an acceptable substitute for the original statement text or original signer page.

**Still needed:**

- the complete first-party text of `A Call to Prayer & Lament`
- the original named signatory list and role labels from a stable first-party capture
- any first-party explanation of the authorship/organizing group and the separate later `Committed to Prayer & Lament` list if that list remains distinct

**Already preserved:** Secondary sources establish that the statement existed and was publicly signed, but no statement-level or signer-level records have been normalized from those secondary descriptions.

**Recovery path:** Manual/local browser capture of the original site or a faithful first-party/archive snapshot. Preserve the page text and signer list before normalization. Do not reconstruct the statement or signer roster from hostile or sympathetic secondary commentary.

### 7. 2021 Overture 37 recorded-negative-vote roster

**Primary source:** `https://www.pcahistory.org/pca/ga/48th_pcaga_2021.pdf`, Minutes pp. 91-96.

**Current blocker:** The repository chronology records that 207 commissioners requested their negative votes on the final Overture 37 action be recorded, and the official minutes are text-indexed in the current web environment. However, the PDF page-image/screenshot interface could not open the relevant pages, so the complete 207-name roster could not be safely transcribed and verified here. Secondary summaries confirm the count but are not sufficient to reconstruct the official roster.

**Still needed:** The complete 207-name recorded-negative-vote roster exactly as printed, including office and presbytery labels where present.

**Already preserved:** The event-level action and 207-person count are represented in `sources/normalized/general-assembly/2019-2023-sexuality-formal-position-chronology.json`. The 28-name Overture 37 minority-report signer roster is separately normalized and must not be substituted for the negative-vote roster.

**Recovery path:** Manual/local inspection of Minutes pp. 91-96 from the repository's existing 2021 GA PDF or a locally downloaded official copy; transcribe the printed roster and normalize only after page-image verification. Do not spend automated research cycles on alternate extraction workarounds.

## Current partial-evaluation items

These are not wholly inaccessible sources, but their evidence is incomplete enough that future work should not mistake current coverage for source saturation.

### Save the PCA February 8, 2026 Functional Female Officer workbook

The exact research copy supplied to this project was analyzed and is identified by SHA-256 `b746fbdd1ccbb6087feeb6ed5abee91b4ac203a3cacc08de167c46a8cf9d0150`. Its sheet structure, row counts, classifications, and source metadata are preserved in `sources/raw/external-datasets/save-the-pca-functional-female-officers/README.md`.

**Current blocker:** The public hosted XLSX at `https://www.savethepca.com/wp-content/uploads/2026/02/ffo_public_dataset_020826.xlsx` could not be independently binary-downloaded in the current runtime, and the exact XLSX binary has not yet been committed to the repository. Therefore byte-for-byte equality between the analyzed research copy and the currently hosted public file has not been independently established.

**Still needed:** Download the hosted XLSX outside the restricted runtime, compare its SHA-256 to the research copy, and if it matches, preserve that exact binary in the repository source directory. If it differs, retain both dated versions and normalize the hosted version separately.

**Recovery path:** Manual/local browser download and hash comparison. Do not spend automated research cycles on alternate binary-download workarounds.

### AMR archived captions

The AMR video inventory and archived caption tracks are accessible. Multiple bounded issue-position extractions are now normalized, but the remaining caption corpus has not yet been exhaustively evaluated for issue-level claims. This is a research-completeness gap, not an access failure.

### Long-tail identity cases

Some source records remain unmatched or review-only because available evidence is insufficient to prove identity equivalence. These are not source-access failures and must remain separate from this ledger's inaccessible-source entries. Do not resolve them by generalized middle-initial, nickname, or ideological heuristics.

## Evidence rule

- A known source that cannot be opened is a backlog item, not evidence of absence.
- Aggregate counts do not create named person-level records.
- Secondary sources may help locate a primary source, but should not be used to reconstruct an unavailable official roll call by inference.
- Partial archives must be labeled partial.
- Whenever a future source cannot be retrieved or evaluated, add it to this ledger before moving on so the gap remains actionable.
