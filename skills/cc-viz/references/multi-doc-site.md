# Multi-doc site

Reference for the **Multi-doc / iterated** route. Use when generating a small site (2–6 pages) that needs visual coherence, post-generation editability, and easy local rendering. Examples: a 3-layer architecture spec (brand · sales · technical), a multi-section internal memo, a versioned product overview.

The output is a folder, not a single HTML file. The user edits the markdown, re-runs `render.py`, the HTML rebuilds.

## When this beats single-HTML

The breakpoint is roughly **3 pages × non-trivial editability**. Below that, write HTML directly (Instant / Framed). Above that, the script pays off because every prose edit is a markdown change, not a hunt through `<p>` tags.

| Situation | Single HTML | Multi-doc |
|---|---|---|
| 1 doc, fixed content | ✓ winner | overkill |
| 3+ docs, user will iterate post-gen | tedious | ✓ winner |
| Visual coherence across pages required | manual discipline | shared CSS enforces |
| User wants markdown to edit in-place | fights HTML | ✓ winner |
| User wants to add a new doc later | manual stylesheet copy | drop a `.md`, run script |

## File layout

```
project-folder/
  index.md              # source-of-truth landing
  page-a.md             # source-of-truth section
  page-b.md
  page-c.md
  index.html            # generated — do not edit
  page-a.html
  page-b.html
  page-c.html
  styles.css            # shared stylesheet
  render.py             # one-shot render script
```

Output location: `~/.agent/diagrams/<site-name>/`. Open `index.html` in the browser.

## Scaffold

The skill ships a complete starter at `templates/multi-doc-site/`:

- `render.py` — parameterized via a `PAGES` tuple and a small set of `# TODO:` markers. Copy and customize per project.
- `styles.css` — generic shared stylesheet with sidebar TOC, status badges, TLDR block, lede paragraph, atmospheric background, light + dark mode.
- `_example-index.md` and `_example-page.md` — markdown scaffolds showing where TL;DR, status codes, lede paragraph, and the index table go.

Copy the template folder, rename it, edit the markdown sources, run `python3 render.py`.

## What the render script does

Eight transforms turn N markdown files into a coherent site. Each one is in the scaffolded `render.py`; you adjust the inputs, not the machinery.

1. **PAGES tuple** — single source of truth driving the render loop *and* the top-nav rendering. Add a page, register once.
2. **Status-code badges.** Inline `` `STATUS` `` codes in markdown become styled `<span class="status …">` badges. Customize the `STATUS_TOKENS` whitelist and `cls_map` for your domain. A real-world example carried 12 tokens (`LOCKED`, `EVIDENCE`, `ALIGNMENT`, `OPEN`, `DEFINED`, `PARTIAL`, `AMBIGUOUS`, `DEPENDENT`, `FAIL`, `RISK`, `PASS-CONDITIONAL`, `PASS`) collapsed onto 5 visual classes — domain-specific. The default scaffold ships 5 (`PASS`, `FAIL`, `WARN`, `OPEN`, `LOCKED`); add or collapse as your domain needs.
3. **TLDR block.** A paragraph beginning `<strong>TL;DR.</strong>` in the rendered HTML becomes a styled `.tldr` block — a label + body grid. Place it in the markdown wherever the TL;DR belongs (usually right after the lede).
4. **Lede paragraph.** The first blockquote after the h1 promotes to a `.lede` element (serif, larger, max-width-constrained). Use markdown blockquote `>` syntax in the source.
5. **h2 numbering + anchor ids + sidebar TOC.** `add_section_numbers_and_ids` increments a counter, slugifies the h2 text, sets `id` and `data-num` on each h2, and emits a `[(num, slug, text)]` list. `render_toc` turns that into a sticky on-this-page sidebar. The layout switches between `layout` (with sidebar) and `layout-no-sidebar` (index page only).
6. **Card-grid index restructure.** A markdown table on the index page gets replaced with a card-grid HTML block. The table stays as the source-of-truth in markdown (scannable, editable); the grid is the visual rendering. Edit the cards-html in `render.py` to match your page set.
7. **Download .md button.** Both an inline footer link and a sticky bottom-right floater. Lets readers grab the raw markdown source. The "markdown is source of truth" claim is only honest if the markdown is reachable.
8. **Meta strip + footer.** Top meta strip with brand dot, page label, inline top nav. Footer with date, brand name, breadcrumb path, and the download button. Provides cross-page consistency.

## CSS conventions

These are baked into the scaffolded `styles.css`. Edit the palette tokens; leave the structural patterns.

- **Numbered section markers** via CSS `::before` reading `data-num` — mono font, letter-spaced, accent-colored, with a divider rule.
- **Status badge classes** — one per visual class (evidence/alignment/open/locked/fail). Use sparingly as scan markers.
- **TLDR block** — two-column grid (label + body) collapsing to single-column on mobile.
- **Lede paragraph** — serif, ~22px, max-width 720px. The doc's pull quote.
- **Card grid for index** — 1fr column with a 130px num column inside each card. Hover lifts the card and shifts the right-arrow.
- **Sidebar TOC** — sticky, `top: 24px`, `max-height: calc(100dvh - 48px)`, scrolls independently. Hides under 960px viewport.
- **Atmospheric background** — radial gradient overlay + repeating-line texture at 2-3% opacity. Same rule cc-viz enforces for single-file diagrams: no flat void.
- **Light + dark token redefinition** — full palette swap in `@media (prefers-color-scheme: dark)`. Both modes look intentional.
- **Multi-font load** — three fonts, three distinct roles (body / display-serif / mono). The scaffold ships Satoshi + Instrument Serif + JetBrains Mono as one paper/ink-friendly pairing; substitute any pairing from `references/libraries.md`. Body font typically loads from Google Fonts; the scaffold's Satoshi is from Fontshare and requires its own `<link>` if you keep it.

## Title convention

`Page Name · Brand Name` (middle-dot separator). Consistent across all pages. The brand name goes in the meta strip and footer too.

## Markdown source conventions

The scaffold's `_example-page.md` shows the shape. Key elements:

- **h1** = page title. One per page.
- **Lede blockquote** immediately after the h1: `> One-sentence orientation.`
- **TL;DR paragraph** after the lede: `**TL;DR.** One-paragraph executive summary.`
- **h2** = section. Numbered automatically. Use plain text — slugified to anchor id.
- **Status codes** inline: `` `EVIDENCE` `` or `` `EVIDENCE 2026-05-01` ``. Inline-code only; don't wrap in HTML.

## Optional: publish

> **Surface caveat.** Publishing and local preview require shell access + network — Claude Code (CLI / IDE) or another agent surface with local bash. On Claude.ai web or desktop, skip this section: generate the folder, hand off to the user, let them publish locally.

Multi-doc output is a static folder. Two one-line publish options when shell is available:

**Cloudflare Pages (Wrangler):**
```bash
cd ~/.agent/diagrams/<site-name>
npx wrangler pages deploy . --project-name=<site-name>
```

**Vercel:**
```bash
cd ~/.agent/diagrams/<site-name>
vercel --prod
```

Both require their respective CLI installed and authenticated.

**Local preview** (also shell-only):

```bash
cd ~/.agent/diagrams/<site-name>
python3 -m http.server 8000
# open http://localhost:8000
```

Publishing is not part of the skill's contract. Generate the folder; the user decides whether to ship it.

## Anti-patterns

- **Don't put status badges in markdown as HTML spans.** Keep markdown clean (`` `STATUS` ``). The script transforms.
- **Don't generate inline styles per page.** Shared CSS is the whole point.
- **Don't use markdown for diagram-heavy content.** If a page is mostly a diagram, write HTML directly or embed a Mermaid block via a regex hook in render.py.
- **Don't fight the markdown grammar.** If you need a card grid, add a regex transform; don't try to encode it in markdown syntax.
- **Don't auto-number h2s across the whole site.** Reset per page in `add_section_numbers_and_ids` (already does). Otherwise page B starts at 11 because page A had 10 sections.
- **Don't skip the atmosphere rule for the shared stylesheet.** The same void test applies — dark backgrounds need gradient, texture, or vignette.
- **Don't ship without the .md download button.** If you claim markdown is the source of truth, make the markdown reachable.

## When to drop this pattern

If the user starts asking for substantial layout-per-page (different grid systems, custom hero sections, magazine-style spreads), the markdown abstraction is fighting you. Either:

1. Move that one page to hand-crafted HTML (keep the rest scripted), or
2. Move the whole site to a static-site generator (Astro, Eleventy) where templates are first-class.

The script pattern lives between "throw HTML in a folder" and "set up a static site generator." Narrow but real sweet spot.

## Variant: per-page CSS hooks

If one page needs a unique visual treatment (a ladder diagram, a flow diagram, a custom hero), let the markdown include a semantic marker comment:

```markdown
<!-- diagram: four-stage-flow -->
```

`render.py` recognizes the marker and injects a hand-crafted HTML snippet at that point. The marker stays in the markdown (source intact); the visual lives in the script's snippet library. The scaffold leaves this as a comment placeholder — add hooks as needed.

## Tradeoffs

| | Single HTML | Multi-doc script |
|---|---|---|
| Visual ceiling | Higher (every pixel intentional) | Lower (constrained by CSS templates) |
| Editability | Find the `<p>` and rewrite | Edit markdown, re-run |
| Cross-page coherence | Manual discipline | Stylesheet enforces |
| Adding a new page | Copy + adapt full HTML | Add `.md`, register in `PAGES`, re-run |
| User who'll never touch the file | Single HTML is fine | Overkill |
| User who'll iterate over weeks | Single HTML decays | Script keeps source clean |

## Origin

Pattern extracted from a real internal site: a seven-page architecture spec covering brand, sales, technical architecture, engagement paths, products, and next-steps. Replaced a single ~2000-line working doc with seven shorter, structurally-distinct documents under one stylesheet. The split was the win. Each page got its own register and visual treatment while staying coherent through shared CSS.
