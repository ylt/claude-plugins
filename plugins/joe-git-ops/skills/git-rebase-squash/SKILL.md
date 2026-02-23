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

# View all commits on your branch since the fork point
git log --oneline $BASE..HEAD
```

This is more reliable than manually counting with `HEAD~N` — it automatically finds exactly the right base regardless of how many commits exist on the branch.

### 3. Create Rebase Plan File

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

### 4. Execute Rebase

```bash
# Use GIT_SEQUENCE_EDITOR to point to your plan file, rebase onto the fork point
GIT_SEQUENCE_EDITOR='cp /tmp/git-rebase-todo' git rebase -i $BASE
```

Where `$BASE` is the merge-base commit found in step 2.

### 5. Handle Interactive Steps

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

### 6. Verify Result

```bash
# Check the new history
git log --oneline -N

# View detailed commit messages
git log -N --format="commit %h%n%s%n%b"
```

### 7. Force Push

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

- **Use merge-base**: Always use `git merge-base origin/main HEAD` to find the fork point — avoids miscounting commits
- **Fetch first**: Run `git fetch origin` before merge-base to ensure you have the latest remote state
- **Check order**: Rebase plans list commits oldest-to-newest (opposite of git log)
- **Use fixup**: Prefer `fixup` over `squash` to avoid accumulating commit messages
- **Verify before push**: Always check `git log` before force pushing
- **--force-with-lease**: Safer than `--force`—prevents overwriting unexpected remote changes

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
