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
/brain:process --project myproject
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
ls {brain_path}/Areas/
```

### 5. Route Content Intelligently

**CRITICAL: Use session dates, NOT today's date.**
Each extracted session includes a `**Session date (use for journal/tasks):**` line. Use THAT date for all routing — journal file names, task dates, frontmatter `created`/`updated` fields, and people `last_contact`. You are often processing sessions from past days, so the current date is irrelevant.

Read the extracted content and route to the appropriate location:

| Content Type | Destination | Action |
|---|---|---|
| People mentioned (not casually) | `{brain_path}/People/{name}.md` | Create or append interaction (use session date) |
| Tasks / TODOs | See Task Routing Intelligence below | Route based on urgency |
| Project work (general) | `{brain_path}/Projects/{name}/{name}.md` | Update with activity (use session date) |
| Meeting notes | `{brain_path}/Projects/{name}/Meetings/{date}-{type}.md` | Create structured meeting note |
| Technical docs | `{brain_path}/Projects/{name}/{descriptive}.md` | Create project-specific sub-note |
| Architecture decisions | `{brain_path}/Projects/{name}/{topic}.md` | Document in project folder |
| Technical learnings | `{brain_path}/Notes/{topic}.md` | Create or update (use session date) |
| Daily summary | `{brain_path}/Journal/{SESSION_DATE}.md` | Create or update (file named by session date) |
| Decisions | `{brain_path}/Notes/decision-{topic}.md` | Create with context (use session date) |
| Area-related (ongoing) | See Areas Intelligence below | Route to appropriate area |
| External links/resources | See Resource Capture Intelligence below | Fetch metadata, create rich note |

#### Date Rules

- **Journal**: File goes to `Journal/{SESSION_DATE}.md`, NOT `Journal/{TODAY}.md`. A session from Jan 15 goes into `Journal/2026-01-15.md`, even if you process it on Feb 9.
- **Tasks**: Include the session date when appending: `- [ ] Task description [[Projects/project|Context]] (2026-01-15)`
- **People**: Set `last_contact` to the session date, not today
- **Frontmatter**: `created` = session date (for new files), `updated` = session date (for existing files)
- **Multi-day sessions**: If a session spans multiple days (date headers in extract), route content to the day it occurred. Journal entries may need to go to multiple date files.

#### Areas Intelligence (Decision Tree)

**Question 1: Is it time-bound with a deadline?**
- YES → It's a **Project**, not an Area
- NO → Continue to Question 2

**Question 2: Is it ongoing responsibility without an end date?**
- YES → It's an **Area**
- NO → It's a **Note** (one-off learning/insight)

**Examples:**

| Content | Decision | Destination |
|---------|----------|-------------|
| "Started running every morning" | Ongoing habit, no deadline | `Areas/health.md` |
| "Q1 marketing campaign planning" | Time-bound, has deadline | `Projects/q1-marketing/` |
| "Learned async/await patterns" | One-off learning | `Notes/async-await-patterns.md` |
| "Monthly budget review process" | Ongoing responsibility | `Areas/finances.md` |
| "Building new landing page" | Time-bound project | `Projects/landing-page-redesign/` |
| "Family dinner traditions" | Ongoing, no deadline | `Areas/family.md` |

**Default Areas (create if they don't exist):**
- `career.md` — professional development, skills, networking
- `health.md` — fitness, wellness, habits, routines
- `family.md` — relationships, quality time, traditions
- `finances.md` — budget, investments, income tracking

**Custom Areas:** User can create new areas as single files (e.g., `side-projects.md`, `learning.md`)

**Rules:**
- Areas are FLAT files (one `.md` per area, no subfolders)
- If an area grows >200 lines → extract sections to `Notes/` and link
- If an area becomes time-bound → move to `Projects/`

#### Task Routing Intelligence (Auto-Classification)

**Scan task for urgency signals:**

| Urgency | Keywords | Destination | Max Count |
|---------|----------|-------------|-----------|
| **URGENT** | "by Friday", "asap", "urgent", "today", "this week", "deadline", specific near date | `Tasks/tasks.md` → ## Focus | 10 |
| **IMPORTANT** | "should", "need to", "reminder", "important", "priority" | `Tasks/tasks.md` → ## Next Up | 15 |
| **BACKLOG** | "eventually", "maybe", "someday", "Phase X", "v2", "future" | `Projects/{name}/{name}.md` → ## Tasks → ### Backlog | No limit |

**Examples:**

```markdown
"Deploy site by Friday"
→ Urgency: URGENT (deadline keyword + near date)
→ Destination: Tasks/tasks.md (Focus)
→ Format: - [ ] Deploy site by Friday [[Projects/myproject/myproject|MyProject]] ⚡

"Research payment providers"
→ Urgency: IMPORTANT (no deadline, but action verb)
→ Destination: Tasks/tasks.md (Next Up)
→ Format: - [ ] Research payment providers [[Projects/myproject/myproject|MyProject]]

"Phase 2 features: user dashboard"
→ Urgency: BACKLOG (phase keyword, future scope)
→ Destination: Projects/myproject/myproject.md (Tasks → Backlog)
→ Format: - [ ] User dashboard implementation
```

**Task Format:**
```markdown
# In Tasks/tasks.md (Focus/Next Up):
- [ ] Task description [[Projects/project/project|Project Name]] [⚡ if urgent] (YYYY-MM-DD)

# In Projects/{name}/{name}.md (Backlog):
## Tasks
### Backlog
- [ ] Task description
```

**Rules:**
- If task mentions a project → add link to project file
- If urgency unclear → default to Next Up
- If Focus already has 10 items → push to Next Up
- Never duplicate between tasks.md and project files (choose one)

#### Persona Learning (Evidence Extraction)

**After routing ALL content, analyze sessions for behavioral patterns.**

**Pattern Categories:**

1. **User Corrections** — user changed Claude's approach
2. **Repeated Workflows** — same sequence of actions multiple times
3. **Communication Preferences** — tone, formality, language
4. **Decision-Making Patterns** — how user evaluates options
5. **Code Style Preferences** — naming, structure, frameworks

**Detection Logic:**

```markdown
# Scan session for:

## User Corrections
- User said "no, do it this way instead"
- User modified Claude's output
- User rejected a suggestion
→ Add to Persona.md ## Evidence Log: "[DATE] User prefers X over Y (context)"

## Repeated Workflows
- Same action sequence appears 3+ times across sessions
- User mentions "I always do X"
→ Add to Persona.md ## Workflow section

## Communication Preferences
- User writes in Romanian/English/mixed
- User prefers concise vs detailed responses
- User uses specific terminology
→ Add to Persona.md ## Communication section

## Decision-Making
- User evaluates options based on X criteria
- User prioritizes Y over Z consistently
→ Add to Persona.md ## Decision-Making section

## Code Style
- User consistently uses specific naming patterns
- User prefers certain frameworks/libraries
- User has strong opinions on architecture
→ Add to Persona.md ## Code Style section
```

**Update Rules:**

1. **Reinforces existing pattern** → Add evidence line with `[DATE]` prefix
2. **New pattern** → Add to appropriate section + evidence
3. **Contradicts pattern** → Update section, note change in evidence

**Persona.md Update:**
```markdown
---
updated: {SESSION_DATE}  # Most recent session processed
---

# Persona

## Communication
- Prefers concise, no-fluff responses
- Uses Romanian for casual, English for technical

## Evidence Log
- [2026-02-12] Corrected task routing — prefers Focus/Next Up over distributed
- [2026-02-11] Chose flat Areas structure over nested folders
```

**ONLY capture clear, meaningful patterns. Skip routine/trivial behavior.**

#### Resource Capture Intelligence (Web URLs)

**When session contains external URLs:**

1. **Detect URL** — any `http://` or `https://` link
2. **Fetch Metadata** — use `web_fetch(url)` to extract:
   - Page title
   - Author (if meta tag exists)
   - Description/summary
   - Content preview (first 2-3 paragraphs)
3. **Classify Type** — article, tool, video, book, documentation
4. **Determine Subfolder** — `Resources/articles/`, `Resources/tools/`, etc.
5. **Create Rich Note**:

```markdown
---
source: {URL}
author: {AUTHOR}
type: {TYPE}
created: {SESSION_DATE}
tags: [resource, {topic-tags}]
related: []
---

# {PAGE_TITLE}

## Summary
{Auto-extracted 2-3 sentence summary}

## Key Takeaways
{Bullet points from content or ask user}

## Why It Matters
{Infer from session context or ask user}

## Related
{Auto-link to related Projects/Notes}
```

6. **Auto-Link** — Scan for related content:
   - Mentions project → link `[[Projects/{name}/{name}|Name]]`
   - Mentions topic → link `[[Notes/{topic}]]`
   - Update related notes' frontmatter

**Example:**

```markdown
User: "Save this: https://example.com/article-on-async-patterns"

1. web_fetch(url) → extract metadata
2. Create Resources/articles/async-patterns-in-python.md:

---
source: https://example.com/article-on-async-patterns
author: Jane Doe
type: article
created: 2026-02-12
tags: [resource, python, async, patterns]
related: ["[[Notes/async-await-patterns]]", "[[Projects/myproject/myproject]]"]
---

# Async Patterns in Python

## Summary
Deep dive into asyncio patterns for handling concurrent operations in Python applications.

## Key Takeaways
- Use asyncio.gather() for parallel execution
- Context managers work with async
- Proper error handling in async contexts

## Why It Matters
Relevant for current API refactoring work in myproject.

## Related
- [[Notes/async-await-patterns]]
- [[Projects/myproject/myproject|MyProject]] — API optimization task
```

**Error Handling:**
- If `web_fetch` fails → create minimal note with URL only, flag for manual review
- If no metadata available → ask user for context

#### Routing Rules (General)

**People** — Only create/update for meaningful interactions:
- Meetings, calls, discussions with named individuals
- NOT for casual mentions or names in code
- Update `last_contact` in frontmatter to session date, append to `## Interactions`

**Projects** — Match to existing projects when possible:
- Check `{brain_path}/Projects/` for existing project folders
- Update recent activity section
- Link to people involved
- **Sub-notes:** Create `Projects/{name}/{descriptive}.md` for technical docs, architectural decisions, specs
- **Meetings:** Create `Projects/{name}/Meetings/{date}-{type}.md` for meeting notes

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

**Tasks** — See Task Routing Intelligence above

#### Linking Rules

**Obsidian handles backlinks automatically.** When you link `[[People/john-smith]]` in a Journal entry, Obsidian shows that Journal entry in john-smith's Backlinks panel. You do NOT need to manually create links in both directions.

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

**Example — session about a meeting with someone about a project:**
1. `Journal/{date}.md` → add section with `[[Projects/myproject/myproject|MyProject]]`, `[[People/john-smith]]`, summary of what happened
2. `People/john-smith.md` → update `last_contact`, add interaction entry (actual content about what was discussed)
3. `Projects/myproject/myproject.md` → add to `## Log` (actual work/decisions, not just a link)
4. `Tasks/tasks.md` → add action items with `[[Projects/myproject/myproject|MyProject]]`
5. `Persona.md` → add evidence if behavioral pattern observed

**Do NOT:** Go back to `People/john-smith.md` to add `[[Journal/2026-02-09]]` — Obsidian shows that automatically in backlinks.

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

**See "Persona Learning (Evidence Extraction)" section above.**

This runs AFTER all content routing. Scan processed sessions for behavioral patterns and update `Persona.md`.

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
  - People/john-smith.md (new)
  - Notes/decision-second-brain-architecture.md (new)
  - Resources/articles/async-patterns-python.md (new)

Updated:
  - Journal/2026-02-09.md (+2 sections)
  - Projects/myproject/myproject.md (activity update)
  - Tasks/tasks.md (+3 tasks: 1 Focus, 2 Next Up)
  - Persona.md (+2 evidence lines)
  - Areas/health.md (+1 entry)

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
- External resources (articles, tools, links)
- Behavioral patterns (for Persona)

**Skip:**
- Routine code generation / debugging (too granular)
- Plugin installation and setup sessions
- Sessions that are mostly tool calls with little conversation
- System/meta messages

## Error Handling

- If extract.py fails → show error, skip that session, continue with others
- If a file write fails → warn user, continue with remaining routes
- If no unprocessed sessions → tell user, suggest using "remember this:" for immediate capture
- If web_fetch fails → create minimal resource note, flag for manual review
