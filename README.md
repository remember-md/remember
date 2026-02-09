# Remember - Second Brain Plugin for Claude Code

A Claude Code plugin that captures your knowledge into an Obsidian-compatible Second Brain using PARA + Zettelkasten methodology.

## What It Does

Remember gives you two ways to build your knowledge base:

1. **Brain Dump** (immediate) — Say "remember this: ..." during any session. The hook detects keywords and injects routing context so Claude writes to the correct location.
2. **Process Sessions** (on-demand) — Run `/brain:process` to extract valuable content from past Claude Code transcripts.

Your Second Brain is plain markdown files with wikilinks — works with Obsidian, Logseq, or any text editor.

## Install

```bash
git clone https://github.com/remember-md/remember.git ~/.claude/plugins/remember
```

Then in Claude Code:

```
/brain:init
```

This creates your brain directory structure and Persona file. Default location: `~/remember`.

## Brain Structure

```
~/remember/
├── Inbox/          # Quick capture
├── Projects/       # Active work
├── Areas/          # Ongoing responsibilities
├── Notes/          # Permanent knowledge, decisions
├── Resources/      # Links, articles, references
├── Journal/        # Daily notes (YYYY-MM-DD.md)
├── People/         # One note per person
├── Tasks/          # Centralized task tracking
├── Templates/      # Note templates
├── Archive/        # Completed projects
└── Persona.md      # Your behavioral patterns (loaded every session)
```

## Commands

| Command | Description |
|---------|-------------|
| `/brain:init` | Initialize brain structure and config |
| `/brain:process` | Process unprocessed Claude sessions into brain |
| `/brain:status` | Show brain statistics (file counts, recent activity) |
| "remember this: ..." | Immediate brain dump via hook |
| "save this: ..." | Immediate brain dump via hook |

## How It Works

### Hook (Automatic)

On every `UserPromptSubmit`, `scripts/user_prompt.sh` runs:

- **First message** of a session: loads `Persona.md` and injects it as context, along with active projects and today's journal status.
- **Brain dump keywords** detected: injects full routing rules (existing People, Projects, Areas) so Claude knows where to write.

### Processing (Manual)

`/brain:process` uses `scripts/extract.py` to:
1. Find unprocessed JSONL transcripts in `~/.claude/projects/`
2. Extract clean user/assistant messages
3. Route content to the right brain location (People, Projects, Journal, Notes, Tasks)
4. Update `Persona.md` with observed behavioral patterns

### Persona

`Persona.md` lives at your brain root and captures how you prefer to work — communication style, code preferences, workflow habits. It's loaded at every session start and updated during `/brain:process`.

## Configuration

`/brain:init` saves your chosen brain path to a persistent config that survives plugin updates.

Config location:
- **User scope** (default): `~/.claude/plugin-config/remember/config.json`
- **Project scope**: `.claude/plugin-config/remember/config.json`

The plugin reads config in this order:
1. User-scope config (persistent, created by `/brain:init`)
2. Project-scope config (persistent)
3. `config.defaults.json` shipped with the plugin (`~/remember`)

To change your brain location after init:

```bash
# Edit the config
cat ~/.claude/plugin-config/remember/config.json
```

```json
{
  "paths": {
    "data_root": "~/my-custom-path"
  }
}
```

## Note Format

All notes use YAML frontmatter + wikilinks:

```markdown
---
created: 2026-02-09
updated: 2026-02-09
tags: [topic]
---

# Title

Content with [[People/name]] and [[Projects/project/project|Project]] links.
```

Obsidian handles backlinks automatically — you only need to link forward.

## Privacy

- All data is local markdown files
- No cloud, no telemetry
- Git-friendly (version control your brain)
- Your data stays yours

## Requirements

- Claude Code (latest version)
- Python 3 (for session extraction)
- Git (optional, for version control)

## Compatibility

Works with any markdown editor. Optimized for **Obsidian** (wikilinks, backlinks, graph view).

## Credits

Built on ideas from:
- [continuous-learning-v2](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2) — Hooks architecture
- **PARA Method** (Tiago Forte) — Organization structure
- **Zettelkasten** (Niklas Luhmann) — Linked thinking

## License

MIT — see [LICENSE](LICENSE).
