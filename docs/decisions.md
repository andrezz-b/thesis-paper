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

- **Status:** superseded by [D-019](#d-019)
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

- **Status:** superseded by [D-015](#d-015)
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

## <a id="d-015"></a>D-015 (2026-10-30): Timeline v1 (project plan)

- **Status:** tentative
- **Decision:** The timeline of the first project plan (`plan/gantt.tex`):
  - milestones: project plan hand-in 2026-12-02; dataset frozen 2027-01-22;
    results frozen 2027-03-16; full draft to the supervisor 2027-03-22; hand-in
    2027-04-02 (fixed);
  - a small agent prototype on the POC examples (about one week of effort,
    2026-12-07 to 2026-12-18) to test the model setup on the HPC early; the main
    agent work starts after the dataset freeze;
  - a pilot generation and review round 2026-12-14 to 2026-12-22, full generation
    and review 2027-01-04 to 2027-01-22;
  - tuning on the dev split ends 2027-02-26; the test split is only used after that.
- **Rationale:** Moves the dataset freeze from mid-January ([D-013](#d-013)) to 2027-01-22
  for one more week of buffer. The user works a part-time job 3 days per week (can be
  reduced to 2), works at a reduced pace between Christmas and New Year
  (2026-12-23 to 2027-01-01), and the final buffer includes the Easter holidays
  (2027-03-25 to 2027-03-29). If the schedule slips, the stretch goal (multi-image
  questions, [D-009](#d-009)) is dropped first. The prototype and the dev/test rule came up in
  planning and review of the project plan.
- **Related:** [D-013](#d-013), [D-008](#d-008), [D-009](#d-009), [AG-04](questions/AG-04-gemma-hpc.md), [DS-09](questions/DS-09-generation-pipeline.md), [DS-11](questions/DS-11-split-proportions.md), `plan/gantt.tex`

## <a id="d-016"></a>D-016 (2026-10-30): LLM-assisted, manually curated questions

- **Status:** decided
- **Decision:** The dataset is not generated automatically by an LLM, and the Gemma
  model on the HPC is not used for it.
  - Any available LLM (also through a chat interface) is asked for question ideas.
    The prompt states the scope: question types, difficulty and similar details.
  - The student refines the ideas into items (question, gold SPARQL, answer, image)
    only if they meet the acceptance criteria (working list in [DS-09](questions/DS-09-generation-pipeline.md)).
  - The prompts and models used are logged for reproducibility.
  - The "generation" phases in [D-015](#d-015) now mean curation; the dates stay the same.
- **Rationale:** The user's intended method: LLMs as a source of ideas, with
  quality controlled by manual curation against explicit criteria.
- **Related:** [DS-09](questions/DS-09-generation-pipeline.md), [DS-10](questions/DS-10-dataset-size.md), [AG-04](questions/AG-04-gemma-hpc.md), [D-015](#d-015)

## <a id="d-017"></a>D-017 (2026-10-30): The dataset is a contribution, not a research question

- **Status:** tentative
- **Decision:** The evaluation dataset is presented as a contribution of the thesis.
  The research questions are only about the agent (RQ1 agent, RQ2 grounding, RQ3
  difficulty; see [FR-01](questions/FR-01-research-questions.md)). The dataset construction has no hypothesis.
- **Rationale:** With manual curation ([D-016](#d-016)), building the dataset is a method and
  not something that is measured. Tentative until the supervisor answers the
  question about this in the project plan.
- **Related:** [FR-01](questions/FR-01-research-questions.md), [D-016](#d-016)

## <a id="d-018"></a>D-018 (2026-11-03): Thesis title

- **Status:** decided
- **Decision:** The title is
  - English: "Multimodal Knowledge Graph Question Answering using an Agentic/ReAct Framework";
  - Danish: "Besvarelse af spørgsmål over multimodale vidensgrafer ved hjælp af en agentbaseret/ReAct-tilgang".
- **Rationale:** Given by the user (2026-11-03). Confirmed by the user for use in the
  thesis and project plan.
- **Related:** [FR-02](questions/FR-02-thesis-title.md)

## <a id="d-019"></a>D-019 (2026-11-03): Use DTU CampusAI instead of "Gemma on the HPC"

- **Status:** tentative
- **Decision:** The LLM deployment at DTU is called CampusAI
  (https://campusai.compute.dtu.dk/models/, only reachable through the DTU VPN). Models
  are used through its OpenAI-compatible API with a key from the CampusAI console. No
  paid APIs (as in [D-010](#d-010)). Which model runs the agent is not decided yet ([AG-04](questions/AG-04-gemma-hpc.md)).
- **Rationale:** The catalog shown by the user (2026-11-03) lists Qwen3.8-27B as the
  flagship chat model and Gemma 4 E4B only as the image-input model, so "Gemma, about
  29B" from [D-010](#d-010) does not match. Tentative until the model choice is made.
- **Related:** [D-010](#d-010), [AG-04](questions/AG-04-gemma-hpc.md), [AG-05](questions/AG-05-experiment-configurations.md)
