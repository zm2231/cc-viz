# Page Title

> Lede sentence — sits right under the h1. First blockquote becomes the styled `.lede` paragraph (serif, larger, max-width-constrained). One sentence; the page's spine in compressed form.

**TL;DR.** One-paragraph summary of this page. Becomes a styled TLDR block (label + body grid). Three to five sentences max. Says what the page argues and what the reader walks away knowing.

## First section

Each `<h2>` gets an auto-numbered marker (01, 02, ...) and an anchor id (slugified from the heading text). The sidebar TOC on the right links to every h2.

Inline status codes use backticks: `PASS`, `FAIL`, `WARN`, `OPEN`, `LOCKED`. Add a date or context after the token and the whole thing becomes the badge label: `PASS 2026-05-04` renders as a single styled span.

Sub-points use normal markdown:

- Bulleted lists with one item per line
- Inline `code spans` for technical references
- **Bold** for emphasis on key terms
- *Italic* sparingly — one emphasis point per heading or paragraph

### Subsection

`<h3>` is body-font, bold, smaller. Used for deeper structure inside a section. Doesn't get a number or anchor.

#### Mono label

`<h4>` renders as a mono-font uppercase label. Use for short scan-markers above a list or callout.

## Second section

Tables render with mono uppercase headers and clean dividers:

| Column A | Column B | Status |
|---|---|---|
| Row 1 thing | What it does | `PASS` |
| Row 2 thing | What it does | `OPEN` |

Code blocks use triple backticks:

```python
def example():
    return "code blocks have surface background and a border"
```

Blockquotes (after the lede) render with an accent left-border and tinted background:

> A pull quote or callout. Stands out from body prose. Use sparingly — they're scan-stoppers.

## Third section

The page can be as long as it needs to be. The sidebar TOC stays sticky so readers can navigate between sections without losing place. On mobile (<960px) the TOC hides and the article goes full-width.

If a section needs a custom visual treatment (a diagram, a ladder, a custom hero), add a marker comment:

<!-- diagram: my-custom-diagram -->

Then add a regex hook in `render.py` that recognizes the marker and injects a hand-crafted HTML snippet. The marker stays in the markdown source; the visual lives in the script.

---

**Drafted YYYY-MM-DD.** Page-level provenance or revision notes go at the bottom.
