---
name: markdown-vault-sync
description: >
  Two trigger modes: (A) IMMEDIATE - invoke this skill FIRST, before writing any
  local files, when the user mentions syncing to Obsidian, getting docs into the
  vault, or putting project documentation in Obsidian. Do NOT create local .md
  files first. (B) OFFER - after creating or editing markdown outside the vault
  (documentation, notes, research, guides, plans, summaries), offer to sync it.
  Do not wait for the user to ask in mode B - offer after substantive markdown
  is written.
---

# Markdown Vault Sync

## Trigger Modes

### Mode A: Immediate (user asks for vault sync)

When the user mentions syncing to Obsidian, getting docs into the vault, or putting project documentation in Obsidian — invoke this skill **immediately** and go straight to the Sync Workflow. Do NOT create local `.md` files first.

### Mode B: Offer (after markdown work)

After creating or substantially editing markdown outside the vault, offer to sync if the content is:

- Reference material (guides, documentation, how-tos, API notes)
- Project-related (plans, itineraries, research, decisions, specs)
- Personal notes (meeting notes, summaries, journal-style entries)
- Knowledge capture (anything the user might want to find later)

Do **not** offer for READMEs/CHANGELOGs (belong in codebase), throwaway content, or files already in the vault.

Ask concisely: "Want me to sync this to your Obsidian vault?"

## Project Documentation Mode

When the user asks to get a project's documentation into the vault (e.g. "sync this project to Obsidian", "get project docs into the vault"), don't just mirror existing files. **Generate documentation from the codebase** to fill gaps.

### What to Generate

Survey the project (README, config files, source code, tests, existing docs) and produce vault-ready notes for:

- **Project overview** - what it does, tech stack, architecture, how to run it
- **Architecture/conventions** - key patterns, code structure, design decisions
- **API/tool reference** - endpoints, tools, interfaces (if applicable)
- **Status/progress** - current state, what's done, what's planned

Only generate notes where the content is substantive enough to be useful. Don't create empty stubs. Synthesize from source code and config when docs don't exist - the vault note should be more useful than the raw files.

### What NOT to Generate

- Don't duplicate repo-standard files verbatim (README, CHANGELOG)
- Don't create notes for trivial projects with nothing to document
- Don't generate notes the user didn't agree to in the proposal

## Sync Workflow (Two Phases)

Syncing happens in two phases: **propose** (main context) then **execute** (dedicated agent).

### Phase 1: Propose Placement (Main Context)

Survey the project and propose what to sync **before** spawning the agent. This lets the user confirm, adjust, or add/remove notes.

**Do NOT call any `mcp__obsidian__*` tools in Phase 1.** Propose paths using the conventions below. The agent will check for duplicates and handle conflicts.

1. **Load the obsidian-vault skill** first (invoke it via the Skill tool). This loads the classification decision tree and vault conventions needed to propose correct paths.
2. Read project files (local, not vault) to understand what exists and what's missing.
3. **Always include a project index note** as the first note: `ProjectName/ProjectName.md`. This is the folder note that links to all sub-pages and provides the project overview.
4. **Use the full vault path structure.** For projects: `Projects/YYYY/QN/ProjectName/`. Use the current year and quarter. Never use flat paths like `Projects/ProjectName/`.
5. Propose a table of vault notes with:
   - Note title and brief description
   - Full vault path (e.g. `Projects/2026/Q1/ProjectName/ProjectName.md`)
   - Source (existing file, or "generated from codebase")
6. Wait for user confirmation (they may adjust paths, titles, or scope)

### Phase 2: Execute via vault-sync Agents

Use `TaskCreate` to track page creation and index maintenance for user visibility.

#### Step 1: Create pages

**Pre-written content:** Call `mcp__obsidian__vault` `create` directly from the main context — make all create calls in parallel. Each note needs a back-link to its parent folder index. No agent needed; the content is already prepared.

**Generated content:** Spawn a `vault-sync` agent in background (`run_in_background: true`, `subagent_type: "vault-sync"`) for notes that need synthesis from source files. The agent does the real work: reading source, synthesizing, creating. Prompt must say **do NOT update indexes**.

#### Step 2: Index agent (foreground, after all pages exist)

Spawn ONE `vault-sync` agent in foreground. This agent:
- Receives the list of all created vault paths
- Updates all parent indexes (project folder note, quarter, year, category)
- Creates any missing index notes
- Verifies graph health
- Reports back

## Agent Prompt Guidelines

Include in any generation agent's prompt:
- Vault paths and titles for notes to generate
- Source file paths with generation instructions
- Brief project context (what the project does, tech stack)
- **Explicit instruction: do NOT update indexes**

Include in the index agent's prompt:
- List of all vault paths that were created
- The project name and base path
- Instruction to update all index levels and verify graph health

Keep original files in place - the vault gets copies, not moves.
