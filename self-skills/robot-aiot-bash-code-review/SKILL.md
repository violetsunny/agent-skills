---
name: robot-aiot-bash-code-review
description: >
  Review bash code blocks in skill documentation (.md) files for syntax, functional
  correctness, and pattern matching accuracy. Use when creating or updating skills that
  contain bash code blocks, when the user asks to verify/review/validate bash code in
  docs, or after any skill doc edit that touches bash blocks. Triggers on: "review bash",
  "verify code blocks", "check bash", "bash 验证", "代码块审查", "code review skill docs".
---

# Bash Code Review for Skill Documentation

Systematically verify bash code blocks in `.md` skill files. Three layers: syntax → functional → pattern accuracy. Pattern accuracy is the most critical layer — visually identical strings (e.g., 6 g's vs 7 g's) cause complete exclusion failure.

## Review Process

### Step 1: Extract and syntax-check

Extract all `bash` fenced blocks, run `bash -n` on each:

```bash
FILE="<path-to-skill.md>"
awk '/^```bash/{flag=1; n++; next} /^```/{if(flag){flag=0}} flag{print > ("/tmp/block_" n ".sh")}' "$FILE"
for f in /tmp/block_*.sh; do
  [ -f "$f" ] || continue
  num=$(basename "$f" .sh | sed 's/block_//')
  bash -n "$f" 2>&1 && echo "块$num: OK" || echo "块$num: FAIL"
done
```

All blocks must pass `bash -n` before proceeding. `bash -n` catches syntax only — it does not verify behavior.

### Step 2: Functional verification

For each block that performs real operations (not just inline documentation examples):

1. Create a temp directory with representative test data
2. Run the block against test data
3. Verify **both** positive cases (should match/succeed) and negative cases (should exclude/fail)
4. Check output content, not just exit codes

Skip functional verification for blocks that are purely illustrative (e.g., showing a command format without actual execution).

### Step 3: Pattern matching verification

This is the critical step. Patterns used for inclusion/exclusion (`grep`, `find -path`, `case`) must be verified against **actual filesystem paths**, not assumed-correct strings.

#### 3a. Get actual name programmatically

```bash
actual=$(ls -d /path/to/prefix*suffix 2>/dev/null | head -1)
dirname=$(basename "$actual")
echo "name: [$dirname]"
echo "char count: ${#dirname}"
echo "char breakdown: $(echo "$dirname" | fold -w1 | tr '\n' ' ')"
```

Never count characters visually. Terminal fonts cannot reliably distinguish repeated characters.

#### 3b. Test pattern against actual path

```bash
test_path="$actual/sub/.git/objects/pack/tmp_pack_test"
echo "$test_path" | grep "/$dirname/"    # must match (rc=0)
echo "$test_path" | grep "/wrongname/"   # must not match (rc=1)
```

#### 3c. Test exclusion patterns

```bash
printf '%s\n' "$protected_path" "$normal_path" | grep -v "/$dirname/"
# Output must contain ONLY $normal_path
```

If the protected path appears in output, the exclusion pattern is broken.

#### 3d. Precise pattern counting in files

Use perl with lookbehind/lookahead to count exact pattern occurrences without substring false positives:

```bash
perl -ne 'while(/(?<!g)PATTERN(?!g)/g){$c++} END{print $c//0}' "$file"
```

`grep -o` uses greedy matching and can mask discrepancies (e.g., matching 7-char string when searching for 6-char pattern, because 6-char is a substring of 7-char).

### Step 4: maxdepth verification

For `find -maxdepth N` commands, verify N covers the deepest nested path:

```bash
for d in 3 4 5 6; do
  count=$(find /path -maxdepth $d -mindepth 1 -type d -name ".git" 2>/dev/null | wc -l | tr -d ' ')
  echo "maxdepth $d: $count"
done
```

If count increases between depths, the shallower depth is missing items. Set maxdepth to the first depth where count stabilizes.

## Verification Checklist

For each bash code block:

- [ ] `bash -n` syntax check passes
- [ ] Functional test with representative data (if block is executable, not illustrative)
- [ ] Positive case verified (pattern matches what it should)
- [ ] Negative case verified (pattern excludes what it should)
- [ ] All directory/file name patterns verified programmatically (character count + exact match)
- [ ] `grep -v` slash-anchored patterns tested against actual paths
- [ ] `find -maxdepth` verified to cover deepest nested path
- [ ] `find -maxdepth 1` paired with `-mindepth 1` (depth 0 is the search root itself)
- [ ] Guard case-sensitivity matches lookup case-sensitivity (`case` vs `find -iname`)
- [ ] Protection/skip list checked against **both** source name and matched target name
- [ ] `rsync` between potential git repos carries `--exclude '.git/'`
- [ ] `rsync` difference counting does **not** use `--ignore-times`
- [ ] Silently-skipped operations (`rsync -u`) explicitly detected and reported
- [ ] No `else` default to success/OK in classification logic
- [ ] Exit code checked before reporting success (`rc≠0` → `[FAIL]` with output)
- [ ] Parallelism capped at 4 for `xargs -P`
- [ ] Success判断 based on output content, not exit code
- [ ] `continue`-chained dispatch branches tested against real multi-match items (mutual exclusivity silently drops content)
- [ ] Prose name lists match code blocks, and both match actual filesystem names
- [ ] Prose-stated exclusion rules applied to **every** rsync/copy call, not just some branches

## Key Rules

1. **Never verify name patterns visually.** Always use `tr -cd 'X' | wc -c` or `fold -w1` to count characters. 6 g's and 7 g's look identical in terminal.

2. **Slash-anchored patterns require exact match.** `grep "/name/"` does NOT substring-match across slash boundaries. `/ggggggood/` (6g) does not match `/gggggggood/` (7g) even though `ggggggood` is a substring of `gggggggood`.

3. **Test exclusion with both protected and normal paths.** A pattern that "works" on normal paths may silently fail to exclude protected paths.

4. **Guard and lookup must agree on case sensitivity.** A `case`-based skip list is case-sensitive; `find -iname` is not. Mixed-case names bypass the guard yet still resolve to the protected target. Normalize both sides to lowercase and check the matched target name too.

5. **`rsync` needs `--exclude '.git/'`** whenever source and target may be independent clones. Without it the target's `.git/HEAD` and refs get overwritten, destroying repo identity.

6. **No else-default to OK.** Unrecognized output must be `[UNKNOWN]`, not `[OK]`. Check `rc` first so partial failures are never reported as success.

7. **Judge by output, not exit code.** `xargs -P >4` causes bash job table race conditions. Exit codes become unreliable.

8. **Silent skips must be surfaced.** `rsync -u` produces no output for skipped files. Detect them with a two-pass dry run (`-rtn -i` minus `-rtun -i`, without `--ignore-times`) and report the count.

9. **Verify maxdepth empirically.** Don't assume depth — count at increasing depths until stable.

10. **`continue`-chained branches are mutually exclusive — verify multi-match items.** An item matching several `if ... continue` branches only gets the first branch's handling; content unique to later branches is silently dropped. Enumerate real-world structure combinations and check what each branch actually reaches.

11. **Prose and code must agree with the filesystem.** A name list in prose can diverge from the same list in code (`vercel-skills` vs `vercel-agent-skills`), and a prose exclusion rule can be applied to only some rsync calls. Diff prose lists against code lists, and verify both against `ls`; check every rsync/copy call carries the full stated exclusion set.

## Pitfalls Reference

For detailed pitfall descriptions with reproduction commands and root cause analysis, read `references/pitfalls.md`.

## Output Format

Report findings as:

```
块N: [OK|FAIL] - description
  问题: (if FAIL) specific issue
  修复: (if FAIL) recommended fix
```

Summary:

```
总块数: N
语法通过: N/N
功能验证: N passed, N failed
模式验证: N passed, N failed
```
