# CSS Patterns for Diagrams

Reusable patterns for layout, connectors, theming, and visual effects in self-contained HTML diagrams.

## Typography & Rhythm

These rules fix the most common cc-viz readability defects: dense unbroken paragraphs, line lengths that stretch to viewport width, dark-mode text that reads flat, and muddy hierarchy from too-similar font sizes.

### Body measure: 65–75ch

Every prose container (`<p>`, `.section-intro`, card body) must cap at `max-width: 68ch` (or 65–75ch). Above 75ch the eye loses its place tracking line wraps; below 45ch reading rhythm fragments. This is the highest-impact fix for "isn't very clean to read."

```css
p, .section-intro, .ve-card p, .pull p {
  max-width: 68ch;
  line-height: 1.6;
}
```

When a section has both prose and a wide diagram, the prose constrains to 68ch even if the diagram fills 1100px. Prose centers in the column or aligns with the section's left rule.

### Dark-mode text compensation triad

Light text on a dark background looks lighter than dark text on light at the same numeric weight. Perceived weight drops on three axes simultaneously, so all three need to be compensated:

```css
@media (prefers-color-scheme: dark) {
  body {
    line-height: 1.65;          /* +0.05 over light mode's 1.6 */
    letter-spacing: 0.01em;     /* hairline tracking */
    font-weight: 450;            /* one notch heavier than 400 */
  }
}
```

If the body font doesn't have a 450 weight (most don't), use 500 and step display weights down by one to keep the scale ratio. Without this triad, dark-mode prose reads heavy-flat: visually thick but optically dim. The fix is invisible if you do all three; halfway fixes look broken.

### Vertical rhythm: line-height as the spacing unit

Pick body line-height (e.g. 24px on 16px base = 1.5). Every vertical spacing value in the page is a multiple of that 24px: `padding-bottom: 24px`, `margin-top: 48px`, gap between sections `72px`. Card padding is `24px` or `48px`, never `28px` or `32px`. Subconscious harmony comes from the math, not from "feels about right."

This applies to grid gaps too: `gap: 24px`, not `gap: 16px` next to elements with 24px line-height.

### Paragraph rhythm: space OR indent, never both

Pick one:
- **Space-between** (digital default): `p + p { margin-top: 1em; }`, no first-line indent.
- **Indent-only** (long-form editorial): `p + p { text-indent: 1.5em; margin-top: 0; }`, no inter-paragraph space.

Doing both (what most AI-generated layouts do by reflex) produces visual noise. The reader sees both an indent and a gap and the rhythm collapses.

### Modular scale: ≥1.25 ratio between steps

Flat scales (14, 15, 16, 18, 20px) read as muddy hierarchy. Use one of these named ratios and commit:

| Name | Ratio | 5-step scale from 16px |
|---|---|---|
| Major third | 1.25 | 10 / 13 / 16 / 20 / 25 |
| Perfect fourth | 1.333 | 9 / 12 / 16 / 21 / 28 |
| Perfect fifth | 1.5 | 7 / 11 / 16 / 24 / 36 |

Headings step *up* the scale; small/caption text steps *down*. A page should never have more than 5 sizes total. Fewer sizes with more contrast beats more sizes with less.

### Light text on color: gray is dead

Never put gray text on a colored background. Gray reads washed out and lifeless on color. Use a darker shade of the background color, or a low-opacity black/white. `color: rgba(0,0,0,0.7)` on a colored card reads infinitely better than `color: #6b7280`.

### Pull quotes — no `<pre>`

Use `<blockquote>` with a `<cite>`. Never `<pre>` (it preserves whitespace and forces monospace by default; the trailing newline pushes the left-rule bar past the text):

```html
<blockquote class="pull">
  <p>The session is the minimum unit of work. A single commit at 11:47pm is not the unit; the six-hour session is.</p>
  <cite>— Invariant #4, ARCHITECTURE.md</cite>
</blockquote>
```

```css
.pull {
  font-family: var(--font-display);
  font-style: italic;
  font-size: 1.5rem;       /* not 32px+ — that overheaters the visual weight */
  line-height: 1.35;
  color: var(--text);
  border-left: 2px solid var(--accent);
  padding: 0.25em 0 0.25em 1.25em;  /* tight to text — bar matches text height */
  max-width: 60ch;
  margin: 3rem 0;
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
```

The padding is `0.25em` top and bottom; the bar height tracks the text height naturally. With `<pre>`, the trailing newline adds blank space below the cite which inflates the bar.

## Theme Setup

Always define both light and dark palettes via custom properties. Start with whichever fits the chosen aesthetic, ensure both work.

```css
:root {
  /* Pick a pairing from references/libraries.md — never default to Inter, Roboto, or system fonts. */
  --font-body: /* approved sans (e.g. DM Sans, IBM Plex Sans) */, system-ui, sans-serif;
  --font-mono: /* approved mono (e.g. JetBrains Mono, IBM Plex Mono) */, 'SF Mono', Consolas, monospace;

  --bg: #f8f9fa;
  --surface: #ffffff;
  --surface-elevated: #ffffff;
  --border: rgba(0, 0, 0, 0.08);
  --border-bright: rgba(0, 0, 0, 0.15);
  --text: #1a1a2e;
  --text-dim: #6b7280;
  --accent: #0891b2;
  --accent-dim: rgba(8, 145, 178, 0.1);
  /* Semantic accents for diagram elements */
  --node-a: #0891b2;
  --node-a-dim: rgba(8, 145, 178, 0.1);
  --node-b: #059669;
  --node-b-dim: rgba(5, 150, 105, 0.1);
  --node-c: #d97706;
  --node-c-dim: rgba(217, 119, 6, 0.1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface-elevated: #1c2333;
    --border: rgba(255, 255, 255, 0.06);
    --border-bright: rgba(255, 255, 255, 0.12);
    --text: #e6edf3;
    --text-dim: #8b949e;
    --accent: #22d3ee;
    --accent-dim: rgba(34, 211, 238, 0.12);
    --node-a: #22d3ee;
    --node-a-dim: rgba(34, 211, 238, 0.12);
    --node-b: #34d399;
    --node-b-dim: rgba(52, 211, 153, 0.12);
    --node-c: #fbbf24;
    --node-c-dim: rgba(251, 191, 36, 0.12);
  }
}
```

## Background Atmosphere

Flat backgrounds feel dead. Use subtle gradients or patterns.

```css
/* Radial glow behind focal area */
body {
  background: var(--bg);
  background-image: radial-gradient(ellipse at 50% 0%, var(--accent-dim) 0%, transparent 60%);
}

/* Faint dot grid */
body {
  background-color: var(--bg);
  background-image: radial-gradient(circle, var(--border) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Diagonal subtle lines */
body {
  background-color: var(--bg);
  background-image: repeating-linear-gradient(
    -45deg, transparent, transparent 40px,
    var(--border) 40px, var(--border) 41px
  );
}

/* Gradient mesh (pick 2-3 positioned radials) */
body {
  background: var(--bg);
  background-image:
    radial-gradient(at 20% 20%, var(--node-a-dim) 0%, transparent 50%),
    radial-gradient(at 80% 60%, var(--node-b-dim) 0%, transparent 50%);
}
```

## Section / Card Components

The fundamental building block. A colored card representing a system component, pipeline step, or data entity.

**IMPORTANT: Never use `.node` as a CSS class name.** Mermaid.js internally uses `.node` on its SVG `<g>` elements with `transform: translate(x, y)` for positioning. Any page-level `.node` styles (hover transforms, box-shadows, transitions) will leak into Mermaid diagrams and break their layout. Use `.ve-card` instead (namespaced to avoid collisions with CSS frameworks like Bootstrap/Tailwind that also use `.card`).

```css
.ve-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
  position: relative;
}

/* Colored accent border (left or top) */
.ve-card--accent-a {
  border-left: 3px solid var(--node-a);
}

/* --- Depth tiers: vary card depth to signal importance --- */

/* Elevated: KPIs, key sections, anything that should pop */
.ve-card--elevated {
  background: var(--surface-elevated);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
}

/* Recessed: code blocks, secondary content, detail panels */
.ve-card--recessed {
  background: color-mix(in srgb, var(--bg) 70%, var(--surface) 30%);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
  border-color: var(--border);
}

/* Hero: executive summaries, focal elements — demands attention */
.ve-card--hero {
  background: color-mix(in srgb, var(--surface) 92%, var(--accent) 8%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.04);
  border-color: color-mix(in srgb, var(--border) 50%, var(--accent) 50%);
}

/* Glass: special-occasion overlay effect (use sparingly) */
.ve-card--glass {
  background: color-mix(in srgb, var(--surface) 60%, transparent 40%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Section label (monospace, uppercase, small) */
.ve-card__label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--node-a);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Colored dot indicator */
.ve-card__label::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}
```

## Overflow Protection

Grid and flex children default to `min-width: auto`, which prevents them from shrinking below their content width. Long text, inline code badges, and non-wrapping elements will blow out containers.

### Global rules

```css
/* Every grid/flex child must be able to shrink */
.grid > *, .flex > *,
[style*="display: grid"] > *,
[style*="display: flex"] > * {
  min-width: 0;
}

/* Long text wraps instead of overflowing */
body {
  overflow-wrap: break-word;
}
```

### Side-by-side comparison panels

```css
.comparison {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.comparison > * {
  min-width: 0;
  overflow-wrap: break-word;
}

@media (max-width: 768px) {
  .comparison { grid-template-columns: 1fr; }
}
```

### Never use `display: flex` on `<li>` for marker characters

Using `display: flex` on a list item to position a `::before` marker creates an anonymous flex item for the remaining text content. That anonymous flex item gets `min-width: auto` and you **cannot** set `min-width: 0` on anonymous boxes. Lines with many inline `<code>` badges will overflow their container with no CSS fix possible.

Use absolute positioning for markers instead:

```css
/* WRONG — causes overflow with inline code badges */
li {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
li::before {
  content: '›';
  flex-shrink: 0;
}

/* RIGHT — text wraps normally */
li {
  padding-left: 14px;
  position: relative;
}
li::before {
  content: '›';
  position: absolute;
  left: 0;
}
```

## Mermaid Zoom Controls

Mermaid diagrams are often too small to read comfortably, especially complex flowcharts and sequence diagrams. Add zoom controls to every `.mermaid-wrap` container.

**SVG sizing fix (critical).** Mermaid bakes a hardcoded `height` attribute into every SVG it renders. Without removing it, the SVG keeps its fixed pixel height regardless of container size and zoom. After `mermaid.initialize()`, call `mermaid.run().then(...)` to strip the height attribute and set `width: 100%; height: auto` on every `.mermaid svg`. This is what makes diagrams fit their container and scale correctly.

**Use `style.zoom` on `.mermaid`, with a flex+overflow:hidden wrap.** Set `target.style.zoom = next` on the `.mermaid` div. The `.mermaid-wrap` MUST be `display: flex; justify-content: center; align-items: center; overflow: hidden; min-height: 340px`. CSS `zoom` causes layout reflow in real Chrome/Safari, so the wrap grows with the diagram. The frame stays in proportion to content.

Do NOT switch to `svg.style.width` percentage scaling. That approach scales the SVG inside a fixed-width wrap with `overflow: auto` — which produces scrollbars and visually cuts off the diagram horizontally. Tested and rejected in favor of the e3-share pattern.

Do NOT use `transform: scale`. It scales visually but doesn't reflow at all, so the wrap stays at min-height even when the diagram needs more room.

WKWebView caveat: `style.zoom` doesn't visually apply in WKWebView (cmux). Generated HTML is intended for real-browser viewing. If you need to validate in cmux, you won't see zoom changes; open the file in Chrome/Safari directly.

**Small diagrams in slides.** If a diagram has fewer than ~7 nodes with no branching, it will render tiny in a full-viewport slide container. For simple linear flows (A → B → C → D), use CSS pipeline cards instead of Mermaid (see `slide-patterns.md` "CSS Pipeline Slide"). Reserve Mermaid for complex graphs where automatic edge routing earns its place.

### CSS

```css
.mermaid-wrap {
  position: relative;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 340px;
}

.mermaid-wrap .mermaid {
  transition: zoom 0.15s ease;
}

.zoom-controls {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 2px;
  z-index: 10;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 2px;
}

.zoom-controls button {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--text-dim);
  font-family: var(--font-mono);
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease, color 0.15s ease;
}

.zoom-controls button:hover {
  background: var(--border);
  color: var(--text);
}

.mermaid-wrap.is-zoomed { cursor: grab; }
.mermaid-wrap.is-panning { cursor: grabbing; user-select: none; }

@media (prefers-reduced-motion: reduce) {
  .mermaid-wrap .mermaid { transition: none; }
}

/* ER diagram: relationship labels overlap connector circles by default.
   Solid bg + padding so labels sit cleanly over the line. */
.mermaid .relationshipLabelBox {
  fill: var(--surface) !important;
  rx: 4px;
}
.mermaid .relationshipLabel {
  font-family: var(--font-mono) !important;
  font-size: 11px !important;
  fill: var(--text-dim) !important;
}
```

### HTML

```html
<div class="mermaid-wrap">
  <div class="zoom-controls">
    <button onclick="zoomDiagram(this, 1.2)" title="Zoom in">+</button>
    <button onclick="zoomDiagram(this, 0.8)" title="Zoom out">&minus;</button>
    <button onclick="resetZoom(this)" title="Reset zoom">&#8634;</button>
    <button onclick="openMermaidInNewTab(this.closest('.mermaid-wrap'))" title="Expand">&#x26F6;</button>
  </div>
  <pre class="mermaid">
    graph TD
      A --> B
  </pre>
</div>
```

### JavaScript

Two scripts required. First, the ESM Mermaid init block. Add the `.then()` post-processor to fix SVG sizing:

```javascript
// In your <script type="module"> alongside mermaid.initialize(...)
mermaid.run().then(function() {
  document.querySelectorAll('.mermaid svg').forEach(function(svg) {
    svg.removeAttribute('height');
    svg.style.width = '100%';
    svg.style.maxWidth = '100%';
    svg.style.height = 'auto';
  });
});
```

Second, the zoom/pan controls. Add once at the end of the page:

```javascript
// Set style.zoom on .mermaid. CSS zoom causes layout reflow in real Chrome/Safari,
// so the parent .mermaid-wrap grows with the diagram. Pattern proven in production.
var INITIAL_ZOOM = 1;

function zoomDiagram(btn, factor) {
  var wrap = btn.closest('.mermaid-wrap');
  var target = wrap.querySelector('.mermaid');
  var current = parseFloat(target.dataset.zoom || INITIAL_ZOOM);
  var next = Math.min(Math.max(current * factor, 0.5), 5);
  target.dataset.zoom = next;
  target.style.zoom = next;
}

function resetZoom(btn) {
  var wrap = btn.closest('.mermaid-wrap');
  var target = wrap.querySelector('.mermaid');
  target.dataset.zoom = INITIAL_ZOOM;
  target.style.zoom = INITIAL_ZOOM;
}

function openMermaidInNewTab(wrap) {
  var svg = wrap.querySelector('.mermaid svg');
  if (!svg) return;
  var clone = svg.cloneNode(true);
  clone.style.zoom = '';
  var bg = getComputedStyle(document.documentElement).getPropertyValue('--bg').trim() || '#fff';
  var html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:' + bg + ';padding:40px}svg{max-width:100%;max-height:90vh;height:auto}</style></head><body>' + clone.outerHTML + '</body></html>';
  window.open(URL.createObjectURL(new Blob([html], { type: 'text/html' })), '_blank');
}
```

Zoom range 0.5x–5x. The wrap's `min-height: 340px` keeps it stable when the diagram is small; the absence of a fixed max-height lets it grow when zoomed. The expand button opens the raw SVG in a new tab for printing or full-screen inspection.

## Grid Layouts

### Architecture Diagram (2-column with sidebar)
```css
.arch-grid {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto;
  gap: 20px;
  max-width: 1100px;
  margin: 0 auto;
}

.arch-grid__sidebar { grid-column: 1; }
.arch-grid__main { grid-column: 2; }
.arch-grid__full { grid-column: 1 / -1; }
```

### Pipeline (horizontal steps)
```css
.pipeline {
  display: flex;
  align-items: stretch;
  gap: 0;
  overflow-x: auto;
  padding-bottom: 8px;
}

.pipeline__step {
  min-width: 130px;
  flex-shrink: 0;
}

.pipeline__arrow {
  display: flex;
  align-items: center;
  padding: 0 4px;
  color: var(--border-bright);
  font-size: 18px;
  flex-shrink: 0;
}

/* Parallel branch within a pipeline */
.pipeline__parallel {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
```

### Card Grid (dashboard / metrics)
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}
```

### Data Tables

Use real `<table>` elements for tabular data. Wrap in a scrollable container for wide tables.

```css
/* Scrollable wrapper for wide tables */
.table-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
}

.table-scroll {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Base table */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  line-height: 1.5;
}

/* Header */
.data-table thead {
  position: sticky;
  top: 0;
  z-index: 2;
}

.data-table th {
  background: var(--surface-elevated, var(--surface2, var(--surface)));
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-dim);
  text-align: left;
  padding: 12px 16px;
  border-bottom: 2px solid var(--border-bright);
  white-space: nowrap;
}

/* Cells */
.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
  color: var(--text);
}

/* Let text-heavy columns wrap naturally */
.data-table .wide {
  min-width: 200px;
  max-width: 500px;
}

/* Right-align numeric columns */
.data-table td.num,
.data-table th.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-family: var(--font-mono);
}

/* Alternating rows */
.data-table tbody tr:nth-child(even) {
  background: var(--accent-dim);
}

/* Row hover */
.data-table tbody tr {
  transition: background 0.15s ease;
}

.data-table tbody tr:hover {
  background: var(--border);
}

/* Last row: no bottom border (container handles it) */
.data-table tbody tr:last-child td {
  border-bottom: none;
}

/* Code inside cells */
.data-table code {
  font-family: var(--font-mono);
  font-size: 11px;
  background: var(--accent-dim);
  color: var(--accent);
  padding: 1px 5px;
  border-radius: 3px;
}

/* Secondary detail text */
.data-table small {
  display: block;
  color: var(--text-dim);
  font-size: 11px;
  margin-top: 2px;
}
```

#### Status Indicators

Styled spans for match/gap/warning states. Never use emoji.

```css
.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

.status--match {
  background: var(--green-dim, rgba(5, 150, 105, 0.1));
  color: var(--green, #059669);
}

.status--gap {
  background: var(--red-dim, rgba(239, 68, 68, 0.1));
  color: var(--red, #ef4444);
}

.status--warn {
  background: var(--orange-dim, rgba(217, 119, 6, 0.1));
  color: var(--orange, #d97706);
}

.status--info {
  background: var(--accent-dim);
  color: var(--accent);
}

/* Dot variant (compact, no text) */
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot--match { background: var(--green, #059669); }
.status-dot--gap { background: var(--red, #ef4444); }
.status-dot--warn { background: var(--orange, #d97706); }
```

Usage in table cells:
```html
<td><span class="status status--match">Match</span></td>
<td><span class="status status--gap">Gap</span></td>
<td><span class="status status--warn">Partial</span></td>
```

#### Table Summary Row

For totals, counts, or aggregate status at the bottom:

```css
.data-table tfoot td {
  background: var(--surface-elevated, var(--surface2, var(--surface)));
  font-weight: 600;
  font-size: 12px;
  border-top: 2px solid var(--border-bright);
  border-bottom: none;
  padding: 12px 16px;
}
```

#### Sticky First Column (for very wide tables)

```css
.data-table th:first-child,
.data-table td:first-child {
  position: sticky;
  left: 0;
  z-index: 1;
  background: var(--surface);
}

.data-table tbody tr:nth-child(even) td:first-child {
  background: color-mix(in srgb, var(--surface) 95%, var(--accent) 5%);
}
```

## Connectors

### CSS Arrow (vertical, between stacked sections)
```css
.flow-arrow {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  color: var(--text-dim);
  font-family: var(--font-mono);
  font-size: 12px;
  padding: 6px 0;
}

/* Down arrow via SVG icon */
.flow-arrow svg {
  width: 20px;
  height: 20px;
  fill: none;
  stroke: var(--border-bright);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
```

Down arrow SVG (reuse inline):
```html
<svg viewBox="0 0 20 20"><path d="M10 4 L10 16 M6 12 L10 16 L14 12"/></svg>
```

### CSS Arrow (horizontal, between inline steps)
Use `::after` or a literal arrow character:
```css
.h-arrow::after {
  content: '→';
  color: var(--border-bright);
  font-size: 18px;
  padding: 0 4px;
}
```

### SVG Curved Connector (between arbitrary nodes)
For connections that aren't simple vertical/horizontal, use an absolutely positioned SVG overlay:
```html
<svg class="connectors" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none;">
  <path d="M 150,100 C 150,200 350,100 350,200" fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <!-- Arrowhead -->
  <polygon points="348,195 352,205 356,195" fill="var(--accent)"/>
</svg>
```

Position the parent container as `position: relative` to scope the SVG overlay.

## Animations

### Staggered Fade-In on Load

Define the keyframe once, then stagger via a `--i` CSS variable set per element. This approach works regardless of DOM nesting or interleaved non-animated elements (unlike `nth-child` which breaks when siblings aren't all the same type).

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.ve-card {
  animation: fadeUp 0.4s ease-out both;
  animation-delay: calc(var(--i, 0) * 0.05s);
}
```

Set `--i` per element in the HTML to control stagger order:

```html
<div class="ve-card" style="--i: 0">First</div>
<div class="connector">...</div>
<div class="ve-card" style="--i: 1">Second</div>
<div class="connector">...</div>
<div class="ve-card" style="--i: 2">Third</div>
```

### Hover Lift
```css
.ve-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ve-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

### Scale-Fade (for KPI cards, badges, status indicators)

```css
@keyframes fadeScale {
  from { opacity: 0; transform: scale(0.92); }
  to { opacity: 1; transform: scale(1); }
}

.kpi-card {
  animation: fadeScale 0.35s ease-out both;
  animation-delay: calc(var(--i, 0) * 0.06s);
}
```

### SVG Draw-In (for connectors, progress rings, path elements)

```css
@keyframes drawIn {
  from { stroke-dashoffset: var(--path-length); }
  to { stroke-dashoffset: 0; }
}

/* Set --path-length to the path's getTotalLength() value */
.connector path {
  stroke-dasharray: var(--path-length);
  animation: drawIn 0.8s ease-in-out both;
  animation-delay: calc(var(--i, 0) * 0.1s);
}
```

### CSS Counter (for hero numbers without JS)

Uses `@property` to animate a custom property as an integer, then display it via `counter()`. No JS required. Falls back to showing the final value immediately in browsers without `@property` support.

```css
@property --count {
  syntax: '<integer>';
  initial-value: 0;
  inherits: false;
}

@keyframes countUp {
  to { --count: var(--target); }
}

.kpi-card__value--animated {
  --target: 247;
  counter-reset: val var(--count);
  animation: countUp 1.2s ease-out forwards;
}

.kpi-card__value--animated::after {
  content: counter(val);
}
```

### Choreography

Don't use the same animation for everything. Mix types by element role, with easing stagger (fast-then-slow, not linear):

- **Cards**: `fadeUp` — the default entrance, reliable and subtle
- **KPI / badges**: `fadeScale` — scale draws the eye to important numbers
- **SVG connectors**: `drawIn` — reveals flow direction, pairs with card stagger
- **Hero numbers**: `countUp` — counting motion signals "this number matters"
- **Stagger timing**: `calc(var(--i) * 0.06s)` with lower `--i` values on important elements so they appear first

### Respect Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Sparklines and Simple Charts (Pure SVG)

For simple inline visualizations without a library:

```html
<!-- Sparkline -->
<svg viewBox="0 0 100 30" style="width:100px;height:30px;">
  <polyline points="0,25 15,20 30,22 45,10 60,15 75,5 90,12 100,8"
    fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round"/>
</svg>

<!-- Progress bar -->
<div style="height:6px;background:var(--border);border-radius:3px;overflow:hidden;">
  <div style="height:100%;width:72%;background:var(--accent);border-radius:3px;"></div>
</div>
```

## Responsive Breakpoint

Include a single breakpoint for narrow viewports:

```css
@media (max-width: 768px) {
  .arch-grid { grid-template-columns: 1fr; }
  .pipeline { flex-wrap: wrap; gap: 8px; }
  .pipeline__arrow { display: none; }
  body { padding: 16px; }
}
```

## Badges and Tags

Small inline labels for categorizing elements:

```css
.tag {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 500;
  padding: 2px 7px;
  border-radius: 4px;
  background: var(--node-a-dim);
  color: var(--node-a);
}
```

## Lists Inside Nodes

For tool listings, feature lists, table columns:

```css
.node-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 12px;
  line-height: 1.8;
}

.node-list li {
  padding-left: 14px;
  position: relative;
}

.node-list li::before {
  content: '›';
  color: var(--text-dim);
  font-weight: 600;
  position: absolute;
  left: 0;
}

.node-list code {
  font-family: var(--font-mono);
  font-size: 11px;
  background: var(--accent-dim);
  color: var(--accent);
  padding: 1px 5px;
  border-radius: 3px;
}
```

## KPI / Metric Cards

Large hero number with trend indicator and label. For dashboards, review summaries, and impact sections.

```css
.kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
}

.kpi-card {
  background: var(--surface-elevated);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.kpi-card__value {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -1px;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.kpi-card__label {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-dim);
  margin-top: 6px;
}

.kpi-card__trend {
  font-family: var(--font-mono);
  font-size: 12px;
  margin-top: 4px;
}

.kpi-card__trend--up { color: var(--node-b, #059669); }
.kpi-card__trend--down { color: var(--red, #ef4444); }
```

```html
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-card__value">247</div>
    <div class="kpi-card__label">Lines Added</div>
    <div class="kpi-card__trend kpi-card__trend--up">+34%</div>
  </div>
  <!-- ... more cards -->
</div>
```

## Before / After Panels

Two-column comparison with diff-colored headers. For review pages, migration docs, and feature comparisons.

```css
.diff-panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

.diff-panels > * { min-width: 0; overflow-wrap: break-word; }

.diff-panel__header {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 10px 16px;
}

.diff-panel__header--before {
  background: var(--red-dim, rgba(239, 68, 68, 0.08));
  color: var(--red, #ef4444);
  border-bottom: 2px solid var(--red, #ef4444);
}

.diff-panel__header--after {
  background: var(--green-dim, rgba(5, 150, 105, 0.08));
  color: var(--green, #059669);
  border-bottom: 2px solid var(--green, #059669);
}

.diff-panel__body {
  padding: 16px;
  background: var(--surface);
  font-size: 13px;
  line-height: 1.6;
}

/* Highlight changed items within a panel */
.diff-changed {
  background: var(--accent-dim);
  border-radius: 3px;
  padding: 0 3px;
}

@media (max-width: 768px) {
  .diff-panels { grid-template-columns: 1fr; }
}
```

```html
<div class="diff-panels">
  <div class="diff-panel__header diff-panel__header--before">Before</div>
  <div class="diff-panel__header diff-panel__header--after">After</div>
  <div class="diff-panel__body">Previous implementation...</div>
  <div class="diff-panel__body">New implementation...</div>
</div>
```

## Collapsible Sections

Native `<details>/<summary>` with styled disclosure. Zero JS, accessible. For lower-priority content: file maps, decision logs, reference sections.

```css
details.collapsible {
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

details.collapsible summary {
  padding: 14px 20px;
  background: var(--surface);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text);
  transition: background 0.15s ease;
}

details.collapsible summary:hover {
  background: var(--surface-elevated, var(--surface));
}

details.collapsible summary::-webkit-details-marker { display: none; }

/* Chevron indicator */
details.collapsible summary::before {
  content: '▸';
  font-size: 11px;
  color: var(--text-dim);
  transition: transform 0.15s ease;
}

details.collapsible[open] summary::before {
  transform: rotate(90deg);
}

details.collapsible .collapsible__body {
  padding: 16px 20px;
  border-top: 1px solid var(--border);
  font-size: 13px;
  line-height: 1.6;
}
```

```html
<details class="collapsible">
  <summary>File Map (14 files changed)</summary>
  <div class="collapsible__body">
    <!-- content here -->
  </div>
</details>
```

## Generated Images

For SVG or raster illustrations embedded inline. Use sparingly: hero banners, conceptual illustrations, educational diagrams, decorative accents.

### Hero Banner

Full-width image cropped to a fixed height with a gradient fade into the page background. Place at the top of the page before the title, or between the title and the first content section.

```css
.hero-img-wrap {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 24px;
}

.hero-img-wrap img {
  width: 100%;
  height: 240px;
  object-fit: cover;
  display: block;
}

/* Gradient fade into page background */
.hero-img-wrap::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to top, var(--bg), transparent);
  pointer-events: none;
}
```

```html
<div class="hero-img-wrap">
  <img src="data:image/png;base64,..." alt="Descriptive alt text">
</div>
```

Generate with `--aspect-ratio 16:9` for hero banners.

### Inline Illustration

Centered image with border, shadow, and optional caption. Use within content sections for conceptual or educational illustrations.

```css
.illus {
  text-align: center;
  margin: 24px 0;
}

.illus img {
  max-width: 480px;
  width: 100%;
  border-radius: 10px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.illus figcaption {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-dim);
  margin-top: 8px;
}
```

```html
<figure class="illus">
  <img src="data:image/png;base64,..." alt="Descriptive alt text">
  <figcaption>How the message queue routes events between services</figcaption>
</figure>
```

Generate with `--aspect-ratio 1:1` or `--aspect-ratio 4:3` for inline illustrations.

### Side Accent

Small image floated beside a section. Use when the illustration supports but doesn't dominate the content.

```css
.accent-img {
  float: right;
  max-width: 200px;
  margin: 0 0 16px 24px;
  border-radius: 10px;
  border: 1px solid var(--border);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

@media (max-width: 768px) {
  .accent-img {
    float: none;
    max-width: 100%;
    margin: 0 0 16px 0;
  }
}
```

```html
<img class="accent-img" src="data:image/png;base64,..." alt="Descriptive alt text">
```
