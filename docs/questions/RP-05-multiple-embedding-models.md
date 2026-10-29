---
id: RP-05
title: How does the repository support several embedding models?
area: repo
status: open
phase: dataset
priority: low
depends_on: [IX-03]
informs: []
---

## Question

How are several embedding models and their index collections handled side by side?

## Why it matters

Needed only if several embedding models are compared ([IX-03](IX-03-embedding-models.md)).

## Notes

- The POC already has a pluggable embedder registry
  ([`embeddings/index.js`](https://github.com/andrezz-b/thesis-dataset-poc/blob/main/embeddings/index.js),
  `EMBEDDER=<key>`) and names collections `<example id>__<model>`. With one shared
  index this becomes something like `<dataset>__<model>`.

## Resolution

_Not resolved yet._
