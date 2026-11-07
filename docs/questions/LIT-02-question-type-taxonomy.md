---
id: LIT-02
title: What question-type taxonomy and terminology does the literature use?
area: literature
status: researching
phase: dataset
priority: high
depends_on: []
informs: []
---

## Question

How do existing KGQA datasets classify questions (semantic types, structural query
shapes, complexity), and which terminology should the thesis adopt?

## Why it matters

The question types of the dataset ([DS-01](DS-01-question-types.md)) should be defined from established
terminology rather than ad hoc, so results are comparable and the thesis can cite it.

## Notes

- Initial ad-hoc list from the user: first order (single-hop), multi-hop, comparison
  (e.g. which company came first), yes/no, list, count.
- Sources to go through (links in [`../related-work.md`](../related-work.md)):
  - Mintaka: complexity types such as count, comparative, superlative, ordinal,
    multi-hop, intersection, difference, yes/no (verify exact list).
  - LC-QuAD 2.0: template classes.
  - KQA Pro: compositional programs.
  - ComplexWebQuestions: composition, conjunction, comparative, superlative.
  - GrailQA: three levels of generalisation (i.i.d., compositional, zero-shot).
  - Bonifati et al.: structural query shapes (single edge, chain, star, tree, flower).
  - SPINACH and WDQL: statistics of SPARQL features (clauses, projections, filters,
    aggregates, optional, union, ...).
- There are probably several independent axes: semantic type, structural shape,
  number of hops, and a visual axis (role of the image, [DS-05](DS-05-image-role.md)).
- 2026-11-07: M3-VQA splits multi-hop questions into parallel (several entities reasoned about independently, then combined) and sequential (the output of one hop feeds the next) (paper §3). Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-07: KVQA groups questions into ten non-exclusive challenge categories: spatial, 1-hop, multi-hop, Boolean, intersection, subtraction, comparison, counting, multi-entity, multi-relation (§Analysis of KVQA, Fig. 2, Table 5). Source: [KVQA note](../literature/shah2019kvqa.md).
- 2026-11-07: ReasonVQA's types follow the Wikidata property used (who designed, how tall, which country, ...) with a template per property, and it has hop count (1 to 3) as the only structural dimension; no comparison, count or boolean types (§3.2.1, App. 1.2). 20 predefined knowledge domains are assigned by property (§3.2.1, App. 2.2). Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).

## Resolution

_Not resolved yet._
