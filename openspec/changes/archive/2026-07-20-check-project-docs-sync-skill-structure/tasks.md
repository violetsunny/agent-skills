## 1. Fix Nested Fenced Code Blocks

- [x] 1.1 In SKILL.md: change the outer opening fence of the AGENTS.md template block (line ~154) from ` ``` ` to ```` ```` ```` and its matching closing fence similarly
- [x] 1.2 In SKILL.md: change the outer opening fence of the README.md template block (line ~236) from ` ``` ` to ```` ```` ```` and its matching closing fence similarly
- [x] 1.3 In SKILL.md: change the outer opening fence of the project-map template block in Step 6a (line ~436) from ` ``` ` to ```` ```` ```` and its matching closing fence similarly
- [x] 1.4 Verify each of the three templates now renders as a single unbroken code block — also fixed Step 6b architecture template (same issue, caught during verification)

## 2. Fix README Self-Check Checkboxes

- [x] 2.1 In SKILL.md Step 4: replace all 6 `- [ ]` self-check items with `- ☐` (Unicode ballot box U+2610) to prevent GFM task-list parsing
- [x] 2.2 Verify no `- [ ]` pattern remains in the self-check section after the fix

## 3. Clean Up Step 0 Git Commands

- [x] 3.1 Remove the two lines in Step 0 (`git tag --sort=-version:refname | head -5` and `git log --oneline -20`) that produce unassigned output — annotated with `# 仅供参考 — 输出不赋值给变量，Step 5 会重新读取`
- [x] 3.2 Verify Step 0's bash block outputs only labelled variables (`PROJECT_ROOT:`, `INIT_COMMAND_FOUND:`, `HAS_*:`) or annotated informational lines

## 4. Annotate Optional Architecture Sections

- [x] 4.1 In the `docs/architecture.md` template in Step 6b: add `<!-- optional -->` after the `## 依赖关系` heading
- [x] 4.2 Add `<!-- optional -->` after the `## 扩展点` heading
- [x] 4.3 Add `<!-- optional -->` after the `## 已知限制` heading

## 5. Final Verification

- [x] 5.1 Read the full updated SKILL.md and confirm no remaining triple-backtick nesting issues in any template block — 4 pairs of 4-backtick fences confirmed (lines 155/215, 237/302, 437/478, 482/530)
- [x] 5.2 Confirm the self-check section contains no `- [ ]` GFM task markers — grep returned 0 matches
- [x] 5.3 Confirm Step 0 contains no unreferenced output-producing Git commands (or they are annotated) — annotation added on line 69
- [x] 5.4 Confirm the three architecture template sections carry `<!-- optional -->` annotations — lines 511, 515, 519
