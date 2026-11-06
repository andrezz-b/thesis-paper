---
id: DS-09
title: How are question ideas collected and curated into items?
area: dataset
status: researching
phase: dataset
priority: high
depends_on: [DS-01, DS-02]
informs: [DS-10, RP-04]
---

## Question

How are question ideas collected from LLMs (prompts, scope, which models), and how
are they curated into items: the procedure and the acceptance criteria?

## Why it matters

Determines dataset quality and how many questions can be produced before the deadline
([DS-10](DS-10-dataset-size.md)).

## Notes

- Superseded by [D-016](../decisions.md#d-016) (2026-10-30): "Tentative: LLM generation with human
  checking." Now: LLMs only suggest question ideas; curation is manual.
- Superseded by [D-016](../decisions.md#d-016) (2026-10-30): "Which LLM? Probably Gemma on the HPC
  ([AG-04](AG-04-gemma-hpc.md)), since no API credits are planned." Now: any available LLM, also
  through a chat interface; Gemma on the HPC is not used for the dataset.
- Query-first vs question-first (with [D-016](../decisions.md#d-016) the approach is question-first; the
  options are kept for reference):
  - query-first: sample a path or SPARQL query, then verbalise it. Used by WDQL's
    SPARQL-to-question agent, and similar to the templates in ReasonVQA and M³-VQA.
  - question-first: write the question, then the query.
- Review criteria to define: the entity is not named ([D-004](../decisions.md#d-004)), the question is natural
  and unambiguous, the gold query is correct ([DS-08](DS-08-gold-answers.md)).
- Review tooling is undecided.
- 2026-10-30: The plan has a pilot round 2026-12-14 to 2026-12-22 and full
  curation 2027-01-04 to 2027-01-22 ([D-015](../decisions.md#d-015)). Earlier the pilot was meant to set an
  acceptance-rate target for a dataset hypothesis; that hypothesis was removed
  ([D-017](../decisions.md#d-017)).
- 2026-10-30: Method decided in [D-016](../decisions.md#d-016): LLMs suggest question ideas from prompts
  that state the scope (question types, difficulty); ideas become items only if
  they meet the acceptance criteria; prompts and models used are logged.
- 2026-10-30: Working list of acceptance criteria [Tentative]:
  - a single correct, unambiguous answer;
  - the answer is stable in the snapshot used ([DS-04](DS-04-endpoint-snapshot.md));
  - the depicted entity is not named ([D-004](../decisions.md#d-004));
  - the image is necessary (not answerable from the text alone);
  - the gold SPARQL query runs and returns the answer ([DS-08](DS-08-gold-answers.md));
  - natural phrasing;
  - the image licence allows reuse ([D-005](../decisions.md#d-005)).
- 2026-11-04 (supervisor meeting): ideas should cover a range of difficulty and
  carry labels ([DS-13](DS-13-difficulty-levels.md), [DS-14](DS-14-question-labels.md)).
- 2026-11-06: SPINACH built its dataset with an LLM-assisted, expert-verified pipeline: GPT-4o suggested verbalisations and a modify/include/exclude decision, experts verified by running intermediate queries (App. C.3). Supports [D-016](../decisions.md#d-016) and can be cited in the method section. Source: [SPINACH note](../literature/liu2024spinach.md).

## Resolution

_Not resolved yet._
