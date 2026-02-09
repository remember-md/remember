#!/usr/bin/env python3
"""Extract clean content from Claude Code session transcripts.

Reads JSONL transcript files and outputs clean markdown with user messages
and short assistant responses. Supports finding unprocessed sessions.

Usage:
    python3 extract.py <transcript.jsonl>           # Extract one session
    python3 extract.py --unprocessed                 # List unprocessed sessions
    python3 extract.py --unprocessed --project <name> # Filter by project name
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_brain_root():
    """Resolve brain root from config. Search order:
    1. ~/.claude/plugin-config/remember/config.json  (user scope, persistent)
    2. .claude/plugin-config/remember/config.json    (project scope, persistent)
    3. ${PLUGIN_ROOT}/config.defaults.json           (shipped default)
    4. Hardcoded ~/remember
    """
    plugin_dir = Path(__file__).resolve().parent.parent
    config_candidates = [
        Path.home() / ".claude" / "plugin-config" / "remember" / "config.json",
        Path(".claude") / "plugin-config" / "remember" / "config.json",
        plugin_dir / "config.defaults.json",
    ]
    for config_path in config_candidates:
        if not config_path.exists():
            continue
        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
            data_root = config.get("paths", {}).get("data_root", "")
            if data_root:
                return Path(os.path.expanduser(data_root))
        except (json.JSONDecodeError, OSError):
            continue
    return Path.home() / "remember"


BRAIN_ROOT = get_brain_root()
PROCESSED_FILE = BRAIN_ROOT / ".processed_sessions"
CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"
MAX_ASSISTANT_TEXT_LEN = 500


def get_processed_sessions():
    """Read set of already-processed session IDs."""
    if not PROCESSED_FILE.exists():
        return set()
    return set(PROCESSED_FILE.read_text(encoding="utf-8").strip().splitlines())


def mark_session_processed(session_id):
    """Append session ID to processed file."""
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(session_id + "\n")


def find_all_transcripts():
    """Find all JSONL transcript files across all projects."""
    transcripts = []
    if not CLAUDE_PROJECTS_DIR.exists():
        return transcripts
    for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl in project_dir.glob("*.jsonl"):
            transcripts.append(jsonl)
    return transcripts


def get_session_id(path):
    """Extract session ID from transcript filename."""
    return Path(path).stem


def get_project_name(path):
    """Extract human-readable project name from the project directory."""
    parent = Path(path).parent.name
    parts = parent.split("-")
    # Find "projects" marker and take everything after
    try:
        idx = parts.index("projects")
        project_parts = [p for p in parts[idx + 1:] if p]
        if project_parts:
            return "/".join(project_parts)
    except ValueError:
        pass
    # No "projects" in path or no parts after it — use last 2 meaningful parts
    meaningful = [p for p in parts if p]
    return "/".join(meaningful[-2:]) if len(meaningful) >= 2 else parent


def is_noise_content(content):
    """Check if user message content is noise (commands, system tags, etc)."""
    if not isinstance(content, str):
        return False
    noise_prefixes = [
        "<local-command-",
        "<command-name>",
        "<system-",
        "<user-prompt-submit-hook>",
    ]
    return any(content.strip().startswith(p) for p in noise_prefixes)


def extract_user_text(message):
    """Extract clean text from a user message."""
    content = message.get("content", "")
    if isinstance(content, str):
        if is_noise_content(content):
            return None
        text = content.strip()
        return text if text else None
    elif isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                t = block["text"].strip()
                if t and not is_noise_content(t):
                    texts.append(t)
            elif isinstance(block, str):
                if not is_noise_content(block):
                    texts.append(block.strip())
        return "\n".join(texts) if texts else None
    return None


def extract_assistant_text(message):
    """Extract short text responses from assistant messages (skip tool calls)."""
    content = message.get("content", [])
    if isinstance(content, str):
        return content.strip() if len(content) <= MAX_ASSISTANT_TEXT_LEN else None
    if not isinstance(content, list):
        return None
    texts = []
    has_tool_use = False
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_use":
            has_tool_use = True
        elif block.get("type") == "text":
            t = block.get("text", "").strip()
            if t:
                texts.append(t)

    if not texts:
        return None

    combined = "\n".join(texts)
    # Skip long assistant messages - they're usually code/tool output
    if len(combined) > MAX_ASSISTANT_TEXT_LEN:
        return None
    # If it was only tool calls with a tiny preamble, skip
    if has_tool_use and len(combined) < 20:
        return None
    return combined


def parse_timestamp(ts_str):
    """Parse ISO timestamp to datetime object."""
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def format_timestamp(ts_str, include_date=False):
    """Format ISO timestamp to readable format."""
    dt = parse_timestamp(ts_str)
    if not dt:
        return ""
    if include_date:
        return dt.strftime("%Y-%m-%d %H:%M")
    return dt.strftime("%H:%M")


def extract_session(path):
    """Extract clean content from a single transcript file.

    Returns dict with session metadata and extracted messages.
    """
    session_id = get_session_id(path)
    project = get_project_name(path)
    messages = []
    session_cwd = None
    first_ts = None
    last_ts = None

    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            entry_type = entry.get("type")
            ts = entry.get("timestamp", "")

            if first_ts is None and ts:
                first_ts = ts
            if ts:
                last_ts = ts

            if not session_cwd and entry.get("cwd"):
                session_cwd = entry["cwd"]

            if entry_type == "user":
                # Skip meta messages
                if entry.get("isMeta"):
                    continue
                msg = entry.get("message", {})
                text = extract_user_text(msg)
                if text:
                    messages.append({
                        "role": "user",
                        "text": text,
                        "time": format_timestamp(ts),
                        "timestamp": ts,
                    })

            elif entry_type == "assistant":
                msg = entry.get("message", {})
                text = extract_assistant_text(msg)
                if text:
                    messages.append({
                        "role": "assistant",
                        "text": text,
                        "time": format_timestamp(ts),
                        "timestamp": ts,
                    })

    # Detect if session spans multiple days
    spans_multiple_days = False
    if first_ts and last_ts:
        first_dt = parse_timestamp(first_ts)
        last_dt = parse_timestamp(last_ts)
        if first_dt and last_dt and first_dt.date() != last_dt.date():
            spans_multiple_days = True

    return {
        "session_id": session_id,
        "project": project,
        "cwd": session_cwd,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "spans_multiple_days": spans_multiple_days,
        "session_date": first_ts,
        "messages": messages,
    }


def format_session_markdown(session):
    """Format extracted session data as clean markdown."""
    lines = []
    date_str = ""
    end_date_str = ""
    if session["first_ts"]:
        dt = parse_timestamp(session["first_ts"])
        if dt:
            date_str = dt.strftime("%Y-%m-%d")
    if session["last_ts"]:
        dt = parse_timestamp(session["last_ts"])
        if dt:
            end_date_str = dt.strftime("%Y-%m-%d")

    spans = session.get("spans_multiple_days", False)

    lines.append(f"# Session: {session['project']}")
    if date_str:
        if spans and end_date_str and date_str != end_date_str:
            lines.append(f"**Date:** {date_str} to {end_date_str}")
        else:
            lines.append(f"**Date:** {date_str}")
    lines.append(f"**Session date (use for journal/tasks):** {date_str}")
    if session["cwd"]:
        lines.append(f"**Working dir:** `{session['cwd']}`")
    lines.append(f"**Session ID:** `{session['session_id']}`")
    lines.append("")

    if not session["messages"]:
        lines.append("*(empty session)*")
        return "\n".join(lines)

    current_day = None
    for msg in session["messages"]:
        # Show date headers when session spans multiple days
        if spans and msg.get("timestamp"):
            msg_dt = parse_timestamp(msg["timestamp"])
            if msg_dt:
                msg_day = msg_dt.strftime("%Y-%m-%d")
                if msg_day != current_day:
                    current_day = msg_day
                    lines.append(f"### {msg_day}")
                    lines.append("")

        time_prefix = f"[{msg['time']}] " if msg["time"] else ""
        if msg["role"] == "user":
            lines.append(f"**{time_prefix}User:** {msg['text']}")
        else:
            lines.append(f"*{time_prefix}Claude: {msg['text']}*")
        lines.append("")

    return "\n".join(lines)


def cmd_extract(path):
    """Extract and print a single session."""
    if not os.path.exists(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    session = extract_session(path)
    print(format_session_markdown(session))


def cmd_list_unprocessed(project_filter=None):
    """List unprocessed transcript files."""
    processed = get_processed_sessions()
    transcripts = find_all_transcripts()

    unprocessed = []
    for t in transcripts:
        sid = get_session_id(t)
        if sid in processed:
            continue
        project = get_project_name(t)
        if project_filter and project_filter.lower() not in project.lower():
            continue
        # Get file size to skip tiny sessions
        size = t.stat().st_size
        if size < 500:  # Skip very small files (likely empty/init sessions)
            continue
        unprocessed.append((t, project, size))

    # Sort by modification time (oldest first)
    unprocessed.sort(key=lambda x: x[0].stat().st_mtime)

    if not unprocessed:
        print("No unprocessed sessions found.")
        return

    print(f"Found {len(unprocessed)} unprocessed session(s):\n")
    for path, project, size in unprocessed:
        sid = get_session_id(path)
        mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        size_kb = size / 1024
        print(f"  {sid}")
        print(f"    Project: {project}")
        print(f"    Modified: {mtime}")
        print(f"    Size: {size_kb:.0f}KB")
        print(f"    Path: {path}")
        print()


def cmd_mark_processed(session_id):
    """Mark a session as processed."""
    mark_session_processed(session_id)
    print(f"Marked as processed: {session_id}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--unprocessed":
        project_filter = None
        if "--project" in sys.argv:
            idx = sys.argv.index("--project")
            if idx + 1 < len(sys.argv):
                project_filter = sys.argv[idx + 1]
        cmd_list_unprocessed(project_filter)
    elif arg == "--mark-processed":
        if len(sys.argv) < 3:
            print("Usage: extract.py --mark-processed <session-id>", file=sys.stderr)
            sys.exit(1)
        cmd_mark_processed(sys.argv[2])
    else:
        cmd_extract(arg)


if __name__ == "__main__":
    main()
