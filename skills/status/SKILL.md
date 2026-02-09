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

## Steps

### 1. Resolve Brain Path

Read config from `~/.claude/plugin-config/remember/config.json` (user scope) or `.claude/plugin-config/remember/config.json` (project scope), falling back to `${CLAUDE_PLUGIN_ROOT}/config.defaults.json` → get `paths.data_root` value.
Expand `~` to home directory. Use this as `{brain_path}`.
If config missing or brain path doesn't exist → tell user to run `/brain:init`.

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
