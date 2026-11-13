---
id: DS-08
title: How are gold queries and gold answers defined, frozen and verified?
area: dataset
status: researching
phase: dataset
priority: high
depends_on: [LIT-03, DS-04]
informs: [RP-03, EV-01]
---

## Question

What does a gold record contain (query, result, which columns), how are gold results
frozen in time, and how is each gold query checked for correctness?

## Why it matters

Evaluation compares the results of the predicted and gold queries ([D-007](../decisions.md#d-007)), so the gold
result defines what "correct" means.

## Notes

- Decided: execution-based evaluation ([D-007](../decisions.md#d-007)).
- Tentative (as in the
  [POC gold queries](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/README.md)):
  the gold query hard-codes the depicted entity, e.g.
  `BIND(wd:Q219691 AS ?product)`. This keeps image grounding separately measurable.
- Open points:
  - **Answer columns:** which projected columns count. POC queries also project
    intermediate variables and labels.
  - **Snapshot:** store gold results with a date (see [DS-04](DS-04-endpoint-snapshot.md)).
  - **Verification:** the query runs and returns a non-empty, stable result; a human
    checks it; optionally an independently written second query gives the same
    result.
  - **Edge cases:** multiple valid answers, ties, yes/no questions (ASK queries).
- 2026-11-06: SPINACH gold queries are real queries run on the live Wikidata Query Service, kept only if non-empty and under 10 MB, with optimisation, formatting and `mwapi` clauses removed (§3, §3.1, App. C.3); no snapshot date is stated. Source: [SPINACH note](../literature/liu2024spinach.md).
- 2026-11-07: Possible shortcut (user idea, not decided): derive a first gold query from ReasonVQA items; recorded in [DS-09](DS-09-generation-pipeline.md). Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-08: KGVoyager failure analysis (App. F, Table 9): 18% of complete failures (28 of 156) are answer-representation errors, where the content is analogous to the gold but the form differs: result shape (20, e.g. extra label columns), SELECT instead of ASK (4), label instead of IRI (4). Relevant for which columns count and for yes/no questions. Source: [KGVoyager note](../literature/wisam2026kgvoyager.md).
- 2026-11-13: QAWiki writes each gold query "as generally as possible" (property paths such as `P131*/P17?/P30?` so the entity can be swapped) and allows several gold queries per question; gold returns identifiers only (§3.4, §4.1). User is unsure about both; recorded as options, not adopted. Its query tags no ties and incomplete (§3.5) are handled by exclusion here ([DS-09](DS-09-generation-pipeline.md)). Result-only scoring can credit a wrong query, especially for ASK (§4.4). Source: [QAWiki note](../literature/loustaunau2025qawiki.md).

## Resolution

_Not resolved yet._
