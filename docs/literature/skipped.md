# Skipped papers

Papers that were looked at and rejected, so the scout does not suggest them again. One
row per paper; the first cell is the paper ID (`arXiv:...`, `DOI:...` or `S2:...`).
Rows are added by the `paper-review` skill after the user confirms.

| ID | Title | Date | Reason |
| --- | --- | --- | --- |
| arXiv:2412.18702 | CypherBench: Towards Precise Retrieval over Full-scale Modern Knowledge Graphs in the LLM Era | 2026-11-06 | Text-to-Cypher over property graphs; the thesis generates SPARQL over Wikidata [D-003](../decisions.md#d-003) |
| DOI:10.18653/v1/2026.acl-long.1601 | CypherSmith: Transforming Text-to-Cypher Generation for LLMs with Synthetic Data | 2026-11-06 | Text-to-Cypher with synthetic training data; the thesis uses SPARQL and has no training split ([D-008](../decisions.md#d-008)) |
| arXiv:2609.19417 | Less Is More: Graph-free Multimodal RAG via Multi-signal Late Fusion | 2026-11-07 | Image + question fusion for document-style RAG without a KG; no Wikidata or SPARQL link |
| S2:c94a8af151b91e5146041871e20e0033480c71e5 | Un jeu de données pour répondre à des questions visuelles à propos d'entités nommées | 2026-11-07 | Named-entity VQA dataset (ViQuAE line); not needed beyond ViQuAE already in related work |
| arXiv:2301.04366 | Multimodal Inverse Cloze Task for Knowledge-based Visual Question Answering | 2026-11-07 | Pre-training method for named-entity VQA; the thesis does not train models ([D-008](../decisions.md#d-008)) |
| DOI:10.18653/v1/2021.acl-short.60 | In Factuality: Efficient Integration of Relevant Facts for Visual Question Answering | 2026-11-07 | KVQA fact-selection method; not relevant to an agentic SPARQL approach |
| arXiv:1607.08221 | MS-Celeb-1M: A Dataset and Benchmark for Large-Scale Face Recognition | 2026-11-07 | Face-recognition dataset; the thesis images are not faces |
| arXiv:2204.10448 | Hypergraph Transformer: Weakly-Supervised Multi-hop Reasoning for Knowledge-based Visual Question Answering | 2026-11-07 | Trained KB-VQA model; the thesis does not train models ([D-008](../decisions.md#d-008)) |
| arXiv:1710.08092 | VGGFace2: A Dataset for Recognising Faces across Pose and Age | 2026-11-07 | Face-recognition dataset; the thesis images are not faces |
| arXiv:2512.13573 | MMhops-R1: Multimodal Multi-hop Reasoning | 2026-11-07 | Relation to the thesis not established (abstract not read); skipped on the user's call |
| arXiv:1908.02962 | CRIC: A VQA Dataset for Compositional Reasoning on Vision and Commonsense | 2026-11-07 | Commonsense knowledge (ConceptNet), not Wikidata ([D-003](../decisions.md#d-003)) |
| arXiv:2009.00145 | Cross-modal Knowledge Reasoning for Knowledge-based Visual Question Answering | 2026-11-07 | Trained KB-VQA method; the thesis does not train models ([D-008](../decisions.md#d-008)) |
| arXiv:2107.05348 | Zero-shot Visual Question Answering using Knowledge Graph | 2026-11-07 | Trained KB-VQA method on a non-Wikidata KB; the thesis does not train models ([D-008](../decisions.md#d-008)) |
