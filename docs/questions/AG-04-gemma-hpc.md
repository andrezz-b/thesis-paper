---
id: AG-04
title: Which CampusAI models and setup are used, and what do they support?
area: agent
status: researching
phase: dataset
priority: high
depends_on: []
informs: [AG-03, AG-05]
---

## Question

Which of the models on DTU's CampusAI are used for the agent, and what do they
support? Can the setup be changed for the experiments?

## Why it matters

It is the only planned model (no API credits, [D-010](../decisions.md#d-010)). Its capabilities decide which
agent configurations are possible ([AG-05](AG-05-experiment-configurations.md)). It is not used to build the dataset
([D-016](../decisions.md#d-016)), so question generation no longer depends on it.

## Notes

To check with the people running it:

- exact model and size (originally assumed Gemma 4, about 29B; see catalog below);
- image input support;
- tool or function calling;
- context length;
- API type (OpenAI-compatible?), rate limits and throughput, availability;
- whether things can be swapped for tests (e.g. vision on or off, another model).
- 2026-11-03 (user, CampusAI catalog; weights name the checkpoint behind an alias, the
  alias stays stable when the model changes): 6 models, 7 names. OpenAI-compatible API
  with a key from the console; browser chat also available. Only reachable through the
  DTU VPN (`/opt/cisco/secureclient/bin/vpn -s connect vpn.dtu.dk`).

  | Name | Model / weights | Context | Tools |
  | --- | --- | --- | --- |
  | `auto` | picks chat, chat:think or vision per request | 96K | yes |
  | `vision` | Gemma 4 E4B, `google/gemma-4-E4B-it`, image input | 96K | yes |
  | `chat` | Qwen3.8-27B, `RedHatAI/Qwen3.8-27B-INT4`, reasoning off, lowest latency | 224K | yes |
  | `chat:think` | Qwen3.8-27B, flagship, reasoning on (weights not listed) | 224K | yes |
  | `embed` | BGE-M3, `BAAI/bge-m3`, 1024-d multilingual dense | 8K | no |
  | `rerank` | BGE reranker v2-m3, `BAAI/bge-reranker-v2-m3`, cross-encoder | 8K | no |
  | `decision` | typed decisions (choice, score, ...) with probabilities, `vllm-sr/d3-edge`; `POST /v1/systemone` | – | – |

  Consequences: [D-010](../decisions.md#d-010)'s "Gemma ~29B" does not match; Gemma 4 E4B is only the vision
  model. Qwen3.8-27B (text) has tool calling and a large context, so it is the
  obvious agent candidate (assistant suggestion, not decided). Image input appears to
  be only on `vision` (E4B); unclear whether Qwen3.8 chat takes images. `embed` and
  `rerank` may be usable for entity/property search tools ([AG-02](AG-02-tool-set.md)). Still unknown:
  rate limits, throughput, whether the model behind an alias is pinned for the
  experiments (reproducibility), whether the `decision` endpoint is relevant. See [D-019](../decisions.md#d-019).
- 2026-10-30: Planned to be tested in practice with a small agent prototype on the
  POC examples, 2026-12-07 to 2026-12-18 (about one week of effort, [D-015](../decisions.md#d-015)).
- 2026-11-04 (supervisor meeting): contact for CampusAI questions: Benjamin Jakobsen
  (bstja@dtu.dk). To ask: which models and checkpoints are served and whether they
  are pinned, throttling and rate limits, throughput, availability.
- 2026-11-05 (user): Benjamin Jakobsen has not been contacted yet.

## Resolution

_Not resolved yet._
