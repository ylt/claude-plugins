#!/usr/bin/env bash
set -euo pipefail

# Register this marketplace in Claude Code settings.
# Adds the directory as an extraKnownMarketplace and enables all its plugins
# (skipping any already listed in enabledPlugins).
#
# Usage: ./scripts/register-marketplace.sh [settings-file]
#   settings-file  defaults to ~/.claude/settings.json

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
MARKETPLACE="$PROJECT_DIR/.claude-plugin/marketplace.json"
SETTINGS="${1:-$HOME/.claude/settings.json}"

if ! command -v jq &>/dev/null; then
  echo "error: jq is required" >&2
  exit 1
fi

if [[ ! -f "$MARKETPLACE" ]]; then
  echo "error: no marketplace.json at $MARKETPLACE" >&2
  exit 1
fi

if [[ ! -f "$SETTINGS" ]]; then
  echo "error: settings file not found: $SETTINGS" >&2
  exit 1
fi

MARKETPLACE_NAME="$(jq -r '.name' "$MARKETPLACE")"
PLUGIN_NAMES="$(jq -r '.plugins[].name' "$MARKETPLACE")"

if [[ -z "$MARKETPLACE_NAME" || "$MARKETPLACE_NAME" == "null" ]]; then
  echo "error: marketplace.json has no name" >&2
  exit 1
fi

echo "marketplace: $MARKETPLACE_NAME ($PROJECT_DIR)"
echo "settings:    $SETTINGS"
echo ""

# Build the jq filter
# 1. Ensure extraKnownMarketplaces exists and add/update our entry
# 2. Ensure enabledPlugins exists and add plugins not already listed
FILTER='
  .extraKnownMarketplaces //= {} |
  .extraKnownMarketplaces[$marketplace] = {
    "source": {
      "source": "directory",
      "path": $dir
    }
  } |
  .enabledPlugins //= {} |
  reduce $plugins[] as $p (
    .;
    if .enabledPlugins | has("\($p)@\($marketplace)") then . else
      .enabledPlugins["\($p)@\($marketplace)"] = true
    end
  )
'

# Convert plugin names to a JSON array for jq
PLUGINS_JSON="$(echo "$PLUGIN_NAMES" | jq -R . | jq -s .)"

RESULT="$(jq \
  --arg marketplace "$MARKETPLACE_NAME" \
  --arg dir "$PROJECT_DIR" \
  --argjson plugins "$PLUGINS_JSON" \
  "$FILTER" \
  "$SETTINGS")"

echo "$RESULT" > "$SETTINGS"

echo "registered marketplace \"$MARKETPLACE_NAME\""
echo ""
echo "plugins:"
for p in $PLUGIN_NAMES; do
  KEY="${p}@${MARKETPLACE_NAME}"
  STATUS="$(echo "$RESULT" | jq -r ".enabledPlugins[\"$KEY\"]")"
  echo "  $KEY = $STATUS"
done

# Register sync-marketplace.sh as a SessionStart hook if not already present
SYNC_SCRIPT="$SCRIPT_DIR/sync-marketplace.sh"
if [[ -x "$SYNC_SCRIPT" ]]; then
  HOOK_CMD="$SYNC_SCRIPT"
  ALREADY="$(jq -r \
    --arg cmd "$HOOK_CMD" \
    '[.hooks.SessionStart // [] | .[].hooks[]? | select(.command == $cmd)] | length' \
    "$SETTINGS")"

  if [[ "$ALREADY" == "0" ]]; then
    RESULT="$(jq \
      --arg cmd "$HOOK_CMD" \
      '.hooks.SessionStart //= [] |
       .hooks.SessionStart += [{
         "hooks": [{"type": "command", "command": $cmd}]
       }]' \
      "$SETTINGS")"
    echo "$RESULT" > "$SETTINGS"
    echo ""
    echo "added SessionStart hook: $HOOK_CMD"
  fi
fi
