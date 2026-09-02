---
description: "创建 OpenSpec 变更并生成全部规划产物，完成后进入迭代精化循环。/opsx-propose <变更名或需求描述>"
allowed-tools: Bash(openspec:*)
---

Propose a new change — create the change and generate all artifacts in one step, then enter an iterative refinement loop with the user.

**Planning boundary**: This workflow creates planning artifacts only. Do not edit project code. After the planning artifacts are complete and the user is satisfied, stop. Wait for a new user request to start implementation.

**Store selection:** If the user names a store or the work lives in one, run `openspec store list --json` to discover registered store ids, then pass `--store <id>` on commands that read or write specs and changes. Once selected, treat `--store <id>` as sticky for the rest of the workflow.

**Input**: The argument after `/opsx-propose` is the change name (kebab-case), OR a description of what the user wants to build. A requirement description is analyzed (goal, scope, ambiguities, suggested name) and confirmed with the user before the change is created.

$ARGUMENTS

---

## Phase 1: Create Artifacts

### Step 1 — Analyze the requirement in $ARGUMENTS

Classify the input first:

- **Empty** → ask the user (open-ended, no preset options):
  > "What change do you want to work on? Describe what you want to build or fix."
- **Kebab-case identifier** (e.g., `add-user-auth`) → treat it as the change name and skip the requirement analysis below.
- **Anything else** → treat it as a requirement description and analyze it before creating the change.

Requirement analysis for a requirement description:

- **Goal** — the core outcome the user wants to achieve
- **Scope** — what is included, and what is explicitly out of scope
- **Material ambiguities** — points that would affect scope, externally observable behavior, compatibility, or acceptance criteria
- **Suggested change name** — derive a kebab-case name (e.g., "add user authentication" → `add-user-auth`)

Present a short analysis summary to the user and confirm before creating the change.

**IMPORTANT**: Do NOT proceed without understanding what the user wants to build.

If the analysis surfaces ambiguity that would materially affect scope, externally observable behavior, compatibility, or acceptance criteria, ask the user before creating the change. For minor details, make a reasonable assumption and record it in the planning artifacts.

### Step 2 — Determine the workflow schema

Use the configured default schema unless the user explicitly requests a different workflow.

**Use a different schema only if the user:**
- Explicitly requests a specific schema by name → use `--schema <schema-name>`
- Asks to "show workflows" or asks "what workflows" exist → resolve the authoritative root by running `openspec context --json`, then run `openspec schemas --json` and let them choose.

Otherwise, omit `--schema` to preserve the configured default.

### Step 3 — Create the change directory

```bash
openspec new change "<name>"
```

Or with an explicit schema:
```bash
openspec new change "<name>" --schema "<schema-name>"
```

### Step 4 — Get the artifact build order

```bash
openspec status --change "<name>" --json
```

Parse the JSON to get:
- `applyRequires`: array of artifact IDs needed before implementation
- `artifacts`: list of all artifacts with `status` and `requires` edges
- `planningHome`, `changeRoot`, `artifactPaths`, and `actionContext`

### Step 5 — Create every artifact in the required set

Use a todo list to track progress. Loop through artifacts in dependency order:

a. **For each artifact that is `ready` (dependencies satisfied)**:
   - Get instructions:
     ```bash
     openspec instructions <artifact-id> --change "<name>" --json
     ```
   - The instructions JSON includes `context`, `rules`, `template`, `instruction`, `resolvedOutputPath`, `dependencies`
   - If `skipped` or `warning` is present, the change declares `skip_specs` and this artifact must NOT be created — stop and pick another artifact
   - Read any completed dependency files for context (re-read from disk, not conversation memory)
   - If `instruction` delegates to a specific skill or command, invoke it to produce the artifact
   - Otherwise create the artifact file using `template` as the structure and write to `resolvedOutputPath`
   - Apply `context` and `rules` as constraints — do NOT copy them into the file
   - Show brief progress: "Created <artifact-id>"

b. **Continue until every artifact in the required set exists**:
   - After creating each artifact, re-run `openspec status --change "<name>" --json`
   - The required set is `applyRequires` plus every artifact reachable by following `requires` edges transitively
   - `status` is file-existence only — a `done` artifact does NOT mean its dependencies exist. Use each artifact's `requires` edges, not its `status`, to build the required set
   - An artifact with `status: "skipped"` is satisfied — do not create it
   - Skip an artifact only when `status` reports it `skipped`, or when its own `instruction` field marks it optional (e.g., "create only if..."). Tell the user and do not reconsider
   - Dependencies are enablers, not gates: if a required artifact is `blocked` only because you skipped a conditional dependency, write it anyway
   - Stop when every artifact in the required set is `done`, `skipped`, or deliberately skipped

c. **If an artifact requires user input**: Ask, then continue.

### Step 6 — Show final status

```bash
openspec status --change "<name>"
```

Summarize:
- Change name and location
- List of artifacts created with brief descriptions
- "All artifacts needed for implementation are ready."
- Prompt: "The artifacts are ready for review. Entering refinement loop..."

### Artifact Creation Guidelines

- Follow the `instruction` field from `openspec instructions` — it is authoritative
- Read dependency artifacts before creating new ones — re-read from disk
- Use `template` as the structure for your output file
- `context` and `rules` are constraints for YOU, not content for the file — do NOT copy them into the artifact

### Phase 1 Guardrails

- Planning only — do NOT implement, edit project code, or start the apply workflow
- Create every artifact the apply phase transitively depends on
- If a change with that name already exists, ask if user wants to continue it or create a new one
- Verify each artifact file exists after writing before proceeding

---

## Phase 2: Iterative Refinement Loop (Hook A)

The first proposal is rarely final. This phase keeps the user in a fast iteration loop so the proposal converges before any implementation starts.

### Step 1 — Ask for feedback

Use the AskUserQuestion tool (open-ended, no preset options) to ask:

> "Proposal complete. Do you have any new ideas, changes, or concerns you'd like to incorporate before moving to implementation? If helpful, here are one or two optional proposal prompts to react to: (1) add a missing edge case or acceptance condition, (2) simplify one implementation step or split an oversized task. Enter your thoughts, or say 'looks good' / 'no' to proceed."

### Step 2 — Evaluate the response

- **If the user signals satisfaction** ("looks good", "no", "proceed", "go ahead", blank/empty, or affirmative with no actionable content):
  - Print: `Proposal locked. Run /opsx-apply when ready to implement.`
  - Stop. Do not loop.

- **If the user provides new ideas or concerns:**
  - Acknowledge the input briefly in one sentence.
  - First decide whether this is a **tiny artifact change** (≤ 5 changed lines, one artifact file, no new function/API/schema/task breakdown/design change/cross-file impact): apply directly and do lightweight validation only.
  - If requirement understanding is still materially incomplete or the user is choosing between competing directions, load `grill-me` before editing artifacts.
  - If not a tiny change, determine **one primary workstream** and use a fresh sub agent to analyze or draft artifact changes before the main thread writes them.

### Step 3 — Use sub agents as the default non-trivial planning worker

Launch a fresh sub agent when any of the following is true:
- the change affects more than one planning artifact
- the request changes scope, acceptance criteria, design, or task structure
- competing interpretations must be compared before editing
- substantial drafting is needed for proposal/design/tasks

Give the sub agent one narrow job: classify the request, propose exact artifact deltas, or draft replacement text.

After the sub agent returns, the main thread must:
- Review the result
- Write the actual artifact files
- Run `openspec status --change "<name>" --json`
- Summarize the update to the user

Do not let a sub agent directly close the user loop or declare the proposal locked.

### Step 4 — Route to the minimum effective planning skills

- **Backend code writing** (Java/Python services, APIs, persistence, integration): start with `codebase-design`. Add `spring-boot-patterns`, `design-patterns`, `jpa-patterns`, or `api-contract-review` only when directly relevant.
- **Frontend code auto-generation** (HTML/CSS/Vue, generated pages/components): load `ui-ux-pro-max` first and keep it active. Add `frontend-design` only when visual direction materially changes. Add `ui-styling` only for stack-specific constraints. Do not load `web-artifacts-builder` — this is planning-only.
- **Technical-solution or knowledge-content writing** (design docs, ADRs, proposals, tutorials): load `doc-coauthoring` first. Add `domain-modeling` when terminology boundaries matter. Add `research` only for fact-heavy claims. Add `teach` only for instructional content. Add `internal-comms` only for stakeholder-facing formats.

### Step 5 — Reflect the chosen workstream in the planning artifacts

- `proposal.md` — user-visible goals, acceptance criteria, scope
- `design.md` — architecture, UI/content structure, trade-offs, risks
- `tasks.md` — execution order plus matching review, test, and validation tasks

If a request spans multiple areas, keep one primary workstream and add only the minimum secondary skills.

### Step 6 — Classify the edit path

- **Tiny artifact change** — ≤ 5 changed lines, one file, no structural impact → shortcut path
- **Artifact-level change** — changes scope, design, acceptance criteria, task structure, or cross-file behavior → full path

### Step 7 — Apply the chosen path

**Tiny artifact change:**
- Update the small planning artifact directly.
- Do not edit implementation files.
- Run lightweight validation only.
- Report: `Applied tiny artifact update directly — updated <file>`
- Return to Step 1 and ask for more ideas.

**Artifact-level change:**
- Identify affected artifacts: scope/goal → `proposal.md`, architecture → `design.md`, tasks → `tasks.md`
- Update only affected files. Do not rewrite unaffected files.
- After writing, verify:
  ```bash
  openspec status --change "<name>" --json
  ```
- Confirm the artifact still shows `status: "done"`. If not, fix and re-check.
- Print a brief diff summary.
- Return to Step 1 and ask again.

### Step 8 — Loop until the user is satisfied

There is no forced exit. Keep iterating until the user explicitly signals they are done.

### Phase 2 Guardrails

- This phase is planning-only: never edit project code, even when the user asks for a tiny fix. Route implementation to `/opsx-apply`.
- For non-trivial planning work, prefer a fresh sub agent over doing all reasoning in the main thread.
- The main thread is the control plane: only it talks to the user, writes artifacts, runs OpenSpec status checks, and decides whether to loop or stop.
- Use the minimum effective skill set for the active workstream.
- `grill-me` is for materially incomplete requirements, not routine wording tweaks.
- Choose one primary workstream per iteration. Add secondary skills only when they directly support the same request.
- Ensure `tasks.md` records matching review, test, and validation work.
- If the user's input is ambiguous, treat it as a change request and propose an update, then ask for confirmation.
- Surgical edits only: change exactly what the user asked for, nothing more.
- If the user's request contradicts an existing artifact constraint, surface the conflict and ask which takes priority.
