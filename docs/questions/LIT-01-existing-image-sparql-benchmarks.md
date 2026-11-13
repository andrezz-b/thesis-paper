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
- 2026-11-07: KVQA checked (full paper). Gold answers come from SPARQL over Wikidata (RDF dump of 2018-05-05) but the queries are deliberately not released (S3, p. 8879). Entities are persons only, identified by face; no agentic system, baselines are memory networks. So KVQA does not release image + question + gold SPARQL and contrasts with the planned dataset. Source: [KVQA note](../literature/shah2019kvqa.md).
- 2026-11-07: ReasonVQA checked (paper, project page, demo, code repository). Wikidata, 1 to 3 hops, images from Visual Genome and Google Landmarks v2; the released items are question + answer (open-ended or multiple choice), SPARQL is used only to link objects and fetch facts (§3.1, App. 1.2). The project page and demo do not mention SPARQL, the code repository held only a LICENSE file on 2026-11-07, and the Hugging Face release (checked later the same day) has per question the main-entity QID, a route of QIDs, the last property and the hop count, but no SPARQL. Questions name the class ("this church"), there is no image index and only plain vision-language models are evaluated (§4.2). So ReasonVQA does not provide image + question + gold SPARQL and contrasts with the planned dataset. WikiVQABench is still unchecked. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-08: InfoSeek checked (full paper, [note](../literature/chen2023can.md)). The Wikidata split (1.3M) turns triples for 300 relations into questions with human-written templates (§3.2); each question comes from one triple, so single-hop. The depicted entity is not named (hypernym placeholder). No gold SPARQL is described or released. Only pipelines and end-to-end models are evaluated, no agent. Contrasts with our gold-SPARQL, agentic setup, like the other benchmarks above.
- 2026-11-08: OVEN checked (full paper, [note](../literature/hu2023open.md)). It is the standalone identification step: image + intent query (entity not named; annotators rewrote the human-set queries so no other object fits, App. 10.2) linked to one of 6,063,945 English Wikipedia entities (dump 2022-10-01). Output is an entity, no gold SPARQL, no KG reasoning, no agent; entities not shown in the image are left to follow-up work (InfoSeek). Contrasts with our setup. Possible source of example images and entities (user's view), but a lower one than ReasonVQA, whose multi-hop questions are linked through SPARQL. Source: [OVEN note](../literature/hu2023open.md).
- 2026-11-12: RETINA checked (full paper, [note](../literature/lee2025breaking.md)). Wikipedia text KB, not Wikidata; 120k generated training questions and a 2k human-curated test set; the question never names the depicted entity (demonstrative phrase), but there is no SPARQL or graph query, only a gold Wikipedia document; no agent, retrievers plus a fixed VILA-13B reader (Sec. 3, 5.1). Contrasts with our setup; relevant for the related-entity-image idea ([DS-07](DS-07-related-entity-images.md)).

## Resolution

_Not resolved yet._
