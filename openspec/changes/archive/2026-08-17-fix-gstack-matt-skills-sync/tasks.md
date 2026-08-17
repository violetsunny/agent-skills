## 1. Fix matt-skills in Module 3

- [x] 1.1 Update `skills/robot-aiot-self-skill-sync/modules/module3-skill-sync.md` section 3.3 to change matt-skills from `[NPX-MANUAL]` to automatic `npx skills@latest add mattpocock/skills` execution with timeout and error handling
- [x] 1.2 Remove gstack section 3.7 from `module3-skill-sync.md` entirely

## 2. Add gstack to Module 4

- [x] 2.1 Update `skills/robot-aiot-self-skill-sync/modules/module4-knowledge-base.md` step 4.1A to add a third directory structure: `.agents/skills/` for gstack, with explicit full path `/Users/kangll13/aiot/java-code/self/skills/gstack/.agents/skills/`
- [x] 2.2 Update the 4.1A script to handle gstack's `.agents/skills/` structure: if `self/skills/gstack/.agents/skills/` exists, iterate its subdirectories and sync each to `agent-skills/skills/{skill_name}/`

## 3. Update Summary and Shared Docs

- [x] 3.1 Update `skills/robot-aiot-self-skill-sync/modules/summary.md` to change matt-skills status from `[NPX-MANUAL]` to `[NPX-AUTO]` / `[NPX-FAILED]`, and add gstack to knowledge base sync summary
- [x] 3.2 Update `skills/robot-aiot-self-skill-sync/modules/shared.md` if it references matt-skills as `[NPX-MANUAL]`

## 4. Sync and Validate

- [x] 4.1 Sync updated `robot-aiot-self-skill-sync` from project to `~/.agents/skills/`
- [x] 4.2 Verify both project and `.agents` copies are identical
