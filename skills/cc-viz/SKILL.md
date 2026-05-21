---
name: cc-viz
description: Generate beautiful, self-contained HTML pages that visually explain systems, code changes, plans, and data. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
compatibility: Requires a browser to view generated HTML files.
metadata:
  version: "1.0.0"
---

# cc-viz

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. You can still include a brief text summary in the chat, but the table itself should be the HTML page.

## Workflow

cc-viz is a router. The same invocation can mean wildly different things depending on context, audience, and intent. Route correctly before committing to a path or you'll spend ten rounds correcting the output. The most common failure mode of this skill is running the deepest, slowest path on a request that wanted the fastest, lightest one (or the reverse).

### 0. Route the request

Before anything else, classify what kind of visualization this is. Use signals from:

- **Conversation context**: have we been working in a specific repo or project for a while? Have files been read? Is there a subject already loaded into the conversation? Rich context = lean on what's loaded, ship fast. Cold start (`/cc-viz make me a diagram of X` with no prior context) = scope first.
- **Invocation phrasing**: *"throw something together to share"* vs *"draft a strategic brief"* vs *"diagram this"* vs *"deck for the board"* — these are different requests.
- **Mode commands**: if a more specific mode (`/project-recap`, `/diff-review`, `/plan-review`, `/generate-slides`, `/fact-check`) fits the request better than the top-level skill, surface that to the user first. Don't quietly run the wrong tool.

Map the intent to a mode and route accordingly:

| Intent | Signals | Methodology |
|---|---|---|
| **Quick share** | Mid-flow in a repo, "make me a quick page", subject already loaded | Lean on conversation context. Skip deep research. Single-pass form, fast aesthetic, ship in minutes. |
| **Internal brief / memo** | "Memo for the team", "decision doc", "what should we do" | Grounded research. Tight prose. Tables + status. Audience-specific register. |
| **External / client deliverable** | "Page for the client", "external review", "publish-grade" | Polish-grade. Form commitment. No internal jargon. Atmosphere matters. |
| **Diagram / topology** | "Draw / visualize / show how X works" | Architecture or flow primary. Mermaid or CSS-grid topology. Prose minimal. |
| **Slide deck** | "Deck about X" or `--slides` flag | Magazine-quality scroll-snap deck. See `references/slide-patterns.md`. |
| **Recap / fact-check / diff-review / plan-review** | Specific intent named | Defer to the matching mode-specific skill if one exists. |

### 0.5. When the intent is ambiguous, ask. When it's clear, don't.

If two or more modes plausibly apply and the conversation context doesn't disambiguate, surface one or two clarifying questions before drafting. Examples:

- *"Quick share, internal brief, or external deliverable?"*
- *"Who's reading it — you, your team, or someone outside?"*
- *"Form preference — board memo, magazine editorial, broadside, or something else?"*

Ask at most two. Ask only what conversation context doesn't already answer. Do not ask "what's this about" when invoked in a project where the answer is obvious from the prior turns.

If intent is clear from context, do not ask. The cost of the wrong question is the same as the cost of the wrong answer — it makes the skill feel like a wizard.

### 0.7. Load accumulated judgment

Skills compound only if they remember. Before drafting, check for project-specific context:

- A `.cc-viz/context.md` in the project root, or
- A `~/.cc-viz/projects/<project-name>.md` per-project memory file

These files capture: this project's typical audience, register preferences, anti-pattern history, prior decisions about form, accumulated diction notes, things to never repeat from past sessions. If one exists, read it and apply.

If something non-obvious gets established during this session (audience preference, register choice, an aesthetic that landed, a phrase or font that didn't), write it back to the context file at the end. The next invocation in this project should not require re-explaining what was learned.

### 1. Frame the story (before anything visual)

A visualization is an argument made in a particular voice for a particular reader. Skip this step and the result is "list of facts in nice boxes" — technically correct, voice-flat, forgettable. Answer all four before opening a template.

**Ground claims before drafting.** Speculation reads identical to truth on the page; only the reader who knows the territory can tell the difference. Any visualization that makes claims about a real system, project, person, market, or decision must be grounded in evidence first. README plus a docs glance is not enough — it misses what's actually moving. Adjust the depth of the grounding pass to the routed mode (Quick share = lean on what's loaded; Internal brief = thorough; External deliverable = exhaustive), but never skip it entirely.

The grounding-pass shape, generically:

- **Read the system's actual state, not its description of itself.** For a codebase: the entry file end-to-end, every config that defines runtime bindings, the schema or migrations, a sample of route handlers or core modules, the recent commit log. For a project or team: recent meeting/decision artifacts, ownership notes, what's moved in the last weeks. For a market or competitive landscape: current state of the named players (their docs, their changelogs, their recent shipping cadence), not training-stale impressions.
- **Check what's been changing.** `git log` for code, recent activity feeds for projects, recent web/news for markets. The story should foreground what's *currently* in motion, not what the docs froze months ago.
- **Read the corner files.** `CLAUDE.md`, `AGENTS.md`, `DEVELOPMENT.md`, design docs in subdirectories — these often hold the real invariants and gotchas the top-level README skips.
- **Use whatever evidence corpora are available to you.** Web search, semantic search over a research index, vector indexes, knowledge-management systems, MCP-exposed services, the project's own search/grep tools, transcripts, prior session notes. The methodology is generic; the tooling is whatever this user/project has wired up. The skill does not mandate specific tools — it mandates that grounding happens.

If a brief was prepared upstream by a research agent or by the user, use it. If not, do the work yourself before drafting. Either way, the story is built from the actual state of the thing being visualized, not from the marketing version of it.

**What's the story arc?** From start to end, what does the reader walk away knowing? State it in one sentence. "context-layer ingests ten source types, classifies every observation against the existing entity graph, and lets confirmed patterns surface as Logseq pages — backed by one Postgres and one inference gateway." If you can't write that sentence, the diagram has no spine.

**Report vs argument.** Decide which kind of page this is. They are not the same and they need different structures.

A **report** presents facts. *"Here are the eight source connectors. Here are the four layers. Here are the columns and thresholds."* The reader walks away knowing what exists. Spine is the inventory; structure is the matrix or the schema.

An **argument** makes a claim. *"context-layer was built to extract a four-dimension framework but quietly invented two things the framework hasn't named yet — system metacognition and source-level epistemics. The interesting question is whether they generalize."* The reader walks away with a position they can agree with, push back on, or build on. Spine is the claim; structure is claim → evidence → implication.

Most analytical, mapping, comparison, synthesis, decision-memo, or strategic work is argument-led. The artifacts (files, columns, thresholds, schema references, commit hashes, framework citations) are *evidence FOR the argument*, not the argument itself. A page that lists "these files exist, these columns exist, this maps to that" has shown evidence; it has not told a story. The page must be summarizable in one sentence as: *"X is the case, and here's why it matters."*

If you find yourself building a feature inventory or a matrix as the page's spine, ask whether the page should actually be a report (intent: catalog or reference) or an argument (intent: make a claim about what the catalog means). For argument intent, restructure: lead with the load-bearing claim, support each section with the evidence that defends it, close with the implication. The matrix may still appear, but as one supporting element under a claim, not as the page's backbone.

**Who is the audience and at what level?** A developer reading code (technical depth, jargon OK) ≠ a teammate joining the project (mental model, label-what-things-are) ≠ an executive reviewing a proposal (impact, tradeoffs, no implementation). Density and vocabulary follow audience.

**What's the register/voice?** Editorial-narrative ("Three layers, one Dream cycle"), technical-precise ("FOR UPDATE SKIP LOCKED, total-order claim"), engineering-confessional ("we got this wrong twice"), or executive-impact ("60% reduction in classification miss rate"). Pick one and hold it across every label, heading, and paragraph. Mixing registers is what makes prose feel AI-generated.

**What information at what level of detail?** Every section answers a question the reader has at that point. The reader's questions arrive in an order — answer them in that order. Inventory what must appear (file paths, decision rationale, error rates, schema names) and assign each to the section where the reader will need it.

**Reader's knowledge baseline.** Before drafting, separate two lists for the audience: *what they already know* and *what they need to know from this page*. The page exists only to close the gap between them. Re-teaching the first list reads as condescending; assuming the second is already known reads as opaque. Neither is digestible.

For technical subjects: name the reader's expertise level concretely (junior in this stack, senior in this stack, methodology specialist, executive who has seen demos). Then write to the gap, not from scratch and not from the assumption that everything is already understood. A page mapping context-layer to a methodology framework should NOT re-introduce what context-layer is to someone who built it; it should foreground the *mapping*, which is the new thing.

Ask, before writing each section: *"Does the reader already know this? If yes, why is it on the page?"*

**Diction, voice, and prose-discipline rules** live in `references/voice-and-diction.md`. Read it before drafting any prose-led page. The summary you cannot skip:

- No em dashes (`—`) in body prose — strongest single AI tell. Citations only.
- Sentences ≤22 words; paragraphs ≤3 sentences. One technical-precision exception per page.
- Direct address (*you / your*) only when the reader is an actor (system behavior, touchpoints, consequences). Not in meta-framing about the page itself, not in neutral reference captions.
- One italic-emphasis point per heading, per pull quote, per card. Italic-emphasis is a budget, not a default.
- Story sections narrate; reference sections may use literal headings when scanability matters.
- No yap. Cut every hedge-starting sentence. Trim before commit.

The full forbidden vocabulary list, the full no-yap heuristics, the heading rules, and the audience-leakage warning are all in `references/voice-and-diction.md`. The full anti-pattern library (with regex-checkable failure modes) is in `references/anti-patterns.md`.

### 2. Pick a form, commit fully

Form precedes aesthetic. Pick one form's structural vocabulary and commit. Frankensteins — a board-memo recommendation card grafted onto a magazine drop-cap, a slide-deck hero pasted above a dashboard grid — read as half-finished. The page should feel like one designer made one thing.

The forms cc-viz knows:

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

Pick based on the routed intent (Step 0) and the framed audience/register (Step 1). If two forms could plausibly fit, pick the one that does the audience's reading work for them — the form that lets them read in three minutes what would take ten in another form.

Anti-Frankenstein rule: once the form is chosen, every element on the page must serve that form. No board-memo recommendation cards inside a magazine spread. No magazine drop-caps inside a board memo. No dashboard KPI strips inside a notebook spread. The form's structural vocabulary is the only structural vocabulary you use.

### 3. Aesthetic (5 seconds, not 5 minutes)

Now commit to a visual direction. Don't default to "dark theme with blue accents" every time.

**What type of diagram?** Architecture, flowchart, sequence, data flow, schema/ER, state machine, mind map, data table, timeline, or dashboard. Each has distinct layout needs and rendering approaches (see Diagram Types below).

**What aesthetic?** Pick one and commit. The constrained aesthetics (Blueprint, Editorial, Paper/ink) are safer — they have specific requirements that prevent generic output. The flexible ones (IDE-inspired) require more discipline.

**Constrained aesthetics (prefer these):**
- Blueprint (technical drawing feel, subtle grid background, deep slate/blue palette, monospace labels, precise borders) — see `websocket-implementation-plan.html` for reference
- Editorial (serif headlines like Instrument Serif or Crimson Pro, generous whitespace, muted earth tones or deep navy + gold)
- Paper/ink (warm cream `#faf7f5` background, terracotta/sage accents, informal feel)
- Monochrome terminal (green/amber on near-black, monospace everything, CRT glow optional)

**Flexible aesthetics (use with caution):**
- IDE-inspired (borrow a real, named color scheme: Dracula, Nord, Catppuccin Mocha/Latte, Solarized Dark/Light, Gruvbox, One Dark, Rosé Pine) — commit to the actual palette, don't approximate
- Data-dense (small type, tight spacing, maximum information, muted colors)

**Explicitly forbidden:**
- Neon dashboard (cyan + magenta + purple on dark) — always produces AI slop
- Gradient mesh (pink/purple/cyan blobs) — too generic
- Any combination of Inter font + violet/indigo accents + gradient text

Vary the choice each time. If the last diagram was dark and technical, make the next one light and editorial. The swap test: if you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

### 4. Structure

**Read the reference template** before generating. Don't memorize it — read it each time to absorb the patterns.
- For text-heavy architecture overviews (card content matters more than topology): read `./templates/architecture.html`
- For flowcharts, sequence diagrams, ER, state machines, mind maps: read `./templates/mermaid-flowchart.html`
- For data tables, comparisons, audits, feature matrices: read `./templates/data-table.html`
- For slide deck presentations (when `--slides` flag is present or `/generate-slides` is invoked): read `./templates/slide-deck.html` and `./references/slide-patterns.md`

**For CSS/layout patterns and SVG connectors**, read `./references/css-patterns.md`.

**For pages with 4+ sections** (reviews, recaps, dashboards), also read `./references/responsive-nav.md` for section navigation with sticky sidebar TOC on desktop and horizontal scrollable bar on mobile.

**Choosing a rendering approach:**

| Diagram type | Approach | Why |
|---|---|---|
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content (descriptions, code, tool lists) needs CSS control |
| Architecture (topology-focused) | **Mermaid** | Visible connections between components need automatic edge routing |
| Flowchart / pipeline | **Mermaid** | Automatic node positioning and edge routing |
| Sequence diagram | **Mermaid** | Lifelines, messages, and activation boxes need automatic layout |
| Data flow | **Mermaid** with edge labels | Connections and data descriptions need automatic edge routing |
| ER / schema diagram | **Mermaid** | Relationship lines between many entities need auto-routing |
| State machine | **Mermaid** | State transitions with labeled edges need automatic layout |
| Mind map | **Mermaid** | Hierarchical branching needs automatic positioning |
| Data table | HTML `<table>` | Semantic markup, accessibility, copy-paste behavior |
| Timeline | CSS (central line + cards) | Simple linear layout doesn't need a layout engine |
| Dashboard | CSS Grid + Chart.js | Card grid with embedded charts |

**Mermaid theming:** Always use `theme: 'base'` with custom `themeVariables` so colors match your page palette. Use `layout: 'elk'` for complex graphs (requires the `@mermaid-js/layout-elk` package — see `./references/libraries.md` for the CDN import). Override Mermaid's SVG classes with CSS for pixel-perfect control. See `./references/libraries.md` for full theming guide.

**Mermaid zoom controls:** Always add zoom controls (+/−/reset/expand buttons) to every `.mermaid-wrap` container. Two critical requirements: (1) Set `target.style.zoom` on the `.mermaid` div (NOT on the SVG, NOT via `transform: scale`, NOT via `svg.style.width` percentage scaling). The `.mermaid-wrap` MUST be `display: flex; justify-content: center; align-items: center; overflow: hidden; min-height: 340px` — this is the proven e3-share pattern where CSS zoom reflows in Chrome/Safari and the wrap grows with the diagram so the frame stays in proportion. Other patterns produce content that gets cut off or scrollbars where you don't want them. (2) After `mermaid.initialize()`, call `mermaid.run().then(...)` to remove the hardcoded `height` attribute from every `.mermaid svg` and set `width: 100%; height: auto` — without this the SVG keeps a fixed pixel height and won't fit its container. See `./references/css-patterns.md` and `./templates/mermaid-flowchart.html`.

**Mermaid CSS class collision constraint:** Never define `.node` as a page-level CSS class. Mermaid.js uses `.node` internally on SVG `<g>` elements with `transform: translate(x, y)` for positioning. Page-level `.node` styles (hover transforms, box-shadows) leak into diagrams and break layout. Use the namespaced `.ve-card` class for card components instead. The only safe way to style Mermaid's `.node` is scoped under `.mermaid` (e.g., `.mermaid .node rect`).


### 5. Style

Apply these principles to every diagram:

**Typography is the diagram.** Pick a distinctive font pairing from the list in `./references/libraries.md`. Every page should use a different pairing from recent generations.

**Forbidden as `--font-body`:** Inter, Roboto, Arial, Helvetica, system-ui alone — AI slop signals. Also forbidden: any Inter variant (Inter Tight, Inter Display, etc.) — closing the loophole. Also forbidden: italic-by-design display serifs (Instrument Serif, Playfair Display Italic, EB Garamond Italic) — they are exquisite for headlines and pull-quotes but unreadable as paragraph body. Pair them as `--font-display` with a separate sans for `--font-body`.

**Good pairings (use these):**
- DM Sans + Fira Code (technical, precise)
- Instrument Serif (display only) + DM Sans (body) + JetBrains Mono (editorial, refined — tri-font: serif for h1/pull-quotes, sans for paragraph body, mono for labels)
- IBM Plex Sans + IBM Plex Mono (reliable, readable)
- Bricolage Grotesque + Fragment Mono (bold, characterful)
- Plus Jakarta Sans + Azeret Mono (rounded, approachable)

Load via `<link>` in `<head>`. Include a system font fallback in the `font-family` stack for offline resilience.

**Color tells a story.** Use CSS custom properties for the full palette. Define at minimum: `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, and 3-5 accent colors. Each accent should have a full and a dim variant (for backgrounds). Name variables semantically when possible (`--pipeline-step` not `--blue-3`). Support both themes.

**Forbidden accent colors:** `#8b5cf6` `#7c3aed` `#a78bfa` (indigo/violet), `#d946ef` (fuchsia), the cyan-magenta-pink combination. These are Tailwind defaults that signal zero design intent.

**Good accent palettes (use these):**
- Terracotta + sage (`#c2410c`, `#65a30d`) — warm, earthy
- Teal + slate (`#0891b2`, `#0369a1`) — technical, precise
- Rose + cranberry (`#be123c`, `#881337`) — editorial, refined
- Amber + emerald (`#d97706`, `#059669`) — data-focused
- Deep blue + gold (`#1e3a5f`, `#d4a73a`) — premium, sophisticated

Put your primary aesthetic in `:root` and the alternate in the media query:

```css
/* Light-first (editorial, paper/ink, blueprint): */
:root { /* light values */ }
@media (prefers-color-scheme: dark) { :root { /* dark values */ } }

/* Dark-first (neon, IDE-inspired, terminal): */
:root { /* dark values */ }
@media (prefers-color-scheme: light) { :root { /* light values */ } }
```

**Surfaces whisper, they don't shout.** Build depth through subtle lightness shifts (2-4% between levels), not dramatic color changes. Borders should be low-opacity rgba (`rgba(255,255,255,0.08)` in dark mode, `rgba(0,0,0,0.08)` in light) — visible when you look, invisible when you don't.

**Backgrounds create atmosphere — especially in dark mode.** Any dark palette that reads as flat produces the worst output cc-viz can emit: a void with text floating on it. Dark backgrounds MUST have one of:
- A subtle two-stop gradient between two near-neighbors (e.g. `#0e1726` → `#162033` corner-to-corner) — gives the page depth without color shift
- A faint dot-grid or hairline-grid pattern at low opacity (1–3%) — gives the page texture
- A vignette: lighter at center, ~5% darker at edges, via radial-gradient overlay
- A focal radial glow behind the hero/h1 in the accent color at 8–12% opacity

The check: stand back from the screen and look at the corner vs the center. If you can't tell them apart, you have a void; add atmosphere or pick a light-first aesthetic. Some palettes ship with notoriously flat default backgrounds — Nord polar-night `#2e3440`, plain `#1e1e1e` IDE darks, plain `#0a0a0a` — these still need exactly the same atmosphere treatment as any other dark palette; they're not special-cased, they just fail the void test more often by default.

Light backgrounds are more forgiving. A flat `#faf7f5` reads as "paper" rather than "void," so the atmosphere requirement is softer — a hairline grid or warm gradient is still better, but flat is survivable.

**Visual weight signals importance.** Not every section deserves equal visual treatment. Executive summaries and key metrics should dominate the viewport on load (larger type, more padding, subtle accent-tinted background zone). Reference sections (file maps, dependency lists, decision logs) should be compact and stay out of the way. Use `<details>/<summary>` for sections that are useful but not primary — the collapsible pattern is in `./references/css-patterns.md`.

**Surface depth creates hierarchy.** Vary card depth to signal what matters. Hero sections get elevated shadows and accent-tinted backgrounds (`ve-card--hero` pattern). Body content stays flat (default `.ve-card`). Code blocks and secondary content feel recessed (`ve-card--recessed`). See the depth tiers in `./references/css-patterns.md`. Don't make everything elevated — when everything pops, nothing does.

**Animation earns its place.** Staggered fade-ins on page load are almost always worth it — they guide the eye through the diagram's hierarchy. Mix animation types by role: `fadeUp` for cards, `fadeScale` for KPIs and badges, `drawIn` for SVG connectors, `countUp` for hero numbers. Hover transitions on interactive-feeling elements make the diagram feel alive. Always respect `prefers-reduced-motion`. CSS transitions and keyframes handle most cases. For orchestrated multi-element sequences, anime.js via CDN is available (see `./references/libraries.md`).

**Forbidden animations:**
- Animated glowing box-shadows (`@keyframes glow { box-shadow: 0 0 20px... }`) — this is AI slop
- Pulsing/breathing effects on static content
- Continuous animations that run after page load (except for progress indicators)

Keep animations purposeful: entrance reveals, hover feedback, and user-initiated interactions. Nothing should glow or pulse on its own.

### 6. Deliver

**Output location:** Write to `~/.agent/diagrams/`. Use a descriptive filename based on content: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. The directory persists across sessions.

**Open in browser:**
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`

**Tell the user** the file path so they can re-open or share it.

## Diagram Types

### Architecture / System Diagrams
Two approaches depending on what matters more:

**Text-heavy overviews** (card content matters more than connections): CSS Grid with explicit row/column placement. Sections as rounded cards with colored borders and monospace labels. Vertical flow arrows between sections. Nested grids for subsystems. The reference template at `./templates/architecture.html` demonstrates this pattern. Use when cards need descriptions, code references, tool lists, or other rich content that Mermaid nodes can't hold.

**Topology-focused diagrams** (connections matter more than card content): **Use Mermaid.** A `graph TD` or `graph LR` with custom `themeVariables` produces proper diagrams with automatic edge routing. Use when the point is showing how components connect rather than describing what each component does in detail.

### Flowcharts / Pipelines
**Use Mermaid.** Automatic node positioning and edge routing produces proper diagrams with connecting lines, decision diamonds, and parallel branches — dramatically better than CSS flexbox with arrow characters. Use `graph TD` for top-down or `graph LR` for left-right. Color-code node types with Mermaid's `classDef` or rely on `themeVariables` for automatic styling.

### Sequence Diagrams
**Use Mermaid.** Lifelines, messages, activation boxes, notes, and loops all need automatic layout. Use Mermaid's `sequenceDiagram` syntax. Style actors and messages via CSS overrides on `.actor`, `.messageText`, `.activation` classes.

### Data Flow Diagrams
**Use Mermaid.** Data flow diagrams emphasize connections over boxes — exactly what Mermaid excels at. Use `graph LR` or `graph TD` with edge labels for data descriptions. Thicker, colored edges for primary flows. Source/sink nodes styled differently from transform nodes via Mermaid's `classDef`.

### Schema / ER Diagrams
**Use Mermaid.** Relationship lines between entities need automatic routing. Use Mermaid's `erDiagram` syntax with entity attributes. Style via `themeVariables` and CSS overrides on `.er.entityBox` and `.er.relationshipLine`.

### State Machines / Decision Trees
**Use Mermaid.** Use `stateDiagram-v2` for states with labeled transitions. Supports nested states, forks, joins, and notes. Decision trees can use `graph TD` with diamond decision nodes.

**`stateDiagram-v2` label caveat:** Transition labels have a strict parser — colons, parentheses, `<br/>`, HTML entities, and most special characters cause silent parse failures ("Syntax error in text"). If your labels need any of these (e.g., `cancel()`, `curate: true`, multi-line labels), use `flowchart LR` instead with rounded nodes and quoted edge labels (`|"label text"|`). Flowcharts handle all special characters and support `<br/>` for line breaks. Reserve `stateDiagram-v2` for simple single-word or plain-text labels.

### Mind Maps / Hierarchical Breakdowns
**Use Mermaid.** Use `mindmap` syntax for hierarchical branching from a root node. Mermaid handles the radial layout automatically. Style with `themeVariables` to control node colors at each depth level.

### Data Tables / Comparisons / Audits
Use a real `<table>` element — not CSS Grid pretending to be a table. Tables get accessibility, copy-paste behavior, and column alignment for free. The reference template at `./templates/data-table.html` demonstrates all patterns below.

**Use proactively.** Any time you'd render an ASCII box-drawing table in the terminal, generate an HTML table instead. This includes: requirement audits (request vs plan), feature comparisons, status reports, configuration matrices, test result summaries, dependency lists, permission tables, API endpoint inventories — any structured rows and columns.

Layout patterns:
- Sticky `<thead>` so headers stay visible when scrolling long tables
- Alternating row backgrounds via `tr:nth-child(even)` (subtle, 2-3% lightness shift)
- First column optionally sticky for wide tables with horizontal scroll
- Responsive wrapper with `overflow-x: auto` for tables wider than the viewport
- Column width hints via `<colgroup>` or `th` widths — let text-heavy columns breathe
- Row hover highlight for scanability

Status indicators (use styled `<span>` elements, never emoji):
- Match/pass/yes: colored dot or checkmark with green background
- Gap/fail/no: colored dot or cross with red background
- Partial/warning: amber indicator
- Neutral/info: dim text or muted badge

Cell content:
- Wrap long text naturally — don't truncate or force single-line
- Use `<code>` for technical references within cells
- Secondary detail text in `<small>` with dimmed color
- Keep numeric columns right-aligned with `tabular-nums`

### Timeline / Roadmap Views
Vertical or horizontal timeline with a central line (CSS pseudo-element). Phase markers as circles on the line. Content cards branching left/right (alternating) or all to one side. Date labels on the line. Color progression from past (muted) to future (vivid).

### Dashboard / Metrics Overview
Card grid layout. Hero numbers large and prominent. Sparklines via inline SVG `<polyline>`. Progress bars via CSS `linear-gradient` on a div. For real charts (bar, line, pie), use **Chart.js via CDN** (see `./references/libraries.md`). KPI cards with trend indicators (up/down arrows, percentage deltas).

## Slide Deck Mode

An alternative output format for presenting content as a magazine-quality slide presentation instead of a scrollable page. **Opt-in only** — the agent generates slides when the user invokes `/generate-slides`, passes `--slides` to an existing prompt (e.g., `/diff-review --slides`), or explicitly asks for a slide deck. Never auto-select slide format.

**Before generating slides**, read `./references/slide-patterns.md` (engine CSS, slide types, transitions, nav chrome, presets) and `./templates/slide-deck.html` (reference template showing all 10 types). Also read `./references/css-patterns.md` for shared patterns and `./references/libraries.md` for Mermaid/Chart.js theming.

**Slides are not pages reformatted.** They're a different medium. Each slide is exactly one viewport tall (100dvh) with no scrolling. Typography is 2–3× larger. Compositions are bolder. The agent composes a narrative arc (impact → context → deep dive → resolution) rather than mechanically paginating the source.

**Content completeness.** Changing the medium does not mean dropping content. Follow the "Planning a Deck from a Source Document" process in `slide-patterns.md` before writing any HTML: inventory the source, map every item to slides, verify coverage. Every section, decision, data point, specification, and collapsible detail from the source must appear in the deck. If a plan has 7 sections, the deck covers all 7. If there are 6 decisions, present all 6 — not the 2 that fit on one slide. Collapsible details in the source become their own slides. Add more slides rather than cutting content. A 22-slide deck that covers everything beats a 13-slide deck that looks polished but is missing 40% of the source.

**Slide types (10):** Title, Section Divider, Content, Split, Diagram, Dashboard, Table, Code, Quote, Full-Bleed. Each has a defined layout in `slide-patterns.md`. Content that exceeds a slide's density limit splits across multiple slides — never scrolls within a slide.

**Visual richness:** Use SVG decorative accents, per-slide background gradients, inline sparklines, and small Mermaid diagrams. Visual-first, text-second.

**Compositional variety:** Consecutive slides must vary spatial approach — centered, left-heavy, right-heavy, split, edge-aligned, full-bleed. Three centered slides in a row means push one off-axis.

**Curated presets:** Four slide-specific presets as starting points (Midnight Editorial, Warm Signal, Terminal Mono, Swiss Clean) plus the existing 8 aesthetic directions adapted for slides. Pick one and commit. See `slide-patterns.md` for preset CSS values.

**`--slides` flag on existing prompts:** When a user passes `--slides` to `/diff-review`, `/plan-review`, `/project-recap`, or other prompts, the agent gathers data using the prompt's normal data-gathering instructions, then presents the content as a slide deck instead of a scrollable page. The slide version tells the same story with different structure and pacing — but the same breadth of coverage. Don't use the slide format as an excuse to summarize or skip sections that the scrollable version would have included.

## File Structure

Every diagram is a single self-contained `.html` file. No external assets except CDN links (fonts, optional libraries). Structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties, theme, layout, components — all inline */
  </style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <!-- No script needed for static CSS-only diagrams -->
  <!-- Optional: <script> for Mermaid, Chart.js, or anime.js when used -->
</body>
</html>
```

## Quality Checks

Before delivering, grade against `references/quality-rubric.md`. The rubric has six weighted dimensions (Form-Audience Match, Story Discipline, Voice & Diction, Grounding, Visual Quality, Anti-Pattern Free). A passing output scores ≥ 75/100 with no FAIL on `script` or `hybrid` dimensions.

The fast-pass tests, in addition to the rubric:

- **Squint test:** blur your eyes. Hierarchy still readable? Sections distinct?
- **Swap test:** if the fonts and colors were replaced with a generic dark theme, would the page be indistinguishable from a template? If yes, push the aesthetic further.
- **Both themes:** light and dark both look intentional, not broken.
- **Void test (dark mode):** corner of the page and center are visually distinguishable. If not, add atmosphere.
- **Re-teaching audit:** walk every section. *"Does the reader already know this? If yes, why is it here?"*
- **Argument vs report:** can you summarize the page's spine in one sentence? Is the spine the right shape (claim for argument-led work, inventory for report-led work)?
- **Mermaid syntax review** (if the diagram uses Mermaid): scan every block against the parser-break list in `references/anti-patterns.md` §6 and `references/libraries.md` "Common Pitfalls".

The full anti-pattern library — typography, color, layout, animation, Mermaid syntax, form mismatch, voice modulation, content discipline, grounding — lives in `references/anti-patterns.md`. Read it before generating; re-read the relevant section while drafting if the page touches that category.

**Self-audit script.** For pages that make claims about real systems (file paths, table names, schema columns, framework definitions), run `scripts/strip-html.py <output.html> --stdout` to get a readable markdown rendering. Grep the result against the source repos to verify every named identifier exists. The grounding dimension of `quality-rubric.md` requires this for any output where fabricated identifiers would mislead the reader.

## Anti-Patterns

The full library lives in `references/anti-patterns.md` (10 categories, ~30 documented failure modes from real cc-viz runs). Read it. The summary you cannot skip:

- **Typography:** no Inter or Inter variants as `--font-body`; no italic-by-design display serifs as body; numerals use mono with `tabular-nums`, not display serif italic.
- **Color:** no Tailwind purple/violet/indigo defaults; no gradient text on headings; no flat solid dark backgrounds (atmosphere required).
- **Layout:** no symmetric mirrors; no three-dot window chrome on code blocks; no card grid orphan rows; no multi-column sentence-break (use `break-inside: avoid-column`); no italic-emphasis stacking; no `<pre>` for pull quotes.
- **Animation:** no glowing pulsing shadows; no opacity-0 stuck state if entry animation skips.
- **Mermaid:** quote dotted-edge labels with periods; avoid colons/parens/`<br/>` in `stateDiagram-v2`; no `{}` `[]` `<>` `&` in sequence messages.
- **Form & structure:** no Frankenstein form mixing; match form to content shape; no prior-draft bleed; no default-option blindness in decision documents.
- **Grounding:** no fabricated table/file names; no training-stale claims about external state; ground time estimates in observed velocity.

Every pattern in `references/anti-patterns.md` lists: name, what happens, why it's bad, the rule, the fix, and a regex check where applicable.
