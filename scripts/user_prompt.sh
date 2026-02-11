#!/bin/bash
set -euo pipefail
# Remember - User Prompt Hook
# Detects brain dump keywords and injects routing instructions.
# Fires on every UserPromptSubmit. Persona loading is handled by SessionStart hook.

[ "${REMEMBER_PROCESSING:-}" = "1" ] && exit 0

# Read stdin
INPUT=$(cat)

# Resolve plugin root
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

# Get keywords from config and check for brain dump match
BRAIN_DUMP=$(python3 -c "
import json, sys
sys.path.insert(0, '${PLUGIN_ROOT}/scripts')
from config import load_config
cfg = load_config()
keywords = cfg['session']['brain_dump_keywords']
text = sys.stdin.read().lower()
print('true' if any(k in text for k in keywords) else 'false')
" <<< "$INPUT" 2>/dev/null)

[ "$BRAIN_DUMP" != "true" ] && exit 0

# Use shared config resolver
BRAIN_PATH=$(python3 "${PLUGIN_ROOT}/scripts/config.py" paths.data_root 2>/dev/null)
BRAIN_PATH="${BRAIN_PATH:-$HOME/remember}"
BRAIN_PATH="${BRAIN_PATH/#\~/$HOME}"

[ ! -d "$BRAIN_PATH" ] && exit 0

# Build the JSON output safely via Python
python3 -c "
import json, os, sys

brain_path = sys.argv[1]
plugin_root = sys.argv[2]
today = sys.argv[3]

# Gather brain structure
def ls_names(path, strip_ext=True, dirs_only=False):
    try:
        entries = os.listdir(path)
    except OSError:
        return 'none'
    if dirs_only:
        entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    if strip_ext:
        entries = [os.path.splitext(e)[0] for e in entries]
    return ', '.join(sorted(entries)) if entries else 'none'

people = ls_names(os.path.join(brain_path, 'People'))
projects = ls_names(os.path.join(brain_path, 'Projects'), strip_ext=False, dirs_only=True)
areas = ls_names(os.path.join(brain_path, 'Areas'))

# Read template
template_path = os.path.join(plugin_root, 'assets', 'templates', 'brain-dump-context.md')
try:
    with open(template_path, encoding='utf-8') as f:
        instructions = f.read().replace('{{TODAY}}', today)
except OSError:
    instructions = '(template missing)'

context = (
    f'BRAIN DUMP — Full processing instructions. Brain: {brain_path}. Today: {today}.\n\n'
    f'EXISTING: People: {people}. Projects: {projects}. Areas: {areas}.\n\n'
    f'{instructions}'
)

output = {
    'hookSpecificOutput': {
        'hookEventName': 'UserPromptSubmit',
        'additionalContext': context
    }
}

print(json.dumps(output, ensure_ascii=False))
" "$BRAIN_PATH" "$PLUGIN_ROOT" "$(date +%Y-%m-%d)"

exit 0
