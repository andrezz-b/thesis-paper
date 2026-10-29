---
id: IX-04
title: What does the index store per entity?
area: index
status: open
phase: dataset
priority: low
depends_on: []
informs: [AG-02]
---

## Question

Which payload is stored with each vector (QID only, label, description), and how many
images per entity go into the index?

## Why it matters

Determines what the image tool returns to the agent.

## Notes

- Leaning: QID only. The agent can look up labels through SPARQL.
- POC payload: `{ qid, label, image }`. Answers are never stored in the index (see
  the conventions in the POC's
  [AGENTS.md](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/AGENTS.md)).

## Resolution

_Not resolved yet._
