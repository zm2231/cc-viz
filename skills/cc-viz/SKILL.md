---
name: cc-viz
description: Generate self-contained HTML pages that visually explain systems, code, plans, and data. Produces documents, briefs, memos, diagrams, audits, recaps, comparison tables, slide decks, multi-doc sites. Triggers: "diagram", "visualize", "render as a page", "build a brief", "memo for the team", "deck about", "audit", "recap", "fact-check", "plan review", "diff review", "small site I'll edit". Also fires proactively when about to render an ASCII table with 4+ rows or 3+ columns (generate HTML instead). NOT for applications, interactive UIs, landing pages, brand sites, dashboards-as-products, or component libraries. NOT for one-line answers, tiny markdown tables, code-as-artifact responses, or discussion-not-document conversations.
license: MIT
compatibility: Requires a browser to view generated HTML files.
metadata:
  version: "1.2.0"
---

# cc-viz

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask. Render it as HTML automatically and tell them the file path. Brief text summary in the chat is fine; the table itself is the HTML page. Proactive tables are implicitly **Quick share mode** — skip routing and framing, just ship the table.

## When NOT to use cc-viz

Skill mis-fires are nearly as bad as not firing at all. Don't generate an HTML page when:

- **Small tables** — ≤3 rows or ≤2 columns. A markdown table in chat is the right answer.
- **One-line or short-paragraph answers** — if the response fits in 3 chat lines, ship it as chat. Don't paginate prose into HTML.
- **Code is the artifact** — when the user asks for a function, a config, a script, the code goes in chat or a file, not wrapped in an HTML page.
- **Discussion, not document** — when the user is thinking through a problem with you, finish the discussion before generating anything. Mid-conversation HTML pages interrupt the reasoning.
- **Marketing / UI / brand sites** — landing pages, app shells, dashboards-as-products, component libraries are out of scope. Different skill, different output shape.
- **Trivial confirmations** — "yes that works", "looks good", "shipped" don't need a styled page.

If unsure, ask one short question before generating, or default to chat. A page that should have been chat is a worse failure than chat that should have been a page.

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

**Skip 0.5 entirely when invoked mid-session with rich context from prior turns.** If you've been working on a subject for an hour and the user asks for a page about it, the audience and form are already known. Don't ask. Asking what conversation context already answers feels like a wizard.

### 0.7. Load accumulated judgment (if present)

Before drafting, check for `.cc-viz/context.md` in the project root. **Most invocations won't have one** — don't expect it. When it exists, it was created intentionally by the user after a few iterations on this project, and it captures: typical audience, register preferences, anti-pattern history, prior decisions about form, accumulated diction notes, things to never repeat.

If present, read it and apply. If absent, proceed normally.

**Writing back.** At the end of a session, if something non-obvious got established (an aesthetic that landed, a phrase that didn't, an audience preference, a font that worked) — and the user gives a signal the work will continue (multiple iterations, "next time", "for future runs") — offer to create or update `.cc-viz/context.md` with one or two lines capturing the lesson. Don't write back unprompted on a one-off run; the file should accumulate slowly, not bloat.

### 1. Frame the story (before anything visual)

Five gates. All five must be filled before Step 2. Skipping them is the most common cc-viz failure: agent jumps from source to HTML, page becomes a list of facts in boxes. Gate 5 only applies when the audience is non-expert in the subject; skip it for peer-audience pages.

**Gate 1 — Spine sentence (REQUIRED, fill the blank before continuing):**

> *"[Subject] [does / is / argues] [X]. [Why-it-matters clause]."*

Examples:
- *"context-layer was built to extract a four-dimension framework but quietly invented two things the framework hasn't named yet: system metacognition and source-level epistemics. The interesting question is whether they generalize."*
- *"Dennis is gone and the SOW is an orphan, but the systems intelligence is real. Here's what we actually need to know to proposal this correctly."*
- *"The migration cuts query p99 latency by 40% but introduces a backfill window we have to plan for."*

If you can't write the spine sentence in 10 seconds, stop. Re-read the source. Don't proceed until the sentence is on the page (literally, in your draft notes, before you write any HTML).

**Gate 2 — Ground claims.** Speculation reads identical to truth on the page; only the reader who knows the territory can tell the difference. Any page making claims about a real system, project, or decision must be grounded in evidence first. Adjust depth to the routed mode (Quick share = lean on what's loaded; Internal brief = thorough; External deliverable = exhaustive). Never skip entirely. Methodology: `references/story-framing.md`.

> **Context-rich escape.** If the session has already loaded the source material (you've been reading transcripts, files, docs for this subject for the last 30+ minutes), Gate 2 is satisfied. Don't re-fetch what's already in context. Re-verify only specific claims that feel uncertain or that came from memory rather than the loaded context.

**Gate 3 — Report vs argument.** Most analytical work is argument-led: artifacts (files, columns, schema, citations) are *evidence FOR a claim*, not the claim itself. A page listing "these files exist, these columns exist, this maps to that" has shown evidence but not told a story. If the page's spine is a matrix, decide: catalog intent (report) or claim about the catalog (argument)? Argument-led pages lead with the claim, support each section with the evidence that defends it, close with the implication.

**Gate 4 — Re-teaching audit.** List in your head (or notes) what the reader *already knows* from the conversation, the project, or their role. Any section that re-teaches that list is decoration. Cut it. A page mapping context-layer to a framework should NOT re-introduce what context-layer is to someone who built it; it should foreground the *mapping*, which is the new thing. Re-teaching is the most common failure for pages that look thorough but feel flat.

**Gate 5 — Translation audit.** When the audience is non-expert in the subject (non-coders reading about a dev tool, executives reading about a system, customers reading about engineering work), translate at three levels, not one:

1. **Vocabulary:** swap technical terms for plain analogues (worktree → sealed room, YAML → recipe, orchestrator → kitchen line).
2. **Framing:** the *category* of thing you're describing must come from their world, not yours. *"Running a small operation through ChatGPT"* assumes business-operator framing; *"software teams"* assumes professional context. Both fail for a general community audience. Pick framings the reader already lives inside.
3. **Examples and aspirations:** every example, every "if you've been feeling…" hook, every comparison must point at a situation the reader has actually been in. If the example needs translation, the example is wrong — pick a different one.

The most common Gate-5 failure is translating vocabulary while leaving framing and examples in the original audience's world. The page reads like a tech doc with the words swapped, not a piece written for the reader from scratch.

**Audience, register, baseline** — name the audience concretely (not "technical reader" but "senior backend engineer who knows our stack but hasn't seen this subsystem"), pick one register and hold it. Full taxonomy and baseline discipline in `references/story-framing.md`.

**Voice & diction rules** — non-negotiable, even in Quick share mode. Full set in `references/voice-and-diction.md`:

- No em dashes (`—`) in body prose. Strongest single AI tell. Citations only.
- Sentences ≤22 words; paragraphs ≤3 sentences. One technical-precision exception per page.
- Direct address (*you / your*) only when the reader is an actor (system behavior, touchpoints, consequences). Not in meta-framing.
- One italic-emphasis point per heading, per pull quote, per card. Italic is a budget, not a default.
- No yap. Cut every hedge-starting sentence. Trim before commit.

### 2. Pick a form, commit fully

Form precedes aesthetic. Pick one form's structural vocabulary and commit. Frankensteins read as half-finished: a board-memo recommendation card grafted onto a magazine drop-cap, a slide-deck hero pasted above a dashboard grid.

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

Pick based on routed intent (Step 0) and framed audience/register (Step 1). If two forms could plausibly fit, pick the one that does the audience's reading work for them: the form that lets them read in three minutes what would take ten in another form.

**Anti-Frankenstein rule.** Once the form is chosen, every element on the page serves that form. The form's structural vocabulary is the only structural vocabulary you use.

**Patterns that have landed.** Before inventing new composition, check `references/patterns.md`. It catalogs specific cc-viz forms that worked in real runs (status strip + recommendation card, three-column kicker masthead, etc.) with markup examples. A pattern that's worked before is more likely to work again than a freshly invented one.

**Tabs vs scrolling.** Tabs are right when content has 3+ distinct lenses on the same subject (who / what / how / when, or technical / business / risk / next-steps). 4–5 is the sweet spot; ≥6 means the lenses aren't actually distinct, fold some together. Tabs are wrong when content flows linearly (intro → context → analysis → recommendation): use a single scrolling page. For side-by-side comparison, use a two-column layout instead.

**Serif body vs sans body.** Reading-serif body (Source Serif 4, Lora, Newsreader) is the strongest "document" signal. Use it when body is paragraphs of prose (memos, briefs, analyses, recaps). Sans body (IBM Plex Sans, DM Sans) is right when body is dense cards, short labels, tables, or status indicators where a serif at 13–14px feels slow. Don't force serif body on a card-heavy page; the form decides.

### 3. Aesthetic (5 seconds, not 5 minutes)

Commit to a visual direction. Don't default to "dark theme with blue accents" every time. Vary from recent generations.

**Aesthetic serves the form's reading task; memorability is a side effect, not the goal.** A cc-viz page exists to be read, scanned, and acted on. If you find yourself reaching for spectacle (dramatic shadows, gradient meshes, noise grain, oversized hero typography for the sake of impact), you're designing a brand site, not a document. Pull back. Form-fit produces memorability on its own when the fit is high.

**Constrained aesthetics (prefer):** their specific requirements prevent generic output.
- **Blueprint:** technical drawing feel, subtle grid background, deep slate/blue, monospace labels, precise borders
- **Editorial:** serif headlines (Instrument Serif / Crimson Pro), generous whitespace, muted earth tones or deep navy + gold
- **Paper/ink:** warm cream `#faf7f5`, terracotta/sage accents, informal feel
- **Monochrome terminal:** green/amber on near-black, monospace everything, CRT glow optional

**Flexible aesthetics (use with discipline):** IDE-inspired (borrow a real named scheme — Dracula, Nord, Catppuccin, Solarized, Gruvbox, One Dark, Rosé Pine — and commit to the actual palette); data-dense (small type, tight spacing, muted colors).

**Forbidden.** Neon dashboard (cyan + magenta + purple on dark) is always AI slop. Same for gradient mesh (pink/purple/cyan blobs) and Inter + violet/indigo + gradient text.

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

**Mermaid theming, zoom controls, and class-collision constraints** all live in `references/libraries.md` and `references/css-patterns.md`. Three rules to remember inline: (1) `theme: 'base'` with custom `themeVariables`, never the default; (2) zoom controls require `target.style.zoom` on the `.mermaid` div (not transform, not SVG width); (3) never define `.node` as a page-level CSS class. Mermaid uses it internally; scope under `.mermaid` only.

### 5. Style

Apply these inline rules; reach for the references for detail.

**Typography.** Pick a font pairing from `./references/libraries.md`. Vary from recent generations. cc-viz outputs should read as documents, not brand sites or landing pages. The font list and bans reflect that.
- **Forbidden as `--font-body`:** Inter (and any Inter variant: Tight, Display, etc.), Roboto, Arial, Helvetica, system-ui alone, **Space Grotesk, Manrope, General Sans, Cabinet Grotesk** (current-decade AI-startup landing-page tells), italic-by-design display serifs (Instrument Serif, Playfair Italic, Fraunces Italic). Display serifs go in `--font-display`, never `--font-body`.
- **Strongest cc-viz signal:** reading-serif body pairings (Source Serif 4, Lora, Newsreader; pairings 14/15/16 in libraries.md). Long-form body serifs almost never appear on landing pages; they read as "report" immediately.

**Color.** CSS custom properties for the full palette. Define at minimum `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, 3-5 semantic accents. Both themes (light + dark) intentional.
- **Forbidden accents:** `#8b5cf6` `#7c3aed` `#a78bfa` `#d946ef`, the cyan-magenta-pink combination. Tailwind defaults signaling zero design intent.

**Atmosphere is mandatory in dark mode** (also recommended in light). Flat backgrounds produce a void with text floating on it. The void test: corner vs. center distinguishable? If not, fix it.

**Prefer reading-friendly atmospheres** — they support the document register:
- Faint dot or hairline grid (1–3% opacity)
- Fine paper texture (subtle warm tint variation)
- Subtle vignette darkening at corners
- Two-stop gradient with very low contrast (≤4% lightness shift)

**Skip spectacle atmospheres** — they pull the page toward "brand site" feel:
- Gradient meshes (multiple overlapping radial color blobs)
- Large radial glows behind the hero (more than 25% of the viewport)
- Noise / film grain overlays
- Dramatic depth via layered drop shadows on the page background

**Visual weight + surface depth.** Hero sections elevated (accent-tinted, larger type). Body content flat. Code/secondary recessed. `<details>/<summary>` for useful-but-not-primary content. Detail in `references/css-patterns.md`.

**Animation earns its place.** Staggered fade-ins guide the eye through hierarchy. Mix `fadeUp` / `fadeScale` / `drawIn` / `countUp` by role. Respect `prefers-reduced-motion`.
- **Forbidden:** glowing/pulsing box-shadows (`@keyframes glow` is AI slop), continuous animations after page load, opacity-0 stuck state if entry animation skips.

### 6. Deliver

**Output location:** `~/.agent/diagrams/`. Descriptive filename: `modem-architecture.html`, `pipeline-flow.html`, `schema-overview.html`. Directory persists across sessions. For multi-doc sites: a folder, `~/.agent/diagrams/<site-name>/`.

**Always open in the browser after writing.** Required, not optional.
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`
- Multi-doc: open `index.html` from the folder.

After opening, **tell the user** the absolute file path so they can re-open, attach, or share.

**Share / handoff (mode-conditional):**

- **Quick share / internal brief / memo:** state the path. The user opens or attaches as they need.
- **External / client deliverable:** ask whether the user wants it published before handing off. If yes and the surface has shell access, offer the wrangler/vercel options from `references/multi-doc-site.md`. If no, just hand off the path.
- **Multi-doc site:** open `index.html`; publish options in `references/multi-doc-site.md`.

Don't auto-publish. Generation and distribution are different concerns; the user decides where the artifact goes.

## Diagram-specific notes

Most diagram types are routed through Mermaid (see Step 4 table). Notes that don't fit the table:

**Architecture / system.** Two approaches. *Text-heavy overviews* (card content > connections) → CSS Grid with explicit row/column placement, rounded cards with colored borders, monospace labels, vertical flow arrows, nested grids for subsystems (`./templates/architecture.html`). *Topology-focused* (connections > card content) → Mermaid `graph TD` / `graph LR` with custom `themeVariables`.

**State machines.** `stateDiagram-v2` has a strict parser: colons, parens, `<br/>`, and HTML entities cause silent parse failures. If labels need any of these (e.g., `cancel()`, `curate: true`, multi-line), use `flowchart LR` with quoted edge labels (`|"label text"|`) instead. Reserve `stateDiagram-v2` for plain-text labels.

**Data tables.** Real `<table>`, not CSS-Grid-pretending. Sticky `<thead>`, alternating row backgrounds, optionally sticky first column, responsive `overflow-x: auto`, column-width hints, row-hover. Status as styled `<span>`, never emoji. Detail + reference in `./templates/data-table.html`.

**Timeline.** Vertical or horizontal with a CSS pseudo-element line. Phase markers as circles on the line. Cards alternating or single-side. Color progression from past (muted) to future (vivid).

**Dashboard.** Card grid with hero numbers. Sparklines via inline SVG `<polyline>`. Progress bars via CSS gradient. Real charts via Chart.js (CDN — see `references/libraries.md`). KPI cards with trend indicators.

## Slide Deck Mode

**When to choose slides.** Slides are right when the artifact will be shown live (presentation, walkthrough, talk, demo, community session) or when the user explicitly asks for a deck. Trigger words that justify auto-selecting slides: *"deck about"*, *"presenting"*, *"showing tomorrow"*, *"walk them through"*, *"talk on"*, *"slides for"*, or the `--slides` / `/generate-slides` invocation. Live-delivery context is a valid signal — don't refuse to pick slides just because the user said "brief" if they also said "showing tomorrow."

**When NOT to choose slides.** A document meant for asynchronous reading (memo, audit, RFC, recap, status report) is a scrolling page, not a deck. If the user says "brief" or "memo" without any live-delivery context, default to scrolling. If genuinely ambiguous between brief and deck, ask one question.

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

Grade against the rubric inline before delivering. Six weighted dimensions, 100 points total. Passing score **≥ 75/100** with no FAIL on `script` or `hybrid` dimensions. Full criteria in `references/quality-rubric.md`.

| # | Dimension | Pts | What it checks |
|---|---|---|---|
| 1 | **Form-Audience Match** | 25 | Right form for the routed intent + framed audience? Re-teaching audit passed? **Translation audit passed (Gate 5) if non-expert audience?** Tabs vs scroll vs side-by-side chosen correctly? |
| 2 | **Story Discipline** | 20 | Spine sentence written? Argument vs report decided? Each section advances or supports the spine? No decoration sections? |
| 3 | **Voice & Diction** | 15 | Zero em-dashes in body prose. Sentences ≤22 words. No yap. One italic per heading max. Direct address only when reader is an actor. **Pre-ship grep required (see below).** |
| 4 | **Grounding** | 15 | Claims sourced. Names, dates, paths, numbers verifiable. `scripts/strip-html.py` + grep against source confirms (for system-claim pages). |
| 5 | **Visual Quality** | 15 | Typography distinctive. Atmosphere present (void test). Both themes intentional. No anti-patterns from `references/anti-patterns.md`. |
| 6 | **Anti-Pattern Free** | 10 | No Frankenstein form mixing. No forbidden fonts/colors/animations. No glow/pulse. No gradient text. No three-dot code chrome. |

If you score yourself below 75, don't ship. Fix the lowest dimension first. Inflated self-grading is also a failure mode: if you're scoring 78 with re-teaching present or no spine statement, you're grading lenient. The dimensions that matter most for argument-led pages are #1 and #2. A page with beautiful typography (#5) still fails if the spine is missing.

**Pre-ship text checks (Bash, before opening browser).** Run these from the shell. Visual inspection is unreliable across surfaces; text checks are not. If shell is available, every page goes through these before delivery.

```bash
# 1. Em-dash audit. Should return only structural uses (titles, citations, list labels).
#    Any em-dash inside a paragraph or sentence is a fail.
grep -n "—" ~/.agent/diagrams/<file>.html

# 2. Forbidden body fonts.
grep -niE "font-body:[^;]*\b(Inter|Roboto|Arial|Helvetica|Space Grotesk|Manrope|General Sans|Cabinet Grotesk)\b" ~/.agent/diagrams/<file>.html

# 3. Forbidden accent colors (Tailwind defaults).
grep -niE "#(8b5cf6|7c3aed|a78bfa|d946ef|06b6d4)" ~/.agent/diagrams/<file>.html

# 4. Mermaid post-processing present (only for pages using Mermaid).
grep -c "mermaid.run().then" ~/.agent/diagrams/<file>.html

# 5. Atmosphere present (any of: gradient, dot grid, hairline, vignette).
grep -ciE "radial-gradient|linear-gradient|repeating-linear-gradient|background-image" ~/.agent/diagrams/<file>.html
```

If any check returns a hit you didn't intend, fix it before opening. Inspecting em-dashes by reading is unreliable; grep is not.

Fast-pass tests:
- **Squint:** hierarchy still readable when blurred? Sections distinct?
- **Swap:** replace your styling with a generic dark theme. Would anyone notice?
- **Both themes:** light and dark both intentional, not broken.
- **Void (dark mode):** corner vs. center visually distinguishable.
- **Re-teaching audit:** *"Does the reader already know this? If yes, why is it here?"* for every section.
- **Argument vs report:** can you summarize the spine in one sentence? Right shape (claim for argument, inventory for report)?
- **Mermaid syntax:** scan against the parser-break list in `references/anti-patterns.md` §6 and `references/libraries.md` "Common Pitfalls".

**Self-audit script.** For pages claiming things about real systems (file paths, table names, schema columns, framework definitions), run `scripts/strip-html.py <output.html> --stdout` and grep the result against the source repos. The grounding rubric dimension requires this.

## Anti-Patterns

Full library: `references/anti-patterns.md` (10 categories, ~30 documented failure modes). Read before generating; re-read the relevant section while drafting if the page touches that category.
