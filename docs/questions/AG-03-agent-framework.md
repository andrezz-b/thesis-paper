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
- Depends on how the model is served on the HPC ([AG-04](AG-04-gemma-hpc.md)), e.g. whether there is an
  OpenAI-compatible API.

## Resolution

_Not resolved yet._
