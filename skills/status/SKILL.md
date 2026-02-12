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

## Important: Use Built-in Tools

**Use built-in tools (LS, Glob, Grep, Read) instead of Bash commands for brain operations. These are auto-approved and don't require permission prompts.**

- List files → use `LS` tool (not `bash ls`)
- Find files by pattern → use `Glob` tool (not `bash find`)
- Search content → use `Grep` tool (not `bash grep`)
- Read files → use `Read` tool (not `bash cat`)
- Count files → use `Glob` tool and count results (not `bash wc`)

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

Read the brain directory and count files. No external metadata files needed — just `ls` and `wc`.

## Notes

- Fast command (just reads directory listings)
- Can run anytime
- No JSON metadata files required — counts come from the filesystem
