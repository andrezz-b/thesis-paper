"""Look up papers, BibTeX and citation links for the literature notes in docs/literature/.

Data comes from the Semantic Scholar Graph API (no key needed, but throttled; set
S2_API_KEY for a higher rate limit), DBLP and doi.org. Responses are cached in
.cache/papers/ for a week. Output is compact Markdown meant to be read by an agent.

A paper ID can be an arXiv ID (`2507.08107`, `arXiv:2507.08107`, an arxiv.org URL),
a DOI (`10.1145/3477495.3531753`, `DOI:...`, a doi.org URL), a Semantic Scholar ID
(`S2:<40 hex chars>` or the bare hash) or any other URL known to Semantic Scholar.

Usage:
    uv run scripts/papers.py meta   <id>                 # title, authors, venue, links, abstract
    uv run scripts/papers.py bibtex <id>                 # BibTeX with a key like walter2025grasp
    uv run scripts/papers.py refs   <id> [--top N]       # papers this paper cites
    uv run scripts/papers.py cites  <id> [--top N]       # papers citing it, with citation sentences
    uv run scripts/papers.py recs   <id> [--top N]       # Semantic Scholar recommendations
    uv run scripts/papers.py stub   <id>                 # create docs/literature/<key>.md (queued)

`refs`, `cites` and `recs` accept `--abstracts`, `--sort influence|year|citations` and
`--json`. `stub` never overwrites an existing note.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIT_DIR = ROOT / "docs" / "literature"
TEMPLATE = LIT_DIR / "_template.md"
CACHE_DIR = ROOT / ".cache" / "papers"
CACHE_TTL = 7 * 24 * 3600

S2 = "https://api.semanticscholar.org/graph/v1"
S2_RECS = "https://api.semanticscholar.org/recommendations/v1"
UA = "thesis-paper-tools/0.1 (literature notes; mailto:none)"

PAPER_FIELDS = (
    "title,authors,year,venue,publicationVenue,publicationDate,externalIds,"
    "abstract,citationCount,influentialCitationCount,openAccessPdf,tldr,url"
)
LIST_FIELDS = "title,authors,year,venue,externalIds,citationCount,abstract,openAccessPdf"
STOPWORDS = {"a", "an", "the", "on", "of", "for", "and", "in", "to", "towards", "toward", "with", "is", "are"}


class PaperError(Exception):
    pass


def fetch(url: str, headers: dict[str, str] | None = None, *, cache: bool = True, tries: int = 6) -> str:
    key = hashlib.sha256((url + json.dumps(headers or {}, sort_keys=True)).encode()).hexdigest()
    cache_file = CACHE_DIR / f"{key}.txt"
    if cache and cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL:
        return cache_file.read_text(encoding="utf-8")

    req_headers = {"User-Agent": UA, **(headers or {})}
    if "semanticscholar.org" in url and os.environ.get("S2_API_KEY"):
        req_headers["x-api-key"] = os.environ["S2_API_KEY"]

    delay = 3.0
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=req_headers), timeout=30) as resp:
                text = resp.read().decode("utf-8", errors="replace")
            break
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                wait = float(exc.headers.get("Retry-After") or delay)
                print(f"  (HTTP {exc.code}, retrying in {wait:.0f}s)", file=sys.stderr)
                time.sleep(wait)
                delay *= 1.7
                continue
            raise PaperError(f"HTTP {exc.code} for {url}") from exc
        except urllib.error.URLError as exc:
            raise PaperError(f"cannot reach {url}: {exc.reason}") from exc
    else:
        raise PaperError(f"giving up on {url}")

    if cache:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(text, encoding="utf-8")
    return text


def get_json(url: str) -> dict:
    return json.loads(fetch(url))


def normalise_id(raw: str) -> str:
    """Map user input to a Semantic Scholar paper identifier."""
    raw = raw.strip()
    m = re.match(r"^https?://(?:www\.)?arxiv\.org/(?:abs|pdf|html)/([^?#\s]+?)(?:\.pdf)?(?:v\d+)?/?$", raw)
    if m:
        return f"ARXIV:{m.group(1)}"
    m = re.match(r"^https?://(?:dx\.)?doi\.org/(.+)$", raw)
    if m:
        return f"DOI:{urllib.parse.unquote(m.group(1))}"
    if re.match(r"^https?://", raw):
        return f"URL:{raw}"
    m = re.match(r"^(?:arxiv:)?(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?$", raw, re.IGNORECASE)
    if m:
        return f"ARXIV:{m.group(1)}"
    m = re.match(r"^(?:doi:)?(10\.\d{4,9}/\S+)$", raw, re.IGNORECASE)
    if m:
        return f"DOI:{m.group(1)}"
    m = re.match(r"^(?:s2:)?([0-9a-f]{40})$", raw, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    return raw


def paper(pid: str) -> dict:
    ident = urllib.parse.quote(normalise_id(pid), safe=":/")
    try:
        return get_json(f"{S2}/paper/{ident}?fields={PAPER_FIELDS}")
    except PaperError as exc:
        raise PaperError(f"{exc}\nSemantic Scholar does not know '{pid}' (try another ID form, e.g. DOI:)") from exc


def ascii_lower(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", text.lower())


def cite_key(p: dict) -> str:
    authors = p.get("authors") or []
    last = ascii_lower(authors[0]["name"].split()[-1]) if authors else "anon"
    words = [ascii_lower(w) for w in re.split(r"[\s:\-]+", p.get("title") or "")]
    first = next((w for w in words if w and w not in STOPWORDS), "paper")
    return f"{last}{p.get('year') or 'xxxx'}{first}"


def short_id(p: dict) -> str:
    ext = p.get("externalIds") or {}
    if ext.get("ArXiv"):
        return f"arXiv:{ext['ArXiv']}"
    if ext.get("DOI"):
        return f"DOI:{ext['DOI']}"
    return f"S2:{p.get('paperId', '?')}"


def venue_of(p: dict) -> str:
    pv = p.get("publicationVenue") or {}
    return p.get("venue") or pv.get("name") or ""


def public_url(p: dict) -> str:
    ext = p.get("externalIds") or {}
    if ext.get("ArXiv"):
        return f"https://arxiv.org/abs/{ext['ArXiv']}"
    if ext.get("DOI"):
        return f"https://doi.org/{ext['DOI']}"
    return p.get("url") or ""


def rekey(bib: str, key: str) -> str:
    return re.sub(r"^(\s*@\w+\s*\{)[^,]+,", lambda m: f"{m.group(1)}{key},", bib.strip(), count=1)


def prettify(bib: str) -> str:
    """doi.org returns BibTeX on one line; put one field per line."""
    bib = bib.strip()
    if "\n" in bib:
        return bib
    head, _, rest = bib.partition(",")
    rest = rest.rstrip().removesuffix("}").strip()
    fields = re.split(r",\s*(?=\w+\s*=)", rest)
    return head + ",\n" + ",\n".join(f"  {f.strip()}" for f in fields) + "\n}"


def generated_bibtex(p: dict, key: str) -> str:
    ext = p.get("externalIds") or {}
    authors = " and ".join(a["name"] for a in p.get("authors") or [])
    fields = [("title", "{" + (p.get("title") or "") + "}"), ("author", authors), ("year", str(p.get("year") or ""))]
    if ext.get("ArXiv"):
        fields += [("eprint", ext["ArXiv"]), ("archiveprefix", "arXiv")]
    if ext.get("DOI"):
        fields.append(("doi", ext["DOI"]))
    if public_url(p):
        fields.append(("url", public_url(p)))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@misc{{{key},\n{body}\n}}"


def bibtex(p: dict) -> tuple[str, str]:
    """Return (bibtex, source). Prefers DBLP, then DOI content negotiation, then generated."""
    key = cite_key(p)
    ext = p.get("externalIds") or {}
    if ext.get("DBLP"):
        try:
            bib = fetch(f"https://dblp.org/rec/{ext['DBLP']}.bib", cache=False, tries=1)
            if bib.strip().startswith("@"):
                return rekey(bib, key), "DBLP"
        except PaperError:
            pass
    doi = ext.get("DOI")
    if doi and not doi.lower().startswith("10.48550/arxiv"):
        try:
            bib = fetch(f"https://doi.org/{urllib.parse.quote(doi)}", {"Accept": "application/x-bibtex"}, tries=2)
            if bib.strip().startswith("@"):
                return prettify(rekey(bib, key)), "doi.org"
        except PaperError:
            pass
    return generated_bibtex(p, key), "generated from Semantic Scholar metadata (check it)"


def authors_line(p: dict, limit: int = 4) -> str:
    names = [a["name"] for a in p.get("authors") or []]
    return ", ".join(names[:limit]) + (" et al." if len(names) > limit else "")


def trim(text: str, n: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def cmd_meta(args: argparse.Namespace) -> int:
    p = paper(args.id)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    ext = p.get("externalIds") or {}
    oa = (p.get("openAccessPdf") or {}).get("url")
    print(f"# {p.get('title')}")
    print(f"- key: {cite_key(p)}")
    print(f"- authors: {', '.join(a['name'] for a in p.get('authors') or [])}")
    print(f"- year: {p.get('year')}  venue: {venue_of(p) or '(none listed; probably preprint)'}")
    print(f"- ids: arXiv={ext.get('ArXiv', '-')}  DOI={ext.get('DOI', '-')}  DBLP={ext.get('DBLP', '-')}  S2={p.get('paperId')}")
    print(f"- url: {public_url(p)}")
    print(f"- open-access pdf: {oa or '(none found)'}")
    print(f"- citations: {p.get('citationCount')} (influential: {p.get('influentialCitationCount')})")
    if (p.get("tldr") or {}).get("text"):
        print(f"- S2 tldr: {p['tldr']['text']}")
    print(f"\n{p.get('abstract') or '(no abstract)'}")
    return 0


def cmd_bibtex(args: argparse.Namespace) -> int:
    bib, source = bibtex(paper(args.id))
    print(bib)
    print(f"% source: {source}", file=sys.stderr)
    return 0


def sort_entries(entries: list[dict], mode: str) -> list[dict]:
    def paper_of(e: dict) -> dict:
        return e.get("citingPaper") or e.get("citedPaper") or e

    if mode == "year":
        return sorted(entries, key=lambda e: (paper_of(e).get("year") or 0, paper_of(e).get("citationCount") or 0), reverse=True)
    if mode == "citations":
        return sorted(entries, key=lambda e: paper_of(e).get("citationCount") or 0, reverse=True)
    return sorted(
        entries,
        key=lambda e: (
            bool(e.get("isInfluential")),
            len(e.get("contexts") or []),
            paper_of(e).get("citationCount") or 0,
        ),
        reverse=True,
    )


def print_entries(entries: list[dict], args: argparse.Namespace) -> None:
    for e in entries:
        p = e.get("citingPaper") or e.get("citedPaper") or e
        if not p.get("title") or not p.get("paperId"):
            continue
        venue = venue_of(p)
        flags = []
        if e.get("isInfluential"):
            flags.append("influential")
        if e.get("intents"):
            flags.append("intent: " + "/".join(e["intents"]))
        meta = [f"{p.get('year') or '?'}"] + ([venue] if venue else []) + [f"{p.get('citationCount') or 0} cites"] + flags
        print(f"- **{p['title']}** ({authors_line(p, 3)}; {', '.join(meta)})  `{short_id(p)}`")
        for ctx in (e.get("contexts") or [])[:2]:
            print(f"  > {trim(ctx, 320)}")
        if args.abstracts and p.get("abstract"):
            print(f"  abstract: {trim(p['abstract'], 500)}")


def cmd_links(args: argparse.Namespace) -> int:
    ident = urllib.parse.quote(normalise_id(args.id), safe=":/")
    kind = args.command
    if kind == "recs":
        url = f"{S2_RECS}/papers/forpaper/{ident}?fields={LIST_FIELDS}&limit={min(max(args.top, 1), 100)}"
        entries = get_json(url).get("recommendedPapers", [])
    else:
        sub = "citingPaper" if kind == "cites" else "citedPaper"
        fields = ",".join(
            ["contexts", "intents", "isInfluential"] + [f"{sub}.{f}" for f in LIST_FIELDS.split(",")]
        )
        endpoint = {"cites": "citations", "refs": "references"}[kind]
        url = f"{S2}/paper/{ident}/{endpoint}?fields={fields}&limit=500"
        entries = get_json(url).get("data", [])
    if args.json:
        print(json.dumps(entries[: args.top], indent=2))
        return 0
    total = len(entries)
    entries = sort_entries(entries, args.sort)[: args.top]
    label = {"cites": "cited by (newer papers citing this one)", "refs": "references (papers this one cites)", "recs": "recommended"}[kind]
    print(f"## {label}: showing {len(entries)} of {total} fetched, sorted by {args.sort}\n")
    print_entries(entries, args)
    return 0


def yaml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def cmd_stub(args: argparse.Namespace) -> int:
    p = paper(args.id)
    key = cite_key(p)
    path = LIT_DIR / f"{key}.md"
    if path.exists():
        print(f"{path.relative_to(ROOT)} already exists; not overwriting", file=sys.stderr)
        return 1
    ext = p.get("externalIds") or {}
    bib, source = bibtex(p)
    oa = (p.get("openAccessPdf") or {}).get("url") or ""
    venue = venue_of(p)
    authors = ", ".join(yaml_str(a["name"]) for a in p.get("authors") or [])
    lines = [
        "---",
        f"key: {key}",
        f"title: {yaml_str(p.get('title') or '')}",
        f"authors: [{authors}]",
        f"year: {p.get('year') or 'null'}",
        f"venue: {yaml_str(venue)}",
        f"url: {yaml_str(public_url(p))}",
        f"pdf: {yaml_str(oa)}",
        f"arxiv: {yaml_str(ext.get('ArXiv', ''))}",
        f"doi: {yaml_str(ext.get('DOI', ''))}",
        f"s2_id: {yaml_str(p.get('paperId', ''))}",
        'code: ""',
        'data: ""',
        "status: queued",
        "relevance: null",
        "read_depth: null",
        "informs: []",
        "themes: []",
        f"added: {date.today().isoformat()}",
        "reviewed: null",
        "candidates: []",
        "bibtex: |",
        *[f"  {line}" for line in bib.splitlines()],
        "---",
    ]
    template = TEMPLATE.read_text(encoding="utf-8")
    body = re.sub(r"^---\n.*?\n---\n\n?", "", template, count=1, flags=re.DOTALL)
    body = body.replace("# Full paper title", f"# {p.get('title') or key}", 1)
    LIT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)} (bibtex: {source})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("meta", "bibtex", "refs", "cites", "recs", "stub"):
        sp = sub.add_parser(name)
        sp.add_argument("id")
        if name in ("meta", "refs", "cites", "recs"):
            sp.add_argument("--json", action="store_true")
        if name in ("refs", "cites", "recs"):
            sp.add_argument("--top", type=int, default=20)
            sp.add_argument("--abstracts", action="store_true")
            sp.add_argument("--sort", choices=["influence", "year", "citations"], default="influence")
    args = parser.parse_args()
    handler = {"meta": cmd_meta, "bibtex": cmd_bibtex, "stub": cmd_stub}.get(args.command, cmd_links)
    try:
        return handler(args)
    except PaperError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
