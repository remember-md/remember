# Changelog

All notable changes to Remember will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Routing intelligence** — AI-driven classification for tasks (urgent/important/backlog), areas vs projects, persona learning, and resource capture
- Helper scripts: `persona_utils.py`, `task_utils.py` (replaced keyword-based detection with AI semantic understanding)

### Changed

- Task and persona detection now uses AI semantic analysis instead of regex patterns (multilingual support built-in)

## [1.0.0] - 2026-02-08

### Major Release: Skill to Plugin Transformation

Complete redesign from OpenClaw skill to Claude Code plugin.

### Added

- `.claude-plugin/plugin.json` — Claude Code plugin metadata
- `hooks/hooks.json` — UserPromptSubmit hook for session context + brain dump routing
- `scripts/user_prompt.sh` — Hook handler: loads Persona on first message, injects routing on brain dump keywords
- `scripts/extract.py` — Session transcript parser: extracts clean content from JSONL files
- `config.json` — Configurable brain path
- `commands/init.md` — `/brain:init` to create brain structure and Persona
- `commands/process.md` — `/brain:process` to route past sessions into brain
- `commands/status.md` — `/brain:status` to show brain file counts
- `skills/brain-session/SKILL.md` — Session context loader (loads Persona + recent context)
- PARA + Zettelkasten directory structure (Projects, People, Areas, Notes, Journal, Tasks, etc.)
- Obsidian-native wikilinks throughout
- Persona.md — behavioral patterns loaded every session, updated during processing

### Changed

- **README.md** — Rewritten for plugin usage
- **marketplace-entry.json** — Updated from skill to plugin

### Kept

- **SKILL.md** — Preserved for direct skill usage
- **LICENSE** — MIT (unchanged)
- **assets/templates/** — Note templates (unchanged)

### Breaking Changes

- Requires Claude Code (hooks needed for automatic context loading)
- Must run `/brain:init` after install

---

## [0.x] - Before 2026-02-08

Legacy versions as OpenClaw skill. See git history for details.

[1.0.0]: https://github.com/remember-md/remember/releases/tag/v1.0.0
