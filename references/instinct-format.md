# Instinct Format Reference

**For Supabrain brain-curator agent**

## Problem

Obsidian YAML parser cannot handle complex nested structures in frontmatter.

**❌ Don't do this:**
```yaml
evidence:
  - type: observation
    timestamp: 2026-02-08T16:38:00Z
    context: "Description"
brain_context:
  related_notes: ["[[Note1]]", "[[Note2]]"]
```

**Result:** Obsidian shows "?" icon, cannot parse.

---

## Solution

**Keep frontmatter simple. Put complex data in body.**

---

## Correct Format

### Frontmatter (Simple Data Only)

```yaml
---
id: workflow-001-documentation
trigger: when making decisions or completing work
confidence: 0.85
domain: workflow
created: 2026-02-08
last_observed: 2026-02-08
observation_count: 10
related_notes: ["[[content/Notes/task-management-best-practices]]"]
related_projects: ["[[content/Projects/supabrain/supabrain]]"]
related_people: []
---
```

**Allowed in frontmatter:**
- ✅ Strings: `trigger: "when X happens"`
- ✅ Numbers: `confidence: 0.85`
- ✅ Dates: `created: 2026-02-08`
- ✅ Simple arrays: `related_notes: ["[[Note1]]", "[[Note2]]"]`
- ❌ Nested objects (use body instead)
- ❌ Multi-line values (use body instead)

---

### Body (Complex Details in Markdown)

```markdown
# Pattern Name

## Trigger
When this situation occurs...

## Pattern
Description of the observed behavior

## Action
What to do when triggered

## Reasoning
Why this pattern exists

## Evidence

**Observations:**
- 2026-02-08T16:38 - Requested research on task management
- 2026-02-08T16:08 - Decided rebrand after analysis
- 2026-02-08T16:52 - Approved structure alignment

**Notes & Journal:**
- [[content/Journal/2026-02-08]] - Full day log
- [[content/Notes/note-title]] - Relevant context

## Confidence
85% - Reasoning for confidence level (e.g., "Strong pattern, limited sample size")
```

---

## brain-curator Instructions

When creating instincts:

1. **Frontmatter = Simple**
   - id, trigger, confidence, domain, dates, counts
   - Simple arrays for related notes/projects/people
   - NO nested objects, NO multi-line strings

2. **Body = Detailed**
   - Evidence section with observations (timestamp + description)
   - Journal/note references with context quotes
   - Action steps, reasoning, pattern description
   - Confidence reasoning

3. **Wikilinks**
   - Use in both frontmatter arrays: `["[[Note]]"]`
   - Use in body: `[[content/Journal/2026-02-08]]`

4. **Timestamps**
   - Frontmatter dates: `2026-02-08` (simple)
   - Body observations: `2026-02-08T16:38` (human-readable)

---

## Template

```markdown
---
id: domain-NNN-short-name
trigger: when [situation]
confidence: 0.XX
domain: workflow | communication | decision-making | code-style
created: YYYY-MM-DD
last_observed: YYYY-MM-DD
observation_count: N
related_notes: []
related_projects: []
related_people: []
---

# Pattern Name

## Trigger
[When this happens]

## Pattern
[What is observed]

## Action
[What to do]
1. Step 1
2. Step 2

## Reasoning
[Why this pattern exists]

## Evidence

**Observations:**
- YYYY-MM-DDTHH:MM - Description
- YYYY-MM-DDTHH:MM - Description

**Notes & Journal:**
- [[content/Journal/YYYY-MM-DD]] - Quote or context
- [[content/Notes/note-title]] - Reference

## Confidence
XX% - [Reasoning for confidence level]
```

---

## Why This Matters

**Obsidian compatibility** = Users can browse instincts natively  
**Simple frontmatter** = Obsidian Dataview queries work  
**Structured body** = AI can parse easily, humans can read  

**Result:** Best of both worlds - machine-readable + human-friendly + Obsidian-compatible.
