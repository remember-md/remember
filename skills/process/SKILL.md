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

## Important: Use Built-in Tools

**Use built-in tools (LS, Glob, Grep, Read) instead of Bash commands for brain operations. These are auto-approved and don't require permission prompts.**

- List files → use `LS` tool (not `bash ls`)
- Find files by pattern → use `Glob` tool (not `bash find`)
- Search content → use `Grep` tool (not `bash grep`)
- Read files → use `Read` tool (not `bash cat`)

Note: Python scripts (extract.py) still use Bash — that's expected. This applies to brain directory operations.

## Steps

### 1. Resolve Brain Path

Read `$REMEMBER_BRAIN_PATH` env var, fallback `~/remember`. Use this as `{brain_path}`. If the directory doesn't exist → tell user to run `/brain:init`.

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

#### Task Routing Intelligence (AI-Driven Classification)

**YOU (the AI) classify tasks by understanding context and urgency semantically, not via keywords.**

**Goal:** Route tasks to the right place based on urgency and importance.

**Classification Categories:**

| Urgency | Description | Destination | Max Count |
|---------|-------------|-------------|-----------|
| **URGENT** | Has a near deadline or blocking priority | `Tasks/tasks.md` → ## Focus | 10 |
| **IMPORTANT** | Needs to be done, but no immediate deadline | `Tasks/tasks.md` → ## Next Up | 15 |
| **BACKLOG** | Future work, nice-to-have, roadmap item | `Projects/{name}/{name}.md` → ## Tasks → ### Backlog | No limit |

**How to Classify (Semantic Understanding):**

**URGENT — Ask yourself:**
- Does this have a deadline within the next 7 days?
- Is someone waiting on this?
- Will something break if this isn't done soon?
- Does the user express time pressure? (any language: "urgent", "asap", "de mâine", "azi", "by Friday")

**IMPORTANT — Ask yourself:**
- Is this a clear action item without a deadline?
- Should this be done relatively soon?
- Is it a stepping stone for something bigger?
- User says "trebuie să" / "need to" / "should" without urgency?

**BACKLOG — Ask yourself:**
- Is this future work? ("Phase 2", "v2", "eventually", "someday")
- Is it exploratory? ("research", "maybe", "consider")
- Is it part of a roadmap but not active work?
- User says "eventual" / "later" / "când am timp"?

**Multi-Language Urgency Signals:**

**Urgent (any of these):**
- English: "by [day/date]", "urgent", "asap", "today", "this week", "deadline", "blocking"
- Other languages: "de mâine", "urgent", "azi", "săptămâna asta", "până [când]", "blochează"
- Context: Specific near date mentioned (numeric or day name)

**Important (any of these):**
- English: "should", "need to", "important", "priority", "reminder"
- Other languages: "trebuie", "ar trebui", "important", "prioritate", "să nu uit"
- Context: Action verb without deadline

**Backlog (any of these):**
- English: "eventually", "someday", "maybe", "Phase X", "v2", "future", "later", "nice to have"
- Other languages: "eventual", "cândva", "poate", "viitor", "mai târziu", "când am timp"
- Context: Conditional or distant future tense

**Edge Cases:**

1. **Ambiguous urgency** → Default to IMPORTANT (safer than backlog)
2. **Focus already at 10 items** → Push to Next Up (even if urgent)
3. **Next Up already at 15 items** → Push to Backlog + note in journal
4. **No clear project link** → Still add to tasks.md with generic category

**Task Format:**

```markdown
# In Tasks/tasks.md (Focus/Next Up):
- [ ] Task description [[Projects/project/project|Project Name]] [⚡ if urgent] (YYYY-MM-DD)

# In Projects/{name}/{name}.md (Backlog):
## Tasks
### Backlog
- [ ] Task description (session date if relevant)
```

**Classification Examples:**

**Example 1: Urgent**
```
User: "Deploy site by Friday, clientul așteaptă"
Analysis:
- Deadline: "by Friday" (2-3 days away)
- Urgency signal: "așteaptă" (someone waiting)
→ URGENT → tasks.md (Focus)
→ Format: - [ ] Deploy site by Friday [[Projects/website-project/website-project|Website Project]] ⚡ (2026-02-12)
```

**Example 2: Important**
```
User: "Trebuie să researchez payment providers pentru 99marketing"
Analysis:
- Action verb: "trebuie" (need to)
- No deadline mentioned
→ IMPORTANT → tasks.md (Next Up)
→ Format: - [ ] Research payment providers [[Projects/marketing-project/marketing-project|Marketing Project]] (2026-02-12)
```

**Example 3: Backlog**
```
User: "Phase 2: add user dashboard pentru saas-app, eventual"
Analysis:
- Future scope: "Phase 2"
- Low urgency: "eventual"
→ BACKLOG → Projects/saas-app/saas-app.md
→ Format: - [ ] User dashboard implementation (under ## Tasks → ### Backlog)
```

**Linking Rules:**

- If task mentions a project → add `[[Projects/{name}/{name}|Name]]` link
- If project not mentioned but you know context → infer and link
- If truly generic → add to tasks.md without project link (user can add later)
- Always add session date for traceability

**Duplication Prevention:**

- **NEVER duplicate** same task in both tasks.md AND project file
- **Rule:** If it goes to Focus/Next Up → link to project, but don't duplicate content in project file
- **Exception:** Roadmap items in project files are NOT tasks (descriptive text, not checkboxes)

**Zero Duplication Example:**

```markdown
# tasks.md (Focus):
- [ ] Deploy site by Friday [[Projects/website-project/website-project|Website Project]] ⚡ (2026-02-12)

# Projects/website-project/website-project.md:
## Tasks
### Active
[No entry here - it's in Focus already]

## Roadmap
### Phase 1
- site integration (in progress, deploy scheduled Friday)
  ↑ This is descriptive, NOT a checkbox task
```

**After Classification:**

1. Write task to appropriate location (tasks.md or project file)
2. Add session date for context
3. Link to project if applicable
4. Mark urgent tasks with ⚡
5. Report in final summary where task was added

**CRITICAL: Understand urgency semantically across languages. Context > keywords.**



### Backlog
- [ ] Task description
```

**Rules:**
- If task mentions a project → add link to project file
- If urgency unclear → default to Next Up
- If Focus already has 10 items → push to Next Up
- Never duplicate between tasks.md and project files (choose one)

#### Persona Learning (AI-Driven Evidence Extraction)

**After routing ALL content, analyze sessions for behavioral patterns using semantic understanding.**

**YOU (the AI) analyze the session content. Don't rely on keyword matching - understand context in any language.**

**Pattern Categories to Detect:**

1. **User Corrections**
   - User changed your approach or rejected a suggestion
   - User said "no, do it this way" (în orice limbă)
   - User modified your output
   - Example detection: User disagreed with how you did something → note what they prefer instead

2. **Stated Preferences**
   - User explicitly says what they like/don't like
   - "I prefer X over Y", "Never use Z", "Always do W"
   - Language-agnostic: "prefer" = "preferă" = "mai bine cu"
   - Example: User says they prefer concise responses → add evidence

3. **Repeated Workflows**
   - Same sequence of actions appears multiple times across sessions
   - User mentions "I always..." or "usually I..."
   - Pattern: If user does X → Y → Z repeatedly → it's a workflow
   - Example: User always runs tests before commit → document workflow

4. **Communication Style**
   - How user writes: concise vs detailed, formal vs casual
   - Language preferences: English for code, native language for casual
   - Tone indicators: emojis, punctuation, formality
   - Example: User uses "hai să" instead of "let's" → native language preference for casual

5. **Decision-Making Patterns**
   - What criteria user uses to evaluate options
   - What they prioritize (speed vs quality, cost vs features, etc.)
   - Consistency in choices across sessions
   - Example: User always picks simpler solution → document preference

6. **Code/Technical Style**
   - Naming conventions user prefers
   - Frameworks/tools they favor
   - Architecture patterns they use
   - Example: User consistently uses kebab-case → add to Code Style

**Detection Logic (Semantic, Not Regex):**

Ask yourself these questions when reading the session:

- **Did the user correct me?** → What did they want instead? Why?
- **Did the user state a preference explicitly?** → What exactly?
- **Did the user repeat a behavior?** → Check past sessions for pattern
- **How does the user communicate?** → Formal? Casual? Mixed language?
- **How does the user make decisions?** → What matters to them?
- **What technical choices do they make consistently?** → Patterns?

**Multi-Language Support:**

- Other languages: "prefer", "mai bine", "nu-mi place", "întotdeauna"
- English: "I prefer", "always", "never use", "better with"
- Mixed: User switches languages → note that preference
- Understand intent, not just keywords: "de mâine" = urgent, "eventual" = backlog

**Update Rules:**

1. **Read Persona.md first** → see existing patterns
2. **If session reinforces existing pattern** → Add evidence line:
   ```markdown
   - [YYYY-MM-DD] User again preferred X over Y (context: project Z)
   ```
3. **If session reveals NEW pattern** → Add to appropriate section + evidence:
   ```markdown
   ## Communication
   - Prefers concise, no-fluff responses
   
   ## Evidence Log
   - [YYYY-MM-DD] User asked to skip intro/outro in responses
   ```
4. **If session CONTRADICTS pattern** → Update section, note change:
   ```markdown
   ## Evidence Log
   - [YYYY-MM-DD] Previous preference changed — now wants detailed explanations for complex topics
   ```

**What to Capture vs Skip:**

**Capture:**
- Clear, meaningful behavioral patterns
- Preferences stated explicitly or shown repeatedly
- Communication style signals (language, tone, formality)
- Decision criteria that appear consistent
- Technical choices made 3+ times

**Skip:**
- One-off actions with no pattern
- Routine/trivial behavior (opening files, running commands)
- Contradictory signals (user experimenting, not deciding)
- Ambiguous situations (unclear intent)

**Evidence Format:**

```markdown
[YYYY-MM-DD] Brief description of what happened + what it reveals

Good examples:
- [2026-02-12] User corrected task routing — prefers Focus/Next Up structure over distributed
- [2026-02-12] User switched to native language mid-conversation for casual topic
- [2026-02-11] User chose flat Areas structure over nested folders (simplicity priority)

Bad examples:
- [2026-02-12] User opened a file (too trivial)
- [2026-02-12] User said something (no insight)
- [2026-02-12] Pattern detected (what pattern??)
```

**Persona.md Update Process:**

1. **Read current Persona.md** → load existing knowledge
2. **Analyze session semantically** → detect patterns (questions above)
3. **Determine updates needed:**
   - New evidence for existing pattern → append to Evidence Log
   - New pattern → add to appropriate section + evidence
   - Contradiction → update section + note change
4. **Write updates** → prepend new evidence (newest first)
5. **Update frontmatter** → `updated: {SESSION_DATE}`

**Example Analysis:**

**Session excerpt:**
```
User: "hai să implementezi 5-8. vezi ca in instructiuni sa nu existe referince la nume reale"
```

**Analysis (semantic understanding):**
- Language: native language ("hai să" = "let's")
- Preference: Generic examples over real data (privacy/reusability concern)
- Communication: Direct, concise instruction
- Decision criteria: Values clean documentation

**Persona update:**
```markdown
## Evidence Log
- [2026-02-12] User requested removing hardcoded names from docs — values generic, reusable examples
- [2026-02-12] User gave instructions in native language with direct, concise style
```

**CRITICAL: Use AI semantic understanding, NOT keyword matching. Understand intent across languages.**

**After analysis:**
- If meaningful patterns found → update Persona.md
- If no clear patterns → skip (better to miss than hallucinate)
- Report what was updated in final summary


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
