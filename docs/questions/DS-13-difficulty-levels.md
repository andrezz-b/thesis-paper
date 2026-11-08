---
id: DS-13
title: How is question difficulty defined and measured (easy, medium, hard)?
area: dataset
status: researching
phase: dataset
priority: high
depends_on: []
informs: [DS-01, DS-03, DS-09, DS-14, FR-01]
---

## Question

The dataset should contain easy, medium and hard questions. What makes a question
easy or hard, how is difficulty measured (a priori from properties of the question,
a posteriori from agent results, or both), and how is the spread kept useful?

## Why it matters

Supervisor feedback: the questions should cover a range of difficulty, and the
results should not end up in 100% or 0% correct territory, where nothing can be
learned. Difficulty also underlies RQ3 (difficulty) in [FR-01](FR-01-research-questions.md) and the per-level
reporting in [EV-01](EV-01-metrics.md).

## Notes

- 2026-11-04 (supervisor meeting, user's notes): range of questions, easy / medium /
  hard. Open: what is the difficulty and how do we measure it? Do not end up in 100%
  or 0% correct territory.
- Candidate difficulty axes (assistant suggestions, not decided):
  - number of hops ([DS-03](DS-03-hop-depth.md)) and question type ([DS-01](DS-01-question-types.md));
  - grounding difficulty: number and similarity of distractors ([IX-01](IX-01-distractor-strategy.md), [IX-02](IX-02-distractor-count.md));
  - image complexity: the image contains other things besides the subject, e.g.
    "What is the object that the person is holding in their right hand?" (idea from
    the supervisor meeting, see [DS-05](DS-05-image-role.md); not a decision);
  - query complexity (aggregation, filters, number of triple patterns).
- A posteriori calibration: pilot runs with the agent prototype (2026-12-07 to
  2026-12-18, [D-015](../decisions.md#d-015)) could show whether the spread is useful, before the dataset
  is frozen (2027-01-22). Suggestion, not decided.
- If results approach 100% accuracy, harder items or axes are needed; this is a
  design consideration for the dataset, not a change of scope.
- 2026-11-05 (user): not sure yet how to measure difficulty; first assumption is to
  define it from the properties of the question only (leaning, not decided).
  If results approach 100%, the user would consult the supervisor, but expects that
  something would be done about it (e.g. harder items).
- 2026-11-07: M3-VQA defines difficulty by hop count and entity count (paper §3, Table 2) and sees accuracy fall with both under the gold-evidence oracle (§5.5). Reusing some of its questions or images as a difficulty axis is an option, not committed: it would need filtering and rewriting as Wikidata SPARQL, and not all items would work. Source: [M3-VQA note](../literature/ma2026m3.md).
- 2026-11-07: ReasonVQA supports hop count as a difficulty axis: accuracy is clearly lower on 3-hop, while 1-hop is only slightly better than 2-hop and sometimes worse, which the authors attribute to the longer 2-hop questions giving more context (§4.4, Fig. 6). Questions that use scene-graph information score lower than the others (§4.4). Answer-distribution balancing (top ten answers per property) made the benchmark slightly harder (§3.3.1, Table 2). Fixed multiple-choice distractors are random draws (§3.2.2), so a multiple-choice setting is a weak difficulty control. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-08: KGVoyager measures the complexity of gold queries by the number of triple patterns and the number of distinct special constructs (aggregation, FILTER, OPTIONAL, UNION, MINUS, EXISTS, subqueries, property paths) (App. C, Fig. 6). Its advantage over GRASP shrinks for complex queries: pooled F1 58.8 vs. 57.4 with seven or more triple patterns, against 66.7 to 70.8 vs. 62.9 to 67.4 with three to six. A possible difficulty proxy next to hop count. Source: [KGVoyager note](../literature/wisam2026kgvoyager.md).

## Resolution

_Not resolved yet._
