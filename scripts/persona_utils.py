#!/usr/bin/env python3
"""Persona utilities — read/write Persona.md (AI does pattern detection).

AI-driven approach: This script only handles file I/O. The AI analyzes sessions
semantically and determines what to update.

Usage:
    python3 persona_utils.py --read ~/remember/Persona.md
    python3 persona_utils.py --add-evidence "2026-02-12" "User preferred X" ~/remember/Persona.md
    echo "Evidence line" | python3 persona_utils.py --add-evidence-stdin "2026-02-12" ~/remember/Persona.md
"""

import re
import sys
from pathlib import Path
from datetime import datetime


def read_persona(persona_path: Path) -> dict:
    """Read Persona.md and return structured content.
    
    Returns:
        {
            "frontmatter": {...},
            "sections": {
                "Communication": "...",
                "Workflow": "...",
                "Evidence Log": [...]
            },
            "raw": "..."
        }
    """
    if not persona_path.exists():
        return {"error": "Persona.md not found"}
    
    content = persona_path.read_text(encoding="utf-8")
    
    # Extract frontmatter
    frontmatter = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm_text = content[3:end]
            for line in fm_text.strip().split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
    
    # Extract sections (basic split by ## headers)
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[3:].strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()
    
    return {
        "frontmatter": frontmatter,
        "sections": sections,
        "raw": content
    }


def add_evidence(persona_path: Path, date: str, evidence_text: str) -> str:
    """Add evidence line to Persona.md Evidence Log.
    
    Args:
        persona_path: Path to Persona.md
        date: Evidence date (YYYY-MM-DD)
        evidence_text: What to add (without date prefix)
    
    Returns:
        Success message or error
    """
    if not persona_path.exists():
        return "Error: Persona.md not found"
    
    content = persona_path.read_text(encoding="utf-8")
    
    # Format evidence line
    evidence_line = f"- [{date}] {evidence_text}"
    
    # Find Evidence Log section
    if "## Evidence Log" in content:
        # Insert at top of Evidence Log
        log_start = content.index("## Evidence Log") + len("## Evidence Log")
        
        # Find next section or end
        next_section = content.find("\n## ", log_start)
        if next_section == -1:
            next_section = len(content)
        
        # Insert evidence
        existing_log = content[log_start:next_section]
        new_content = (
            content[:log_start] +
            "\n" + evidence_line + "\n" +
            existing_log +
            content[next_section:]
        )
    else:
        # Create Evidence Log section
        new_content = content + f"\n\n## Evidence Log\n{evidence_line}\n"
    
    # Update frontmatter date
    if "updated:" in new_content:
        new_content = re.sub(
            r"updated:\s+\d{4}-\d{2}-\d{2}",
            f"updated: {date}",
            new_content
        )
    
    # Write back
    persona_path.write_text(new_content, encoding="utf-8")
    
    return f"Added evidence: [{date}] {evidence_text[:50]}..."


def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Persona.md utilities (AI-driven pattern detection)")
    parser.add_argument("persona_path", help="Path to Persona.md")
    parser.add_argument("--read", action="store_true", help="Read and output structured Persona")
    parser.add_argument("--add-evidence", nargs=2, metavar=("DATE", "TEXT"), help="Add evidence line")
    parser.add_argument("--add-evidence-stdin", metavar="DATE", help="Add evidence from stdin")
    args = parser.parse_args()
    
    persona_path = Path(args.persona_path).expanduser()
    
    if args.read:
        # Read and output
        result = read_persona(persona_path)
        print(json.dumps(result, indent=2))
    
    elif args.add_evidence:
        # Add evidence
        date, text = args.add_evidence
        result = add_evidence(persona_path, date, text)
        print(result)
    
    elif args.add_evidence_stdin:
        # Add evidence from stdin
        text = sys.stdin.read().strip()
        result = add_evidence(persona_path, args.add_evidence_stdin, text)
        print(result)
    
    else:
        parser.error("Use --read, --add-evidence, or --add-evidence-stdin")


if __name__ == "__main__":
    main()
