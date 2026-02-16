#!/usr/bin/env python3
"""Build a compact knowledge index of the brain directory.

Scans People/, Projects/, Areas/, Notes/, Tasks/tasks.md, Journal/
and outputs formatted markdown tables for use as AI context.

Usage:
    python3 build_index.py              # Full index
    python3 build_index.py --compact    # Compact (names only, for hooks)
"""

import os
import re
import sys
from pathlib import Path

def _brain_path() -> Path:
    return Path(os.path.expanduser(os.environ.get("REMEMBER_BRAIN_PATH", "~/remember")))

def parse_frontmatter(filepath: Path, max_bytes=2048) -> dict:
    """Parse YAML frontmatter + H1 from first ~2KB of a file."""
    try:
        text = filepath.read_text(encoding="utf-8")[:max_bytes]
    except OSError:
        return {}
    
    meta = {}
    # Extract frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            fm = text[3:end]
            for line in fm.strip().splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if val.startswith("[") and val.endswith("]"):
                        val = val[1:-1].strip()
                    meta[key] = val
    
    # Extract H1
    h1 = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if h1:
        meta['_title'] = h1.group(1).strip()
    
    return meta

def scan_people(brain: Path) -> list:
    people_dir = brain / "People"
    if not people_dir.is_dir():
        return []
    results = []
    for f in sorted(people_dir.glob("*.md")):
        m = parse_frontmatter(f)
        results.append({
            'file': f.stem,
            'name': m.get('_title', f.stem.replace('-', ' ').title()),
            'role': m.get('role', ''),
            'org': m.get('org', m.get('organization', '')),
            'last_contact': m.get('last_contact', m.get('updated', '')),
            'tags': m.get('tags', ''),
        })
    return results

def scan_projects(brain: Path) -> list:
    proj_dir = brain / "Projects"
    if not proj_dir.is_dir():
        return []
    results = []
    for d in sorted(proj_dir.iterdir()):
        if not d.is_dir():
            continue
        main_file = d / f"{d.name}.md"
        if not main_file.exists():
            # try any .md
            mds = list(d.glob("*.md"))
            main_file = mds[0] if mds else None
        if not main_file:
            continue
        m = parse_frontmatter(main_file)
        # Count sub-files
        sub_count = len(list(d.glob("*.md"))) - 1
        results.append({
            'file': d.name,
            'name': m.get('_title', d.name.replace('-', ' ').title()),
            'status': m.get('status', ''),
            'tags': m.get('tags', ''),
            'updated': m.get('updated', ''),
            'sub_notes': sub_count,
        })
    return results

def scan_areas(brain: Path) -> list:
    areas_dir = brain / "Areas"
    if not areas_dir.is_dir():
        return []
    results = []
    for f in sorted(areas_dir.glob("*.md")):
        m = parse_frontmatter(f)
        results.append({
            'file': f.stem,
            'name': m.get('_title', f.stem.replace('-', ' ').title()),
            'updated': m.get('updated', ''),
        })
    return results

def scan_notes(brain: Path) -> list:
    notes_dir = brain / "Notes"
    if not notes_dir.is_dir():
        return []
    results = []
    for f in sorted(notes_dir.glob("*.md")):
        m = parse_frontmatter(f)
        results.append({
            'file': f.stem,
            'name': m.get('_title', f.stem.replace('-', ' ').title()),
            'tags': m.get('tags', ''),
            'created': m.get('created', ''),
        })
    return results

def scan_tasks(brain: Path) -> dict:
    tasks_file = brain / "Tasks" / "tasks.md"
    if not tasks_file.exists():
        return {'focus': 0, 'next_up': 0, 'backlog': 0, 'done': 0}
    try:
        text = tasks_file.read_text(encoding="utf-8")
    except OSError:
        return {'focus': 0, 'next_up': 0, 'backlog': 0, 'done': 0}
    
    counts = {'focus': 0, 'next_up': 0, 'backlog': 0, 'done': 0}
    current_section = None
    for line in text.splitlines():
        lower = line.strip().lower()
        if lower.startswith('## focus'):
            current_section = 'focus'
        elif lower.startswith('## next up'):
            current_section = 'next_up'
        elif lower.startswith('## backlog'):
            current_section = 'backlog'
        elif lower.startswith('## done') or lower.startswith('## completed'):
            current_section = 'done'
        elif lower.startswith('## '):
            current_section = None
        elif current_section and re.match(r'^-\s*\[.\]', line.strip()):
            counts[current_section] += 1
    return counts

def scan_journal(brain: Path) -> dict:
    journal_dir = brain / "Journal"
    if not journal_dir.is_dir():
        return {'count': 0, 'latest': ''}
    entries = sorted(journal_dir.glob("*.md"))
    return {
        'count': len(entries),
        'latest': entries[-1].stem if entries else '',
    }

def format_full(brain: Path):
    lines = [f"# Knowledge Index\n**Brain:** `{brain}`\n"]
    
    # People
    people = scan_people(brain)
    if people:
        lines.append("## People\n| Name | Role/Org | Last Contact | Tags |")
        lines.append("|------|----------|--------------|------|")
        for p in people:
            org = f"{p['role']}" + (f" @ {p['org']}" if p['org'] else '')
            lines.append(f"| [[People/{p['file']}\\|{p['name']}]] | {org} | {p['last_contact']} | {p['tags']} |")
    else:
        lines.append("## People\n*None yet*")
    lines.append("")
    
    # Projects
    projects = scan_projects(brain)
    if projects:
        lines.append("## Projects\n| Name | Status | Updated | Sub-notes | Tags |")
        lines.append("|------|--------|---------|-----------|------|")
        for p in projects:
            lines.append(f"| [[Projects/{p['file']}/{p['file']}\\|{p['name']}]] | {p['status']} | {p['updated']} | {p['sub_notes']} | {p['tags']} |")
    else:
        lines.append("## Projects\n*None yet*")
    lines.append("")
    
    # Areas
    areas = scan_areas(brain)
    if areas:
        lines.append("## Areas\n| Name | Updated |")
        lines.append("|------|---------|")
        for a in areas:
            lines.append(f"| [[Areas/{a['file']}\\|{a['name']}]] | {a['updated']} |")
    else:
        lines.append("## Areas\n*None yet*")
    lines.append("")
    
    # Notes
    notes = scan_notes(brain)
    if notes:
        lines.append(f"## Notes ({len(notes)} total)\n| Name | Tags | Created |")
        lines.append("|------|------|---------|")
        for n in notes:
            lines.append(f"| [[Notes/{n['file']}\\|{n['name']}]] | {n['tags']} | {n['created']} |")
    else:
        lines.append("## Notes\n*None yet*")
    lines.append("")
    
    # Tasks
    tasks = scan_tasks(brain)
    lines.append(f"## Tasks\n- **Focus:** {tasks['focus']} items")
    lines.append(f"- **Next Up:** {tasks['next_up']} items")
    lines.append(f"- **Backlog:** {tasks['backlog']} items")
    lines.append(f"- **Done:** {tasks['done']} items")
    lines.append("")
    
    # Journal
    journal = scan_journal(brain)
    lines.append(f"## Journal\n- **Entries:** {journal['count']}")
    if journal['latest']:
        lines.append(f"- **Latest:** {journal['latest']}")
    
    return "\n".join(lines)

def format_compact(brain: Path):
    """One-line-per-category summary for hook injection."""
    people = [p['file'] for p in scan_people(brain)]
    projects = [p['file'] for p in scan_projects(brain)]
    areas = [a['file'] for a in scan_areas(brain)]
    notes = [n['file'] for n in scan_notes(brain)]
    tasks = scan_tasks(brain)
    journal = scan_journal(brain)
    
    lines = [
        f"BRAIN INDEX ({brain})",
        f"People: {', '.join(people) or 'none'}",
        f"Projects: {', '.join(projects) or 'none'}",
        f"Areas: {', '.join(areas) or 'none'}",
        f"Notes ({len(notes)}): {', '.join(notes[:20]) or 'none'}{'...' if len(notes) > 20 else ''}",
        f"Tasks: {tasks['focus']} focus, {tasks['next_up']} next, {tasks['backlog']} backlog",
        f"Journal: {journal['count']} entries, latest {journal['latest']}",
    ]
    return "\n".join(lines)

def main():
    brain = _brain_path()
    if not brain.is_dir():
        print(f"Brain not found at {brain}. Run /brain:init first.", file=sys.stderr)
        sys.exit(1)
    
    compact = "--compact" in sys.argv
    print(format_compact(brain) if compact else format_full(brain))

if __name__ == "__main__":
    main()
