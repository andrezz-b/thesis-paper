---
id: DS-14
title: Which labels does each dataset question carry?
area: dataset
status: researching
phase: dataset
priority: medium
depends_on: [DS-01]
informs: [DS-13, RP-03, EV-01]
---

## Question

Which labels (e.g. number of hops, question type, answer type, image role,
distractor setting, difficulty) are attached to each item, so that it is clear what
each question tests and what the dataset as a whole contains?

## Why it matters

Labels give an overview of the dataset (distribution of types, hops, ...) and allow
reporting results per label. They are part of the record format ([RP-03](RP-03-dataset-format.md)).

## Notes

- 2026-11-04 (supervisor meeting, user's notes): label the questions with the number
  of hops, question type and other labels. The user's intent: label the different
  questions so we know what each one does and have a sense of what questions we
  have.
- Candidate labels (assistant suggestions, not decided): hop count ([DS-03](DS-03-hop-depth.md)), question
  type ([DS-01](DS-01-question-types.md)), difficulty level ([DS-13](DS-13-difficulty-levels.md)), answer type (entity, number, date,
  boolean, list), image role ([DS-05](DS-05-image-role.md)), Wikidata class of the depicted entity ([DS-02](DS-02-wikidata-subset.md)).
- [RP-03](RP-03-dataset-format.md) already lists "question type label(s), hop count" as candidate fields.
- 2026-11-05 (user): no further labels known yet beyond hops and question type.
- 2026-11-07: KVQA's ten non-exclusive challenge categories (spatial, 1-hop, multi-hop, Boolean, intersection, subtraction, comparison, counting, multi-entity, multi-relation) are a possible starting point for the tag set; not committed. See [LIT-02](LIT-02-question-type-taxonomy.md). Source: [KVQA note](../literature/shah2019kvqa.md).
- 2026-11-07: ReasonVQA tags each question with hop count, one or more of 20 knowledge domains (by property), whether scene-graph information was used, and the source image dataset (§3.2.1, §4.4, App. 2.2). Possible starting points for labels; not committed. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-08: entity popularity (e.g. Wikipedia page views or sitelink count; not decided how to measure) is a candidate label, since the vision-only configuration should do better on popular entities (user expectation, InfoSeek §5.2 Fig. 7). Source: [InfoSeek note](../literature/chen2023can.md).
- 2026-11-08: OVEN also splits results by monthly page views (Fig. 6), supporting popularity as a candidate label next to the InfoSeek evidence. Source: [OVEN note](../literature/hu2023open.md).
- 2026-11-13: user leaning: QAWiki's answer-type category (§3.1) is a candidate label; its property mention types (§3.3) are too costly to annotate and unlikely to be used. Quality tags are not labels here: tagged items are excluded ([DS-09](DS-09-generation-pipeline.md)). Source: [QAWiki note](../literature/loustaunau2025qawiki.md).

## Resolution

_Not resolved yet._
