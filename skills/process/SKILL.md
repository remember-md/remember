---
name: brain:process
description: Process unprocessed Claude sessions into your Second Brain
user-invocable: true
---

# /brain:process — Process Sessions into Second Brain

Reads unprocessed Claude Code transcripts and routes valuable content into your Second Brain using a knowledge-aware pipeline.

## ⚠️ MANDATORY: Built-in Tools Only (NO Bash for file ops!)

| Operation | ✅ Use This | ❌ NOT This |
|-----------|------------|-------------|
| List files | `LS` tool | `bash ls` |
| Find files | `Glob` tool | `bash find` |
| Search content | `Grep` tool | `bash grep` |
| Read files | `Read` tool | `bash cat` |
| Create files | `Write` tool | `bash echo >` |
| Update files | `Edit` tool (old_string → new_string) | `bash sed` / rewrite |
| Count files | `Glob` tool + count | `bash wc` |

**Only use bash for:** running Python scripts (`extract.py`, `build_index.py`).

---

## Step 1: Resolve Brain Path & Build Knowledge Index

1. Read `$REMEMBER_BRAIN_PATH` env var (fallback `~/remember`). Call this `{brain}`.
2. If directory doesn't exist → tell user to run `/brain:init` and stop.
3. Run the knowledge index:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_index.py
   ```
4. **Read the output carefully.** This is your map of everything that exists. Use it throughout all remaining steps to prevent duplicates and enable smart linking.

---

## Step 1b: Load User Instructions

Read `{brain}/REMEMBER.md` if it exists. This contains explicit preferences for:
- **Capture Rules** — what to always/never capture
- **Processing** — routing overrides, output style, tagging rules
- **Custom Types** — entity types beyond standard PARA
- **Connections** — auto-linking rules, people context
- **Templates** — overrides for Journal, People, etc.

**These instructions take precedence over default routing in Step 4.**

If REMEMBER.md says "Never capture X" → skip X even if normally captured.
If it says "Route Y to Z" → route to Z even if defaults say otherwise.
If it defines a Custom Type → create files matching that specification.

---

## Step 2: Find Unprocessed Sessions

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py --unprocessed
```

With project filter:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py --unprocessed --project <name>
```

Show the list. Ask user which to process: **All**, **specific sessions by number**, or **Skip**.

---

## Step 3: Extract Each Session

For each selected session:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py <transcript_path>
```

Note the `**Session date (use for journal/tasks):**` line — use THAT date for everything (journal filenames, frontmatter, last_contact, task dates). Never use today's date.

---

## Step 4: Process Each Session

For each extracted session, do sub-steps 4a through 4e **with the knowledge index in context**.

### 4a. Build Resolution Map

For every name, project, topic, or reference in the session, resolve it:

| Reference in session | Resolution | Action |
|---------------------|------------|--------|
| Matches existing person | `People/{existing-file}.md` | **Edit** (update) |
| Matches existing project | `Projects/{existing}/` | **Edit** (update) |
| Matches existing note | `Notes/{existing}.md` | **Edit** (update) |
| Matches existing area | `Areas/{existing}.md` | **Edit** (update) |
| New person | `People/{new-name}.md` | **Write** (create) |
| New project | `Projects/{new}/` | **Write** (create) |
| New topic/learning | `Notes/{new-topic}.md` | **Write** (create) |

**Fuzzy matching:** "John", "john smith", "John S." all resolve to `People/john-smith.md` if it exists. Check the knowledge index!

### 4b. Classify Content (with User Instructions)

Before classifying, check REMEMBER.md:
1. **Capture Rules** → apply Always/Never filters FIRST
2. **Processing → Routing Overrides** → apply before default routing table
3. **Custom Types** → check if content matches user-defined type
4. Then fall through to default classification table

Read the session and classify every piece of valuable content:

| Category | What to look for | Destination |
|----------|-----------------|-------------|
| **Decisions** | "We decided...", "Going with...", chose X over Y | `Notes/decision-{topic}.md` |
| **Commitments** | "I'll do X by Friday", promises with owners/deadlines | `Tasks/tasks.md` + link |
| **Tasks** | "Need to...", "TODO", "trebuie să..." | See Task Routing below |
| **Learnings** | "TIL", insights, patterns discovered, "am învățat că..." | `Notes/{topic}.md` |
| **People interactions** | Meetings, calls, discussions with named people | `People/{name}.md` |
| **Project updates** | Work done, progress, status changes | `Projects/{name}/{name}.md` |
| **Area updates** | Health habits, career moves, family events, finances | `Areas/{area}.md` |
| **Resources/URLs** | External links shared | `Resources/{type}/{title}.md` |
| **Behavioral patterns** | Corrections, preferences, repeated workflows | `Persona.md` |

**Skip:** routine code generation, debugging noise, tool call chatter, system messages.

### 4c. Update EXISTING Files (Edit Tool)

**For files that already exist, use the `Edit` tool for surgical updates. Do NOT rewrite the whole file.**

#### People — Update Interaction Log
```
Read People/{name}.md first.
Use Edit tool:
  old_string: (last line of ## Interactions or ## Interaction Log section)
  new_string: (that line + new interaction entry)

Also update last_contact in frontmatter:
  old_string: "last_contact: 2026-01-15"
  new_string: "last_contact: {SESSION_DATE}"
```

#### Projects — Update Log
```
Read Projects/{name}/{name}.md first.
Find the ## Log section, add entry:
  old_string: "## Log\n"  (or last log entry)
  new_string: "## Log\n\n### {SESSION_DATE}\n- {what was done}\n"
```

#### Journal — Append Sections
```
If Journal/{SESSION_DATE}.md exists, read it first.
Use Edit to append new project sections.
If it doesn't exist, use Write (see 4d).
```

#### Tasks — Add to Correct Section
```
Read Tasks/tasks.md first.
Find ## Focus or ## Next Up section.
Use Edit to insert new task after section header.
```

#### Areas — Append Content
```
Read Areas/{area}.md. Find relevant section.
Use Edit to append new content to that section.
```

**Always update frontmatter `updated:` field to SESSION_DATE (only if newer than existing).**

### 4d. Create NEW Files (Write Tool)

When creating new files, check REMEMBER.md `## Templates` section:
- If user defined a template override → use their template
- Otherwise → use default from `assets/templates/`

For new entities, use the `Write` tool with proper templates:

#### New Person
```markdown
---
created: {SESSION_DATE}
updated: {SESSION_DATE}
tags: [person]
role: {role if known}
organization: {org if known}
last_contact: {SESSION_DATE}
related: []
---

# {Person Name}

{Brief description from session context}

## Who
- **Role:** {role}
- **Context:** {how they came up}

## Notes to Remember
- {key things mentioned}

## Interactions

### {SESSION_DATE}
- {what happened/was discussed}
```

#### New Project
```markdown
---
created: {SESSION_DATE}
status: active
tags: [project]
related: []
---

# {Project Name}

## Overview
{from session context}

## Tasks
### Active
- [ ] {tasks from session}

## Log
### {SESSION_DATE}
- Project created from session context
- {details}
```

#### New Note
```markdown
---
created: {SESSION_DATE}
updated: {SESSION_DATE}
tags: [{topic-tags}]
related: [{wikilinks to related entities}]
---

# {Topic Title}

{Content — insight, learning, decision rationale}

## Related
- [[Projects/{related}]] — context
- [[People/{related}]] — who was involved
```

#### New Journal Entry
```markdown
---
created: {SESSION_DATE}
tags: [journal]
---

# {SESSION_DATE}

## {Project/Topic Name}
- {What happened}
- Discussed with [[People/{name}]]
- Decision: {what was decided}
- See [[Notes/{related-note}]]
```

**Use [[wikilinks]] everywhere.** Link forward; Obsidian handles backlinks.

### 4e. Update Persona.md — Behavioral Pattern Detection

**After all content is routed**, analyze the session for patterns. This is semantic analysis — understand intent, don't keyword-match.

**What to detect:**

1. **User corrections** — User changed your approach, rejected a suggestion, said "no, do it this way"
   → What do they actually prefer?

2. **Stated preferences** — "I prefer X", "Never use Z", "Always do W", "prefer", "mai bine cu"
   → Record the preference explicitly

3. **Repeated workflows** — Same sequence appears again, "I always...", "usually I..."
   → Document the workflow

4. **Communication style** — Concise vs detailed, formal vs casual, language switching (EN↔RO)
   → Note style signals

5. **Decision criteria** — What they prioritize (speed vs quality, simplicity vs features)
   → Record decision patterns

6. **Code/technical style** — Naming conventions, frameworks, architecture preferences
   → Add to code style section

**How to update Persona.md:**

1. **Read current Persona.md** first
2. If pattern **reinforces existing** → add evidence line:
   ```
   - [{SESSION_DATE}] User again preferred X over Y (context: Z)
   ```
3. If **new pattern** → add to appropriate section + evidence
4. If **contradicts existing** → update section, note the change
5. Update frontmatter `updated:` to SESSION_DATE

**Skip if:** no clear patterns found. Better to miss than hallucinate.

---

## Step 5: Mark Processed & Report

### Mark each session:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py --mark-processed <session_id>
```

### Report summary:
```
Brain updated from {N} sessions:

Created:
  - People/john-smith.md (new)
  - Notes/decision-api-architecture.md (new)

Updated:
  - Journal/2026-02-09.md (+2 sections)
  - Projects/myproject/myproject.md (log entry)
  - Tasks/tasks.md (+3 tasks: 1 Focus, 2 Next Up)
  - Persona.md (+2 evidence lines)

Processed: {N} sessions
Remaining unprocessed: {M}
```

---

## Task Routing Intelligence

Classify tasks semantically (understand urgency in any language):

| Urgency | Signals | Destination | Limit |
|---------|---------|-------------|-------|
| **URGENT** | Deadline this week, someone waiting, "asap", "urgent", "de mâine", "azi" | `Tasks/tasks.md` → ## Focus | 10 |
| **IMPORTANT** | Clear action, no deadline, "trebuie să", "need to", "should" | `Tasks/tasks.md` → ## Next Up | 15 |
| **BACKLOG** | Future work, "Phase 2", "eventually", "eventual", "când am timp" | `Projects/{name}/{name}.md` → ## Tasks/Backlog | ∞ |

**Format:** `- [ ] Task description [[Projects/name/name|Name]] [⚡ if urgent] ({SESSION_DATE})`

**Rules:**
- Never duplicate between tasks.md and project files
- Ambiguous → default to IMPORTANT
- Focus full (10) → push to Next Up
- Next Up full (15) → push to Backlog + journal note

---

## Date Rules (Critical!)

- **Journal filename:** `Journal/{SESSION_DATE}.md` — NOT today
- **Frontmatter created:** SESSION_DATE (new files)
- **Frontmatter updated:** SESSION_DATE (if newer than existing)
- **People last_contact:** SESSION_DATE
- **Task dates:** SESSION_DATE for traceability
- **Multi-day sessions:** Route content to the day it occurred

---

## Areas Intelligence

| Question | YES → | NO → |
|----------|-------|------|
| Time-bound with deadline? | Project | Continue |
| Ongoing responsibility? | Area | Note (one-off) |

Default areas: `career.md`, `health.md`, `family.md`, `finances.md`
Areas are **flat files** — one `.md` per area, no subfolders.

---

## Resource Capture (URLs)

When session contains URLs:
1. Fetch metadata: `web_fetch(url)` → title, author, summary
2. Classify: article, tool, video, book, docs
3. Create `Resources/{type}/{title}.md` with frontmatter + summary + key takeaways
4. Auto-link to related Projects/Notes
5. If fetch fails → create minimal note with URL, flag for review

---

## Linking Rules

- Use `[[wikilinks]]` everywhere: `[[People/name]]`, `[[Projects/name/name|Display]]`, `[[Notes/topic]]`
- **Link forward only** — Obsidian handles backlinks
- Write actual content in multiple files only when adding real information (not just backlinks)
- In frontmatter: `related: ["[[Notes/topic]]", "[[Projects/name/name]]"]`

---

## Error Handling

- extract.py fails → show error, skip session, continue with others
- File write fails → warn user, continue with remaining
- No unprocessed sessions → tell user, suggest "remember this:" for immediate capture
- web_fetch fails → create minimal resource note, flag for review
