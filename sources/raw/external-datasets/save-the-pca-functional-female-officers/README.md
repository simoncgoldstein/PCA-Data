# Save the PCA — Functional Female Officer dataset

Receipt captured: **2026-09-03**

## Primary source page

https://www.savethepca.com/downloads/

The source page labels the current workbook:

**Dataset, Updated February 8th, 2026**

## Direct workbook URL

https://www.savethepca.com/wp-content/uploads/2026/02/ffo_public_dataset_020826.xlsx

Filename inferred from the source URL:

`ffo_public_dataset_020826.xlsx`

## Source-page context

Save the PCA groups this workbook under `The Functional Female Officer Report Downloads` alongside:

- `Is There a Third Way in Complementarian Women’s Ministry?`
- `The Case for Commissioning (Not Ordaining) Deaconesses.`
- `Overture 34: Amend RAO 16 to Require Reporting on Session and Diaconate Membership and Duties`
- `The Functional Female Officer Report`

The source page also links later commentary from multiple authors. Those articles are secondary commentary and should remain separate from the dataset itself.

## Binary archive status

`raw_copy_status: pending-user-or-browser-upload`

The workbook URL is verified, but the current research runtime could not retrieve the XLSX binary. The web tool resolves the link but rejects the spreadsheet MIME type for direct parsing, and the container runtime lacks external DNS access.

**Needed later:** place the exact downloaded workbook at:

`sources/raw/external-datasets/save-the-pca-functional-female-officers/ffo_public_dataset_020826.xlsx`

After upload:

1. calculate SHA-256 and commit a manifest;
2. inspect workbook sheet names and raw headers;
3. export a lossless normalized JSON/CSV representation while retaining all raw fields;
4. resolve churches against the PCA church directory;
5. preserve all source/evidence URLs and notes in the workbook;
6. treat the 2026-02-08 classification as a versioned external assessment rather than the project's own conclusion.

## Attribution rule

The eventual graph must model:

`Save the PCA dataset (2026-02-08) → assessment/classification → Church`

separately from:

`Person → role/member/pastor → Church`

A pastor, staff member, elder, or member of a church classified by this dataset must **not** automatically inherit the dataset's classification as a personal theological position.

## Versioning rule

Do not overwrite prior assessments if Save the PCA publishes a later workbook. Each version receives its own source ID/date/hash and classification records so the site can show changes over time.
