# cc-viz Anti-Patterns

Concrete failure modes observed in real cc-viz runs, organized by category. Every pattern listed here has fired at least once and required correction. If you find yourself about to do the thing in the **What happens** column, stop and apply the **Rule**.

Read this before generating. Re-read the relevant section while drafting if the page touches that category.

---

## 1. Diction & voice

### 1.1 Em dashes in body prose
**What happens:** *"L1, added in Phase 5, is an agent that calls 11 substrate tools — and that loop is how the conditional ridge becomes legible."* The interruption-em-dash pattern appears in nearly every LLM-authored paragraph.
**Why bad:** Single strongest AI tell in 2026. Reads as machine cadence, regardless of how good the rest of the prose is.
**Rule:** Zero em dashes (`—`) in body prose. Allowed only in citation lines (`— Author, Source`).
**Fix:** Replace with a period, comma, parentheses, or rephrase.
**Script check:** `grep -c '—' <body-prose>` — should be zero outside citation/cite elements.

### 1.2 Marketing slop vocabulary
**What happens:** *"This robust, scalable solution leverages cutting-edge AI to seamlessly unlock comprehensive insights."*
**Why bad:** The vocabulary is generic across thousands of LLM outputs. Reads as content-marketing template.
**Rule:** Forbidden in body prose: *leverage, unlock, robust, seamless, powerful, intuitive, comprehensive, elegant, harness, delve, in essence, at its core, cutting-edge, state-of-the-art, various, numerous, multiple, several, essentially, basically, very, really, quite, incredibly, extremely.*
**Fix:** Use concrete verbs and specific nouns. *"This stack handles 27,309 events through one Worker"* > *"This robust solution comprehensively processes events."*
**Script check:** regex against the forbidden list, case-insensitive, word boundaries.

### 1.3 Adjective stacking
**What happens:** *"A robust, scalable, modern architecture..."* / *"Clean, intuitive, powerful UX..."*
**Why bad:** Three-adjective strings are a tell. They substitute volume for precision.
**Rule:** No string of three adjectives in a row.
**Fix:** Pick one adjective that earns its place. Cut the other two.

### 1.4 Hedge-starting sentences
**What happens:** *"It's worth noting that the system is in production."* / *"In essence, the layer is a classifier."* / *"Generally speaking, this is the canonical case."*
**Why bad:** The sentence after the hedge is usually fine; the hedge is yap.
**Rule:** Cut every sentence that opens with *"It's worth noting that"*, *"In essence,"*, *"Generally speaking,"*, *"To be clear,"*, *"As we've seen,"*, *"Of course,"*.
**Fix:** Drop the hedge, keep the rest.

### 1.5 Restating the visual in prose
**What happens:** A diagram shows L1 → L1.5 → L2 → L3, and the prose underneath says *"First L1 runs, then L1.5 runs, then L2 runs, then L3 runs."*
**Why bad:** Doubles the read time without adding meaning. Prose should add what the diagram cannot show: the *why*, the constraint, the gotcha.
**Rule:** Prose under a visual adds the why or the qualification, not a verbal version of the visual.
**Fix:** Ask, for each prose paragraph adjacent to a visual: *"What does this say that the visual doesn't?"* If nothing, cut it.

---

## 2. Typography

### 2.1 Inter or any Inter variant as `--font-body`
**What happens:** Subagent picks "Inter Tight" or "Inter Display" thinking it's a different font.
**Why bad:** Inter is the most overused AI default. Variants are still Inter.
**Rule:** No Inter, Inter Tight, Inter Display, Inter Pro, or any other Inter cut as `--font-body`.
**Fix:** Pick from the approved pairings in `libraries.md` (DM Sans, IBM Plex Sans, Bricolage Grotesque, Plus Jakarta Sans, Sora, Fraunces with sans body, etc.).
**Script check:** `grep -i 'Inter[\s,]' <css>` should not match `--font-body` declarations.

### 2.2 Italic-by-design display serif as `--font-body`
**What happens:** Subagent uses Instrument Serif, Playfair Display Italic, Fraunces Italic, or EB Garamond Italic for body paragraphs.
**Why bad:** These are exquisite for headlines. Unreadable as paragraph body. Italic at body size loses x-height clarity.
**Rule:** Italic-by-design display serifs may appear as `--font-display` only. Pair with a sans body and a mono.
**Fix:** Tri-font pairing. Display serif for h1/h2/pull-quote; sans for body; mono for labels.

### 2.3 Numbers in display-serif italic
**What happens:** KPI strip with "27,309" set in Fraunces italic 36px.
**Why bad:** Numerals in display-serif italic read as decorative, not data. The eye expects tabular numerals for tabular data.
**Rule:** Numerical figures in stat strips, KPI cards, comparison columns, or tabular data use mono or sans with `font-variant-numeric: tabular-nums`.
**Fix:** Switch the `.num` or `.kpi` CSS to `font-family: var(--font-mono); font-variant-numeric: tabular-nums;`.

### 2.4 Drop-cap at theatrical scale
**What happens:** `font-size: 7.5em` drop-cap.
**Why bad:** Reads as performative, not editorial. Crowds the surrounding column.
**Rule:** Editorial drop-caps cap at 5–6em without an explicit reason.
**Fix:** `font-size: 5em; line-height: 0.86;` is the safe upper bound.

---

## 3. Color & background

### 3.1 Tailwind default purple/violet/indigo accents
**What happens:** Subagent picks `#8b5cf6`, `#7c3aed`, `#a78bfa`, `#d946ef`, or "indigo-500" range.
**Why bad:** These are the Tailwind defaults that signal zero design intent.
**Rule:** Forbidden accent colors: `#8b5cf6`, `#7c3aed`, `#a78bfa`, `#d946ef`, the indigo/violet Tailwind range, the cyan-magenta-pink neon combination.
**Fix:** Use approved palettes from `css-patterns.md` (terracotta+sage, teal+slate, rose+cranberry, amber+emerald, deep blue+gold) or derive from real IDE themes (Dracula, Nord, Solarized, Gruvbox, Catppuccin).

### 3.2 Gradient text on headings
**What happens:** `background: linear-gradient(...); -webkit-background-clip: text;` on h1.
**Why bad:** Screams AI-generated. Used in approximately every LLM-produced landing page.
**Rule:** No gradient text on headings, ever.
**Fix:** Solid color or italic emphasis for h1 accents.

### 3.3 Flat solid dark background
**What happens:** Page renders with `background: #2e3440` (Nord polar-night), `#1e1e1e`, or `#0a0a0a` and nothing else.
**Why bad:** Produces a void. Text floats with no atmosphere.
**Rule:** Dark mode bg MUST have one of: subtle two-stop gradient, faint dot/hairline grid pattern, vignette overlay, focal accent radial glow.
**Fix:** Pass the **void test** — stand back from the screen, look at the corner vs the center. If you can't tell them apart, you have a void; add atmosphere.
**Note:** Nord polar-night `#2e3440`, plain `#1e1e1e` IDE darks, and `#0a0a0a` fail this most often. Same rule applies to all dark palettes; Nord just fails by default more often than others.

### 3.4 Animated glowing box-shadows
**What happens:** `@keyframes glow { box-shadow: 0 0 20px var(--accent); }` on cards.
**Why bad:** AI slop. Pulsing/breathing on static content adds nothing.
**Rule:** No animated glowing shadows. No continuous animations after page load except progress indicators.
**Fix:** Static border or static box-shadow. Earn animations on entrance reveals or hover only.

---

## 4. Layout

### 4.1 Symmetric mirror layouts
**What happens:** Left half and right half are perfect mirrors, every card identical, uniform padding everywhere.
**Why bad:** No hierarchy, no focal point. Reads as template.
**Rule:** Vary visual weight. Hero sections dominate. Reference sections stay compact. Asymmetric beats symmetric for diagrams.
**Fix:** Use depth tiers (hero > elevated > default > recessed) on cards. Vary card padding by importance.

### 4.2 Three-dot window chrome on code blocks
**What happens:** Code block topped with red/yellow/green dots mimicking macOS window chrome.
**Why bad:** Cliché. Used in approximately every LLM landing page since 2023.
**Rule:** No three-dot window chrome on code blocks.
**Fix:** Plain code block with filename or language label in the corner.

### 4.3 Card grid orphan rows
**What happens:** 4 cards in a grid that auto-fits to 3 columns at the viewport width. Produces 3 cards on top and 1 lonely orphan beneath.
**Why bad:** Looks broken. Asymmetric without intent.
**Rule:** Match column count to item count. 4 items → 2×2 or 4×1. 5 items → reorganize content. 6 items → 2×3 or 3×2.
**Fix:** Force `grid-template-columns: repeat(2, 1fr)` for 4-item grids, or restructure content.

### 4.4 Multi-column sentence-break
**What happens:** Two-column or three-column body has a paragraph that splits a sentence across columns: left column ends *"Not a developer"* and right column starts *"marketplace."*
**Why bad:** Typesetting failure. Sentence integrity broken.
**Rule:** Any element using `column-count` or `column-fill` must apply `break-inside: avoid-column` to its paragraph descendants.
**Fix:** `.column-container p { break-inside: avoid-column; }`.

### 4.5 Italic-emphasis stacking
**What happens:** Hero has *italic do* and *italic do* twice in the same heading, plus an italic phrase in the lede underneath, all in the same accent color.
**Why bad:** Multiple emphases compete and dilute. Reads as theatrical.
**Rule:** Single italic-emphasis point per heading, per pull quote, per card. The lede gets one accent point or the heading gets one, not both.
**Fix:** Pick one phrase to emphasize. Cut the others. The reader's eye should land on exactly one accent point per element.

### 4.6 Pull quote in `<pre>`
**What happens:** Pull quote markup is `<pre class="pull">"text..."</pre>` with the citation on a new line.
**Why bad:** `<pre>` preserves whitespace and forces monospace by default. The trailing newline pushes the left-rule bar past the text, producing an over-extended bar.
**Rule:** Pull quotes use `<blockquote class="pull">` with inner `<p>` and `<cite>`. Padding in `em` units so the bar tracks text height.
**Fix:** `<blockquote class="pull"><p>...</p><cite>— Source</cite></blockquote>` with `padding: 0.25em 0 0.25em 1.25em`.

### 4.7 Letter-in-circle centering via `line-height`
**What happens:** Letter inside a circular badge uses `line-height: 22px` to center vertically, but font baseline drift makes glyphs visually off-center.
**Why bad:** Different glyphs (D, P, C, M) have different visual centers. line-height tricks fail unevenly.
**Rule:** Use `display: inline-flex; align-items: center; justify-content: center` for letter-in-circle centering.
**Fix:**
```css
.dot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px; height: 22px;
  font-family: var(--font-mono);
  font-size: 10px;
  line-height: 1;
}
```

---

## 5. Animation

### 5.1 Opacity-0 stuck state when entry animation fails
**What happens:** Page uses `@keyframes fadeUp { from { opacity: 0; } }` with `animation: fadeUp 0.5s both;`. The animation never fires (WKWebView quirk, `prefers-reduced-motion: reduce`, JS race), and the content stays at `opacity: 0`. Page renders empty.
**Why bad:** Page looks broken in a non-trivial fraction of viewing environments (cmux, screen readers, low-power mode).
**Rule:** Animation visibility fallback. The end state must be reachable without the animation firing. Either use `animation-fill-mode: forwards` and trust the keyframe end state, OR initialize the element at the visible state and let the animation animate FROM the hidden state on a delay.
**Fix:** Either:
- `.fade { opacity: 1; animation: fadeUp 0.5s both; }` (start visible, animation runs and ends visible; if anim skips, still visible).
- Or: feature-detect `prefers-reduced-motion` and skip the initial-hidden state.

---

## 6. Mermaid syntax

These break the parser silently and produce "Syntax error in text mermaid version X" — there is no partial render.

### 6.1 Dotted edge labels with periods
**What happens:** `A -.below 0.60.-> B` parses as `-.below 0.` (label = "below 0") then garbage.
**Rule:** Quote dotted-edge labels containing any `.`, decimal, ellipsis: `A -. "below 0.60" .-> B`.
**Same applies:** thick edges with `=` or `.`: `A == "step.5" ==> B`.

### 6.2 `stateDiagram-v2` transition labels with special chars
**What happens:** `state A --> state B : cancel()` breaks the parser (parens). `state A --> state B : foo<br/>bar` breaks (br tag).
**Rule:** Avoid colons (after the first delimiter), parens, `<br/>`, HTML entities in `stateDiagram-v2` transition labels.
**Fix:** Use `flowchart LR` with quoted labels (`-->|"text with: special chars"|`) when labels need any of these.

### 6.3 Sequence diagram messages with `{}`, `[]`, `<>`, `&`
**What happens:** `A->>B: web_search({queries: [...]})` breaks the parser AND causes the entire diagram to render as raw text.
**Rule:** Sequence diagram messages are plain text only. No braces, brackets, angle brackets, ampersands.
**Fix:** Rephrase as plain English: `A->>B: Call web_search with queries`.

### 6.4 Pipe inside flowchart label
**What happens:** `A -->|foo|bar| B` — pipes are the edge-label delimiter; literal pipes break it.
**Rule:** Use `#124;` HTML entity, or rephrase to avoid the literal pipe.

### 6.5 Reserved word as node ID
**What happens:** `end --> next` — `end` is a reserved word in Mermaid for subgraph closing.
**Rule:** Don't use `end`, `class`, `subgraph`, `direction` as node IDs. Suffix or rename.

---

## 7. Form & structure

### 7.1 Frankenstein form mixing
**What happens:** A board-memo recommendation card grafted into a magazine spread. A magazine drop-cap inside a notebook. A dashboard KPI strip inside a slide-deck.
**Why bad:** Mixed structural vocabulary reads as half-finished. The page feels like two designers worked on it without speaking.
**Rule:** Once the form is chosen in Step 2, every element on the page must serve that form. No exceptions.
**Fix:** If you find a Frankenstein, either change the whole page to the form the offending element belongs to, or change the element to match the chosen form.

### 7.2 Form mismatched to content shape
**What happens:** Magazine editorial picked for matrix-shaped structural-mapping content. Data journalism picked for an argument-led decision memo.
**Why bad:** The form's structural vocabulary fights the content. Form is wrong before any element is wrong.
**Rule:** Match form to content shape. Matrix-shaped content → data journalism or topology. Argument-led content → position memo or magazine editorial. Decision-oriented content → board memo. Personal/working-notes → notebook spread.
**Fix:** Re-route at Step 2. The wrong form is unrecoverable through other improvements.

### 7.3 Reporting when intent was argument
**What happens:** Page presents a feature inventory or matrix as the spine, with conceptual claims appearing as footnotes underneath. Reader walks away with a list of facts, not a position.
**Why bad:** The artifacts (files, columns, citations) should be evidence FOR a claim. When they're the spine, the page is a report. For analytical/mapping/synthesis/decision work, that's the wrong shape.
**Rule:** For argument-led intent: lead with the load-bearing claim, support each section with evidence that defends it, close with the implication. The matrix may appear as one supporting element under a claim, not as the page's backbone.
**Fix:** Restructure. The first section is the claim, not the inventory.

### 7.4 Prior-draft bleed
**What happens:** Body prose contains *"the original brief"*, *"the previous version"*, *"the corrected take"*, *"now that we know better"*, *"as we discussed earlier"*.
**Why bad:** Tells the reader they're reading version N of N rather than the only document. Reads as a working note, not a deliverable.
**Rule:** Each draft reads as the only document that has ever existed.
**Fix:** Remove all prior-version references. The reader who picks this up has no prior context.

### 7.5 Default-option blindness
**What happens:** A decision memo about what to do with a stalled product surfaces only kill / ship / repurpose. Misses out-of-the-box options like hire / sell / license / transfer / partner.
**Why bad:** AI defaults to the obvious branches. Strategic value lives in the non-default paths.
**Rule:** For decision-oriented documents, surface at least 2 non-default options explicitly.
**Fix:** Ask: *"What are the options if we stop being the operator?"* Hire someone. Sell. License. Transfer. Spin off. Partner.

---

## 8. Voice modulation

### 8.1 Direct address over-applied to framing prose
**What happens:** *"You read this to get a working mental model in one pass."* / *"You'll find one row per classified event in the observations table."*
**Why bad:** The reader IS reading; telling them so is awkward. Schema descriptions don't have an actor.
**Rule:** Use *you/your* only when the reader is an actor in the sentence: system behavior they interact with, touchpoints, or workflow consequences. NOT in framing prose about the page itself or in neutral reference captions.
**Fix:** *"This page walks the pipeline top to bottom"* > *"You read this page to walk the pipeline top to bottom."*

### 8.2 Register shift mid-page
**What happens:** Engineering-formal in §1, marketing-warm in §2, executive-impact in §3. Reader feels the shifts.
**Why bad:** Mixed registers signal AI authoring.
**Rule:** Pick one register in Step 1 and hold it across every label, heading, and paragraph.
**Fix:** Read the page aloud. If a section sounds like a different person wrote it, the register slipped.

### 8.3 Audience leakage
**What happens:** Subagent is told audience = a non-engineering team and subject = a technical codebase. Subagent picks a generic non-technical illustration instead of the named subject.
**Why bad:** Audience-derived register pulled the agent away from the named subject. Subject lost.
**Rule:** The subject does not change with the audience. Only the register changes. If subject = X, the page is about X regardless of who's reading.
**Fix:** State subject and audience as separate constraints. Don't let one override the other.

---

## 9. Content discipline

### 9.1 Re-teaching the audience what they already know
**What happens:** A page mapping a subsystem to a methodology framework spends a section explaining what the subsystem is to the person who built it.
**Why bad:** Condescending to the audience and pads the page. They came for the new claim, not a refresher.
**Rule:** Inventory two lists at Frame: *what the reader already knows* and *what they need to know from this page*. Foreground the second; cut the first.
**Fix:** Walk every section and ask: *"Does the reader already know this? If yes, why is it here?"*

### 9.2 Inflated time estimates
**What happens:** Page claims "Path A: 2-3 weeks" for what's really a 3-day cleanup based on actual sprint pace.
**Why bad:** AI defaults to round-number weeks. Reality often runs in days.
**Rule:** Time estimates ground in observed velocity. For codebases: `git log --since=<window>` to see what shipped per active day. Categorize by effort tier (Quick / Sprint week / Multi-week / Multi-month) rather than wall-clock weeks.
**Fix:** Convert weeks to days based on observed velocity before committing a number to the page.

---

## 10. Grounding

### 10.1 Fabricated identifiers
**What happens:** Page claims `temporal_window` and `temporal_link` exist as tables. They don't.
**Why bad:** Claims about real systems must be true. A fabricated identifier in a technical doc is the worst kind of error: confident-sounding and wrong.
**Rule:** Every claimed file path, table name, column name, or schema identifier must exist in the referenced repo. Verify before claiming.
**Fix:** `grep` or read the actual schema before naming it on the page. If unsure, omit.

### 10.2 Training-stale claims about external state
**What happens:** Page claims "Anthropic will eventually ship a marketplace and crush this wedge" — when Anthropic shipped it 4 months ago.
**Why bad:** The page treats speculation as forecast when the event has already happened.
**Rule:** For claims about external markets, current state of named players, or what's shipped, ground via web search, claude-code-guide, or whatever current-state tool is wired up. Don't speculate from training-stale knowledge.
**Fix:** When a claim depends on "what's true now in the world," verify before writing.

---

## How this list is maintained

A new pattern enters this list when:
- It fires once and required a correction.
- The correction is mechanical (rule-checkable) or judgment-based-but-recurring (a register slip that keeps happening).

A pattern leaves this list when:
- It hasn't fired in 3+ consecutive sessions and is well-understood.
- It's superseded by a more general pattern that catches it.

Every entry should have: name, what happens, why bad, rule, fix. Optionally: script-checkable regex.

Last refined: 2026-04-30 after the cc-viz session (16 test outputs, ~30 user refinements).
