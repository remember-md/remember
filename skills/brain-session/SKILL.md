---
name: brain-session
description: Remember session context loader - loads Second Brain context
version: 1.1.0
---

# Brain Session

Loads Second Brain context at session start.

## When to use

**Automatically** at the start of every Claude Code session.

## What it does

### 1. Resolve Brain Path (MANDATORY FIRST STEP)

**You MUST read the config file before doing anything else.** Do NOT assume or hardcode any path.

Try these locations in order, use the first one that exists:
1. `~/.claude/plugin-config/remember/config.json` (user scope, persistent)
2. `.claude/plugin-config/remember/config.json` (project scope, persistent)
3. `${CLAUDE_PLUGIN_ROOT}/config.defaults.json` (shipped default)

Parse JSON → extract `paths.data_root` value. Expand `~` to the user's home directory. Use this resolved path as `{brain_path}` for ALL subsequent operations.

If no config file exists → tell user to run `/brain:init`.

### 2. Load Persona

**Read `{brain_path}/Persona.md` FIRST.** This file contains behavioral patterns and preferences. Apply them throughout the entire session.

### 3. Load Recent Context

Read recent Second Brain content:

**Today's Journal (if exists):**
Read `{brain_path}/Journal/YYYY-MM-DD.md` (today's date)

**Active Projects:**
List projects with recent activity (last 7 days)

**Recent People:**
List recently modified files in `{brain_path}/People/`

### 4. Greet with Context

Provide brief context (apply Persona preferences — concise, Romanian if appropriate):
```
Session loaded | Brain: {brain_path}

Recent:
- [[Projects/impact3|Impact3]] - last active today
- [[People/archie]] - last contact yesterday

Capture: say "remember this: ..."
Process past sessions: /brain:process
```

## Configuration

User config is at `~/.claude/plugin-config/remember/config.json` (user scope) or `.claude/plugin-config/remember/config.json` (project scope).

```json
{
  "paths": {
    "data_root": "/path/to/brain"
  }
}
```

**IMPORTANT:** Always read the config. Never use hardcoded paths. Check user-scope config first, then project-scope, then `${CLAUDE_PLUGIN_ROOT}/config.defaults.json`.

## Error Handling

If config file missing or brain path doesn't exist:
- Tell user to run `/brain:init`
- Minimal greeting

## Notes

- Runs **once** per session at start
- No background agents — brain is populated via brain dump keywords or `/brain:process`
