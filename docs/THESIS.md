# Thesis description

Source of truth for what this master thesis (DTU) is about. Agents: read this before
working on anything thesis-related. It reflects the *current* state and is updated as
the thesis progresses. Update it only through the `thesis-description` skill
(`.opencode/skills/thesis-description/SKILL.md`).

Markers used below:

- **[Decided]**: settled; the reason is in [`decisions.md`](decisions.md).
- **[Tentative]**: current working assumption; may change.
- **[Open: ID]**: an open question; see the file in [`questions/`](questions/README.md).
- **[Stretch]**: only if time allows.

_Last reviewed: 2026-11-07._

## TL;DR

The thesis studies answering **multimodal questions (an image plus a natural-language
question) over Wikidata by generating SPARQL with an agentic, ReAct-style LLM**. The
question refers to the entity in the image without naming it ("In which year was this
phone's manufacturer founded?"). The agent must first identify the entity, e.g. by
searching a vector index of entity images, and then write and execute the query.
Because no suitable evaluation data seems to exist [Open: [LIT-01](questions/LIT-01-existing-image-sparql-benchmarks.md)], the first part of
the thesis builds an evaluation dataset of (image, question, gold SPARQL) items plus a
shared image index with distractors. The second part builds and evaluates an agent on
it.

## Status and timeline

| Milestone | Date | Status |
| --- | --- | --- |
| Start | 2026-11-02 | [Decided] |
| Project plan hand-in | 2026-12-02 | [Tentative], [D-015](decisions.md#d-015) |
| Agent prototype on the POC examples (about one week) | 2026-12-07 to 2026-12-18 | [Tentative], [D-015](decisions.md#d-015) |
| Dataset frozen | 2027-01-22 | [Tentative] personal deadline, [D-015](decisions.md#d-015) |
| Results frozen | 2027-03-16 | [Tentative], [D-015](decisions.md#d-015) |
| Full draft to supervisor | 2027-03-22 | [Tentative], [D-015](decisions.md#d-015) |
| Hand-in | 2027-04-02 | [Decided] |

- Current phase: preparation. Research for the dataset is starting.
- Capacity: the user works a part-time job 3 days per week (can be reduced to 2);
  reduced pace 2026-12-23 to 2027-01-01; the final buffer includes Easter
  (2027-03-25 to 2027-03-29). If the schedule slips, the stretch goal is dropped first.
  Full schedule: `plan/gantt.tex`.
- Title [Decided, [D-018](decisions.md#d-018)]:
  - English: Multimodal Knowledge Graph Question Answering using an Agentic/ReAct Framework
  - Danish: Besvarelse af spørgsmål over multimodale vidensgrafer ved hjælp af en agentbaseret/ReAct-tilgang
- Next steps: `mise run questions:next`, or the *Ready now* table in
  [`questions/README.md`](questions/README.md).

## Research focus

- Framing: **agentic text-to-SPARQL extended to images** [Decided, [D-001](decisions.md#d-001)]. The dataset
  is built first because evaluation data is needed [Decided, [D-002](decisions.md#d-002)].
- Research questions and hypotheses: a draft (RQ1 agent, RQ2 grounding, RQ3
  difficulty, with H1–H3) is in the project plan, awaiting supervisor feedback
  [Tentative; Open: [FR-01](questions/FR-01-research-questions.md)]. The dataset is a contribution, not a research
  question [Tentative, [D-017](decisions.md#d-017)].
- Positioning against the closest work (M³-VQA, ReasonVQA, KVQA, InfoSeek, ...):
  [Open: [LIT-01](questions/LIT-01-existing-image-sparql-benchmarks.md)]. See [`related-work.md`](related-work.md).

## Scope

In scope:

- Wikidata as the only knowledge graph [Decided, [D-003](decisions.md#d-003)].
- An evaluation dataset with gold SPARQL and an image index [Decided, [D-002](decisions.md#d-002), [D-006](decisions.md#d-006)].
- An agent with SPARQL, exploration and image-search tools, evaluated on the dataset
  [Tentative].

Out of scope:

- Tools that work across knowledge graphs, i.e. KG-agnostic tooling as in GRASP or
  KGVoyager [Decided, [D-003](decisions.md#d-003)]. Generalisation is future work.
- Training or fine-tuning models; there is no train split [Decided, [D-008](decisions.md#d-008)].
- Paid model APIs [Decided, [D-010](decisions.md#d-010)].

Stretch goals:

- Questions with several images [Stretch, [D-009](decisions.md#d-009), [DS-06](questions/DS-06-multi-image-questions.md)].

## Task definition

- **Input:** a question in natural language plus an image (multiple images:
  [Stretch]).
- **Output:** a SPARQL query over Wikidata. Its result is the answer.
- The question never names the depicted entity [Decided, [D-004](decisions.md#d-004)].
- The image mostly shows one entity, which is the subject of the question
  [Tentative; Open: [DS-05](questions/DS-05-image-role.md)]. Images of related entities instead of the subject:
  [Open: [DS-07](questions/DS-07-related-entity-images.md)]. More complex images with other things in them
  (e.g. "the object the person holds in their right hand") are an idea from the supervisor
  meeting, not a decision; see [DS-05](questions/DS-05-image-role.md) and [DS-13](questions/DS-13-difficulty-levels.md).
- **Gold:** each item has a gold SPARQL query that hard-codes the depicted entity
  (e.g. `BIND(wd:Q219691 AS ?product)`) [Tentative], and a gold result [Open: [DS-08](questions/DS-08-gold-answers.md)].
- **Evaluation:** execution-based. The results of the predicted and gold queries are
  compared [Decided, [D-007](decisions.md#d-007)]. Details: [Open: [DS-08](questions/DS-08-gold-answers.md), [EV-01](questions/EV-01-metrics.md)].

Example from the proof of concept
([`examples/nokia`](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples/nokia)):
Nokia 3310 photo + "In which year was this phone's manufacturer founded?". The path is
`manufacturer (P176) → inception (P571)`.

## Dataset

- Built first, before the agent [Decided, [D-002](decisions.md#d-002)].
- Knowledge graph: Wikidata [Decided, [D-003](decisions.md#d-003)].
  - Which domains or classes ("well connected"): [Open: [DS-02](questions/DS-02-wikidata-subset.md)]. The main criterion is
    available hop paths; image coverage (P18) is secondary [Tentative].
  - Endpoint and snapshot (WDQS, QLever, dump): [Open: [DS-04](questions/DS-04-endpoint-snapshot.md)].
  - Maximum hop depth: [Open: [DS-03](questions/DS-03-hop-depth.md)].
- Question types:
  - Initial ideas: single-hop ("first order"), multi-hop, comparison, yes/no, list,
    count [Tentative].
  - Difficulty: the dataset should span easy, medium and hard questions, avoiding
    results near 100% or 0% [Tentative, supervisor feedback 2026-11-04]. Definition and
    measurement: [Open: [DS-13](questions/DS-13-difficulty-levels.md)].
  - Labels per question (hops, type, others) to know what each question tests:
    [Open: [DS-14](questions/DS-14-question-labels.md)].
  - To be formalised from the literature: [Open: [LIT-02](questions/LIT-02-question-type-taxonomy.md), [DS-01](questions/DS-01-question-types.md)].
- Construction:
  - LLM-assisted, manually curated: any available LLM suggests question ideas from
    prompts that state the scope (question types, difficulty); ideas become items
    only if they meet the acceptance criteria; prompts and models used are logged
    [Decided, [D-016](decisions.md#d-016)]. Criteria and procedure: [Tentative; Open: [DS-09](questions/DS-09-generation-pipeline.md)].
  - Size: depends on progress [Open: [DS-10](questions/DS-10-dataset-size.md)].
- Query images:
  - Wikimedia Commons photos of the same entity, different from the image in the
    index; Commons licences are followed and attributions generated [Decided, [D-005](decisions.md#d-005)].
  - Selection and leakage rules: [Open: [DS-12](questions/DS-12-query-images-and-leakage.md)].
- Splits: dev + test, no train [Decided, [D-008](decisions.md#d-008)]. Proportions: [Open: [DS-11](questions/DS-11-split-proportions.md)].
- Release: a public repository (no Hugging Face release planned) [Decided, [D-011](decisions.md#d-011)].

## Image index

- Wikidata has no vector index of images, so the thesis builds one [Decided, [D-006](decisions.md#d-006)].
- One shared index for the whole dataset, containing images of the gold entities plus
  distractor images [Decided, [D-006](decisions.md#d-006)].
- Distractors:
  - Initial idea: entities of the same or a closely related category [Tentative].
  - Strategy: [Open: [IX-01](questions/IX-01-distractor-strategy.md)]. Amount: [Open: [IX-02](questions/IX-02-distractor-count.md)].
- Embedding model: CLIP ViT-B/32 as in the POC [Tentative]. Comparing others is a
  nice-to-have [Open: [IX-03](questions/IX-03-embedding-models.md)].
- Payload per entity: leaning towards the QID only [Tentative; Open: [IX-04](questions/IX-04-index-payload.md)].

## Agent

- A ReAct-style loop with tools [Decided, [D-001](decisions.md#d-001)].
  - Expected tools: SPARQL execution, entity and property search, schema exploration,
    image-index search [Tentative].
  - Exact tool set: [Open: [AG-02](questions/AG-02-tool-set.md)]. Inspiration: SPINACH, GRASP, KGVoyager.
    Leaning: SPINACH's Wikidata tools plus the image-index search as one more tool in the
    same loop, and a high-level zero-shot prompt like SPINACH's [Tentative].
- The tools are specific to Wikidata [Decided, [D-003](decisions.md#d-003)].
- Own implementation vs. building on GRASP: [Open: [AG-01](questions/AG-01-own-agent-vs-grasp.md)]. Leaning towards an own
  implementation, to learn more.
- Framework or loop implementation: [Open: [AG-03](questions/AG-03-agent-framework.md)].
- Model: served by DTU CampusAI (OpenAI-compatible API, DTU VPN only) [Tentative, [D-019](decisions.md#d-019)].
  Available: Qwen3.8-27B (`chat`, `chat:think`, 224K context, tools), Gemma 4 E4B
  (`vision`, image input), BGE-M3 (`embed`), BGE reranker v2-m3 (`rerank`). Contact for
  CampusAI questions (throttling etc.): Benjamin Jakobsen (bstja@dtu.dk). Which model
  runs the agent and how images are handled: [Open: [AG-04](questions/AG-04-gemma-hpc.md)].
- Planned configurations: oracle (entity named in the text), vision only, index only,
  and both [Tentative; Open: [AG-05](questions/AG-05-experiment-configurations.md)].

## Evaluation

- Execution-based [Decided, [D-007](decisions.md#d-007)]. Metrics from the literature, e.g. SPINACH's
  row-major F1 as used by GRASP and KGVoyager [Open: [LIT-03](questions/LIT-03-kgqa-metrics.md), [EV-01](questions/EV-01-metrics.md)].
- Also of interest: image-grounding accuracy, cost, iterations, tool usage
  [Tentative; Open: [EV-01](questions/EV-01-metrics.md)].
- Baselines: [Open: [EV-02](questions/EV-02-baselines.md)]. Ablations: [Open: [EV-03](questions/EV-03-ablations.md)].

## Related work

See [`related-work.md`](related-work.md): full paper names, links, relevance and what
still needs checking. Visual knowledge graphs (scene graphs) were suggested by the
supervisor as inspiration for visual papers [Open: [LIT-05](questions/LIT-05-visual-knowledge-graphs.md)].

## Artifacts

| Artifact | Location | Notes |
| --- | --- | --- |
| Thesis (LaTeX) | this repo, `thesis/` | DTU template |
| Project plan | this repo, `plan/` | draft v1 ([PR #1](https://github.com/andrezz-b/thesis-paper/pull/1)); title and metadata are placeholders |
| Published PDFs | https://andrezz-b.github.io/thesis-paper/ | GitHub Pages |
| Dataset proof of concept | [andrezz-b/thesis-dataset-poc](https://github.com/andrezz-b/thesis-dataset-poc) (local checkout: `../dataset-poc`) | JavaScript (Node 24), Qdrant, CLIP ViT-B/32; 4 hand-made [examples](https://github.com/andrezz-b/thesis-dataset-poc/tree/main/examples) (egg chair, Game Boy, Nokia 3310, ThinkPad), 26 indexed entities each |
| Dataset repository | not created yet | new repo based on the POC [Decided, [D-012](decisions.md#d-012)]; open: [RP-01](questions/RP-01-image-storage.md) to [RP-06](questions/RP-06-dataset-versioning.md) |
| Agent code | not created yet | language and base: [Open: [RP-02](questions/RP-02-languages.md), [AG-01](questions/AG-01-own-agent-vs-grasp.md)] |

## Glossary

- **Depicted entity / gold entity:** the Wikidata item shown in the query image that
  the question is about.
- **Query image:** the image given to the system together with the question.
- **Index image:** an image stored in the vector index; for a gold entity it is a
  different photo than the query image.
- **Distractor:** an entity whose image is in the index but which is not the answer
  to the image grounding. A **hard negative** is a visually similar distractor.
- **Gold query / gold result:** the reference SPARQL query and its result at a fixed
  snapshot date.
- **Hop:** one edge (property) followed in the graph from the depicted entity towards
  the answer.
- **Oracle setting:** the entity is named in the text, so no image grounding is
  needed; an upper bound.
- **QID / PID:** Wikidata item and property identifiers (e.g. Q219691, P176).
  **P18:** the "image" property.
- **KGQA:** knowledge graph question answering. **ReAct:** an agent loop that
  interleaves reasoning and tool calls (think, act, observe).
- **POC:** the dataset proof of concept,
  [andrezz-b/thesis-dataset-poc](https://github.com/andrezz-b/thesis-dataset-poc)
  (local checkout: `../dataset-poc`).

## Open questions and decisions

- All open questions, their dependencies and what is ready to work on:
  [`questions/README.md`](questions/README.md), generated by `mise run questions`.
- Decision log (append-only): [`decisions.md`](decisions.md).
