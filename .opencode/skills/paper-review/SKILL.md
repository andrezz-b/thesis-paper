---
name: paper-review
description: Review a research paper together with the user and write or update its literature note in docs/literature/ (metadata, BibTeX, key parts, relevance to the thesis, citable claims), then find related papers (references and citing papers) and maintain the reading queue. Use when the user shares a paper (arXiv ID, DOI, URL, PDF, or their own reading notes), says they read or want to review a paper, asks what to read next, or runs /paper. Not for general thesis information (use thesis-description) or for writing thesis text.
---

# Review a paper into a literature note

Each paper gets one note, `docs/literature/<key>.md`, written together with the user.
Notes are the reference for later writing: a writing agent must be able to cite a paper
correctly from its note alone. Accurate beats complete; say "not stated in the paper" or
"not checked" instead of filling a gap with something plausible.

| File | Role | Edit rules |
| --- | --- | --- |
| `docs/literature/<key>.md` | One note per paper: YAML front matter + sections | Created by `scripts/papers.py stub`; sections are drafted with the user |
| `docs/literature/README.md` | **Generated** index: reviewed, in progress, reading queue | Never edit; `mise run lit` |
| `docs/literature/skipped.md` | Rejected papers, so they are not suggested again | Append rows after the user confirms |
| `docs/literature/_template.md` | Template (sections, checklist, field comments) | Copy via the script |
| `docs/related-work.md` | Curated thematic overview, owned by `thesis-description` | Do not edit here; see step 5 |

## Hard rules

1. **Never invent facts.** Every statement about the paper comes from its text, with a
   location (section, table, figure or page). Quote numbers exactly. Mark your own
   judgement as such ("assistant reading", "our concern").
2. **`## My notes` belongs to the user.** Put what they tell you there verbatim (or
   tidied only if they ask). Never rewrite or delete it.
3. **Never copy BibTeX into `thesis/bibliography.bib`.** The entry stays in the note's
   front matter; it is added to the `.bib` only when the thesis actually cites the paper.
4. **Metadata is checked, not trusted.** The BibTeX and metadata come from the script
   (DBLP, doi.org or Semantic Scholar). Compare title, authors and year with the paper's
   first page. If the script says the BibTeX was "generated", say so to the user.
5. **Do not set `relevance`, `status: reviewed` or `informs` without the user's
   agreement.** Propose, then wait.
6. **Do not change `docs/` other than `docs/literature/`.** Thesis-level consequences go
   through `thesis-description` (step 5).
7. Write in English, concisely.

## Tools

```bash
uv run scripts/papers.py meta   <id>             # metadata, abstract, open-access PDF link
uv run scripts/papers.py bibtex <id>             # BibTeX with the note key
uv run scripts/papers.py stub   <id>             # create docs/literature/<key>.md (never overwrites)
uv run scripts/papers.py refs|cites|recs <id> [--top N] [--sort influence|year|citations] [--abstracts]
mise run lit            # regenerate the index
mise run lit:check      # validate notes and index
mise run lit:queue      # print the reading queue
```

`<id>` is an arXiv ID, DOI, Semantic Scholar ID or URL. Semantic Scholar is throttled
without a key (the script retries on its own; `S2_API_KEY` raises the limit). If a lookup
fails, say so; do not fill the gap from memory.

## Procedure

### 1. Capture

1. Resolve the paper: `uv run scripts/papers.py meta <id>`. If `docs/literature/` already
   has a note for it (same arXiv ID or DOI), continue with that note. Otherwise run
   `stub`. The note starts as `status: queued`; set it to `reading` when the user is
   reading it.
2. Get the full text, in this order: `https://arxiv.org/html/<arxiv-id>` (cleanest, use
   `webfetch`), then the open-access PDF link, then a local PDF the user names (or
   `docs/literature/pdf/<key>.pdf`). If only the abstract is reachable (paywall), tell the
   user and restrict the note to what the abstract supports; mark it `read_depth: skim`.
3. Collect the user's own notes: from the chat, or from `## My notes` if they already
   wrote there. Put chat notes into `## My notes` verbatim.
4. Read the context: `docs/THESIS.md` (scope, decisions), `docs/questions/README.md`
   (open questions and IDs) and the question files the paper plausibly touches. Also
   `docs/related-work.md` for what is already known about this paper.

### 2. Review: draft, then grill

1. Draft the sections of the note from the text: TL;DR, Problem and contribution, Method,
   Data / benchmark (only for dataset or benchmark papers; answer each checklist item or
   write "not stated"), Key results (number + location), Limitations (separate "authors
   say" from "we see"), Relevance to the thesis, Citable claims, Open doubts.
   - **Relevance to the thesis**: one bullet per question ID or thesis part (`LIT-01`,
     `AG-02`, ...), each saying **adopt**, **contrast** or **cite** and what exactly, with
     the location in the paper. Use bare IDs; `mise run questions` links them.
   - **Citable claims**: only what the paper says, in our words, with a location. These
     are what a writing agent will cite.
2. **Use the user's notes as the starting point**: where their notes and the paper
   disagree, or their notes mention something you cannot find, flag it.
3. **Grill**: ask 3 to 5 targeted questions, one round, no more. Prioritise (a) places
   where the paper touches an open question the user did not mention, (b) claims you could
   not verify, (c) what the user found most useful or unconvincing. "Don't know yet" goes
   into Open doubts; it is not a failure.
4. Revise the note from the answers. Show the user a short summary of the changes, not the
   whole file.

### 3. Finalise the note

Propose, then apply after the user agrees:

- `relevance`: **core** (the thesis positions itself against it, or builds on it directly),
  **high** (supplies a method, metric, dataset or baseline we will use), **medium**
  (useful background or one citable point), **low** (read for completeness).
- `read_depth`: `full` or `skim`; `informs`: question IDs; `themes`: a few short tags, reuse
  existing ones (`grep -h "^themes:" docs/literature/*.md`).
- `status: reviewed`, `reviewed: <today>`, `url`/`pdf`/`code`/`data` filled where known.

### 4. Explore related papers

Offer this at the end of every review (the user may decline). Launch the `lit-scout`
subagent, in the background if the user wants to keep working, with a prompt that holds:
the paper's ID and note path, one or two sentences on why it matters for the thesis (from
`Relevance to the thesis`), and the question IDs it informs. It returns candidates
(papers it cites, papers citing it, recommendations) as ready-to-paste YAML plus
suggestions to skip.

Then, with the user:

1. Go through the candidates; for each the user keeps, add it to the note's `candidates:`
   list (fields `id`, `title`, `via`, `why`). Drop the rest.
2. For candidates the user rejects for good, append a row to `docs/literature/skipped.md`
   (`| ID | Title | date | reason |`).
3. If a candidate is clearly a **core** paper for an open question, say so; the user may
   want to read it next.

### 5. Hand off thesis-level findings

If the review produced findings that change the thesis description (e.g. "this benchmark
does not release SPARQL", which bears on LIT-01), list them and offer to run the
`thesis-description` skill (procedure A) with them. Let that skill decide about questions,
decisions and `docs/related-work.md`. If a row for this paper exists in
`docs/related-work.md`, suggest linking it to the note (`docs/literature/<key>.md`); that
skill makes the edit.

### 6. Validate

```bash
mise run questions        # links bare question IDs in the note
mise run lit              # index
mise run lit:check        # must pass
mise run spell            # typos
```

Report: the note path, relevance, which questions it informs, candidates added, and what
the next item in the reading queue is (`mise run lit:queue`).

## Other requests

- **"What should I read next?"** Run `mise run lit:queue` and present the top items with the
  reason from `why`. Change no files.
- **"Explore from this paper"** (no review): run step 4 only; the paper needs a note first
  (`stub`), because candidates are stored in it.
- **A pile of paper IDs**: `stub` each (status `queued`) and stop; reviews happen one paper
  at a time.
