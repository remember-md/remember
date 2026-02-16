---
name: remember
description: >
  Your personal knowledge repository — capture, organize, and retrieve everything using PARA + Zettelkasten.
  Triggers on: "save this", "remember", "note", "capture", "brain dump".
  Process past sessions with /brain:process. Stores everything as .md files in a Git repo for Obsidian.
---

# Remember — Brain Dump Skill

Immediate capture: when the user says "remember this", "save this", "brain dump", etc., route content to the right place in the Second Brain.

## ⚠️ MANDATORY: Built-in Tools Only (NO Bash for file ops!)

| Operation | ✅ Use This | ❌ NOT This |
|-----------|------------|-------------|
| List files | `LS` tool | `bash ls` |
| Find files | `Glob` tool | `bash find` |
| Search content | `Grep` tool | `bash grep` |
| Read files | `Read` tool | `bash cat` |
| Create files | `Write` tool | `bash echo >` |
| Update files | `Edit` tool (old_string → new_string) | `bash sed` / rewrite |

**Only use bash for:** running `build_index.py`.

---

## Brain Dump Pipeline

### Step 1: Get Knowledge Index

Run:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_index.py --compact
```

This tells you what already exists (People, Projects, Areas, Notes, Tasks counts). **Use this to prevent duplicates and enable smart linking.**

### Step 1b: Check REMEMBER.md

Read `{brain}/REMEMBER.md` if it exists. Apply Capture Rules and Processing
instructions throughout all steps. User instructions override defaults.

### Step 2: Parse User Input

Extract structured data from the conversational input:

| Look for | Example | Extract |
|----------|---------|---------|
| Person name | "met with John about..." | Person: John → check if `People/john.md` exists |
| Project reference | "for the website project..." | Project → resolve to existing `Projects/website/` |
| Task/action item | "need to deploy by Friday" | Task + deadline → urgency classification |
| Decision | "decided to go with Next.js" | Decision + rationale |
| Learning/insight | "learned that async..." | Topic + content |
| Area update | "started running again" | Area: health |
| URL | "check out https://..." | Resource + metadata |

### Step 3: Build Resolution Map

For every name/reference, resolve against the knowledge index:

- **Matches existing entity** → will use `Edit` tool to update
- **New entity** → will use `Write` tool to create
- **Ambiguous** → ask user for clarification

**Fuzzy matching:** "John", "john smith", "John S." → `People/john-smith.md` if exists in index.

### Step 4: Route & Write

#### For EXISTING files → Use `Edit` tool

**People — add interaction:**
```
Read People/{name}.md first.
Edit tool:
  old_string: (last entry in ## Interactions)
  new_string: (last entry + new interaction)
Update last_contact in frontmatter.
```

**Projects — add log/task:**
```
Read Projects/{name}/{name}.md.
Edit tool to append to ## Log or ## Tasks section.
```

**Tasks — add to section:**
```
Read Tasks/tasks.md.
Edit tool to insert after ## Focus or ## Next Up header.
```

**Areas — append content:**
```
Read Areas/{area}.md.
Edit tool to append to relevant section.
```

**Journal — add section:**
```
Read or create Journal/{TODAY}.md.
Edit/Write to add project section.
```

#### For NEW files → Use `Write` tool

**New Person:**
```markdown
---
created: {TODAY}
updated: {TODAY}
tags: [person]
role: {if known}
last_contact: {TODAY}
related: []
---

# {Name}

{Context from user input}

## Who
- **Role:** {role}
- **Context:** {how they relate}

## Notes to Remember
- {key info}

## Interactions

### {TODAY}
- {what user said}
```

**New Note/Decision:**
```markdown
---
created: {TODAY}
updated: {TODAY}
tags: [{topic-tags}]
related: [{wikilinks}]
---

# {Title}

{Content}
```

**New Project:**
```markdown
---
created: {TODAY}
status: active
tags: [project]
related: []
---

# {Project Name}

## Overview
{from user input}

## Tasks
### Active
- [ ] {any tasks mentioned}

## Log
### {TODAY}
- Project created
```

### Step 5: Link Entities

Use `[[wikilinks]]` in all content:
- `[[People/name]]` or `[[People/name|Display Name]]`
- `[[Projects/name/name|Project Name]]`
- `[[Notes/topic]]`

**Link forward only** — Obsidian handles backlinks automatically.

In frontmatter: `related: ["[[Notes/topic]]", "[[Projects/name/name]]"]`

### Step 6: Confirm

Report briefly (one line per file):
```
✅ Brain updated:
  - Updated People/john-smith.md (+interaction)
  - Created Notes/decision-nextjs.md
  - Updated Tasks/tasks.md (+1 Focus)
  - Updated Journal/2026-02-15.md (+1 section)
```

---

## Task Routing

| Urgency | Signals | Destination |
|---------|---------|-------------|
| **URGENT** | Deadline soon, "asap", "urgent", "de mâine" | `Tasks/tasks.md` → ## Focus (max 10) |
| **IMPORTANT** | "Need to", "trebuie să", no deadline | `Tasks/tasks.md` → ## Next Up (max 15) |
| **BACKLOG** | "Eventually", "Phase 2", "când am timp" | `Projects/{name}/{name}.md` → Backlog |

Format: `- [ ] Task [[Projects/name/name|Name]] [⚡ if urgent] ({DATE})`

---

## Content Type → Destination

| Content | Destination |
|---------|-------------|
| Person interaction | `People/{name}.md` |
| Task with deadline | `Tasks/tasks.md` (Focus) |
| Task without deadline | `Tasks/tasks.md` (Next Up) |
| Future/roadmap task | `Projects/{name}/{name}.md` |
| Project update | `Projects/{name}/{name}.md` |
| Decision | `Notes/decision-{topic}.md` |
| Learning/insight | `Notes/{topic}.md` |
| Area update | `Areas/{area}.md` |
| URL/resource | `Resources/{type}/{title}.md` |
| Unclear | `Inbox/{topic}.md` |

---

## Areas Intelligence

- Time-bound + deadline → Project
- Ongoing responsibility → Area (flat .md file)
- One-off insight → Note

Default areas: `career.md`, `health.md`, `family.md`, `finances.md`

---

## Resource Capture (URLs)

1. `web_fetch(url)` → title, summary
2. Create `Resources/{type}/{title}.md` with frontmatter + summary
3. Link to related entities
4. If fetch fails → minimal note with URL

---

## File Naming

- Folders: `kebab-case/`
- Files: `kebab-case.md`
- People: `firstname.md` or `firstname-lastname.md`
- Dates: `YYYY-MM-DD.md`

---

## Commands Reference

| Command | Action |
|---------|--------|
| `/brain:init` | Initialize brain structure |
| `/brain:process` | Process past sessions |
| `/brain:status` | Show brain stats |
| "remember this: X" | Immediate brain dump (this skill) |
| "save this: X" | Immediate brain dump (this skill) |
