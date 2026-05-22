# cc-viz Winning Patterns

Patterns extracted from cc-viz outputs that landed well. Each entry: name, when to use, why it works, example markup or composition. Prefer reaching for these over inventing new patterns from scratch — a pattern that has worked once will likely work again on similar content shape.

Read while drafting if your form matches one of these.

---

## 1. Status strip + recommendation card on top

**Form:** Board memo, decision memo, internal brief.

**When to use:** Decision-oriented documents where the reader needs the answer first and the supporting work below. The reader is busy and may stop reading after section 1; make sure the recommendation lives there.

**Why it works:** Burying the recommendation in section 6 means readers who scan only the top half miss it. The status strip gives concrete anchors (counts, dates, dimensions) that frame what's real before the argument starts.

**Composition:**

```html
<!-- Status strip: 3-4 facts at glance, mono numerals, sans labels -->
<div class="stat-strip">
  <div class="stat"><span class="num">2</span><span class="lbl">products live</span></div>
  <div class="stat"><span class="num">0</span><span class="lbl">public launches</span></div>
  <div class="stat"><span class="num">2</span><span class="suffix">mo</span><span class="lbl">since last team push</span></div>
  <div class="stat"><span class="num">1</span><span class="lbl">decision pending</span></div>
</div>

<!-- Recommendation card: bordered, accent rule, display-type answer up top -->
<aside class="reco">
  <div class="reco__eyebrow">What we should do</div>
  <h2 class="reco__answer">A then <em>B</em>. Three weeks total.</h2>
  <p class="reco__explain">Two weeks to lock the rails. One week to ship the slice.</p>
</aside>
```

**Key constraints:**
- Status strip uses `font-family: var(--font-mono); font-variant-numeric: tabular-nums;` for numerals.
- Recommendation card has a single accent rule (left border or top border) in the page's primary accent color.
- Recommendation answer is set in display type, with single italic emphasis if any.
- Lives BEFORE the situation prose, not after.

---

## 2. Comparison table with "DO THIS" tagged rows

**Form:** Board memo, decision memo, options brief.

**When to use:** When the page has 3+ options and the reader needs to scan them side by side, with the recommended one(s) visually called out.

**Why it works:** A table makes options scannable. Tagging the recommended rows means the reader sees the answer in their first glance at the table, not after reading every cell.

**Composition:**

```html
<table class="options">
  <thead>
    <tr><th>Option</th><th>What it is</th><th>Effort</th><th>Reuse</th><th>Decision criterion</th></tr>
  </thead>
  <tbody>
    <tr class="options__pick">
      <td><strong>A.</strong> Recommit to infrastructure <span class="tag">DO THIS</span></td>
      <td>Lock the stack down as the team's delivery rails.</td>
      <td>Sprint week · 3 days focused</td>
      <td>95%</td>
      <td>Are we the infrastructure team?</td>
    </tr>
    <!-- other rows -->
  </tbody>
</table>
```

**Key constraints:**
- Tagged rows have a left-border accent rule plus the "DO THIS" pill — both, not either.
- Untagged rows stay visually quieter (no accent, no border emphasis).
- Effort column uses tier names (`Quick`, `Sprint week`, `Multi-week sprint`, `Multi-month`) followed by day counts, not just weeks.
- Decision criterion column is a question, not a description.

---

## 3. Drop-cap + multi-column body + Roman-numeraled close

**Form:** Magazine editorial.

**When to use:** Voice-driven, narrative-heavy, argument-led work where prose IS the art and the reader's job is to follow a line of thought, not scan a structure.

**Why it works:** The drop-cap signals "feature article, sit and read" which calibrates the reader's attention. Multi-column body increases information density without feeling cramped. Roman-numeraled close (i. ii. iii. iv.) gives the won't-do list editorial gravitas instead of corporate-bullet feel.

**Composition:**

```html
<section class="thesis">
  <span class="kicker">§ I · The thesis</span>
  <div class="thesis__body">
    <p>Most frameworks for capturing expertise stop at what an expert knows. Cognitive Fingerprint goes further. We ask four questions of every observable move, and we hold the answers apart on purpose.</p>
    <p>The four are <em>declarative</em> (what they know), <em>procedural</em> (how they do it), <em>conditional</em> (when they apply it), and <em>metacognitive</em> (how they think about their own thinking).</p>
  </div>
</section>

<style>
  .thesis__body {
    column-count: 2;
    column-gap: 56px;
    column-rule: 1px solid var(--rule-soft);
    font-size: 19px;
    line-height: 1.62;
  }
  .thesis__body p { margin: 0 0 1em; break-inside: avoid-column; }
  .thesis__body p:first-of-type::first-letter {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 5em;
    line-height: 0.86;
    float: left;
    padding: 4px 12px 0 0;
    margin-top: 6px;
    color: var(--accent);
  }
</style>

<!-- Won't-do close, end of page -->
<section class="wont">
  <h3>Three things we are explicitly not doing.</h3>
  <ol class="wont__list">
    <li><span class="num">i.</span> Pretend the wedge is still there.</li>
    <li><span class="num">ii.</span> Pursue Path D unless a founder commits to owning it.</li>
    <li><span class="num">iii.</span> Stay in the loop.</li>
  </ol>
</section>
```

**Key constraints:**
- Drop-cap caps at 5em, not 7.5em (theatrical).
- `break-inside: avoid-column` on every paragraph — sentences don't split across columns.
- Roman numerals are lowercase italic (i, ii, iii) for editorial register, not capital I/II/III.

---

## 4. Argument-led position memo

**Form:** Position memo (board memo register, argument-led structure).

**When to use:** Analytical, mapping, comparison, synthesis work where the reader needs a position they can agree with, push back on, or build on. NOT when the reader needs an inventory.

**Why it works:** Lead with the load-bearing claim, support each section with evidence that defends it, close with the implication. The artifacts (file paths, columns, citations) appear as evidence under claims, not as the page's spine.

**Composition:**

```html
<!-- Hero: state the spine -->
<section class="hero">
  <span class="kicker">A position memo</span>
  <h1>The substrate already speaks the methodology, and where it doesn't.</h1>
  <p class="lede">Five framework dimensions. Three layers. The page reads the substrate against the methodology, names which artifacts <strong>instantiate</strong> which dimension, and flags two places the implementation has quietly invented something the framework hasn't named yet.</p>
</section>

<!-- Each section is a claim, with evidence under it -->
<section class="claim">
  <h2>Session assembly <em>is</em> a Conditional engine.</h2>
  <p>The 30-min gap and 0.65 cosine drift rules don't just chunk events. They define the conditions under which a behavior counts as one episode.</p>
  <aside class="evidence">
    <code>session-assembly.ts</code> · <code>30min gap</code> · <code>topic-drift 0.65</code>
  </aside>
</section>
```

**Key constraints:**
- Hero h1 IS the load-bearing claim, full sentence, single italic emphasis.
- Each section heading is a claim ("X *is* Y", "Y is the spine", "Why we hold the four apart"), not a topic ("Conditional Dimension", "Section II").
- Evidence appears as supporting markup under the claim — code tags, file paths, schema references — not as the section's primary content.
- Closing section names the implication or open question, not just a summary.

---

## 5. Data-journalism layer × dimension matrix

**Form:** Data journalism / matrix ledger.

**When to use:** Genuinely matrix-shaped content where the reader's job is to scan a grid (which X touches which Y, which feature appears in which version). NOT when the content is argument-shaped — the matrix becomes a feature inventory and the page reports when it should argue.

**Why it works:** When the content actually IS a matrix (capability vs platform, layer vs dimension, feature vs tier), the table is the most efficient form. Cold, precise, scannable.

**Composition:**

```html
<table class="matrix">
  <thead>
    <tr>
      <th>Layer</th>
      <th>What it does</th>
      <th><span class="dim-swatch dim--D"></span> D</th>
      <th><span class="dim-swatch dim--P"></span> P</th>
      <th><span class="dim-swatch dim--C"></span> C</th>
      <th><span class="dim-swatch dim--M"></span> M</th>
      <th><span class="dim-swatch dim--E"></span> E</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>L1</strong> Categorization</td>
      <td class="note">Receives observable behavior. Privacy tier set at receive. Sessions form by quiet gaps + topic drift.</td>
      <td><span class="dot full--P">P</span></td>
      <td><span class="dot full--P">P</span></td>
      <td><span class="dot partial--C">C</span></td>
      <td>·</td>
      <td>·</td>
    </tr>
  </tbody>
</table>
```

**Key constraints:**
- Cells use `display: inline-flex; align-items: center; justify-content: center` for the letter-in-dot, not `line-height` tricks.
- Three states per cell: filled (`full`), partial (`partial`), empty (`·`). Legend explains.
- The "What it does" column carries the methodology framing in tight prose. Not a feature list.
- Matrix is supported by 2–3 defended-claim cards underneath. The matrix alone is a report; the cards make it an argument.

---

## 6. Pull quote: blockquote + bar tracks text

**Form:** Any prose-led page. Especially editorial, position memo.

**When to use:** A single load-bearing line that should hit the reader hard. The page's strongest sentence.

**Why it works:** Properly bounded, the bar visually marks the quote without over-extending. Italic display serif at 24–28px (NOT 32px+) reads as gravitas without theatrics.

**Composition:**

```html
<blockquote class="pull">
  <p>None is launched in the sense that the team has stopped working on it and started selling it.</p>
  <cite>— Internal team analysis, pattern note</cite>
</blockquote>

<style>
  .pull {
    font-family: var(--font-display);
    font-style: italic;
    font-weight: 400;
    font-size: 24px;
    line-height: 1.35;
    color: var(--text);
    border-left: 2px solid var(--accent);
    padding: 0.25em 0 0.25em 1.25em;
    max-width: 60ch;
    margin: 3rem 0;
    text-wrap: balance;
  }
  .pull p { margin: 0; }
  .pull cite {
    display: block;
    margin-top: 0.75em;
    font-family: var(--font-mono);
    font-style: normal;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-dim);
  }
</style>
```

**Key constraints:**
- `<blockquote>` not `<pre>`. `<pre>` preserves trailing whitespace and inflates the bar past the text.
- Inner `<p>` and `<cite>` — NOT free text and an inline cite tag.
- `padding: 0.25em` top/bottom in em units — bar tracks text height naturally.
- Font-size 24px max. 32px+ overheats.
- Em dash in cite is allowed (citation line). NOT in the quote body.

---

## 7. Tri-font system: display + sans body + mono labels

**Form:** Any.

**When to use:** Most cc-viz outputs. The default to reach for.

**Why it works:** Three fonts give clean role separation. Display carries hero/h1/pull-quote with character. Sans body is readable at small sizes. Mono signals "code, label, datum" reliably. Fewer than three fonts feels under-designed; more than three feels chaotic.

**Approved combinations from this session:**

| Display | Body | Mono | Register |
|---|---|---|---|
| Instrument Serif (italic) | DM Sans (450) | JetBrains Mono | Editorial, voice-led |
| Fraunces (variable) | DM Sans (450) | JetBrains Mono | Magazine, gravitas |
| IBM Plex Sans (display) | IBM Plex Sans (400/450) | IBM Plex Mono | Technical, reliable |
| Bricolage Grotesque | DM Sans | Fragment Mono | Bold, characterful |
| Sora | Sora (450) | JetBrains Mono | Modern, precise |

**Body weight 450 is critical for dark-mode pages** (per `css-patterns.md` dark-mode text-compensation triad). Use 500 if the font lacks a 450 cut.

---

## 8. Double radial atmosphere on dark backgrounds

**Form:** Any dark-mode page.

**When to use:** Whenever the page's bg is dark — the void test demands atmosphere.

**Why it works:** Two soft radial washes from corners give the page a horizon and depth without color shift. A single radial reads as a spotlight; two reads as a room.

**Composition:**

```css
body {
  background:
    radial-gradient(ellipse at 50% 0%, var(--accent-glow), transparent 55%),
    radial-gradient(ellipse at 100% 100%, var(--secondary-glow), transparent 50%),
    linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%);
  background-attachment: fixed;
}
```

**Key constraints:**
- One radial in the accent color, one in a quieter secondary (slate, deep teal, etc.).
- Linear gradient as the base layer — between two near-neighbor colors, not contrasty.
- `background-attachment: fixed` so the atmosphere doesn't scroll with content.
- Optional 2.5% opacity hairline grid pattern on top for surface texture.

---

## 9. Mermaid zoom controls — `style.zoom` + flex wrap + min-height

**Form:** Any page using Mermaid diagrams.

**When to use:** Always, for every Mermaid diagram. Default. The proven pattern.

**Why it works:** CSS `zoom` reflows in real Chrome/Safari, so the wrap grows with the diagram and the frame stays in proportion to content. SVG-width percentage scaling cuts off content horizontally; `transform: scale` doesn't reflow. `style.zoom` on `.mermaid` is the only approach that gets all three (visual scale, layout reflow, drag-to-pan compatibility).

**Composition:** see `references/css-patterns.md` "Mermaid Zoom Controls". Already documented.

---

## How this list is maintained

A pattern enters when:
- It's been used in 2+ outputs that scored well on the rubric.
- It's load-bearing (the page degrades visibly without it).
- It's reproducible (the description is precise enough that the next agent can apply it).

A pattern leaves when:
- It's been superseded by a better pattern for the same use case.
- It hasn't been used in 3+ consecutive sessions.
- The skill rubric stops scoring its absence as a fail.

Last refined: 2026-04-30. Patterns 1, 2, 6 from a10 (board memo). Patterns 3, 4, 6 from a12 (magazine editorial). Pattern 5 from a14 (matrix ledger). Patterns 7, 8 across the session. Pattern 9 from the zoom-fix sequence.
