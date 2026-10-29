---
id: AG-04
title: What exactly does the Gemma setup on the DTU HPC support?
area: agent
status: open
phase: dataset
priority: high
depends_on: []
informs: [AG-03, AG-05, DS-09]
---

## Question

Which Gemma model is available on the university cluster, and what does it support?
Can the setup be changed for the experiments?

## Why it matters

It is the only planned model (no API credits, [D-010](../decisions.md#d-010)). Its capabilities decide which
agent configurations are possible ([AG-05](AG-05-experiment-configurations.md)) and whether it can generate questions
([DS-09](DS-09-generation-pipeline.md)).

## Notes

To check with the people running it:

- exact model and size (the user thinks it is Gemma 4, around 29B);
- image input support;
- tool or function calling;
- context length;
- API type (OpenAI-compatible?), rate limits and throughput, availability;
- whether things can be swapped for tests (e.g. vision on or off, another model).

## Resolution

_Not resolved yet._
