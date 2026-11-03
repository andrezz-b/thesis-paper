---
id: RP-02
title: Which programming language(s) for the dataset pipeline and the agent?
area: repo
status: open
phase: dataset
priority: high
depends_on: []
informs: [RP-04]
---

## Question

Does the new dataset repo stay JavaScript like the POC, and what is the agent written
in?

## Why it matters

Decides whether there is one stack or two, and what can be reused.

## Notes

- The [POC](https://github.com/andrezz-b/thesis-dataset-poc) is JavaScript only
  (Node 24, ESM, explicitly "no Python"), using `wikibase-sdk`, Qdrant and
  `@huggingface/transformers`.
- The agent is likely Python (the OpenAI-compatible CampusAI API, GRASP and most KGQA code are Python;
  [AG-01](AG-01-own-agent-vs-grasp.md)).

## Resolution

_Not resolved yet._
