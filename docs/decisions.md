# Decision log

Append-only log of thesis decisions. Never delete or rewrite an entry. If a decision
changes, add a new entry and mark the old one `superseded by D-0xx`.

Entry format: ID, date, title; **Status** (`decided` | `tentative` |
`superseded by D-0xx`); **Decision**; **Rationale**; **Related** (question IDs or
files).

## <a id="d-001"></a>D-001 (2026-10-29): Topic and framing

- **Status:** decided
- **Decision:** The thesis is about converting multimodal questions (image + text)
  into SPARQL over Wikidata with an agentic, ReAct-style approach. The framing is
  "agentic text-to-SPARQL extended to images".
- **Rationale:** The user's topic. Inspired by SPINACH, GRASP and KGVoyager.
- **Related:** [FR-01](questions/FR-01-research-questions.md)

## <a id="d-002"></a>D-002 (2026-10-29): Dataset first, then the agent

- **Status:** decided
- **Decision:** First build an evaluation dataset of (image, question, gold SPARQL)
  items, then build and evaluate the agent on it.
- **Rationale:** No suitable evaluation data with images seems to exist (to verify in
  [LIT-01](questions/LIT-01-existing-image-sparql-benchmarks.md)). The dataset has a fixed (personal) deadline, [D-013](#d-013).
- **Related:** [LIT-01](questions/LIT-01-existing-image-sparql-benchmarks.md), [D-013](#d-013)

## <a id="d-003"></a>D-003 (2026-10-29): Wikidata only

- **Status:** decided
- **Decision:** Wikidata is the only knowledge graph, and the agent's tools may be
  Wikidata-specific. Tools that work across knowledge graphs (as in GRASP or
  KGVoyager) are out of scope; generalisation is future work. Whether to build on
  GRASP stays open.
- **Rationale:** Keeps the scope from exploding. Supporting other graphs would need
  class/property indexes and handling of different modelling conventions, plus a
  second benchmark, without adding to the core (multimodal) contribution. The image
  tool maps an image to entity IDs and is therefore not tied to Wikidata anyway.
- **Related:** [AG-01](questions/AG-01-own-agent-vs-grasp.md)

## <a id="d-004"></a>D-004 (2026-10-29): The depicted entity is never named

- **Status:** decided
- **Decision:** The question text never names the entity shown in the image; it is
  only reachable through the image.
- **Rationale:** Otherwise the image is not needed and the task becomes plain
  text-to-SPARQL.
- **Related:** [DS-01](questions/DS-01-question-types.md), [DS-09](questions/DS-09-generation-pipeline.md), [DS-12](questions/DS-12-query-images-and-leakage.md)

## <a id="d-005"></a>D-005 (2026-10-29): Query images come from Wikimedia Commons

- **Status:** decided
- **Decision:** Query images are Commons photos of the same entity, different from
  the image stored in the index. Commons licensing is followed; attributions are
  generated and published with the dataset.
- **Rationale:** Freely licensed images that can be linked to Wikidata items. Using a
  different photo avoids trivial exact-match retrieval (as in the POC).
- **Related:** [DS-12](questions/DS-12-query-images-and-leakage.md), [RP-01](questions/RP-01-image-storage.md), [RP-06](questions/RP-06-dataset-versioning.md)

## <a id="d-006"></a>D-006 (2026-10-29): One shared image index with distractors

- **Status:** decided
- **Decision:** Build an own vector index of entity images (Wikidata has none). There
  is one index shared by the whole dataset, containing the images of the gold
  entities plus distractor images.
- **Rationale:** More realistic than one small index per question (as in the POC);
  the gold entities of other questions act as distractors too.
- **Related:** [IX-01](questions/IX-01-distractor-strategy.md), [IX-02](questions/IX-02-distractor-count.md), [IX-04](questions/IX-04-index-payload.md)

## <a id="d-007"></a>D-007 (2026-10-29): Execution-based evaluation

- **Status:** decided
- **Decision:** Predictions are evaluated by running the predicted and the gold query
  and comparing their results, not by comparing query text.
- **Rationale:** Many syntactically different queries are equivalent; SPINACH, GRASP
  and KGVoyager all evaluate this way. Details (columns, snapshot, verification) are
  open.
- **Related:** [DS-08](questions/DS-08-gold-answers.md), [LIT-03](questions/LIT-03-kgqa-metrics.md), [EV-01](questions/EV-01-metrics.md)

## <a id="d-008"></a>D-008 (2026-10-29): Dev and test splits, no train split

- **Status:** decided
- **Decision:** The dataset has a dev split (for tuning prompts and tools) and a test
  split; there is no train split.
- **Rationale:** No training or fine-tuning is planned. Without a dev split, tuning
  would happen on the test set.
- **Related:** [DS-11](questions/DS-11-split-proportions.md)

## <a id="d-009"></a>D-009 (2026-10-29): Multi-image questions are a stretch goal

- **Status:** decided
- **Decision:** Questions with several images are only attempted if time allows.
- **Rationale:** Pessimistic planning; the single-image dataset comes first.
- **Related:** [DS-06](questions/DS-06-multi-image-questions.md)

## <a id="d-010"></a>D-010 (2026-10-29): Gemma on the DTU HPC, no paid APIs

- **Status:** tentative
- **Decision:** Use the Gemma model running on the university HPC cluster (believed to
  be Gemma 4, about 29B). No API credits are planned.
- **Rationale:** Available to the user without cost. Exact version and capabilities
  are unverified.
- **Related:** [AG-04](questions/AG-04-gemma-hpc.md), [AG-05](questions/AG-05-experiment-configurations.md)

## <a id="d-011"></a>D-011 (2026-10-29): Release as a public repository

- **Status:** decided
- **Decision:** The dataset and code are released in public repositories; a Hugging
  Face release is not planned.
- **Rationale:** User preference.
- **Related:** [RP-01](questions/RP-01-image-storage.md), [RP-06](questions/RP-06-dataset-versioning.md)

## <a id="d-012"></a>D-012 (2026-10-29): New dataset repository based on the POC

- **Status:** decided
- **Decision:** The real dataset pipeline goes into a new repository based on the
  proof of concept,
  [andrezz-b/thesis-dataset-poc](https://github.com/andrezz-b/thesis-dataset-poc)
  (local checkout: `../dataset-poc`).
- **Rationale:** The POC validated the approach (Commons images, CLIP + Qdrant index,
  gold SPARQL) but is structured around hand-made examples.
- **Related:** [RP-01](questions/RP-01-image-storage.md) to [RP-06](questions/RP-06-dataset-versioning.md)

## <a id="d-013"></a>D-013 (2026-10-29): Timeline

- **Status:** tentative
- **Decision:** Start 2026-11-02, hand-in 2027-04-02 (both fixed). Dataset finished
  by mid-January 2027 (personal deadline, so that the agent work fits before the
  hand-in).
- **Rationale:** Dates given by the user; the dataset deadline is self-imposed.
- **Related:** [DS-10](questions/DS-10-dataset-size.md)

## <a id="d-014"></a>D-014 (2026-10-29): How the thesis description is organised

- **Status:** decided
- **Decision:** The thesis description lives in `docs/`:
  - `THESIS.md` (overview);
  - `decisions.md` (this log);
  - `related-work.md`;
  - one file per open question in `docs/questions/`, whose index is generated by
    `scripts/questions.py` (`mise run questions`).
  Updates go through the local `thesis-description` skill.
- **Rationale:** Gives agents one source of truth. Per-question files can grow into
  research notes, and their front matter makes dependencies and the next steps
  visible.
- **Related:** `.opencode/skills/thesis-description/SKILL.md`
