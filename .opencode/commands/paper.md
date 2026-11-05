---
description: Review a paper into a literature note (docs/literature/), or explore related papers. Usage /paper <arXiv ID | DOI | URL | PDF path> [explore]
---

Load the `paper-review` skill and follow it for this request: $ARGUMENTS

If the arguments end with `explore`, run only the "Explore related papers" step for that
paper. If they are empty, run `mise run lit:queue`, show the reading queue and ask which
paper to review.
