# REMEMBER.md Guide

> Your custom instructions for how your Second Brain captures, processes, and organizes knowledge.

---

## What is REMEMBER.md?

`REMEMBER.md` is a user-editable file at your brain root (e.g., `~/remember/REMEMBER.md`) where you define custom rules for how Remember works. It uses plain markdown — no schemas, no config syntax, just natural language that Claude reads and follows.

**Key principles:**

- **You own it** — Remember never auto-modifies this file (unlike Persona.md)
- **All sections are optional** — leave a section empty or remove it entirely to use defaults
- **Additive by default** — your instructions augment built-in behavior, not replace it
- **Zero config works** — if you never touch REMEMBER.md, Remember works exactly as before

### REMEMBER.md vs Persona.md

| | REMEMBER.md | Persona.md |
|---|---|---|
| **Who writes it** | You (the user) | The system (`/brain:process`) |
| **Purpose** | What you WANT the brain to do | What the AI OBSERVES about you |
| **Nature** | Prescriptive (instructions) | Descriptive (patterns) |
| **Auto-modified** | Never | Yes, during processing |

**Precedence:** `REMEMBER.md > Built-in Defaults > Persona.md`

---

## Sections Reference

### `## Capture Rules`

Define what to always or never capture, and set thresholds.

**Example:**

```markdown
## Capture Rules

### Always Capture
- Client meetings and who attended
- Decisions with rationale (especially "why NOT" something)
- Book/article recommendations from anyone
- Health observations (symptoms, energy levels, sleep quality)

### Never Capture
- Casual greetings or small talk
- Debugging sessions (unless a reusable lesson emerges)
- Code snippets without context (code belongs in repos, not the brain)
- Venting — if I'm just frustrated, don't save it unless I explicitly say so

### Capture Thresholds
- Ignore messages under 5 words unless they contain a name or decision
- For long sessions, prioritize: decisions > tasks > learnings > context
```

**How it works:** During brain dumps and `/brain:process`, Claude checks these rules FIRST before applying default routing. "Never Capture" items are skipped even if they'd normally be captured. "Always Capture" items are saved even if they seem too minor by default.

---

### `## Processing`

Control how content is routed, formatted, and tagged.

**Example:**

```markdown
## Processing

### Routing Overrides
- Anything about "Impact3" → Projects/impact3/ (always, even if it sounds like an Area)
- Health data → Areas/health.md, but mental health → Areas/personal-growth.md
- "Reading list" items → Resources/books/ even if no URL is provided

### Output Style
- Journal entries: bullet points grouped by project, not prose paragraphs
- People interactions: include direct quotes when available
- Decisions: always include "Alternatives considered" and "Why this choice"
- Tasks: include estimated effort when I mention it (⏱️ tag)

### Tagging
- Auto-tag client meetings with `billable` and the client name
- Tag all decisions with `decision` + domain (tech, business, personal)
- Tag learnings from mistakes with `lesson-learned`
```

**How it works:** Routing Overrides apply before the default routing table. Output Style affects how content is formatted when written. Tagging rules are applied to frontmatter tags.

---

### `## Custom Types`

Define entity types beyond the standard PARA structure.

**Example:**

```markdown
## Custom Types

### Meeting Notes (→ Projects/{project}/meetings/)
When processing a meeting or call:
- Create: `Projects/{project}/meetings/YYYY-MM-DD-topic.md`
- Sections: Attendees, Key Points, Decisions, Action Items
- Always link attendees to People/

### Habits (→ Areas/health.md, section: ## Habit Tracker)
When I mention starting, stopping, or tracking a habit:
- Format: `| Date | Habit | Status | Notes |`
- Track: exercise, meditation, reading, sleep schedule

### Bookmarks (→ Resources/bookmarks.md)
When I share a URL without much context:
- Don't create a full Resource file
- Instead, append to Resources/bookmarks.md as: `- [Title](url) — one-line description ({date})`
```

**How it works:** During classification, Claude checks if content matches a Custom Type before falling through to the default routing table. Each Custom Type specifies where and how to store the content.

---

### `## Connections`

Define auto-linking rules and people context.

**Example:**

```markdown
## Connections

### Auto-Link Rules
- Any mention of "Impact3" + a person → link both to Projects/impact3/
- "Family" topics → always cross-link to People/ entries for family members
- Tech decisions → link to both the Project and Notes/decision-*

### People Context
- Maria = my wife (don't re-explain this in every People/ interaction)
- Alex = cofounder at Impact3 (link to Projects/impact3/ automatically)
```

**How it works:** When creating or updating notes, Claude uses these rules to add wikilinks automatically. People Context prevents redundant "who is this person" explanations in interaction logs.

---

### `## Language`

Control multilingual capture and processing behavior.

**Example:**

```markdown
## Language

- I switch between English and Romanian freely
- Capture in whatever language I used
- Process/organize using English for headers and tags
- Romanian is fine for content/body text
```

**How it works:** Injected into both brain dump hooks and `/brain:process` context. Tells Claude how to handle language in file names, headers, tags, and body content.

---

### `## Templates`

Override default note templates for specific file types.

**Example:**

```markdown
## Templates

### Journal Override
My daily journal should have these sections:
```
## {Project/Topic}
- What happened
- Decisions made

## Reflections
- What went well
- What to improve
```

### People Override
Add a "## Shared Interests" section after "## Who" in new People files.
```

**How it works:** When creating new files, Claude checks this section first. If a template override exists for the file type, it uses your template instead of the default from `assets/templates/`.

---

### `## Notes`

Free-form space for anything else you want the brain to know.

**Example:**

```markdown
## Notes

- I'm a morning person — weight morning captures higher than evening ones
- I use Obsidian daily, so wikilinks and graph compatibility matter a lot
- When in doubt about where something goes, ask me rather than guessing wrong
```

---

## Getting Started

After running `/brain:init`, you'll find a starter `REMEMBER.md` with empty sections:

```markdown
# REMEMBER.md

Instructions for how your Second Brain captures and processes knowledge.
All sections are optional.

---

## Capture Rules

## Processing

## Custom Types

## Connections

## Language

## Templates

## Notes
```

Just fill in the sections that matter to you. Empty sections are ignored — defaults apply.

## Tips

1. **Start small** — add one or two Capture Rules, see how it works, then expand
2. **Be specific** — "Never capture debugging sessions" is clearer than "Don't save technical stuff"
3. **Use examples** — "Route like this: X → Y" is better than abstract descriptions
4. **Review periodically** — as your workflow evolves, update REMEMBER.md to match
5. **Don't duplicate Persona.md** — REMEMBER.md is for instructions, Persona.md is for patterns. Let each do its job.

## FAQ

**Q: What happens if REMEMBER.md conflicts with Persona.md?**
A: REMEMBER.md wins. It represents your explicit intent, which takes precedence over observed patterns.

**Q: Can I delete sections I don't use?**
A: Yes. Missing sections use defaults. You can also leave them empty — same effect.

**Q: Will `/brain:process` modify my REMEMBER.md?**
A: Never. REMEMBER.md is exclusively user-edited. Only Persona.md is auto-updated.

**Q: How many tokens does REMEMBER.md use?**
A: A moderate file (~50 lines) uses ~500 tokens. For brain dumps, only Capture Rules, Processing, Custom Types, and Language sections are injected (not the full file). For `/brain:process`, the full file is loaded (batch operation with larger token budget).

**Q: Can I have project-specific REMEMBER.md files?**
A: Not yet — this is planned for a future release. Currently, one REMEMBER.md at your brain root applies globally.
