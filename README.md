# Remember — The AI-Powered Second Brain That Builds Itself

> **Your second brain, in your terminal.** Zero-effort knowledge capture for developers who use Claude Code.

Remember is a **free**, **local-first**, **open-source** Claude Code plugin that captures your knowledge **deterministically** — plain markdown files that work with Obsidian, Logseq, or any text editor.

It automatically builds your second brain using **PARA + Zettelkasten** methodology. Say "remember this" during any coding session, and your knowledge lands in the right place — People, Projects, Notes, Journal — without you organizing anything.

**This is not another note-taking app.** This is an AI-powered knowledge base that captures while you work.

---

## Why Remember?

Every second brain tool asks you to do the work. Remember does it for you.

| Feature | Remember | Mem.ai | Reflect | Notion AI |
|---------|----------|--------|---------|-----------|
| **Model** | **Free & Open Source** | Subscription | Subscription | Freemium |
| **Capture** | **100% (deterministic hooks)** | AI-based | AI-based | Manual |
| **Privacy** | **Local-first** | Cloud | Cloud | Cloud |
| **Data Ownership** | **Full (Git)** | Limited | Limited | Locked-in |
| **Offline** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Obsidian Compatible** | ✅ Yes | ❌ No | ❌ No | ⚠️ Export only |
| **Open Source** | ✅ Yes | ❌ No | ❌ No | ❌ No |

---

## What Makes Remember Different

### 🎯 100% Deterministic Capture

Hooks-based capture (not AI inference) means nothing gets missed. When you say "remember this," it captures. Every. Single. Time. No probabilistic filtering — just reliable, predictable knowledge capture.

### 🔒 Privacy-First & Local

Your data lives on your machine, in Git-friendly markdown. No cloud servers, no terms of service on your thoughts. Your second brain is truly yours.

### 🆓 Free & Open Source

MIT licensed, community-driven, transparent development. The core plugin will always be free and open source.

### 🧠 AI-Native Architecture

Built for Claude Code from day one, designed for AI collaboration. The AI isn't an add-on — it's the interface. Claude understands PARA methodology, routes your knowledge automatically, and builds a **Persona.md** that learns how you think.

### 🔗 Obsidian-Native

PARA + Zettelkasten structure that works with your existing workflow. Remember creates **Obsidian-compatible markdown** with wikilinks, frontmatter, and full graph view support. Use Remember for AI-powered capture, Obsidian for beautiful browsing.

---

## Who Is This For?

✅ **You want a second brain but maintaining it feels like a second job**
✅ **You use Claude Code daily and want automatic knowledge capture**
✅ **You value privacy and data ownership (local-first, Git-friendly)**
✅ **You prefer open source and local-first tools**
✅ **You want full control over your data and workflow**
✅ **You want Obsidian's power + AI automation**

❌ Not for you if: You need mobile apps or cloud sync (coming in Remember Pro)

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
# 1. Add the marketplace
/plugin marketplace add remember-md/marketplace

# 2. Install the plugin
/plugin install remember

# 3. Initialize your second brain
/brain:init
```

`/brain:init` creates your second brain directory structure and Persona file (default: `~/remember`), and configures permissions automatically.

---

## Second Brain Structure

Remember organizes your knowledge base using PARA + Zettelkasten:

```
~/remember/
├── REMEMBER.md     # Your custom brain instructions (you edit this)
├── Persona.md      # Your behavioral patterns (auto-updated)
├── Inbox/          # Quick capture
├── Projects/       # Active work
├── Areas/          # Ongoing responsibilities
├── Notes/          # Permanent knowledge, decisions
├── Resources/      # Links, articles, references
├── Journal/        # Daily notes (YYYY-MM-DD.md)
├── People/         # One note per person
├── Tasks/          # Centralized task tracking
├── Templates/      # Note templates
└── Archive/        # Completed projects
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

`SessionStart` fires once and injects your Persona as model-visible context. `UserPromptSubmit` only activates when it detects keywords like "remember this" — then it injects the full routing instructions (existing People, Projects, Areas) so Claude knows where to write. **This deterministic approach achieves 100% capture rate** — every trigger is handled reliably and predictably.

### Processing (Manual)

`/brain:process` uses `scripts/extract.py` to:
1. Find unprocessed JSONL transcripts in `~/.claude/projects/`
2. Extract clean user/assistant messages
3. Route content to the right second brain location (People, Projects, Journal, Notes, Tasks)
4. Update `Persona.md` with observed behavioral patterns

### Persona — An AI That Learns How You Think

`Persona.md` lives at your brain root and captures how you prefer to work — communication style, code preferences, workflow habits. It's loaded at every session start and updated during `/brain:process`. This adaptive persona system is a core part of what makes Remember unique.

---

## Configuration

`/brain:init` writes your brain path to Claude Code's `settings.json` (auto-detects user vs project scope):

```json
{
  "env": { "REMEMBER_BRAIN_PATH": "~/remember" },
  "permissions": { "additionalDirectories": ["~/remember"] }
}
```

- **User scope** (default): `~/.claude/settings.json` — works across all projects
- **Project scope**: `.claude/settings.json` — project-specific brain path

To change your brain location, edit `REMEMBER_BRAIN_PATH` in the appropriate `settings.json`, or re-run `/brain:init`.

---

## Customize Your Brain

Edit `REMEMBER.md` in your brain root to customize how Remember works:

- **Capture Rules** — what to save, what to skip
- **Processing** — routing, formatting, tagging preferences
- **Custom Types** — define new entity types beyond PARA
- **Connections** — auto-linking rules, people context
- **Language** — multilingual capture/processing preferences
- **Templates** — override default note templates

`REMEMBER.md` is your file — Remember never auto-modifies it. It augments the built-in defaults; anything not specified uses standard behavior.

For full documentation, see [REMEMBER.md Guide](docs/REMEMBER-md-guide.md).

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

**Q: How does Remember compare to other Second Brain tools?**
A: Remember is free and open source, with a focus on local-first privacy and deterministic capture. Tools like Mem.ai and Reflect offer cloud sync and mobile apps (great features!), while Remember prioritizes data ownership and transparency. Choose what fits your workflow best!

**Q: Can I use this with Obsidian?**
A: Yes! Remember creates Obsidian-compatible markdown with wikilinks, frontmatter, and PARA structure. It's a great Obsidian companion for automatic note-taking.

**Q: Is there a cloud/mobile version?**
A: Not yet — see [Future Plans](#future-plans) below. The core plugin is local-only and always will be free.

**Q: How much does it cost?**
A: The core plugin is 100% free and open source. Always. Pro features (cloud, mobile) will be opt-in for those who want them.

**Q: Do I need Obsidian to use Remember?**
A: No. Remember works with any markdown editor. But Obsidian gives you the best experience with graph view, backlinks, and community plugins.

---

## Future Plans

**Remember Pro (Coming Soon)**
- ☁️ Cloud sync across devices
- 📱 Mobile apps (iOS & Android)
- 🌐 Web dashboard
- 👥 Team collaboration

The core plugin will always remain free and open source. Pro features are opt-in for those who want them.

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

Works with any markdown editor. Optimized for **Obsidian** (wikilinks, backlinks, graph view).

---

## Credits

Built on ideas from:
- [continuous-learning-v2](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2) — Hooks architecture
- **PARA Method** (Tiago Forte) — Organization structure
- **Zettelkasten** (Niklas Luhmann) — Linked thinking

## License

MIT — see [LICENSE](LICENSE).

---

**Remember: The free, open-source second brain that builds itself.** Start capturing knowledge automatically.

⭐ [Star on GitHub](https://github.com/remember-md/remember) if this is useful!
