# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A Claude Code plugin marketplace containing personal plugins. There is no build system, no tests, and no compiled code. All content is Markdown, JSON, YAML, and one Python script.

## Repository Structure

```
.claude-plugin/marketplace.json    # Marketplace manifest — registers plugins
plugins/
  joes-toolkit/                    # Obsidian, humor, and plugin-creation skills
    .claude-plugin/plugin.json
    skills/
      obsidian-vault/              # Vault organization, classification, graph health
      obsidian-markdown/           # Obsidian Flavored Markdown syntax reference
      obsidian-bases/              # Obsidian Bases (.base files) reference
      markdown-vault-sync/         # Sync markdown content to Obsidian vault
      quip/                        # Dark dev humor generation with reference formats
      plugin-creator/              # Guide + scaffolder for creating Claude Code plugins
  joe-git-ops/                     # Git workflow skills
    .claude-plugin/plugin.json
    skills/
      git-rebase-squash/           # Non-interactive rebase/squash via GIT_SEQUENCE_EDITOR
```

## Key Conventions

- **Skill anatomy**: Every skill is a directory containing `SKILL.md` (with YAML frontmatter: `name` + `description`), optional `references/` for detailed content, and optional `scripts/`.
- **SKILL.md descriptions** use third person ("This skill should be used when...") with specific trigger phrases. The body uses imperative form.
- **Progressive disclosure**: Keep SKILL.md lean (1,500–2,000 words). Detailed reference material goes in `references/` subdirectories and is loaded on demand.
- **Plugin structure rule**: Component directories (`commands/`, `agents/`, `skills/`, `hooks/`) must be at the plugin root, never inside `.claude-plugin/`. Only `plugin.json` goes in `.claude-plugin/`.
- **Marketplace manifest** (`.claude-plugin/marketplace.json`) lists plugins with `source` paths relative to repo root.

## Working With Skills

When editing a skill's `SKILL.md`:
- Frontmatter `description` drives auto-activation — include the exact phrases users would say.
- The `quip` skill **requires** reading a format's reference file before generating any joke (enforced in its workflow section).
- The `plugin-creator` skill has a scaffolding script at `plugins/joes-toolkit/skills/plugin-creator/scripts/scaffold-plugin.py` — run with `python3 scripts/scaffold-plugin.py <name> --path <dir> [--components <list>]`.

## Obsidian Skills Relationship

Four skills work together for Obsidian vault operations:
- `obsidian-vault` — where files go, index maintenance, graph health (organizational)
- `obsidian-markdown` — how to format note content (syntax reference)
- `obsidian-bases` — how to build `.base` database views (syntax reference)
- `markdown-vault-sync` — two-phase workflow for syncing content into the vault

The vault skill always reads `VAULT.md` from the live vault first via MCP tools. The sync skill proposes placement before executing, and separates page creation from index maintenance.
