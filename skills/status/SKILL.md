---
name: brain:status
description: Show Remember learning statistics and status
user-invocable: true
---

# /brain:status - Remember Status

Displays brain statistics: file counts, recent activity, and brain health.

## Usage

```
/brain:status
```

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


## Steps

### 1. Resolve Brain Path

Read `$REMEMBER_BRAIN_PATH` env var, fallback `~/remember`. Use this as `{brain_path}`.
If brain path doesn't exist → tell user to run `/brain:init`.

### 2. Show Brain Statistics

Count files and directories in the brain:

```
Brain: {brain_path}

Projects: {count} active
  - project-a (list names)
  - project-b

People: {count} total
  - name-a
  - name-b

Areas: {count}
Notes: {count} knowledge notes
Journal: {count} days logged
Tasks: show open/completed count from Tasks/tasks.md
Resources: {count}
Inbox: {count} items
```

### 3. Show Recent Activity

List recently modified files (last 7 days) across People/, Projects/, Journal/, Notes/.

### 4. Show Persona Summary

Read `{brain_path}/Persona.md` and show a brief summary of captured patterns.

## Implementation

Use `LS` and `Glob` tools to read directories and count files. For complex stats, use a subagent.

## Notes

- Fast command (uses built-in LS/Glob/Read tools — no Bash needed)
- Can run anytime
- No JSON metadata files required — counts come from the filesystem
