#!/usr/bin/env python3
"""Persona learning — extract behavioral patterns from sessions.

Usage:
    python3 persona_learner.py <session_markdown> --persona-path ~/remember/Persona.md
    python3 persona_learner.py --stdin --persona-path ~/remember/Persona.md
"""

import re
import sys
from pathlib import Path
from datetime import datetime


# Pattern detection rules
CORRECTION_PATTERNS = [
    r"no[,\s]+(do\s+it|use|try|change)",
    r"instead[,\s]+(do|use|try)",
    r"actually[,\s]+(I|we)\s+(want|prefer|need)",
    r"don't\s+(do|use)\s+\w+[,\s]+use\s+\w+",
]

PREFERENCE_PATTERNS = [
    r"I\s+(always|usually|prefer|like)\s+(\w+)",
    r"(never|don't)\s+use\s+(\w+)",
    r"stick\s+with\s+(\w+)",
]

WORKFLOW_PATTERNS = [
    r"first[,\s]+(I|we)\s+(\w+)",
    r"then[,\s]+(I|we)\s+(\w+)",
    r"process\s+is\s+(.+)",
    r"workflow:\s+(.+)",
]

COMMUNICATION_PATTERNS = [
    r"(concise|brief|short|detailed|thorough)",
    r"(Romanian|English|mixed)",
    r"(formal|informal|casual)",
]


def detect_corrections(session_text: str) -> list:
    """Detect user corrections/preferences."""
    corrections = []
    for pattern in CORRECTION_PATTERNS:
        matches = re.finditer(pattern, session_text, re.IGNORECASE)
        for match in matches:
            # Get surrounding context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(session_text), match.end() + 50)
            context = session_text[start:end].strip()
            corrections.append({
                "type": "correction",
                "pattern": match.group(0),
                "context": context,
            })
    return corrections


def detect_preferences(session_text: str) -> list:
    """Detect stated preferences."""
    preferences = []
    for pattern in PREFERENCE_PATTERNS:
        matches = re.finditer(pattern, session_text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 50)
            end = min(len(session_text), match.end() + 50)
            context = session_text[start:end].strip()
            preferences.append({
                "type": "preference",
                "pattern": match.group(0),
                "context": context,
            })
    return preferences


def detect_workflows(session_text: str) -> list:
    """Detect workflow patterns."""
    workflows = []
    for pattern in WORKFLOW_PATTERNS:
        matches = re.finditer(pattern, session_text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 30)
            end = min(len(session_text), match.end() + 100)
            context = session_text[start:end].strip()
            workflows.append({
                "type": "workflow",
                "pattern": match.group(0),
                "context": context,
            })
    return workflows


def detect_communication_style(session_text: str) -> list:
    """Detect communication preferences."""
    styles = []
    for pattern in COMMUNICATION_PATTERNS:
        matches = re.finditer(pattern, session_text, re.IGNORECASE)
        for match in matches:
            start = max(0, match.start() - 40)
            end = min(len(session_text), match.end() + 40)
            context = session_text[start:end].strip()
            styles.append({
                "type": "communication",
                "pattern": match.group(0),
                "context": context,
            })
    return styles


def analyze_session(session_text: str, session_date: str = None) -> dict:
    """Analyze session for behavioral patterns.
    
    Returns:
        {
            "corrections": [...],
            "preferences": [...],
            "workflows": [...],
            "communication": [...],
            "session_date": "YYYY-MM-DD"
        }
    """
    if not session_date:
        session_date = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "corrections": detect_corrections(session_text),
        "preferences": detect_preferences(session_text),
        "workflows": detect_workflows(session_text),
        "communication": detect_communication_style(session_text),
        "session_date": session_date,
    }


def format_evidence_line(pattern: dict, session_date: str) -> str:
    """Format a single evidence line for Persona.md.
    
    Returns: "[YYYY-MM-DD] Brief description based on pattern"
    """
    context = pattern["context"][:100]  # Limit to 100 chars
    return f"[{session_date}] {context}"


def update_persona_file(persona_path: Path, patterns: dict) -> str:
    """Update Persona.md with new evidence.
    
    Returns: Summary of changes made
    """
    if not persona_path.exists():
        return "Error: Persona.md not found"
    
    # Read existing Persona
    content = persona_path.read_text(encoding="utf-8")
    
    # Prepare evidence lines
    evidence_lines = []
    for correction in patterns["corrections"]:
        evidence_lines.append(format_evidence_line(correction, patterns["session_date"]))
    for preference in patterns["preferences"]:
        evidence_lines.append(format_evidence_line(preference, patterns["session_date"]))
    
    if not evidence_lines:
        return "No significant patterns detected"
    
    # Find Evidence Log section
    if "## Evidence Log" in content:
        # Insert new evidence at the top of the log
        log_start = content.index("## Evidence Log") + len("## Evidence Log")
        # Find next section or end
        next_section = content.find("\n## ", log_start)
        if next_section == -1:
            next_section = len(content)
        
        # Insert evidence
        existing_log = content[log_start:next_section]
        new_evidence = "\n" + "\n".join(f"- {line}" for line in evidence_lines) + "\n"
        updated_content = (
            content[:log_start] + 
            new_evidence + 
            existing_log +
            content[next_section:]
        )
    else:
        # Create Evidence Log section
        new_evidence = "\n\n## Evidence Log\n" + "\n".join(f"- {line}" for line in evidence_lines) + "\n"
        updated_content = content + new_evidence
    
    # Update frontmatter date
    if "updated:" in updated_content:
        updated_content = re.sub(
            r"updated:\s+\d{4}-\d{2}-\d{2}",
            f"updated: {patterns['session_date']}",
            updated_content
        )
    
    # Write back
    persona_path.write_text(updated_content, encoding="utf-8")
    
    return f"Added {len(evidence_lines)} evidence line(s) to Persona.md"


def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Extract behavioral patterns from sessions")
    parser.add_argument("session_file", nargs="?", help="Session markdown file")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--persona-path", required=True, help="Path to Persona.md")
    parser.add_argument("--date", help="Session date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, don't update Persona")
    args = parser.parse_args()
    
    # Read session text
    if args.stdin:
        session_text = sys.stdin.read()
    elif args.session_file:
        session_text = Path(args.session_file).read_text(encoding="utf-8")
    else:
        parser.error("Provide session file or use --stdin")
    
    # Analyze
    patterns = analyze_session(session_text, session_date=args.date)
    
    # Output patterns
    print(json.dumps(patterns, indent=2))
    
    # Update Persona if not dry-run
    if not args.dry_run:
        persona_path = Path(args.persona_path).expanduser()
        result = update_persona_file(persona_path, patterns)
        print(f"\n{result}", file=sys.stderr)


if __name__ == "__main__":
    main()
