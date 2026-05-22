#!/usr/bin/env python3
"""Render a multi-doc site from markdown sources with shared CSS.

Copy this script + styles.css into your site folder alongside your *.md sources.
Customize the TODOs below, then run:  python3 render.py

Requires: pip install markdown-it-py
"""
from markdown_it import MarkdownIt
from pathlib import Path
import re

ROOT = Path(__file__).parent

# TODO: replace with your project's pages.
# (slug, html-title, top-nav-label)
PAGES = [
    ("index", "Overview · TODO Brand", "Overview"),
    ("page-a", "Page A · TODO Brand", "Page A"),
    ("page-b", "Page B · TODO Brand", "Page B"),
]

# TODO: customize for your domain. Token in markdown `<code>` → CSS class.
# Add or remove tokens; collapse onto the 5 visual classes in styles.css.
STATUS_TOKENS = ["PASS", "FAIL", "WARN", "OPEN", "LOCKED"]
STATUS_CLS_MAP = {
    "PASS": "evidence",
    "FAIL": "fail",
    "WARN": "alignment",
    "OPEN": "open",
    "LOCKED": "locked",
}

# TODO: brand string for meta strip + footer.
BRAND = "TODO Brand"
# TODO: footer date (ISO).
FOOTER_DATE = "2026-05-04"
# TODO: footer breadcrumb path (purely cosmetic).
FOOTER_PATH = "site / multi-doc"

md = (
    MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": False})
    .enable("table")
    .enable("strikethrough")
)


def render_status_codes(html: str) -> str:
    pattern = r'<code>(' + '|'.join(STATUS_TOKENS) + r')([^<]*?)</code>'

    def repl(m):
        token = m.group(1)
        suffix = m.group(2) or ""
        cls = STATUS_CLS_MAP.get(token, "open")
        label = (token + suffix).strip()
        return f'<span class="status {cls}">{label}</span>'

    return re.sub(pattern, repl, html)


def slugify(text: str) -> str:
    s = re.sub(r'<[^>]+>', '', text).lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return s


def add_section_numbers_and_ids(html: str):
    """Add numbered markers + ids to h2s. Returns (html, toc-list)."""
    counter = [0]
    toc = []

    def repl(m):
        counter[0] += 1
        n = counter[0]
        text = m.group(1)
        slug = slugify(text)
        toc.append((f"{n:02d}", slug, text))
        return f'<h2 id="{slug}" data-num="{n:02d}">{text}</h2>'

    return re.sub(r'<h2>(.*?)</h2>', repl, html), toc


def enhance_lede(html: str) -> str:
    """First blockquote after h1 becomes .lede paragraph."""
    return re.sub(
        r'(<h1[^>]*>.*?</h1>\s*)<blockquote>\s*<p>(.*?)</p>\s*</blockquote>',
        r'\1<p class="lede">\2</p>',
        html, count=1, flags=re.DOTALL,
    )


def render_tldr(html: str) -> str:
    """A paragraph starting with <strong>TL;DR.</strong> becomes a styled block."""
    return re.sub(
        r'<p><strong>TL;DR\.?</strong>\s*(.*?)</p>',
        lambda m: (
            '<div class="tldr">'
            '<span class="tldr-label">TL;DR</span>'
            f'<div class="tldr-body">{m.group(1).strip()}</div>'
            '</div>'
        ),
        html, flags=re.DOTALL,
    )


# TODO: customize the index card grid for your page set.
# This replaces a markdown table on the index page. The table stays as the
# source-of-truth (editable, scannable); this grid is the visual rendering.
INDEX_CARDS_HTML = """<div class="cards">
<a class="card" href="page-a.html">
<span class="num">01 · Page A</span>
<div class="card-body">
<h3>Short headline for page A <span class="card-arrow">→</span></h3>
<p class="card-aud">For: TODO audience.</p>
<p>One-sentence summary of what's on this page and its current state.</p>
</div>
</a>
<a class="card" href="page-b.html">
<span class="num">02 · Page B</span>
<div class="card-body">
<h3>Short headline for page B <span class="card-arrow">→</span></h3>
<p class="card-aud">For: TODO audience.</p>
<p>One-sentence summary.</p>
</div>
</a>
</div>"""


def restructure_index_cards(html: str) -> str:
    """Replace the first markdown table on the index page with the card grid."""
    pattern = re.compile(r'<table>.*?</table>', re.DOTALL)
    return pattern.sub(INDEX_CARDS_HTML, html, count=1)


def render_toc(toc):
    if not toc:
        return ""
    items = "".join(
        f'<a href="#{slug}"><span class="toc-num">{num}</span>{text}</a>'
        for num, slug, text in toc
    )
    return f'<nav class="toc"><h4>On this page</h4>{items}</nav>'


def shell(title: str, body: str, current: str, label: str, slug: str, toc_html: str):
    nav_items = [(f"{p[0]}.html", p[2], p[0]) for p in PAGES]
    nav_html = ' · '.join(
        f'<a href="{href}"{" class=\"current\"" if pslug==current else ""}>{lbl}</a>'
        for href, lbl, pslug in nav_items
    )
    download_btn = (
        f'<a class="download-md" href="{slug}.md" download '
        f'title="Download Markdown source"><span>↓</span> download {slug}.md</a>'
    )
    sticky_download = (
        f'<div class="sticky-download">'
        f'<a href="{slug}.md" download>⬇ Download Markdown</a>'
        f'</div>'
    )
    layout_class = "layout" if toc_html else "layout layout-no-sidebar"
    sidebar = toc_html if toc_html else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.fontshare.com">
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="page">
<div class="meta">
<span><span class="dot"></span>{BRAND}</span>
<span class="meta-label">{label}</span>
<span class="topnav">{nav_html}</span>
</div>
<div class="{layout_class}">
{sidebar}
<article class="main">
{body}
</article>
</div>
<footer>
<span>{BRAND} · {FOOTER_DATE}</span>
{download_btn}
<span>{FOOTER_PATH}</span>
</footer>
</div>
{sticky_download}
</body>
</html>
"""


def main():
    for slug, title, label in PAGES:
        src = ROOT / f"{slug}.md"
        if not src.exists():
            print(f"MISSING: {src}")
            continue
        text = src.read_text()
        html = md.render(text)
        html = render_status_codes(html)
        html = render_tldr(html)
        toc_html = ""
        if slug == "index":
            html = restructure_index_cards(html)
        else:
            html = enhance_lede(html)
            html, toc = add_section_numbers_and_ids(html)
            toc_html = render_toc(toc)
        final = shell(title, html, slug, label, slug, toc_html)
        out = ROOT / f"{slug}.html"
        out.write_text(final)
        print(f"wrote {out.name} ({len(final):,} bytes)")


if __name__ == "__main__":
    main()
