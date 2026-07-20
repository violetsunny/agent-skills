# Spec: changelog-generation

## Purpose

Generate a `CHANGELOG.md` at the project root from Git commit history, following Keep a Changelog format and Semantic Versioning.

## Requirements

### Requirement: Generate CHANGELOG from Git history
The skill SHALL read Git commit history and produce a `CHANGELOG.md` at the project root following Keep a Changelog format and Semantic Versioning.

#### Scenario: Repo has tags — generate from last tag to HEAD
- **WHEN** the project repository has one or more Git tags
- **THEN** the skill SHALL fetch commits from the most recent tag to HEAD and write them into a new version block

#### Scenario: Repo has no tags — generate from full history
- **WHEN** the project repository has no Git tags
- **THEN** the skill SHALL fetch up to 100 recent commits and place them under an `[Unreleased]` block, suggesting `v0.1.0` as the initial version

#### Scenario: Classify commits by Conventional Commits type
- **WHEN** a commit message starts with a recognised type prefix (`feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`, `deps`)
- **THEN** the skill SHALL place the commit under the corresponding named section (e.g. ✨ 新功能, 🐛 Bug 修复)

#### Scenario: Non-conforming commits placed in fallback section
- **WHEN** a commit message does not match Conventional Commits format
- **THEN** the skill SHALL place it under a "🔧 其他变更" section rather than discarding it

#### Scenario: Breaking changes appear first
- **WHEN** any commit contains `BREAKING CHANGE:` in the footer or uses `!` after the type (e.g. `feat!:`)
- **THEN** the skill SHALL place those entries in a `⚠️ Breaking Changes` section at the top of the version block

#### Scenario: Empty sections are omitted
- **WHEN** a CHANGELOG section has no entries (e.g. no security fixes in this release)
- **THEN** the skill SHALL omit that section header entirely from the output

#### Scenario: Existing CHANGELOG is preserved
- **WHEN** `CHANGELOG.md` already exists at the project root
- **THEN** the skill SHALL prepend the new version block at the top, leaving all prior content intact

#### Scenario: SemVer version suggestion
- **WHEN** the skill determines the type of changes in the current batch
- **THEN** it SHALL suggest a new version number: major bump for breaking changes, minor for feat, patch for fix/docs/chore
