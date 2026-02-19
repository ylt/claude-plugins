# Component Patterns Reference

How to write each plugin component type with correct format, frontmatter, and best practices.

## Table of Contents

- [Commands](#commands)
- [Agents](#agents)
- [Skills](#skills)
- [Hooks](#hooks)
- [MCP Servers](#mcp-servers)
- [LSP Servers](#lsp-servers)

---

## Commands

Slash commands users invoke directly. Located in `commands/` as `.md` files.

### Format

```markdown
---
description: What the command does (shown in /help)
argument-hint: Description of expected arguments
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
---

# Command Title

Instructions FOR Claude to execute when this command is invoked.
Write as a prompt — Claude follows these instructions when the user runs the command.

Use $ARGUMENTS to reference what the user passes after the command name.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Shown in command listing |
| `argument-hint` | No | Describes expected arguments |
| `allowed-tools` | No | Restricts which tools Claude can use |

### Key Principles

- Write instructions **for Claude**, not documentation for the user
- Use `$ARGUMENTS` placeholder for user-provided input
- Keep commands focused on a single workflow
- Reference skills or agents when complex logic is needed
- Command filename becomes the slash command name: `deploy.md` → `/plugin:deploy`

### Example: Code Review Command

```markdown
---
description: Review code changes for quality, security, and best practices
argument-hint: Optional file path or PR number to review
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Code Review

Perform a thorough code review on the specified target.

If $ARGUMENTS contains a file path, review that file.
If $ARGUMENTS contains a PR number, use `gh pr diff $ARGUMENTS` to get the diff.
If $ARGUMENTS is empty, review staged changes with `git diff --cached`.

## Review Checklist

1. **Correctness**: Logic errors, edge cases, off-by-one errors
2. **Security**: Injection, XSS, hardcoded secrets, OWASP top 10
3. **Performance**: N+1 queries, unnecessary allocations, missing indexes
4. **Maintainability**: Naming, complexity, duplication

Present findings organized by severity: Critical > Warning > Suggestion.
```

---

## Agents

Specialized subagents Claude can invoke automatically or users invoke manually. Located in `agents/` as `.md` files.

### Format

```markdown
---
name: agent-name
description: |
  What this agent specializes in.

  <example>
  user: Example user message that triggers this agent
  assistant: (uses agent-name)
  </example>

  <example>
  user: Another triggering scenario
  assistant: (uses agent-name)
  </example>
model: sonnet
tools: ["Read", "Glob", "Grep", "Bash", "Write", "Edit"]
---

Detailed system prompt defining the agent's role, expertise, constraints, and output format.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier (kebab-case) |
| `description` | Yes | When to use, with `<example>` blocks |
| `model` | No | `sonnet`, `opus`, `haiku` |
| `tools` | No | Tool allowlist |
| `color` | No | Display color in UI |

### Description with Examples

The `<example>` blocks in the description are critical for reliable auto-triggering. Include 2-4 examples showing realistic user messages:

```yaml
description: |
  Security analysis specialist for code and configurations.

  <example>
  user: Check this API endpoint for security vulnerabilities
  assistant: (uses security-reviewer)
  </example>

  <example>
  user: Is this authentication implementation secure?
  assistant: (uses security-reviewer)
  </example>
```

### System Prompt Patterns

**Analysis agent:** Define what to analyze, criteria, output format
**Generation agent:** Define what to create, constraints, quality standards
**Validation agent:** Define what to check, pass/fail criteria, reporting format
**Orchestration agent:** Define workflow steps, decision points, delegation rules

---

## Skills

Auto-activating knowledge packs. Located in `skills/` as subdirectories with `SKILL.md`.

### Format

```markdown
---
name: Skill Name
description: "This skill should be used when the user asks to \"do X\", \"perform Y\", or mentions Z. Specific trigger phrases and scenarios."
---

# Skill Name

Core instructions and guidance. Keep lean (1,500-2,000 words).
Move detailed content to references/ subdirectory.

## Additional Resources

- **`references/patterns.md`** - Detailed patterns and examples
- **`scripts/validate.sh`** - Validation utility
```

### Structure

```
skill-name/
├── SKILL.md           # Core instructions (required)
├── references/        # Detailed docs (loaded as needed)
├── examples/          # Working code examples
├── scripts/           # Utility scripts
└── assets/            # Templates, images, etc.
```

### Key Principles

- **Description triggers activation** — include specific user phrases
- **Third person** in description: "This skill should be used when..."
- **Imperative form** in body: "Configure the server" not "You should configure"
- **Progressive disclosure**: lean SKILL.md, detailed references
- **Reference the skill-creator skill** for full methodology on creating high-quality skills

### Creating Skills Within Plugins

For creating skills as part of a plugin, invoke the **skill-creator** skill (`/skill-creator`). It provides the complete methodology for:
- Understanding use cases with concrete examples
- Planning reusable contents (scripts, references, assets)
- Writing effective SKILL.md with strong triggers
- Progressive disclosure design
- Packaging and validation

Create the skill directory within the plugin's `skills/` directory instead of the default skill path.

---

## Hooks

Event-driven automation. Configured in `hooks/hooks.json` or inline in `plugin.json`.

### Configuration Format

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command|prompt|agent",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hook.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

For inline in plugin.json, use the same structure under a top-level `"hooks"` key.

### Available Events

| Event | When | Matcher |
|-------|------|---------|
| `PreToolUse` | Before tool execution | Tool name pattern |
| `PostToolUse` | After successful tool use | Tool name pattern |
| `PostToolUseFailure` | After tool failure | Tool name pattern |
| `PermissionRequest` | Permission dialog shown | — |
| `UserPromptSubmit` | User submits prompt | — |
| `Notification` | Notification sent | — |
| `Stop` | Claude attempts to stop | — |
| `SubagentStart` | Subagent starts | — |
| `SubagentStop` | Subagent attempts to stop | — |
| `SessionStart` | Session begins | — |
| `SessionEnd` | Session ends | — |
| `TeammateIdle` | Teammate about to go idle | — |
| `TaskCompleted` | Task marked completed | — |
| `PreCompact` | Before history compaction | — |

### Hook Types

**command** — Execute a shell command/script:
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

**prompt** — Evaluate with an LLM (uses `$ARGUMENTS` for context):
```json
{
  "type": "prompt",
  "prompt": "Review this tool call for safety concerns: $ARGUMENTS. Respond with JSON: {\"decision\": \"allow|block\", \"reason\": \"...\"}"
}
```

**agent** — Run an agentic verifier with tools:
```json
{
  "type": "agent",
  "prompt": "Verify the code changes are safe and follow conventions: $ARGUMENTS"
}
```

### Hook Script Requirements

- Must be executable (`chmod +x`)
- Include shebang (`#!/usr/bin/env bash`)
- Use `${CLAUDE_PLUGIN_ROOT}` for paths
- Input via stdin (JSON with tool_name, tool_input, etc.)
- Output JSON to stdout for decisions:

```json
{"decision": "allow", "reason": "Checks passed"}
{"decision": "block", "reason": "Blocked: dangerous operation"}
```

---

## MCP Servers

External tool integrations via Model Context Protocol. Configured in `.mcp.json` or inline in `plugin.json`.

### Configuration Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": {
        "API_KEY": "${API_KEY}",
        "DATA_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

### Server Types

**stdio (local process):**
```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
  "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
}
```

**SSE (hosted, often with OAuth):**
```json
{
  "url": "https://api.example.com/mcp",
  "headers": { "Authorization": "Bearer ${TOKEN}" }
}
```

### Key Principles

- Servers start automatically when plugin enables
- Use `${CLAUDE_PLUGIN_ROOT}` for all plugin-relative paths
- Environment variables expand at runtime
- Document required env vars in plugin README
- Server tools integrate seamlessly with Claude's toolkit

---

## LSP Servers

Language Server Protocol integration for code intelligence. Configured in `.lsp.json` or inline in `plugin.json`.

### Configuration Format

```json
{
  "language-name": {
    "command": "language-server-binary",
    "args": ["serve"],
    "extensionToLanguage": {
      ".ext": "language-id"
    }
  }
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `command` | LSP binary to execute (must be in PATH) |
| `extensionToLanguage` | Maps file extensions to language identifiers |

### Optional Fields

| Field | Description |
|-------|-------------|
| `args` | Command-line arguments |
| `transport` | `stdio` (default) or `socket` |
| `env` | Environment variables |
| `initializationOptions` | Options for server init |
| `settings` | Passed via `workspace/didChangeConfiguration` |
| `restartOnCrash` | Auto-restart on crash |
| `maxRestarts` | Max restart attempts |

### Example: TypeScript LSP

```json
{
  "typescript": {
    "command": "typescript-language-server",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ts": "typescript",
      ".tsx": "typescriptreact",
      ".js": "javascript",
      ".jsx": "javascriptreact"
    }
  }
}
```

**Important:** The language server binary must be installed separately. LSP plugins configure the connection, not the server itself.
