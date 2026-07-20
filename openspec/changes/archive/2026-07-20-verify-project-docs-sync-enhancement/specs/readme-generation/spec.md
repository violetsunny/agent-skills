## MODIFIED Requirements

### Requirement: README satisfies 30-second value judgment
The skill SHALL generate or update `README.md` such that a first-time visitor can determine within 30 seconds what the project does, who it is for, and how to install it. The README MUST contain: (1) a one-sentence value proposition as the opening line, (2) an explicit statement of the target audience or use case, and (3) the shortest possible install command in a copyable code block.

#### Scenario: Value proposition is the first non-badge line
- **WHEN** creating or updating README.md
- **THEN** the first substantive text line (after the title and optional badges) SHALL be a one-sentence value proposition that names the problem solved, containing no filler adjectives such as "强大", "优雅", or "现代化"

#### Scenario: Install command is copyable
- **WHEN** writing the installation section
- **THEN** the install command SHALL appear in a fenced code block and SHALL be derived from an actual package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`) found in the repository

#### Scenario: Self-check checklist is applied before finalising
- **WHEN** the skill completes writing README.md
- **THEN** it SHALL verify all items in the self-check list: value proposition present, shortest runnable example present, installation/usage/contributing/license sections present, no AI-style marketing language, all commands are copy-pasteable

#### Scenario: Existing README updated with Edit, not Write
- **WHEN** `README.md` already exists at the project root with substantial content
- **THEN** the skill SHALL use the Edit tool to update only stale sections and SHALL NOT use the Write tool to replace the entire file

#### Scenario: Missing information marked TODO
- **WHEN** a required README section cannot be populated from the codebase
- **THEN** the skill SHALL write "待补充" at that location rather than inventing placeholder text
