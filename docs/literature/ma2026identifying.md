---
key: ma2026identifying
title: "Identifying and Resolving Pitfalls of Knowledge-Based VQA Benchmarks: Auditing, Repairing, and Augmenting"
authors: ["Qian Ma", "S M Rayeed", "Charles V. Stewart", "Qiong Wu", "Yao Ma"]
year: 2026
venue: "European Conference on Computer Vision (ECCV) 2026"
url: "https://arxiv.org/abs/2607.00159"
pdf: "https://arxiv.org/pdf/2607.00159"
arxiv: "2607.00159"
doi: "10.1007/978-3-032-37574-2_1"
s2_id: ""
code: "https://github.com/VAN-QIAN/ECCV26-ARA"
data: "https://huggingface.co/datasets/VanQianMa/ECCV26-ARA"
status: reviewed
relevance: medium
read_depth: full
informs: [LIT-01, DS-05, DS-07, DS-08, DS-09, DS-13, IX-01]
themes: [kgqa, dataset-construction, distractors]
added: 2026-11-20
reviewed: 2026-11-20
candidates:
  - id: "S2:895b552280a5dacc75f7dfe8ba9306e180a9f27b"
    title: "A Wikidata-based Benchmark for Evaluating LLM-based Question Answering"
    via: recs
    priority: high
    why: "Wikidata-grounded QA benchmark; direct comparison for LIT-01 and gold-answer/validation practice (DS-08, DS-09). Title only: metadata lookup failed (HTTP 429), venue/year unverified, may be text-only."
bibtex: |
  @inbook{ma2026identifying,
    title={Identifying and Resolving Pitfalls of Knowledge-Based VQA Benchmarks: Auditing, Repairing, And Augmenting},
    ISBN={9783032375742},
    ISSN={1611-3349},
    url={http://dx.doi.org/10.1007/978-3-032-37574-2_1},
    DOI={10.1007/978-3-032-37574-2_1},
    booktitle={Computer Vision – ECCV 2026},
    publisher={Springer Nature Switzerland},
    author={Ma, Qian and Rayeed, S. M. and Stewart, Charles V. and Wu, Qiong and Ma, Yao},
    year={2026},
    pages={1–18}
  }
---

# Identifying and Resolving Pitfalls of Knowledge-Based VQA Benchmarks: Auditing, Repairing, and Augmenting

## TL;DR

Audits and repairs answer-evidence mismatches and underspecified questions in InfoSeek and E-VQA, then adds a distractor entity to each query image to test grounded disambiguation. Its checks suggest useful acceptance criteria for our dataset, while its image-composite augmentation is a possible separate difficulty setting—not the same as adding distractors to our shared image index.

## Problem and contribution

The paper argues that answer accuracy does not reliably measure knowledge-grounded reasoning when (A) the answer is not supported by the benchmark's knowledge source, (B) the question permits multiple reasonable answers, or (C) a single salient entity lets retrieval bypass grounded disambiguation (§1, §3). It contributes a four-stage audit-and-repair protocol for (A) and (B), and an image-level distractor augmentation protocol for (C) (§4–5).

## Method

The fixing pipeline verifies evidence, checks answer derivability and corrects or filters mismatches, minimally repairs missing attribute/temporal/spatial constraints, then rechecks for answer leakage, evidence support and a unique answer (§4.1). Two LLM verifiers are used for evidence checks; InfoSeek items are removed as unsupported only when both agree (§4.1). The augmentation composites one distractor with the anchor image: an intra-category distractor gets a minimal spatial or distinguishing cue in the question, while an inter-category distractor leaves the question unchanged (§5.1).

## Data / benchmark

This is an audit and augmentation of existing KB-VQA benchmarks, not a new image-plus-SPARQL benchmark.

- **Gold SPARQL:** No. The evaluation uses question-answer annotations and Wikipedia evidence/articles, not released executable graph queries (§4, §6.1).
- **Is the depicted entity named in the question?** The paper does not systematically report this for the original benchmark items. In intra-category augmentation it adds a spatial or distinguishing reference to identify the anchor; inter-category augmentation preserves the original question (§5.1–5.2).
- **Knowledge source:** E-VQA uses a controlled corpus of about 2 million Wikipedia articles; InfoSeek uses a 100K-article Wikipedia KB (§6.1). InfoSeek's QA construction uses Wikidata triples while its evaluation evidence is Wikipedia, which is the source of the mismatch studied in §3.1. No queryable KG endpoint or snapshot date is specified for the evaluated KBs.
- **Hops and question types:** The paper introduces no new hop taxonomy. It explicitly evaluates E-VQA in the single-hop setting (§6.1); the study is not a multi-hop SPARQL benchmark.
- **Image retrieval and distractors:** Initial image retrieval uses EVA-CLIP-8B and Faiss to retrieve articles (§6.1). Augmentation adds an image-level distractor alongside the anchor, not a distractor entity to a shared image index (§5.1). The paper does not describe releasing a thesis-style entity image index.
- **Agentic systems:** Five KB-VQA methods are evaluated, including Wiki-PRF's multi-round retrieval and tools (§6.1). None is a text-to-SPARQL agent.
- **Size, splits, licence:** After repair, InfoSeek retains 58,285 of 71,335 instances (81.7%); an entity-unique controlled subset has 1,924 items. The fixed E-VQA evaluation split has 4,750 items (§4.2). The paper reports 1,604 InfoSeek and 3,871 E-VQA augmented variants (§5.2). The code repository lists fixed/unfixed and augmented CSVs and tools; composite images are hosted in the linked Hugging Face dataset, while large original images, indexes, checkpoints and full raw outputs are not duplicated in Git (repository README). A data licence was not stated in the paper or repository overview checked.

## Key results

- The initial audit marks unsupported annotations in about 1% of E-VQA and 22% of InfoSeek (§3.1).
- The ambiguity audit reports 59% of E-VQA and 47% of InfoSeek questions as ambiguous; the tagged patterns are missing attribute, temporal or spatial constraints (§3.2).
- Fixing changes measured performance and can change method rankings on the same sample IDs. For example, InfoSeek IBA rises from 34.5 to 42.4, while ReflectiVA is 38.1 after fixing; IBA then exceeds ReflectiVA (§6.2, Table 1 and accompanying analysis).
- Adding one image-level distractor sharply lowers initial retrieval recall. R@1 on InfoSeek falls from 43.5% on the full fixed set to 14.7% intra-category and 20.4% inter-category; on E-VQA it falls from 13.4% to 3.5% and 2.9%, respectively (§6.3, Table 2).
- End-to-end QA accuracy also drops. On InfoSeek, IBA falls from 40.1% on the anchor subset to 21.4%/21.6% (intra/inter); EchoSight falls from 38.7% to 15.9%/17.8% (§6.3, Table 4).

## Limitations

**Authors say:** No dedicated limitations section was found in the main-text HTML. The conclusion calls for evidence-derivable, well-specified questions and evaluation that measures grounding robustness as well as answer correctness (§7).

**We see:** The audit relies on LLM judgments, and human checks cover samples rather than every item: 475 E-VQA and 200 InfoSeek fixed items, and 100 examples per augmentation type and dataset (§4.2, §5.2). The evidence is specific to two Wikipedia-based benchmarks and a single added image distractor; it does not establish that the same effects or repair workflow transfer directly to Wikidata execution-based QA or distractors in an entity image index. The human review supports the sampled repairs but cannot establish full-dataset validity.

## Relevance to the thesis

- **[LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md) — contrast:** This is relevant KB-VQA audit work, not an existing image + question + gold-SPARQL benchmark. Evaluation uses Wikipedia articles/evidence, not executable Wikidata queries (§4, §6.1).
- **[DS-09](../questions/DS-09-generation-pipeline.md) — adopt as candidate checks:** Check evidence support, sufficient question constraints for a unique answer, and answer leakage; the paper's examples of missing attribute, temporal and spatial constraints can inform manual review (§3.2, §4.1). Adapt evidence checks to the frozen Wikidata snapshot and the gold SPARQL result.
- **[DS-08](../questions/DS-08-gold-answers.md) — cite:** The answer-derivability check reinforces verifying that the gold answer follows from the chosen evidence source (§4.1). Our execution-based gold still needs its own snapshot and query validation.
- **[DS-05](../questions/DS-05-image-role.md) — cite:** The paper's composites add another entity to the query image while preserving an anchor. This is a possible image-role variant, distinct from multiple-image questions (§5.1).
- **[DS-07](../questions/DS-07-related-entity-images.md) — contrast:** Its distractor is a co-present entity in a composite image, not a related-entity query image of the kind used by RETINA (§5.1).
- **[DS-13](../questions/DS-13-difficulty-levels.md) — exploratory candidate:** The intra/inter composite settings could be considered as a separate image-level difficulty setting. They are not the same as shared-index distractors, and their large performance drops establish difficulty only for the tested retrieval methods and setup (§5.1, §6.3).
- **[IX-01](../questions/IX-01-distractor-strategy.md) — contrast:** This paper does not test which entities to put in the shared image index. Its distractor is inserted into the input image, so its results are not direct evidence for an index-distractor strategy (§5.1).

## Citable claims

- In the authors' audits, unsupported annotations occur in about 1% of E-VQA and 22% of InfoSeek (§3.1).
- The authors classify 59% of E-VQA and 47% of InfoSeek questions as ambiguous under their attribute, temporal and spatial constraint tags (§3.2).
- InfoSeek's QA construction from Wikidata triples and evaluation against Wikipedia evidence can produce answers unsupported by the evaluation KB (§3.1, Figure 1).
- Adding one same- or different-category distractor to the query image lowers initial retrieval R@1 and end-to-end QA accuracy on both datasets (§5.1, §6.3, Tables 2 and 4).
- After fixing, InfoSeek method rankings can change; IBA's reported score is 42.4 versus ReflectiVA's 38.1 (§6.2, Table 1 and accompanying analysis).

## My notes
- Main issues
	- Answer-evidence misalignment - e.g KB says 10 answer says 8
	- Under-specified questions - I think we address this in some of our requirements about ambiguous questions
	- Visually simplified scenes - our difficulty axis, and also we can approach it with the knowledge from the RETINA paper
- Their underspecified question patterns could be used as checks when creating our questions
	- Perhaps their repair steps can be converted to checks for us
- Augmentation setup of adding a distractor on the side of the image
	- I think this is an interesting approach, but it is mostly tailored for automatic fixing of these large datasets, as our will be much smaller we are better of using the RETINA paper approach or multi entity images from the [M³-VQA paper](ma2026m3.md)
- Even their distractor approach sharply drops performance which confirms multi entity (whichever approach) as good difficulty axis
	- 2026-11-20 (user): "Potentially, as a separate difficulty setting"; use all three checks (evidence support, unique answer, no answer leakage); the multi-entity-images paper meant here is M³-VQA.


## Open doubts

- Whether to include composite query images as a separate difficulty setting, and how to keep that distinct from the shared image-index distractor experiments ([DS-05](../questions/DS-05-image-role.md), [DS-13](../questions/DS-13-difficulty-levels.md), [IX-01](../questions/IX-01-distractor-strategy.md)).
- If included, which augmentation setting and how many items should be used; the paper's intra-category setting changes the question while its inter-category setting does not (§5.1).
- The example in My notes, "KB says 10 answer says 8," was not matched verbatim: §3.1 gives an unsupported "10 foot" annotation and a separate contradiction of 1,302 vs. 1,301 kg. Check whether the note refers to another example.
