---
id: RP-01
title: Where are images stored?
area: repo
status: open
phase: dataset
priority: high
depends_on: []
informs: [RP-06]
---

## Question

How are index images and query images stored and distributed for the (public) dataset
repository?

## Why it matters

Affects repository size, reproducibility and licence compliance.

## Notes

- Options:
  - commit to git (the
    [POC](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples) commits
    512 px thumbnails);
  - git-LFS;
  - Google Drive or similar;
  - store only Commons URLs and fetch them with a reproducible download script plus a
    local cache.
- Assistant suggestion (not decided): URLs + script + cache, which keeps the repo
  small and attribution exact.
- The repo will be public ([D-011](../decisions.md#d-011)). Commons licences (often CC BY-SA) allow
  redistribution with attribution.

## Resolution

_Not resolved yet._
