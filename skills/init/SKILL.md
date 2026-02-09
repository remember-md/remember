---
name: brain:init
description: Initialize Remember structure and configuration
user-invocable: true
---

# /brain:init - Initialize Remember

Creates the Second Brain directory structure, Persona file, and configures permissions.

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

### 2. Save Config

Determine config location based on install scope:
- If installed at **user scope** (default) → `~/.claude/plugin-config/remember/config.json`
- If installed at **project scope** → `.claude/plugin-config/remember/config.json`

To detect scope: if `${CLAUDE_PLUGIN_ROOT}` contains `/.claude/plugins/cache/`, it's user scope. Otherwise, check if it's under a project directory for project scope.

Create the directory and write the config:

```bash
mkdir -p ~/.claude/plugin-config/remember
```

```json
{
  "paths": {
    "data_root": "/chosen/path"
  }
}
```

This location persists across plugin updates (it's outside the plugin cache).

### 3. Add Permissions

Add read/write permissions for the brain path to `~/.claude/settings.json` so the plugin can access files without prompting every time.

Read `~/.claude/settings.json`, add to `permissions.allow`:

```json
{
  "permissions": {
    "allow": [
      "Read(//{brain_path}/**)",
      "Edit(//{brain_path}/**)"
    ]
  }
}
```

**Important:** Use double-slash `//` prefix for absolute paths. Merge with existing permissions, don't overwrite.

### 4. Create Directory Structure

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

### 5. Create Persona.md

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

### 6. Create Tasks File

Create `{brain_path}/Tasks/tasks.md`:

```markdown
---
created: {{date}}
tags: [tasks, overview]
---

# Tasks Overview

Central hub for all tasks.
```

### 7. Create Templates

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

### 8. Initialize Git (Optional)

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

### 9. Confirm

```
Second Brain initialized at {brain_path}/

Structure: Inbox, Journal, Projects, Areas, Notes, People, Tasks, Resources, Archive
Persona: Created (will learn your patterns over time)
Permissions: Read/Edit auto-allowed for brain path
Templates: project, person

Next steps:
- Work normally in Claude Code — Persona loads every session
- Say "remember this: ..." to capture thoughts
- Run /brain:process to extract value from past sessions
```

## Error Handling

- If path already exists with content: skip existing dirs, only create missing ones
- If settings.json has existing permissions: merge, don't overwrite
- Safe to run multiple times (won't delete existing content)
