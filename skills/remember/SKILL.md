---
name: remember
description: >
  Your personal knowledge repository — capture, organize, and retrieve everything using PARA + Zettelkasten.
  Triggers on: "save this", "remember", "note", "capture", "brain dump".
  Process past sessions with /brain:process. Stores everything as .md files in a Git repo for Obsidian.
---

# Remember

Your personal knowledge repository. Two ways to populate it:

1. **Brain Dump** (immediate) — Say "remember this: ..." and content routes to the right place
2. **Process Sessions** (on-demand) — Run `/brain:process` to extract value from past Claude sessions

## Brain Location

Read config from `~/.claude/plugin-config/remember/config.json` (user scope) or `.claude/plugin-config/remember/config.json` (project scope) → `paths.data_root`.
Falls back to `${CLAUDE_PLUGIN_ROOT}/config.defaults.json` → `~/remember/`.

## First Run Check

**Before any action**, check if brain is initialized:

1. Read config → get brain path
2. Check if path exists with expected structure (Inbox/, Projects/, Areas/)
3. If NOT found → Tell user to run `/brain:init`
4. If found → Proceed

## Repository Structure

```
remember/
├── Inbox/          # Quick capture (clear daily)
├── Projects/       # Active work with deadlines
│   └── <name>/
│       ├── <name>.md           # Project overview
│       ├── Meetings/           # Meeting notes
│       └── *.md                # Technical docs, specs
├── Areas/          # Ongoing responsibilities (flat files)
│   ├── career.md
│   ├── health.md
│   ├── family.md
│   └── finances.md
├── Notes/          # Permanent knowledge, learnings, decisions
├── Resources/      # External links, articles, references
│   ├── articles/
│   ├── tools/
│   └── books/
├── Journal/        # Daily notes (YYYY-MM-DD.md)
├── People/         # One note per person
├── Tasks/          # Centralized task tracking (tasks.md)
├── Templates/      # Note templates
└── Archive/        # Completed projects
```

## How It Works

### Brain Dump (Immediate Capture)

When user says "remember this", "save this", "brain dump", etc., the `UserPromptSubmit` hook
injects routing context. Claude (current session) then writes directly to the correct location.

The hook runs `scripts/user_prompt.sh` which:
- Detects brain dump keywords
- Lists current brain structure (existing People, Projects, Areas)
- Injects routing rules as additional context

### Process Sessions (On-Demand)

`/brain:process` reads unprocessed Claude Code transcripts from `~/.claude/projects/`.
Uses `scripts/extract.py` to parse JSONL transcripts into clean markdown, then routes content.

## Routing Rules

### Content Type → Destination

| Content | Decision Logic | Destination |
|---------|----------------|-------------|
| Time-bound work with deadline | Is it a project? | `Projects/{name}/{name}.md` |
| Ongoing responsibility | No deadline, recurring | `Areas/{area}.md` |
| One-off learning | Single insight | `Notes/{topic}.md` |
| Person interaction | Meaningful contact | `People/{name}.md` |
| Task with deadline this week | Urgent | `Tasks/tasks.md` (Focus) |
| Task without deadline | Important | `Tasks/tasks.md` (Next Up) |
| Future/roadmap task | Backlog | `Projects/{name}/{name}.md` (Tasks) |
| Meeting | Structured notes | `Projects/{name}/Meetings/{date}-{type}.md` |
| Technical doc | Project-specific | `Projects/{name}/{descriptive}.md` |
| Decision | Strategic choice | `Notes/decision-{topic}.md` |
| External URL | Resource | `Resources/{type}/{title}.md` |
| Daily summary | Journal | `Journal/YYYY-MM-DD.md` |

### Areas Intelligence

**Decision Tree:**

1. **Is it time-bound with a deadline?** → YES = Project
2. **Is it ongoing responsibility?** → YES = Area
3. **Otherwise** → Note (one-off insight)

**Examples:**
- "Started running every morning" → `Areas/health.md` (ongoing habit)
- "Q1 marketing campaign" → `Projects/q1-marketing/` (time-bound)
- "Learned async patterns" → `Notes/async-patterns.md` (one-off learning)

**Default Areas:** `career.md`, `health.md`, `family.md`, `finances.md`

### Task Routing Intelligence

**Auto-classification based on urgency:**

| Urgency | Keywords | Destination |
|---------|----------|-------------|
| **URGENT** | "by Friday", "asap", "urgent", "today", deadline this week | `Tasks/tasks.md` (Focus, max 10) |
| **IMPORTANT** | "should", "need to", "reminder", no deadline | `Tasks/tasks.md` (Next Up, max 15) |
| **BACKLOG** | "eventually", "Phase X", "v2", "future" | `Projects/{name}/{name}.md` (Tasks/Backlog) |

**Examples:**
- "Deploy site by Friday" → Focus (deadline keyword)
- "Research payment options" → Next Up (no deadline)
- "Phase 2 dashboard features" → Project backlog (future scope)

### Resource Capture Intelligence

**When user shares a URL:**

1. **Fetch metadata** — use `web_fetch(url)` to extract title, author, summary
2. **Classify type** — article, tool, video, book, documentation
3. **Create rich note** in `Resources/{type}/{title}.md`:
   - Auto-extracted summary
   - Key takeaways
   - Why it matters (from context)
   - Related links to Projects/Notes
4. **Auto-link** — connect to relevant content in brain

### Persona Learning

**Behavioral pattern extraction** during `/brain:process`:

- User corrections → preferences
- Repeated workflows → habits
- Communication style → tone/language
- Decision criteria → priorities
- Code style → technical preferences

Updates `Persona.md` with evidence-based learning.

## Note Format

Every note uses minimal frontmatter:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
---

# Title

Content here. Link to [[Related Notes]] freely.
```

## Persona

`Persona.md` at the brain root contains behavioral patterns and preferences. It's:
- **Loaded** at every session start (via brain-session)
- **Updated** during `/brain:process` when new patterns are observed

This is how Claude gets smarter about working with you over time.

## Commands

| Command | Action |
|---------|--------|
| `/brain:init` | Initialize brain structure |
| `/brain:process` | Process unprocessed Claude sessions + update Persona |
| `/brain:status` | Show brain statistics |
| "remember this: X" | Immediate brain dump |
| "save this: X" | Immediate brain dump |

## File Naming

- Folders: `kebab-case/`
- Files: `kebab-case.md`
- Dates: `YYYY-MM-DD.md`
- People: `firstname.md` or `firstname-lastname.md`

## Linking

Use `[[wiki-links]]` to connect notes:

```markdown
Met with [[People/john-smith]] about [[Projects/myproject/myproject|MyProject]].
Relevant insight: [[Notes/async-patterns]]
```

Obsidian handles backlinks automatically — link forward, don't duplicate.
