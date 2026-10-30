---
id: FR-01
title: What are the research questions and hypotheses?
area: framing
status: researching
phase: dataset
priority: medium
depends_on: [LIT-01]
informs: [FR-02, DS-01, EV-02, EV-03]
---

## Question

What exactly does the thesis ask or claim, and which hypotheses are tested?

## Why it matters

Decides which question types, configurations and ablations are worth the effort and
what the evaluation has to show. Also needed for the project plan and the title.

## Notes

- The framing is decided: agentic text-to-SPARQL extended to images ([D-001](../decisions.md#d-001)).
- The user expects some hypotheses but none are defined yet.
- Candidate directions (not agreed, only suggestions so far):
  - how accuracy changes with the number and similarity of distractors ([IX-02](IX-02-distractor-count.md));
  - how accuracy changes with hop count and question type ([DS-01](DS-01-question-types.md), [DS-03](DS-03-hop-depth.md));
  - how much an image-retrieval tool adds compared to a vision-capable model that
    recognises the entity itself ([AG-05](AG-05-experiment-configurations.md)).
- The contribution statement depends on what the closest related work already covers
  ([LIT-01](LIT-01-existing-image-sparql-benchmarks.md)).
- 2026-10-30 (superseded by the next entry, [D-017](../decisions.md#d-017)): Draft research questions and
  hypotheses for the first project plan
  (`plan/main.tex`), to be refined after the literature review and supervisor
  feedback. The plan asks the supervisor whether the number and scope are right and
  whether the dataset (RQ1) counts as a research question and contribution on its own.
  - RQ1 (dataset): How can an evaluation dataset of items consisting of an image, a
    question and a gold SPARQL query be built semi-automatically from Wikidata and
    Wikimedia Commons, such that the depicted entity is only reachable through the
    image and the gold answers are verifiable?
    - H1: Generating questions from sampled Wikidata paths with an LLM, followed by
      human review, yields valid items at a manageable review cost (an
      acceptance-rate target is set after the pilot in December). Most rejected items
      are ambiguous or reveal the entity in the question text.
  - RQ2 (agent): How accurately can a ReAct-style agent based on an open-weight LLM
    answer such questions by generating SPARQL, and how large is the gap to an oracle
    setting in which the entity is named in the text?
    - H2: The agent performs clearly below the oracle setting, and most of the gap
      comes from failing to identify the entity in the image rather than from writing
      wrong SPARQL, measured by comparing grounding accuracy with answer accuracy
      given correct grounding.
  - RQ3 (grounding): How do the model's own vision, retrieval from an image index,
    and the combination of both compare in grounding accuracy and in final answer
    quality?
    - H3: The image index works better than the model's own vision for less
      well-known or fine-grained entities, while vision works better for well-known
      ones (popularity measured e.g. by the number of Wikipedia sitelinks). Combining
      both works best.
  - RQ4 (difficulty): How does performance change with question complexity (number
    of hops, question type) and with the number and visual similarity of distractors
    in the image index?
    - H4: Accuracy drops as the number of hops grows and as more visually similar
      distractors are added. Comparison, count and list questions are harder than
      single-hop lookups.
  - Review remarks (2026-10-30, not yet acted on): RQ4 bundles three factors and
    depends on open questions ([DS-03](DS-03-hop-depth.md), [IX-01](IX-01-distractor-strategy.md), [IX-02](IX-02-distractor-count.md)); "visual similarity" could become
    "if time allows". H2 and H3 need precise definitions once [EV-01](EV-01-metrics.md) is settled.
- 2026-10-30: Current draft, in the project plan. The dataset is a contribution,
  not a research question ([D-017](../decisions.md#d-017), tentative), because it is curated manually
  ([D-016](../decisions.md#d-016)). The agent questions are renumbered:
  - RQ1 (agent): How accurately can a ReAct-style agent based on an open-weight LLM
    answer image-based questions over Wikidata by generating SPARQL, and how large
    is the gap to an oracle setting in which the entity is named in the text?
    - H1: as the previous H2.
  - RQ2 (grounding): as the previous RQ3. H2: as the previous H3.
  - RQ3 (difficulty): as the previous RQ4. H3: as the previous H4.
  - The review remarks above still apply to the new RQ3 (old RQ4).
  - The supervisor box in the plan now asks whether presenting the dataset as a
    contribution instead of a research question is fine.

## Resolution

_Not resolved yet._
