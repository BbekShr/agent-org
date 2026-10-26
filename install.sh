#!/usr/bin/env bash
# Install agent-org's skills into ~/.claude/skills (for use without the plugin system).
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/skills"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"
for s in org-init org-doctor org-eval org-feedback; do
  if [ -e "$DEST/$s" ]; then echo "skip $s: $DEST/$s already exists (remove it to reinstall)"; continue; fi
  cp -R "$SRC/$s" "$DEST/$s" && echo "installed $s -> $DEST/$s"
done
