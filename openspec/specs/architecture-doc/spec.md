# Spec: architecture-doc

## Purpose

Generate `docs/architecture.md` containing a system overview, a Mermaid `graph TD` diagram, a data-flow description, a core module table, and a FAQ section.

## Requirements

### Requirement: Generate architecture document with Mermaid diagram
The skill SHALL produce `docs/architecture.md` containing a system overview, a Mermaid `graph TD` diagram, a data-flow description, a core module table, and a FAQ section.

#### Scenario: Mermaid diagram reflects inferred component relationships
- **WHEN** writing `docs/architecture.md`
- **THEN** the skill SHALL include a `mermaid` code block containing a `graph TD` diagram that represents the major components and their data/control flow as inferred from the file structure and imports

#### Scenario: Uncertain inferences are marked TODO
- **WHEN** the skill cannot confidently infer an architectural relationship from the codebase
- **THEN** it SHALL write `<!-- TODO: verify -->` at that point rather than fabricating content

#### Scenario: Core module table is included
- **WHEN** writing `docs/architecture.md`
- **THEN** the skill SHALL include a table with columns: module name, Chinese responsibility description, key interface or entry point

#### Scenario: FAQ section included
- **WHEN** writing `docs/architecture.md`
- **THEN** the skill SHALL include at least two Q&A entries derived from common questions implied by the project's domain and structure

#### Scenario: docs/ directory is created if absent
- **WHEN** the project root does not contain a `docs/` directory
- **THEN** the skill SHALL create it before writing `docs/architecture.md`

#### Scenario: Existing architecture doc is preserved with Edit
- **WHEN** `docs/architecture.md` already exists with substantial content
- **THEN** the skill SHALL use the Edit tool to update stale sections rather than overwriting the entire file
