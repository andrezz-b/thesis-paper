---
key: choi2025progressive
title: "Progressive Multimodal Search and Reasoning for Knowledge-Intensive Visual Question Answering"
authors: ["Changin Choi", "Wonseok Lee", "Jungmin Ko", "Wonjong Rhee"]
year: 2026
venue: "Annual Meeting of the Association for Computational Linguistics"
url: "https://arxiv.org/abs/2509.00798"
pdf: "https://aclanthology.org/2026.acl-long.881.pdf"
arxiv: "2509.00798"
doi: "10.18653/v1/2026.acl-long.881"
s2_id: "c8be027aee9e9cea105f26e8a82da9bccc6ad8a8"
code: ""
data: ""
status: reviewed
relevance: medium
read_depth: full
informs: [AG-02, AG-01, IX-03]
themes: [vqa, agentic-sparql]
added: 2026-11-21
reviewed: 2026-11-21
candidates:
  - id: "arXiv:2611.19933"
    title: "SAGE-VQA: A Training-Free, Self-Evolving Agentic Framework with Grounded Evidence for Knowledge-Based Visual Question Answering"
    via: recs
    priority: high
    scout_priority: medium
    why: "Training-free agentic KB-VQA with a co-verified visual grounding module and evidence verification; fits the no-training scope and tests the same entity-grounding question as AG-01 and AG-02. Judged from abstract; venue not checked (Semantic Scholar unavailable)."
bibtex: |
  @inproceedings{choi2025progressive,
    title={Progressive Multimodal Search and Reasoning for Knowledge-Intensive Visual Question Answering},
    url={http://dx.doi.org/10.18653/v1/2026.acl-long.881},
    DOI={10.18653/v1/2026.acl-long.881},
    booktitle={Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
    publisher={Association for Computational Linguistics},
    author={Choi, Changin and Lee, Wonseok and Ko, Jungmin and Rhee, Wonjong},
    year={2026},
    pages={19291–19315}
  }
---

# Progressive Multimodal Search and Reasoning for Knowledge-Intensive Visual Question Answering

## TL;DR

PMSR answers knowledge-intensive VQA (image + question, answer from Wikipedia) with a
training-free loop: retrieve evidence, condense it into a short "reasoning record",
and use the records to write the next queries, with two retrieval knowledge bases (text and
image-text). Each record is built only from the newly retrieved evidence, which the authors
say limits error propagation. For this thesis it is a worked example of iterative,
image-grounded retrieval, but the answer is free text from Wikipedia, not a KG query.

## Problem and contribution

- Problem (§1): single-pass "retrieve-then-read" multimodal RAG often retrieves too little or
  distracting evidence; agentic approaches condition each step on the full growing
  history, so early errors can propagate and drift.
- Contribution (§1, Fig. 1): PMSR, built on two ideas: **record-isolated updates** (each new
  record is synthesised only from newly retrieved evidence) and **dual-scope querying**
  (a query from the latest record plus a query from the whole trajectory). Also
  heterogeneous KBs (text + image-text) and adaptive termination.
- Claims improved retrieval recall and end-to-end accuracy on six benchmarks (E-VQA,
  InfoSeek, MMSearch, LiveVQA, FVQA, OK-VQA) (Abstract, §4).

## Method

Notation: question `Q`, input image `I`, record `r_t`, trajectory `⟨r_0..r_t⟩`.
All operators `G_*` are MLLM prompts (Appendix A, not read); no training.

1. **Initial record (§3.1).** `d0 = G_desc(Q, I)` (question-relevant image description);
   `q_init = [Q; d0]`; retrieve `D0` from both KBs; `r0 = G_reason(Q, I, D0)`.
   Uses parametric knowledge (description) plus retrieved knowledge.
2. **Dual-scope queries (§3.2).** Per iteration `t`:
   - record-level: `[Q; r_{t-1}]` (concatenation, Eq. 4; local refinement of the latest deduction);
   - trajectory-level: `G_trajectory(Q, I, ⟨r_0..r_{t-1}⟩)` (an MLLM call, Eq. 5; finds
     gaps and conflicts, keeps the overall goal).
3. **Joint search (§3.3).** Text KB: cosine similarity of query and passage (Eq. 6).
   Multimodal KB: `λ·sim_text(q, caption) + (1-λ)·sim_img(I, I_c)` with λ = 0.5 (Eq. 7).
   Per iteration up to 20 passages and 10 image-text pairs, budget split evenly between
   the two queries.
4. **New record (§3.4).** `r_t = G_reason(Q, I, D_t)`; it sees only the new candidates, not
   earlier records; appended to the trajectory.
5. **Adaptive termination (§3.5).** Stop when the max cosine similarity between a new
   query and any earlier query is at least τ = 0.9 (Eqs. 9-10); the MLLM then answers from
   `Q`, `I` and the full trajectory. Maximum 5 iterations in the ablations (§5).

Setup (§4.1): fixed KBs, 2M Wikipedia image-text pairs (from InfoSeek) and about 21M
Wikipedia passages (FlashRAG); retrievers SigLIP2 (images), Qwen3-Embedding (text for the
multimodal KB), E5-base-v2 (text KB); backbones Qwen2.5-VL, Qwen3-VL (4B, 8B) and Gemini-2.5-Flash.

Implementation details (appendices):

- Prompts (App. A): `G_desc` = "Concisely describe the image which is relevant to the question";
  `G_trajectory` = a two-part prompt (`## Analysis`, then `## Output` with one new question)
  over query + accumulated records; `G_reason` = "summarize the correct and relevant
  information with respect to the image and question"; final answer = question + records +
  image, "provide a detailed answer". No length or schema constraint on records is given.
- Multimodal retrieval (App. D): normalised image and text embeddings are concatenated and
  searched with FAISS `IndexFlatIP`; with λ = 0.5 this equals the decoupled score of Eq. 7.
  KB from the InfoSeek Wikipedia dump of 2022-10-01.
- Web variant (App. B, C): Google Lens via ScrapingDog at t = 0 only, Ollama Web Search with
  GPT-OSS 120B summarisation afterwards, plus a query-condensation prompt; used for the
  search benchmarks (assistant reading: the Table 3 setup mixes web tools and the Wikipedia KB).
- Record-level query design (App. Q): plain concatenation was comparable to or better than
  entity extraction (E-VQA acc. 43.5 vs 41.0).

Worked example (Appendix O, Case 1, E-VQA, diet of a sea star): `r0` has only generic
sea-star knowledge; the record-level query refines species-level grounding, the
trajectory-level query keeps the diet intent; later records name *Pacific blood star*
(*Henricia leviuscula*) and answer "sponges and small bacteria".

## Data / benchmark

Not a dataset paper; it evaluates on existing benchmarks (§4.1, Appendix E). Items relevant
to our checklist:

- Gold SPARQL: not applicable; answers are text strings from Wikipedia (E-VQA, InfoSeek).
  InfoSeek questions are "grounded in Wikidata entities" and generated from templates
  over hundreds of relation types, kept only if Wikipedia evidence exists (App. E); no
  SPARQL is mentioned.
- Knowledge source: Wikipedia text and a 2M image-text KB (§4.1, App. D), not a KG.
- Image index: yes, 2M image-text pairs; distractors are not designed, but App. M studies
  their effect (see Key results).
- Agentic systems: compared in Table 3 (OmniSearch, MMSearch-R1, WebWatcher, DeepEyesV2)
  and App. N (WebWatcher).
- Sizes (App. E): InfoSeek 5K (M2KR val subset), E-VQA single-hop test split, FVQA 1.8K,
  OK-VQA 5K, InfoSeek Human 2K, LiveVQA 3,602, MMSearch 171 (visual subset).
- Whether the depicted entity is named in the question: not stated.

## Key results

- Recall (Table 1): cumulative recall at adaptive termination, 4B: 87.4 (InfoSeek), 64.3
  (E-VQA); 8B: 87.7 and 67.3. Previous best in the table: ReflectiVA 86.4 at R@20 (InfoSeek),
  OMGM† 58.7 at R@20 (E-VQA). Note: cumulative recall over several iterations is compared
  with single-pass R@k.
- Accuracy (Table 4): E-VQA single-hop 46.4 (Qwen3-VL-8B), 59.9 (Gemini-2.5-Flash) vs OMGM†
  51.2 (GPT-4o); InfoSeek M2KR 41.5 (8B) and 50.5 (Gemini). InfoSeek uses LLaVA-MORE-8B as the
  final answerer, so numbers are not comparable to rows with their own generator.
- Search benchmarks (Table 3, Qwen2.5-VL-7B): FVQA 61.2, InfoSeek Human 58.2, MMSearch 54.3
  (DeepEyesV2 63.7), LiveVQA 54.2.
- Iterations (Table 5, Qwen3-VL-8B, fixed 5 iterations): E-VQA BEM 37.1 → 47.1, recall 59.0 → 67.5;
  largest gains in iterations 1-2.
- Component ablation (Table 6, E-VQA): single-pass multimodal-only 30.7 BEM / 48.7 recall;
  full 46.4 / 67.3; adding the text KB gives recall 48.7 → 58.4; dual-scope BEM 34.4 → 37.3
  (hetero KB, no iteration).
- Adaptive termination (Table 7): 3.3 (InfoSeek) / 3.5 (E-VQA) average iterations instead
  of 5, with 55.1 vs 56.3 CEM and 46.4 vs 47.1 BEM.
- Trajectory types (Table 8, E-VQA): Stable-Correct 47.73%, Correction 30.06%, Conflict
  17.31%, Persistent-Fail 4.91%.
- Latency (Appendix P, Tables A10-A11): 17.20 s per iteration sequential on an RTX 3090
  (single-step RAG: 3.91 s); 4.33 s per iteration with concurrent retrieval and an H100;
  about 15.15 s per sample with 3.5 iterations.
- Distractors (App. M, Table A8, E-VQA subset with oracle text, Qwen3-VL-8B): oracle text
  alone 86.6% accuracy; plus 10 retrieved image-text pairs 78.7%; plus web text 72.5%; with
  20 pairs 64.3%. The authors suggest visually similar but irrelevant images interfere with
  entity grounding.
- Versus an agent (App. N, Table A9, E-VQA, same KB and retriever): Persistent-Fail 4.9%
  (PMSR) vs 51.8% (WebWatcher); Correction 30.1% vs 31.2%.
- Image-plus-text scoring (App. D, Table A1): image+text beats image-only on E-VQA (R@5 43.1
  vs 36.2, SigLIP2-g + Qwen3-Embedding-0.6B). λ sensitivity (App. L): R@5 48.2 at λ = 0.3
  down to 42.5 at λ = 0.7.
- Record in the query (App. I, Table A4): question + record vs question only, E-VQA R@5
  46.6 vs 43.1.
- Retrievers (App. J, S): larger retriever pair gives higher recall and BEM (E-VQA 8B BEM
  45.5 → 47.1); a Qwen3-VL-Embedding-2B retriever was not better (recall 60.2 vs 66.7 on E-VQA).
- Top-k (App. K): k = 20 vs 10 raises recall (67.3 → 72.8, 8B) with no BEM gain (46.4 vs 46.3).
- Per-iteration recall by KB (App. G, Table A2): heterogeneous KB highest at every step.
- OK-VQA accuracy (App. H): 66.0% (Qwen3-VL-8B, Wikipedia only) vs 59.9 MMSearch-R1 and
  67.8 DeepMMSearch-R1 (web).
- Record behaviour (App. R, LLM-judged): Compose 48.0/50.5% and Resolve Conflicts 62.0/70.5%
  (InfoSeek/E-VQA).
- Text-only HotpotQA (App. T): 59.8 accuracy, vs Search-R1-7B 58.6 and s3 59.0.

## Limitations

Stated by the authors (§8):

- Iterative retrieval and reasoning cost more than single-pass RAG.
- Sensitive to retrieval quality and query formulation; standard dense retrievers used.
- Limited by the MLLM's grounding and reasoning; small backbones may struggle.

We see (assistant reading, to confirm):

- Single evaluation run, no variance reported (§4.1).
- The drift argument is tested against one agent only (WebWatcher, App. N); its Table A9
  Persistent-Fail gap may also reflect other differences between the systems.
- Records are LLM summaries; App. R's behaviour labels are themselves LLM-judged.
- The recall comparison mixes cumulative recall with R@k of other methods (Table 1).
- Correct records exceed final accuracy on E-VQA (>70% Stable-Correct plus Correction vs
  46.4% accuracy, §6.1): the answer step is a bottleneck.
- Code or data link: none found in the text I read.

## Relevance to the thesis

Proposed, partly agreed with the user (see My notes).

- [AG-02](../questions/AG-02-tool-set.md): cite, optional approach. PMSR's iterative refine-the-grounding loop is an approach the
  agent could take, ideally as a switchable mode that can be tested; it is not a commitment
  because enabling it looks like substantial work (§3.2-3.4, App. O Case 1).
- [AG-01](../questions/AG-01-own-agent-vs-grasp.md): cite. A fixed workflow with per-step retrieval, not a free ReAct agent
  (contrast with the thesis' ReAct choice; §3).
- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): contrast. Benchmarks used here have no gold KG queries; answers are text
  from Wikipedia (§4.1).
- [LIT-04](../questions/LIT-04-distractor-literature.md) / [IX-01](../questions/IX-01-distractor-strategy.md) (proposed, not yet in `informs`): cite. Appendix M shows that visually
  similar but irrelevant retrieved images lowered accuracy even with oracle text (86.6% to
  78.7%, Table A8); this is evidence on the effect of distractors.
- [IX-03](../questions/IX-03-embedding-models.md): cite what they use. SigLIP2 for images (§4.1) vs CLIP ViT-B/32 in the thesis POC;
  Appendix J (scaling retrievers) not read.
- [EV-03](../questions/EV-03-ablations.md): possible. Ablating iterations, dual queries and KB type (Table 6) is a template for
  agent ablations.

## Citable claims

- Single-pass retrieve-then-read multimodal RAG often fails to gather sufficient
  knowledge and offers no way to revise misdirected reasoning (Abstract, §1).
- Agent frameworks that condition each step on the full history can let early errors
  drift into later steps (§1; this is the authors' argument, not shown for those systems).
- PMSR maintains a trajectory of compact records, each built only from newly retrieved
  evidence, and queries at both record and trajectory scope (§1, §3.2, §3.4).
- Iterating improves E-VQA from 37.1 to 47.1 BEM over 5 iterations, with the largest
  gains early (Table 5).
- Adding a textual KB to a multimodal KB raised E-VQA recall from 48.7 to 58.4 (Table 6).
- Adaptive termination cut the average iterations from 5.0 to 3.3-3.5 with comparable
  accuracy (Table 7).
- On E-VQA, Correction trajectories (30.06%) outnumber Conflict trajectories (17.31%) (Table 8).
- With the oracle text present, adding retrieved image-text pairs lowered E-VQA accuracy
  from 86.6% to 78.7% (Qwen3-VL-8B, App. M, Table A8).
- Combining image and text similarity retrieved better than image-only on E-VQA (App. D, Table A1).

## My notes

The user's own notes. Agents never rewrite or delete this section.

- Note it as an approach we could take for AG-02. In my mind it would be a nice thing to have
  and to be able to test; in an ideal world it would be a switch that I could toggle and then
  it would run in this mode. But realistically it feels like it will be some work to enable
  this, and with all the other possible challenges and time constraints I don't feel
  confident committing to this.
- Embedding model (IX-03): just note what they use.
- Gemini numbers: not used as a baseline.
- Cite the 2026 (conference) version: the thesis prefers conference papers over preprints.

## Open doubts

- The key `choi2025progressive` keeps 2025 (arXiv v1), while `year` and the BibTeX are 2026 (ACL 2026), which is the version to cite. Rename the key only if it is cited in the thesis and the mismatch bothers you.
- Exact record format and length: only the prompt wording is given (App. A.3), no schema.
- Table 3 mixes web tools and the Wikipedia KB for the web-equipped variant; what exactly
  each search-benchmark number uses is not fully clear (App. C).
- Gemini-2.5-Flash is a paid API; the thesis excludes paid APIs ([D-010](../decisions.md#d-010)), so its numbers (Table 4) are not used as a baseline (user decision).
