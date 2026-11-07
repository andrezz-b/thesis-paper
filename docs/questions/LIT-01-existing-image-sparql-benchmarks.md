---
id: LIT-01
title: Does a benchmark with image + question + gold SPARQL already exist?
area: literature
status: researching
phase: dataset
priority: high
depends_on: []
informs: [FR-01, DS-01, DS-09]
---

## Question

Is there already a dataset or benchmark that pairs an image and a question with an
executable gold SPARQL query (over Wikidata or another KG)? How does this thesis
differ from the closest work?

## Why it matters

The working assumption is that no such dataset exists. That claim motivates the
dataset part of the thesis, so it must hold up. The answer also shapes the research
questions ([FR-01](FR-01-research-questions.md)).

## Notes

Closest candidates found so far (details and links in
[`../related-work.md`](../related-work.md)). For each, check: is gold SPARQL
released? Is the entity in the image named in the text? Which KG? Multi-hop? Is an
image index with distractors provided? Are agentic systems evaluated?

- **M³-VQA** (ACL 2026): uses SPARQL over Wikidata (QLever) to extract answers,
  multi-entity and multi-hop, evaluates agentic retrieval. Closest so far; check
  whether the queries are released.
- **ReasonVQA** (ICCV 2025): 1–3 hop questions generated from Wikidata.
- **WikiVQABench** (2026): knowledge-grounded VQA from Wikipedia and Wikidata,
  multiple-choice.
- **KVQA** (AAAI 2019): persons, Wikidata, reference images for visual entity linking.
- **InfoSeek** (EMNLP 2023), **Encyclopedic-VQA** (ICCV 2023), **ViQuAE** (SIGIR 2022):
  entity-centric knowledge VQA; answers, not SPARQL.

Likely gap (to be confirmed): executable gold SPARQL + a shared image index with
distractors + evaluation of agentic text-to-SPARQL systems.

Expected output: a comparison table in `related-work.md` and a short gap statement in
`THESIS.md`.
- 2026-11-04 (supervisor meeting): visual knowledge graphs were suggested as
  inspiration for visual papers; see [LIT-05](LIT-05-visual-knowledge-graphs.md).
- 2026-11-07: M3-VQA checked (paper, GitHub repo, Hugging Face dataset). Released fields are question, answers, answer aliases, image entity names (labels, no Wikidata IDs), Wikipedia evidence sentences and URLs; there is no SPARQL and no QIDs. SPARQL was used only during construction of the parallel questions (paper §4.1); QLever was used for entity linking (App. D.2). So M3-VQA does not release image + question + gold SPARQL and contrasts with the planned dataset. Other candidates (ReasonVQA, WikiVQABench) are still unchecked. Source: [M3-VQA note](../literature/ma2026m3.md).

## Resolution

_Not resolved yet._
