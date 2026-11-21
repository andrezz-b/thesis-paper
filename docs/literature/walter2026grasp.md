---
key: walter2026grasp
title: "GRASP and GRISP for Question Answering over Wikidata"
authors: ["Sebastian Walter", "Hannah Bast"]
year: 2026
venue: "Proceedings of the First Wiki-Based Knowledge Graph Question Answering Challenge (WikiKGQA 2026), co-located with ISWC 2026, CEUR-WS Vol-4284"
url: "https://ceur-ws.org/Vol-4284/paper5.pdf"
pdf: "https://ceur-ws.org/Vol-4284/paper5.pdf"
arxiv: ""
doi: ""
s2_id: "f5281a4defb47a4f0bc322b03a9fd3940c6ebcfc"
code: "https://github.com/ad-freiburg/grasp"
data: "https://doi.org/10.5281/zenodo.19474009"
status: reviewed
relevance: medium
read_depth: full
informs: [AG-01, AG-02, AG-04, DS-04, LIT-03, EV-01, EV-02, FR-01, LIT-01]
themes: [agentic-sparql, kgqa, metrics, wikidata]
added: 2026-11-20
reviewed: 2026-11-21
candidates:
  - id: "https://ceur-ws.org/Vol-4284/intro1.pdf"
    title: "WikiKGQA 2026: The First Wiki-Based Knowledge Graph Question Answering Challenge"
    via: recs
    priority: medium
    scout_priority: high
    why: "Challenge overview (same CEUR volume, not cited by the seed): task, tracks, data and the Codabench QALD-F1 scoring; may settle the 'protocols coincide' doubt (LIT-03, DS-04). (title only)"
  - id: "https://ceur-ws.org/Vol-4284/paper4.pdf"
    title: "Can Skill-Driven LLM Agents Solve Text2SPARQL through Autonomous Exploration and Iterative Refinement?"
    via: recs
    priority: high
    why: "Agent with autonomous exploration and iterative refinement on the same Wikidata challenge (same CEUR volume); ideas for exploration notes and tools (AG-01, AG-02). (title only)"
bibtex: |
  @inproceedings{walter2026grasp,
    title = {{GRASP} and {GRISP} for Question Answering over {Wikidata}},
    author = {Walter, Sebastian and Bast, Hannah},
    booktitle = {Proceedings of the First Wiki-Based Knowledge Graph Question Answering Challenge (WikiKGQA 2026), co-located with the 25th International Semantic Web Conference (ISWC 2026)},
    editor = {Schmidt, David Maria and Arzoo, Shakeeb and Banerjee, Debayan and Moya Loustaunau, Alberto and Usbeck, Ricardo and Cimiano, Philipp and Hogan, Aidan},
    series = {CEUR Workshop Proceedings},
    volume = {4284},
    publisher = {CEUR-WS.org},
    address = {Bari, Italy},
    year = {2026},
    url = {https://ceur-ws.org/Vol-4284/paper5.pdf}
  }
---

# GRASP and GRISP for Question Answering over Wikidata

## TL;DR

Challenge report: the GRASP authors enter GRASP (zero-shot LLM agent) and GRISP (fine-tuned
SLM) in the WikiKGQA 2026 text-to-SPARQL challenge over a fixed Wikidata dump. GRASP with
GPT-5.4 wins both without-mentions tracks (85.0 / 83.0 macro QALD-F1, Table 2) and matches an
off-the-shelf Claude Code agent at a fraction of its cost. For the thesis it is the most
recent GRASP evidence on Wikidata, a precedent for a frozen dump behind a local QLever, and the
source for the QALD-F1 metric.

## Problem and contribution

- Task (§2): question (English or Spanish) → one SPARQL query, answered against the
  Wikidata version fixed by the challenge (hosted endpoint or provided dump, 21 billion
  triples, fn. 1). Four tracks: {English, Spanish} × {without, with mentions}; "with mentions"
  adds entity/property annotations from QAWiki metadata.
- Contribution: description and results of their submissions to the two without-mentions
  tracks, plus standalone Claude Code agents as a reference for an off-the-shelf agentic LLM
  without KGQA tooling (Abstract, §1). No new method; GRASP and GRISP predate the challenge
  (§1).
- Materials: evaluation at grasp.cs.uni-freiburg.de/wiki-kgqa-evaluation, materials at
  ad-publications.cs.uni-freiburg.de/grasp/wiki-kgqa, code at github.com/ad-freiburg/grasp
  (§1).

## Method

- Endpoint (§3): all systems run against their own local QLever loaded with the challenge
  dump, for control over load and resource limits; no QLever-specific extensions are used.
- GRASP (§3.1): ReAct-style loop with a fixed function set (execute SPARQL, list triples
  matching a pattern, search over entities, properties and literals); it ends with a final
  answer function that takes the SPARQL query and a human-readable answer. Search indices are
  built from, and queries executed on, the local QLever.
- GRASP automatic setup from only an endpoint (§3.1, steps 1–5), new compared to the 2025
  paper (assistant reading):
  1. `setup info`: prefixes and a short KG description.
  2. `notes explore` (structural mode): the model explores around seed entities and
     properties and writes notes that are later added to its context.
  3. `setup indices`: the model writes the extraction and display-metadata SPARQL for the
     entity, property and literal indices.
  4. `setup shapes`: an instance pattern and a schema pattern yield a shape index of
     ShEx-like class shapes (properties and value types); top 500 classes, others computed
     on the fly.
  5. `notes explore` (functional mode): notes on how each function behaves.
  - Optional: *self-QA* (model invents and answers questions, taking notes) or *samples*
    (few-shot example index from the train set via `search_example`, plus notes from
    comparing GRASP traces with gold queries on the validation questions).
  - Spanish setup: entity/property indices rebuilt with Spanish labels and aliases,
    functional notes retaken in Spanish (§3.1).
- GRISP (§3.2): skeleton generation + left-to-right placeholder resolution with re-ranking,
  KG-constrained search and backtracking (see the GRISP note). Qwen2.5 7B/14B with LoRA,
  starting from WDQL-pre-trained checkpoints; trained per track or on "all KGQA sources"
  (other language, QALD-7, QALD-10, GRASP trace-derived pairs).
- Claude Code baselines (§3.3): `/auto` mode; single session or orchestrator with one
  sub-agent per question; some runs with `/goal` (a smaller model checks a completion
  condition after each turn). First prompted to explore the endpoint. Best validation run saw
  all validation questions upfront (not gold SPARQL); the test run had train and validation
  samples, matching GRASP's samples setting.
- Backbones (§4): GRASP with GPT-5.4 (and mini), GPT-5.5, Kimi K2.7, Claude Sonnet 4.6; Claude
  Code with Sonnet 4.6 and Opus 4.8; all at medium reasoning effort.
- Post-processing (§4): a Claude Haiku 4.5 agent rewrites every predicted query to project a
  single answer variable (ASK and single-column queries pass through) and checks against the
  endpoint that the result rows do not change.

## Data / benchmark

Not a dataset paper, but it describes the challenge data (§2):

- Gold SPARQL: yes, each sample has a reference query (Fig. 1); derived from QAWiki, a full
  snapshot is on Zenodo (doi:10.5281/zenodo.19474009, fn. 2).
- Entity named in the question: yes; text only, no images.
- KG: Wikidata, fixed version (provided dump of 21B triples, or the challenge endpoint)
  (§2, fn. 1).
- Multi-hop / question types: not stated in this paper.
- Image index / distractors: none.
- Agentic systems evaluated: yes (GRASP, Claude Code, and "agentic-text2sparql-skills"
  from another team, Table 2).
- Size and splits: 317 train, 100 validation, 75 test per track; English and Spanish are
  translations sharing the gold query; with- and without-mentions share train and validation
  questions, but their test sets are disjoint (§2). Licence: not stated (the CEUR paper is
  CC BY 4.0).
- Mention annotations (§3): English train has 4.6 mentions per question, 62.5% with nested
  mention strings, only 56.7% of annotated IRIs occur in the gold query; test has 3.0 mentions
  and 5.3% nesting.

## Key results

- Test, macro QALD-F1 (Table 2), English without mentions: GRASP GPT-5.4 with samples 85.0
  (56.3 s/q, 13.7 steps/q, $9); Claude Code Opus 4.8 + Sonnet 4.6 sub-agents with samples 85.0
  (113 s/q, $26 sub-agents + $29 orchestrator); GRASP Kimi K2.7 with samples 81.0; other team
  agentic-text2sparql-skills 81.0; GRASP GPT-5.4 80.0; other team AMA-KBQA 79.0; GRISP 14B
  57.0.
- Test, Spanish (Table 2): GRASP GPT-5.4 with Spanish setup 83.0 (with or without samples);
  Kimi K2.7 79.0; GRISP 56.0. No other team submitted.
- Validation, F1 per GRASP protocol (Table 1), English: GRASP GPT-5.4 86.8, GPT-5.5 86.3,
  Sonnet 4.6 80.7, GPT-5.4 mini 78.1; best GRISP 68.7; Claude Code best 86.6 (questions upfront),
  80.8 without, Sonnet single context 72.0.
- Backbone matters substantially (§4): GPT-5.4 86.8 vs mini 78.1; Kimi K2.7 4 points behind
  GPT-5.4 on both test tracks.
- Notes do not help uniformly (§4): self-QA −2.7 for GPT-5.4 (86.8 → 84.1), ±0 for Sonnet;
  samples +5 on English test (80.0 → 85.0), +0 on Spanish.
- One-time GRASP setup cost about $11 (English) / $10 (Spanish) with GPT-5.4, plus $8
  self-QA and $5 samples (Table 1 caption).
- Test is harder than validation for every run; GPT-5.4 English needs 9.6 steps/q on
  validation vs 12.4–13.7 on test (§4).
- With vs without mentions (§3): best English with-mentions 88.0 vs their 85.0; both teams in
  both English tracks did better with mentions (81.0 → 88.0, 79.0 → 87.0); disjoint test sets,
  so not conclusive.

### QALD-F1 vs. the SPINACH/GRASP F1 (answer to the question in My notes)

The paper only says the official metric is "macro QALD-F1, computed on Codabench following
the definition used by GERBIL QA [6]" (§2). The definition below comes from that reference
(Usbeck et al., *Benchmarking question answering systems*, Semantic Web 10, 2019, §5.2) and
GERBIL's code (`FMeasureCalculator.java`, branch `QuestionAnswering`, `calculateF1QALD`),
not from this paper:

- Per question, P and R on the answer **set** (one column of values):
  - gold empty and system empty: P = R = F1 = 1;
  - gold empty, system non-empty (or no correct answer at all): P = R = F1 = 0;
  - gold non-empty, system empty: **P = 1**, R = 0 (the "QALD" exception: an empty answer
    counts as "I cannot answer", not as wrong).
  - otherwise the standard P, R.
- Aggregation: average P and R over questions (macro P, macro R), then
  **QALD-F1 = 2·P̄·R̄ / (P̄ + R̄)**. GERBIL's plain "Macro F1" instead averages the per-question
  F1. The QALD variant exists for compatibility with older QALD challenges (GitHub issue
  dice-group/gerbil#211).

Differences from the SPINACH row-major F1 used by GRASP, KGVoyager and QAWiki ([LIT-03](../questions/LIT-03-kgqa-metrics.md)):

| | QALD-F1 (GERBIL) | SPINACH / GRASP F1 |
| --- | --- | --- |
| Unit compared | Set of single answer values | Rows of a result table, optimally matched; extra predicted columns not penalised |
| Empty prediction | P = 1, R = 0 | F1 = 0 |
| Aggregation | Harmonic mean of macro P and macro R | Mean of per-question F1 |
| Multi-column results | Not supported; needs a single answer column | Supported |

Consequence (assistant reading): because the harmonic mean is concave, F1 of the averaged P
and R is at least the average of per-question F1, and abstaining raises P̄; so QALD-F1 is
generally ≥ the GRASP F1 on the same predictions, and the two are not directly comparable.
The paper says that after single-column post-processing "the two protocols coincide on the
runs we report" (§2); this holds for column handling, but the aggregation still differs (see
Open doubts).

## Limitations

Authors say:

- The best configurations are still fairly slow (§5).
- Wikidata's prevalence in LLM training data likely washes out differences between methods;
  they ask for challenges on KGs unseen by the systems (§5).
- Partial backbone comparison: models were released at different times, so part of the spread
  reflects model generation (§4).
- Claude Code test costs are estimates for a run spread over several days; validation costs
  not tracked (§4, Table 1 caption).
- With- vs without-mentions cannot be compared directly (disjoint test sets) (§3).

We see (assistant reading):

- Small test set (75 questions per track) and single runs; no variance reported.
- The authors are GRASP's authors; the Claude Code baselines are their own configurations.
- All backbones are paid APIs except Kimi K2.7 and GRISP; no small open model as GRASP
  backbone, so little evidence for a ~27B CampusAI model.
- Notes (samples) are taken on the validation questions themselves, so validation F1 is not
  reported for those configurations (§3.1).
- Text-only; no images.

## Relevance to the thesis

- [AG-01](../questions/AG-01-own-agent-vs-grasp.md): cite. Current GRASP (setup pipeline, notes, shape index, §3.1) is the strongest
  system in the challenge; an off-the-shelf Claude Code agent matches it only at about 2–6×
  the cost ($55 vs $9, or $25 with GRASP's one-time setup; Table 2, §4). Supports GRASP as the reference system; does not change the leaning
  towards an own agent.
- [AG-02](../questions/AG-02-tool-set.md): adopt (ideas only). The user found two ideas most useful: agent-written
  exploration notes added to the context, and a shape index of class shapes (properties with
  value types) as a schema tool (§3.1, steps 2, 4, 5). Smaller ideas: literal search; a final
  answer function returning SPARQL plus a human-readable answer. Not decided.
- [AG-04](../questions/AG-04-gemma-hpc.md): cite. Backbone choice moves F1 by about 9 points (GPT-5.4 86.8 vs mini 78.1, Table 1);
  the open-weight Kimi K2.7 is 4 points behind GPT-5.4 (§4).
- [DS-04](../questions/DS-04-endpoint-snapshot.md): cite (precedent only, no change of leaning). A challenge fixes one Wikidata dump and
  the authors serve it from their own QLever instance to get consistent results and control
  over limits (§2, §3).
- [LIT-03](../questions/LIT-03-kgqa-metrics.md) / [EV-01](../questions/EV-01-metrics.md): cite (note only). Official metric is macro QALD-F1 (GERBIL QA); validation
  uses the GRASP F1 (§2). The definition and comparison are recorded above; the user does not
  plan to report QALD-F1, the primary metric stays the SPINACH/GRASP F1.
- [DS-08](../questions/DS-08-gold-answers.md): not informed. The single-answer-column requirement and the LLM rewrite to one answer
  variable (§4) exist only because of QALD-F1, which the thesis does not plan to use.
- [EV-02](../questions/EV-02-baselines.md): contrast. A generic coding agent (Claude Code) as baseline is an interesting idea, but
  paid APIs are out of scope ([D-010](../decisions.md#d-010)).
- [FR-01](../questions/FR-01-research-questions.md): cite. Wikidata's prevalence in LLM training data as a threat to validity (§5).
- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): cite. WikiKGQA is another text-only Wikidata benchmark (derived from QAWiki); no
  images (§2).

## Citable claims

- GRASP reached the best result of all submissions in both without-mentions tracks of
  WikiKGQA 2026: 85.0 (English) and 83.0 (Spanish) macro QALD-F1 (Abstract, Table 2).
- An off-the-shelf Claude Code agent matched GRASP's best English test score (85.0) at about
  $55 vs $9 for the run ($25 including GRASP's one-time setup) (Table 2, §4).
- GRASP can set itself up on a KG from only a SPARQL endpoint, including model-written
  indices, class shapes and notes (§3.1).
- GRASP's accuracy depends substantially on the backbone LLM (§4, Table 1).
- WikiKGQA 2026 evaluates with macro QALD-F1 as defined by GERBIL QA (§2).
- The authors suspect Wikidata's prevalence in LLM training data reduces the measurable
  differences between methods (§5).
- Mention annotations in the WikiKGQA train set are over-segmented: 4.6 mentions per question,
  only 56.7% of annotated IRIs in the gold query (§3).

## My notes
- What is QALD-F1 and how does it compare to the SPINACH/GRASP metric we mention in the questions

## Open doubts

- §2 says the Codabench QALD-F1 and the GRASP F1 "coincide" on single-column runs. With
  GERBIL's definition the aggregation differs (harmonic mean of macro P/R vs mean of F1), and
  empty answers score differently. Not checked: the Codabench scoring script, which might
  compute it differently.
- Test scores are whole numbers (85.0, 81.0, 79.0, ...) on 75 questions; possibly leaderboard
  rounding. Not stated.
- Not read: the challenge overview paper (Vol-4284, intro1) and the other team papers
  (AMA-KBQA, agentic-text2sparql-skills), which may define the metric and data more fully.
- Metadata: Semantic Scholar lists no venue or year for this paper; venue, editors and volume
  were taken from the CEUR Vol-4284 page; CEUR gives no page range.
