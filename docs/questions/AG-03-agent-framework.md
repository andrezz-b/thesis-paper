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

## Resolution

_Not resolved yet._
