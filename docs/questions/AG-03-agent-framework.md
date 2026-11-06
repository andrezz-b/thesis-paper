---
id: AG-03
title: Which agent framework or loop implementation is used?
area: agent
status: open
phase: agent
priority: low
depends_on: [AG-01]
informs: []
---

## Question

Is the ReAct loop custom-written, or does it use a framework (e.g. LangGraph,
smolagents)?

## Why it matters

Affects implementation effort and how traces and metrics (iterations, tool usage) are
logged.

## Notes

- The user has no preference yet.
- Depends on how the model is served on CampusAI ([AG-04](AG-04-gemma-hpc.md)), e.g. whether the OpenAI-compatible
  API supports tool calling (CampusAI lists tools as supported).
- 2026-11-06: SPINACH uses a zero-shot, high-level policy prompt ("start with very simple queries", "confirm all assumptions") and found that low-level control of the action choice did not help (§4.2, Prompt 12); it also resets the state on repeated actions or an early `stop`, with a budget of 15 actions plus 15 for rollbacks. Leaning (user): adopt a high-level prompt. Whether it works with a weaker open model is untested ([AG-04](AG-04-gemma-hpc.md)). Source: [SPINACH note](../literature/liu2024spinach.md).

## Resolution

_Not resolved yet._
