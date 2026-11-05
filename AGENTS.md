# Thesis Paper

This repository contains the LaTeX source for a master thesis, based on the
[DTU Thesis template](https://gitlab.gbar.dtu.dk/latex/dtutemplates/-/tree/master/templates/Thesis).
Writing is augmented with AI/agentic tooling, so this document exists to
orient an agent (or a human) quickly.

**What the thesis is about:** read [`docs/THESIS.md`](docs/THESIS.md) first.
It is the source of truth for topic, scope, decisions and open questions.
Update it only via the `thesis-description` skill
(`.opencode/skills/thesis-description/SKILL.md`).

## Toolchain

- **TeX distribution:** [TeX Live](https://tug.org/texlive/) (full scheme),
  not managed by mise. The upstream installer is recommended over distro
  packages (distro TeX Live is often outdated):
  download `install-tl-unx.tar.gz` from `mirror.ctan.org/systems/texlive/tlnet/`,
  unpack, then run
  `perl ./install-tl --no-interaction --texdir ~/.local/texlive/2026`
  and add `~/.local/texlive/2026/bin/<arch>` (e.g. `x86_64-linux`) to `PATH`.
  Any other full TeX distribution (MacTeX, MiKTeX) works too.
- **LaTeX engine:** XeLaTeX (both documents use `fontspec`).
- **Fonts:** the DTU template specifies Arial; we use **Liberation Sans**
  (metric-compatible, so layout is identical; installable as
  `fonts-liberation`). Switch back in `thesis/Setup/Settings.tex` if desired.
- **Build orchestration:** `latexmk` with one shared root `.latexmkrc`
  (XeLaTeX, biber, output to `build/`). Documents are built with
  `latexmk -cd <doc>/main.tex`. latexmk only reads the rc file in the
  current directory, so each document folder has a tiny `.latexmkrc` that
  does `do '../.latexmkrc';` to load the shared one (this also makes VS Code
  LaTeX Workshop work).
- **Bibliography:** `biblatex` + `biber` (not classic bibtex).
- **Linting:** `chktex`; spelling with `typos` (`_typos.toml`).
- **Formatting:** [`tex-fmt`](https://github.com/WGUNDERWOOD/tex-fmt).
- **Hooks:** `lefthook` (`lefthook.yml`): pre-commit runs tex-fmt check,
  chktex (advisory) and typos on staged files.
- **mise** pins `tex-fmt`, `lefthook`, `typos`, `python` and `uv`
  (`mise install`). `latexmk`, `xelatex`, `biber`, `chktex`, `latexdiff-vc`,
  `texcount` come from TeX Live.
- **Python helper scripts** (`scripts/`) run via `uv run`; dependencies are in
  `pyproject.toml`/`uv.lock`, the venv is `.venv/` (gitignored). mise sets
  `UV_PYTHON_DOWNLOADS=never` so uv uses the mise-managed Python.

## mise tasks

Run with `mise run <task>`:

| Task                              | What it does                                                         |
| --------------------------------- | -------------------------------------------------------------------- |
| `doctor`                          | Verifies all required tools are on `PATH`.                            |
| `build`                           | Builds both documents.                                                |
| `build:thesis` / `build:plan`     | Build one document (`<doc>/build/main.pdf`).                          |
| `watch:thesis` / `watch:plan`     | Continuous rebuild (`latexmk -pvc`) for live preview.                 |
| `lint`                            | `chktex` over all `.tex` files (advisory; template has warnings).     |
| `fmt` / `fmt:check`               | Format in place / check formatting with `tex-fmt`.                    |
| `spell`                           | Spell-check with `typos`.                                             |
| `wordcount`                       | `texcount` word count of the thesis.                                  |
| `questions`                       | Link bare question/decision IDs in `docs/` and regenerate `docs/questions/README.md`. |
| `questions:check`                 | Validate `docs/` (metadata, links); fail if anything is stale.        |
| `questions:next`                  | List open questions that are ready to work on.                        |
| `lit` / `lit:check`               | Regenerate / validate the literature notes index (`docs/literature/README.md`). |
| `lit:queue`                       | Print the reading queue (suggested papers not yet read or skipped).   |
| `paper <cmd> <id>`                | Paper lookup: `meta`, `bibtex`, `refs`, `cites`, `recs`, `stub` (`scripts/papers.py`). |
| `diff <git-ref> [thesis\|plan]`   | latexdiff against a git ref -> `<doc>/build/diff.pdf` (default thesis). The ref must contain `<doc>/main.tex`. |
| `clean` / `rebuild`               | Remove build artifacts of both documents / clean then build.          |
| `hooks`                           | Install git hooks (`lefthook install`).                               |

## Structure

- `thesis/` — self-contained thesis document (build with
  `mise run build:thesis`):
  - `main.tex` — entry point, `\input`s everything else (paths are relative
    to `thesis/`).
  - `Setup/` — preamble, packages, settings (`Statics.tex` has thesis
    metadata: title, author, department, etc. — edit this first).
  - `Frontmatter/`, `Chapters/`, `Backmatter/`, `Pictures/`,
    `bibliography.bib`, `TEMPLATE_README.md` (original DTU readme).
- `plan/` — project plan (`article` class): `main.tex` and `gantt.tex`
  (pgfgantt chart, `\input` from the Timeline section).
- `docs/` — thesis description (source of truth, Markdown):
  - `THESIS.md` — overview with [Decided]/[Tentative]/[Open: ID] markers.
  - `decisions.md` — append-only decision log (`D-NNN`).
  - `related-work.md` — papers with full titles, links, verification status.
  - `questions/` — one file per open question (YAML front matter: status,
    phase, priority, `depends_on`, `informs`); `README.md` there is generated
    by `scripts/questions.py`.
  - `literature/` — one note per paper (front matter: authors, URL, BibTeX,
    relevance, `informs` question IDs, follow-up `candidates`; sections: key
    parts, relevance to the thesis, citable claims, the user's own notes).
    `README.md` there (reviewed papers, in progress, reading queue) is generated
    by `scripts/literature.py`; `skipped.md` lists rejected papers.
- `scripts/` — Python helpers (`questions.py`, `literature.py`, `papers.py`),
  run with `uv run`. `papers.py` queries Semantic Scholar, DBLP and doi.org
  (cache in `.cache/`, gitignored; optional `S2_API_KEY` env var).
- `.opencode/skills/` — project skills (`thesis-description`, `paper-review`).
- `.opencode/commands/paper.md` — `/paper <id|url|pdf> [explore]` starts a paper review.
- `.opencode/agents/lit-scout.md` — read-only subagent that finds related papers.
- `site/` — static GitHub Pages landing page (`index.html`, `style.css`).
- `.github/` — workflows: `ci.yml` (PRs/branches: fmt, lint, spell, build,
  PDF artifacts), `pages.yml` (push to main: build changed docs, reuse
  deployed PDFs for unchanged ones, deploy to Pages at
  `andrezz-b.github.io/thesis-paper/{thesis,project-plan}.pdf`),
  `release.yml` (tags `v*`: GitHub Release with both PDFs). Shared setup in
  `.github/actions/setup-tex` (runs in the `texlive/texlive` container).
- Root config: `.latexmkrc`, `mise.toml`, `lefthook.yml`, `_typos.toml`,
  `.editorconfig`, `pyproject.toml` + `uv.lock`, `.vscode/` (LaTeX Workshop + LTeX+).

## Agent conventions

- For thesis context, read `docs/THESIS.md`; never contradict it silently.
  When the user shares new thesis information or decisions, use the
  `thesis-description` skill. Never hand-edit `docs/questions/README.md`
  or the decision anchors; write question/decision IDs bare (`DS-02`,
  `D-007`) and run `mise run questions` to turn them into links.
- For a paper the user has read or wants to review, use the `paper-review` skill
  (`/paper`): it writes the note in `docs/literature/`. BibTeX stays in the note;
  copy it to `thesis/bibliography.bib` only when the thesis cites the paper.
  Never hand-edit `docs/literature/README.md`; run `mise run lit`.
- After drafting or editing any `.tex` file, format it: `mise run fmt`.
  (tex-fmt prints pre-existing "negative indent" warnings for
  `thesis/Setup/Settings.tex`; ignore them.)
- Quick compile check: `mise run build` (or `build:thesis` / `build:plan`).
  latexmk re-runs biber automatically when citations change.
- Before finishing: `mise run fmt:check`, `mise run spell`; optionally
  `mise run lint` (pre-existing template warnings are expected). If `docs/`
  changed: `mise run questions:check`; if `docs/literature/` changed: `mise run lit:check`.
- If a task fails, read the `latexmk`/`chktex`/`typos` output, fix the file
  that was modified, and re-run the task.
- Do not commit build output (`*/build/`); it is gitignored.
