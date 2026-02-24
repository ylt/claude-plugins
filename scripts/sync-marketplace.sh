#!/usr/bin/env bash
set -euo pipefail

# SessionStart hook: pull latest plugins and re-register the marketplace.
# Runs silently — only prints on error.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

# Pull latest (fast-forward only, no editor, no merge commits)
git pull --ff-only --quiet 2>/dev/null || true

# Re-register marketplace and plugins
"$SCRIPT_DIR/register-marketplace.sh" >/dev/null
