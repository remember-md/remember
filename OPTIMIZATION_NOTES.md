# Optimization Notes — Remember Enhancement

## Overview

This update implements intelligent routing and learning capabilities:

1. **Areas Intelligence** — Decision tree for Project vs Area vs Note classification
2. **Task Routing Intelligence** — Auto-classification based on urgency keywords
3. **Persona Learning** — Evidence extraction from sessions for behavioral patterns
4. **Resource Capture Intelligence** — Auto-fetch metadata for URLs, create rich notes

---

## What Changed

### Skills Updated

**`skills/process/SKILL.md`**
- Added Areas Intelligence decision tree
- Added Task Routing Intelligence (urgent/important/backlog)
- Added Persona Learning (evidence extraction)
- Added Resource Capture Intelligence (URL metadata)
- Removed hardcoded project/person names (replaced with generic examples)

**`skills/brain-session/SKILL.md`**
- Removed hardcoded examples (no real project/person names)
- Simplified to focus on Persona loading

**`skills/remember/SKILL.md`**
- Added routing intelligence overview
- Added examples of new classification logic
- Updated routing table with new rules

### Scripts Added

**`scripts/task_router.py`**
- Classify tasks by urgency (urgent/important/backlog)
- Auto-route to tasks.md or project files
- Output formatted task with proper links

**`scripts/persona_learner.py`**
- Extract behavioral patterns from session text
- Detect corrections, preferences, workflows, communication style
- Update Persona.md Evidence Log automatically

**`scripts/resource_enricher.py`**
- Fetch URL metadata (title, author, description)
- Classify resource type (article/tool/video/book/documentation)
- Create rich notes in Resources/ with auto-linking

---

## Usage Examples

### Task Routing

```bash
# Classify a task
python3 scripts/task_router.py "Deploy site by Friday" --project myproject --date 2026-02-12

# Output:
{
  "urgency": "urgent",
  "destination": "tasks.md",
  "section": "Focus",
  "formatted": "- [ ] Deploy site by Friday [[Projects/myproject/myproject|Myproject]] ⚡ (2026-02-12)"
}
```

### Persona Learning

```bash
# Extract patterns from a session
python3 scripts/persona_learner.py session.md --persona-path ~/remember/Persona.md --date 2026-02-12

# Output: JSON with corrections, preferences, workflows
# Updates Persona.md Evidence Log automatically
```

### Resource Enrichment

```bash
# Enrich a URL
python3 scripts/resource_enricher.py "https://example.com/article" \
  --output ~/remember/Resources/articles/ \
  --date 2026-02-12

# Creates: Resources/articles/article-title.md with metadata
```

---

## Routing Logic

### Areas vs Projects vs Notes

**Decision Tree:**
1. Time-bound with deadline? → **Project**
2. Ongoing responsibility? → **Area**
3. One-off learning? → **Note**

**Examples:**
- "Started running daily" → `Areas/health.md` (ongoing)
- "Q1 campaign" → `Projects/q1-campaign/` (deadline)
- "Learned async patterns" → `Notes/async-patterns.md` (one-off)

### Task Classification

| Urgency | Keywords | Destination | Max |
|---------|----------|-------------|-----|
| Urgent | "by Friday", "asap", "urgent", "today" | tasks.md (Focus) | 10 |
| Important | "should", "need to", "reminder" | tasks.md (Next Up) | 15 |
| Backlog | "eventually", "Phase X", "v2" | project file | ∞ |

### Resource Types

Auto-detected based on URL domain and content:
- **Video:** youtube.com, vimeo.com
- **Documentation:** docs.*, readthedocs.io
- **Tool:** pages with "pricing", "features", "sign up"
- **Article:** default

---

## Integration with /brain:process

All optimizations are integrated into `/brain:process`:

1. **Session extraction** → clean markdown
2. **Content routing:**
   - Check Areas decision tree
   - Classify tasks by urgency
   - Enrich URLs with metadata
   - Extract project-specific notes to subfolders
3. **Persona learning:**
   - Scan for behavioral patterns
   - Update Evidence Log
4. **Report results** → summary of all changes

---

## Breaking Changes

None. All changes are additive — existing brains work without modification.

---

## Testing

Recommended test scenarios:

1. **Areas routing:**
   - "I started meditating daily" → should go to Areas/health.md
   - "Building landing page for Q1 launch" → should create Projects/landing-page/

2. **Task classification:**
   - "Deploy by Friday" → Focus (urgent)
   - "Research tools" → Next Up (important)
   - "Phase 2 features" → Project backlog

3. **Resource capture:**
   - Share URL → should fetch metadata and create rich note

4. **Persona learning:**
   - Process session with user corrections → Evidence Log should update

---

## Future Enhancements

- Semantic search via vector embeddings (remember-pro)
- Auto-linking enrichment (scan for related notes post-creation)
- Meeting intelligence (auto-extract participants, decisions, actions)
- Daily review automation (summary generation)

---

**Author:** Implemented Feb 2026  
**Version:** 1.4.0
