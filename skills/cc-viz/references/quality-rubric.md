# cc-viz Quality Rubric

Six weighted dimensions, 100 points total. Every cc-viz output should be gradable against this rubric — no hand-patching outputs without naming the dimension that failed first.

Each dimension carries a `grading:` tag:
- `script` — mechanical check (regex, word count, file existence). No human or LLM judgment.
- `hybrid` — script catches obvious failures, judgment grades the rest.
- `judgment` — must be read by a grader. User-taste judgment routes to the human; domain-neutral judgment can be LLM-graded.

A passing output scores **≥ 75/100** with no FAIL on `script` or `hybrid` dimensions.

---

## Dimension 1: Form-Audience Match (25 pts) — `judgment`

The form chosen in Step 2 serves the routing call from Step 0 and the audience framed in Step 1. The structural vocabulary stays consistent end-to-end. No Frankenstein elements.

**PASS:**
- The form's structural vocabulary (e.g. board-memo's status strip + recommendation card + tables; magazine editorial's drop-cap + multi-column + colophon) is used consistently throughout the page.
- The form choice is justifiable from the routed intent (quick share, internal brief, external deliverable, diagram, slide deck, recap, decision memo).
- Audience-derived register (we / you / first-person plural / executive-impact / engineering-confessional) holds across every section heading and paragraph.

**FAIL:**
- A board-memo recommendation card appears inside a magazine spread, or a magazine drop-cap appears inside a board memo. Mixed structural vocabulary.
- The form was chosen for aesthetic reasons disconnected from the content shape (e.g., magazine editorial picked for matrix-shaped structural-mapping content).
- The register shifts mid-page (engineering-formal in one section, marketing-slop in another).

**Notes:** This is the highest-weighted dimension because form failure is unrecoverable through other improvements. A page with the wrong form looks polished and still doesn't work.

---

## Dimension 2: Story Discipline (20 pts) — `judgment`

The page has an identifiable spine and the right kind of spine. Argument-led work argues; report-led work catalogs cleanly. No re-teaching what the audience already knows.

**PASS:**
- The page can be summarized in one sentence as either "X is the case, here's why" (argument) or "here are the facts about X organized by Y" (report) — and the chosen shape matches the routed intent.
- For analytical, mapping, comparison, synthesis, or decision-oriented work: the spine is the load-bearing CLAIM, with artifacts (files, columns, citations) as evidence under it. Not a feature inventory with claims as footnotes.
- The page does not re-teach foundations the routed audience already knows. Re-introductions appear only where the audience genuinely needs them.

**FAIL:**
- The page reports when it should argue. The conceptual mapping (the new understanding) appears as embellishment under a feature list.
- The audience built the system being mapped, but the page spends 30%+ of its real estate explaining what they built.
- The page has no identifiable spine — sections accumulate but don't compose into a single takeaway.

**Notes:** This dimension caught the test-a14 → a16 inversion (matrix as spine vs argument as spine). When grading, ask: *"What's the one sentence the reader walks away with?"* If the answer is "here are the files" or "here are the dimensions," the spine is wrong.

---

## Dimension 3: Voice & Diction (20 pts) — `hybrid`

Script gates the mechanical failures; judgment grades register match.

**Script-checkable PASS criteria:**
- Zero em dashes (`—`) in body prose. Allowed only in citation lines (`— Author, Source`).
- Zero forbidden vocabulary in body prose: *leverage, unlock, robust, seamless, powerful, intuitive, comprehensive, elegant, harness, delve, in essence, at its core, cutting-edge, state-of-the-art, various, numerous, multiple, several, essentially, basically, very, really, quite, incredibly, extremely.*
- Zero adjective stacking (any string of three adjectives in a row).
- All body sentences ≤22 words. **Exception:** a single longer sentence per page is permitted for technical-precision content (API contracts, invariants, edge-case conditions).
- All body paragraphs ≤3 sentences.
- `--font-body` is not Inter (any variant: Inter, Inter Tight, Inter Display), Roboto, Arial, Helvetica, system-ui alone, Space Grotesk, Manrope, General Sans, Cabinet Grotesk, or an italic-by-design display serif (Instrument Serif, Playfair Display Italic, Fraunces Italic, EB Garamond Italic).

**Judgment PASS criteria:**
- Register matches the routed audience (we-pronoun for team-collaborative; you-pronoun for system-behavior or consequence prose; declarative third-person for framing/reference; past-tense narrative for postmortem).
- Direct address (you/your) appears only where the reader is an actor — system-behavior, touchpoints, or workflow consequences. Not in framing prose about the page itself, not in neutral reference captions.
- Single italic-emphasis point per heading, per pull quote, per card. Not two italic-color emphases competing in the same element.

**FAIL:** any script-checkable rule violated, or register mixes mid-page, or italic-emphasis budget exceeded.

---

## Dimension 4: Grounding (15 pts) — `hybrid`

Claims about real systems, projects, people, markets, or decisions are supported by verifiable evidence. No fabricated identifiers.

**Script-checkable PASS criteria:**
- Every claimed file path exists in the referenced repo.
- Every claimed table name, column name, or schema identifier exists in the referenced schema.
- Every claimed external citation (Anthropic marketplace state, framework definitions, market data) is dated or sourced.

**Judgment PASS criteria:**
- The grounding pass was performed at the depth the routed mode requires (Quick share = lean; Internal brief = thorough; External deliverable = exhaustive).
- Speculative claims are explicitly flagged as positions, not facts.
- Time/effort estimates are grounded in observed velocity (git log for codebases, recent activity for projects), not theoretical complexity.

**FAIL:**
- A file, table, or column referenced on the page does not exist in the repo (the fabricated-identifier failure mode).
- Claims about external state are training-stale (the "vendor will eventually ship" failure mode where the vendor already shipped months ago).
- Time estimates are 2-3× inflated relative to observed sprint velocity.

---

## Dimension 5: Visual Quality (15 pts) — `judgment`

Aesthetic distinct, atmosphere present, hierarchy clear.

**PASS criteria:**
- **The swap test.** Replacing the page's fonts and colors with a generic dark theme would noticeably degrade it. The aesthetic carries intent.
- **The void test.** For dark-mode pages: the corner of the page and the center are visually distinguishable (gradient, hairline grid, vignette, or focal accent glow present). Flat solid dark backgrounds fail.
- **The squint test.** Blurring the eyes still preserves the section hierarchy. Hero, section heads, body, captions are visually distinct.
- **The numerals test.** Numerical figures (KPI strips, timing estimates, tabular data) use mono tabular-numerals or a sans with `font-variant-numeric: tabular-nums`. NOT display serif italic.
- **The centering test.** Letter-in-circle or letter-in-badge elements use `display: inline-flex; align-items: center; justify-content: center` for centering. NOT `line-height` tricks.
- **The aesthetic budget.** A new page does not reuse the aesthetic of a recent prior session output (palette + typography combo).

**FAIL:** any of the above tests fails.

---

## Dimension 6: Anti-Pattern Free (5 pts) — `script`

None of the documented anti-patterns from `references/anti-patterns.md` fire. Each anti-pattern is regex-checkable.

**Script:** run the anti-pattern checks listed in `references/anti-patterns.md` against the generated HTML. Every fail is one point off this dimension.

---

## How to grade

For each generated page, produce a grade card:

```
test-aN-<slug>: 82/100
  ✅ Form-Audience Match (22/25)        — magazine editorial committed cleanly; minor weak spot in §III
  ❌ Story Discipline (10/20)           — page reports when intent was argument; mapping appears as footnote
  ✅ Voice & Diction (18/20)            — em-dash count 0; sentence cap respected; one slop word in §V
  ✅ Grounding (15/15)                  — every file/column/threshold verified
  ✅ Visual Quality (12/15)             — aesthetic distinct; void test passes; numerals fail
  ✅ Anti-Pattern Free (5/5)            — clean
```

Save grade cards to `evals/iteration-N/grades.md` if running an iteration loop.

Use `<thinking>` blocks when grading judgment dimensions:

```xml
<thinking>
Story Discipline check on test-a14:
- The page presents a layer × dimension matrix as the spine
- The conceptual claims (system-M ≠ user-M, source-priors-as-unclaimed-E) appear in §iii as supporting
- One-sentence summary attempt: "here are the artifacts that touch each dimension" — that's a report sentence
- But the routed intent was argument-led structural mapping
- Mismatch: spine is artifact-led, intent was claim-led
→ FAIL
</thinking>
```

## When this rubric needs updating

Add a new dimension or refine an existing one when:
- A failure mode appears that no current dimension catches (add to anti-patterns first; promote to a dimension only if it's load-bearing).
- A dimension stops discriminating (every output passes it) — collapse it into another or replace it.
- The user surfaces a quality concern that grades against an unscored axis (digestibility was added this way; report-vs-argument was added this way).

This rubric was last refined: 2026-04-30 after the cc-viz refactor session.
