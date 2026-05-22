# Voice & Diction

The words on a cc-viz page carry as much weight as the layout. Wrong voice is unrecoverable through better palette or typography. Read this section while drafting any prose-led page (memo, brief, recap, decision doc); skim for diagram-only pages.

---

## Audience first, register second

The five gates in SKILL.md Step 1 (spine, ground claims, report-vs-argument, re-teaching audit, translation audit) are not optional. The audience determines vocabulary, density, and pronoun choice. Get the audience wrong and every downstream choice compounds the error.

| Audience | Register | Pronoun | Vocabulary |
|---|---|---|---|
| Self (working notes, own brief) | Confessional, engineering-honest, second-person | *you* | Whatever you'd use in your head |
| Small team you work with | Plain, direct, board-memo, first-person plural | *we, our* | Plain English; technical terms only when load-bearing |
| Engineering team / technical peers | Technical-precise, jargon allowed | *we, our* | Domain vocabulary fine |
| External / client / public | Polish-grade, no internal jargon | depends on register; usually third-person declarative | Concrete and specific; never marketing-warm |
| Executive / leadership | Executive-impact, strategic | depends; often third-person declarative | Numbers, tradeoffs, no implementation detail |
| Postmortem / historical | Past-tense narrative | varies | Specific to the incident |

If the audience isn't named explicitly in the request, default to **the team that owns the work**: the people who would read this if it were finished. The agent's most common audience-leakage failure is defaulting to "abstract stakeholder" when the real audience is the small team.

> **Story arc and reader baseline** belong to story framing, not diction. See `story-framing.md` for the spine sentence requirement, the report-vs-argument distinction, and the reader's-knowledge-baseline audit. This file covers voice and diction only.

---

## Diction rules

### Forbidden vocabulary (body prose)

These words and phrases trigger the "AI authored this" reflex in technical readers. Eliminate from body prose:

| Category | Forbidden |
|---|---|
| Marketing slop | *leverage, unlock, robust, seamless, powerful, intuitive, comprehensive, elegant, harness, delve, in essence, at its core, cutting-edge, state-of-the-art* |
| Vague volume | *various, numerous, multiple, a range of, a variety of, several* |
| Weak hedges | *essentially, basically, in many ways, to a large extent, generally speaking* |
| Empty intensifiers | *very, really, quite, incredibly, extremely* |

**Adjective stacking.** No string of three adjectives in a row. *"A robust, scalable, modern architecture..."* is a tell. Pick one adjective that earns its place.

### Em dashes: banned in body prose

The em dash (`—`) interruption pattern is the strongest AI tell in 2026. The interruption pattern appears in nearly every LLM-authored paragraph and reads as machine cadence.

**Rule:** Zero em dashes in body prose. Allowed only in citation lines (`— Author, Source`).

**En dashes** (`–`) inside numeric ranges only (`5–10`), never as a punctuation substitute.

**Replacements:** comma, period, parentheses, or rephrase to remove the interruption entirely.

### Sentence and paragraph caps

- Body sentences: ≤22 words. **Exception:** one longer sentence per page is allowed for technical-precision content (API contracts, invariants, edge-case conditions). Use sparingly.
- Body paragraphs: ≤3 sentences. Most should be 1–2.

The read-aloud test: if you can't say the sentence in one breath, it's too long.

### Direct address scoping

Use *you* and *your* only when the reader is an actor in the sentence:
- System behavior they experience: *"when you go quiet for 30 minutes"*
- Touchpoints: *"your data flows in through the connector"*
- Workflow consequences: *"if your code breaks one of these, your code is wrong"*

Do NOT use direct address in:
- Meta-framing about the page itself: *"You read this to get a mental model"*. The reader is already reading.
- Neutral reference captions: *"You'll find one row per classified event in the observations table"*. Schemas don't have actors.

Prefer: *"This page walks the pipeline top to bottom"* over *"You read this page to walk the pipeline top to bottom."*

**Exceptions:** postmortems and historical timelines may use past-tense narrative without direct address.

---

## Anti-yap heuristics

Sprawl is the default failure mode of LLM-authored visualizations. More sections, more paragraphs, more cards "to be thorough." Every section, paragraph, and card must earn its place against this question: *"What does THIS reader specifically gain from this, here, in this register?"* If you can't answer in one sentence, cut.

Hard heuristics:

- **Cut every sentence that starts with a hedge.** *"It's worth noting that…"*, *"In essence, …"*, *"Generally speaking, …"*. The sentence after the hedge is usually fine; the hedge is the yap.
- **Cap section count.** Diagram page 4–8 sections; recap 5–8; deck 8–24 slides. If you're past 10 sections on a diagram page, you're info-dumping. Merge or cut.
- **One thought per card.** Cards holding 3+ paragraphs are a section pretending to be a card. Either promote to a section or cut down.
- **Don't restate the visual in prose.** Prose adds the why, the constraint, the gotcha. Not a verbal version of the diagram.
- **Trim before commit.** Draft, then strike a third. The version that ships is the third draft, not the first.

---

## Headings: narrate vs label

**Story sections** narrate a claim or a beat:
- *"Three layers, one full cycle"* > *"Architecture Overview"*
- *"Where it has been, and where it is now"* > *"Roadmap"*
- *"Sources flow into one substrate, then leave as pages"* > *"Data Flow"*
- *"Five paths. One we'd pick. Three we wouldn't"* > *"Options"*

**Reference sections** (file maps, schema reference, decision logs, invariant lists, dependency tables) MAY use literal headings when scanability matters more than voice:
- *"Schema reference"*: fine, this is a Cmd-F target
- *"File map"*: fine
- *"Invariants"*: fine

The test: *would a reader Cmd-F to find this section?* If yes, the heading should be the word they'd search for.

If a story heading reads like a textbook table of contents, rewrite it.

---

## Italic emphasis is a budget

One italic-color emphasis point per heading, per pull quote, per card. Not two italic-color phrases competing in the same element. At display scale (≥40px) on serif headlines, prefer zero italic emphasis.

**Wrong:**
> What we should *do*, and *do* first.

(Two italic *do*s plus the lede underneath also has an italic phrase. Three accent points in the same hero element.)

**Right:**
> What we should do, and do first.
>
> Two products are live. Neither has been launched. The community keeps asking the foundational questions, and the wedge has been hiding in plain sight: *methodologies that just work for non-developers.*

(Heading is plain; italic emphasis budget spent on the lede's load-bearing phrase.)

---

## Register match by section

Even within one register, different page sections speak differently:
- **Hero / lede:** State the spine. Single italic emphasis if any.
- **Body sections:** Hold the chosen register. No mid-page register shifts.
- **Reference / data tables:** Plain declarative. No editorial flourish.
- **Pull quotes:** The strongest sentence on the page, italic display, properly cited.
- **Closings / colophons:** Brief, return to the hero's register.

A page where the hero is editorial-warm and the closing is engineering-formal feels like two writers. Pick one register and hold it.

---

## Audience-leakage warning

When a request gives both a subject and an audience, the audience determines the *register*, not the *subject*. If subject = X, the page is about X regardless of who's reading.

**Failure pattern observed:** subject = a technical codebase, audience = a non-engineering team. Agent picks a generic non-technical example to fit the audience. Subject lost.

**Fix:** state subject and audience as separate constraints in the Frame step. Don't let one override the other.
