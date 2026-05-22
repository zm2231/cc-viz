# Story framing

Elaboration of SKILL.md Step 1. The inline rules (frame story before drafting, ground claims, voice rules) are load-bearing and stay in SKILL.md. This file holds the *how*: the grounding-pass methodology, the report-vs-argument distinction at depth, and the reader-baseline discipline.

Load this when the routed mode is Internal brief, External deliverable, Strategic / decision memo, or anytime the page is making claims about a real system, project, person, market, or decision and the stakes warrant grounding past README-depth.

> **Example spine sentences below are illustrative, built around a hypothetical "ingestion service" subsystem. Substitute your own subject when applying the methodology. The shape of the framing matters, not the names.**

## The grounding pass

Speculation reads identical to truth on the page; only the reader who knows the territory can tell the difference. Adjust depth to the routed mode (Quick share = lean on what's loaded; Internal brief = thorough; External deliverable = exhaustive). Never skip it entirely.

The methodology is generic; the tooling is whatever this user or project has wired up. The skill does not mandate specific tools. It mandates that grounding happens.

**Read the system's actual state, not its description of itself.**
- For a codebase: the entry file end-to-end, every config that defines runtime bindings, the schema or migrations, a sample of route handlers or core modules, the recent commit log.
- For a project or team: recent meeting/decision artifacts, ownership notes, what's moved in the last weeks.
- For a market or competitive landscape: current state of the named players (their docs, their changelogs, their recent shipping cadence), not training-stale impressions.

**Check what's been changing.** `git log` for code, recent activity feeds for projects, recent web/news for markets. The story should foreground what's *currently* in motion, not what the docs froze months ago.

**Read the corner files.** `CLAUDE.md`, `AGENTS.md`, `DEVELOPMENT.md`, design docs in subdirectories. These often hold the real invariants and gotchas the top-level README skips.

**Use whatever evidence corpora the surface exposes.** On Claude.ai web/desktop: web search and uploaded files. In Claude Code (CLI / IDE) or another shell-enabled surface: also the project's grep/search tools, semantic indexes, MCP-exposed services, vector indexes over your own corpus, transcripts, prior session notes. The methodology is identical; the available tools differ.

If a brief was prepared upstream by a research agent or by the user, use it. If not, do the work yourself before drafting. Either way, the story is built from the actual state of the thing being visualized, not from the marketing version of it.

## Report vs argument

These are not the same kind of page and they need different structures.

A **report** presents facts. *"Here are the eight source connectors. Here are the four layers. Here are the columns and thresholds."* The reader walks away knowing what exists. Spine is the inventory; structure is the matrix or the schema.

An **argument** makes a claim. *"The ingestion service was built to extract a four-dimension framework but quietly invented two things the framework hasn't named yet: system metacognition and source-level epistemics. The interesting question is whether they generalize."* The reader walks away with a position they can agree with, push back on, or build on. Spine is the claim; structure is claim → evidence → implication.

Most analytical, mapping, comparison, synthesis, decision-memo, or strategic work is argument-led. The artifacts (files, columns, thresholds, schema references, commit hashes, framework citations) are *evidence FOR the argument*, not the argument itself. A page that lists "these files exist, these columns exist, this maps to that" has shown evidence; it has not told a story. The page must be summarizable in one sentence as: *"X is the case, and here's why it matters."*

If you find yourself building a feature inventory or a matrix as the page's spine, ask whether the page should be a report (intent: catalog or reference) or an argument (intent: make a claim about what the catalog means). For argument intent, restructure: lead with the load-bearing claim, support each section with the evidence that defends it, close with the implication. The matrix may still appear, but as one supporting element under a claim, not as the page's backbone.

## Story arc

From start to end, what does the reader walk away knowing? State it in one sentence. *"The ingestion service classifies every incoming event against the existing entity graph and surfaces confirmed patterns to the editor surface. Backed by one Postgres and one inference gateway."* If you can't write that sentence, the diagram has no spine.

The arc is the page's compression. Each section either advances the arc or supports it with evidence. Sections that do neither are decoration and should be cut.

## Audience and level

A developer reading code (technical depth, jargon OK) ≠ a teammate joining the project (mental model, label-what-things-are) ≠ an executive reviewing a proposal (impact, tradeoffs, no implementation). Density and vocabulary follow audience.

Name the audience concretely before drafting. Not "technical reader" but "senior backend engineer who knows our stack but hasn't seen this subsystem." Not "exec" but "VP eng deciding whether to greenlight the rewrite." Specificity here forces specificity in vocabulary and density downstream.

## Register and voice

Pick one and hold it across every label, heading, and paragraph. Mixing registers is what makes prose feel AI-generated.

- **Editorial-narrative.** *"Three layers, one Dream cycle."* Voice-driven, declarative. For strategy briefs, narrative explainers, when the prose is the art.
- **Technical-precise.** *"FOR UPDATE SKIP LOCKED, total-order claim."* Names the primitives. For codebase explanations to peers.
- **Engineering-confessional.** *"We got this wrong twice."* Honest about the path. For post-mortems, lessons-learned, retro decks.
- **Executive-impact.** *"60% reduction in classification miss rate."* Numbers and consequence. For leadership reviews, proposals, board memos.

The form chosen in Step 2 constrains register. Magazine editorial doesn't mix with executive-impact; broadside doesn't mix with engineering-confessional. If the chosen register fights the form, change one of them. Don't ship the mix.

## Information at what level of detail

Every section answers a question the reader has at that point. The reader's questions arrive in an order. Answer them in that order.

Inventory what must appear (file paths, decision rationale, error rates, schema names) and assign each to the section where the reader will need it. Don't dump an inventory in one section and refer back to it; surface the relevant detail where the question lands.

## Reader's knowledge baseline

Separate two lists for the audience: *what they already know* and *what they need to know from this page*. The page exists only to close the gap between them. Re-teaching the first list reads as condescending; assuming the second is already known reads as opaque. Neither is digestible.

For technical subjects: name the reader's expertise level concretely (junior in this stack, senior in this stack, methodology specialist, executive who has seen demos). Then write to the gap, not from scratch and not from the assumption that everything is already understood. A page mapping a subsystem to a methodology framework should not re-introduce what the subsystem is to someone who built it; it should foreground the *mapping*, which is the new thing.

Ask, before writing each section: *"Does the reader already know this? If yes, why is it on the page?"*

Re-teaching is the most common failure mode for pages that look thorough but feel flat. The audit catches it.

## Connecting back to drafting

By the time you've worked through grounding, story arc, report-vs-argument, audience, register, info-detail, and baseline, the draft is mostly inevitable. You know what each section answers, in what order, in what voice, with what evidence. The drafting itself takes minutes; the framing took the work.

Skip the framing and the drafting takes ten rounds.
