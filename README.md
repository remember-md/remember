# Remember — The AI-Powered Second Brain That Builds Itself

> **Your second brain, in your terminal.** Zero-effort knowledge capture for developers who use Claude Code.

Unlike Mem.ai or Reflect, Remember is **free**, **local-first**, and captures **100% of your knowledge deterministically** — no AI guessing, no cloud lock-in, no $10/month subscriptions. Just plain markdown files that work with Obsidian, Logseq, or any text editor.

Remember is an open-source Claude Code plugin that automatically builds your second brain using **PARA + Zettelkasten** methodology. Say "remember this" during any coding session, and your knowledge lands in the right place — People, Projects, Notes, Journal — without you organizing anything.

**This is not another note-taking app.** This is an AI-powered knowledge base that captures while you work.

---

## Why Remember?

Every second brain tool asks you to do the work. Remember does it for you.

| Feature | Remember | Mem.ai | Reflect | Notion AI |
|---------|----------|--------|---------|-----------|
| **Price** | **Free (OSS)** | $12/mo | $10/mo | $10/mo |
| **Capture Rate** | **100% (hooks)** | ~60% AI guess | ~60% AI guess | Manual |
| **Privacy** | **Local-first** | Cloud | Cloud | Cloud |
| **Data Ownership** | **Full (Git)** | Limited | Limited | Locked-in |
| **Offline** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Obsidian Compatible** | ✅ Yes | ❌ No | ❌ No | ⚠️ Export only |
| **Open Source** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Vendor Lock-in** | **None** | High | Medium | High |

**Remember is the free, open-source alternative to Mem.ai and Reflect** — with better capture rates and full data ownership.

---

## What Makes Remember Different

### 🎯 100% Capture Rate (Not AI Guessing)

Mem.ai and Reflect use AI to *guess* what's important — and miss ~40% of valuable content. Remember uses **deterministic hooks** that trigger on explicit commands. When you say "remember this," it captures. Every. Single. Time.

### 🔒 Privacy-First, Local-First Knowledge Management

Your notes never leave your machine. No cloud servers, no terms of service on your thoughts, no data mining. Remember stores everything as **plain markdown files** in a Git-friendly directory. Your second brain is truly yours.

### 🆓 Free Forever (Not $120/Year)

Mem.ai charges $12/month. Reflect charges $10/month. Notion AI charges $10/month. That's **$120+/year** for basic automatic note-taking. Remember is **100% free and open source**. Forever. No bait-and-switch pricing.

### 🧠 AI-Native, Not AI-Bolted-On

Unlike Notion AI or Obsidian's community AI plugins, Remember was built *around* Claude from day one. The AI isn't an add-on — it's the interface. Claude understands PARA methodology, routes your knowledge automatically, and even builds a **Persona.md** that learns how you think.

### 🔗 Obsidian Compatible (Best of Both Worlds)

Unlike Mem.ai's proprietary format or Reflect's closed ecosystem, Remember creates **Obsidian-compatible markdown** with wikilinks, frontmatter, and PARA structure. Use Remember for AI-powered capture, Obsidian for beautiful browsing and graph view.

---

## Who Is This For?

✅ **You want a second brain but maintaining it feels like a second job**
✅ **You use Claude Code daily and want automatic knowledge capture**
✅ **You value privacy and data ownership (local-first, Git-friendly)**
✅ **You're tired of $10/mo subscriptions for basic note-taking**
✅ **You want Obsidian's power + AI automation**
✅ **You're looking for a free Mem.ai alternative or Notion alternative**

❌ Not for you if: You need mobile apps or cloud sync (coming in Pro version)

---

## How It Works

Remember gives you two ways to build your AI-powered knowledge base:

1. **Brain Dump** (immediate) — Say "remember this: ..." during any Claude Code session. The hook detects keywords and routes content to the correct location automatically.
2. **Process Sessions** (on-demand) — Run `/brain:process` to extract valuable content from past Claude Code transcripts into your second brain.

Your second brain is plain markdown files with wikilinks — zero-effort PKM that works with Obsidian, Logseq, or any text editor.

---

## Real Results

> "After 1 week of using Remember, I have 47 notes, 12 people tracked, and 5 project files — all auto-populated. I didn't organize anything manually." — Early user

---

## Install

```bash
git clone https://github.com/remember-md/remember.git ~/.claude/plugins/remember
```

Then in Claude Code:

```
/brain:init
```

This creates your second brain directory structure and Persona file. Default location: `~/remember`.

---

## Second Brain Structure

Remember organizes your knowledge base using PARA + Zettelkasten:

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

---

## Commands

| Command | Description |
|---------|-------------|
| `/brain:init` | Initialize your second brain structure and config |
| `/brain:process` | Process unprocessed Claude sessions into your brain |
| `/brain:status` | Show brain statistics (file counts, recent activity) |
| "remember this: ..." | Immediate brain dump via hook (zero-effort capture) |
| "save this: ..." | Immediate brain dump via hook |

---

## How Capture Works

### Hooks (Automatic Note-Taking)

| Hook | When | What |
|------|------|------|
| `SessionStart` | Session begins | Loads `Persona.md` into Claude's context |
| `UserPromptSubmit` | Every message | Detects brain dump keywords, injects routing rules |

`SessionStart` fires once and injects your Persona as model-visible context. `UserPromptSubmit` only activates when it detects keywords like "remember this" — then it injects the full routing instructions (existing People, Projects, Areas) so Claude knows where to write. **This deterministic capture is why Remember achieves 100% capture rate** — unlike AI-guessing approaches used by Mem.ai or Reflect.

### Processing (Manual)

`/brain:process` uses `scripts/extract.py` to:
1. Find unprocessed JSONL transcripts in `~/.claude/projects/`
2. Extract clean user/assistant messages
3. Route content to the right second brain location (People, Projects, Journal, Notes, Tasks)
4. Update `Persona.md` with observed behavioral patterns

### Persona — An AI That Learns How You Think

`Persona.md` lives at your brain root and captures how you prefer to work — communication style, code preferences, workflow habits. It's loaded at every session start and updated during `/brain:process`. **No other second brain tool has this.** Not Mem.ai, not Reflect, not Notion AI.

---

## Configuration

`/brain:init` saves your chosen brain path to a persistent config that survives plugin updates.

Config location:
- **User scope** (default): `~/.claude/plugin-config/remember/config.json`
- **Project scope**: `.claude/plugin-config/remember/config.json`

The plugin reads config in this order:
1. User-scope config (persistent, created by `/brain:init`)
2. Project-scope config (persistent)
3. `config.defaults.json` shipped with the plugin (`~/remember`)

To change your second brain location after init:

```bash
cat ~/.claude/plugin-config/remember/config.json
```

```json
{
  "paths": {
    "data_root": "~/my-custom-path"
  }
}
```

---

## Note Format

All notes use YAML frontmatter + wikilinks (Obsidian-compatible):

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

---

## FAQ

**Q: How is this different from Mem.ai or Reflect?**
A: Remember is free, local-first, and captures 100% of your work deterministically (not AI guessing). Your data stays on your machine in Git-friendly markdown. No subscription, no cloud lock-in.

**Q: Can I use this with Obsidian?**
A: Yes! Remember creates Obsidian-compatible markdown with wikilinks, frontmatter, and PARA structure. It's the best free Obsidian AI plugin for automatic note-taking.

**Q: Is there a cloud/mobile version?**
A: Not yet. The free second brain plugin is local-only. A Pro cloud version with sync and mobile apps is planned.

**Q: How much does it cost?**
A: The plugin is 100% free and open source. Forever. No trials, no limits, no bait-and-switch.

**Q: What about Notion AI?**
A: Notion AI is a walled garden — your data is cloud-locked in proprietary format. Remember uses plain markdown you can take anywhere. Plus, Notion AI requires manual capture; Remember captures automatically.

**Q: Do I need Obsidian to use Remember?**
A: No. Remember works with any markdown editor. But Obsidian gives you the best experience with graph view, backlinks, and community plugins.

---

## Privacy & Data Ownership

- All data is **local markdown files** — nothing leaves your machine
- **No cloud, no telemetry, no tracking**
- **Git-friendly** — version control your entire second brain
- **No vendor lock-in** — plain markdown works everywhere
- Your knowledge base stays yours, forever

---

## Requirements

- Claude Code (latest version)
- Python 3 (for session extraction)
- Git (optional, for version control)

## Compatibility

Works with any markdown editor. Optimized for **Obsidian** (wikilinks, backlinks, graph view). Great as a free alternative to Mem.ai, Reflect, or Notion AI for developers who want local-first knowledge management.

---

## Credits

Built on ideas from:
- [continuous-learning-v2](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2) — Hooks architecture
- **PARA Method** (Tiago Forte) — Organization structure
- **Zettelkasten** (Niklas Luhmann) — Linked thinking

## License

MIT — see [LICENSE](LICENSE).

---

**Remember: The free, open-source second brain that builds itself.** Stop paying $120/year for AI note-taking. Start capturing knowledge automatically.

⭐ [Star on GitHub](https://github.com/remember-md/remember) if this is useful!
