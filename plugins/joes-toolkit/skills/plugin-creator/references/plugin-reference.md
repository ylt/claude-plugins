# Plugin Technical Reference

Complete technical reference for the Claude Code plugin system.

## Table of Contents

- [Plugin Manifest Schema](#plugin-manifest-schema)
- [Directory Structure](#directory-structure)
- [Auto-Discovery Mechanism](#auto-discovery-mechanism)
- [Environment Variables](#environment-variables)
- [Installation Scopes](#installation-scopes)
- [Plugin Caching](#plugin-caching)
- [CLI Commands](#cli-commands)
- [Version Management](#version-management)
- [Debugging](#debugging)
- [Common Issues](#common-issues)

---

## Plugin Manifest Schema

Located at `.claude-plugin/plugin.json`. Optional — if omitted, Claude Code auto-discovers components and derives the name from the directory.

### Required Fields

Only `name` is required (if manifest exists):

```json
{
  "name": "plugin-name"
}
```

Name must be kebab-case, unique across installed plugins.

### All Fields

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": "./custom/commands/special.md",
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Component Path Fields

| Field | Type | Description |
|-------|------|-------------|
| `commands` | string\|array | Additional command files/directories |
| `agents` | string\|array | Additional agent files |
| `skills` | string\|array | Additional skill directories |
| `hooks` | string\|array\|object | Hook config paths or inline config |
| `mcpServers` | string\|array\|object | MCP config paths or inline config |
| `outputStyles` | string\|array | Output style files/directories |
| `lspServers` | string\|array\|object | LSP configs |

**Path rules:**
- Custom paths supplement defaults (don't replace them)
- Must be relative to plugin root, starting with `./`
- Support arrays for multiple locations

---

## Directory Structure

```
plugin-name/
├── .claude-plugin/           # Metadata (only plugin.json goes here)
│   └── plugin.json
├── commands/                 # Slash commands (.md files)
├── agents/                   # Subagent definitions (.md files)
├── skills/                   # Skills (subdirectories with SKILL.md)
│   └── skill-name/
│       └── SKILL.md
├── hooks/                    # Event handlers
│   ├── hooks.json
│   └── scripts/
├── .mcp.json                 # MCP server definitions
├── .lsp.json                 # LSP server configurations
└── scripts/                  # Shared utilities
```

**Critical:** Component directories MUST be at plugin root, NOT inside `.claude-plugin/`.

---

## Auto-Discovery Mechanism

Claude Code automatically discovers components:

1. Reads `.claude-plugin/plugin.json` when plugin enables
2. Scans `commands/` for `.md` files
3. Scans `agents/` for `.md` files
4. Scans `skills/` for subdirectories containing `SKILL.md`
5. Loads `hooks/hooks.json` or manifest hooks
6. Loads `.mcp.json` or manifest MCP config
7. Loads `.lsp.json` or manifest LSP config

No restart required — changes take effect on next session.

---

## Environment Variables

### ${CLAUDE_PLUGIN_ROOT}

Absolute path to the plugin directory. Use in all intra-plugin path references:

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"
}
```

Available in:
- Hook command paths
- MCP server command/args
- Script execution
- As environment variable in executed scripts

**Never use:** hardcoded absolute paths, relative paths from working directory, or `~/` shortcuts.

---

## Installation Scopes

| Scope | Settings File | Use Case |
|-------|--------------|----------|
| `user` | `~/.claude/settings.json` | Personal, all projects (default) |
| `project` | `.claude/settings.json` | Team, shared via VCS |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |
| `managed` | `managed-settings.json` | Read-only, update only |

---

## Plugin Caching

Marketplace plugins are copied to `~/.claude/plugins/cache`. Implications:

- Plugins cannot reference files outside their directory
- Path traversal (`../shared-utils`) won't work after install
- Symlinks are honored during copy (use for external dependencies)

---

## CLI Commands

```bash
# Install
claude plugin install <name>[@marketplace] [--scope user|project|local]

# Uninstall (aliases: remove, rm)
claude plugin uninstall <name>[@marketplace] [--scope user|project|local]

# Enable/Disable
claude plugin enable <name> [--scope ...]
claude plugin disable <name> [--scope ...]

# Update
claude plugin update <name> [--scope user|project|local|managed]
```

---

## Version Management

Follow semver: `MAJOR.MINOR.PATCH`

- Set in `plugin.json` or marketplace entry (plugin.json takes priority)
- Bump version before distributing changes (caching prevents updates otherwise)
- Pre-release versions: `2.0.0-beta.1`

---

## Debugging

Run `claude --debug` (or `/debug` in TUI) to see:
- Plugin loading details
- Manifest errors
- Component registration
- MCP server initialization

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Plugin not loading | Invalid plugin.json | Validate JSON syntax |
| Commands not appearing | Wrong directory | Ensure `commands/` at root, not in `.claude-plugin/` |
| Hooks not firing | Script not executable | `chmod +x script.sh` |
| MCP server fails | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all paths |
| Path errors | Absolute paths | Use relative paths starting with `./` |
| LSP executable not found | Server not installed | Install the binary separately |

### Hook Troubleshooting

1. Check executable: `chmod +x ./scripts/your-script.sh`
2. Verify shebang: `#!/usr/bin/env bash`
3. Check path uses `${CLAUDE_PLUGIN_ROOT}`
4. Test manually: `./scripts/your-script.sh`

### MCP Server Troubleshooting

1. Verify command exists and is executable
2. Check all paths use `${CLAUDE_PLUGIN_ROOT}`
3. Use `claude --debug` to see initialization errors
4. Test server outside Claude Code
