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

## Editing

Open this folder in VS Code with the
[LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
extension (recommended in `.vscode/extensions.json`). `.vscode/settings.json`
configures it to build with the same `latexmk -xelatex` recipe used by the
`mise run build` task, output to `build/`, build on save, and preview the PDF
in an editor tab.

## Structure

- `main.tex` — document entry point, `\input`s everything else.
- `Setup/` — preamble, packages, and document-wide settings
  (`Statics.tex` has thesis metadata: title, author, department, etc. — edit
  this first).
- `Frontmatter/` — title page, copyright, approval, abstract, acknowledgements.
- `Chapters/` — main content chapters.
- `Backmatter/` — appendix and back page.
- `Pictures/` — images and DTU logos used by the front/back pages.
- `bibliography.bib` — references, compiled with biber/biblatex.
- `TEMPLATE_README.md` — original template readme from DTU, kept for reference.

## Agent conventions

- After drafting or editing any `.tex` file, format it: `mise run fmt`.
- For a quick compile check: `mise run build`.
- If citations or the bibliography changed, still just use `mise run build`
  — `latexmk` re-runs biber automatically as needed.
- To check for typographic/LaTeX issues: `mise run lint`.
- If a task fails, read the `latexmk`/`chktex` output, fix the LaTeX in the
  file that was modified, and re-run the task.
