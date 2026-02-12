---
name: brain-session
description: >
  Load your Persona at session start. This hooks into SessionStart to inject behavioral
  patterns and preferences from Persona.md into every conversation.
---

# brain-session — Session Start Hook

Loads `Persona.md` from your brain at the start of each Claude Code session, so Claude knows your preferences, patterns, and communication style.

## How It Works

1. **SessionStart hook triggers** — runs automatically when a new Claude session begins
2. **Resolve brain path** — read config → `paths.data_root`
3. **Check for Persona.md** — look for `{brain_path}/Persona.md`
4. **Inject as context** — if found, prepend Persona content to session
5. **Show brain stats** — quick overview of your brain structure

## What Gets Loaded

**Persona.md** contains:
- Communication preferences (tone, language, formality)
- Workflow patterns (how you work, habits)
- Decision-making criteria (what you prioritize)
- Code style preferences (naming, frameworks, structure)
- Evidence log (dated observations from past sessions)

This is how Claude gets smarter about working with you over time.

## Brain Stats Display

Shows a quick overview at session start:

```
🧠 Brain loaded (~/remember/)

Recent activity:
- [[Projects/myproject|MyProject]] - last active today
- [[Projects/another-project|AnotherProject]] - last active yesterday

People:
- [[People/john-smith]] - last contact yesterday
- [[People/jane-doe]] - last contact 3 days ago

Tasks:
- 5 in Focus
- 12 in Next Up

Journal: 45 entries

Commands: /brain:init | /brain:process | /brain:status
```

## File Location

- **Persona.md** — `{brain_path}/Persona.md`
- Updated by `/brain:process` when behavioral patterns are detected

## Config

Reads config from:
1. `~/.claude/plugin-config/remember/config.json` (user scope)
2. `.claude/plugin-config/remember/config.json` (project scope)
3. Falls back to `${CLAUDE_PLUGIN_ROOT}/config.defaults.json`

Uses `paths.data_root` for brain location.
