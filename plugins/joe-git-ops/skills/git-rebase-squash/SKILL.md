---
name: git-rebase-squash
description: Clean up git commit history by squashing/reorganizing commits using non-interactive rebase. Use when user asks to "tidy up commits", "squash commits", "clean up history", "rebase", or wants N specific commits total. This skill handles the mechanics of rebasing in non-interactive environments where `git rebase -i` won't work.
---

# Git Rebase & Squash (Non-Interactive)

Clean up git commit history by squashing and reorganizing commits using a file-based rebase workflow.

## Critical Constraints

**DO NOT** use `git rebase -i` directly—it requires interactive terminal input and will hang or fail in automated environments.

**ALWAYS** use `GIT_SEQUENCE_EDITOR` with a pre-written rebase plan file.

## Workflow

### 1. Commit All Changes First

If there are unstaged changes that are part of the cleanup:

```bash
# Commit them first - DO NOT stash
git add <files>
git commit -m "Description of changes"
```

**Why**: Stashing complicates the rebase process. Committing allows you to include these changes in the rebase plan.

### 2. Identify Commits to Rebase

```bash
# Fetch latest remote state
git fetch origin

# Find the fork point — the commit where your branch diverged from origin/main
BASE=$(git merge-base origin/main HEAD)

# View all commits on your branch since the fork point, with size info
git log --oneline $BASE..HEAD
```

**Before proceeding, sanity-check the commit list. Confirm with the user if any of the following apply:**
- The branch is more than ~20 commits ahead of `origin/main` and no base was specified
- The commits look unrelated to what the user described (e.g. a mix of entirely different features), suggesting the wrong base was found
- Any commit in the list is a **merge commit** (`Merge branch ...`) — rebasing over a merge commit will likely produce unexpected results

When confirming, phrase it as a single question covering whichever flags triggered: *"Before I proceed — this branch is N commits ahead of `origin/main` [and/or includes a merge commit / includes unrelated commits]. Is `origin/main` the right base, or should I use a different one?"*

```bash
git log $BASE..HEAD --format="%h %s" | while read hash msg; do
  stats=$(git diff-tree --no-commit-id -r --stat $hash | tail -1)
  echo "$hash | $stats | $msg"
done
```

This gives you a per-commit breakdown of files changed and lines added/removed — essential for deciding how to group commits.

### 3. Present Squash Options

Before running the rebase, **present the user with 2–3 breakdown options** at different commit counts (e.g. into 3, 4, 5 commits). For each option show:
- The proposed commit groups with their combined size (files / LOC)
- A recommended option with a brief rationale (e.g. "4 commits keeps CI/CD infra separate from engine changes")

Example presentation format:

```
**Option A — 3 commits** ⭐ recommended
  1. Add CI/CD pipeline and deploy infrastructure  (12 files, +450/-80)
  2. Add OTEL telemetry and fix git identity       (4 files, +45/-12)
  3. Add HTTPRoute and HealthCheckPolicy           (4 files, +57/-3)

**Option B — 4 commits**
  1. Fix Helm chart security contexts              (3 files, +18/-6)
  2. Add CI/CD pipeline and deploy scripts         (9 files, +432/-74)
  3. Add OTEL telemetry and fix git identity       (4 files, +45/-12)
  4. Add HTTPRoute and HealthCheckPolicy           (4 files, +57/-3)

**Option C — 5 commits**
  1. Fix Helm chart security contexts              (3 files, +18/-6)
  2. Add CI/CD pipeline and deploy scripts         (9 files, +432/-74)
  3. Add OTEL telemetry config                     (3 files, +39/-8)
  4. Fix git identity in push_branch               (1 file,  +6/-4)
  5. Add HTTPRoute and HealthCheckPolicy           (4 files, +57/-3)
```

Wait for user to confirm before proceeding.

### 4. Create Rebase Plan File

Create a file with the rebase instructions:

```bash
cat << 'EOF' > /tmp/git-rebase-todo
pick <commit-hash-1> <commit message>
fixup <commit-hash-2> <commit message>  # squash into previous, discard message
fixup <commit-hash-3> <commit message>  # squash into previous, discard message
pick <commit-hash-4> <commit message>
squash <commit-hash-5> <commit message> # squash into previous, keep message
EOF
```

**Key Commands**:
- `pick`: Keep this commit as-is
- `fixup`: Squash into previous commit, discard this commit's message
- `squash`: Squash into previous commit, keep this commit's message for editing
- `reword`: Keep commit but change the message
- `edit`: Stop at this commit to make changes
- `drop`: Remove this commit entirely

**Order**: Commits are listed from oldest to newest (chronological order)

### 5. Execute Rebase

```bash
# Use GIT_SEQUENCE_EDITOR to point to your plan file, rebase onto the fork point
GIT_SEQUENCE_EDITOR='cp /tmp/git-rebase-todo' git rebase -i $BASE
```

Where `$BASE` is the merge-base commit found in step 2.

### 6. Handle Interactive Steps

If you used `edit` or `reword` commands:

```bash
# For 'edit' - make changes, then:
git add <files>
git commit --amend
git rebase --continue

# For 'reword' - the rebase will stop and wait:
git commit --amend -m "New commit message"
git rebase --continue
```

### 7. Verify Result

```bash
# Check the new history
git log --oneline origin/main..HEAD

# Diff against the old HEAD — must be empty
git diff <old-HEAD> HEAD --stat

# If the diff is non-empty, the rebase dropped or altered content — abort and investigate
```

**Always diff against the old HEAD before pushing.** A non-empty diff means commits were dropped or conflicts were resolved incorrectly.

### 8. Force Push

Since rebase rewrites history:

```bash
# Use force-with-lease for safety (fails if remote has new commits)
git push --force-with-lease

# OR regular force push (less safe)
git push --force
```

## Common Mistakes to Avoid

### ❌ DON'T: Use `git rebase -i` directly
```bash
git rebase -i HEAD~5  # Will hang waiting for interactive input
```

### ✅ DO: Use GIT_SEQUENCE_EDITOR
```bash
BASE=$(git merge-base origin/main HEAD)
cat > /tmp/rebase-plan << 'EOF'
pick abc123
fixup def456
EOF
GIT_SEQUENCE_EDITOR='cp /tmp/rebase-plan' git rebase -i $BASE
```

---

### ❌ DON'T: Stash uncommitted changes
```bash
git stash
git rebase -i HEAD~5
git stash pop
```

### ✅ DO: Commit them first
```bash
git add .
git commit -m "WIP changes"
# Now rebase all branch commits including the new one
BASE=$(git merge-base origin/main HEAD)
GIT_SEQUENCE_EDITOR='cp /tmp/rebase-plan' git rebase -i $BASE
```

---

### ❌ DON'T: Use `git reset --soft` without understanding the implications
```bash
git reset --soft HEAD~5  # Dangerous - loses commit metadata
```

### ✅ DO: Use proper rebase workflow
```bash
# Creates clean history while preserving authorship and timestamps
BASE=$(git merge-base origin/main HEAD)
GIT_SEQUENCE_EDITOR='cp /tmp/plan' git rebase -i $BASE
```

---

### ❌ DON'T: Forget to verify before pushing
```bash
git push --force  # Push without checking
```

### ✅ DO: Always verify first
```bash
git log --oneline -5  # Check commits
git show HEAD         # Review latest commit
git push --force-with-lease
```

## Example: Squash 6 Commits into 3

**Goal**: Combine 6 commits into exactly 3 clean commits.

**Starting commits** (newest to oldest):
```
f - Fix test-backend changes
e - Fix migration part 4
d - Fix migration part 3
c - Fix migration part 2
b - Fix test-engine changes
a - Fix migration part 1
```

**Desired result**:
1. Fix test-engine (commit b)
2. Fix migration (commits a, c, d, e squashed together)
3. Fix test-backend (commit f)

**Steps**:

1. **Find fork point and verify current state**:
```bash
git fetch origin
BASE=$(git merge-base origin/main HEAD)
git log --oneline $BASE..HEAD
# f - Fix test-backend changes
# e - Fix migration part 4
# d - Fix migration part 3
# c - Fix migration part 2
# b - Fix test-engine changes
# a - Fix migration part 1
```

2. **Create rebase plan** (oldest to newest):
```bash
cat << 'EOF' > /tmp/git-rebase-todo
pick a Fix migration part 1
fixup c Fix migration part 2
fixup d Fix migration part 3
fixup e Fix migration part 4
pick b Fix test-engine changes
pick f Fix test-backend changes
EOF
```

Note: Commits must be in chronological order (oldest first)!

3. **Execute rebase**:
```bash
GIT_SEQUENCE_EDITOR='cp /tmp/git-rebase-todo' git rebase -i $BASE
```

4. **Reword commit messages** (optional, second rebase pass):
```bash
NEW_BASE=$(git merge-base origin/main HEAD)
cat << 'EOF' > /tmp/git-rebase-todo
reword <hash-a> Fix migration part 1
reword <hash-b> Fix test-engine changes
reword <hash-f> Fix test-backend changes
EOF
GIT_SEQUENCE_EDITOR='cp /tmp/git-rebase-todo' git rebase -i $NEW_BASE

# When stopped at each commit:
git commit --amend -m "Better commit message with details"
git rebase --continue
```

5. **Verify and push**:
```bash
git log --oneline -3
git push --force-with-lease
```

## Tips

- **Fetch first**: Always run `git fetch origin` before finding the base — a stale ref will give you the wrong merge-base
- **Your rebase plan must list ALL commits between BASE and HEAD**: If you omit any, they get silently dropped. Use `git log $BASE..HEAD` to confirm the full list before writing the plan
- **Check order**: Rebase plans list commits oldest-to-newest (opposite of git log)
- **Use fixup**: Prefer `fixup` over `squash` to avoid accumulating commit messages; use `reword` on the lead commit if you want a better message
- **Present options first**: Show 2–3 breakdown options with sizes before running anything — let the user choose
- **Diff before push**: Always run `git diff <old-HEAD> HEAD --stat` after rebasing and before force pushing — empty diff = safe
- **--force-with-lease**: Safer than `--force` — fails if the remote has moved on since your last fetch

## When Things Go Wrong

### Rebase conflict:
```bash
# See what's conflicting
git status

# Fix conflicts in files, then:
git add <resolved-files>
git rebase --continue

# OR abandon the rebase:
git rebase --abort
```

### Wrong commits squashed:
```bash
# Abort and start over
git rebase --abort

# OR if already pushed, force push the old state:
git reflog  # Find the commit before rebase
git reset --hard <commit-hash>
git push --force-with-lease
```

### Rebase stuck/hanging:
```bash
# Don't use interactive commands in the shell
# Always use GIT_SEQUENCE_EDITOR approach shown above
```
