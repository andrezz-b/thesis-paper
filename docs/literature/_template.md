---
key: walter2025grasp # author + year + first title word; same key in the BibTeX entry below
title: Full paper title
authors: ["First Author", "Second Author"]
year: 2025
venue: "" # empty for preprints
url: "" # canonical public page (arXiv abstract page or DOI)
pdf: "" # only if open access
arxiv: ""
doi: ""
s2_id: ""
code: ""
data: ""
status: queued # queued | reading | reviewed
relevance: null # core | high | medium | low (set when reviewed)
read_depth: null # skim | full
informs: [] # question IDs from docs/questions, e.g. [LIT-01, AG-02]
themes: [] # free tags, e.g. [kvqa, agentic-sparql, metrics]
added: 2026-01-01
reviewed: null # date of the review session
candidates: [] # follow-up papers, filled in after the user confirms them
# candidates:
#   - id: "arXiv:2507.08107"
#     title: Paper title
#     via: cites # cites (newer paper citing this one) | refs (cited by this one) | recs
#     why: One line on why it matters for the thesis
bibtex: |
  @misc{walter2025grasp,
    title = {Title},
  }
---

# Full paper title

## TL;DR

Two or three sentences: what the paper does and why it matters for this thesis.

## Problem and contribution

## Method

## Data / benchmark

Only for dataset or benchmark papers. Checklist (answer each, with a location):

- Is gold SPARQL released?
- Is the depicted entity named in the question text?
- Which knowledge graph? Snapshot or endpoint?
- Multi-hop? Which question types?
- Is there an image index, and are there distractors?
- Are agentic systems evaluated?
- Size, splits, licence.

## Key results

Numbers with the table or section they come from, e.g. "F1 0.63 on Wikidata (Table 2)".

## Limitations

Stated by the authors, and ones we see (mark which is which).

## Relevance to the thesis

One entry per question ID or thesis part it touches. Say whether we **adopt**,
**contrast** with, or only **cite** it for that point.

- ID: adopt / contrast / cite. What exactly, and where in the paper.

## Citable claims

Claims the thesis may cite, each with a location, so nothing is cited that the paper
does not say.

- "Claim in our words" (§3.2, p. 4)

## My notes

The user's own notes. Agents never rewrite or delete this section.

## Open doubts

Things to check later (unclear details, results that look odd, missing ablations).
