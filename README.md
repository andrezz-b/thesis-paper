# Thesis Paper

LaTeX source for a DTU master thesis, based on the
[DTU Thesis template](https://gitlab.gbar.dtu.dk/latex/dtutemplates/-/tree/master/templates/Thesis).

The thesis studies answering **multimodal questions (an image plus a natural-language
question) over Wikidata by generating SPARQL with an agentic, ReAct-style LLM**. It first
builds an evaluation dataset of (image, question, gold SPARQL) items with a shared image
index, then builds and evaluates an agent on it. Hand-in: 2027-04-02.

Published PDFs: <https://andrezz-b.github.io/thesis-paper/>
(`thesis.pdf`, `project-plan.pdf`).

## Where to start

- [`docs/THESIS.md`](docs/THESIS.md): source of truth for topic, scope, decisions and open questions.
- [`docs/decisions.md`](docs/decisions.md): decision log.
- [`docs/related-work.md`](docs/related-work.md): papers and verification status.
- [`docs/questions/README.md`](docs/questions/README.md): open questions and what is ready to work on.
- [`AGENTS.md`](AGENTS.md): toolchain, tasks, and conventions for agents and humans.

## Repository layout

| Path | Contents |
| --- | --- |
| [`thesis/`](thesis/) | The thesis document ([`main.tex`](thesis/main.tex), [`Setup/`](thesis/Setup/), [`Chapters/`](thesis/Chapters/), [`bibliography.bib`](thesis/bibliography.bib)) |
| [`plan/`](plan/) | Project plan ([`main.tex`](plan/main.tex), [`gantt.tex`](plan/gantt.tex)) |
| [`docs/`](docs/) | Thesis description (Markdown) |
| [`scripts/`](scripts/) | Python helpers ([`questions.py`](scripts/questions.py)) |
| [`site/`](site/) | GitHub Pages landing page |
| [`.github/workflows/`](.github/workflows/) | CI ([`ci.yml`](.github/workflows/ci.yml)), Pages ([`pages.yml`](.github/workflows/pages.yml)), releases ([`release.yml`](.github/workflows/release.yml)) |
| [`.opencode/skills/`](.opencode/skills/thesis-description/SKILL.md) | Project skill for maintaining `docs/` |

Config: [`.latexmkrc`](.latexmkrc), [`mise.toml`](mise.toml), [`lefthook.yml`](lefthook.yml), [`_typos.toml`](_typos.toml).

Related repo: the dataset proof of concept,
[andrezz-b/thesis-dataset-poc](https://github.com/andrezz-b/thesis-dataset-poc).

## Setup

1. Install a full [TeX Live](https://tug.org/texlive/) (XeLaTeX, latexmk, biber, chktex) and the
   `fonts-liberation` font. Details in [`AGENTS.md`](AGENTS.md#toolchain).
2. Install the pinned tools with [mise](https://mise.jdx.dev/): `mise install`.
3. Check everything is available: `mise run doctor`.
4. Optionally install git hooks: `mise run hooks`.

## Common tasks

Run with `mise run <task>` (full list in [`AGENTS.md`](AGENTS.md#mise-tasks)):

| Task | What it does |
| --- | --- |
| `build` | Build thesis and plan (`<doc>/build/main.pdf`) |
| `watch:thesis` / `watch:plan` | Continuous rebuild |
| `fmt` / `fmt:check` | Format / check with tex-fmt |
| `lint` / `spell` | chktex / typos |
| `questions` / `questions:next` | Regenerate question index / list ready questions |
