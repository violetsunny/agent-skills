# AGENTS.md

This repo is a **Skill package** for AI agents (Claude Code / Codex / Cursor). It generates single-file HTML slide decks. There is no build system, no package.json, no test framework — just templates, reference docs, and Node.js validation scripts.

## Architecture

Two independent visual systems, **never mixable**:

- **Style A** (电子杂志风): `assets/template.html` + `references/layouts.md` (10 layouts) + `references/themes.md` (5 presets) + `references/components.md`
- **Style B** (瑞士国际主义): `assets/template-swiss.html` + `references/layouts-swiss.md` (22 locked layouts S01–S22) + `references/themes-swiss.md` (4 presets) + `references/swiss-layout-lock.md`

Same-named classes have **different visual behavior** across templates (e.g. `h-hero` is serif in A, sans-serif ExtraLight in B). A deck must use exactly one system.

`assets/motion.min.js` — Motion One local copy for offline animation fallback.

`assets/screenshot-backgrounds/` — WebP background assets for CleanShot X-style screenshot framing (style-a: 5 sets, style-b: 4 sets).

## Validation Scripts

Node.js 20+ required. No dependencies to install — scripts use only Node builtins (+ optional Playwright for render measurement).

```bash
# Swiss deck structural + render validation (Style B only)
node scripts/validate-swiss-deck.mjs path/to/index.html
# Allow experimental layouts (rare, only when user explicitly requests)
node scripts/validate-swiss-deck.mjs path/to/index.html --allow-experimental

# Presenter mode validation (both styles, for formal presentations)
node scripts/validate-presenter-mode.mjs path/to/index.html
node scripts/validate-presenter-mode.mjs path/to/index.html --target-minutes 30

# Cross-template presenter runtime drift check (run before committing template changes)
node scripts/check-presenter-runtime-sync.mjs
```

`validate-swiss-deck.mjs` does static checks always; if Playwright is available in the environment, it also measures real DOM overflow, bottom whitespace, nav safety line, and title gaps (M1/M2 metrics).

## CI

`.github/workflows/presenter-runtime-sync.yml` runs `check-presenter-runtime-sync.mjs` on every PR and push to main that touches `assets/template*.html`. The two templates must keep their presenter CSS and JS blocks **byte-identical** (delimited by `/* ====... 演讲者模式 ...==== */` markers).

## Critical Rules (most common bug sources)

1. **Template is the only source of truth for class names.** Before writing any slide HTML, read the chosen template's `<style>` block. If a class from layouts.md is missing in the template, add it to the template's `<style>` — never inline-redefine per slide.
2. **No custom hex colors.** Only preset themes from `themes.md` / `themes-swiss.md`. Reject user-supplied hex values.
3. **Style B: only S01–S22 layouts.** Every `<section class="slide">` must have `data-layout="Sxx"`. Do not invent S23+ unless user explicitly asks for experimental mode.
4. **Style B: one accent color per deck.** No multi-color highlighting.
5. **Style B: no gradients, shadows, or border-radius.** Hairline (1px) dividers are the only exception.
6. **Style B: large text uses weight 200 (ExtraLight).** Font weight must decrease as font size increases. 16px body text minimum weight 400.
7. **Style B: large font-size must be double-constrained** — `font-size: min(Xvw, Yvh)`. vw-only overflows on standard 16:9 screens.
8. **Replace `[必填]` placeholder in `<title>`** immediately after copying template. Grep for `[必填]` to confirm all replaced.
9. **Presenter notes stored by stable `data-slide-id`**, not array index or page number — reordering pages must not break note persistence.
10. **Images use standard ratios only** (21:9, 16:9, 16:10, 4:3, 3:2, 1:1). Never copy raw image pixel dimensions.

## Style B Layout Selection

Read `swiss-layout-lock.md` **before** `layouts-swiss.md`. The lock file defines which layouts are registered and the hard constraints.

- 7–8 page deck: ≥ 6 distinct S-numbers
- 10+ page deck: ≥ 8 distinct S-numbers
- No 3 consecutive pages with same structure
- Image pages: single large image → S22; 2–3 images → S15/S16 grid adaptation

## Swiss Map Component (S08 extension)

For geographic/historical/city relationship pages, use `S08 + Swiss Map Component` per `references/swiss-map-component.md` (MapLibre-based). Still write `data-layout="S08"`.

## Contribution Constraints

- Do not invent new default body layouts without explicit discussion.
- Adding a class to `template-swiss.html` requires syncing `layouts-swiss.md` + `swiss-layout-lock.md` + `validate-swiss-deck.mjs`.
- Presenter runtime changes must update **both** templates + `presenter-mode.md` + `checklist.md` + `validate-presenter-mode.mjs`.
- New themes go in `themes.md` / `themes-swiss.md` with recommended use cases.
- Run `check-presenter-runtime-sync.mjs` before committing any template change.

## File Roles

| File | Role |
|------|------|
| `SKILL.md` | Skill entry point: full workflow, design principles, class pre-flight lists |
| `references/checklist.md` | P0/P1/P2/P3 quality checklist — P0 issues are blocking |
| `references/presenter-mode.md` | Speaker note schema, rehearsal, audience screen sync contract |
| `references/image-prompts.md` | GPT-Image / GPT-M prompt templates for deck illustrations |
| `references/screenshot-framing.md` | CleanShot X-style screenshot adaptation semantics |
| `docs/unification-plan.md` | Internal planning doc (not user-facing) |

## Key Design Philosophy

This skill is **opinionated by design**. Constrained layout systems produce more reliable AI-generated decks than unlimited customization. When in doubt, preserve existing visual rules and improve the workflow around them.
