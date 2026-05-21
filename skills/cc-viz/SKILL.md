---
name: cc-viz
description: Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
compatibility: Requires a browser to view generated HTML files.
metadata:
  version: "1.1.0"
---

# cc-viz

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. Brief text summary in the chat is fine; the table itself is the HTML page.

## Workflow

cc-viz is a router. The same invocation can mean wildly different things depending on context, audience, and intent. Route correctly before committing to a path or you'll spend ten rounds correcting the output. The most common failure mode is running the deepest, slowest path on a request that wanted the fastest, lightest one (or the reverse).

### 0. Route the request

Classify what kind of visualization this is. Signals:

- **Conversation context**: working in a specific repo for a while? Files already read? Subject already loaded? Rich context = lean on what's loaded, ship fast. Cold start (`/cc-viz make me a diagram of X` with no prior context) = scope first.
- **Invocation phrasing**: *"throw something together to share"* vs *"draft a strategic brief"* vs *"diagram this"* vs *"deck for the board"* vs *"a small site I'll edit"* — different requests.
- **Mode commands**: if a more specific mode (`/project-recap`, `/diff-review`, `/plan-review`, `/generate-slides`, `/fact-check`) fits the request better than the top-level skill, surface that to the user first. Don't quietly run the wrong tool.

Map the intent to a mode:

| Intent | Signals | Methodology |
|---|---|---|
| **Quick share** | Mid-flow in a repo, "make me a quick page", subject already loaded | Lean on conversation context. Skip deep research. Single-pass form, fast aesthetic, ship in minutes. |
| **Internal brief / memo** | "Memo for the team", "decision doc", "what should we do" | Grounded research. Tight prose. Tables + status. Audience-specific register. See `references/story-framing.md`. |
| **External / client deliverable** | "Page for the client", "external review", "publish-grade" | Polish-grade. Form commitment. No internal jargon. Atmosphere matters. See `references/story-framing.md`. |
| **Diagram / topology** | "Draw / visualize / show how X works" | Architecture or flow primary. Mermaid or CSS-grid topology. Prose minimal. |
| **Slide deck** | "Deck about X" or `--slides` flag | Magazine-quality scroll-snap deck. See `references/slide-patterns.md`. |
| **Multi-doc / iterated site** | "Small site", "3 pages I'll edit", "versioned overview" | Folder output: markdown sources + render.py + shared styles.css. See `references/multi-doc-site.md` and `templates/multi-doc-site/`. |
| **Recap / fact-check / diff-review / plan-review** | Specific intent named | Defer to the matching mode-specific skill. |

### 0.5. When the intent is ambiguous, ask. When it's clear, don't.

If two or more modes plausibly apply and the conversation context doesn't disambiguate, surface one or two clarifying questions before drafting:

- *"Quick share, internal brief, or external deliverable?"*
- *"Who's reading it — you, your team, or someone outside?"*
- *"Form preference — board memo, magazine editorial, broadside, or something else?"*

Ask at most two. Ask only what conversation context doesn't already answer. Don't ask "what's this about" when invoked in a project where the answer is obvious from prior turns.

If intent is clear from context, do not ask. The cost of the wrong question is the same as the cost of the wrong answer — it makes the skill feel like a wizard.

### 0.7. Load accumulated judgment

Skills compound only if they remember. Before drafting, check for project-specific context:

- A `.cc-viz/context.md` in the project root, or
- A `~/.cc-viz/projects/<project-name>.md` per-project memory file

These files capture: typical audience for this project, register preferences, anti-pattern history, prior decisions about form, accumulated diction notes, things to never repeat. If one exists, read it and apply.

If something non-obvious gets established during this session (audience preference, register choice, an aesthetic that landed, a phrase or font that didn't), write it back at the end. The next invocation should not require re-explaining what was learned.

### 1. Frame the story (before anything visual)

A visualization is an argument made in a particular voice for a particular reader. Skip this and the result is "list of facts in nice boxes" — voice-flat, forgettable.

**Ground claims before drafting.** Speculation reads identical to truth on the page; only the reader who knows the territory can tell the difference. Any visualization making claims about a real system must be grounded in evidence first. README plus a docs glance is not enough — it misses what's actually moving. Adjust depth to the routed mode (Quick share = lean on what's loaded; Internal brief = thorough; External deliverable = exhaustive), but never skip entirely.

**Story arc.** State in one sentence what the reader walks away knowing. If you can't write that sentence, the diagram has no spine.

**Report vs argument.** Most analytical / mapping / comparison / decision-memo work is argument-led — the artifacts (files, columns, schema references, framework citations) are *evidence FOR a claim*, not the claim itself. A page listing "these files exist, these columns exist, this maps to that" has shown evidence but not told a story. If the page's spine is a matrix, ask whether it should actually be a report (catalog intent) or an argument (claim about what the catalog means). For argument intent, lead with the claim, support each section with the evidence that defends it, close with the implication.

**Audience, register, info-detail, baseline.** Name the audience concretely (not "technical reader" but "senior backend engineer who knows our stack but hasn't seen this subsystem"). Pick one register and hold it (editorial-narrative, technical-precise, engineering-confessional, executive-impact). Each section answers a question the reader has at that point — and only that. Separate what they already know from what they need to learn; the page closes that gap and nothing else.

For the full grounding-pass methodology, the report-vs-argument distinction at depth, audience/register depth, and reader-baseline discipline: `references/story-framing.md`.

**Voice & diction rules** — non-negotiable, even in Quick share mode. Full set in `references/voice-and-diction.md`:

- No em dashes (`—`) in body prose. Strongest single AI tell. Citations only.
- Sentences ≤22 words; paragraphs ≤3 sentences. One technical-precision exception per page.
- Direct address (*you / your*) only when the reader is an actor (system behavior, touchpoints, consequences). Not in meta-framing.
- One italic-emphasis point per heading, per pull quote, per card. Italic is a budget, not a default.
- No yap. Cut every hedge-starting sentence. Trim before commit.

### 2. Pick a form, commit fully

Form precedes aesthetic. Pick one form's structural vocabulary and commit. Frankensteins — a board-memo recommendation card grafted onto a magazine drop-cap, a slide-deck hero pasted above a dashboard grid — read as half-finished.

| Form | Register | Structural vocabulary | When |
|---|---|---|---|
| **Board memo** | Calm, plain, scannable | Eyebrow + hero h1 + status strip + recommendation card + comparison tables + brief paragraphs + plain footer | Internal team decisions, status updates, planning notes |
| **Magazine editorial** | Voice-driven, gravitas | Three-column kicker masthead + display hero + drop-cap + multi-column body + full-bleed feature strip + roman-numeraled close + colophon | Strategy briefs, narrative-heavy explainers, when the prose is the art |
| **Broadside / one-page poster** | Maximalist, declarative | Single bold composition fitting one viewport, oversized type, a typographic system instead of tables | Manifestos, statements, single-page advocacy |
| **Slide deck** | Visual-first, paced | Viewport-snapped slides, one big idea per slide, scroll-snap | Pitches, walkthroughs intended to be shown not read |
| **Data journalism** | Cold, precise, numerical | Tabular numerics, axis lines, sparklines, mono-font headers, FT/Bloomberg cadence | Quantitative comparisons, audits, dashboards |
| **Notebook / margin spread** | Personal, warm, informal | Warm cream base, marginalia, hand-drawn-feeling rules, pencil-sketch arrows, asides as if jotted | Self-briefs, working notes, inside-the-head register |
| **Architecture / topology** | Technical, structural | Mermaid or CSS-grid topology primary; prose minimal and supporting | "Show how X works" — the diagram IS the document |
| **Quick share / lightweight** | Direct, low-friction | Single page, focused, fast, minimal chrome | Mid-flow shares, work-in-progress pings, "send Max this" |
| **Multi-doc site** | Form follows page register | Per-page registers under one shared stylesheet | 3+ pages user will iterate; see `references/multi-doc-site.md` |

Pick based on routed intent (Step 0) and framed audience/register (Step 1). If two forms could plausibly fit, pick the one that does the audience's reading work for them — the form that lets them read in three minutes what would take ten in another form.

**Anti-Frankenstein rule.** Once the form is chosen, every element on the page serves that form. The form's structural vocabulary is the only structural vocabulary you use.

### 3. Aesthetic (5 seconds, not 5 minutes)

Commit to a visual direction. Don't default to "dark theme with blue accents" every time. Vary from recent generations.

**Constrained aesthetics (prefer these — they have specific requirements that prevent generic output):**
- Blueprint — technical drawing feel, subtle grid background, deep slate/blue, monospace labels, precise borders
- Editorial — serif headlines (Instrument Serif / Crimson Pro), generous whitespace, muted earth tones or deep navy + gold
- Paper/ink — warm cream `#faf7f5`, terracotta/sage accents, informal feel
- Monochrome terminal — green/amber on near-black, monospace everything, CRT glow optional

**Flexible aesthetics (use with discipline):** IDE-inspired (borrow a real, named scheme: Dracula, Nord, Catppuccin, Solarized, Gruvbox, One Dark, Rosé Pine — commit to the actual palette); data-dense (small type, tight spacing, muted colors).

**Forbidden.** Neon dashboard (cyan + magenta + purple on dark) — always AI slop. Gradient mesh (pink/purple/cyan blobs). Inter + violet/indigo + gradient text — closes the loophole on the worst combo.

**Swap test.** If you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

Palette and font detail in `references/libraries.md`. Surface and atmosphere detail in `references/css-patterns.md`.

### 4. Structure

**Read the reference template before generating.** Read each time to absorb the patterns; don't memorize.
- Text-heavy architecture (card content > topology): `./templates/architecture.html`
- Flowcharts, sequence, ER, state machines, mind maps: `./templates/mermaid-flowchart.html`
- Data tables, comparisons, audits, feature matrices: `./templates/data-table.html`
- Slide decks (when `--slides` or `/generate-slides`): `./templates/slide-deck.html` + `./references/slide-patterns.md`
- Multi-doc sites: `./templates/multi-doc-site/` (render.py + styles.css + markdown scaffolds)
- Ready-to-paste font `<link>` blocks for all 13 pairings: `./templates/font-loaders.html`

CSS/layout patterns + SVG connectors: `./references/css-patterns.md`. Pages with 4+ sections: `./references/responsive-nav.md` for sticky sidebar TOC + mobile horizontal scroll.

**Choosing a rendering approach:**

| Diagram type | Approach | Why |
|---|---|---|
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content needs CSS control |
| Architecture (topology) | **Mermaid** | Connections need automatic edge routing |
| Flowchart / pipeline | **Mermaid** | Automatic node positioning |
| Sequence diagram | **Mermaid** | Lifelines, messages, activation boxes |
| Data flow | **Mermaid** with edge labels | Connection labels + auto-routing |
| ER / schema | **Mermaid** | Relationship lines between many entities |
| State machine | **Mermaid** | Labeled transitions |
| Mind map | **Mermaid** | Radial hierarchical layout |
| Data table | HTML `<table>` | Semantic markup, a11y, copy-paste |
| Timeline | CSS (central line + cards) | Simple linear, no layout engine needed |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |

**Mermaid theming, zoom controls, and class-collision constraints** — all in `references/libraries.md` and `references/css-patterns.md`. Three rules to remember inline: (1) `theme: 'base'` with custom `themeVariables`, never the default; (2) zoom controls require `target.style.zoom` on the `.mermaid` div (not transform, not SVG width); (3) never define `.node` as a page-level CSS class — Mermaid uses it internally, scope under `.mermaid` only.

### 5. Style

Apply these inline rules; reach for the references for detail.

**Typography.** Pick a font pairing from `./references/libraries.md`. Vary from recent generations.
- **Forbidden as `--font-body`:** Inter and any Inter variant (Inter Tight / Display / etc.), Roboto, Arial, Helvetica, system-ui alone, italic-by-design display serifs (Instrument Serif, Playfair Italic). Display serifs go in `--font-display`, never `--font-body`.

**Color.** CSS custom properties for the full palette. Define at minimum `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, 3-5 semantic accents. Both themes (light + dark) intentional.
- **Forbidden accents:** `#8b5cf6` `#7c3aed` `#a78bfa` `#d946ef`, the cyan-magenta-pink combination. Tailwind defaults signaling zero design intent.

**Atmosphere is mandatory in dark mode.** Flat dark backgrounds produce a void with text floating on it — the worst output cc-viz can emit. Dark backgrounds must have one of: subtle two-stop gradient, faint dot/hairline grid at 1–3% opacity, vignette, or focal radial glow behind the hero. The void test: corner vs. center distinguishable? If not, fix it.

**Visual weight + surface depth.** Hero sections elevated (accent-tinted, larger type). Body content flat. Code/secondary recessed. `<details>/<summary>` for useful-but-not-primary content. Detail in `references/css-patterns.md`.

**Animation earns its place.** Staggered fade-ins guide the eye through hierarchy. Mix `fadeUp` / `fadeScale` / `drawIn` / `countUp` by role. Respect `prefers-reduced-motion`.
- **Forbidden:** glowing/pulsing box-shadows (`@keyframes glow` is AI slop), continuous animations after page load, opacity-0 stuck state if entry animation skips.

### 6. Deliver

**Output location:** `~/.agent/diagrams/`. Descriptive filename: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. Directory persists across sessions.

**For multi-doc sites:** output is a folder, `~/.agent/diagrams/<site-name>/`. Open `index.html`.

**Open in browser:**
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`

**Tell the user** the file path so they can re-open or share.

## Diagram-specific notes

Most diagram types are routed through Mermaid (see Step 4 table). Notes that don't fit the table:

**Architecture / system.** Two approaches. *Text-heavy overviews* (card content > connections) → CSS Grid with explicit row/column placement, rounded cards with colored borders, monospace labels, vertical flow arrows, nested grids for subsystems (`./templates/architecture.html`). *Topology-focused* (connections > card content) → Mermaid `graph TD` / `graph LR` with custom `themeVariables`.

**State machines.** `stateDiagram-v2` has a strict parser — colons, parens, `<br/>`, HTML entities cause silent parse failures. If labels need any of these (e.g., `cancel()`, `curate: true`, multi-line), use `flowchart LR` with quoted edge labels (`|"label text"|`) instead. Reserve `stateDiagram-v2` for plain-text labels.

**Data tables.** Real `<table>`, not CSS-Grid-pretending. Sticky `<thead>`, alternating row backgrounds, optionally sticky first column, responsive `overflow-x: auto`, column-width hints, row-hover. Status as styled `<span>`, never emoji. Detail + reference in `./templates/data-table.html`.

**Timeline.** Vertical or horizontal with a CSS pseudo-element line. Phase markers as circles on the line. Cards alternating or single-side. Color progression from past (muted) to future (vivid).

**Dashboard.** Card grid with hero numbers. Sparklines via inline SVG `<polyline>`. Progress bars via CSS gradient. Real charts via Chart.js (CDN — see `references/libraries.md`). KPI cards with trend indicators.

## Slide Deck Mode

Opt-in only — invoke via `/generate-slides`, `--slides` flag, or explicit "slide deck" request. Never auto-select.

Slides are a different medium, not pages reformatted. Each slide is exactly one viewport tall (100dvh) with no scrolling. Typography 2–3× larger. Compose a narrative arc (impact → context → deep dive → resolution), not mechanically paginated source.

**Content completeness.** Changing medium doesn't drop content. Every section, decision, data point, and collapsible detail in the source appears in the deck. A 22-slide deck covering everything beats a 13-slide deck that looks polished but misses 40%.

Full slide-type catalog (10 types), composition variety rules, presets, and the "Planning a Deck from a Source Document" process: `references/slide-patterns.md`. Reference template: `./templates/slide-deck.html`.

## File Structure

Single-file modes (Instant, Framed, Slides): one self-contained `.html`. No external assets except CDN links (fonts, optional libraries).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <link href="https://fonts.googleapis.com/..." rel="stylesheet">
  <style>/* All inline. */</style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <!-- Optional <script> for Mermaid, Chart.js, anime.js when used -->
</body>
</html>
```

Multi-doc mode: a folder with `index.md`, `*.md`, `render.py`, `styles.css`, and generated `*.html`. See `references/multi-doc-site.md`.

## Quality Checks

Grade against `references/quality-rubric.md` before delivering. Six weighted dimensions (Form-Audience Match, Story Discipline, Voice & Diction, Grounding, Visual Quality, Anti-Pattern Free). Passing score ≥ 75/100 with no FAIL on `script` or `hybrid`.

Fast-pass tests:
- **Squint:** hierarchy still readable when blurred? Sections distinct?
- **Swap:** generic dark theme replaces yours — would anyone notice?
- **Both themes:** light and dark both intentional, not broken.
- **Void (dark mode):** corner vs. center visually distinguishable.
- **Re-teaching audit:** *"Does the reader already know this? If yes, why is it here?"* for every section.
- **Argument vs report:** can you summarize the spine in one sentence? Right shape (claim for argument, inventory for report)?
- **Mermaid syntax:** scan against the parser-break list in `references/anti-patterns.md` §6 and `references/libraries.md` "Common Pitfalls".

**Self-audit script.** For pages claiming things about real systems (file paths, table names, schema columns, framework definitions), run `scripts/strip-html.py <output.html> --stdout` and grep the result against the source repos. The grounding rubric dimension requires this.

## Anti-Patterns

Full library: `references/anti-patterns.md` (10 categories, ~30 documented failure modes). Read before generating; re-read the relevant section while drafting if the page touches that category.
