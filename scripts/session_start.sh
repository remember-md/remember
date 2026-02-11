#!/bin/bash
set -euo pipefail
# Remember - Session Start Hook
# Loads Persona.md into Claude's context at the start of every session.
# Fires once on SessionStart. Stdout is injected as model-visible context.

# Resolve plugin root
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

# Use shared config resolver
BRAIN_PATH=$(python3 "${PLUGIN_ROOT}/scripts/config.py" paths.data_root 2>/dev/null)
BRAIN_PATH="${BRAIN_PATH:-$HOME/remember}"
BRAIN_PATH="${BRAIN_PATH/#\~/$HOME}"

[ ! -d "$BRAIN_PATH" ] && exit 0

# Load Persona
PERSONA=""
[ -f "$BRAIN_PATH/Persona.md" ] && PERSONA=$(cat "$BRAIN_PATH/Persona.md")
[ -z "$PERSONA" ] && exit 0

cat <<EOF
REMEMBER BRAIN LOADED. Brain: ${BRAIN_PATH}

PERSONA (apply throughout session):
${PERSONA}

Commands: /brain:process, /brain:status, 'remember this: ...'
EOF

exit 0
