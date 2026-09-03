# Save the PCA — Functional Female Officer dataset

Receipt captured: **2026-09-03**

## Primary source page

https://www.savethepca.com/downloads/

The source page labels the current workbook:

**Dataset, Updated February 8th, 2026**

## Direct workbook URL

https://www.savethepca.com/wp-content/uploads/2026/02/ffo_public_dataset_020826.xlsx

## Verified workbook supplied to this research project

Conversation upload located and materialized on 2026-09-03:

`ffo_public_dataset_020826(2).xlsx`

Size: **446,537 bytes**

SHA-256:

`b746fbdd1ccbb6087feeb6ed5abee91b4ac203a3cacc08de167c46a8cf9d0150`

The workbook's internal file timestamps are 2026-02-08 and its sheet structure/content match the February 8, 2026 dataset described by Save the PCA's download page. The public URL could not be independently binary-downloaded in this runtime, so byte-for-byte equality with the hosted file has **not** been independently established. The hash above identifies the exact research copy analyzed here.

`raw_copy_status: available-in-chat; repository-binary-copy-pending`

The GitHub connector is suitable for text files but a 446 KB XLSX binary is awkward to push through the chat connector. Until a browser/Work pass can upload the binary directly, this directory preserves the public source URL, exact research-copy hash, sheet audit, and extracted source metadata.

## Workbook sheet audit

The exact uploaded workbook contains:

- `church_list`
- `statistics`
- `bucketed_data`
- `raw_data`
- `ambiguous_data`
- `presbyteries`
- `interactive_presbyteries`
- `interactive_titles`

### Core populated rows

Excluding headers/format-only blank rows:

- `church_list`: **1,964 churches**
- `raw_data`: **802 person/role instances**
- `bucketed_data`: **802 person/role instances**
- `ambiguous_data`: **180 person/role instances**
- `presbyteries`: **87 presbyteries**

### Workbook statistics / classifications independently recovered from the sheets

`church_list` contains source-attributed church-level fields for:

- Functional Female Elders? (Y/N)
- Functional Female Deacons? (Y/N)
- website/officer visibility fields
- website status
- comments

Counts from the exact uploaded workbook:

- churches classified `Functional Female Elders = Y`: **61**
- churches classified `Functional Female Deacons = Y`: **104**
- churches classified `Y` for both: **18**
- churches classified `Y` for either category: **147**
- churches classified `N` for both: **782**

Blank values are common because the workbook distinguishes reviewed/available evidence from churches where a classification was not available. Blank must **not** be normalized as `N`.

Website-status counts in `church_list`:

- Operational: **1,532**
- Korean: **213**
- No Website: **143**
- Broken: **65**
- Spanish: **8**
- Japanese: **1**
- Chinese: **1**
- Russian: **1**

### `raw_data` / `bucketed_data` receipt fields

Both core instance sheets contain:

- Presbytery
- Church
- Phone
- Website
- Position
- Name
- Review Date
- Archive Link

The `raw_data` sheet preserves the source site's wording for positions. `bucketed_data` preserves Save the PCA's normalized category. The archive links are especially important receipts and should remain attached to every imported person/role observation.

`ambiguous_data` additionally includes `Bucketed Position` while preserving the original ambiguous title.

## Normalization rule

The eventual graph must model:

`Save the PCA dataset (2026-02-08) → source-attributed assessment → Church`

and separately:

`Person → dated role/member/pastor relationship → Church`

A pastor, staff member, elder, deacon, or member of a church classified by this dataset must **not** automatically inherit the dataset's church-level classification as a personal theological position.

For instance-level rows, preserve both:

- the exact `Position` wording from `raw_data`;
- the normalized/bucketed title from `bucketed_data`;
- the `Archive Link` as the receipt for the underlying church webpage when supplied.

## Versioning rule

Do not overwrite prior assessments if Save the PCA publishes a later workbook. Each version receives its own source ID/date/hash and classification records so the site can show changes over time.

## Next import work

1. Create a normalized church table from all 1,964 `church_list` rows.
2. Create normalized role-observation tables from all 802 `raw_data` and `bucketed_data` rows, retaining archive links.
3. Preserve all 180 `ambiguous_data` rows as unresolved/source-attributed observations.
4. Resolve the 1,964 church records against an official PCA church-directory snapshot before attaching stable church IDs.
5. Cross-reference individuals only after identity resolution; same-name matches must remain unresolved until corroborated.
6. Upload the exact XLSX binary to this directory during the later browser/Work ingestion wave and verify its SHA-256 against the research copy above.
