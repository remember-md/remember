# 🧠 BrainRepo

**Auto-learning Second Brain plugin for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude-Code-7C3AED)](https://claude.ai/code)
[![AI Ready](https://img.shields.io/badge/AI-Powered-00D4AA)](https://github.com/codezz/brainrepo)

BrainRepo is a Claude Code plugin that automatically builds and evolves your Second Brain as you work:

- **📥 Auto-populates** Projects, People, Areas, Notes, Journal from your Claude sessions
- **🧠 Learns patterns** from your work (code style, workflow, communication)
- **🌱 Evolves knowledge** into executable skills and agents
- **💯 100% capture** via hooks (not probabilistic)
- **🤖 Zero manual work** - just code, BrainRepo maintains itself

---

## ✨ Features

### Automatic Second Brain Population
- **Projects/** - Auto-created when you work on projects
- **People/** - Auto-created when people are mentioned
- **Areas/** - Auto-detected recurring domains
- **Notes/** - Knowledge extracted from repeated patterns
- **Journal/** - Daily summaries of your sessions
- **Tasks/** - TODOs auto-captured and tracked

### Pattern Learning
- **Instincts** - Small learned behaviors (0.3-0.9 confidence)
- **Evolution** - Clusters of 5+ instincts → skills/agents
- **Cross-project** - Learns from ALL your Claude sessions
- **Evidence-based** - Links to journal entries and observations

### Privacy & Control
- **Local-first** - Your data stays on your machine
- **Git-friendly** - Commits content, not observations
- **Configurable** - Set your own data path
- **Export/Import** - Share patterns, not personal data

---

## 🚀 Quick Start

### 1. Install Plugin

**Clone to Claude plugins directory:**
```bash
git clone https://github.com/codezz/brainrepo.git ~/.claude/plugins/brainrepo
```

### 2. Initialize

Open Claude Code, run:
```
/brain:init
```

You'll be asked:
1. **Where to create your brain?** (default: `~/brainrepo` or custom path)
2. **Your name** (for identity)
3. **Technical level** (technical / semi-technical / non-technical / chaotic)
4. **Preferred language** (Romanian / English / Both)

BrainRepo creates the structure and you're ready!

### 3. Work Normally

Just use Claude Code! BrainRepo:
- Captures 100% of activity (via hooks)
- Processes every 5 min (background agent)
- Auto-populates your Second Brain
- Learns your patterns

### 4. Check Progress

```
/brain:status
```

See what's learned and what's ready to evolve.

### 5. Evolve (When Ready)

When 5+ patterns cluster:
```
/brain:evolve
```

Creates skills, agents, or knowledge notes.

---

## 📂 What Gets Created

After installation and `/brain:init`:

```
~/brainrepo/                          # (or your custom path)
├── content/                          # 🌟 Your Second Brain
│   ├── Inbox/                        # Quick captures
│   ├── Projects/                     # Auto-created projects
│   ├── People/                       # Auto-created people
│   ├── Areas/                        # Auto-detected domains
│   ├── Notes/                        # Knowledge extraction
│   ├── Resources/                    # Links & references
│   ├── Journal/                      # Daily summaries
│   ├── Tasks/                        # Task tracking
│   └── Templates/                    # Note templates
│
└── learning/                         # 📊 Meta-learning
    ├── observations/                 # Raw session data
    ├── instincts/                    # Learned patterns
    │   ├── personal/                 # Auto-learned
    │   └── inherited/                # Imported
    ├── evolved/                      # Generated artifacts
    │   ├── skills/
    │   ├── agents/
    │   └── commands/
    └── meta/                         # Stats & identity
```

---

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `/brain:init` | Initialize BrainRepo (run once) |
| `/brain:status` | Show stats, clustering, activity |
| `/brain:evolve` | Evolve clustered instincts |
| `/brain:export` | Share learned patterns (privacy-safe) |
| `/brain:import` | Adopt patterns from others |

---

## 🔄 How It Works

### 1. Capture (100% Reliable)

Hooks fire on **every** tool use:
```
PreToolUse → capture.sh → observations.jsonl
PostToolUse → capture.sh → observations.jsonl
Stop → on_stop.sh → update stats
```

No probabilistic skills - hooks are **deterministic**.

### 2. Process (Background Agent)

`brain-curator` agent runs every 5 min:

**Primary:** Auto-populate Second Brain
- Project detected → create/update `Projects/`
- Person mentioned → create/update `People/`
- Session ends → update `Journal/`
- Pattern 3x → create `Notes/`

**Secondary:** Learn patterns
- Observe behavior → create instincts
- Track confidence (0.3 → 0.9)
- Detect clustering (5+ → ready to evolve)

### 3. Evolve (Manual)

When clustering detected:
```
/brain:evolve
```

Synthesizes 5+ instincts into:
- **Skills** - Auto-triggered behaviors
- **Agents** - Specialist reasoning
- **Commands** - User-invoked actions
- **Notes** - Knowledge documentation

---

## ⚙️ Configuration

### Change Data Path (After Init)

Path is set during `/brain:init`, but you can change it later.

Edit `~/.claude/plugins/brainrepo/config.json`:

```json
{
  "paths": {
    "data_root": "/new/path/to/brain"
  }
}
```

**Note:** This changes WHERE commands look for your brain, but doesn't move existing data. You'll need to manually move the folder if you want to relocate it.

### Tune Observer Frequency

```json
{
  "curator": {
    "interval_minutes": 10    // Run every 10 min instead of 5
  }
}
```

### Adjust Detection Thresholds

```json
{
  "detection": {
    "project_threshold": 3,      // Require 3 sessions before creating project
    "pattern_threshold": 5       // Require 5 observations for pattern
  }
}
```

### Disable Auto-Population

```json
{
  "curator": {
    "auto_populate": {
      "people": false,           // Don't auto-create people
      "areas": false             // Don't auto-detect areas
    }
  }
}
```

---

## 🧬 Auto-Population Rules

| Entity | Trigger | Output | Threshold |
|--------|---------|--------|-----------|
| Project | Work in folder OR mention | `content/Projects/{name}/` | 1 session |
| Person | Name in conversation | `content/People/{name}.md` | 1 mention |
| Area | Recurring domain | `content/Areas/{domain}/` | 3 sessions |
| Note | Repeated pattern | `content/Notes/{topic}.md` | 3 observations |
| Task | TODO detected | `content/Tasks/tasks.md` | Immediate |
| Journal | Daily | `content/Journal/YYYY-MM-DD.md` | Session end |

---

## 🔒 Privacy & Security

### What's Stored Locally

**Observations** (never shared):
- Tool use events
- Timestamps
- Project context
- NO actual code/prompts

**Instincts** (shareable via export):
- Abstract patterns only
- Evidence descriptions (sanitized)
- No personal content

### Git Strategy

Default `.gitignore` (auto-created):
```
learning/observations/current.jsonl
learning/observations/archive/
```

**What gets committed:**
- ✅ content/ (Second Brain)
- ✅ learning/instincts/ (patterns)
- ✅ learning/evolved/ (skills)
- ❌ observations (privacy)

---

## 📊 Example After 1 Week

**Auto-created:**
- 5 Projects/ (dollie, project-a, staxwp, ...)
- 8 People/ (teammates, collaborators)
- 2 Areas/ (development, business)
- 12 Notes/ (patterns, solutions)
- 7 Journal/ entries
- 20 Tasks (extracted TODOs)

**Learned:**
- 18 instincts (code-style: 7, workflow: 5, communication: 4, decision: 2)
- 2 domains ready to evolve

**Evolved:**
- 1 skill: `my-code-style`
- 1 knowledge note: `Notes/Meta/my-workflow-philosophy.md`

**Manual effort:** Zero (except 2x `/brain:evolve`)

---

## 🤝 Sharing Patterns

### Export

```
/brain:export
```

Creates tarball of instincts (no personal data):
- ✅ Pattern descriptions
- ✅ Confidence scores
- ❌ No observations
- ❌ No actual code

### Import

```
/brain:import path/to/instincts.tar.gz
```

Imported patterns:
- Go to `learning/instincts/inherited/`
- Validated through observation
- Graduate to `personal/` if proven
- Auto-archived if contradicted

---

## 🔧 Troubleshooting

### Plugin not loading

Check installation:
```bash
ls -la ~/.claude/plugins/brainrepo/
```

Verify `plugin.json` exists.

### Brain-curator not running

Check config:
```json
{
  "curator": {
    "enabled": true    // Must be true
  }
}
```

### No observations captured

Check hooks are registered (restart Claude Code after install).

### Custom path not working

Ensure path is absolute or uses `~`:
```json
{
  "paths": {
    "data_root": "~/Documents/my-brain"    // ✅ Good
  }
}
```

---

## 📖 Documentation

- **README.md** (this file) - Quick start & overview
- **SKILL.md** - Detailed skill documentation (OpenClaw compatibility)
- **agents/brain-curator.md** - Curator agent logic
- **commands/*.md** - Command documentation
- **config.json** - Configuration reference

---

## 🎯 Architecture

### Plugin (Code)
```
~/.claude/plugins/brainrepo/
├── config.json
├── hooks/
├── scripts/
├── agents/
├── skills/
└── commands/
```

### Data (Content)
```
~/brainrepo/           # (or your custom path)
├── content/
└── learning/
```

**Clean separation:** Plugin (portable) ≠ Data (personal)

---

## 🧪 Compatibility

### Claude Code
✅ Primary target - full support

### OpenClaw
✅ SKILL.md preserved for compatibility  
⚠️ Hooks unavailable (OpenClaw doesn't support hooks yet)  
💡 Use as skill - manual observation

### Other Platforms
❌ Requires Claude Code hooks infrastructure

---

## 🙏 Inspiration

Based on best practices from:
- [continuous-learning-v2](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2) - Hooks + instincts
- [homunculus](https://github.com/humanplane/homunculus) - Confidence scoring + evolution
- [PARA Method](https://fortelabs.com/blog/para/) - Projects, Areas, Resources, Archive
- [Zettelkasten](https://zettelkasten.de/) - Atomic notes + wikilinks

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repo
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📄 License

MIT License - use freely, modify, share!

See [LICENSE](LICENSE) for details.

---

## 🌟 Support

- **Issues:** [GitHub Issues](https://github.com/codezz/brainrepo/issues)
- **Discussions:** [GitHub Discussions](https://github.com/codezz/brainrepo/discussions)
- **Star ⭐** if this helps you think better!

---

**Made with 🧠 for knowledge workers**

*Build a brain worth having.*
