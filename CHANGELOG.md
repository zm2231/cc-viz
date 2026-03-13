# Changelog

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
