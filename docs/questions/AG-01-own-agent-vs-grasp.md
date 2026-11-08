---
id: AG-01
title: Build an own agent or build on top of GRASP?
area: agent
status: researching
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
- 2026-11-06: GRASP (Walter and Bast, ISWC 2025) is a single-context ReAct-style loop with a KG-independent function set (§3.1, §3.2); code and indices are open (github.com/ad-freiburg/grasp). Its generality (a `kg` argument on every function, federated queries) is out of scope for the thesis ([D-003](../decisions.md#d-003)); no image input. Leaning unchanged: own agent, GRASP as a possible baseline. Source: [GRASP note](../literature/walter2025grasp.md).
- 2026-11-08: Leaning (user): build an own implementation and use the GRASP and KGVoyager code and tool specifications (KGVoyager App. G) as inspiration, because building it is the part the user enjoys. KGVoyager's code is only an anonymous review link so far. Its gain over GRASP (+3.7 F1 on average, Table 3) is not what decides this. Source: [KGVoyager note](../literature/wisam2026kgvoyager.md).

## Resolution

_Not resolved yet._
