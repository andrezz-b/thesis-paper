---
id: AG-05
title: Which agent configurations are evaluated?
area: agent
status: open
phase: agent
priority: medium
depends_on: [AG-04]
informs: [EV-02, EV-03]
---

## Question

Which combinations of "the model sees the image" and "the agent has the image-index
tool" are run?

## Why it matters

Separates how much comes from the model recognising the entity itself from how much
comes from retrieval. Serves as both the baselines and the ablation set, using one
model.

## Notes

Proposed set (the user wants to test without the index, without vision, and with
both):

| Config | Model sees image? | Index tool? | Measures |
| --- | --- | --- | --- |
| Oracle | n/a (entity named in text) | no | upper bound: SPARQL ability alone |
| Vision-only | yes | no | recognition from the model's own knowledge |
| Index-only | no | yes | retrieval-driven grounding |
| Full | yes | yes | combined |

Feasibility depends on [AG-04](AG-04-gemma-hpc.md).

## Resolution

_Not resolved yet._
