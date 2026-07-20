## 1. Verify Current SKILL.md Structure

- [x] 1.1 Read `skills/project-docs-sync/SKILL.md` and confirm frontmatter version is `"2.0"`
- [x] 1.2 Confirm the skill description field includes all new trigger phrases: "生成 changelog", "项目结构地图", "写技术文档"
- [x] 1.3 Confirm Step numbering runs 0–7 (not 0–5 as in v1.0)
- [x] 1.4 Confirm Step 5 (CHANGELOG) is present with Git history bash commands, commit classification table, SemVer strategy table, and Keep-a-Changelog output template
- [x] 1.5 Confirm Step 6 (docs/) is present with both 6a (project-map.md) and 6b (architecture.md) subsections
- [x] 1.6 Confirm Step 7 (report) references all five output files

## 2. Verify CHANGELOG Generation Spec Coverage

- [x] 2.1 Confirm Step 5 handles repos with tags (fetch from last tag to HEAD)
- [x] 2.2 Confirm Step 5 handles repos without tags (full history, suggest v0.1.0)
- [x] 2.3 Confirm commit classification table covers all 10 types from changelog-gen (feat, fix, docs, refactor, perf, test, chore, breaking, security, deps)
- [x] 2.4 Confirm non-conforming commits are placed in a fallback "其他变更" section (not silently dropped)
- [x] 2.5 Confirm breaking changes appear first in the version block
- [x] 2.6 Confirm empty sections are omitted from output
- [x] 2.7 Confirm existing CHANGELOG.md is prepended, not overwritten (Edit guardrail)

## 3. Verify Project Structure Map Spec Coverage

- [x] 3.1 Confirm Step 6a outputs to `docs/project-map.md`
- [x] 3.2 Confirm template includes ASCII tree, module table, and "💡 入口建议" section
- [x] 3.3 Confirm excluded directories list covers node_modules, .git, vendor, __pycache__, dist, build, .next
- [x] 3.4 Confirm monorepo handling is mentioned (separate trees per package)
- [x] 3.5 Confirm max depth of 3 is stated

## 4. Verify Architecture Doc Spec Coverage

- [x] 4.1 Confirm Step 6b outputs to `docs/architecture.md`
- [x] 4.2 Confirm template includes a `mermaid` graph TD block
- [x] 4.3 Confirm data-flow section is included in the template
- [x] 4.4 Confirm core module table is included
- [x] 4.5 Confirm FAQ section is included
- [x] 4.6 Confirm "TODO: verify" instruction for uncertain inferences — FIXED: added to Step 6b system-overview prompt

## 5. Verify README Quality Upgrade

- [x] 5.1 Confirm Step 4 includes the "首屏 30 秒价值判断" rule (value prop + audience + shortest install)
- [x] 5.2 Confirm the README template uses Chinese section headings with emoji (✨, 📦, 🚀, etc.)
- [x] 5.3 Confirm the self-check checklist (6 items) is present in Step 4
- [x] 5.4 Confirm the rule prohibiting filler words ("强大", "优雅", "现代化") is stated
- [x] 5.5 Confirm "Edit over Write" rule is present for existing README files

## 6. Verify Guardrails Completeness

- [x] 6.1 Confirm all 8 guardrails are present in the Guardrails section
- [x] 6.2 Confirm "Edit 优先于 Write" guardrail covers both README and CHANGELOG
- [x] 6.3 Confirm "空分类省略" guardrail is present
- [x] 6.4 Confirm "中文为主" guardrail is present and correctly scoped (human-facing docs only, not AGENTS.md)
- [x] 6.5 Confirm "内容可溯源" guardrail is preserved from v1.0 and extended to all five files — FIXED: updated "两个文件" → "所有五个文档文件"
- [x] 6.6 Confirm "仅限文档范围" (documentation-only scope) guardrail explicitly lists all five output files

## 7. Backward Compatibility Check

- [x] 7.1 Confirm all original v1.0 trigger phrases are preserved in the description field
- [x] 7.2 Confirm AGENTS.md generation logic (Steps 0–3) is functionally unchanged from v1.0
- [x] 7.3 Confirm the init command detection bash snippets are present and unmodified
- [x] 7.4 Confirm "Init command takes precedence" guardrail is preserved
