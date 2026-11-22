---
key: shen2026sage
title: "SAGE-VQA: A Training-Free, Self-Evolving Agentic Framework with Grounded Evidence for Knowledge-Based Visual Question Answering"
authors: ["Ruirui Shen", "Jianqi Gao", "Xiangfeng Luo", "Yonggang Zhang", "Muran Yu", "Barney Haoyun Miao", "Hang Yu", "Yike Guo"]
year: 2026
venue: "arXiv preprint (v1, 15 Nov 2026)"
url: "https://arxiv.org/abs/2611.19933"
pdf: "https://arxiv.org/pdf/2611.19933"
arxiv: "2611.19933"
doi: ""
s2_id: "89d48e8ce4a7c7b71ad687d98a0b2bb1fa20c1aa"
code: ""
data: ""
status: reviewed
relevance: medium
read_depth: full
informs: [AG-02, EV-03]
themes: [vqa, visual-grounding, agentic-retrieval]
added: 2026-11-21
reviewed: 2026-11-22
candidates: []
bibtex: |
  @misc{shen2026sage,
    doi = {10.48550/ARXIV.2611.19933},
    url = {https://arxiv.org/abs/2611.19933},
    author = {Shen, Ruirui and Gao, Jianqi and Luo, Xiangfeng and Zhang, Yonggang and Yu, Muran and Miao, Barney Haoyun and Yu, Hang and Guo, Yike},
    keywords = {Computer Vision and Pattern Recognition (cs.CV), FOS: Computer and information sciences},
    title = {SAGE-VQA: A Training-Free, Self-Evolving Agentic Framework with Grounded Evidence for Knowledge-Based Visual Question Answering},
    publisher = {arXiv},
    year = {2026},
    copyright = {arXiv.org perpetual, non-exclusive license}
  }
---

# SAGE-VQA: A Training-Free, Self-Evolving Agentic Framework with Grounded Evidence for Knowledge-Based Visual Question Answering

## TL;DR

SAGE-VQA is a training-free KB-VQA pipeline around a frozen VLM. It parses the question into visual prompts and KG entities, segments the prompted objects with SAM3, lets the VLM verify each crop, and uses only verified crops for image-based KG retrieval. A readiness score decides whether to answer or to recheck or retrieve more. A self-evolving memory bank (SHM) is added on top. For us the useful part is the verify-then-retrieve step for image crops (§3.2, App. A.7); the memory part is out of scope. Full text read (arXiv HTML); the figures were not inspected.

## Problem and contribution

- Problem: VLMs spend capacity on irrelevant regions and make perception errors (object hallucination, missed details) that propagate into retrieval and reasoning; experience from similar questions is not reused (§1).
- Contribution (§1): (1) Co-verified Visual Grounding, where a segmentation model proposes regions and the VLM checks them; (2) SHM, a memory bank of declarative and procedural experience refined from feedback; (3) EDAR, the loop that combines visual evidence, KG facts and memories under a readiness check; (4) results on four datasets with a frozen backbone and no parameter training.

## Method

### Overall loop (EDAR, §3.4, Alg. 1, App. A.6)

1. A frozen VLM (the "fact reasoner" ℳ) writes a global caption C of the image. It parses question plus caption into two sets (Eq. 6): open-vocabulary visual prompts (text descriptions of target objects) and knowledge entities.
2. Per iteration t (at most T = 3, App. D): ground the visual prompts (below), query the KG, reason over everything, and compute a readiness score r_t in [0, 1] with a list of unresolved issues.
3. Stop when r_t ≥ 0.95 or t = T. Otherwise the issue category picks the next action: conflicting or missing visual details trigger a focused visual recheck, missing facts or definitions trigger more KG retrieval (§3.4, App. A.8). Issue categories: breadth, depth, contradiction, relevance.
4. In practice the loop rarely repeats: 97.97% of the 4,241 ScienceQA test questions stop after one iteration, mean 1.022 (App. F.5).
5. Cost (§3.4, App. A.6): O(mK) verification calls per iteration for m prompts with at most K candidates each, plus one readiness call per iteration; unchanged results are reused in later iterations.

### Visual grounding step (§3.2, App. A.3, A.7)

1. **Detect (parse):** the VLM turns question plus caption into visual prompts, for example "white and orange jersey". The prompts come from the question and a caption, not from the raw image directly.
2. **Segment:** SAM3 gets each text prompt and proposes up to K candidate regions, each with a mask and a bounding box.
3. **Verify, candidate vs prompt (Eq. 1):** the VLM sees the masked crop and the prompt ("Does it primarily show a '{target object}'?", JSON with `is_match` and `confidence_score`, App. A.2 Table 8). This gives a binary match and a confidence.
4. **Compare with the whole image:** the VLM compares the annotated candidates with its whole-image observations and notes disagreements in objects, attributes, counts and relations. This is a separate comparison, not part of Eq. 1 (App. A.3).
5. **Keep failures:** failed candidates stay in the evidence with their failure flags. An empty candidate set means missing perceptual support, not proof the object is absent (App. A.3). No extra confidence threshold is applied to either check (App. D).
6. **Arbitration:** one adjudicator prompt resolves disagreements between VLM observations and SAM3 detections. It states that SAM3 can miss objects (so counts are checked) and that for abstract concepts and relations the VLM is trusted (App. A.2 Table 9).

### How grounding feeds the KG query (§3.4, App. A.7)

- Two channels, both used in the first iteration; later iterations only query what is missing:
  - Entity channel: parsed entities query the Neo4j-hosted MMKG (cites Liu et al., 2019). This does not wait for grounding.
  - Visual channel: only candidates with `is_match = 1` are used. The bounding-box crop is embedded with CLIP, the 2 nearest images in the KG image index (FAISS) are found, and their linked graph entities are added (Eq. 8 to 10).
- Both entity sets give one-hop relations and facts, 15 triples per entity (Table 13); results are added to the accumulated knowledge, not replaced.
- The mask crop is used for verification, the box crop for retrieval.
- So verification gates only the visual channel, not the whole KG query. KG access is a retrieval function over a graph database, not SPARQL generation (the paper does not describe the graph schema further).

### Comparison with the M³-VQA agent ([ma2026m3](ma2026m3.md), §5.4, App. F.2 to F.5)

| Step | M³-VQA agent | SAGE-VQA |
| --- | --- | --- |
| Controller | Planner (GPT-4o) checks for enough information before each Executor call | The same frozen VLM parses, verifies, arbitrates and scores readiness |
| Detect | Qwen2.5-VL-7B outputs bounding boxes as JSON for the Planner's query | SAM3 from text prompts: masks and boxes |
| Crop | One crop per box | Mask crop for verification, box crop for retrieval |
| Verify | None | VLM checks each crop against its prompt, then compares local with global observations |
| Image retrieval | CLIP ViT-L, top 10 entities per crop | CLIP, top 2 images per verified crop, then one-hop facts |
| Text/entity retrieval | Question-aware retrieval over chapters of the matched Wikipedia pages | Parsed entities query the MMKG |
| Loop | Planner decides before each call | Readiness score with threshold 0.95 and budget 3 |

Assistant reading: SAGE-VQA is M³'s detect, crop, retrieve flow plus a verification stage, a global-vs-local comparison and a readiness loop. Complexity added over M³: one VLM verification call per candidate crop, an extra comparison call, a readiness call per iteration, a SAM3 model, and a caption plus parsing call at the start.

### Memory (SHM, §3.3, App. A.4, A.5): summary only, out of scope for us

A notebook of lessons the agent writes for itself; no model weights change.

- Entry types: episodic (lesson from one case), semantic (rule distilled from at least N = 10 similar episodes, with links to the sources), procedural (executable code with parameter schema and applicability conditions). The initial bank has 420 entries: 296 episodic, 53 semantic, 71 procedural (App. A.4).
- Retrieval: embed the question and compare with entry **titles** only; take the top max(3k, 5) with k = 2, weight each score by a usage weight and a type weight (1 / 1.15 / 1.20), keep entries above a threshold. The result can be empty (App. A.5, Table 13). Procedural entries run only if the question fits their conditions and all inputs exist.
- Update after answering, using the gold answer: a correct answer raises usage statistics; a wrong answer rewrites an applicable retrieved entry or only lowers the retrieval priority of an inapplicable one; if nothing was retrieved and the answer was wrong (or right after more than one iteration), a new entry may be extracted (Eq. 2 to 4, Alg. 2).
- Cold start: run EDAR on training samples without memory, record trajectories and feedback, build the bank (App. A.5).
- Illustration (assistant, not from the paper): the model answers "Which team wears white and orange?" wrongly (gold: Knicks) and nothing relevant was retrieved, so it stores an episodic lesson "identify the described team's colours before reading nearby text". A later similar question retrieves it by title similarity; if the answer is right, its success count goes up.
- Paper's own example (App. A.4): the semantic entry *Strictly Separate Visual Evidence from Historical Inference* was retrieved for two different MMMU questions (British-India trade, silver flows).
- Requirement that matters for us: updates need reference answers during evaluation, and the bank keeps changing while the test set is run (App. A.5, App. D).

## Data / benchmark

Not a dataset paper. It evaluates on ScienceQA (official test, 4,241 questions per App. F.5; 21,208 total), A-OKVQA (1,145 validation questions, MC and DA), MMMU (900 validation questions) and MicroQuant-VQA, a private dataset built by the authors (1,000 validation questions of 4,970, micro-CT lineal-path probabilities) (§4.1, App. C). No gold SPARQL; the KG is an MMKG in Neo4j with an image index; agentic evaluation is only of the authors' own system. Licence, data release and code: not stated.

## Key results

- ScienceQA, avg. accuracy: Qwen3.5-9B 95.33, 27B 98.56, Qwen3.6-35B 98.92, GPT-4o-mini 88.56; the training-free MG²-RAG (Qwen3.5-27B) reaches 97.85 (Table 1).
- A-OKVQA, multiple choice / direct answer: 9B 89.98 / 68.91, 27B 90.82 / 69.84, 35B 91.54 / 72.67 (Table 2).
- MMMU: 9B 66.30, 27B 75.32, GPT-4o-mini 64.59 against 59.40 for plain GPT-4o-mini (Table 3).
- MicroQuant-VQA: 9B 23.10 to 35.80, 27B 29.30 to 87.50 (Table 4); the benchmark is private.
- Incremental ablation, Qwen3.5-9B (Table 5): ScienceQA 70.79 (bare) to 76.96 (+MMKG) to 92.76 (+EDAR) to 95.33 (+SHM); MMMU 50.12 to 54.44 to 61.29 to 66.30. Qwen3.5-27B (Table 14): ScienceQA 91.98 to 93.00 to 96.11 to 98.56; MMMU 54.20 to 58.36 to 68.12 to 75.32.
- Case study (Table 7): the VLM misread a jersey, but image-based KG retrieval linked the photo to the New York Knicks, and the VLM then checked this against the colours. In a counting question, one SAM3 detection supported the correct count of one.
- Retrieval budgets are non-monotonic: the best accuracy is at k_m = 2 and k_g = 15 and drops when either is raised (App. F.4, Fig. 6).
- Memory-specific ablations: Table 15 (declarative vs procedural), Table 6 (84 hard cases, 5 passes, accuracy rises to 48.81% then falls, with regressions each pass). Not used by us.

## Limitations

Stated by the authors:

- Readiness is not a calibrated probability; budget exhaustion does not establish evidence sufficiency; missing image details and limited graph coverage can leave uncertainty (App. A.8).
- The fact reasoner must still have the concepts to interpret the evidence; verification cannot add them (App. G).
- Extensions to other domains (documents, medical triage, embodied agents) need separate evaluation (App. G).

We see (assistant reading):

- No ablation isolates verification. The "+EDAR" row adds visual verification and adaptive reasoning together (App. E, "Controlled internal baselines"). The +15.80 (9B ScienceQA) cannot be credited to verify-then-retrieve alone; with 97.97% of ScienceQA questions finishing in one iteration, the readiness loop may contribute little there, but this is not tested. The two checks (candidate-vs-prompt, local-vs-global) are not ablated separately either.
- The verifier is the same VLM that may hallucinate; no precision or recall of the verification step is reported, and no threshold on the confidence is used (App. D).
- The ScienceQA 9B gain (+15.80) is much larger than the 27B gain (+3.11 on ScienceQA, Table 14), so the benefit depends on the backbone.
- The memory bank is updated with gold-answer feedback during evaluation and started from a bank built on training data, which makes comparison with truly static baselines less clean (App. A.5, App. D). Retrieval budgets were tuned on the ScienceQA training split (App. D).
- No code or data link; MicroQuant-VQA is private; the KG is only named (MMKG, Neo4j) and not described.
- Datasets are ScienceQA, A-OKVQA, MMMU: not Wikidata, no entity-centric long-tail questions, so transfer to our setting is untested.

## Relevance to the thesis

Proposed, to be agreed with the user:

- [AG-02](../questions/AG-02-tool-set.md): adopt the verify-then-retrieve idea for an image crop tool. Detect or segment the entity regions, check each crop against the prompt that produced it, and send only the verified crops to the image-index search (§3.2, App. A.7, Eq. 8). Failed crops stay visible to the agent with a flag instead of being silently dropped (App. A.3). This extends the detect, crop, retrieve flow of M³-VQA ([ma2026m3](ma2026m3.md), §5.4) with one check. Suggested simplification (user idea): merge the paper's two checks (crop vs prompt, local vs global) into one "check" call that sees the crop and the whole image together and returns match, confidence and any disagreement. Cost to keep in mind: one extra VLM call per candidate crop (App. A.6). Contrast: SAGE-VQA uses SAM3 masks and a fixed pipeline controlled by a readiness score; we would keep box crops and let the agent decide when to use the tool. Cite for evidence that grounding and arbitration help (Tables 5, 14, 7), with the caveat that EDAR is not isolated.
- [EV-03](../questions/EV-03-ablations.md): possible ablation, only if we adopt the crop tool. Compare image-index search with (a) the whole image, (b) crops without check, (c) crops with the merged check. The paper has no such isolated test of verification, so this would also be a small contribution. If the two checks are kept separate, a fourth arm could add the second check; merging avoids that.

## Citable claims

- Verifying locally segmented candidates with the VLM and comparing them with whole-image observations, before the visual information is used for reasoning and retrieval, is the paper's way to reduce perception errors propagating into reasoning (§3.2).
- Only verified candidates (match flag 1) are used as query crops for image-based KG retrieval; failed candidates stay in the evidence with their annotations (§3.2, App. A.3, App. A.7, Eq. 8).
- An empty detection set is treated as missing perceptual support, not as evidence of absence; SAM3 can miss objects, so counts are checked against the VLM (App. A.3, App. A.2 Table 9).
- On Qwen3.5-9B, adding visual verification and adaptive reasoning to KG retrieval raised ScienceQA from 76.96 to 92.76 and MMMU from 54.44 to 61.29; on 27B from 93.00 to 96.11 and from 58.36 to 68.12 (Tables 5, 14). The increment covers verification and the readiness loop together (App. E).
- More retrieved material is not always better: accuracy peaked at 2 memory entries and 15 KG triples per entity and fell when either was increased (App. F.4).
- With a readiness threshold of 0.95 and a budget of 3, 97.97% of ScienceQA test questions finish after one iteration (App. F.5).
- Image-based retrieval can recover from a VLM misreading: in one A-OKVQA case, retrieval linked the photo to the right team although the VLM misread the jersey (Table 7).
- The framework works as a plug-and-play layer on frozen open-source VLMs of 9B to 35B parameters and on GPT-4o-mini, without parameter training (§4.2, §4.5).

## My notes

- How much more complex is the EDAR strategy compared to the M3 approach
- The memory system feels out of scope as it seems pretty complex and there are many other things to do
- The verify-then-retrieve idea and the local-vs-global check are the parts worth taking; possible ablation if we go for the crop tool; maybe merge the two checks into one "check" instead of two

## Open doubts

- Which part of the "+EDAR" gain comes from verification and which from the readiness loop? Not separated in the paper (App. E).
- How accurate is the VLM verifier (false accepts and false rejects of crops)? Not reported.
- Does a single merged check (crop plus whole image in one call) lose anything against the two separate checks? Not tested here.
- What the MMKG contains and how large it is: only named (Neo4j, cites Liu et al., 2019); not described in the main text or App. A.7.
- Not checked: figures 2 to 7 (images), the reference list tail, whether a PDF version differs from the HTML (the HTML table cross-references are inconsistent, e.g. several tables cited as "Table 5").
- No code release found; SAM3 availability and cost for us not checked.
