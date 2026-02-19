---
name: obsidian-vault
description: >
  Maintain an Obsidian vault with clean graph structure, hierarchical indexes,
  and lifecycle-based classification. Use when: (1) creating or editing Obsidian
  vault notes, (2) organizing or classifying content into vault categories,
  (3) maintaining folder indexes and navigation, (4) checking vault graph health
  or finding orphaned notes, (5) working with any Obsidian MCP tools
  (mcp__obsidian__*), or (6) the user mentions their vault, notes, or Obsidian.
---

# Obsidian Vault Maintenance

## First Step: Always Read VAULT.md

Before any vault operation, read the live `VAULT.md` in the vault using `mcp__obsidian__view` for current organizational rules, categories, folder structure, and privacy boundaries. VAULT.md is the single source of truth for all vault-specific details (current areas, projects, naming, privacy classifications).

## Classification Decision Tree

Apply in order when creating or filing a note:

1. Machine-generated? -> `Data/`
2. Script/tool? -> `Automation/`
3. Ongoing responsibility (3-5yr lifespan)? -> `Areas/`
4. Finite effort with eventual end? -> `Projects/YYYY/QN/`
5. Reusable reference info? -> `Knowledge/`
6. Inactive/obsolete? -> `Archive/`

If uncertain, ask the user about timeline (ongoing vs. finite) and purpose (tracking vs. reference).

## Creating a Note

1. **Classify** using the decision tree above
2. **Check existing folders** - use `mcp__obsidian__vault` action `list` to avoid duplicates
3. **Create the note** with `mcp__obsidian__vault` action `create`
   - Add a back-link to parent index: `[[ParentFolder|<- Back to Parent]]`
4. **Update parent index** - use `mcp__obsidian__edit` to add entry to the folder note (`FolderName/FolderName.md`)
   - Keep entries concise: 1-2 lines with link and brief description
5. **Create missing indexes** - if parent folder note doesn't exist, create it first

### Projects: Index Hierarchy

Projects use `Projects/YYYY/QN/ProjectName/` structure with indexes at each level. Each level adds progressively more detail; upper levels stay concise for scanning. Sub-pages are only linked from the project-level index, never from higher indexes.

Create year/quarter indexes when the first project in that period is created. Never skip index levels.

## Index Maintenance

**Folder note convention:** Every folder has `FolderName/FolderName.md`.

When adding content to any folder:
1. Check if folder note exists - if not, create it
2. Add entry to folder note (brief: 1-2 lines)
3. Add back-link in the new file to the folder note
4. Don't link sub-sub-pages from high-level indexes

## Verifying Graph Health

Use `mcp__obsidian__graph` to check connectivity:

- `statistics` - get link counts and identify orphans
- `neighbors` with a sourcePath - check a note's connections
- `backlinks` / `forwardlinks` - verify bidirectional linking
- `traverse` from category entry points to verify reachability

**Every note must be reachable from an index. No orphaned files.**

Common fixes:
- Missing parent index entry -> `mcp__obsidian__edit` action `append` on the folder note
- Missing back-link -> `mcp__obsidian__edit` action `append` on the orphaned note
- Wrong category -> `mcp__obsidian__vault` action `move`, then update both old and new indexes

## Naming Conventions

- **Files:** Title case, descriptive, no dates in names, no special chars except hyphens
- **Folders:** Hyphens for multi-word, no underscores
- **Folder notes:** Match folder name exactly
- **No root-level files** except `Home.md` and `VAULT.md`

## Privacy Boundaries

Read `VAULT.md` for current privacy classifications. Categories are marked as always-private, safe to publish, or review-first.

## Companion Skills

- **obsidian-markdown** - Use for Obsidian Flavored Markdown syntax: wikilinks, embeds, callouts, frontmatter/properties, tags. Defer to this skill for markdown formatting questions.
- **obsidian-bases** - Use for `.base` files: database-like views, filters, formulas, summaries. Defer to this skill when creating or editing Bases.

This skill handles vault-level organization (where files go, index maintenance, graph health). The companion skills handle content-level concerns (how to format notes, how to build views).

## Post-Operation Checklist

After any vault modification, verify:
- [ ] Parent index updated with entry for new/modified note
- [ ] Back-link added in new file pointing to parent index
- [ ] File placed in correct category per decision tree
- [ ] Graph stays connected (no new orphans introduced)
