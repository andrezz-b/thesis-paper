"""Look up papers, BibTeX and citation links for the literature notes in docs/literature/.

Data comes from the Semantic Scholar Graph API (no key needed, but throttled; set
S2_API_KEY for a higher rate limit), the arXiv API (full author names, and metadata for
papers Semantic Scholar lacks), doi.org (BibTeX) and DBLP (often blocked by a bot check).
Responses are cached in .cache/papers/ for a week. Output is compact Markdown meant to be
read by an agent. Warnings go to stderr and must be shown to the user.

A paper ID can be an arXiv ID (`2507.08107`, `arXiv:2507.08107`, an arxiv.org URL), a DOI
(`10.1145/3477495.3531753`, `DOI:...`, a doi.org URL), a Semantic Scholar ID (`S2:<40 hex
chars>` or the bare hash) or any other URL known to Semantic Scholar.

Usage:
    uv run scripts/papers.py meta   <id>                 # title, authors, venue, links, abstract
    uv run scripts/papers.py search <title words...>     # find a paper's ID by title
    uv run scripts/papers.py bibtex <id>                 # BibTeX with a key like walter2025grasp
    uv run scripts/papers.py refs   <id> [--top N]       # papers this paper cites
    uv run scripts/papers.py cites  <id> [--top N]       # papers citing it, with citation sentences
    uv run scripts/papers.py recs   <id> [--top N]       # Semantic Scholar recommendations
    uv run scripts/papers.py stub   <id>                 # create docs/literature/<key>.md (queued)
    uv run scripts/papers.py stub --title T --authors "A; B" --year Y --url U   # no lookup (manual)

`refs`, `cites` and `recs` accept `--no-abstracts`, `--sort influence|year|citations` and
`--json`. `stub` accepts `--title --authors --year --venue --url --pdf --doi --arxiv --code
--data --bibtex-file` to override or replace looked-up values (use it when a lookup fails
or is wrong: the values must come from the paper or the user, never from memory). `stub`
never overwrites a note; if the same paper (arXiv ID, DOI or S2 ID) already has a note it
says so and changes nothing.
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
import xml.etree.ElementTree as ET
from collections.abc import Callable
from datetime import date
from email.utils import parsedate_to_datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LIT_DIR = ROOT / "docs" / "literature"
TEMPLATE = LIT_DIR / "_template.md"
CACHE_DIR = ROOT / ".cache" / "papers"
CACHE_TTL = 7 * 24 * 3600

S2 = "https://api.semanticscholar.org/graph/v1"
S2_RECS = "https://api.semanticscholar.org/recommendations/v1"
ARXIV_API = "https://export.arxiv.org/api/query"
UA = "thesis-paper-tools/0.1 (literature notes)"
ATOM = {"a": "http://www.w3.org/2005/Atom", "ax": "http://arxiv.org/schemas/atom"}
ARXIV_HOSTS = {"arxiv.org", "export.arxiv.org", "ar5iv.org", "ar5iv.labs.arxiv.org", "alphaxiv.org"}

PAPER_FIELDS = (
    "title,authors,year,venue,publicationVenue,publicationDate,externalIds,"
    "abstract,citationCount,influentialCitationCount,openAccessPdf,tldr,url"
)
LIST_FIELDS = "title,authors,year,venue,externalIds,citationCount,abstract,openAccessPdf"
SEARCH_FIELDS = "title,authors,year,venue,externalIds,citationCount"
LINK_LIMIT = 1000
STOPWORDS = {"a", "an", "the", "on", "of", "for", "and", "in", "to", "towards", "toward", "with", "is", "are"}


class PaperError(Exception):
    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def retry_after(value: str | None, default: float) -> float:
    if not value:
        return default
    try:
        return min(float(value), 60.0)
    except ValueError:
        try:
            return min(max((parsedate_to_datetime(value).timestamp() - time.time()), 1.0), 60.0)
        except (TypeError, ValueError):
            return default


def fetch(
    url: str,
    headers: dict[str, str] | None = None,
    *,
    cache: bool = True,
    tries: int = 6,
    accept: Callable[[str], bool] | None = None,
) -> str:
    """GET a URL with retries. A response is cached only if `accept` (when given) approves it."""
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
                wait = retry_after(exc.headers.get("Retry-After"), delay)
                print(f"  (HTTP {exc.code}, retrying in {wait:.0f}s)", file=sys.stderr)
                time.sleep(wait)
                delay *= 1.7
                continue
            raise PaperError(f"HTTP {exc.code} for {url}", exc.code) from exc
        except urllib.error.URLError as exc:
            raise PaperError(f"cannot reach {url}: {exc.reason}") from exc
    else:
        raise PaperError(f"giving up on {url}")

    if cache and (accept is None or accept(text)):
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(text, encoding="utf-8")
    return text


def get_json(url: str) -> dict:
    return json.loads(fetch(url))


def explain(err: PaperError, pid: str) -> str:
    if err.status == 404:
        return (
            f"'{pid}' is not in Semantic Scholar (HTTP 404). Try another ID form (DOI:..., arXiv:...) "
            "or `search <title>`, or create the note with `stub --title ... --authors ... --year ... --url ...` "
            "using values from the paper or the user. Brand-new papers are often missing for a few weeks."
        )
    return (
        f"Lookup of '{pid}' failed ({err}). This does NOT mean the paper is missing: retry later "
        "(set S2_API_KEY for a higher rate limit)."
    )


def normalise_id(raw: str) -> str:
    """Map user input to a Semantic Scholar paper identifier."""
    raw = raw.strip()
    if re.match(r"^https?://", raw, re.IGNORECASE):
        u = urllib.parse.urlparse(raw)
        host = u.netloc.lower().removeprefix("www.")
        if host in ARXIV_HOSTS:
            m = re.match(r"^/(?:abs|pdf|html|overview)/(.+?)/?$", u.path)
            if m:
                ident = re.sub(r"v\d+$", "", re.sub(r"\.pdf$", "", m.group(1)))
                return f"ARXIV:{ident}"
        if host in ("doi.org", "dx.doi.org"):
            return normalise_id("DOI:" + urllib.parse.unquote(u.path.lstrip("/")))
        return f"URL:{raw.split('#')[0]}"
    m = re.match(r"^(?:arxiv:)?(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?$", raw, re.IGNORECASE)
    if m:
        return f"ARXIV:{m.group(1)}"
    m = re.match(r"^(?:doi:)?(10\.\d{4,9}/\S+)$", raw, re.IGNORECASE)
    if m:
        doi = m.group(1)
        am = re.match(r"^10\.48550/arxiv\.(.+?)(?:v\d+)?$", doi, re.IGNORECASE)
        return f"ARXIV:{am.group(1)}" if am else f"DOI:{doi}"
    m = re.match(r"^(?:s2:)?([0-9a-f]{40})$", raw, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    return raw


def s2_get(url: str, pid: str) -> dict:
    try:
        return get_json(url)
    except PaperError as exc:
        raise PaperError(explain(exc, pid), exc.status) from exc


def s2_paper(nid: str, pid: str) -> dict:
    ident = urllib.parse.quote(nid, safe=":/")
    return s2_get(f"{S2}/paper/{ident}?fields={PAPER_FIELDS}", pid)


def entry_to_paper(e: ET.Element) -> dict:
    title = " ".join((e.findtext("a:title", "", ATOM) or "").split())
    abs_url = e.findtext("a:id", "", ATOM)
    m = re.search(r"arxiv\.org/abs/(.+?)(?:v\d+)?$", abs_url)
    ext = {"ArXiv": m.group(1)} if m else {}
    doi = e.findtext("ax:doi", "", ATOM)
    if doi:
        ext["DOI"] = doi.strip()
    published = e.findtext("a:published", "", ATOM)
    return {
        "title": title,
        "authors": [{"name": " ".join(n.text.split())} for n in e.findall("a:author/a:name", ATOM) if n.text],
        "year": int(published[:4]) if published[:4].isdigit() else None,
        "venue": " ".join((e.findtext("ax:journal_ref", "", ATOM) or "").split()),
        "externalIds": ext,
        "abstract": " ".join((e.findtext("a:summary", "", ATOM) or "").split()),
        "openAccessPdf": {"url": f"https://arxiv.org/pdf/{ext['ArXiv']}"} if "ArXiv" in ext else None,
    }


def arxiv_query(params: str) -> list[dict]:
    root = ET.fromstring(fetch(f"{ARXIV_API}?{params}"))
    papers = [entry_to_paper(e) for e in root.findall("a:entry", ATOM)]
    return [p for p in papers if p["title"] and p["title"] != "Error"]


def arxiv_paper(aid: str) -> dict:
    found = arxiv_query(f"id_list={urllib.parse.quote(aid)}&max_results=1")
    if not found:
        raise PaperError(f"arXiv has no paper {aid}", 404)
    return found[0]


def abbreviated(authors: list[dict]) -> bool:
    return any(re.match(r"^[A-Z]\.", a.get("name", "")) for a in authors)


def resolve(pid: str) -> dict:
    """Metadata from Semantic Scholar, enriched or replaced by the arXiv API. Never invents data."""
    nid = normalise_id(pid)
    s2: dict | None = None
    err: PaperError | None = None
    try:
        s2 = s2_paper(nid, pid)
    except PaperError as exc:
        err = exc
    aid = (s2.get("externalIds") or {}).get("ArXiv") if s2 else (nid[6:] if nid.startswith("ARXIV:") else None)
    ax: dict | None = None
    if aid:
        try:
            ax = arxiv_paper(aid)
        except (PaperError, ET.ParseError):
            ax = None
    if s2 is None:
        if ax is None:
            raise err or PaperError(f"cannot resolve '{pid}'")
        warn(f"Semantic Scholar unavailable for '{pid}' ({err}); metadata comes from the arXiv API only, "
             "so refs/cites/recs will not work yet.")
        return ax
    if ax and abbreviated(s2.get("authors") or []):
        if len(ax["authors"]) == len(s2.get("authors") or []):
            s2["authors"] = ax["authors"]
        else:
            warn("Semantic Scholar author names look abbreviated and the arXiv author list differs; check the authors.")
    return s2


def ascii_lower(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", text.lower())


def last_name(name: str) -> str:
    name = name.strip()
    if "," in name:
        return ascii_lower(name.split(",")[0])
    parts = name.split()
    return ascii_lower(parts[-1]) if parts else ""


def cite_key(p: dict) -> str:
    names = [a.get("name", "") for a in p.get("authors") or [] if a.get("name", "").strip()]
    last = (last_name(names[0]) if names else "") or "anon"
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
    if p.get("_url"):
        return p["_url"]
    if ext.get("ArXiv"):
        return f"https://arxiv.org/abs/{ext['ArXiv']}"
    if ext.get("DOI"):
        return f"https://doi.org/{ext['DOI']}"
    return p.get("url") or ""


# ---- BibTeX --------------------------------------------------------------------------


def balanced(text: str) -> bool:
    depth = 0
    for ch in re.sub(r"\\[{}]", "", text):
        depth += (ch == "{") - (ch == "}")
        if depth < 0:
            return False
    return depth == 0


def bib_ok(bib: str) -> bool:
    bib = bib.strip()
    return bib.startswith("@") and balanced(bib) and re.search(r"\btitle\s*=", bib, re.IGNORECASE) is not None


def rekey(bib: str, key: str) -> str:
    return re.sub(r"^(\s*@\w+\s*\{)[^,]+,", lambda m: f"{m.group(1)}{key},", bib.strip(), count=1)


def split_top_level(text: str) -> list[str]:
    parts, cur, depth = [], [], 0
    for ch in text:
        depth += (ch == "{") - (ch == "}")
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [x.strip() for x in parts if x.strip()]


def prettify(bib: str) -> str:
    """doi.org returns BibTeX on one line; put one field per line."""
    bib = bib.strip()
    if "\n" in bib:
        return bib
    m = re.match(r"^(@\w+\s*\{[^,]+),(.*)\}\s*$", bib, re.DOTALL)
    if not m:
        return bib
    fields = split_top_level(m.group(2))
    return m.group(1) + ",\n" + ",\n".join(f"  {f}" for f in fields) + "\n}"


def bib_field(bib: str, name: str) -> str:
    m = re.search(rf"\b{name}\s*=\s*", bib, re.IGNORECASE)
    if not m:
        return ""
    i = m.end()
    if i < len(bib) and bib[i] == "{":
        depth, j = 0, i
        while j < len(bib):
            depth += (bib[j] == "{") - (bib[j] == "}")
            if depth == 0:
                return bib[i + 1 : j]
            j += 1
        return ""
    m2 = re.match(r'"([^"]*)"', bib[i:])
    return m2.group(1) if m2 else ""


def tex_escape(text: str) -> str:
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"(?<!\\)([&%$#_])", r"\\\1", text)


def generated_bibtex(p: dict, key: str) -> str:
    ext = p.get("externalIds") or {}
    authors = " and ".join(tex_escape(a["name"]) for a in p.get("authors") or [] if a.get("name"))
    fields = [("title", "{" + tex_escape(p.get("title") or "") + "}"), ("author", authors), ("year", str(p.get("year") or ""))]
    if ext.get("ArXiv"):
        fields += [("eprint", ext["ArXiv"]), ("archiveprefix", "arXiv")]
    if ext.get("DOI"):
        fields.append(("doi", ext["DOI"]))
    if public_url(p):
        fields.append(("url", public_url(p)))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@misc{{{key},\n{body}\n}}"


def bibtex(p: dict) -> tuple[str, str]:
    """Return (bibtex, source). doi.org (also for arXiv DOIs), then DBLP, then generated."""
    key = cite_key(p)
    ext = p.get("externalIds") or {}
    doi = ext.get("DOI") or (f"10.48550/arXiv.{ext['ArXiv']}" if ext.get("ArXiv") else None)
    bib, source = "", ""
    if doi:
        try:
            got = fetch(f"https://doi.org/{urllib.parse.quote(doi)}", {"Accept": "application/x-bibtex"}, tries=2, accept=bib_ok)
            if bib_ok(got):
                bib, source = prettify(rekey(got, key)), "doi.org"
            else:
                warn(f"doi.org returned no usable BibTeX for {doi}")
        except PaperError as exc:
            warn(f"doi.org BibTeX lookup failed ({exc})")
    if not bib and ext.get("DBLP"):
        try:
            got = fetch(f"https://dblp.org/rec/{ext['DBLP']}.bib", cache=False, tries=1)
            if bib_ok(got):
                bib, source = rekey(got, key), "DBLP"
            else:
                warn("DBLP did not return BibTeX (it often blocks scripts with a bot check)")
        except PaperError as exc:
            warn(f"DBLP lookup failed ({exc})")
    if not bib:
        warn("BibTeX is GENERATED from metadata (no publisher/DBLP entry found): check it, tell the user.")
        return generated_bibtex(p, key), "generated from metadata (check it)"
    a, b = ascii_lower(p.get("title") or ""), ascii_lower(bib_field(bib, "title"))
    if a and b and a != b:
        warn(f"titles differ: metadata '{p.get('title')}' vs BibTeX '{bib_field(bib, 'title')}'. Check which one the paper uses.")
    return bib, source


# ---- output --------------------------------------------------------------------------


def authors_line(p: dict, limit: int = 4) -> str:
    names = [a["name"] for a in p.get("authors") or [] if a.get("name")]
    return ", ".join(names[:limit]) + (" et al." if len(names) > limit else "")


def trim(text: str, n: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def cmd_meta(args: argparse.Namespace) -> int:
    p = resolve(args.id)
    if args.json:
        print(json.dumps(p, indent=2))
        return 0
    ext = p.get("externalIds") or {}
    oa = (p.get("openAccessPdf") or {}).get("url")
    print(f"# {p.get('title')}")
    print(f"- key: {cite_key(p)}")
    print(f"- authors: {', '.join(a['name'] for a in p.get('authors') or [])}")
    print(f"- year: {p.get('year')}  venue: {venue_of(p) or '(none listed; probably preprint)'}")
    print(f"- ids: arXiv={ext.get('ArXiv', '-')}  DOI={ext.get('DOI', '-')}  DBLP={ext.get('DBLP', '-')}  S2={p.get('paperId') or '-'}")
    print(f"- url: {public_url(p)}")
    print(f"- open-access pdf: {oa or '(none found)'}")
    if p.get("citationCount") is not None:
        print(f"- citations: {p.get('citationCount')} (influential: {p.get('influentialCitationCount')})")
    if (p.get("tldr") or {}).get("text"):
        print(f"- S2 tldr: {p['tldr']['text']}")
    print(f"\n{p.get('abstract') or '(no abstract)'}")
    return 0


def cmd_bibtex(args: argparse.Namespace) -> int:
    bib, source = bibtex(resolve(args.id))
    print(bib)
    print(f"% source: {source}", file=sys.stderr)
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    try:
        found = get_json(f"{S2}/paper/search?query={urllib.parse.quote(query)}&limit={args.top}&fields={SEARCH_FIELDS}").get("data", [])
        label = "Semantic Scholar"
    except PaperError as exc:
        warn(f"Semantic Scholar search failed ({exc}); using the arXiv API instead")
        found = arxiv_query(f"search_query=all:{urllib.parse.quote(query)}&max_results={args.top}")
        label = "arXiv"
    print(f"## search results for '{query}' ({label})\n")
    for p in found:
        if not p.get("title"):
            continue
        venue = venue_of(p)
        print(f"- **{p['title']}** ({authors_line(p, 3)}; {p.get('year') or '?'}{', ' + venue if venue else ''})  `{short_id(p)}`")
    if not found:
        print("(no results; try fewer or different words)")
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


def print_entries(entries: list[dict], abstracts: bool) -> None:
    for e in entries:
        p = e.get("citingPaper") or e.get("citedPaper") or e
        if not p.get("title") or not (p.get("paperId") or p.get("externalIds")):
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
        if abstracts and p.get("abstract"):
            print(f"  abstract: {trim(p['abstract'], 500)}")


def cmd_links(args: argparse.Namespace) -> int:
    ident = urllib.parse.quote(normalise_id(args.id), safe=":/")
    kind = args.command
    if kind == "recs":
        url = f"{S2_RECS}/papers/forpaper/{ident}?fields={LIST_FIELDS}&limit={min(max(args.top, 1), 100)}"
        entries = s2_get(url, args.id).get("recommendedPapers", [])
    else:
        sub = "citingPaper" if kind == "cites" else "citedPaper"
        fields = ",".join(["contexts", "intents", "isInfluential"] + [f"{sub}.{f}" for f in LIST_FIELDS.split(",")])
        endpoint = {"cites": "citations", "refs": "references"}[kind]
        entries = s2_get(f"{S2}/paper/{ident}/{endpoint}?fields={fields}&limit={LINK_LIMIT}", args.id).get("data", [])
    total = len(entries)
    entries = sort_entries(entries, args.sort)[: args.top]
    if args.json:
        print(json.dumps(entries, indent=2))
        return 0
    label = {"cites": "cited by (newer papers citing this one)", "refs": "references (papers this one cites)", "recs": "recommended"}[kind]
    print(f"## {label}: showing {len(entries)} of {total} fetched, sorted by {args.sort}\n")
    if kind != "recs" and total >= LINK_LIMIT:
        print(f"(only the first {LINK_LIMIT} entries are fetched; the ranking covers those only)\n")
    print_entries(entries, not args.no_abstracts)
    return 0


# ---- notes ---------------------------------------------------------------------------


def yaml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def id_set(arxiv: str, doi: str, s2_id: str) -> set[str]:
    ids = set()
    if arxiv:
        ids.add("arxiv:" + re.sub(r"v\d+$", "", str(arxiv).strip().lower()))
    if doi:
        d = str(doi).strip().lower()
        am = re.match(r"^10\.48550/arxiv\.(.+?)(?:v\d+)?$", d)
        ids.add(f"arxiv:{am.group(1)}" if am else f"doi:{d}")
    if s2_id:
        ids.add("s2:" + str(s2_id).strip().lower())
    return ids


def read_front_matter(path: Path) -> dict:
    m = re.match(r"^---\r?\n(.*?)\r?\n---", path.read_text(encoding="utf-8"), re.DOTALL)
    try:
        return (yaml.safe_load(m.group(1)) or {}) if m else {}
    except yaml.YAMLError:
        return {}


def apply_overrides(p: dict, args: argparse.Namespace) -> None:
    ext = p.setdefault("externalIds", {})
    if args.title:
        p["title"] = args.title
    if args.authors:
        p["authors"] = [{"name": a.strip()} for a in args.authors.split(";") if a.strip()]
    if args.year:
        p["year"] = args.year
    if args.venue is not None:
        p["venue"] = args.venue
    if args.url:
        p["_url"] = args.url
    if args.pdf:
        p["openAccessPdf"] = {"url": args.pdf}
    if args.doi:
        ext["DOI"] = args.doi
    if args.arxiv:
        ext["ArXiv"] = args.arxiv


def cmd_stub(args: argparse.Namespace) -> int:
    p = resolve(args.id) if args.id else {"title": "", "authors": [], "externalIds": {}}
    apply_overrides(p, args)
    ext = p.get("externalIds") or {}

    missing = []
    if not p.get("title"):
        missing.append("--title")
    if not [a for a in p.get("authors") or [] if a.get("name")]:
        missing.append("--authors")
    if not isinstance(p.get("year"), int):
        missing.append("--year")
    if not public_url(p) and not ext.get("DOI") and not ext.get("ArXiv"):
        missing.append("--url (or --doi / --arxiv)")
    if missing:
        raise PaperError(
            "cannot create the note, missing: " + ", ".join(missing) + ". Take these from the paper itself or ask the user; "
            "never fill them from memory."
        )

    ids = id_set(ext.get("ArXiv", ""), ext.get("DOI", ""), p.get("paperId", ""))
    existing = [f for f in sorted(LIT_DIR.glob("*.md")) if not f.name.startswith("_") and f.name not in ("README.md", "skipped.md")]
    for f in existing:
        fm = read_front_matter(f)
        if ids & id_set(fm.get("arxiv", ""), fm.get("doi", ""), fm.get("s2_id", "")):
            print(f"Already exists: {f.relative_to(ROOT)} (same paper); nothing changed")
            return 0

    base = cite_key(p)
    key, n = base, 0
    while (LIT_DIR / f"{key}.md").exists():
        key = base + chr(ord("a") + n)
        n += 1
        if n > 25:
            raise PaperError(f"too many notes with key {base}")
    if key != base:
        warn(f"key {base} belongs to a different paper; using {key}")
    p_key = key
    path = LIT_DIR / f"{key}.md"

    if args.bibtex_file:
        raw = Path(args.bibtex_file).read_text(encoding="utf-8")
        if not bib_ok(raw):
            raise PaperError(f"{args.bibtex_file} is not a valid BibTeX entry with balanced braces and a title")
        bib, source = rekey(raw, p_key), f"file {args.bibtex_file}"
    else:
        bib, source = bibtex(p)
        bib = rekey(bib, p_key)

    oa = (p.get("openAccessPdf") or {}).get("url") or ""
    authors = ", ".join(yaml_str(a["name"]) for a in p["authors"] if a.get("name"))
    lines = [
        "---",
        f"key: {key}",
        f"title: {yaml_str(p['title'])}",
        f"authors: [{authors}]",
        f"year: {p['year']}",
        f"venue: {yaml_str(venue_of(p))}",
        f"url: {yaml_str(public_url(p))}",
        f"pdf: {yaml_str(oa)}",
        f"arxiv: {yaml_str(ext.get('ArXiv', ''))}",
        f"doi: {yaml_str(ext.get('DOI', ''))}",
        f"s2_id: {yaml_str(p.get('paperId') or '')}",
        f"code: {yaml_str(args.code or '')}",
        f"data: {yaml_str(args.data or '')}",
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
    body = body.replace("# Full paper title", f"# {p['title']}", 1)
    LIT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")
    print(f"Created {path.relative_to(ROOT)} (bibtex: {source})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("meta", "bibtex", "refs", "cites", "recs", "stub", "search"):
        sp = sub.add_parser(name)
        if name == "search":
            sp.add_argument("query", nargs="+")
            sp.add_argument("--top", type=int, default=8)
        elif name == "stub":
            sp.add_argument("id", nargs="?")
            sp.add_argument("--title")
            sp.add_argument("--authors", help='"First Author; Second Author"')
            sp.add_argument("--year", type=int)
            sp.add_argument("--venue")
            sp.add_argument("--url")
            sp.add_argument("--pdf")
            sp.add_argument("--doi")
            sp.add_argument("--arxiv")
            sp.add_argument("--code")
            sp.add_argument("--data")
            sp.add_argument("--bibtex-file")
        else:
            sp.add_argument("id")
        if name in ("meta", "refs", "cites", "recs"):
            sp.add_argument("--json", action="store_true")
        if name in ("refs", "cites", "recs"):
            sp.add_argument("--top", type=int, default=20)
            sp.add_argument("--no-abstracts", action="store_true")
            sp.add_argument("--sort", choices=["influence", "year", "citations"], default="influence")
    args = parser.parse_args()
    handler = {"meta": cmd_meta, "bibtex": cmd_bibtex, "stub": cmd_stub, "search": cmd_search}.get(args.command, cmd_links)
    try:
        return handler(args)
    except (PaperError, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
