# Bash Code Review Pitfalls

Detailed pitfall descriptions with reproduction commands and root cause analysis. Each pitfall was discovered during actual skill documentation review.

## Pitfall 1: Slash-anchored substring matching failure

### Symptom

`grep -v "/pattern/"` fails to exclude paths that contain the pattern as a substring, when the actual directory name has more characters than the pattern.

### Root cause

Slash anchoring prevents cross-boundary substring matching. The slash before the pattern in `/pattern/` must align with a slash in the target path. If the actual name is longer, the character before the substring match is not a slash.

### Reproduction

```bash
# Actual directory: gggggggood (7 g's, 10 chars)
# Pattern in docs: gggggood (6 g's, 9 chars)

actual="/path/to/gggggggood/sub/file"

# Bare substring match WORKS (6g is substring of 7g):
echo "gggggggood" | grep "ggggggood"  # rc=0, matches

# Slash-anchored match FAILS:
echo "$actual" | grep "/ggggggood/"   # rc=1, NO match
echo "$actual" | grep "/gggggggood/"  # rc=0, matches

# Why: in /gggggggood/, the 6g substring ggggggood starts at position 1
# (after the first g). The character before it is 'g', not '/'.
# So /ggggggood/ cannot align with /gggggggood/.
```

### Impact

Protection directory exclusion silently fails. `grep -v "/ggggggood/"` does not filter out `/gggggggood/` paths. Files in the protection directory get deleted.

### Fix

Verify the exact character count of directory names programmatically. Use the correct name in all patterns.

```bash
dirname=$(basename "$(ls -d /path/to/ggg*ood | head -1)")
echo "g count: $(echo "$dirname" | tr -cd 'g' | wc -c)"
# Must be 7, not 6
```

### Affected patterns

| Pattern type | 6g (wrong) | 7g (correct) | Works? |
|---|---|---|---|
| `grep -v "/name/"` | `/ggggggood/` | `/gggggggood/` | 6g: NO, 7g: YES |
| `find -path "*/name/*"` | `*/ggggggood/*` | `*/gggggggood/*` | 6g: NO, 7g: YES |
| `find -path "*name*"` | `*ggggggood*` | `*gggggggood*` | Both YES (substring) |
| `case */name/*)` | `*/ggggggood/*` | `*/gggggggood/*` | 6g: NO, 7g: YES |
| `grep -v "name"` | `ggggggood` | `gggggggood` | Both YES (substring) |

Key insight: patterns WITHOUT slash anchors work via substring matching. Patterns WITH slash anchors require exact name match.

## Pitfall 2: Visual character counting failure

### Symptom

Directory name patterns in documentation have wrong character counts (e.g., 6 g's instead of 7), but the error is not caught during review because the names look identical in terminal output.

### Root cause

Terminal fonts render repeated characters at fixed width. `ggggggood` (6g) and `gggggggood` (7g) are visually indistinguishable in most monospace fonts. Human reviewers cannot reliably count repeated characters by sight.

### Reproduction

```bash
# These two strings look identical in terminal:
echo "ggggggood"   # 6 g's, 9 chars
echo "gggggggood"  # 7 g's, 10 chars

# Programmatic verification:
echo "ggggggood" | tr -cd 'g' | wc -c   # 6
echo "gggggggood" | tr -cd 'g' | wc -c  # 7

# Character breakdown:
echo "ggggggood" | fold -w1 | tr '\n' ' '   # g g g g g g o o d
echo "gggggggood" | fold -w1 | tr '\n' ' '  # g g g g g g g o o d
```

### Impact

All pattern matching mechanisms (grep, find, case) fail silently when the pattern name has wrong character count. The failure is not obvious because the names look the same.

### Fix

Always verify character counts programmatically. Never trust visual inspection for names with repeated characters.

```bash
# Before using a directory name in a pattern:
actual=$(basename "$(ls -d /path/to/prefix*suffix | head -1)")
echo "name: [$actual]"
echo "length: ${#actual}"
echo "char count: $(echo "$actual" | tr -cd 'g' | wc -c)"
```

## Pitfall 3: find -maxdepth too shallow

### Symptom

`find -maxdepth 3` misses nested repositories at depth 4-5. Scan reports fewer repos than actually exist.

### Root cause

`-maxdepth N` limits search to N levels below the starting path. Nested repos in subdirectories (e.g., `group/subgroup/repo/.git`) require deeper maxdepth.

### Reproduction

```bash
# Path structure:
# self/<group>/<repo>/.git                    = depth 3
# self/<group>/<subgroup>/<repo>/.git         = depth 4
# self/<group>/<subgroup>/<subsub>/<repo>/.git = depth 5

for d in 3 4 5 6; do
  count=$(find /path/to/self -maxdepth $d -mindepth 1 -type d -name ".git" 2>/dev/null | wc -l | tr -d ' ')
  echo "maxdepth $d: $count"
done

# Output:
# maxdepth 3: 86    ← missing 17 repos
# maxdepth 4: 100   ← missing 3 repos
# maxdepth 5: 103   ← all found
# maxdepth 6: 103   ← no more
```

### Impact

17 repos not scanned, not pulled, not reported. Silent data loss in sync operations.

### Fix

Set maxdepth to the first depth where count stabilizes. Verify empirically, don't assume.

```bash
# Find the stabilization depth:
prev=0
for d in $(seq 1 8); do
  count=$(find /path -maxdepth $d -mindepth 1 -type d -name ".git" 2>/dev/null | wc -l | tr -d ' ')
  echo "maxdepth $d: $count"
  [ "$count" = "$prev" ] && { echo "stabilized at depth $((d-1))"; break; }
  prev=$count
done
```

## Pitfall 4: grep -o greedy matching masks discrepancies

### Symptom

`grep -o "gggggg*ood"` reports counts that don't match the actual number of 6g vs 7g patterns in a file.

### Root cause

`grep -o` finds the longest match at each position. In `gggggggood` (7g), the pattern `gggggg*ood` matches the full 7g string, not the 6g substring. This makes it impossible to count standalone 6g occurrences when 7g strings are also present.

### Reproduction

```bash
# File contains both 6g and 7g patterns
echo "ggggggood gggggggood" | grep -o "gggggg*ood"
# Output: gggggggood gggggggood
# Both matched as 7g! The 6g was consumed as part of the longer match.

# Precise counting with perl lookbehind/lookahead:
echo "ggggggood gggggggood" | perl -ne 'while(/(?<!g)ggggggood(?!g)/g){$c++} END{print "6g: ", $c//0, "\n"}'
# Output: 6g: 1  (only the standalone 6g, not the one inside 7g)

echo "ggggggood gggggggood" | perl -ne 'while(/(?<!g)gggggggood(?!g)/g){$c++} END{print "7g: ", $c//0, "\n"}'
# Output: 7g: 1
```

### Fix

Use perl with negative lookbehind `(?<!g)` and lookahead `(?!g)` for precise pattern counting:

```bash
# Count standalone 6g patterns (not part of 7g):
perl -ne 'while(/(?<!g)ggggggood(?!g)/g){$c++} END{print $c//0}' "$file"

# Count standalone 7g patterns:
perl -ne 'while(/(?<!g)gggggggood(?!g)/g){$c++} END{print $c//0}' "$file"
```

The lookbehind `(?<!g)` ensures the pattern is not preceded by `g` (which would make it part of a longer g-sequence). The lookahead `(?!g)` ensures it's not followed by `g`.

## Pitfall 5: else-default to OK in classification logic

### Symptom

Output classification logic uses `else` to default to `[OK]`, masking unrecognized output patterns that indicate partial or failed operations.

### Root cause

`else` catches all unmatched cases and labels them as success. This is wrong because unrecognized output may indicate a real problem that needs human review.

### Reproduction

```bash
# git pull output: "* [new tag] v2.16.0 -> v2.16.0"
# This is NOT a successful pull — only tags were fetched, main branch didn't move.

output="* [new tag] v2.16.0 -> v2.16.0"
case "$output" in
  *"Already up to date"*|*"Fast-forward"*|*"files changed"*) echo "[OK]" ;;
  *"could not read Username"*|*"Authentication failed"*) echo "[AUTH]" ;;
  *"fatal:"*|*"error:"*) echo "[FAIL]" ;;
  *) echo "[OK]" ;;  # ← BUG: else-default to OK
esac
# Output: [OK]  ← WRONG! Should be [UNKNOWN]

# Correct:
case "$output" in
  *"Already up to date"*|*"Fast-forward"*|*"files changed"*) echo "[OK]" ;;
  *"could not read Username"*|*"Authentication failed"*) echo "[AUTH]" ;;
  *"fatal:"*|*"error:"*) echo "[FAIL]" ;;
  *) echo "[UNKNOWN]" ;;  # ← Requires human review
esac
```

### Impact

Repo was 102 commits behind after "successful" pull. The fetch only updated tag references; the main branch didn't fast-forward. Else-default masked this as success.

### Fix

Never use `else` to default to success. Unrecognized output → `[UNKNOWN]` → human review. Add a secondary behind-check after every pull round:

```bash
while read -r dir; do
  sb=$(git -C "$dir" status -sb 2>/dev/null | head -1)
  case "$sb" in *"[behind"*) echo "[BEHIND] $dir → $sb" ;; esac
done < /tmp/pull_list.txt
```

## Pitfall 6: Exit code unreliability with high parallelism

### Symptom

`xargs -P 8` reports non-zero exit codes for operations that actually succeeded. 30 repos with `Already up to date.` output were marked as FAIL.

### Root cause

Bash job table race condition at parallelism > 4. The shell's internal job tracking becomes unreliable, causing exit codes to be misattributed between concurrent processes.

### Reproduction

```bash
# Simulate: 8 parallel git pulls, some succeed
# With -P 8, exit codes become unreliable
# With -P 4, exit codes are correct

# Verification: compare exit code vs output content
echo "Already up to date." | grep -q "Already up to date" && echo "output says OK"
# But rc from xargs -P 8 might be non-zero
```

### Fix

1. Cap parallelism at 4: `xargs -P 4`
2. Judge success by output content, not exit code
3. Use a classification table:

| Output contains | Judgment |
|---|---|
| `Already up to date` / `Fast-forward` / `files changed` | `[OK]` |
| `could not read Username` / `Authentication failed` | `[AUTH]` |
| `fatal:` / `error:` | `[FAIL]` |
| Empty (killed by alarm) | `[TIMEOUT]` |
| Only `* [new tag]` / `* [new branch]` | `[UNKNOWN]` |

## Pitfall 7: perl alarm with exec (timeout doesn't work)

### Symptom

`perl -e 'alarm shift; exec @ARGV'` does not enforce timeout. The command runs to completion regardless of alarm value.

### Root cause

`exec` replaces the perl process with the target command. The alarm signal handler is lost when perl is replaced. The target command (e.g., git) has its own timeout (75s) which fires first.

### Reproduction

```bash
# This does NOT timeout after 5 seconds:
perl -e 'alarm 5; exec "sleep", "10"'
# sleep runs for full 10 seconds

# This DOES timeout after 5 seconds:
perl -e '
  my $t = shift;
  my $pid = fork();
  if ($pid == 0) { setpgrp(0, 0); exec @ARGV; exit 127; }
  local $SIG{ALRM} = sub { kill 9, -$pid; exit 124; };
  alarm $t;
  waitpid($pid, 0);
  my $rc = $? >> 8;
  alarm 0;
  exit $rc;
' 5 sleep 10
# Exits with rc=124 after 5 seconds
```

### Fix

Use fork + parent-held alarm. Child calls `setpgrp(0,0)` before `exec` to become process group leader, so `kill 9, -$pid` kills the entire group (including git's subprocesses like `git-remote-https` and `index-pack`).

```bash
perl -e '
  my $t = shift;
  my $pid = fork();
  if ($pid == 0) { setpgrp(0, 0); exec @ARGV; exit 127; }
  local $SIG{ALRM} = sub { kill 9, -$pid; exit 124; };
  alarm $t;
  waitpid($pid, 0);
  my $rc = $? >> 8;
  alarm 0;
  exit $rc;
' "$TIMEOUT" "$GIT" -C "$dir" pull --ff-only
```

## Pitfall 8: tmp_pack residue after kill -9

### Symptom

After timeout-killing git with `kill -9`, subsequent `git fetch`/`pull` fails with `fatal: protocol error: bad pack header`.

### Root cause

`kill -9` (SIGKILL) cannot be caught. Git has no opportunity to clean up temporary pack files in `.git/objects/pack/tmp_pack_*`. These half-written files corrupt subsequent pack operations.

### Reproduction

```bash
# After a timeout kill:
find /path/to/repo/.git/objects/pack/ -name "tmp_pack_*" -ls
# Shows残留 files, potentially hundreds of MB

# Subsequent fetch fails:
git -C /path/to/repo fetch
# fatal: protocol error: bad pack header
```

### Impact

28 repos × 2 rounds of timeout = 18 residual files, 754MB total. All subsequent fetches to these repos fail with `bad pack header`, misdiagnosed as object store corruption.

### Fix

After every pull round, scan and clean tmp_pack residue:

```bash
find /path -maxdepth 7 -type f -name "tmp_pack_*" 2>/dev/null \
  | grep -v "/protected_dir/" \
  | while read -r f; do rm -f "$f"; done
```

Before cleaning, verify repo integrity:
1. `git fsck --full --strict` rc=0, no `missing`/`broken`/`corrupt`
2. `git verify-pack -v <main_pack>.idx` ends with `ok`
3. `git log -1 --oneline` outputs normally

tmp_pack files are not referenced by any `.idx` — deleting them does not damage the repo.

## Pitfall 9: Case-sensitive skip list vs case-insensitive lookup

### Symptom

A protection/skip list fails to block items whose names differ only in case. Protected directories get overwritten despite being explicitly listed.

### Root cause

`case` in bash matches case-sensitively, while `find -iname` matches case-insensitively. When a skip list is checked with `case` but the target is located with `find -iname`, mixed-case names slip past the guard and still resolve to the protected target.

### Reproduction

```bash
SKIP="openspec stock-replay-workbench"
pn="OpenSpec"   # real source dir name, mixed case

# case-sensitive guard does NOT block:
case "$pn" in
  docs|scripts|tests|openspec|stock-replay-workbench) echo "blocked" ;;
  *) echo "NOT blocked" ;;
esac
# Output: NOT blocked

# but case-insensitive lookup DOES find the protected target:
find "$target_base" -maxdepth 1 -type d -iname "$pn"
# Output: /path/target/openspec   ← protected dir located

# Result: rsync overwrites the protected directory.
```

### Impact

Confirmed on real data: source `self/skills/OpenSpec` bypassed the `openspec` skip entry and resolved to target `free-stock-line-skills/openspec` — an independent git repo with 15056 files. The `stock-replay-workbench` key-protection entry is bypassed the same way by `Stock-Replay-Workbench`.

### Fix

Normalize both sides to lowercase before comparing against the skip list, and check the **matched target name** as well as the source name:

```bash
SKIP_LIST="docs scripts tests openspec stock-replay-workbench"

pn_lower=$(printf '%s' "$project_name" | tr '[:upper:]' '[:lower:]')
case " $SKIP_LIST " in
  *" $pn_lower "*) echo "[SKIP-PROTECTED] $project_name"; continue ;;
esac

match=$(find "$target_base" -mindepth 1 -maxdepth 1 -type d -iname "$project_name" | head -1)

mn_lower=$(printf '%s' "$(basename "$match")" | tr '[:upper:]' '[:lower:]')
case " $SKIP_LIST " in
  *" $mn_lower "*) echo "[SKIP-PROTECTED] target $(basename "$match")"; continue ;;
esac
```

The `" $SKIP_LIST "` / `*" $item "*` wrapping prevents partial-name false positives (e.g. `spec` matching inside `openspec`).

Rule: **any guard expressed with `case`/`=` must use the same case sensitivity as the lookup that follows it.** If lookup is `-iname`, the guard must be case-insensitive too.

## Pitfall 10: rsync without --exclude '.git/' destroys target repo identity

### Symptom

After syncing between two directories that are both independent git clones of the same upstream, the target repo's HEAD/refs no longer match its own history. Subsequent `git pull` on the target fails or reports a corrupted state.

### Root cause

`rsync -rtu src/ dst/` with no `--exclude` copies `.git/` along with the working tree. The source's `.git/HEAD`, refs, and objects overwrite the target's, replacing the target repo's identity with the source's.

### Reproduction

```bash
mkdir -p src/p/.git target/p/.git
echo "SRC-GIT" > src/p/.git/HEAD
echo "TGT-GIT" > target/p/.git/HEAD
touch -t 202609010000 src/p/.git/HEAD   # source newer
touch -t 202601010000 target/p/.git/HEAD

rsync -rtu src/p/ target/p/
cat target/p/.git/HEAD
# Output: SRC-GIT   ← target repo identity destroyed

# With exclusion:
rsync -rtu --exclude '.git/' src/p/ target/p/
cat target/p/.git/HEAD
# Output: TGT-GIT   ← preserved
```

### Impact

8 target directories were independent git clones pulled by a separate module. Overwriting their `.git/` breaks that module's pulls and can freeze the clones in a dirty state permanently.

### Fix

Always add `--exclude '.git/'` when syncing between directories that may be independent repos:

```bash
rsync -rtu --exclude '.git/' "$src/" "$dst/"
```

Verify before syncing by listing which targets are repos:

```bash
for d in "$target_base"/*/; do
  [ -d "$d/.git" ] && echo "repo: $(basename "$d")"
done
```

## Pitfall 11: rsync --ignore-times inflates difference counts

### Symptom

A pre-flight count of "files that differ" includes files that are byte-identical and have matching mtimes on both sides. Derived metrics (e.g. "how many files will be skipped") come out too high.

### Root cause

`--ignore-times` tells rsync to disregard the mtime+size quick check and consider every file a transfer candidate. In a dry run it therefore lists all files, not just differing ones.

### Reproduction

```bash
# Setup: a.txt newer on target, b.txt newer on source, same.txt identical both sides
rsync -rtn -i --ignore-times src/p/ target/p/ | grep -c '^[<>ch.]'   # 3  ← includes same.txt
rsync -rtn -i              src/p/ target/p/ | grep -c '^[<>ch.]'    # 2  ← correct
rsync -rtun -i             src/p/ target/p/ | grep -c '^[<>ch.]'    # 1  ← will actually send

# With --ignore-times:  newer_target = 3 - 1 = 2   WRONG
# Without:              newer_target = 2 - 1 = 1   CORRECT
```

### Fix

For difference counting, omit `--ignore-times`:

```bash
all_diff=$(rsync -rtn  -i --exclude '.git/' "$src/" "$dst/" 2>/dev/null | grep -c '^[<>ch.]')
will_send=$(rsync -rtun -i --exclude '.git/' "$src/" "$dst/" 2>/dev/null | grep -c '^[<>ch.]')
skipped=$((all_diff - will_send))
```

Itemize first characters: `<` send, `>` receive, `c` create/local-change, `h` hardlink, `.` no-change. `^[<>ch.]` covers all of them.

## Pitfall 12: rsync -u skips silently, breaking [NEWER-TARGET] reporting

### Symptom

Documentation promises that files skipped because the target is newer will be reported with a marker. Actual runs report nothing — the sync appears to have transferred everything or nothing, with no indication that target-side content was preserved.

### Root cause

`rsync -rtu` produces no output for files skipped by `-u`. Without `-i`/`-v` there is nothing to parse, so the script cannot distinguish "nothing to do" from "skipped N newer target files".

### Reproduction

```bash
# target file newer than source
out=$(rsync -rtu src/p/ target/p/ 2>&1)
echo "[$out]"
# Output: []   ← empty, no way to know a file was skipped

cat target/p/a.txt
# Output: T-NEW   ← silently preserved
```

### Fix

Detect skipped files with a two-pass dry run before the real sync (see Pitfall 11 for the counting method), then report explicitly:

```bash
if [ "$rc" -ne 0 ]; then
  echo "[FAIL] $name rc=$rc: $out"
elif [ "$will_send" -eq 0 ] && [ "$newer_target" -eq 0 ]; then
  echo "[UPTODATE] $name"
elif [ "$newer_target" -gt 0 ]; then
  echo "[SYNC+NEWER-TARGET] $name synced=$will_send skipped=$newer_target"
else
  echo "[SYNC] $name synced=$will_send"
fi
```

Note the ordering: `rc` is checked first, so a partial failure is never reported as success. This is the same principle as Pitfall 5 — no default-to-OK.

### Triggering a real failure for testing

`chmod 500` on the target is often insufficient — rsync may still succeed. Use an unreadable source subdirectory to force rc=23:

```bash
chmod 000 "$src/proj/sub"
rsync -rtu "$src/proj/" "$target/proj/"; echo "rc=$?"   # rc=23
chmod 755 "$src/proj/sub"   # restore before rm -rf, or cleanup fails
```
