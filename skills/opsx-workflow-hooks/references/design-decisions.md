# Design Decisions for opsx-workflow-hooks

## 2026-07-30 Session Decisions

### 1. Dual-path sync requirement
- Source of truth: `agent-skills/skills/opsx-workflow-hooks/SKILL.md`
- Runtime path: `~/.agents/skills/opsx-workflow-hooks/SKILL.md`
- Both MUST be updated when changing this skill or opsx commands
- OpenSpec updates may overwrite `~/.agents/commands/opsx/*.md`, erasing hook injections
- The Bootstrap section handles re-injecting hooks when they're lost

### 2. Review priority order (user-confirmed)
1. Agent built-in `/review` — try first
2. `code-review` skill — primary skill fallback
3. `java-code-review` skill — Java/Spring-specific pass
4. `security-audit` — for security-sensitive flows
5. Other review skills — if none of the above
6. Manual inspection — final fallback

### 3. Skill invocation limitation
Skills cannot directly invoke slash commands (`/review`, `/opsx:archive`, etc.).
The correct approach:
- For review: use the Skill tool to load `code-review` or `java-code-review` into context
- For `/review`: the agent runtime handles this natively; if unreachable, fall through to skill-based review
- For `/opsx:verify` and `/opsx:archive`: these are invoked as slash commands by the agent, not by the skill

### 4. Tiny-change direct execution (Hook A)
- Threshold: `<= 5` changed lines, single file, no new function/API/schema
- Even tiny changes MUST go through `/review`-first review flow
- No `/opsx:apply`, no archive, no task completion marking
- Returns to feedback loop after review

### 5. 7-Phase workflow mapping
| Phase | Hook | Primary tools |
|-------|------|---------------|
| 0 - Requirement clarification | Hook A | `grill-me` |
| 1 - Spec solidification | Hook A | `to-spec`, OpenSpec propose |
| 2 - Architecture & task atomization | Hook A | `brainstorming`, `writing-plans` |
| 3 - Implementation execution | (via /opsx:apply) | Superpowers execution |
| 4 - Test-driven boundary strengthening | (via /opsx:apply) | TDD + edge-case checks |
| 5 - Layered code review | Hook B | `/review` → `code-review` → `java-code-review` |
| 6 - Verification and archive | Hook B | `/opsx:verify` → `/opsx:archive` |

### 6. Minimum viable skill integration
Do NOT load all superpowers/matt-skills. The minimum effective set:
- Hook A: `grill-me` + `brainstorming` + `writing-plans`
- Hook B: `/review` + `code-review` + `java-code-review`

### 7. Hook A feedback prompt enhancement
When asking the user for feedback after propose, include 1-2 optional proposal prompts:
1. Add a missing edge case or acceptance condition
2. Simplify one implementation step or split an oversized task
These must stay within the current proposal's scope — never invent new product requirements.
