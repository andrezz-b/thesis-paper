---
key: lee2025breaking
title: "Breaking the Visual Shortcuts in Multimodal Knowledge-Based Visual Question Answering"
authors: ["Dosung Lee", "Sangwon Jung", "Boyoung Kim", "Minyoung Kim", "Sungyeon Kim", "Junyoung Sung", "Paul Hongsuck Seo"]
year: 2025
venue: "arXiv.org"
url: "https://arxiv.org/abs/2511.22843"
pdf: ""
arxiv: "2511.22843"
doi: "10.48550/arXiv.2511.22843"
s2_id: "f3e5563d308ded15aa4b9da25a330537f0eb1cc5"
code: ""
data: ""
status: reviewed
relevance: high
read_depth: full
informs: [DS-05, DS-07, DS-09, DS-12, DS-13, IX-01, LIT-01]
themes: [vqa, dataset-construction, distractors]
added: 2026-11-08
reviewed: 2026-11-12
candidates:
  - id: "S2:e5d6cebefaa1557d80436eeccccdb9c12f597053"
    title: "MuKA: Multimodal Knowledge Augmented Visual Information-Seeking"
    via: refs
    priority: medium
    scout_priority: high
    why: "Base retriever of MIMIR and the origin of the image-only shortcut test (Fig. 2); template for DS-13 shortcut check; IX-03 is low priority and we do not train retrievers (judged from citing sentences)"
  - id: "arXiv:2402.08327"
    title: "PreFLMR: Scaling Up Fine-Grained Late-Interaction Multi-modal Retrievers"
    via: refs
    priority: medium
    scout_priority: high
    why: "Source of M2KR; its text-only retriever beats single-image retrievers on RETINA (Lee Table 1); IX-03 baseline (abstract seen)"
bibtex: |
  @misc{lee2025breaking,
    doi = {10.48550/ARXIV.2511.22843},
    url = {https://arxiv.org/abs/2511.22843},
    author = {Lee, Dosung and Jung, Sangwon and Kim, Boyoung and Kim, Minyoung and Kim, Sungyeon and Sung, Junyoung and Seo, Paul Hongsuck},
    keywords = {Computer Vision and Pattern Recognition (cs.CV), FOS: Computer and information sciences, FOS: Computer and information sciences},
    title = {Breaking the Visual Shortcuts in Multimodal Knowledge-Based Visual Question Answering},
    publisher = {arXiv},
    year = {2025},
    copyright = {Creative Commons Attribution 4.0 International}
  }
---

# Breaking the Visual Shortcuts in Multimodal Knowledge-Based Visual Question Answering

## TL;DR

Shows that common multimodal KB-VQA benchmarks (InfoSeek, E-VQA) can be solved by matching the query image to the main entity of the target document ("visual shortcut"), and builds RETINA, where the image depicts a related (secondary) entity instead. Existing retrievers drop sharply on it; MIMIR, which adds images of related entities to each document, recovers much of the gap. Relevant to the thesis mainly as a difficulty axis for image-to-entity grounding and as a template for LLM-driven question generation from related entities.

## Problem and contribution

- Problem: in existing MKB-VQA benchmarks the query image shows the main entity of the gold Wikipedia document, so retrieval can be done from the image alone (Sec. 1, Fig. 1a).
- Evidence: a retriever (MuKA) trained with the question text discarded reaches retrieval recall comparable to the image+text model on InfoSeek and E-VQA (Sec. 1, Fig. 2; the exact numbers are only in the figure, not checked).
- Contributions (Sec. 1): (1) RETINA benchmark, 120k automatically generated training samples and a 2k human-curated test set, queries refer to a related entity that is depicted in the image; (2) MIMIR retriever; (3) experiments.

## Method

- Question generation (Sec. 3.1, Fig. 3): an LLM (Qwen2.5-32B, App. A) extracts a one-hop graph around the main entity of a Wikipedia document (related named entities, each tagged with a natural-language relation sentence). Main entity = answer entity; a random related entity = query entity (its image becomes the query image); a second related entity = qualifying entity, added to make the answer unique. The LLM writes the question from this subgraph, must refer to the query entity only by a demonstrative ("this monument"), then paraphrases it. Questions retrievable by BM25 in the top 5 are dropped.
- Query images come from M2KR (OVEN, Google Landmarks v2, iNaturalist); document images from MuKA links, with replacements checked by perceptual hash (App. A.1).
- MIMIR (Sec. 4): extends MuKA (ColBERT-style late interaction, CLIP image encoder). Each document is augmented with the main-entity image of every related entity it mentions (avg. 4.3 related images, no upper bound, App. E), plus a multimodal cross-attention mapping and a learnable Entity Token Embedding marking which text tokens belong to which image. Related entities are found with an LLM; the paper notes Wikipedia hyperlinks could be used instead (Sec. 4.3).

## Data / benchmark

- Gold SPARQL released? Not applicable: Wikipedia text KB, no SPARQL or structured gold queries (Sec. 3, 5.1).
- Depicted entity named in the question? No, by construction: the LLM is instructed to use a demonstrative phrase (Sec. 3.1). Human curators also removed questions answerable without the image (21.27 % of the rejected ones) and with lexical cues (2.26 %) (App. A.3).
- Knowledge base: Wikipedia passages (EVQA subset of M2KR, shared with EVQA); no graph, no snapshot date stated (App. D).
- Multi-hop? The graph is one-hop around the main entity; the question subgraph is query entity, answer entity and qualifying entity (Sec. 3.1). Question types are not categorised. Retrieval is of a single gold document (Sec. 3.2).
- Image index / distractors: documents carry images; "distractors" in Sec. 5.2 are non-gold documents whose main entity equals the query-image entity (Fig. 5). Not a designed distractor set for an image index.
- Agentic systems evaluated? No; retrievers plus a fixed VILA-13B reader on the top-5 (Sec. 5.1).
- Size, splits, licence: 120k train, 2k test split into 1k seen and 1k unseen (GT document appears in training or not) (Sec. 3.2, App. A.3). Licence not stated in the paper; `code`/`data` links not given in the HTML text (only "Project Page" in the abstract).
- Curation: 3 CS students, 6k questions inspected, 29.16 % passed, about 24 h in total; 75.35 % of the rejected had multiple valid answers (App. A.3).

## Key results

- Table 1 (jointly trained on E-VQA and RETINA), Recall@5: RETINA seen / unseen: PreFLMR (text only) 23.6 / 11.1; UniIR 13.8 / 4.7; ReT 15.1 / 6.8; MuKA 20.8 / 8.6; MIMIR 43.2 / 36.9. On InfoSeek MIMIR 53.3 vs MuKA 51.7; on E-VQA 65.8 vs 64.9.
- Text-only PreFLMR beats single-image multimodal retrievers on RETINA, while the reverse holds on InfoSeek and E-VQA (Sec. 5.2, Table 1).
- Answer quality with ground-truth document: BEM 68.5 (seen) and 70.2 (unseen) vs MIMIR 32.7 / 31.6 (Table 1).
- Ablation (Table 2, Recall@5 on RETINA seen / unseen): MuKA 20.8 / 8.6; plus multiple images 38.1 / 33.3; plus multimodal features 41.1 / 34.5; plus entity token embedding 43.2 / 36.9.
- Distractor analysis (Sec. 5.2, Fig. 5): MuKA on the unseen subset retrieves distractors (documents whose main entity matches the query image) more often than the gold document; in the 14.5 % of cases where a distractor was retrieved, 78 % had only distractors in the top 5.
- MIMIR std over runs is about 0.4 to 0.8 points (Table 3, App. F).

## Limitations

- Authors say: MIMIR increases retrieval latency, because of the added image features (App. G). In the conclusion they point to other modalities of related context as future work (Sec. 6).
- We see (assistant reading): the benchmark is generated by an LLM from Wikipedia text, so correctness depends on the LLM and curation; only 29 % of sampled questions survived and most rejections were ambiguity, so the 120k training set still contains ambiguous items (App. B says they are kept deliberately). The relation between query and answer is a single sentence in the text, not a verifiable graph path. Related entities are mentions in the text and are not typed relations. The "visual shortcut" ablation is shown as a figure only; numbers not checked. No code or data link found in the text we read. Answer quality is measured only with BEM and a fixed reader.

## Relevance to the thesis

- [DS-05](../questions/DS-05-image-role.md) and [DS-07](../questions/DS-07-related-entity-images.md): cite. Closest precedent for an image that shows an entity other than the answer entity; reports that this breaks existing retrievers (Table 1, Sec. 1, Fig. 1). The user considers this setup increasingly likely for the thesis, and an adapted version of the related-entity image idea (related entity = graph neighbour of the answer entity in Wikidata, with the gold query built from the graph) an option.
- [DS-13](../questions/DS-13-difficulty-levels.md): adopt as an idea, cite. "Visual shortcut" is a grounding-difficulty axis: easy = image shows the entity the question is about; harder = image shows a related entity (Sec. 1, Fig. 1, Table 1). Also noted: run the image-only check (question text dropped, Fig. 2) on our dataset to test for such a shortcut.
- [DS-09](../questions/DS-09-generation-pipeline.md): contrast, lower priority. The test set (2k curated items) is the more likely source of example questions; the LLM pipeline (Sec. 3.1, App. A: one-hop graph, qualifying entity, demonstrative instead of entity name, BM25 filter, human curation) is a fallback if we run short of ideas, and every item would still need a gold query that this paper does not provide.
- [DS-12](../questions/DS-12-query-images-and-leakage.md): adopt/cite. Leakage controls in the paper (Sec. 3.1, App. A.1 to A.3): the question never names the depicted entity (demonstrative phrase); text-only retrievability checked with BM25 top 5 (37 % before, 25 % after paraphrasing, remaining ones dropped); query and document images from separate pools with a perceptual-hash duplicate check (hash size 8, distance <= 10); human removal of questions solvable without the image or containing the answer. User: questions will be verified by the user, so controls 1 (no entity name in the question) and 4 (human check for image-free solvability and answer in question) can become conditions for dataset questions; 2 and 3 are automatable.
- [IX-01](../questions/IX-01-distractor-strategy.md): cite. Hard distractors are documents whose main entity matches the query image; they dominate single-image retrieval once the shortcut is removed (Sec. 5.2, Fig. 5).
- [LIT-01](../questions/LIT-01-existing-image-sparql-benchmarks.md): cite as a related benchmark, not an answer: image + question, but no SPARQL or graph query (Sec. 3, 5.1).

## Citable claims

- Common MKB-VQA benchmarks are biased towards queries whose image shows the main entity of the gold document, which allows a "visual shortcut" (Sec. 1, Sec. 2).
- A retriever trained without the question text performs comparably to the image+text one on InfoSeek and E-VQA (Sec. 1, Fig. 2).
- On RETINA, where the query image shows a related entity, existing single-image retrievers degrade strongly, and text-only PreFLMR outperforms them (Table 1, Sec. 5.2).
- Adding images of related entities to the document embedding raises Recall@5 on RETINA unseen from 8.6 to 36.9 for MuKA-based retrieval (Table 2).
- In RETINA test construction, 29.16 % of 6k sampled questions passed human curation; the most common problem was multiple valid answers (75.35 % of rejected) (App. A.3).
- Query-image entity near-matches ("distractors") are retrieved more often than the gold document by single-image retrievers when no shortcut exists (Sec. 5.2, Fig. 5).

## My notes
- Difficulty axis - queries often match the primary entity
	- Beetle example - *Where does this animal live* + image of beetle - easy to match the main entity
	- Suggested alternative: *Which beetle from NA feeds on this plant* + image of potato
- Model trained only on images achieved comparable performance to models trained on both image and text
- LLM driven pipeline - use related entities to construct knowledge graphs and then use subgraphs to generate queries
	- Limited to 1 hop
- MIMIR - embedding related text and images along the query entity
	- Text would be less important as we are only on Wikidata?
	- Images of related entities could be perhaps an idea, although I don't understand the math details of it, and could we use an existing model, because if not seems like a lot of extra work

## Open doubts

- Fig. 2 numbers (image-only vs image+text) not read from the figure; check before quoting a number.
- Whether code, data and licence are released (project page not opened).
- The test construction removes related entities whose own document also lists the main entity (Sec. 3.2); effect on the benchmark's coverage unknown.
- Whether the user's notes "limited to 1 hop" is exact: the graph is one-hop around the main entity, but the question uses query, answer and qualifying entities (Sec. 3.1).
