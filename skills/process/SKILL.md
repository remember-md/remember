---
name: brain:process
description: Process unprocessed Claude sessions into your Second Brain
user-invocable: true
---

# /brain:process - Process Sessions into Second Brain

Reads unprocessed Claude Code transcripts and routes valuable content into your Second Brain.

## Usage

```
/brain:process
/brain:process --project impact3
```

## Steps

### 1. Resolve Brain Path

Read config from `~/.claude/plugin-config/remember/config.json` (user scope) or `.claude/plugin-config/remember/config.json` (project scope), falling back to `${CLAUDE_PLUGIN_ROOT}/config.defaults.json` → get `paths.data_root`.
Expand `~` to home directory. Use this as `{brain_path}`. If missing → tell user to run `/brain:init`.

### 2. Find Unprocessed Sessions

Run:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py --unprocessed
```

If `--project` argument was given:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py --unprocessed --project <name>
```

Show the list to the user and ask which sessions to process.
Options:
- **All** — process everything
- **Pick specific sessions** — user selects by number
- **Skip** — cancel

### 3. Extract Each Session

For each selected session, run:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py <transcript_path>
```

This outputs clean markdown with user messages and short assistant responses.

### 4. Read Current Brain Structure

List what exists to avoid duplicates:
```bash
ls {brain_path}/People/
ls {brain_path}/Projects/
ls {brain_path}/Notes/
ls {brain_path}/Journal/
ls {brain_path}/Tasks/tasks.md
```

### 5. Route Content Intelligently

**CRITICAL: Use session dates, NOT today's date.**
Each extracted session includes a `**Session date (use for journal/tasks):**` line. Use THAT date for all routing — journal file names, task dates, frontmatter `created`/`updated` fields, and people `last_contact`. You are often processing sessions from past days, so the current date is irrelevant.

Read the extracted content and route to the appropriate location:

| Content Type | Destination | Action |
|---|---|---|
| People mentioned (not casually) | `{brain_path}/People/{name}.md` | Create or append interaction (use session date) |
| Tasks / TODOs | `{brain_path}/Tasks/tasks.md` | Append new tasks (use session date) |
| Project work | `{brain_path}/Projects/{name}/{name}.md` | Update with activity (use session date) |
| Technical learnings | `{brain_path}/Notes/{topic}.md` | Create or update (use session date) |
| Daily summary | `{brain_path}/Journal/{SESSION_DATE}.md` | Create or update (file named by session date) |
| Decisions | `{brain_path}/Notes/decision-{topic}.md` | Create with context (use session date) |
| Area-related | `{brain_path}/Areas/{area}.md` | Append to relevant area (use session date) |

#### Date Rules

- **Journal**: File goes to `Journal/{SESSION_DATE}.md`, NOT `Journal/{TODAY}.md`. A session from Jan 15 goes into `Journal/2026-01-15.md`, even if you process it on Feb 9.
- **Tasks**: Include the session date when appending: `- [ ] Task description [[Projects/project|Context]] (2026-01-15)`
- **People**: Set `last_contact` to the session date, not today
- **Frontmatter**: `created` = session date (for new files), `updated` = session date (for existing files)
- **Multi-day sessions**: If a session spans multiple days (date headers in extract), route content to the day it occurred. Journal entries may need to go to multiple date files.

#### Routing Rules

**People** — Only create/update for meaningful interactions:
- Meetings, calls, discussions with named individuals
- NOT for casual mentions or names in code
- Update `last_contact` in frontmatter to session date, append to `## Interactions`

**Projects** — Match to existing projects when possible:
- Check `{brain_path}/Projects/` for existing project folders
- Update recent activity section
- Link to people involved

**Journal** — Group by project, not chronologically:
```markdown
## {Project Name}
- What was done
- Decisions made
- People: [[People/name]]
```

**Notes** — For technical insights, patterns, learnings:
- Use `{brain_path}/Notes/{descriptive-kebab-case}.md`
- Prefix decisions with `decision-`

**Tasks** — Append to `{brain_path}/Tasks/tasks.md`:
```markdown
- [ ] Task description [[Projects/project|Context]] (YYYY-MM-DD)
```

#### Linking Rules

**Obsidian handles backlinks automatically.** When you link `[[People/jay-hamilton]]` in a Journal entry, Obsidian shows that Journal entry in jay-hamilton's Backlinks panel. You do NOT need to manually create links in both directions.

**Rule: Link forward from where you write. Obsidian builds the web.**

Use `[[wikilinks]]` everywhere:
- `[[People/name]]` or `[[People/name|Display Name]]`
- `[[Projects/name/name|Project Name]]`
- `[[Notes/topic]]`

**When to write content in multiple files (not just links):**

Only update multiple files when you're adding **actual content** (not just a backlink):

| File | What to write (content, not just backlinks) |
|---|---|
| `People/name.md` | Meaningful interactions: `## Interactions` entries with context, update `last_contact` |
| `Projects/name/name.md` | Work log entries: `## Log` with what was done, decisions made |
| `Journal/{date}.md` | Daily summary grouped by project, with `[[wikilinks]]` to everything mentioned |
| `Notes/topic.md` | Technical learnings with `related:` in frontmatter |
| `Tasks/tasks.md` | New tasks with `[[Projects/name/name|Name]]` and date |
| `Persona.md` | New evidence line if behavioral pattern observed |

**Example — session about a meeting with Jay about Impact3:**
1. `Journal/{date}.md` → add section with `[[Projects/impact3/impact3|Impact3]]`, `[[People/jay-hamilton]]`, summary of what happened
2. `People/jay-hamilton.md` → update `last_contact`, add interaction entry (actual content about what was discussed)
3. `Projects/impact3/impact3.md` → add to `## Log` (actual work/decisions, not just a link)
4. `Tasks/tasks.md` → add action items with `[[Projects/impact3/impact3|Impact3]]`
5. `Persona.md` → add evidence if behavioral pattern observed

**Do NOT:** Go back to `People/jay-hamilton.md` to add `[[Journal/2026-02-09]]` — Obsidian shows that automatically in backlinks.

### 6. File Format

All files use YAML frontmatter + wikilinks. **Dates in frontmatter = session date, not today.**

```markdown
---
created: {SESSION_DATE}
updated: {SESSION_DATE}
tags: [tag1, tag2]
---

# Title

Content with [[wikilinks]].
```

When updating existing files:
- **Read the file first** to match existing style
- **Append** new content, don't replace
- **Update** `updated` in frontmatter to session date (only if session date is newer than existing `updated`)

### 7. Update Persona

**After routing content, check if sessions reveal behavioral patterns worth capturing.**

Read `{brain_path}/Persona.md` and scan the processed sessions for:
- User corrections (changed Claude's approach)
- Repeated workflows or habits
- Communication preferences
- Decision-making patterns
- Code style preferences

If a new pattern is observed:
1. **Reinforces existing pattern** → add a line to `## Evidence Log` with `[SESSION_DATE]` prefix
2. **New pattern** → add it to the appropriate section (Communication, Workflow, Decision-Making, Code Style) AND add evidence
3. **Contradicts existing pattern** → update the section to reflect the new preference, note the change in evidence

**Rules:**
- Only capture clear, meaningful patterns — skip routine/trivial behavior
- Keep the file concise — it's loaded every session start
- Update `updated:` in frontmatter to the most recent session date
- Evidence log: newest first, one line per observation

### 8. Mark Sessions as Processed

After successfully routing content from a session:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/extract.py --mark-processed <session_id>
```

### 9. Report Results

Show summary:
```
Brain updated from 3 sessions:

Created:
  - People/archie.md (new)
  - Notes/decision-second-brain-architecture.md (new)

Updated:
  - Journal/2026-02-09.md (+2 sections)
  - Projects/impact3/impact3.md (activity update)
  - Tasks/tasks.md (+1 task)
  - Persona.md (+2 evidence lines)

Processed sessions: 3
Remaining unprocessed: 12
```

## What to Capture vs Skip

**Capture:**
- Meaningful conversations about work, people, decisions
- Technical learnings and patterns
- Action items and tasks
- Project progress and status
- Strategic discussions

**Skip:**
- Routine code generation / debugging (too granular)
- Plugin installation and setup sessions
- Sessions that are mostly tool calls with little conversation
- System/meta messages

## Error Handling

- If extract.py fails → show error, skip that session, continue with others
- If a file write fails → warn user, continue with remaining routes
- If no unprocessed sessions → tell user, suggest using "remember this:" for immediate capture
