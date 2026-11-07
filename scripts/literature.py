"""Validate the literature notes in docs/literature/ and generate the central index.

Each paper has a note docs/literature/<key>.md with YAML front matter (see
docs/literature/_template.md). `skipped.md` lists papers that were looked at and
rejected, as table rows whose first cell is a paper ID (`arXiv:...`, `DOI:...`, `S2:...`).

`generate` writes docs/literature/README.md:
  - reviewed papers by relevance, with the thesis questions they inform,
  - papers in progress (queued or being read),
  - the reading queue: `candidates` from all notes, de-duplicated, minus papers that
    already have a note or are skipped, ranked by reading priority (the highest among the
    notes pointing to it), then by how many notes point to them,
  - a link to the skipped list.

`check` fails if a note is invalid or the index is stale.

Usage:
    uv run scripts/literature.py generate
    uv run scripts/literature.py check
    uv run scripts/literature.py queue      # print the reading queue
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LIT_DIR = ROOT / "docs" / "literature"
INDEX_FILE = LIT_DIR / "README.md"
SKIPPED_FILE = LIT_DIR / "skipped.md"
QUESTIONS_DIR = ROOT / "docs" / "questions"

STATUSES = ["queued", "reading", "reviewed"]
RELEVANCE = ["core", "high", "medium", "low"]
DEPTHS = ["skim", "full"]
VIAS = ["cites", "refs", "recs"]
PRIORITIES = ["very high", "high", "medium", "low"]  # reading priority, most urgent first
REQUIRED = [
    "key", "title", "authors", "year", "venue", "url", "pdf", "arxiv", "doi", "s2_id",
    "status", "relevance", "read_depth", "informs", "themes", "added", "reviewed",
    "candidates", "bibtex",
]
SECTIONS = [
    "TL;DR", "Problem and contribution", "Method", "Key results", "Limitations",
    "Relevance to the thesis", "Citable claims", "My notes", "Open doubts",
]
REVIEWED_NEEDS_CONTENT = ["TL;DR", "Relevance to the thesis"]


@dataclass
class Note:
    path: Path
    meta: dict
    body: str

    @property
    def key(self) -> str:
        return str(self.meta["key"])

    @property
    def rel_index(self) -> int:
        r = self.meta.get("relevance")
        return RELEVANCE.index(r) if r in RELEVANCE else len(RELEVANCE)


@dataclass
class Candidate:
    id: str
    title: str
    pointers: list[tuple[str, str, str]] = field(default_factory=list)  # (note key, via, why)
    best_rel: int = len(RELEVANCE)
    prio: int = len(PRIORITIES)

    @property
    def priority(self) -> str:
        return PRIORITIES[self.prio] if self.prio < len(PRIORITIES) else "–"


def norm_id(raw: str) -> str:
    """Canonical form of a paper ID, for comparing candidates with notes and skipped papers."""
    raw = str(raw or "").strip().lower()
    raw = re.sub(r"[?#].*$", "", raw)
    raw = re.sub(r"^https?://(www\.|export\.)?(arxiv|alphaxiv)\.org/(abs|pdf|html|overview)/", "arxiv:", raw)
    raw = re.sub(r"^https?://(dx\.)?doi\.org/", "doi:", raw)
    raw = re.sub(r"\.pdf$", "", raw)
    raw = re.sub(r"^doi:10\.48550/arxiv\.", "arxiv:", raw)
    raw = re.sub(r"^10\.48550/arxiv\.", "arxiv:", raw)
    if re.match(r"^\d{4}\.\d{4,5}", raw):
        raw = "arxiv:" + raw
    if re.match(r"^10\.\d{4,9}/", raw):
        raw = "doi:" + raw
    raw = re.sub(r"^(arxiv:.+?)v\d+$", r"\1", raw)
    return raw


def note_ids(meta: dict) -> set[str]:
    ids = set()
    if meta.get("arxiv"):
        ids.add(norm_id(f"arxiv:{meta['arxiv']}"))
    if meta.get("doi"):
        ids.add(norm_id(f"doi:{meta['doi']}"))
    if meta.get("s2_id"):
        ids.add(norm_id(f"s2:{meta['s2_id']}"))
    return ids


def question_files() -> dict[str, Path]:
    files = {}
    for path in QUESTIONS_DIR.glob("*.md"):
        m = re.match(r"^([A-Z]{2,3}-\d{2})-", path.name)
        if m:
            files[m.group(1)] = path
    return files


def parse_note(path: Path, errors: list[str]) -> Note | None:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        errors.append(f"{path.name}: missing YAML front matter")
        return None
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{path.name}: invalid YAML front matter: {exc}")
        return None
    missing = [k for k in REQUIRED if k not in meta]
    if missing:
        errors.append(f"{path.name}: missing keys {missing}")
        return None
    return Note(path, meta, m.group(2))


def section(body: str, name: str) -> str | None:
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", body, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else None


def balanced(text: str) -> bool:
    depth = 0
    for ch in re.sub(r"\\[{}]", "", text):
        depth += (ch == "{") - (ch == "}")
        if depth < 0:
            return False
    return depth == 0


def template_section_texts() -> dict[str, str]:
    path = LIT_DIR / "_template.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return {name: section(text, name) or "" for name in SECTIONS}


def validate(note: Note, questions: dict[str, Path], errors: list[str]) -> None:
    n, meta = note.path.name, note.meta
    if note.path.stem != note.key:
        errors.append(f"{n}: key '{note.key}' must equal the file name")
    if not re.match(r"^[a-z0-9]+$", note.key):
        errors.append(f"{n}: key must be lowercase letters and digits only")
    if meta["status"] not in STATUSES:
        errors.append(f"{n}: status '{meta['status']}' not in {STATUSES}")
    if meta["relevance"] is not None and meta["relevance"] not in RELEVANCE:
        errors.append(f"{n}: relevance '{meta['relevance']}' not in {RELEVANCE}")
    if meta["read_depth"] is not None and meta["read_depth"] not in DEPTHS:
        errors.append(f"{n}: read_depth '{meta['read_depth']}' not in {DEPTHS}")
    for list_key in ("authors", "informs", "themes", "candidates"):
        if not isinstance(meta[list_key], list):
            errors.append(f"{n}: {list_key} must be a list")
    for qid in meta["informs"] if isinstance(meta["informs"], list) else []:
        if qid not in questions:
            errors.append(f"{n}: informs unknown question {qid}")
    for str_key in ("title", "venue", "url", "pdf", "arxiv", "doi", "s2_id", "code", "data"):
        if not isinstance(meta[str_key], str):
            errors.append(f"{n}: {str_key} must be a quoted string (found {type(meta[str_key]).__name__}: {meta[str_key]!r})")
    if not isinstance(meta["year"], int) or isinstance(meta["year"], bool):
        errors.append(f"{n}: year must be an integer")
    if not meta["title"]:
        errors.append(f"{n}: empty title")
    if not (meta["url"] or meta["doi"] or meta["arxiv"]):
        errors.append(f"{n}: give at least one of url, doi, arxiv")
    bib = str(meta["bibtex"] or "")
    bm = re.match(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", bib)
    if not bm:
        errors.append(f"{n}: bibtex is missing or not a BibTeX entry")
    elif bm.group(1) != note.key:
        errors.append(f"{n}: BibTeX key '{bm.group(1)}' must equal the note key '{note.key}'")
    elif not balanced(bib) or not re.search(r"\btitle\s*=", bib, re.IGNORECASE):
        errors.append(f"{n}: BibTeX has unbalanced braces or no title field")

    for i, cand in enumerate(meta["candidates"] if isinstance(meta["candidates"], list) else []):
        if not isinstance(cand, dict) or not cand.get("id") or not cand.get("title"):
            errors.append(f"{n}: candidates[{i}] needs id and title")
            continue
        if cand.get("via") not in VIAS:
            errors.append(f"{n}: candidates[{i}].via must be one of {VIAS}")
        if cand.get("priority") not in PRIORITIES:
            errors.append(f"{n}: candidates[{i}].priority must be one of {PRIORITIES}")
        if cand.get("scout_priority") is not None and cand["scout_priority"] not in PRIORITIES:
            errors.append(f"{n}: candidates[{i}].scout_priority must be one of {PRIORITIES}")

    for name in SECTIONS:
        if section(note.body, name) is None:
            errors.append(f"{n}: missing section '## {name}'")
    if meta["status"] == "reviewed":
        if meta["relevance"] is None:
            errors.append(f"{n}: reviewed notes need a relevance")
        if not meta["reviewed"]:
            errors.append(f"{n}: reviewed notes need a reviewed date")
        template_sections = template_section_texts()
        for name in REVIEWED_NEEDS_CONTENT:
            content = section(note.body, name)
            if not content:
                errors.append(f"{n}: reviewed note has an empty '## {name}' section")
            elif content == template_sections.get(name):
                errors.append(f"{n}: reviewed note still has the template text in '## {name}'")


def load(errors: list[str]) -> list[Note]:
    notes: list[Note] = []
    seen: dict[str, Path] = {}
    for path in sorted(LIT_DIR.glob("*.md")):
        if path.name in (INDEX_FILE.name, SKIPPED_FILE.name) or path.name.startswith("_"):
            continue
        note = parse_note(path, errors)
        if note is None:
            continue
        if note.key in seen:
            errors.append(f"{path.name}: duplicate key {note.key}")
            continue
        seen[note.key] = path
        notes.append(note)
    questions = question_files()
    for note in notes:
        validate(note, questions, errors)
    owner: dict[str, str] = {}
    for note in notes:
        for pid in note_ids(note.meta):
            if pid in owner and owner[pid] != note.key:
                errors.append(f"{note.path.name}: same paper ({pid}) as {owner[pid]}.md; keep one note")
            owner.setdefault(pid, note.key)
    return notes


ID_START_RE = re.compile(r"^((arxiv|doi|s2):\S|https?://|10\.\d{4}|\d{4}\.\d{4})", re.IGNORECASE)


def load_skipped(errors: list[str]) -> dict[str, str]:
    """Map normalised ID -> reason, from the table rows of skipped.md."""
    skipped: dict[str, str] = {}
    if not SKIPPED_FILE.exists():
        return skipped
    for n, line in enumerate(SKIPPED_FILE.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        first = re.sub(r"^\[([^\]]*)\]\([^)]*\)$", r"\1", cells[0]).strip("`").strip()
        if first.lower() == "id" or re.fullmatch(r"[-: ]*", first):
            continue
        if not ID_START_RE.match(first):
            errors.append(f"skipped.md:{n}: first cell '{first}' is not a paper ID (use arXiv:..., DOI:... or S2:...)")
            continue
        skipped[norm_id(first)] = cells[-1].replace("\\|", "|") if len(cells) > 1 else ""
    return skipped


def build_queue(notes: list[Note], skipped: dict[str, str]) -> list[Candidate]:
    known: set[str] = set()
    for note in notes:
        known |= note_ids(note.meta)
    queue: dict[str, Candidate] = {}
    for note in notes:
        for cand in note.meta["candidates"] or []:
            if not isinstance(cand, dict) or not cand.get("id"):
                continue
            cid = norm_id(cand["id"])
            if cid in known or cid in skipped:
                continue
            c = queue.setdefault(cid, Candidate(id=str(cand["id"]), title=str(cand.get("title", ""))))
            c.pointers.append((note.key, str(cand.get("via", "")), str(cand.get("why", ""))))
            c.best_rel = min(c.best_rel, note.rel_index)
            if cand.get("priority") in PRIORITIES:
                c.prio = min(c.prio, PRIORITIES.index(cand["priority"]))
    return sorted(queue.values(), key=lambda c: (c.prio, -len({p[0] for p in c.pointers}), c.best_rel, c.title.lower()))


def cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def qlinks(ids: list[str], questions: dict[str, Path]) -> str:
    out = []
    for qid in ids:
        if qid in questions:
            href = Path(os.path.relpath(questions[qid], LIT_DIR)).as_posix()
            out.append(f"[{qid}]({href})")
    return ", ".join(out) or "–"


def first_author(note: Note) -> str:
    authors = note.meta["authors"] or []
    if not authors:
        return ""
    return str(authors[0]).split()[-1] + (" et al." if len(authors) > 1 else "")


def render(notes: list[Note], skipped: dict[str, str]) -> str:
    questions = question_files()
    out = [
        "# Literature notes",
        "",
        "Generated by `scripts/literature.py` (`mise run lit`); do not edit by hand. One note per",
        "paper in this folder, created with `/paper <id>` (see the `paper-review` skill). The",
        "curated overview of related work by theme stays in [`../related-work.md`](../related-work.md).",
        "",
    ]
    reviewed = sorted((n for n in notes if n.meta["status"] == "reviewed"), key=lambda n: (n.rel_index, n.key))
    out += [f"## Reviewed ({len(reviewed)})", ""]
    if reviewed:
        out += ["| Paper | Relevance | Depth | Informs | Themes | Reviewed |", "| --- | --- | --- | --- | --- | --- |"]
        for n in reviewed:
            m = n.meta
            title = f"[{cell(m['title'])}]({n.path.name}) ({first_author(n)}, {m['year']})"
            out.append(
                f"| {title} | {m['relevance']} | {m['read_depth'] or '–'} | {qlinks(m['informs'], questions)} "
                f"| {cell(', '.join(m['themes'])) or '–'} | {m['reviewed']} |"
            )
    else:
        out.append("_No paper has been reviewed yet._")

    active = sorted((n for n in notes if n.meta["status"] != "reviewed"), key=lambda n: (n.meta["status"], str(n.meta["added"]), n.key))
    out += ["", f"## In progress ({len(active)})", ""]
    if active:
        out += ["| Paper | Status | Added |", "| --- | --- | --- |"]
        for n in active:
            out.append(f"| [{cell(n.meta['title'])}]({n.path.name}) ({first_author(n)}, {n.meta['year']}) | {n.meta['status']} | {n.meta['added']} |")
    else:
        out.append("_Nothing in progress._")

    queue = build_queue(notes, skipped)
    out += [
        "",
        f"## Reading queue ({len(queue)})",
        "",
        "Candidates suggested by the notes above, not yet read or skipped. Ranked by reading priority",
        "(very high, high, medium, low), then by how many notes point to them, then by the relevance",
        "of those notes. Start a note with `/paper <id>`;",
        "reject one by adding a row to [`skipped.md`](skipped.md).",
        "",
    ]
    if queue:
        out += ["| Priority | Paper | ID | Pointed to by | Why |", "| --- | --- | --- | --- | --- |"]
        for c in queue:
            by = ", ".join(sorted({f"[{k}]({k}.md)" for k, _, _ in c.pointers}))
            why = "; ".join(dict.fromkeys(w for _, _, w in c.pointers if w))
            out.append(f"| {c.priority} | {cell(c.title)} | `{c.id}` | {by} | {cell(why) or '–'} |")
    else:
        out.append("_The queue is empty._")

    out += ["", f"## Skipped ({len(skipped)})", "", "See [`skipped.md`](skipped.md).", ""]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["generate", "check", "queue"])
    args = parser.parse_args()

    errors: list[str] = []
    notes = load(errors)
    skipped = load_skipped(errors)
    if errors:
        print("Literature notes have errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    if args.command == "queue":
        queue = build_queue(notes, skipped)
        for c in queue:
            n = len({p[0] for p in c.pointers})
            why = "; ".join(dict.fromkeys(w for _, _, w in c.pointers if w))
            print(f"{c.priority:9} {c.id:28} [{n} note{'s' if n != 1 else ''}] {c.title}" + (f" - {why}" if why else ""))
        if not queue:
            print("The reading queue is empty.")
        return 0

    content = render(notes, skipped)
    current = INDEX_FILE.read_text(encoding="utf-8") if INDEX_FILE.exists() else None
    if args.command == "generate":
        if current != content:
            INDEX_FILE.write_text(content, encoding="utf-8")
            print(f"Updated {INDEX_FILE.relative_to(ROOT)}")
        print(f"OK: {len(notes)} notes, index up to date")
        return 0
    if current != content:
        print("Out of date (run `mise run lit`):", file=sys.stderr)
        print(f"  - {INDEX_FILE.relative_to(ROOT)}", file=sys.stderr)
        return 1
    print(f"OK: {len(notes)} notes, index up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
