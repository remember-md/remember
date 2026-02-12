#!/usr/bin/env python3
"""Task utilities — format tasks for tasks.md (AI does classification).

AI-driven approach: AI determines urgency/routing semantically. This script only
formats the output.

Usage:
    python3 task_utils.py --format "Deploy site" --urgency urgent --project myproject --date 2026-02-12
    python3 task_utils.py --format "Research tools" --urgency important --date 2026-02-12
"""

import sys
from pathlib import Path


def format_task(task_text: str, urgency: str, project: str = None, date: str = None) -> str:
    """Format a task for tasks.md or project file.
    
    Args:
        task_text: Task description
        urgency: "urgent", "important", or "backlog"
        project: Project name (kebab-case) or None
        date: Session date (YYYY-MM-DD) or None
    
    Returns:
        Formatted markdown task line
    """
    # Project link
    if project:
        project_link = f" [[Projects/{project}/{project}|{project.replace('-', ' ').title()}]]"
    else:
        project_link = ""
    
    # Urgency marker
    urgent_marker = " ⚡" if urgency == "urgent" else ""
    
    # Date suffix
    date_suffix = f" ({date})" if date else ""
    
    # Format
    formatted = f"- [ ] {task_text}{project_link}{urgent_marker}{date_suffix}"
    
    return formatted.strip()


def get_destination(urgency: str) -> dict:
    """Get destination info for a task based on urgency.
    
    Returns:
        {
            "file": "tasks.md" or "project_file",
            "section": "Focus" or "Next Up" or "Backlog"
        }
    """
    if urgency == "urgent":
        return {"file": "tasks.md", "section": "Focus"}
    elif urgency == "important":
        return {"file": "tasks.md", "section": "Next Up"}
    else:  # backlog
        return {"file": "project_file", "section": "Backlog"}


def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Task formatting utilities (AI-driven classification)")
    parser.add_argument("--format", metavar="TEXT", help="Format a task")
    parser.add_argument("--urgency", choices=["urgent", "important", "backlog"], help="Task urgency")
    parser.add_argument("--project", help="Project name (kebab-case)")
    parser.add_argument("--date", help="Session date (YYYY-MM-DD)")
    args = parser.parse_args()
    
    if args.format and args.urgency:
        # Format task
        formatted = format_task(args.format, args.urgency, project=args.project, date=args.date)
        destination = get_destination(args.urgency)
        
        result = {
            "formatted": formatted,
            "destination": destination,
            "urgency": args.urgency
        }
        
        print(json.dumps(result, indent=2))
    else:
        parser.error("Use --format and --urgency together")


if __name__ == "__main__":
    main()
