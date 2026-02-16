# Changelog

All notable changes to Remember will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.6.0] - 2026-02-16

### Added

- **Cascading REMEMBER.md support** — two levels of customization:
  - **Global:** `{brain}/REMEMBER.md` — user's universal preferences (existing behavior)
  - **Project:** `{project_root}/REMEMBER.md` — project-specific additions that layer on top
- Project sections **append** to global sections (not replace). If both have `## Capture Rules`, content is concatenated.
- `scripts/user_prompt.sh` now loads and merges both global and project REMEMBER.md files
- `skills/process/SKILL.md`, `skills/remember/SKILL.md`, `skills/init/SKILL.md` updated with cascading instructions
- New "Cascading: Global + Project" section in `docs/REMEMBER-md-guide.md` with full explanation and examples
- FAQ updated: project-specific REMEMBER.md is now supported

## [1.5.1] - 2026-02-16

### Changed

- **Skills refactored for Claude Code best practices:**
  - Progressive disclosure: split SKILL.md into concise instructions + reference.md (935→465 lines, -50%)
  - Skill names fixed: `brain:init`→`init`, `brain:process`→`process`, `brain:status`→`status` (colons invalid per spec, avoids double-namespace)
  - Commands: `/remember:init`, `/remember:process`, `/remember:status`
  - Removed invalid `user-invocable` frontmatter (not in official spec)
  - Shortened `remember` skill description to single line

### Removed

- **`brain-session` skill** — redundant with `session_start.sh` hook (same functionality)

### Fixed

- `config.defaults.json` version mismatch
- Missing CHANGELOG release links for v1.4.6 and v1.5.0

## [1.5.0] - 2026-02-16

### Added

- **REMEMBER.md** — User-editable instructions file for customizing brain behavior
  - `## Capture Rules` — define what to always/never capture, thresholds
  - `## Processing` — routing overrides, output style, tagging rules
  - `## Custom Types` — define entity types beyond standard PARA
  - `## Connections` — auto-linking rules and people context
  - `## Language` — multilingual capture/processing preferences
  - `## Templates` — override default note templates
  - `## Notes` — free-form context and preferences
- `/brain:init` now creates a starter `REMEMBER.md` with empty sections (Step 4b)
- Brain dump hook (`user_prompt.sh`) injects relevant REMEMBER.md sections as user overrides after default routing instructions
- `/brain:process` reads REMEMBER.md for routing, template, and capture customization (Step 1b)
- Brain dump skill reads REMEMBER.md for capture and processing overrides (Step 1b)
- Starter template at `assets/templates/remember.md`
- Full documentation guide at `docs/REMEMBER-md-guide.md`

### Design Principles

- **Pure Markdown** — no YAML/JSON schema, just headers and prose
- **All sections optional** — empty sections use defaults, zero config works exactly as before
- **Additive** — augments built-in behavior, explicit language needed to override
- **Never auto-modified** — user's file, never touched by `/brain:process` (unlike Persona.md)
- **Precedence:** REMEMBER.md > Built-in Defaults > Persona.md

## [1.4.6] - 2026-02-16

### Added

- **`scripts/build_index.py`** — New knowledge index builder that scans the brain and outputs formatted markdown tables (People, Projects, Areas, Notes, Tasks counts, Journal stats). Supports `--compact` mode for hook injection.
- **Knowledge-aware pipeline** — Both `/brain:process` and brain dump now build a Resolution Map against the knowledge index before writing, preventing duplicates and enabling smart entity linking.
- **Edit-first updates** — Skills now instruct the AI to use the `Edit` tool for surgical updates to existing files instead of rewriting entire files.
- **Pattern detection in Persona** — Enhanced behavioral pattern extraction: user corrections, stated preferences, repeated workflows, communication style, decision criteria, code style.

### Changed

- **`skills/process/SKILL.md`** — Complete rewrite. Now structured as 5 clear steps: (1) build knowledge index, (2) find unprocessed, (3) extract, (4) process with Resolution Map + Edit/Write routing, (5) mark & report. Reduced from ~500 lines of mixed concerns to focused pipeline.
- **`skills/remember/SKILL.md`** — Complete rewrite. Brain dump now runs `build_index.py --compact` first, builds Resolution Map, uses Edit tool for existing files and Write for new ones.
- **`scripts/user_prompt.sh`** — Hook now runs `build_index.py --compact` to inject full knowledge index (not just People/Projects/Areas names) into brain dump context.
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

[1.6.0]: https://github.com/remember-md/remember/releases/tag/v1.6.0
[1.5.1]: https://github.com/remember-md/remember/releases/tag/v1.5.1
[1.5.0]: https://github.com/remember-md/remember/releases/tag/v1.5.0
[1.4.6]: https://github.com/remember-md/remember/releases/tag/v1.4.6
[1.0.0]: https://github.com/remember-md/remember/releases/tag/v1.0.0
