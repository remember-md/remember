---
name: brain-session
description: BrainRepo session context loader - loads Second Brain context and spawns curator agent
version: 1.0.0
---

# Brain Session

Activates at session start to load Second Brain context and spawn the curator agent.

## When to use

**Automatically** at the start of every Claude Code session.

## What it does

### 1. Load Identity

Read `~/supabrain/learning/meta/identity.json` to know:
- Who you are (name, technical level)
- Session count
- Last active date

### 2. Load Recent Context

Read recent Second Brain content:

**Today's Journal:**
```bash
cat ~/supabrain/content/Journal/$(date +%Y-%m-%d).md
```

**Yesterday's Journal (if exists):**
```bash
cat ~/supabrain/content/Journal/$(date -d yesterday +%Y-%m-%d).md
```

**Active Projects:**
List projects with recent activity (last 7 days):
```bash
find ~/supabrain/content/Projects/ -name "*.md" -mtime -7
```

### 3. Load Relevant Instincts

Read instincts that might apply to current context:
- Check current working directory
- Load project-specific instincts
- Load general workflow instincts (confidence 0.7+)

### 4. Spawn Curator Agent

**Spawn brain-curator agent in background:**
```
spawn agent brain-curator with instructions:
  - Run every 5 minutes
  - Process new observations
  - Auto-populate Second Brain
  - Learn patterns
  - Check for clustering
```

The curator runs silently in background throughout the session.

### 5. Greet with Context

Provide brief context to user:
```
Good morning! 🧠

Session #42 | Last: 2026-02-07

Recent activity:
- [[Projects/my-app|My App]] - worked on dashboard
- Talked to [[People/alice|Alice]] yesterday

Brain curator running in background.
```

## Example Implementation

```javascript
async function brainSessionStart() {
  const brainRepo = '~/supabrain';
  
  // 1. Load identity
  const identity = await readJSON(`${brainRepo}/learning/meta/identity.json`);
  
  // 2. Load today + yesterday journal
  const today = await readFile(`${brainRepo}/content/Journal/${getDate()}.md`);
  const yesterday = await readFile(`${brainRepo}/content/Journal/${getYesterday()}.md`);
  
  // 3. Find active projects
  const activeProjects = await findRecentProjects(brainRepo, 7);
  
  // 4. Load relevant instincts
  const instincts = await loadInstincts(brainRepo, {
    minConfidence: 0.7,
    domains: ['workflow', 'code-style']
  });
  
  // 5. Spawn curator
  await spawnAgent('brain-curator', {
    interval: 5 * 60 * 1000, // 5 minutes
    background: true
  });
  
  // 6. Greet
  return formatGreeting(identity, activeProjects, instincts);
}
```

## Configuration

Uses settings from `~/.claude/plugins/supabrain/config.json`:
- `curator.enabled` - whether to spawn curator
- `curator.interval_minutes` - how often curator runs
- `curator.auto_populate` - what to auto-populate

## Error Handling

If `~/supabrain/` doesn't exist:
- Suggest running `/brain:init` to set up
- Don't spawn curator
- Minimal greeting

## Notes

- Runs **once** per session at start
- Curator continues in background until session ends
- Stop hook updates session count in identity.json
