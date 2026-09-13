# Thesis Paper

This repository contains the LaTeX source for a master thesis, based on the
[DTU Thesis template](https://gitlab.gbar.dtu.dk/latex/dtutemplates/-/tree/master/templates/Thesis).
Writing is augmented with AI/agentic tooling, so this document exists to
orient an agent (or a human) quickly.

## Toolchain

- **LaTeX engine:** XeLaTeX, via a full [MacTeX](https://tug.org/mactex/)
  installation (installed manually, not managed by mise). The template
  requires `fontspec`/`\setmainfont{Arial}`, which needs XeLaTeX rather than
  pdfLaTeX.
- **Build orchestration:** `latexmk`, configured via `.latexmkrc`
  (`$pdf_mode = 5` for XeLaTeX, biber as the bibliography backend, output to
  `build/`).
- **Bibliography:** `biblatex` + `biber` (not classic bibtex).
- **Linting:** `chktex`, bundled with MacTeX.
- **Formatting:** [`tex-fmt`](https://github.com/WGUNDERWOOD/tex-fmt),
  pinned and installed via [mise](https://mise.jdx.dev/).

`xelatex`, `latexmk`, `biber`, and `chktex` all come from MacTeX and are
expected to already be on `PATH`. mise only manages `tex-fmt`, since it's the
one tool without a MacTeX equivalent.

## mise tasks

Run with `mise run <task>`:

| Task      | What it does                                                      |
| --------- | ------------------------------------------------------------------ |
| `doctor`  | Verifies `xelatex`, `latexmk`, `biber`, `chktex` are on `PATH`.     |
| `build`   | Compiles `main.tex` with XeLaTeX + biber via `latexmk` (one shot).  |
| `watch`   | Continuous rebuild on file changes (`latexmk -pvc`), for live preview. |
| `lint`    | Runs `chktex` over all `.tex` files (typography / LaTeX warnings).  |
| `fmt`     | Formats all `.tex` files in place with `tex-fmt`.                   |
| `clean`   | Removes build artifacts (`latexmk -C`).                             |
| `rebuild` | `clean` then `build`.                                               |

Output PDF and intermediate files go to `build/` (gitignored).

## Structure

- `main.tex` — document entry point (kept at repo root), `\input`s everything
  else from `thesis/`.
- `thesis/` — all LaTeX source for the thesis document itself:
  - `Setup/` — preamble, packages, and document-wide settings
    (`Statics.tex` has thesis metadata: title, author, department, etc. —
    edit this first).
  - `Frontmatter/` — title page, copyright, approval, abstract,
    acknowledgements.
  - `Chapters/` — main content chapters.
  - `Backmatter/` — appendix and back page.
  - `Pictures/` — images and DTU logos used by the front/back pages.
  - `bibliography.bib` — references, compiled with biber/biblatex.
  - `TEMPLATE_README.md` — original template readme from DTU, kept for
    reference.

Keeping all thesis LaTeX content under `thesis/` (rather than scattered at
the repo root) leaves room for other top-level project areas, e.g. a future
agentic literature-review workflow, without mixing concerns.

## Agent conventions

- After drafting or editing any `.tex` file, format it: `mise run fmt`.
- For a quick compile check: `mise run build`.
- If citations or the bibliography changed, still just use `mise run build`
  — `latexmk` re-runs biber automatically as needed.
- To check for typographic/LaTeX issues: `mise run lint`.
- If a task fails, read the `latexmk`/`chktex` output, fix the LaTeX in the
  file that was modified, and re-run the task.
