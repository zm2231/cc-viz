# Multi-doc site pattern: markdown source + render script + shared CSS

Use when generating a small site (2–6 pages) that needs visual coherence, post-generation editability, and easy local rendering. Examples: a 3-layer architecture spec (brand · sales · technical), a multi-section internal memo, a versioned product overview.

## When this beats hand-crafted HTML

| Situation | Hand-crafted HTML | This pattern |
|---|---|---|
| Single visualization, fixed content | ✓ winner | overkill |
| 1 doc, content unlikely to change | ✓ winner | unnecessary |
| 3+ docs, user will iterate post-gen | tedious | ✓ winner |
| Visual coherence across pages required | risk of drift | shared CSS enforces |
| User wants markdown to edit in-place | fights HTML | ✓ winner |
| Status tags / badges across pages | repetitive markup | render once in script |
| User wants to add a new doc later | manual stylesheet copy | drop a `.md`, run script |

The breakpoint is roughly **3 pages × non-trivial editability**. Below that, write HTML directly. Above that, the script pays off because every prose edit is a markdown change, not a hunt through `<p>` tags.

## Structure

```
project-folder/
  index.md              # source-of-truth landing
  page-a.md             # source-of-truth section
  page-b.md
  page-c.md
  index.html            # generated, do not edit
  page-a.html           # generated
  page-b.html
  page-c.html
  styles.css            # shared, hand-tuned
  _render.py            # one-shot render script (or symlink)
```

User edits `*.md` and re-runs the script. HTML is build artifact, not source.

## Core script shape

```python
from markdown_it import MarkdownIt
from pathlib import Path
import re

ROOT = Path("...")
PAGES = [
    ("index", "Title · Section Label", "Overview"),
    ("page-a", "Title · Page A Label", "Page A"),
    # ...
]

md = (
    MarkdownIt("commonmark", {"html": False, "linkify": True})
    .enable("table")
    .enable("strikethrough")
)

def render_status_codes(html: str) -> str:
    """Inline `STATUS` codes → styled badges. Whitelist your tokens."""
    tokens = ["LOCKED", "EVIDENCE", "OPEN", "ALIGNMENT", "FAIL", "PASS"]
    cls_map = {"LOCKED": "locked", "EVIDENCE": "evidence", ...}
    pattern = r'<code>(' + '|'.join(tokens) + r')([^<]*?)</code>'
    return re.sub(
        pattern,
        lambda m: f'<span class="status {cls_map[m.group(1)]}">{(m.group(1)+m.group(2)).strip()}</span>',
        html,
    )

def add_section_numbers(html: str) -> str:
    """h2 → numbered with data-num attribute. CSS handles display."""
    counter = [0]
    def repl(m):
        counter[0] += 1
        return f'<h2 data-num="{counter[0]:02d}">{m.group(1)}</h2>'
    return re.sub(r'<h2>(.*?)</h2>', repl, html)

def enhance_lede(html: str) -> str:
    """First blockquote after h1 becomes .lede paragraph."""
    return re.sub(
        r'(<h1[^>]*>.*?</h1>\s*)<blockquote>\s*<p>(.*?)</p>\s*</blockquote>',
        r'\1<p class="lede">\2</p>',
        html, count=1, flags=re.DOTALL,
    )

# top nav with current-page highlighting
def shell(title, body, current, label):
    nav = ' · '.join(
        f'<a href="{href}" class="{"current" if slug==current else ""}">{lbl}</a>'
        for slug, href, lbl in PAGES
    )
    return f"""<!DOCTYPE html>...<link rel="stylesheet" href="styles.css">
    <body><div class="meta">{nav}</div><article>{body}</article></body>"""

for slug, title, label in PAGES:
    src = ROOT / f"{slug}.md"
    html = md.render(src.read_text())
    html = render_status_codes(html)
    html = enhance_lede(html)
    if slug != "index":
        html = add_section_numbers(html)
    (ROOT / f"{slug}.html").write_text(shell(title, html, slug, label))
```

## CSS conventions that pay off

**Status badge classes** — one for each status type, color-coded. Use sparingly so the eye uses them as scan markers.

**Numbered section markers** via CSS `::before` reading `data-num` attribute, so the script just sets the data attribute and CSS handles all the visual treatment:

```css
h2[data-num]::before {
  content: attr(data-num);
  font-family: monospace;
  letter-spacing: 2.4px;
  color: var(--accent);
  display: block;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 8px;
  margin-bottom: 10px;
}
```

**Card grid for index pages** — replace a markdown table on the index page with a card-grid block via regex substitution. The table stays as the source-of-truth in markdown (editable, scannable); the grid is the visual rendering.

**Lede paragraph** — the first blockquote after the h1 typically reads as the doc's pull quote / orientation. Promote it visually to a `.lede` element with serif type, larger size, max-width constraint.

**Shared stylesheet** — one `styles.css` linked from every HTML. Means a global tweak (palette, spacing) updates the whole site. The user can also drop a new page without touching CSS.

## Anti-patterns

- **Don't put status badges in markdown as HTML spans.** Keep markdown clean (`` `STATUS` ``). The script transforms.
- **Don't generate inline styles per page.** Shared CSS is the whole point.
- **Don't use markdown for diagram-heavy content.** If a page is mostly diagram, write HTML or use a Mermaid block.
- **Don't fight the markdown grammar.** If you need a card grid, add a regex transform; don't try to encode it in markdown syntax.
- **Don't auto-number every h2 across the site.** Reset per page. Otherwise cross-page reading gets weird (page B starts at 11 because page A had 10 sections).

## Tradeoffs vs. hand-crafted HTML

| | Hand-crafted | Script + markdown |
|---|---|---|
| Visual ceiling | Higher (every pixel intentional) | Lower (constrained by CSS templates) |
| Editability | Find the `<p>` and rewrite | Edit markdown, re-run |
| Cross-page coherence | Manual discipline | Stylesheet enforces |
| Adding a new page | Copy + adapt full HTML | Add `.md`, register in `PAGES`, re-run |
| User who'll never touch the file | Hand-crafted is fine | Overkill |
| User who'll iterate over weeks | Hand-crafted decays | Script keeps source clean |

## Variant: per-page CSS hooks

If one page needs a unique visual treatment (e.g. a ladder diagram on a sales page, a flow diagram on an architecture page), let the markdown source include semantic markers:

```markdown
<!-- diagram: four-stage-flow -->
```

The render script recognizes the marker and injects a hand-crafted HTML snippet at that point. The marker stays in the markdown (so the source of truth is intact); the visual lives in the script's snippet library.

## When to drop this pattern

If the user starts asking for substantial layout-per-page (different grid systems, custom hero sections, magazine-style spreads), the markdown abstraction is fighting you. At that point either:

1. Move that one page to hand-crafted HTML (keep the rest scripted), or
2. Move the whole site to a real static-site generator (Astro, Eleventy) where templates are first-class.

The script pattern lives between "throw HTML in a folder" and "set up a static site generator." It's a narrow but real sweet spot.

## Originated

`shared-docs/internal/cf-architecture-2/` (May 2026). Three-layer architecture spec: brand, sales, technical. Replaced a single 1978-line working doc with four shorter, structurally-distinct documents under one stylesheet.
