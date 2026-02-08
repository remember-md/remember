---
name: brain:import
description: Import instincts from others (goes to inherited/)
---

# /brain:import - Import Instincts

Imports instincts from external source into `inherited/` folder (kept separate from personal learning).

## Usage

```
/brain:import path/to/instincts.tar.gz
```

## What it does

### 1. Validate Archive

Check manifest.json:

```javascript
const manifest = await readManifestFromArchive(archivePath);

// Validate
if (!manifest.supabrain_version) {
  throw new Error('Invalid BrainRepo export');
}

console.log(`
Importing instincts from: ${manifest.author}
Export date: ${manifest.export_date}
Domains: ${Object.keys(manifest.domains).join(', ')}
Total: ${manifest.total_instincts} instincts
`);
```

### 2. Preview Import

Show what will be imported:

```
📥 Import Preview

Source: User's instincts (2026-02-08)

Domains to import:
✓ code-style (7 instincts, avg confidence 0.75)
  - prefer-typescript
  - functional-components
  - strict-mode
  - no-any
  - named-exports
  - arrow-functions
  - destructuring

✓ workflow (5 instincts, avg confidence 0.82)
  - test-before-commit
  - commit-granular
  - auto-capture-links
  - daily-review
  - weekly-planning

Total: 18 instincts

These will be imported to:
~/supabrain/learning/instincts/inherited/

Proceed? (y/n)
```

### 3. Extract to inherited/

If user confirms:

```bash
cd ~/supabrain/learning/instincts/inherited/
tar -xzf /path/to/instincts.tar.gz

# Structure:
inherited/
├── gabi-20260208/                # Namespaced by author+date
│   ├── code-style/
│   │   ├── prefer-typescript.md
│   │   └── ...
│   ├── workflow/
│   └── manifest.json
```

### 4. Add Source Metadata

For each imported instinct, prepend:

```yaml
---
# Original frontmatter...
imported_from:
  author: "User"
  date: "2026-02-08"
  source_confidence: 0.75
inherited: true
---

> **Note:** This instinct was imported from [User's patterns].
> Your mileage may vary - observe how it works for you.

# [Original content...]
```

### 5. Track in Stats

Update `~/supabrain/learning/meta/stats.json`:

```json
{
  "imports": [
    {
      "date": "2026-02-08",
      "author": "User",
      "instincts_count": 18,
      "domains": ["code-style", "workflow", "communication", "decision-making"],
      "namespace": "gabi-20260208"
    }
  ]
}
```

### 6. Suggest Review

```
✅ Import Complete

Imported 18 instincts from User to:
~/supabrain/learning/instincts/inherited/gabi-20260208/

These instincts are kept SEPARATE from your personal learning.

Next steps:
1. Review imported patterns
2. As you work, brain-curator will observe:
   - If imported pattern matches your style → confidence ↑
   - If you contradict it → confidence ↓
3. Strong matches may evolve into personal instincts

View imported:
ls ~/supabrain/learning/instincts/inherited/gabi-20260208/
```

## How Inherited Instincts Work

### Initial State
- Confidence = source confidence (e.g., 0.75)
- Marked as `inherited: true`
- Kept in separate `inherited/` folder

### During Work
Brain-curator observes:

```javascript
// If your behavior matches inherited instinct
if (matchesPattern(observation, inheritedInstinct)) {
  inheritedInstinct.confidence += 0.05;
  inheritedInstinct.observation_count += 1;
  
  // If reaches 0.8+ and observed 5+ times
  if (inheritedInstinct.confidence >= 0.8 && 
      inheritedInstinct.observation_count >= 5) {
    // Graduate to personal
    moveToPersonal(inheritedInstinct);
  }
}

// If you contradict inherited instinct
if (contradictsPattern(observation, inheritedInstinct)) {
  inheritedInstinct.confidence -= 0.1;
  
  // If drops below 0.3
  if (inheritedInstinct.confidence < 0.3) {
    // Archive (doesn't work for you)
    archiveInstinct(inheritedInstinct);
  }
}
```

### Graduation
When inherited instinct proves valuable:

```bash
# Moves from:
learning/instincts/inherited/gabi-20260208/code-style/prefer-typescript.md

# To:
learning/instincts/personal/code-style/prefer-typescript.md

# With updated metadata:
imported_from: [kept for history]
graduated: true
graduated_date: "2026-02-15"
```

## Import Options

```bash
# Standard import (review first)
/brain:import path/to/instincts.tar.gz

# Auto-approve (skip confirmation)
/brain:import path/to/instincts.tar.gz --yes

# Import specific domain only
/brain:import path/to/instincts.tar.gz --domain code-style

# Import with lower initial confidence
/brain:import path/to/instincts.tar.gz --confidence 0.5
```

## Sources

Import from:
1. **Teammates:** Share code-style/workflow patterns
2. **Community:** Import popular pattern packs
3. **Yourself:** Restore from backup
4. **Cross-machine:** Sync patterns between computers

## Safety

- ✅ Kept separate from personal learning
- ✅ Can be removed without affecting personal instincts
- ✅ Gradually validated through observation
- ✅ Low-value patterns auto-archived

## Notes

- Multiple imports supported (namespaced by author+date)
- Can import same author multiple times (different namespaces)
- Graduation to personal is automatic (when proven)
- Archive is automatic (when contradicted)
