---
name: brain:init
description: Initialize Remember structure and configuration
user-invocable: true
---

# /brain:init - Initialize Remember

Creates the Second Brain directory structure, Persona file, and configures the `REMEMBER_BRAIN_PATH` env var in Claude settings.

## Usage

```
/brain:init
```

## Steps

### 1. Ask for Path

**Prompt user:**
```
Where should I create your Second Brain?

Default: ~/remember
Custom: Enter a full path (e.g., ~/Documents/my-brain)
```

If user presses Enter → use default `~/remember`
If user enters path → validate and use custom path

**Validate path:**
- Expand `~` to home directory
- Check if writable
- If exists, ask to confirm or choose different path

### 2. Detect Install Scope & Configure Settings

Detect whether the plugin is installed at user scope or project scope:
- If `${CLAUDE_PLUGIN_ROOT}` contains `/.claude/plugins/cache/` → **user scope** → settings file: `~/.claude/settings.json`
- Otherwise → **project scope** → settings file: `.claude/settings.json`

Also ask: **"Install globally or for this project?"** to let the user override the auto-detection.

**Read the target settings.json** (if it exists), then **MERGE** the following into it (don't overwrite existing keys):

```json
{
  "env": {
    "REMEMBER_BRAIN_PATH": "/chosen/path"
  },
  "permissions": {
    "additionalDirectories": ["/chosen/path"],
    "allow": [
      "Bash(ls /chosen/path*)",
      "Bash(find /chosen/path*)",
      "Bash(cat /chosen/path*)",
      "Bash(mkdir -p /chosen/path*)",
      "Bash(wc *)",
      "Bash(echo *)"
    ]
  }
}
```

**Note:** The path in Bash allow rules must be the expanded absolute path (not `~/`), because Bash rules match against the actual command string.

**Merge rules:**
- `env`: add/update the `REMEMBER_BRAIN_PATH` key, keep other env vars
- `permissions.additionalDirectories`: append the brain path if not already present, keep existing entries
- `permissions.allow`: append these Bash rules if not already present, keep existing entries
- All other keys: preserve unchanged

Write the merged JSON back to the settings file.

### 3. Create Directory Structure

```
{brain_path}/
├── Inbox/
├── Journal/
├── Projects/
├── Areas/
├── Notes/
├── People/
├── Tasks/
├── Resources/
├── Templates/
├── Archive/
└── Persona.md
```

```bash
mkdir -p {brain_path}/{Inbox,Journal,Projects,Areas,Notes,People,Tasks,Resources,Templates,Archive}
```

### 4. Create Persona.md

Ask user 3 questions:

1. **What's your name?** (default: User)
2. **What's your timezone?** (default: UTC)
3. **What languages do you speak?** (default: English)

Create `{brain_path}/Persona.md`:

```markdown
---
updated: {{date}}
tags: [persona, system]
---

# Persona

Best practices for working with {{name}}. Loaded at every session start. Updated by `/brain:process`.

---

## Identity

- **Name:** {{name}}
- **Timezone:** {{timezone}}
- **Languages:** {{languages}}

## Communication

_Patterns will be added as the AI learns your preferences._

## Workflow

_Patterns will be added as the AI learns your work style._

## Decision-Making

_Patterns will be added as the AI learns your decision patterns._

## Code Style

_Patterns will be added as the AI learns your coding preferences._

---

## Evidence Log

_Patterns observed across sessions. Newest first._

```

### 5. Create Tasks File

Create `{brain_path}/Tasks/tasks.md`:

```markdown
---
created: {{date}}
tags: [tasks, overview]
---

# Tasks Overview

Central hub for all tasks.
```

### 6. Create Templates

**`Templates/project.md`:**
```markdown
---
created: {{date}}
status: active
tags: [project]
related: []
---

# {{name}}

## Overview

## Goals
- [ ] Goal 1

## Log
### {{date}}
- Created project
```

**`Templates/person.md`:**
```markdown
---
created: {{date}}
tags: [person]
---

# {{name}}

## Who
- **Role:**
- **Relationship:**

## Interactions

### {{date}}
- [First interaction]
```

### 7. Initialize Git (Optional)

Ask: "Initialize git repository?"

If yes:
```bash
cd {brain_path}
git init
git add .
git commit -m "init: second brain"
```

Create `.gitignore`:
```
.DS_Store
.tmp/
```

### 8. Confirm

```
Second Brain initialized at {brain_path}/

Structure: Inbox, Journal, Projects, Areas, Notes, People, Tasks, Resources, Archive
Persona: Created (will learn your patterns over time)
Settings: REMEMBER_BRAIN_PATH and additionalDirectories written to {settings_file}
Templates: project, person

Next steps:
- Work normally in Claude Code — Persona loads every session
- Say "remember this: ..." to capture thoughts
- Run /brain:process to extract value from past sessions
```

## Error Handling

- If path already exists with content: skip existing dirs, only create missing ones
- If settings.json has existing content: merge, don't overwrite
- Safe to run multiple times (won't delete existing content)
