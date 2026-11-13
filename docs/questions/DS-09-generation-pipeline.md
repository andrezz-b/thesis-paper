---
id: DS-09
title: How are question ideas collected and curated into items?
area: dataset
status: researching
phase: dataset
priority: high
depends_on: [DS-01, DS-02]
informs: [DS-10, RP-04]
---

## Question

How are question ideas collected from LLMs (prompts, scope, which models), and how
are they curated into items: the procedure and the acceptance criteria?

## Why it matters

Determines dataset quality and how many questions can be produced before the deadline
([DS-10](DS-10-dataset-size.md)).

## Notes

- Superseded by [D-016](../decisions.md#d-016) (2026-10-30): "Tentative: LLM generation with human
  checking." Now: LLMs only suggest question ideas; curation is manual.
- Superseded by [D-016](../decisions.md#d-016) (2026-10-30): "Which LLM? Probably Gemma on the HPC
  ([AG-04](AG-04-gemma-hpc.md)), since no API credits are planned." Now: any available LLM, also
  through a chat interface; Gemma on the HPC is not used for the dataset.
- Query-first vs question-first (with [D-016](../decisions.md#d-016) the approach is question-first; the
  options are kept for reference):
  - query-first: sample a path or SPARQL query, then verbalise it. Used by WDQL's
    SPARQL-to-question agent, and similar to the templates in ReasonVQA and M³-VQA.
  - question-first: write the question, then the query.
- Review criteria to define: the entity is not named ([D-004](../decisions.md#d-004)), the question is natural
  and unambiguous, the gold query is correct ([DS-08](DS-08-gold-answers.md)).
- Review tooling is undecided.
- 2026-10-30: The plan has a pilot round 2026-12-14 to 2026-12-22 and full
  curation 2027-01-04 to 2027-01-22 ([D-015](../decisions.md#d-015)). Earlier the pilot was meant to set an
  acceptance-rate target for a dataset hypothesis; that hypothesis was removed
  ([D-017](../decisions.md#d-017)).
- 2026-10-30: Method decided in [D-016](../decisions.md#d-016): LLMs suggest question ideas from prompts
  that state the scope (question types, difficulty); ideas become items only if
  they meet the acceptance criteria; prompts and models used are logged.
- 2026-10-30: Working list of acceptance criteria [Tentative]:
  - a single correct, unambiguous answer;
  - no quality-tag issue: not subjective, and the gold result is not incomplete, tie-dependent or based on unconfirmed data (2026-11-13, [Tentative], from QAWiki §3.5);
  - the answer is stable in the snapshot used ([DS-04](DS-04-endpoint-snapshot.md));
  - the depicted entity is not named ([D-004](../decisions.md#d-004));
  - the image is necessary (not answerable from the text alone);
  - the gold SPARQL query runs and returns the answer ([DS-08](DS-08-gold-answers.md));
  - natural phrasing;
  - the image licence allows reuse ([D-005](../decisions.md#d-005)).
- 2026-11-04 (supervisor meeting): ideas should cover a range of difficulty and
  carry labels ([DS-13](DS-13-difficulty-levels.md), [DS-14](DS-14-question-labels.md)).
- 2026-11-06: SPINACH built its dataset with an LLM-assisted, expert-verified pipeline: GPT-4o suggested verbalisations and a modify/include/exclude decision, experts verified by running intermediate queries (App. C.3). Supports [D-016](../decisions.md#d-016) and can be cited in the method section. Source: [SPINACH note](../literature/liu2024spinach.md).
- 2026-11-07: KVQA paraphrased its test questions (online tool, human accept/refine/discard; S5, p. 8879). Possible later extension, not committed; if done, probably LLM-based. Source: [KVQA note](../literature/shah2019kvqa.md).
- 2026-11-07: ReasonVQA builds questions query-first by nesting hand-written templates per Wikidata property, 1 to 3 hops, over Visual Genome and Google Landmarks v2 images; it releases question + answer (open-ended or multiple choice), no gold SPARQL (§3.2.1, App. 1.2; project page and demo checked, the code repository held only a LICENSE file). Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
  - The user does not expect to leave the LLM-curated approach ([D-016](../decisions.md#d-016)) and sees ReasonVQA's pipeline only as a fallback to mention if that changes.
  - Idea (user, not decided): reuse ReasonVQA items as a cheap source of (image, question) pairs. The multiple-choice correct answer could be turned into a SPARQL query, giving a start for the gold query; we would still have to add the distractors ([IX-01](IX-01-distractor-strategy.md)) and write and verify the gold query ([DS-08](DS-08-gold-answers.md)).
  - Checked on the Hugging Face release (2026-11-07, a few rows read): each question has an annotation with the main-entity QID, a route of QIDs and the property of the last hop, plus the hop count, so a gold query can mostly be reconstructed; intermediate properties of 2- and 3-hop routes are not stored and would have to be recovered, e.g. by asking Wikidata which properties link consecutive route nodes (assistant suggestion). The data sample read (6,671 rows of the validation file) was all Google Landmarks v2, i.e. specific landmarks with Wikimedia Commons image URLs, which fits an entity-specific gold query ([D-004](../decisions.md#d-004), [D-005](../decisions.md#d-005)); questions about Visual Genome objects are about classes ("the appliance on the street") and would not fit without filtering.
  - Other caveats (assistant reading): the multiple-choice distractors are random, so they cannot be reused as our distractors; the dataset card says `agpl-3.0` and the Commons file licences were not checked; the domain is mostly landmarks and buildings, which may not match the Wikidata subset chosen in [DS-02](DS-02-wikidata-subset.md).
- 2026-11-07: Possible later check, not planned now (user): test whether ReasonVQA items can be turned into gold SPARQL by reconstructing queries for about 20 items from the released annotations (main-entity QID, route of QIDs, last property, hop) and counting how many resolve cleanly, e.g. by finding the properties that link consecutive route nodes. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-08: InfoSeek's generation recipe: human-written templates per Wikidata relation with a hypernym placeholder, a consistency filter (answer must be found in the entity's Wikipedia article; 97% passed), and subsampling by (relation, category) to avoid skew (§3.2, App. A.2). For us the Wikidata entity holds the answer, but the consistency check and subsampling are worth listing. Source: [InfoSeek note](../literature/chen2023can.md).
- 2026-11-08: OVEN's human evaluation set: 30+ annotators, three annotations per example, who check the entity link, check that the entity is physically present (10.3% not), and rewrite the query so no other object can be the answer and the answer is not in the question (99.9% rewritten; App. 10.2). A template for the review step; not a decision. Related work to read: LLM-assisted data construction for visual entity recognition (arXiv 2410.23676, queued). Source: [OVEN note](../literature/hu2023open.md).
- 2026-11-12: RETINA's pipeline (LLM extracts a one-hop graph with a relation sentence per related entity; query entity + qualifying entity for a unique answer; demonstrative instead of the entity name; paraphrase; BM25 filter; human curation, 29.16 % of 6k sampled questions kept) is described in Sec. 3.1 and App. A. User: the 2k curated test set is the more likely source of example questions; the LLM pipeline is a fallback if ideas run short, as it is not straightforward and every item still needs a gold query (leaning, not decided). The test set has no SPARQL (Sec. 3, 5.1). Source: [Lee et al. note](../literature/lee2025breaking.md).
- 2026-11-13: QAWiki tags questions as ambiguous or subjective and queries as incomplete, no ties (LIMIT 1 on a superlative) or controversial/unconfirmed data, and keeps them with best-effort queries (§3.5). User decision: we exclude such items instead (added to the acceptance criteria above as [Tentative]). QAWiki also runs 14 quality-control SPARQL queries over its Wikibase and uses LLMs to suggest phrasing corrections that are reviewed manually (§3.7), which fits [D-016](../decisions.md#d-016). Source: [QAWiki note](../literature/loustaunau2025qawiki.md).

## Resolution

_Not resolved yet._
