---
id: RP-04
title: How is the new dataset repository structured?
area: repo
status: open
phase: dataset
priority: medium
depends_on: [DS-09, RP-02]
informs: []
---

## Question

How are pipeline stages, question types and generators organised in the new
repository based on the POC?

## Why it matters

Supporting several question types, distractor strategies and embedding models should
not require restructuring later.

## Notes

- Decided: a new repo based on `dataset-poc` ([D-012](../decisions.md#d-012)).
- POC layout ([repo](https://github.com/andrezz-b/thesis-dataset-poc),
  [AGENTS.md](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/AGENTS.md)):
  - [`lib/`](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/lib):
    Wikidata, Commons, schema, runner;
  - [`embeddings/`](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/embeddings):
    pluggable providers;
  - [`vector_index/`](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/vector_index):
    Qdrant;
  - [`examples/<id>/`](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples):
    one folder per hand-made example.
- Likely stages: choose domain, select entities, generate questions, validate, human
  review, build index.
- Ideas: question types and distractor strategy as configuration; one generator per
  type.
- Vector database: Qdrant in the POC; to be confirmed.

## Resolution

_Not resolved yet._
