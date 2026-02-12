---
name: brain-session
description: >
  Load your Persona at session start. This hooks into SessionStart to inject behavioral
  patterns and preferences from Persona.md into every conversation.
version: 1.4.0
user-invocable: false
---

# brain-session — Session Start Hook

Loads `Persona.md` from your brain at the start of each Claude Code session, so Claude knows your preferences, patterns, and communication style.

## ⚠️ MANDATORY: Use Built-in Tools Only (NO Bash!)

**NEVER use Bash commands for brain operations.** Use Claude Code's built-in tools which are auto-approved and require zero permission prompts:

| Operation | ✅ Use This | ❌ NOT This |
|-----------|------------|-------------|
| List files | `LS` tool | `bash ls` |
| Find files | `Glob` tool | `bash find` |
| Search content | `Grep` tool | `bash grep` |
| Read files | `Read` tool | `bash cat` |
| Write/create files | `Write` tool | `bash echo >` / `bash tee` |
| Count files | `Glob` tool + count results | `bash wc` |
| Check env vars | Already available as `$REMEMBER_BRAIN_PATH` | `bash echo $VAR` |

**For complex operations** (stats, counting, multi-step), use a **subagent** (Task tool) that uses the same built-in tools.

**Why:** `additionalDirectories` auto-approves LS/Glob/Grep/Read/Write. Bash always prompts.


## How It Works

1. **SessionStart hook triggers** — runs automatically when a new Claude session begins
2. **Resolve brain path** — read `$REMEMBER_BRAIN_PATH` env var, fallback `~/remember`
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

## Error Handling

If brain path doesn't exist:
- Tell user to run `/brain:init`
- Minimal greeting

## Notes

- Runs **once** per session at start
- No background agents — brain is populated via brain dump keywords or `/brain:process`
