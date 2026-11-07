---
id: DS-03
title: What is the maximum number of hops in a question?
area: dataset
status: open
phase: dataset
priority: medium
depends_on: [DS-01, DS-02]
informs: []
---

## Question

Up to how many hops (from the depicted entity to the answer) should questions go?

## Why it matters

Limits generation effort and query complexity; hop count is a natural axis for
reporting results.

## Notes

- The user has no preference yet.
- ReasonVQA uses 1–3 hops. The POC examples are 2–3 hops (e.g.
  [Game Boy](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples/game-boy):
  `manufacturer → founded by → date of birth`).
- Recognising the entity from the image is an extra grounding step before the first
  hop.
- 2026-11-04 (supervisor meeting): hop count is one candidate difficulty axis and a label per item; see [DS-13](DS-13-difficulty-levels.md) and [DS-14](DS-14-question-labels.md).
- 2026-11-07: M3-VQA reports 1, 2, 3 and 4+ hops (8.3%, 24.2%, 34.6%, 32.8% of 13,125 items; Table 2). Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-07: ReasonVQA caps questions at 3 hops as a trade-off between complexity and grammatical errors in generated questions (App. 1.2). Hop distribution: full set 1.36M / 2.81M / 5.4K for 1 / 2 / 3 hops, ReasonVQA-U 23.8K / 49.5K / 4.8K (App. 2.1, Table 2). Models do clearly worse on 3-hop, but 1-hop is only slightly better than 2-hop (§4.4, Fig. 6). Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).

## Resolution

_Not resolved yet._
