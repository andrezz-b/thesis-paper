---
id: EV-02
title: Which baselines are compared against?
area: evaluation
status: open
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

## Resolution

_Not resolved yet._
