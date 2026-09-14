# National Partnership continuity analysis

This directory contains a bounded, reproducible analysis of how confirmed National Partnership (NP) identities recur in later or contemporaneous PCA public-action and leadership datasets already normalized in this repository.

The purpose is to test claims about **personnel continuity and longitudinal recurrence** without converting association into an unsupported ideological or organizational conclusion.

## What the analysis measures

The generator is:

`scripts/build-national-partnership-continuity-analysis.py`

It consumes the repository's conservative identity crosswalk and generated pairwise-overlap outputs, then writes:

- `continuity-summary.json` — machine-readable cohort coverage, headline continuity signals, identity-resolution warnings, and predictive-validity readiness;
- `action-overlap.csv` — one row per selected action/leadership dataset with confirmed overlap and bounded screening metrics.

For each tracked dataset the analysis distinguishes:

1. **confirmed canonical overlap** — the same reviewed canonical person occurs in NP and the target dataset;
2. **full-roster lower bound** — confirmed overlap divided by the full printed roster denominator;
3. **unresolved exact-name possible overlap** — the same normalized printed name occurs but does not yet share a confirmed canonical identity;
4. **same-name screening ceiling** — confirmed overlap plus unresolved exact-name possible overlap, shown only as a research-screening ceiling, not as confirmed identity.

## What it does not measure

This is **not** yet a causal or predictive-effect model.

In particular, do not treat every person without a confirmed canonical NP edge as a non-member. The NP source layer contains many confirmed printed-name memberships that are not yet canonically identity-resolved. Canonicalization is also plausibly non-random because people who recur elsewhere in the source universe are easier to resolve.

Therefore this analysis intentionally does **not** publish:

- NP-vs-non-NP risk ratios;
- odds ratios;
- causal estimates;
- claims that historical NP membership alone proves a person's complete contemporary theology;
- claims that AMR is formally or legally the same organization as NP.

## Organizational-continuity boundary

Personnel recurrence can be strong evidence of continuity while still falling short of formal succession.

A claim such as “four of six current AMR leaders are confirmed NP members” is a factual personnel-overlap statement. A stronger claim such as “AMR is the National Partnership renamed” would require separate organizational evidence: an explicit succession statement, transfer of governance/infrastructure, a continuation decision, or comparable primary evidence.

AMR's separately normalized organizational statements may be compared with NP organizing priorities downstream, but personnel overlap alone must not transfer every NP action or position to AMR, or vice versa.

## Predictive-validity readiness

Before making an “X times more likely” claim, the project should first:

1. improve identity resolution for the confirmed NP membership roster, especially exact-name possible overlaps with selected later actions;
2. define an opportunity-aware comparison cohort for each outcome;
3. separate events occurring during the 2013–2021 NP archive window from genuinely post-archive outcomes;
4. account for correlated actions so one coalition episode is not treated as many independent trials.

Until those conditions are met, the strongest defensible use of this directory is **descriptive continuity, recurrence, and prioritization of the next identity-resolution work**.
