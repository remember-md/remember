---
name: brain:init
description: Initialize BrainRepo structure and configuration
---

# /brain:init - Initialize BrainRepo

Creates the BrainRepo directory structure and sets up your Second Brain.

## Usage

```
/brain:init
```

## What it does

### 1. Ask for Path

**Prompt user:**
```
🧠 BrainRepo Initialization

Where should I create your Second Brain?

Default: ~/supabrain
Custom: Enter full path (e.g., ~/Documents/my-brain)

Path: ___
```

If user presses Enter → use default `~/supabrain`  
If user enters path → validate and use custom path

**Validate path:**
- Expand `~` to home directory
- Check if writable
- If exists, ask to confirm or choose different path

### 1b. Update Config

Write chosen path to `~/.claude/plugins/supabrain/config.json`:

```json
{
  "paths": {
    "data_root": "/chosen/path"    // ⬅️ User's choice
  }
}
```

This ensures all future commands use the same path.

### 2. Create Directory Structure

```bash
mkdir -p ~/supabrain/
├── content/
│   ├── Inbox/
│   ├── Projects/
│   ├── People/
│   ├── Areas/
│   ├── Notes/
│   │   └── Meta/
│   ├── Resources/
│   ├── Journal/
│   ├── Tasks/
│   ├── Archive/
│   └── Templates/
│       ├── project.md
│       ├── person.md
│       ├── area.md
│       ├── note.md
│       └── journal.md
├── learning/
│   ├── observations/
│   │   ├── current.jsonl
│   │   └── archive/
│   ├── instincts/
│   │   ├── personal/
│   │   │   ├── code-style/
│   │   │   ├── workflow/
│   │   │   ├── communication/
│   │   │   └── decision-making/
│   │   └── inherited/
│   ├── evolved/
│   │   ├── skills/
│   │   ├── agents/
│   │   └── commands/
│   └── meta/
│       ├── identity.json
│       ├── stats.json
│       └── clustering-flags.json
└── README.md
```

### 3. Create Identity

Ask user questions to create `identity.json`:

**Questions:**
1. What's your name? (default: User)
2. Technical level? (technical / semi-technical / non-technical / chaotic)
3. Preferred language? (Romanian / English / Both)

**Create `learning/meta/identity.json`:**
```json
{
  "name": "User",
  "technical_level": "technical",
  "language": "Romanian",
  "sessions_count": 0,
  "first_session": "2026-02-08",
  "last_session": "2026-02-08",
  "clustering_flags": {}
}
```

### 4. Create Templates

**`content/Templates/project.md`:**
```yaml
---
created: {{date}}
status: active
tags: [project]
---

# {{name}}

## Overview
[Project description]

## Status
- **Created:** {{date}}
- **Last Active:** {{date}}
- **Status:** Active

## Tech Stack
- [Technology 1]
- [Technology 2]

## Recent Activity

## People
- [[People/name|Name]] - Role

## Related
- [[Areas/domain|Domain]]

## Decisions
See: [[Projects/{{name}}/decisions|Decisions Log]]
```

**`content/Templates/person.md`:**
```yaml
---
created: {{date}}
tags: [person]
last_contact: {{date}}
---

# {{name}}

## Info
- **Relationship:** [How you know them]
- **Context:** [Relevant context]

## Interactions

### {{date}}
[First interaction]

## Related
- [[Projects/project|Project]] - Collaborates on
```

**`content/Templates/journal.md`:**
```yaml
---
date: {{date}}
tags: [journal]
---

# {{date}}

## Sessions

### Session 1 (HH:MM)
**Project:** [[Projects/project|Project]]

**Activity:**
- [What was done]

**People:**
- [[People/name|Name]] - [Context]

**Decisions:**
- [Decision made]

## Captures
- [[Inbox/item|Item]]

## Insights
[Reflections]
```

Create similar templates for area.md and note.md.

### 5. Initialize Git (Optional)

Ask: "Initialize git repository?"

If yes:
```bash
cd ~/supabrain
git init
git add .
git commit -m "feat: initialize BrainRepo"
```

Create `.gitignore`:
```
learning/observations/current.jsonl
learning/observations/archive/
.DS_Store
```

### 6. Create README

**`README.md`:**
```markdown
# 🧠 BrainRepo

Your extended Second Brain that learns as you work in Claude Code.

## What is this?

A hybrid PARA + Zettelkasten system with automatic population and pattern learning.

## Structure

- `content/` - Your Second Brain (Projects, People, Notes, Journal)
- `learning/` - Meta-learning (observations, instincts, evolved skills)

## Usage

Work normally in Claude Code. BrainRepo:
- Auto-populates Projects/, People/, Journal/
- Learns your workflow patterns
- Evolves into optimized skills

## Commands

- `/brain:status` - View learning stats
- `/brain:evolve` - Trigger evolution when ready
- `/brain:export` - Share learned patterns
- `/brain:import` - Adopt patterns from others

## Getting Started

Just work! The brain-curator agent runs in background and maintains everything.

Check `content/Journal/` daily to see what was captured.

---

Created: {{date}}
Plugin: supabrain v1.0.0
```

### 7. Confirm Success

Return message:
```
✅ BrainRepo initialized at ~/supabrain/

Structure created:
- content/ (Second Brain)
- learning/ (Meta-learning)
- Templates ready
- Identity configured

Next: Just work in Claude Code!
The brain-curator will maintain your Second Brain automatically.

Commands:
- /brain:status - Check stats
- /brain:evolve - Evolve patterns (when 5+ cluster)
```

## Error Handling

- If `~/supabrain/` already exists: ask to confirm overwrite or skip
- If custom path not writable: suggest alternative
- If templates fail: create minimal versions

## Notes

- Only needs to run **once** ever (unless resetting)
- Can re-run to add missing folders
- Safe to run multiple times (won't delete existing content)
