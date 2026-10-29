---
name: thesis-description
description: Maintain the thesis description in docs/ (THESIS.md, decisions.md, related-work.md, questions/). Use whenever the user shares new information about the thesis (research findings, papers, supervisor feedback, experiment results, decisions, changed plans), even unstructured; the skill triages it against existing open questions (resolves, annotates or creates them) and proposes the changes. Also use to add, answer, re-prioritise or drop a question, to ask what to work on next, or to be "grilled" about gaps. Not needed for merely reading the description.
---

# Maintain the thesis description

`docs/` is the source of truth for what the thesis is about. Agents and the user rely
on it being **accurate**, not complete. Recording a gap honestly is better than
filling it with something plausible.

| File | Role | Edit rules |
| --- | --- | --- |
| `docs/THESIS.md` | Overview: current state with markers [Decided], [Tentative], [Open: ID], [Stretch] | Edit in place; keep it short; link to questions instead of repeating them |
| `docs/decisions.md` | Decision log `D-NNN` | **Append only.** Never delete or rewrite; supersede with a new entry |
| `docs/related-work.md` | Papers with full titles, links, relevance, verification date | Mark `unverified` unless checked online |
| `docs/questions/<ID>-<slug>.md` | One open question each, YAML front matter + sections | See schema below |
| `docs/questions/README.md` | **Generated** index + dependency graph | Never edit by hand; `mise run questions` |
| `docs/questions/_template.md` | Template for new questions | Copy it |

## Hard rules

1. **Never invent facts.** Only record what the user said, what you verified (cite
   the source), or what is clearly marked as a suggestion ("assistant suggestion, not
   decided"). Dates, the title, model versions and numbers must come from the user
   or a source.
2. **Never promote** something to [Decided] (or a question to `decided`) without the
   user's explicit confirmation. If in doubt, use [Tentative] and ask.
3. **Do not silently remove anything.**
   - A changed decision gets a new `D-NNN` entry, and the old one gets
     `Status: superseded by D-NNN`.
   - An answered question moves to `decided` (with a Resolution), it is not deleted.
   - An irrelevant question becomes `dropped`, with the reason in its Resolution.
4. The thesis title is set by the user after approval (FR-02). Do not propose one in
   the docs.
5. Write in English, concisely. Use full paper titles plus links in
   `related-work.md`.

## Cross-references

- Write references as bare IDs (`DS-02`, `D-007`) or as existing links.
  `mise run questions` turns bare IDs anywhere in `docs/**/*.md` into relative
  links: question IDs link to the question file, decision IDs to
  `decisions.md#d-NNN`. Front matter, headings and code are left alone.
- Decision headings must look like `## D-NNN (YYYY-MM-DD): Title`. The script adds
  the `<a id="d-NNN"></a>` anchor; never write or edit it by hand.
- Link to the proof of concept on GitHub
  (https://github.com/andrezz-b/thesis-dataset-poc, e.g.
  `.../blob/main/README.md`), not only to the local `../dataset-poc` path.
- `mise run questions:check` fails on unknown IDs, broken relative links, unknown
  decision anchors, or files that still contain bare IDs.

## Question file schema

```yaml
---
id: DS-02            # <PREFIX>-<NN>; prefix by area: FR framing, LIT literature,
                     # DS dataset, IX index, AG agent, EV evaluation, RP repo
title: Which part of Wikidata is well connected enough?   # phrased as a question
area: dataset        # framing | literature | dataset | index | agent | evaluation | repo
status: open         # open | researching | decided | dropped
phase: dataset       # dataset (deadline: mid-Jan 2027) | agent | writing
priority: high       # high | medium | low
depends_on: [DS-01]  # HARD: cannot be settled before these are decided/dropped
informs: [IX-01]     # SOFT: the answer shapes these
---
```

Sections, in order: `## Question`, `## Why it matters`, `## Notes`, `## Resolution`.
The Resolution stays `_Not resolved yet._` until the question is decided or dropped.
The validator rejects `decided`/`dropped` with an empty Resolution.

- File name: `<ID>-<kebab-slug>.md`. A new ID is the next free number in its area.
  IDs are never reused or renumbered.
- `depends_on` only for real blockers; otherwise use `informs`. Dependency cycles are
  rejected.
- `Notes` is the research log. Add findings with sources, options with pros/cons and
  the user's leanings (label them as leanings).

## Procedures

### A. The user shares new information (triage)

This is the main entry point. The user just dumps what they learned (a paper they
read, a supervisor meeting, an experiment result, a decision). Do not make them
say which question it belongs to; work it out and propose.

1. **Split** the input into individual pieces (one finding, decision or idea each).
2. **Match** each piece against what exists:
   - scan all IDs and titles in `docs/questions/README.md` (tables *By area*);
   - search for keywords in the question files and in `docs/decisions.md`, e.g.
     `rg -i "distractor|hard negative" docs/`;
   - read the candidate question files (Question + Notes) and the related THESIS.md
     section.
3. **Classify** each piece into exactly one action:

   | The piece... | Action |
   | --- | --- |
   | fully answers an open question and the user states it as settled | resolve: procedure B, `status: decided` |
   | answers a question, but the user is unsure or it is preliminary | add to Notes, `status: researching`, propose the resolution text, mark [Tentative] in THESIS.md |
   | is a partial finding, source or option for a question | add a dated note `- YYYY-MM-DD: ... (source)`; `open` → `researching` |
   | changes or contradicts an existing decision | new `D-NNN` superseding the old one (procedure B) |
   | reveals a gap not covered by any question | new question (procedure C), with proposed `depends_on`/`informs` |
   | makes a question irrelevant | drop (procedure D) |
   | changes urgency, a deadline or a dependency | front-matter edit (procedure D) |
   | is general context with no open question attached | update the THESIS.md section |

   One piece can touch several questions, e.g. a finding for DS-02 that also informs
   IX-01. Put the note where it belongs and add a one-line pointer in the other.
4. **Propose before writing.** Show a triage table and wait for one confirmation.

   | # | Information (short) | Affects | Action | New status |
   | --- | --- | --- | --- | --- |
   | 1 | QLever has a fixed 2026-09 snapshot | DS-04 | note + propose resolution | researching |
   | 2 | Distractors should vary by similarity | – | new question IX-05 | open |

   - Flag uncertain matches ("could be DS-05 or DS-07?").
   - Ask directly if a piece reads like a decision but is not clearly one.
   - If the user already said "decided" or "apply directly", skip the wait.
5. **Apply** the confirmed actions (procedures B to D). Update the THESIS.md sections
   and markers so they match, and update `_Last reviewed:_` to today's date.
6. **Finish** with procedure E (regenerate and check), then F (consistency), then
   report what changed:
   - which questions were resolved or created;
   - which questions **became ready** because of this: compare
     `mise run questions:next` before and after.

   Then do G (grill), focusing on the newly ready questions.

### B. Record a decision (or resolve a question)

1. Confirm the exact wording with the user if it is not explicit.
2. Append `D-NNN` to `docs/decisions.md` (next number; format as in the file). Use
   `tentative` if the user is not sure.
3. If it answers a question: set `status: decided`, write the Resolution (one or two
   sentences + "See D-NNN").
4. Replace `[Open: ID]` in THESIS.md with `[Decided, D-NNN]` (or [Tentative]).
5. Check the dependents (`informs` and reverse `depends_on`). Add notes there if the
   decision changes them.

### C. Add a question

1. Check that it is not already covered: procedure A, step 2. If an existing
   question is close, extend its Notes or broaden it instead of adding a near
   duplicate.
2. Copy `_template.md` and fill in all fields; link `depends_on` / `informs` in both
   directions where it makes sense.
3. Reference it from the relevant THESIS.md section as `[Open: ID]`.

### D. Drop or re-prioritise

- To drop: set `status: dropped`, write the reason in the Resolution, and remove or
  adjust the THESIS.md marker.
- Changes to priority, phase or dependencies are front-matter edits; mention them in
  the summary to the user.

### E. Regenerate and validate (always, after any change in docs/questions)

```bash
mise run questions        # links bare IDs in docs/, adds decision anchors, rewrites the index
mise run questions:check  # validation; must pass
mise run spell            # typos
```

### F. Consistency check

After updating, check that these do not contradict `docs/`:

- `plan/main.tex`: objectives, approach, timeline (`plan/gantt.tex`), risks;
- `thesis/Setup/Statics.tex`: metadata, title;
- the thesis chapters in `thesis/Chapters/`.

Report conflicts to the user; do not edit LaTeX unless asked. If you do edit `.tex`,
run `mise run fmt`.

### G. Grill round (end of every update)

Ask the user 3–5 targeted questions about the most important remaining gaps.
Prioritise:

1. questions in the *Ready now* table (`mise run questions:next`) in phase `dataset`;
2. items still [Tentative] in THESIS.md that block others;
3. new questions raised by the update itself.

Answers that are "don't know yet" go into the question's Notes. They are not
failures.

### H. "What should I work on next?"

Run `mise run questions:next`. Present the top items with a short reason each (what
they unblock, deadline phase). Do not change any files.

## Growth

If a THESIS.md section grows beyond about a screen, propose splitting it into
`docs/<topic>.md` with a summary and link left in THESIS.md. Ask the user before
restructuring.
