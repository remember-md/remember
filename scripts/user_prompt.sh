#!/bin/bash
set -euo pipefail
# Remember - User Prompt Hook
# Detects brain dump keywords and injects routing instructions.

[ "${REMEMBER_PROCESSING:-}" = "1" ] && exit 0

# Read stdin
INPUT=$(cat)

# Resolve paths
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
BRAIN_PATH="${REMEMBER_BRAIN_PATH:-$HOME/remember}"

[ ! -d "$BRAIN_PATH" ] && exit 0

# Single Python call: check keywords + build JSON output
python3 -c "
import json, os, sys

input_text = sys.stdin.read().lower()
brain_path = sys.argv[1]
plugin_root = sys.argv[2]
today = sys.argv[3]

# Load keywords from config
defaults_file = os.path.join(plugin_root, 'config.defaults.json')
try:
    with open(defaults_file) as f:
        cfg = json.load(f)
    keywords = cfg['session']['brain_dump_keywords']
except Exception:
    keywords = ['save this', 'remember this', 'brain dump', 'note to self',
                'capture this', 'save to brain', 'write to brain', 'add to brain',
                'salvează', 'notează', 'reține']

if not any(k in input_text for k in keywords):
    sys.exit(0)

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

# Build compact knowledge index
import subprocess
index_script = os.path.join(plugin_root, 'scripts', 'build_index.py')
try:
    result = subprocess.run(
        ['python3', index_script, '--compact'],
        capture_output=True, text=True, timeout=5,
        env={**os.environ, 'REMEMBER_BRAIN_PATH': brain_path}
    )
    compact_index = result.stdout.strip()
except Exception:
    compact_index = f'People: {people}. Projects: {projects}. Areas: {areas}.'

# Read template
template_path = os.path.join(plugin_root, 'assets', 'templates', 'brain-dump-context.md')
try:
    with open(template_path, encoding='utf-8') as f:
        instructions = f.read().replace('{{TODAY}}', today)
except OSError:
    instructions = '(template missing)'

# Load REMEMBER.md capture/processing sections (NEW)
remember_file = os.path.join(brain_path, 'REMEMBER.md')
remember_context = ''
if os.path.isfile(remember_file):
    import re
    with open(remember_file, encoding='utf-8') as rf:
        remember_text = rf.read()

    sections_to_extract = ['Capture Rules', 'Processing', 'Custom Types', 'Language']
    extracted = []
    for section_name in sections_to_extract:
        pattern = rf'^## {re.escape(section_name)}\s*\n(.*?)(?=^## |\Z)'
        match = re.search(pattern, remember_text, re.MULTILINE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            if content:  # Skip empty sections
                extracted.append(f'## {section_name}\n{content}')

    if extracted:
        remember_context = (
            '\n\nUSER OVERRIDES (these take precedence over defaults above):\n'
            + '\n\n'.join(extracted)
        )

context = (
    f'BRAIN DUMP — Full processing instructions. Brain: {brain_path}. Today: {today}.\n\n'
    f'{compact_index}\n\n'
    f'{instructions}'
    f'{remember_context}'
)

output = {
    'hookSpecificOutput': {
        'hookEventName': 'UserPromptSubmit',
        'additionalContext': context
    }
}

print(json.dumps(output, ensure_ascii=False))
" "$BRAIN_PATH" "$PLUGIN_ROOT" "$(date +%Y-%m-%d)" <<< "$INPUT"

exit 0
