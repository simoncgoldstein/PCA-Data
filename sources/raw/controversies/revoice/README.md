# Revoice / Side-B controversy in the PCA

This directory is the source dossier for the Revoice-related PCA controversy. Revoice itself was not a PCA agency, so the data model must distinguish conference participation from ecclesiastical actions by Memorial Presbyterian Church, Missouri Presbytery, the General Assembly, and the Standing Judicial Commission.

## Core primary and near-primary sources

### 2018 conference / Memorial Presbyterian

Official later SJC summary in 49th GA Minutes, vol. 2:
https://www.pcahistory.org/pca/ga/49th_pcaga_2022_vol02.pdf

SJC Case 2020-05 states that Memorial Presbyterian Church (PCA), St. Louis, hosted the first Revoice Conference in July 2018 and records the subsequent Missouri Presbytery process.

### Missouri Presbytery investigation and response

Missouri Presbytery open letter, January 2020, republished by The Aquila Report:
https://theaquilareport.com/a-letter-to-the-churches-regarding-revoice-and-pastor-greg-johnson/

The letter states that Missouri Presbytery:
- formed a committee in late 2018 to examine Revoice and Memorial's involvement;
- received its report at a called meeting in May 2019;
- initially approved nine theological judgments and one judicial judgment;
- partially sustained a complaint concerning that action in October 2019;
- reconsidered/amended theological judgments in December 2019;
- investigated whether there was a strong presumption of guilt against Memorial and TE Greg Johnson;
- created a separate affirmations/denials project concerning the issues raised by Revoice;
- supported a denominational study committee on human sexuality.

### 47th General Assembly, 2019

Official minutes:
https://www.pcahistory.org/pca/ga/47th_pcaga_2019.pdf

Key event families to normalize:
- Overture 4 concerning the Nashville Statement.
- Overture 28 and the minority report.
- TE Steven Warhurst's speech supporting the Overture 28 minority report.
- TE Kevin Twit's formal protest concerning language in Warhurst's speech.
- Every signer of the Warhurst protest, exactly as printed in the Minutes.

Useful structured secondary presentation keyed directly to the Minutes:
https://pcapolity.com/case-studies/protest-case-study/overture-28/
https://pcapolity.com/case-studies/protest-case-study/minority-report-supporting-speech/

### Human Sexuality study committee and 48th GA, 2021

Official 48th GA Minutes:
https://www.pcahistory.org/pca/ga/48th_pcaga_2021.pdf

Normalize separately:
- Ad Interim Committee on Human Sexuality membership/authorship.
- Overture 23.
- Overture 37.
- Overture 37 minority report authors/signers and precise proposed language.
- Other formal protests/minority reports directly related to sexual identity, sanctification, officer qualifications, or Side-B terminology.

### SJC decisions / 49th GA, 2022

Official 49th GA Minutes, vol. 2:
https://www.pcahistory.org/pca/ga/49th_pcaga_2022_vol02.pdf

At minimum normalize:
- SJC Case 2020-05, Ryan Speck v. Missouri Presbytery.
- SJC Case 2020-12 and related Greg Johnson/Missouri Presbytery litigation.
- Every commissioner/committee role that is actually named in the formal record.

### Overture 15 and related 2022 actions

Official 49th GA Minutes:
https://www.pcahistory.org/pca/ga/49th_pcaga_2022.pdf

Overture 15 proposed constitutional language disqualifying men who describe themselves as homosexual from church office. The Overtures Committee narrowly recommended answering it in the negative; a minority report recommended affirmative action as amended and contains named signers. Preserve:
- majority action and vote;
- minority-report text;
- every minority-report signer;
- any recorded floor speeches/protests;
- subsequent presbytery ratification vote data where verifiable from official presbytery or GA records.

### Memorial departure, 2022

ByFaith report of Missouri Presbytery's statement:
https://byfaithonline.com/missouri-presbytery-explains-actions-regarding-memorial-pres/

It records that Memorial voted to withdraw from the PCA on 2022-11-18 and that Missouri Presbytery on 2022-12-06 acknowledged the departure; Doug Mendis was honorably retired while Greg Johnson, Keith Robinson, and Sam Dolby requested removal of their names from the presbytery rolls.

## People/entities to model explicitly

This is not an ideological label list. These are roles requiring exact edge types:

- Greg Johnson → Memorial Presbyterian / Revoice / Missouri Presbytery cases
- Memorial Presbyterian Church → host of Revoice 2018
- Missouri Presbytery → investigation, reports, complaints, judicial actions
- Ryan Speck → complainant in SJC cases
- Steven Warhurst → 2019 minority-report speech
- Kevin Twit → protest author/signatory organizer concerning Warhurst speech
- all Warhurst protest signers → public formal protest
- all Overture 37 minority report signers → formal minority report
- all Overture 15 minority report signers → formal minority report
- Human Sexuality AIC members → committee membership, not automatically a stance beyond their actual report/actions

## Required source discipline

- Revoice conference attendance/speaking is a conference edge.
- Hosting Revoice is a church/institution edge.
- Signing a protest/minority report is a formal ecclesiastical-action edge.
- A presbytery vote with no roll call must never be converted into person-level voting claims.
- 'Side B', 'gay Christian', 'Revoice supporter', and similar labels must only be attached where the source directly supports the terminology or role.

## Next pass

1. Extract all 2019 Warhurst protest signers.
2. Extract Human Sexuality AIC roster and report positions.
3. Extract 2021 Overture 23/37 proponents, minority-report signers, and votes.
4. Extract SJC case participants and judgments.
5. Extract 2022 Overture 15 minority-report signers and presbytery ratification results.
6. Cross-reference all resulting people with NP, A Faithful PCA, AMR, Prayer & Lament, Garris letters, racial-reconciliation publications, NAE protest, and current roles.
