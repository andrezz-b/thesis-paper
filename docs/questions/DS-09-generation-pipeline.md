---
id: DS-09
title: How are questions generated and checked (LLM + human review)?
area: dataset
status: open
phase: dataset
priority: high
depends_on: [DS-01, DS-02]
informs: [DS-10, RP-04]
---

## Question

What is the concrete generation pipeline: inputs, which LLM, prompts or templates,
and the human review procedure and criteria?

## Why it matters

Determines dataset quality and how many questions can be produced before the deadline
([DS-10](DS-10-dataset-size.md)).

## Notes

- Tentative: LLM generation with human checking.
- Which LLM? Probably Gemma on the HPC ([AG-04](AG-04-gemma-hpc.md)), since no API credits are planned.
- Query-first vs question-first:
  - query-first: sample a path or SPARQL query, then verbalise it. Used by WDQL's
    SPARQL-to-question agent, and similar to the templates in ReasonVQA and M³-VQA.
  - question-first: write the question, then the query.
- Review criteria to define: the entity is not named ([D-004](../decisions.md#d-004)), the question is natural
  and unambiguous, the gold query is correct ([DS-08](DS-08-gold-answers.md)).
- Review tooling is undecided.

## Resolution

_Not resolved yet._
