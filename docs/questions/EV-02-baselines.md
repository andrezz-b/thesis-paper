---
id: EV-02
title: Which baselines are compared against?
area: evaluation
status: researching
phase: agent
priority: medium
depends_on: [AG-05]
informs: []
---

## Question

Which external or simple baselines are run besides the agent configurations?

## Why it matters

Shows whether the agentic approach is worth it.

## Notes

- Kept open on purpose.
- Candidates:
  - the configurations from [AG-05](AG-05-experiment-configurations.md);
  - caption the image, then run text-to-SPARQL;
  - GRASP extended with an image tool ([AG-01](AG-01-own-agent-vs-grasp.md));
  - a vision-language model answering directly without the KG (InfoSeek-style "no
    KB" setting).
- 2026-11-06: GRASP (text-only, code open) is a candidate baseline, with an image tool added if needed ([AG-01](AG-01-own-agent-vs-grasp.md)). Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-07: ReasonVQA gives a "direct answer, image + question, no KB" baseline over 13 vision-language models, e.g. GPT-4o 62.8 open-ended and 76.6 multiple choice on ReasonVQA-U (Table 2); InfoSeek-style setting like the last candidate above. Source: [ReasonVQA note](../literature/tran2025reasonvqa.md).
- 2026-11-15: GRISP (fine-tuned 7B, needs question-query training pairs, §3 and Limitations) is not a usable baseline: the dataset has no train split ([D-008](../decisions.md#d-008)). Its Table 3 shows GRASP with GPT-4.1 beating it on QALD-7, QALD-10 and SPINACH, which supports GRASP as the external baseline. Source: [GRISP note](../literature/walter2026grisp.md).

## Resolution

_Not resolved yet._
