#!/usr/bin/env python3
"""
Plugin Scaffolder - Creates a new Claude Code plugin from template

Usage:
    scaffold-plugin.py <plugin-name> --path <path> [--components <comma-separated>]

Components: commands,agents,skills,hooks,mcp,lsp,scripts (default: all)

Examples:
    scaffold-plugin.py my-plugin --path ./plugins
    scaffold-plugin.py my-plugin --path ./plugins --components commands,hooks,mcp
"""

import re
import sys
from pathlib import Path


MANIFEST_TEMPLATE = """{{
  "name": "{plugin_name}",
  "version": "0.1.0",
  "description": "TODO: Brief description of {plugin_title}"
}}
"""

COMMAND_TEMPLATE = """---
description: TODO: What this command does (shown in /help listing)
argument-hint: TODO: Expected arguments description
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash"]
---

# {plugin_title} Command

TODO: Replace with command implementation for {plugin_name}.

Write instructions FOR Claude to execute when the user invokes this command.
Commands are prompts — Claude follows these instructions, they are not shown to the user.

Use $ARGUMENTS to reference what the user passes after the command name.

Example real commands from other plugins:
- code-review: Analyzes staged changes for quality, security, and best practices
- deploy: Runs deployment pipeline with environment selection
- test-runner: Executes test suites with coverage reporting

$ARGUMENTS
"""

AGENT_TEMPLATE = """---
name: {plugin_name}-agent
description: |
  TODO: Describe what this agent specializes in and when Claude should invoke it.
  Include 2-4 <example> blocks showing realistic user messages that trigger this agent.

  <example>
  user: TODO: Example user message that should trigger this agent
  assistant: (uses {plugin_name}-agent)
  </example>

  <example>
  user: TODO: Another triggering scenario
  assistant: (uses {plugin_name}-agent)
  </example>
---

# {plugin_title} Agent

TODO: Write the system prompt for this agent.

Define the agent's role, expertise, constraints, and output format.
This prompt is what the agent sees as its instructions when invoked.

Example real agent system prompts follow patterns:
- **Analysis agent**: Define what to analyze, criteria, output format
- **Generation agent**: Define what to create, constraints, quality standards
- **Validation agent**: Define what to check, pass/fail criteria, reporting format
- **Orchestration agent**: Define workflow steps, decision points, delegation rules
"""

SKILL_TEMPLATE = """---
name: {skill_title}
description: "TODO: This skill should be used when the user asks to \\"do X\\", \\"perform Y\\", or mentions Z. Include specific trigger phrases and scenarios that should activate this skill."
---

# {skill_title}

TODO: Replace with skill content for {plugin_name}.

Use the skill-creator skill (/skill-creator) for the complete methodology:
- Understanding use cases with concrete examples
- Planning reusable contents (scripts, references, assets)
- Writing effective SKILL.md with strong triggers
- Progressive disclosure design

Key requirements:
- Description must use third person ("This skill should be used when...")
- Body must use imperative/infinitive form ("Configure the server" not "You should configure")
- Keep SKILL.md lean (1,500-2,000 words), move detailed content to references/
"""

HOOKS_TEMPLATE = """{{
  "hooks": {{
    "TODO: Replace with event name (PreToolUse, PostToolUse, Stop, etc.)": [
      {{
        "matcher": "TODO: Tool name pattern (e.g., Write|Edit)",
        "hooks": [
          {{
            "type": "command",
            "command": "${{CLAUDE_PLUGIN_ROOT}}/hooks/scripts/TODO-rename.sh"
          }}
        ]
      }}
    ]
  }}
}}
"""

HOOK_SCRIPT_TEMPLATE = """#!/usr/bin/env bash
# Hook script for {plugin_name}
#
# This script is called by Claude Code when a hook event fires.
# Input: JSON via stdin with tool_name, tool_input, etc.
# Output: JSON to stdout with decision and reason.
#
# Example real hook scripts:
# - validate-write.sh: Checks file writes for security issues
# - validate-bash.sh: Blocks dangerous shell commands
# - load-context.sh: Injects additional context on session start

set -euo pipefail

# Read hook input from stdin
INPUT=$(cat)

# TODO: Implement hook logic here
# Parse input with jq: echo "$INPUT" | jq -r '.tool_name'

# Output decision (allow or block)
echo '{{"decision": "allow", "reason": "TODO: Implement validation logic"}}'
"""

MCP_TEMPLATE = """{{
  "mcpServers": {{
    "{plugin_name}-server": {{
      "command": "TODO: server binary or runtime (e.g., node, python3)",
      "args": ["${{CLAUDE_PLUGIN_ROOT}}/servers/TODO-server.js"],
      "env": {{
        "TODO_API_KEY": "${{TODO_API_KEY}}"
      }}
    }}
  }}
}}
"""

LSP_TEMPLATE = """{{
  "TODO-language-name": {{
    "command": "TODO: language-server-binary",
    "args": ["--stdio"],
    "extensionToLanguage": {{
      ".TODO": "TODO-language-id"
    }}
  }}
}}
"""

ALL_COMPONENTS = ["commands", "agents", "skills", "hooks", "mcp", "lsp", "scripts"]


def title_case_plugin_name(plugin_name):
    """Convert hyphenated plugin name to Title Case for display."""
    return ' '.join(word.capitalize() for word in plugin_name.split('-'))


def scaffold_plugin(plugin_name, path, components):
    """
    Create a new plugin directory with selected components.

    Args:
        plugin_name: Plugin name in kebab-case
        path: Parent directory for the plugin
        components: List of component types to include

    Returns:
        Path to created plugin directory, or None if error
    """
    plugin_dir = Path(path).resolve() / plugin_name
    plugin_title = title_case_plugin_name(plugin_name)

    # Check if directory already exists
    if plugin_dir.exists():
        print(f"❌ Error: Directory already exists: {plugin_dir}")
        return None

    # Create base structure with manifest
    try:
        (plugin_dir / ".claude-plugin").mkdir(parents=True, exist_ok=False)
        print(f"✅ Created plugin directory: {plugin_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Write plugin.json manifest
    try:
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        manifest_path.write_text(MANIFEST_TEMPLATE.format(
            plugin_name=plugin_name,
            plugin_title=plugin_title
        ))
        print("✅ Created .claude-plugin/plugin.json")
    except Exception as e:
        print(f"❌ Error creating manifest: {e}")
        return None

    # Create requested components
    try:
        for comp in components:
            if comp == "commands":
                cmd_dir = plugin_dir / "commands"
                cmd_dir.mkdir(exist_ok=True)
                (cmd_dir / "example.md").write_text(COMMAND_TEMPLATE.format(
                    plugin_name=plugin_name,
                    plugin_title=plugin_title
                ))
                print("✅ Created commands/ with example command")

            elif comp == "agents":
                agent_dir = plugin_dir / "agents"
                agent_dir.mkdir(exist_ok=True)
                (agent_dir / f"{plugin_name}-agent.md").write_text(AGENT_TEMPLATE.format(
                    plugin_name=plugin_name,
                    plugin_title=plugin_title
                ))
                print(f"✅ Created agents/{plugin_name}-agent.md")

            elif comp == "skills":
                skill_name = f"{plugin_name}-skill"
                skill_title_inner = title_case_plugin_name(skill_name)
                skill_dir = plugin_dir / "skills" / skill_name
                skill_dir.mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text(SKILL_TEMPLATE.format(
                    plugin_name=plugin_name,
                    skill_title=skill_title_inner
                ))
                print(f"✅ Created skills/{skill_name}/SKILL.md")

            elif comp == "hooks":
                hooks_dir = plugin_dir / "hooks" / "scripts"
                hooks_dir.mkdir(parents=True, exist_ok=True)
                (plugin_dir / "hooks" / "hooks.json").write_text(
                    HOOKS_TEMPLATE.format(plugin_name=plugin_name)
                )
                hook_script = hooks_dir / "example-hook.sh"
                hook_script.write_text(HOOK_SCRIPT_TEMPLATE.format(
                    plugin_name=plugin_name
                ))
                hook_script.chmod(0o755)
                print("✅ Created hooks/ with hooks.json and example script")

            elif comp == "mcp":
                (plugin_dir / ".mcp.json").write_text(MCP_TEMPLATE.format(
                    plugin_name=plugin_name
                ))
                print("✅ Created .mcp.json")

            elif comp == "lsp":
                (plugin_dir / ".lsp.json").write_text(LSP_TEMPLATE.format(
                    plugin_name=plugin_name
                ))
                print("✅ Created .lsp.json")

            elif comp == "scripts":
                (plugin_dir / "scripts").mkdir(exist_ok=True)
                print("✅ Created scripts/")

            else:
                print(f"⚠️  Unknown component '{comp}', skipping")

    except Exception as e:
        print(f"❌ Error creating components: {e}")
        return None

    # Print next steps (maps to plugin-creator skill Steps 4-6)
    print(f"\n✅ Plugin '{plugin_name}' scaffolded at {plugin_dir}")
    print("\nNext steps:")
    print("1. Edit .claude-plugin/plugin.json to complete the TODO description and metadata")
    print("2. Implement components — replace TODO items in generated files")
    print("   See references/component-patterns.md for format specs and examples")
    print("3. For skills, invoke /skill-creator for the full skill methodology")
    print("4. Delete any example files not needed for your plugin")
    print(f"5. Test locally: claude --plugin-dir {plugin_dir}")
    print("6. Debug loading: claude --debug")

    return plugin_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: scaffold-plugin.py <plugin-name> --path <path> [--components <list>]")
        print("\nPlugin name requirements:")
        print("  - Kebab-case identifier (e.g., 'my-plugin')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 64 characters")
        print("  - Must match directory name exactly")
        print("\nComponents (comma-separated, default: all):")
        print(f"  {','.join(ALL_COMPONENTS)}")
        print("\nExamples:")
        print("  scaffold-plugin.py my-plugin --path ./plugins")
        print("  scaffold-plugin.py my-plugin --path . --components commands,hooks,mcp")
        sys.exit(1)

    plugin_name = sys.argv[1]
    path = sys.argv[3]

    # Parse optional --components
    components = list(ALL_COMPONENTS)
    i = 4
    while i < len(sys.argv):
        if sys.argv[i] == '--components' and i + 1 < len(sys.argv):
            components = [c.strip() for c in sys.argv[i + 1].split(',')]
            i += 2
        else:
            print(f"❌ Unknown option: {sys.argv[i]}")
            sys.exit(1)

    # Validate name
    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', plugin_name):
        print(f"❌ Error: '{plugin_name}' is not valid kebab-case")
        print("  Use lowercase letters, digits, and hyphens (e.g., 'my-plugin')")
        sys.exit(1)

    if len(plugin_name) > 64:
        print(f"❌ Error: Plugin name exceeds 64 characters")
        sys.exit(1)

    print(f"🔌 Scaffolding plugin: {plugin_name}")
    print(f"   Location: {path}")
    print(f"   Components: {', '.join(components)}")
    print()

    result = scaffold_plugin(plugin_name, path, components)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
