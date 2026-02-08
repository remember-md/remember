---
name: brain:export
description: Export learned instincts for sharing (privacy-safe)
---

# /brain:export - Export Instincts

Creates a shareable archive of your learned instincts (no observations, privacy-safe).

## Usage

```
/brain:export
```

Or specific domain:
```
/brain:export code-style
```

## What it does

### 1. Collect Instincts

If no domain specified, export ALL:
```bash
~/supabrain/learning/instincts/personal/
├── code-style/
├── workflow/
├── communication/
└── decision-making/
```

If domain specified, export only that domain.

### 2. Create Archive

Create tarball with timestamp:

```bash
cd ~/supabrain
mkdir -p exports
tar -czf exports/instincts-$(date +%Y%m%d-%H%M%S).tar.gz \
  learning/instincts/personal/
```

**What's included:**
- ✅ Instinct markdown files (patterns only)
- ✅ Metadata (confidence, evidence descriptions)
- ❌ NO observations.jsonl (privacy)
- ❌ NO actual code/prompts (only patterns)
- ❌ NO personal journal content (only links)

### 3. Privacy Filtering

Before export, sanitize:

```javascript
async function sanitizeInstinct(instinct) {
  // Remove sensitive evidence
  instinct.evidence = instinct.evidence.map(e => {
    if (e.type === 'observation') {
      return {
        type: 'observation',
        timestamp: e.timestamp,
        context: '[redacted]' // Remove actual content
      };
    }
    if (e.type === 'journal') {
      return {
        type: 'journal',
        date: extractDate(e.link),
        excerpt: '[redacted]' // Remove personal content
      };
    }
    return e;
  });
  
  // Keep only pattern description, not personal context
  return instinct;
}
```

### 4. Create Manifest

Include `manifest.json` in archive:

```json
{
  "export_date": "2026-02-08T15:00:00Z",
  "supabrain_version": "1.0.0",
  "author": "User",
  "domains": {
    "code-style": {
      "count": 7,
      "avg_confidence": 0.75,
      "instincts": [
        "prefer-typescript.md",
        "functional-components.md",
        ...
      ]
    },
    "workflow": {
      "count": 5,
      "avg_confidence": 0.82,
      "instincts": [...]
    }
  },
  "total_instincts": 18,
  "note": "Evidence has been sanitized for privacy"
}
```

### 5. Confirm Export

```
✅ Instincts Exported

Archive created:
~/supabrain/exports/instincts-20260208-150000.tar.gz

Contents:
- code-style: 7 instincts
- workflow: 5 instincts
- communication: 4 instincts
- decision-making: 2 instincts

Total: 18 instincts (privacy-safe)

Share this file with others to help them learn from your patterns!

Import on another machine:
/brain:import ~/supabrain/exports/instincts-20260208-150000.tar.gz
```

## Export Options

```bash
# Export all instincts
/brain:export

# Export specific domain
/brain:export code-style

# Export with full evidence (not sanitized - use with caution)
/brain:export --full

# Export to specific path
/brain:export --output /custom/path/instincts.tar.gz
```

## Use Cases

1. **Share with team:** Export code-style instincts for team consistency
2. **Backup:** Archive before major changes
3. **Transfer:** Move instincts to different machine
4. **Contribute:** Share workflow patterns with community

## Security Note

**Exported instincts are SAFE to share:**
- ✅ Contains only abstract patterns
- ✅ No personal code/prompts
- ✅ No sensitive observations
- ✅ Evidence references sanitized

**But always review** before sharing externally!

## Notes

- Export creates new file (doesn't overwrite)
- Archives compressed with gzip
- Can export multiple times safely
- Original instincts unchanged
