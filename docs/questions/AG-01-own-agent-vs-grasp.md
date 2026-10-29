---
id: AG-01
title: Build an own agent or build on top of GRASP?
area: agent
status: open
phase: agent
priority: medium
depends_on: []
informs: [AG-02, AG-03, RP-02, EV-02]
---

## Question

Should the agent be written from scratch or built by extending an existing system
such as GRASP?

## Why it matters

Decides how much engineering is needed and which baselines come for free.

## Notes

- Leaning: build an own agent, to learn more.
- GRASP: Python, Apache-2.0, supports Wikidata, relies on QLever and a prebuilt entity
  index (https://github.com/ad-freiburg/grasp).
- Possible middle ground: own agent, with GRASP (plus an image tool) as a baseline
  ([EV-02](EV-02-baselines.md)).
- Scope is Wikidata only ([D-003](../decisions.md#d-003)); KG-agnostic tooling is out of scope.

## Resolution

_Not resolved yet._
