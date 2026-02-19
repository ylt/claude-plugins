---
name: plugin-creator
description: Guide for creating Claude Code plugins. This skill should be used when the user wants to "create a plugin", "write a plugin", "build a plugin", "scaffold a plugin", "set up plugin structure", "configure plugin.json", "add commands to a plugin", "add agents to a plugin", "add hooks to a plugin", "add MCP server to a plugin", "add LSP to a plugin", "organize plugin components", or needs guidance on Claude Code plugin architecture, manifest configuration, or plugin distribution.
---

# Plugin Creator

Guide for creating complete Claude Code plugins with commands, agents, skills, hooks, MCP servers, and LSP servers.

## About Plugins

A **plugin** is a self-contained directory of components that extends Claude Code. Plugins bundle related functionality into a single distributable package that users install and enable.

### Plugin Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Commands** | Slash commands users invoke | `commands/*.md` |
| **Agents** | Specialized subagents | `agents/*.md` |
| **Skills** | Auto-activating knowledge packs | `skills/*/SKILL.md` |
| **Hooks** | Event-driven automation | `hooks/hooks.json` |
| **MCP Servers** | External tool integrations | `.mcp.json` |
| **LSP Servers** | Code intelligence | `.lsp.json` |

Only include components the plugin actually needs. A minimal plugin may have just one command or skill.

### Plugin Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Manifest (only file in this dir)
├── commands/                 # At root level
├── agents/                   # At root level
├── skills/                   # At root level
├── hooks/
│   ├── hooks.json
│   └── scripts/
├── .mcp.json
├── .lsp.json
└── scripts/
```

**Critical rule:** Component directories MUST be at plugin root, NOT inside `.claude-plugin/`. Only `plugin.json` goes in `.claude-plugin/`.

## Plugin Creation Process

Follow these steps in order. Skip steps only when clearly inapplicable.

1. Understand plugin requirements
2. Plan plugin components
3. Scaffold the plugin
4. Implement components
5. Validate and test
6. Iterate

### Step 1: Understand Plugin Requirements

Clarify the plugin's purpose and scope before building anything.

**Key questions to resolve:**
- What problem does this plugin solve?
- Who will use it and when?
- What component types are needed?
- Any external service dependencies?

For example, when building a `database-tools` plugin, the analysis shows:
1. Users need commands to run migrations and query schemas
2. An MCP server connects to the database
3. A hook validates SQL before execution
4. A skill provides migration best practices

Conclude this step with a clear understanding of which components to build.

### Step 2: Plan Plugin Components

Map requirements to specific components:

| Component | Count | Purpose |
|-----------|-------|---------|
| Commands | 2 | create-migration, run-migration |
| Skills | 1 | Migration best practices |
| MCP | 1 | Database connection |
| Hooks | 1 | SQL validation |

For each component, identify:
- Triggering conditions (commands: user invocation; agents: auto/manual; skills: description match; hooks: event match)
- Required tools and permissions
- External dependencies (binaries, APIs, env vars)

### Step 3: Scaffold the Plugin

Run the scaffolding script to create the directory structure:

```bash
python3 scripts/scaffold-plugin.py <plugin-name> --path <parent-dir> [--components <list>]
```

**Arguments:**
- `plugin-name` — kebab-case identifier (e.g., `database-tools`)
- `--path` — parent directory to create plugin in
- `--components` — comma-separated subset: `commands,agents,skills,hooks,mcp,lsp,scripts` (default: all)

**Example:**
```bash
python3 scripts/scaffold-plugin.py database-tools --path ~/plugins --components commands,skills,hooks,mcp
```

The script creates the directory structure with template files for each component. Customize or delete the generated examples.

**Configure the manifest** in `.claude-plugin/plugin.json`:
```json
{
  "name": "database-tools",
  "version": "0.1.0",
  "description": "Database migration and query tools",
  "keywords": ["database", "migrations", "sql"]
}
```

For the full manifest schema (all fields, component paths, metadata), consult **`references/plugin-reference.md`**.

### Step 4: Implement Components

Implement each component following the patterns in **`references/component-patterns.md`**. Key points per component type:

#### Commands

Markdown files in `commands/` with YAML frontmatter. Write instructions **for Claude** (these are prompts Claude follows). Use `$ARGUMENTS` for user input. Filename becomes the slash command name.

```markdown
---
description: Run database migrations
argument-hint: up|down|status
allowed-tools: ["Read", "Bash", "Glob"]
---

# Run Migrations
Based on $ARGUMENTS, execute the appropriate migration action...
```

#### Agents

Markdown files in `agents/` with `<example>` blocks in the description for reliable auto-triggering. Include 2-4 realistic examples showing user messages that should invoke the agent.

```markdown
---
name: sql-reviewer
description: |
  SQL query and migration review specialist.

  <example>
  user: Review this migration for safety issues
  assistant: (uses sql-reviewer)
  </example>
---

System prompt defining the agent's role and behavior...
```

#### Skills

For creating skills within a plugin, **invoke the skill-creator skill** (`/skill-creator`). It provides the complete methodology for understanding use cases, planning resources, writing effective SKILL.md with strong triggers, and progressive disclosure design.

Create skill directories within the plugin's `skills/` directory. Follow the same standards: third-person description with specific trigger phrases, imperative form in body, lean SKILL.md with detailed content in `references/`.

#### Hooks

Configure in `hooks/hooks.json`. Three hook types: `command` (shell scripts), `prompt` (LLM evaluation), `agent` (agentic verification). Always use `${CLAUDE_PLUGIN_ROOT}` for portable paths.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh"
      }]
    }]
  }
}
```

Hook scripts must be executable (`chmod +x`), include a shebang, read JSON from stdin, and output JSON decisions to stdout.

#### MCP Servers

Configure in `.mcp.json`. Use `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths. Servers start automatically when the plugin enables.

```json
{
  "mcpServers": {
    "database": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/db.js"],
      "env": { "DB_URL": "${DB_URL}" }
    }
  }
}
```

Document required environment variables clearly.

#### LSP Servers

Configure in `.lsp.json`. Map file extensions to language identifiers. The language server binary must be installed separately.

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": { ".ts": "typescript", ".tsx": "typescriptreact" }
  }
}
```

For complete patterns, examples, and all configuration options for every component type, consult **`references/component-patterns.md`**.

### Step 5: Validate and Test

**Test locally:**
```bash
claude --plugin-dir /path/to/plugin-name
```

**Debug loading issues:**
```bash
claude --debug
```

**Validation checklist:**
- [ ] `.claude-plugin/plugin.json` has valid JSON with `name` field
- [ ] Component directories are at plugin root (not in `.claude-plugin/`)
- [ ] All paths use `${CLAUDE_PLUGIN_ROOT}` (no hardcoded paths)
- [ ] Hook scripts are executable with shebangs
- [ ] Skills have `SKILL.md` with frontmatter (`name` + `description`)
- [ ] Agent descriptions include `<example>` blocks
- [ ] MCP server commands exist and are reachable
- [ ] Required environment variables are documented

For debugging details and common issues, consult **`references/plugin-reference.md`**.

### Step 6: Iterate

After testing the plugin on real tasks:
1. Strengthen skill trigger phrases based on what users actually say
2. Add missing edge case handling in hooks
3. Improve agent examples for more reliable auto-triggering
4. Bump `version` in plugin.json before distributing updates (caching prevents updates otherwise)

## Resources

### Reference Files

Consult these when implementing specific component types or troubleshooting:

- **`references/plugin-reference.md`** — Complete technical reference: manifest schema, auto-discovery, environment variables, installation scopes, CLI commands, debugging, common issues
- **`references/component-patterns.md`** — Detailed patterns for every component type: commands, agents, skills, hooks, MCP servers, LSP servers. Includes format specs, frontmatter fields, and working examples

### Scripts

- **`scripts/scaffold-plugin.py`** — Scaffolds a new plugin directory with selected components and template files

### External Skills

- **skill-creator** (`/skill-creator`) — Invoke when creating skills within a plugin. Provides the full methodology for writing effective skills with progressive disclosure.
