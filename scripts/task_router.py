#!/usr/bin/env python3
"""Task routing intelligence — classify tasks by urgency and route appropriately.

Usage:
    python3 task_router.py "Deploy site by Friday" --project myproject
    python3 task_router.py "Research payment options"
    echo "Phase 2 dashboard" | python3 task_router.py --stdin
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Urgency keyword patterns
URGENT_KEYWORDS = [
    r"by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"by\s+\d{4}-\d{2}-\d{2}",  # by YYYY-MM-DD
    r"\basap\b",
    r"\burgent\b",
    r"\btoday\b",
    r"\bthis\s+week\b",
    r"\bdeadline\b",
    r"\bdue\b",
]

IMPORTANT_KEYWORDS = [
    r"\bshould\b",
    r"\bneed\s+to\b",
    r"\breminder\b",
    r"\bimportant\b",
    r"\bpriority\b",
]

BACKLOG_KEYWORDS = [
    r"\beventually\b",
    r"\bmaybe\b",
    r"\bsomeday\b",
    r"phase\s+\d+",
    r"\bv\d+\b",  # v2, v3
    r"\bfuture\b",
    r"\blater\b",
]


def classify_urgency(task_text: str) -> str:
    """Classify task urgency based on keywords.
    
    Returns: "urgent", "important", or "backlog"
    """
    text_lower = task_text.lower()
    
    # Check for urgent patterns first
    for pattern in URGENT_KEYWORDS:
        if re.search(pattern, text_lower):
            return "urgent"
    
    # Check for backlog patterns (before important, as they're more specific)
    for pattern in BACKLOG_KEYWORDS:
        if re.search(pattern, text_lower):
            return "backlog"
    
    # Check for important patterns
    for pattern in IMPORTANT_KEYWORDS:
        if re.search(pattern, text_lower):
            return "important"
    
    # Default: if no clear signal, assume important (better than backlog)
    return "important"


def route_task(task_text: str, project: str = None, session_date: str = None) -> dict:
    """Route task to appropriate destination.
    
    Returns:
        {
            "urgency": "urgent" | "important" | "backlog",
            "destination": "tasks.md" | "project_file",
            "section": "Focus" | "Next Up" | "Backlog",
            "formatted": "- [ ] Task text [[link]] (date)"
        }
    """
    urgency = classify_urgency(task_text)
    
    # Determine destination
    if urgency in ["urgent", "important"]:
        destination = "tasks.md"
        section = "Focus" if urgency == "urgent" else "Next Up"
    else:
        destination = "project_file"
        section = "Backlog"
    
    # Format task
    date_suffix = f" ({session_date})" if session_date else ""
    project_link = f" [[Projects/{project}/{project}|{project.title()}]]" if project else ""
    urgent_marker = " ⚡" if urgency == "urgent" else ""
    
    formatted = f"- [ ] {task_text}{project_link}{urgent_marker}{date_suffix}"
    
    return {
        "urgency": urgency,
        "destination": destination,
        "section": section,
        "formatted": formatted.strip(),
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Route tasks based on urgency")
    parser.add_argument("task", nargs="?", help="Task text to route")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--project", help="Project name (kebab-case)")
    parser.add_argument("--date", help="Session date (YYYY-MM-DD)")
    args = parser.parse_args()
    
    # Get task text
    if args.stdin:
        task_text = sys.stdin.read().strip()
    elif args.task:
        task_text = args.task
    else:
        parser.error("Provide task text or use --stdin")
    
    # Route task
    result = route_task(task_text, project=args.project, session_date=args.date)
    
    # Output as JSON
    import json
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
