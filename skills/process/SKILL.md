---
name: process
description: Process unprocessed Claude Code sessions into your Second Brain
---

# /remember:process — Process Sessions into Second Brain

Reads unprocessed Claude Code transcripts and routes valuable content into your Second Brain using a knowledge-aware pipeline.

## ⚠️ Built-in Tools Only (NO Bash for file ops!)

| Operation | ✅ Use This | ❌ NOT This |
|-----------|------------|-------------|
| List files | `LS` tool | `bash ls` |
| Find files | `Glob` tool | `bash find` |
| Search content | `Grep` tool | `bash grep` |
| Read files | `Read` tool | `bash cat` |
| Create files | `Write` tool | `bash echo >` |
| Update files | `Edit` tool (old_string → new_string) | `bash sed` / rewrite |

**Only use bash for:** running Node.js scripts (`extract.js`, `build-index.js`).

---

## Step 1: Resolve Brain Path & Build Knowledge Index

1. Read `$REMEMBER_BRAIN_PATH` env var (fallback `~/remember`). Call this `{brain}`.
2. If directory doesn't exist → tell user to run `/remember:init` and stop.
3. Run the knowledge index:
   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/build-index.js
   ```
4. **Read the output carefully.** This is your map of everything that exists. Use it throughout all remaining steps to prevent duplicates and enable smart linking.

## Step 1b: Load User Instructions

Read REMEMBER.md files (cascading):
1. **Global:** `{brain}/REMEMBER.md` — user's universal preferences
2. **Project:** `{project_root}/REMEMBER.md` — project-specific additions (if exists)

Merge: project sections append to global sections. Both apply.

These contain explicit preferences for:
- **Capture Rules** — what to always/never capture
- **Processing** — routing overrides, output style, tagging rules
- **Custom Types** — entity types beyond standard PARA
- **Connections** — auto-linking rules, people context
- **Templates** — overrides for Journal, People, etc.

**These instructions take precedence over default routing in Step 4.**

If REMEMBER.md says "Never capture X" → skip X even if normally captured.
If it says "Route Y to Z" → route to Z even if defaults say otherwise.
If it defines a Custom Type → create files matching that specification.

## Step 2: Find Unprocessed Sessions

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js --unprocessed
```

With project filter:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js --unprocessed --project <name>
```

Show the list. Ask user which to process: **All**, **specific sessions by number**, or **Skip**.

## Step 3: Extract Each Session

For each selected session:
```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js <transcript_path>
```

Note the `**Session date (use for journal/tasks):**` line — use THAT date for everything (journal filenames, frontmatter, last_contact, task dates). Never use today's date.

## Step 4: Process Each Session

For each extracted session, do sub-steps 4a through 4e **with the knowledge index in context**.

Read `reference.md` (in this skill's directory) for detailed routing tables, templates, and classification rules.

### 4a. Build Resolution Map

For every name, project, topic in the session, resolve against the knowledge index:
- **Matches existing** → will use `Edit` tool to update
- **New entity** → will use `Write` tool to create
- **Fuzzy matching:** "John", "john smith", "John S." all resolve to `People/john-smith.md` if exists

### 4b. Classify Content (with User Instructions)

Before classifying, check REMEMBER.md:
1. **Capture Rules** → apply Always/Never filters FIRST
2. **Processing → Routing Overrides** → apply before default routing table
3. **Custom Types** → check if content matches user-defined type
4. Then fall through to default classification table (see `reference.md`)

**Skip:** routine code generation, debugging noise, tool call chatter, system messages.

### 4c. Update EXISTING Files (Edit Tool)

Use the `Edit` tool for surgical updates. Do NOT rewrite whole files.
- Update frontmatter `updated:` field to SESSION_DATE (only if newer)
- See `reference.md` for per-type update patterns (People, Projects, Journal, Tasks, Areas)

### 4d. Create NEW Files (Write Tool)

Check REMEMBER.md `## Templates` section first:
- If user defined a template override → use their template
- Otherwise → use templates from `reference.md`

Use `[[wikilinks]]` everywhere. Link forward; Obsidian handles backlinks.

### 4e. Update Persona.md — Behavioral Pattern Detection

After all content is routed, analyze the session for patterns:
1. **User corrections** — what do they actually prefer?
2. **Stated preferences** — "I prefer X", "Never use Z"
3. **Repeated workflows** — same sequence appears again
4. **Communication style** — concise vs detailed, language switching
5. **Decision criteria** — speed vs quality, simplicity vs features
6. **Code/technical style** — naming, frameworks, architecture

Read current Persona.md first. Add evidence lines with `[{SESSION_DATE}]` prefix.
Skip if no clear patterns found. Better to miss than hallucinate.

## Step 5: Mark Processed & Report

```bash
node ${CLAUDE_PLUGIN_ROOT}/scripts/extract.js --mark-processed <session_id>
```

Report summary:
```
Brain updated from {N} sessions:

Created:
  - People/john-smith.md (new)
  - Notes/decision-api-architecture.md (new)

Updated:
  - Journal/2026-02-09.md (+2 sections)
  - Projects/myproject/myproject.md (log entry)
  - Tasks/tasks.md (+3 tasks)
  - Persona.md (+2 evidence lines)

Processed: {N} sessions
Remaining unprocessed: {M}
```

## Error Handling

- extract.py fails → show error, skip session, continue with others
- File write fails → warn user, continue with remaining
- No unprocessed sessions → tell user, suggest "remember this:" for immediate capture
- web_fetch fails → create minimal resource note, flag for review
