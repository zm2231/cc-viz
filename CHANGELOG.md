# Changelog

## [1.2.0]

Major iteration on the skill itself based on field testing and an independent cold audit.

### Workflow
- Reframed Step 0 as explicit routing (Quick share / Internal brief / External deliverable / Diagram / Slide deck / Multi-doc / Mode-specific). Surfaces clarifying questions only when context is genuinely ambiguous.
- Added Step 0.5 (ask if ambiguous, skip if clear) and Step 0.7 (load `.cc-viz/context.md` for project-scoped accumulated judgment).
- Restructured Step 1 as five hard gates: Spine sentence, Ground claims, Report-vs-argument, Re-teaching audit, Translation audit (Gate 5 only fires for non-expert audiences). Spine sentence is fill-in-the-blank with hard "stop if blank" rule.

### Voice and aesthetic
- Added forbidden body fonts: Space Grotesk, Manrope, General Sans, Cabinet Grotesk (current-decade AI-startup landing-page tells). Italic-by-design display serifs now in `--font-display` only.
- Added 3 reading-serif pairings (Source Serif 4, Lora, Newsreader). The 16-pairing catalog is the strongest "document, not landing page" signal cc-viz can make.
- Atmosphere rule split into reading-friendly (prefer) vs spectacle (skip) — pulls cc-viz away from brand-site feel.
- Italic emphasis in display headlines discouraged. Title-slide italic emphasis target is zero.

### Templates and references
- New `templates/font-loaders.html` — ready-to-paste `<link>` blocks for all 16 pairings + Fontshare/Satoshi.
- New `templates/multi-doc-site/` — markdown + render.py + styles.css scaffold for editable multi-page sites.
- New `references/story-framing.md` — full grounding-pass methodology and report-vs-argument depth.
- New `references/anti-patterns.md` — catalog of failure modes.
- New `references/patterns.md` — catalog of compositions that landed in real runs.
- New `references/quality-rubric.md` — 6-dimension graded rubric (Form-Audience 25 / Story 20 / Voice 20 / Grounding 15 / Visual 15 / Anti-pattern 5 = 100, pass ≥75).
- New `references/voice-and-diction.md` — diction rules, sentence caps, italic budget, banned vocabulary.
- New `scripts/strip-html.py` — strip HTML to readable markdown for grounding fact-checks.
- Fixed Mermaid zoom controls: `style.zoom` (not `transform: scale`) + `mermaid.run().then()` post-processor to remove hardcoded SVG height.

### Quality enforcement
- Pre-ship Bash grep checks added (em-dashes, forbidden fonts, forbidden colors, Mermaid post-processor, atmosphere) for shell-enabled surfaces.
- "When NOT to use cc-viz" section: small tables, one-line answers, code-as-artifact, discussion-not-document, marketing/UI/brand sites.

## [1.0.0]

Initial release as cc-viz — a Claude Code skill for generating self-contained HTML visualizations.

### Commands
- `/generate-web-diagram` — generate a styled HTML diagram for any topic
- `/generate-slides` — generate a magazine-quality slide deck presentation
- `/diff-review` — visual diff review with before/after architecture, code review, decision log
- `/plan-review` — cross-reference an implementation plan against the actual codebase
- `/project-recap` — mental model snapshot for context-switching back to a project
- `/fact-check` — verify factual claims in a document against actual code

### Skill
- 11 diagram types with automatic routing (Mermaid, CSS Grid, HTML tables, Chart.js, dashboards)
- 4 reference templates with deliberately distinct palettes (terracotta/sage, teal/cyan, rose/cranberry, midnight editorial)
- Proactive table rendering — HTML instead of ASCII for any table with 4+ rows or 3+ columns
- Zoom controls on all Mermaid containers (buttons, scroll-to-zoom, drag-to-pan)
- Both light and dark themes via CSS custom properties and `prefers-color-scheme`
- Slide deck mode with 10 slide types, cinematic transitions, and 4 curated presets
- Anti-slop guardrails — explicit forbidden fonts, colors, effects, and layout patterns
- Output to `~/.agent/diagrams/`, opens in browser automatically

### Design References
- `css-patterns.md` — depth tiers, animations, overflow protection, component patterns
- `libraries.md` — Mermaid theming, Chart.js, anime.js, 13 font pairings
- `responsive-nav.md` — sticky sidebar TOC on desktop, scrollable bar on mobile
- `slide-patterns.md` — slide engine, all 10 type layouts, transitions, compositional variety rules
