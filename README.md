# 🧠 Supabrain - AI-Powered Second Brain That Builds Itself

**Your personal AI brain that learns, organizes, and evolves as you work**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude-Code-7C3AED)](https://claude.ai/code)
[![AI Powered](https://img.shields.io/badge/AI-Powered-00D4AA)](https://github.com/codezz/supabrain)
[![Second Brain](https://img.shields.io/badge/Second-Brain-FF6B6B)](https://github.com/codezz/supabrain)

> **Stop maintaining notes manually. Start building a brain that maintains itself.**

Supabrain is an **AI-powered Second Brain plugin** for Claude Code that automatically captures your work, learns from your patterns, and evolves into a personalized knowledge management system—zero manual work required.

Perfect for knowledge workers, developers, creators, and anyone building a digital brain.

---

## 🎯 What is Supabrain?

**Supabrain** transforms Claude Code into your **automatic Second Brain**:

- 🧠 **Second Brain Automation** - Auto-captures projects, people, notes, and tasks as you work
- 🤖 **AI Brain Dump** - Instant brain dumps via Claude—no manual note-taking
- 📊 **Personal Knowledge Management (PKM)** - PARA + Zettelkasten structure built automatically
- 🌱 **Self-Learning AI** - Learns your code style, workflow, and communication patterns
- 💡 **Smart Knowledge Base** - Automatically organizes and links your knowledge
- 🔄 **Pattern Evolution** - Clusters insights into executable skills and agents
- 💯 **100% Capture Rate** - Deterministic hooks, not probabilistic prompts
- 🔒 **Privacy-First** - Local storage, Git-friendly, your data stays yours

**Supabrain = Obsidian + Notion + AI Personal Assistant + Automatic Note-Taking**

---

## ✨ Key Features

### 🧠 Automatic Second Brain Building

Build your **Second Brain** without manual effort:

- **Projects/** - Auto-created when you code or discuss projects
- **People/** - Auto-captured when colleagues/collaborators are mentioned
- **Areas/** - Auto-detected recurring life/work domains
- **Notes/** - Knowledge extracted from repeated patterns and insights
- **Journal/** - Daily brain dumps of your sessions (automatic journaling)
- **Tasks/** - TODOs auto-extracted and tracked
- **Resources/** - Links and references organized automatically

**Like Building a Second Brain by Tiago Forte, but fully automated with AI.**

### 🤖 AI-Powered Knowledge Management

Your **AI brain** that learns YOU:

- **Pattern Learning** - Observes how you work, code, and communicate
- **Instinct Formation** - Small learned behaviors (code style, workflow preferences)
- **Knowledge Evolution** - Clusters 5+ patterns → skills, agents, or evergreen notes
- **Cross-Project Learning** - Synthesizes insights across ALL your work
- **Evidence-Based** - Every pattern links to actual observations

**Smart Notes meet AI: Zettelkasten-inspired, AI-powered.**

### 📥 Brain Dump Made Easy

**Instant brain dump** via Claude Code:

- Talk to Claude → Supabrain captures everything
- No need to manually file notes
- Auto-categorizes and links knowledge
- Daily journal summaries generated automatically
- Voice your thoughts, let AI organize them

**The ultimate brain dump tool for knowledge workers.**

### 🔗 Linked Thinking & Knowledge Graph

Build your **personal knowledge graph** automatically:

- Auto-links related notes, people, and projects
- Discovers connections you didn't see
- Creates evergreen notes from patterns
- Bi-directional links (like Obsidian, Roam Research)
- Graph your knowledge, effortlessly

### 🎨 PARA + Zettelkasten Hybrid

Best of both worlds:

- **PARA structure** (Projects, Areas, Resources, Archive) for organization
- **Zettelkasten principles** (atomic notes, links, emergence) for thinking
- **AI-driven** population and linking
- **Markdown files** - portable, future-proof, compatible with Obsidian/Logseq

**Digital garden meets productivity system.**

---

## 🚀 Quick Start

### 1. Install the Plugin

**Clone to your Claude Code plugins directory:**

```bash
git clone https://github.com/codezz/supabrain.git ~/.claude/plugins/supabrain
```

### 2. Initialize Your Second Brain

Open **Claude Code** and run:

```
/brain:init
```

**Setup prompts (30 seconds):**
1. **Brain location?** (default: `~/supabrain` or custom path)
2. **Your name?** (for identity)
3. **Technical level?** (technical / semi-technical / non-technical / chaotic)
4. **Language?** (English / Romanian / Both)

**Done!** Supabrain creates your PARA structure and starts learning.

### 3. Work Normally in Claude Code

Just use Claude Code like you always do:

- Code, ask questions, brainstorm, plan
- Supabrain captures **everything** (100% deterministic)
- Background AI agent processes every 5 minutes
- Your Second Brain auto-populates
- Patterns learned automatically

**Zero manual note-taking. Zero manual organization.**

### 4. Check Your Brain

```
/brain:status
```

See what's been captured, what patterns are forming, what's ready to evolve.

### 5. Evolve Knowledge (Optional)

When 5+ patterns cluster together:

```
/brain:evolve
```

AI synthesizes patterns into:
- **Skills** - Executable behaviors
- **Agents** - Specialist reasoners
- **Knowledge Notes** - Documented insights

---

## 📂 Your Second Brain Structure

After `/brain:init`, Supabrain creates:

```
~/supabrain/                          # Your personal AI brain
├── content/                          # 🧠 Your Second Brain (PARA)
│   ├── Inbox/                        # Brain dumps & quick captures
│   ├── Projects/                     # Active projects (auto-created)
│   │   ├── my-app/
│   │   ├── staxwp/
│   │   └── personal-site/
│   ├── People/                       # Contacts & collaborators (auto-captured)
│   │   ├── alice.md
│   │   ├── roxana.md
│   │   └── clients/
│   ├── Areas/                        # Life/work domains (auto-detected)
│   │   ├── development/
│   │   ├── business/
│   │   └── health/
│   ├── Notes/                        # Evergreen notes & knowledge
│   │   ├── code-patterns/
│   │   ├── design-decisions/
│   │   └── learnings/
│   ├── Resources/                    # Links, references, tools
│   ├── Journal/                      # Daily brain dumps (automatic)
│   │   ├── 2026-02-08.md
│   │   └── 2026-02-09.md
│   ├── Tasks/                        # Task tracking
│   │   └── tasks.md
│   └── Templates/                    # Note templates
│
└── learning/                         # 🤖 AI Learning System
    ├── observations/                 # Raw session captures
    ├── instincts/                    # Learned patterns
    │   ├── personal/                 # Your patterns
    │   └── inherited/                # Imported patterns
    ├── evolved/                      # AI-generated artifacts
    │   ├── skills/
    │   ├── agents/
    │   └── commands/
    └── meta/                         # Stats & identity
```

**Compatible with Obsidian, Logseq, and any Markdown editor.**

---

## 🎮 Commands

| Command | Description | Use Case |
|---------|-------------|----------|
| `/brain:init` | Initialize your Second Brain | First-time setup |
| `/brain:status` | View stats, patterns, activity | Check what's learning |
| `/brain:evolve` | Synthesize clustered patterns | Create skills/agents |
| `/brain:export` | Share learned patterns | Collaborate, backup |
| `/brain:import` | Adopt others' patterns | Learn from community |

---

## 💡 Use Cases

### For Developers

- **Code style learning** - AI learns your preferences, enforces consistency
- **Project documentation** - Auto-generates project notes and READMEs
- **Decision logging** - Captures architecture decisions automatically
- **Refactoring knowledge** - Learns from your refactoring patterns
- **Collaboration context** - Auto-tracks teammates and their expertise

### For Knowledge Workers

- **Meeting notes** - Auto-captures people, decisions, action items
- **Research organization** - Auto-files insights into your knowledge base
- **Writing assistant** - Learns your writing style and preferences
- **Idea management** - Brain dumps instantly organized
- **Cross-project insights** - Synthesizes learnings across all work

### For Creators & Entrepreneurs

- **Content ideas** - Auto-captures inspiration as you work
- **Client management** - Auto-tracks clients and project context
- **Business patterns** - Learns what works, what doesn't
- **Knowledge monetization** - Organized insights = products/courses
- **Personal brand** - Documented expertise and thought leadership

### For Students & Researchers

- **Automatic note-taking** - Capture lectures, readings, discussions
- **Literature review** - Auto-organized research notes
- **Thesis/paper writing** - Knowledge graph of your research
- **Study patterns** - AI learns your learning style
- **Citation management** - Auto-tracks sources and references

---

## 🔄 How It Works (The Magic Behind Your AI Brain)

### 1. 📥 Capture (100% Deterministic)

**Hooks fire on EVERY tool use** (not probabilistic):

```
You work in Claude Code
        ↓
PreToolUse hook → capture.sh → observations.jsonl
        ↓
PostToolUse hook → capture.sh → observations.jsonl
        ↓
Session ends → on_stop.sh → stats update
```

**Result:** Zero missed context. True 100% capture rate.

### 2. 🤖 Process (Background AI Agent)

**brain-curator** AI agent runs every 5 minutes:

**Primary Mission:** Auto-populate your Second Brain

- Project detected → create/update `Projects/{name}/`
- Person mentioned → create/update `People/{name}.md`
- Session ends → generate `Journal/YYYY-MM-DD.md`
- Pattern repeats 3x → create evergreen note in `Notes/`
- TODO detected → add to `Tasks/tasks.md`

**Secondary Mission:** Learn patterns

- Observe your behavior → create instincts
- Track confidence (0.3 → 0.9)
- Detect clustering (5+ similar patterns)
- Flag ready-to-evolve knowledge

### 3. 🌱 Evolve (Manual Trigger)

When clustering detected, you run:

```
/brain:evolve
```

AI synthesizes 5+ instincts into:

- **Skills** - Auto-triggered behaviors (e.g., "my-code-style")
- **Agents** - Specialist reasoning modes (e.g., "architecture-reviewer")
- **Commands** - User-invoked actions (e.g., "/review-pr")
- **Notes** - Documented knowledge (e.g., "My Workflow Philosophy")

**Your Second Brain becomes executable.**

---

## 🧬 Automatic Knowledge Population Rules

| Entity | Trigger | Output | Threshold |
|--------|---------|--------|-----------|
| **Project** | Work in folder OR discuss project | `content/Projects/{name}/` | 1 session |
| **Person** | Name mentioned in conversation | `content/People/{name}.md` | 1 mention |
| **Area** | Recurring domain/responsibility | `content/Areas/{domain}/` | 3 sessions |
| **Note** | Repeated insight/pattern | `content/Notes/{topic}.md` | 3 observations |
| **Task** | TODO/action item detected | `content/Tasks/tasks.md` | Immediate |
| **Journal** | Daily activity summary | `content/Journal/YYYY-MM-DD.md` | Session end |

**Smart Notes that write themselves.**

---

## 📊 Real Example: After 1 Week of Use

**Auto-created in your Second Brain:**

```
content/
├── Projects/         (5 projects auto-created)
│   ├── my-app/
│   ├── staxwp/
│   ├── supabrain/
│   ├── minecraft-dash/
│   └── 99-marketing/
├── People/           (8 people auto-captured)
│   ├── alice.md
│   ├── roxana.md
│   ├── cezar.md
│   └── clients/
│       ├── impact3.md
│       └── john-doe.md
├── Areas/            (2 domains auto-detected)
│   ├── development/
│   └── business/
├── Notes/            (12 evergreen notes created)
│   ├── code-patterns/
│   │   ├── react-best-practices.md
│   │   └── error-handling.md
│   ├── design-decisions/
│   └── learnings/
├── Journal/          (7 daily summaries)
│   ├── 2026-02-02.md
│   ├── 2026-02-03.md
│   └── ...
└── Tasks/            (20 TODOs extracted)
    └── tasks.md
```

**Patterns learned:**

- 18 instincts (code-style: 7, workflow: 5, communication: 4, decision: 2)
- 2 domains ready to evolve
- 1 skill evolved: `my-code-style`
- 1 knowledge note: `Notes/Meta/my-workflow-philosophy.md`

**Your manual effort:** Zero (except 2x `/brain:evolve`)

**Your Second Brain is building itself.**

---

## 🆚 Comparison: Supabrain vs. Alternatives

| Feature | Supabrain | Obsidian | Notion | Mem.ai | Reflect |
|---------|-----------|----------|--------|--------|---------|
| **Auto-capture** | ✅ 100% | ❌ Manual | ❌ Manual | ⚠️ Partial | ⚠️ Partial |
| **AI Learning** | ✅ Yes | ❌ No | ⚠️ Limited | ✅ Yes | ✅ Yes |
| **Pattern Evolution** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |
| **Local-First** | ✅ Yes | ✅ Yes | ❌ Cloud | ❌ Cloud | ❌ Cloud |
| **Git-Friendly** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Price** | ✅ Free (OSS) | ✅ Free | 💵 $8-10/mo | 💵 $8-15/mo | 💵 $10/mo |
| **Claude Code** | ✅ Native | ❌ No | ❌ No | ❌ No | ❌ No |
| **PARA Structure** | ✅ Yes | ⚠️ Manual | ⚠️ Manual | ❌ No | ❌ No |
| **Zettelkasten** | ✅ Yes | ✅ Yes | ⚠️ Limited | ❌ No | ❌ No |

**Supabrain = Obsidian's power + Notion's ease + AI automation**

---

## ⚙️ Configuration & Customization

### Change Brain Location

Edit `~/.claude/plugins/supabrain/config.json`:

```json
{
  "paths": {
    "data_root": "~/Documents/my-brain"
  }
}
```

### Adjust AI Curator Frequency

```json
{
  "curator": {
    "interval_minutes": 10    // Process every 10 min (default: 5)
  }
}
```

### Fine-Tune Detection Thresholds

```json
{
  "detection": {
    "project_threshold": 3,      // Need 3 sessions before creating project
    "pattern_threshold": 5,      // Need 5 observations for pattern
    "confidence_min": 0.3        // Minimum confidence for instinct
  }
}
```

### Disable Specific Auto-Population

```json
{
  "curator": {
    "auto_populate": {
      "people": false,           // Don't auto-create people notes
      "areas": false,            // Don't auto-detect areas
      "journal": true,           // Keep daily journal (recommended)
      "tasks": true              // Keep task extraction
    }
  }
}
```

---

## 🔒 Privacy & Security (Your Brain, Your Data)

### What's Stored Locally

**Observations** (never shared):
- Tool use events (which tools you use, when)
- Project context (folder names, not content)
- Timestamps
- ❌ NO actual code or prompts stored

**Instincts** (shareable if you choose):
- Abstract patterns (e.g., "prefers arrow functions")
- Confidence scores
- Evidence pointers (sanitized)
- ❌ NO personal/private content

### Git Strategy (Smart Privacy)

Auto-created `.gitignore`:

```
learning/observations/current.jsonl
learning/observations/archive/
```

**What gets committed to Git:**
- ✅ content/ (your Second Brain notes)
- ✅ learning/instincts/ (learned patterns)
- ✅ learning/evolved/ (skills & agents)
- ❌ observations/ (raw capture - stays private)

**Your knowledge is yours. Forever.**

### Export & Import (Privacy-Safe Sharing)

**Export patterns:**
```
/brain:export
```
Creates tarball of instincts (NO personal data, NO observations).

**Import patterns from others:**
```
/brain:import path/to/patterns.tar.gz
```

Imported patterns validated through YOUR observations before adoption.

**Share knowledge, not secrets.**

---

## 🤝 Community & Ecosystem

### Share Patterns (Optional)

Export your learned patterns (privacy-safe) and share with:
- Teammates (standardize workflows)
- Open source community
- Students/mentees
- Future you (backup)

### Import Community Patterns

Learn from others' exported patterns:
- Coding best practices
- Workflow optimizations
- Communication styles
- Domain expertise

**Build on collective knowledge.**

### Compatible With

- **Obsidian** - Open `.md` files directly
- **Logseq** - Import as graph database
- **VS Code** - View/edit with Markdown preview
- **Git** - Version control your brain
- **Any text editor** - Plain Markdown files

**Portable knowledge. No vendor lock-in.**

---

## 🎓 Methodology & Philosophy

Supabrain combines proven knowledge management methodologies:

### 📚 Building a Second Brain (Tiago Forte)

- **PARA structure** (Projects, Areas, Resources, Archive)
- **Capture, Organize, Distill, Express** workflow
- But **automated with AI** - zero manual sorting

### 🗂️ Zettelkasten (Niklas Luhmann)

- **Atomic notes** - one idea per note
- **Wikilinks** - bi-directional connections
- **Emergence** - knowledge evolves from links
- But **AI-driven** - auto-linking and synthesis

### 🧠 Personal Knowledge Management (PKM)

- **Evergreen notes** - timeless, grow over time
- **Progressive summarization** - distill insights
- **Linked thinking** - knowledge graphs
- But **AI-augmented** - pattern detection and clustering

### 🌱 Digital Garden

- **Learn in public** (optional - your choice)
- **Notes evolve** - not static documents
- **Serendipity** - discover unexpected connections
- But **AI-cultivated** - automatic growth

**Stop maintaining notes. Start cultivating knowledge.**

---

## 🧪 Technical Details

### Requirements

- **Claude Code** (latest version)
- **Node.js** 18+ (for background agent)
- **Git** (optional, for version control)
- **Markdown editor** (optional, e.g., Obsidian)

### Architecture

**Plugin (Portable):**
```
~/.claude/plugins/supabrain/
├── config.json              # Configuration
├── hooks/                   # Capture hooks
├── scripts/                 # Processing scripts
├── agents/                  # AI curator
├── commands/                # User commands
└── skills/                  # OpenClaw compat
```

**Data (Personal):**
```
~/supabrain/                 # (or your custom path)
├── content/                 # Your Second Brain
└── learning/                # AI learning system
```

**Clean separation:** Code ≠ Data. Portable and privacy-preserving.

### Compatibility

| Platform | Support | Notes |
|----------|---------|-------|
| **Claude Code** | ✅ Full | Primary target, all features |
| **OpenClaw** | ⚠️ Partial | SKILL.md included, hooks unavailable |
| **Other AI tools** | ❌ No | Requires Claude Code hooks |

---

## 📚 Documentation

- **README.md** (this file) - Quick start & overview
- **SKILL.md** - Detailed skill documentation
- **agents/brain-curator.md** - AI curator logic
- **commands/*.md** - Command documentation
- **references/** - Methodology & examples

---

## 🙏 Inspiration & Credits

Built on the shoulders of giants:

- [continuous-learning-v2](https://github.com/affaan-m/everything-claude-code/tree/main/skills/continuous-learning-v2) - Hooks architecture
- [homunculus](https://github.com/humanplane/homunculus) - Confidence scoring & evolution
- **PARA Method** (Tiago Forte) - Organization structure
- **Zettelkasten** (Niklas Luhmann) - Linked thinking
- **Building a Second Brain** (Tiago Forte) - Knowledge management philosophy
- **How to Take Smart Notes** (Sönke Ahrens) - Note-taking methodology

---

## 🤝 Contributing

**Contributions welcome!**

Ways to contribute:
1. 🐛 Report bugs via [GitHub Issues](https://github.com/codezz/supabrain/issues)
2. 💡 Suggest features via [GitHub Discussions](https://github.com/codezz/supabrain/discussions)
3. 🔧 Submit Pull Requests
4. 📖 Improve documentation
5. 🌟 Share your learned patterns (export → community repo)
6. ⭐ Star the repo if it helps you!

**Join the knowledge revolution.**

---

## 🗺️ Roadmap

### v1.x (Current - Free OSS)
- ✅ Automatic Second Brain population
- ✅ Pattern learning & instinct formation
- ✅ Evolution system (skills/agents)
- ✅ Privacy-first local storage
- ✅ Git-friendly structure
- ✅ Export/import patterns

### v2.0 (Planned)
- 🔜 Web dashboard (browse your brain)
- 🔜 Visual knowledge graph
- 🔜 Mobile app (iOS/Android)
- 🔜 Telegram/WhatsApp capture bot
- 🔜 Cloud sync (optional Pro tier)
- 🔜 Team collaboration
- 🔜 API access

**Current version is 100% free and open source. Forever.**

---

## 💬 Support & Community

- **Documentation:** [GitHub Wiki](https://github.com/codezz/supabrain/wiki)
- **Issues:** [GitHub Issues](https://github.com/codezz/supabrain/issues)
- **Discussions:** [GitHub Discussions](https://github.com/codezz/supabrain/discussions)
- **Star ⭐ the repo** - helps others discover Supabrain
- **Share on Twitter/LinkedIn** - spread the word

**Questions? Open an issue. We're here to help.**

---

## 📄 License

**MIT License** - free to use, modify, and share.

See [LICENSE](LICENSE) for full details.

**Your brain, your rules. No strings attached.**

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=codezz/supabrain&type=Date)](https://star-history.com/#codezz/supabrain&Date)

---

## 🧠 Keywords & Topics

**AI & Automation:**
ai brain, ai note taking, ai knowledge management, ai personal assistant, automatic note taking, ai productivity, ai learning, machine learning knowledge base

**Second Brain & PKM:**
second brain, building a second brain, digital brain, personal knowledge management, pkm, knowledge base, knowledge management system, personal wiki, brain dump, mind dump

**Note-Taking & Organization:**
note taking, smart notes, evergreen notes, atomic notes, linked thinking, zettelkasten, digital garden, note automation, automatic journaling

**Productivity & Tools:**
productivity tool, workflow automation, obsidian alternative, notion alternative, roam research, logseq, knowledge graph, mind map, personal database

**Claude & AI:**
claude ai, claude code, claude plugin, ai assistant, ai agent, conversational ai, llm tool, gpt alternative

**Methodology:**
para method, second brain method, zettelkasten method, linked notes, bi-directional links, progressive summarization, personal knowledge graph

---

## 🎉 Get Started Today

**Stop manually managing notes. Let AI build your Second Brain.**

```bash
# 1. Clone the plugin
git clone https://github.com/codezz/supabrain.git ~/.claude/plugins/supabrain

# 2. Open Claude Code

# 3. Run /brain:init

# 4. Work normally - your brain builds itself!
```

**⭐ Star the repo | 🍴 Fork it | 📢 Share it**

---

**Made with 🧠 by knowledge workers, for knowledge workers**

*Build a brain worth having. Build Supabrain.*
