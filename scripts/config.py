#!/usr/bin/env python3
"""Shared config resolver for Remember plugin.

Resolution order:
  1. REMEMBER_CONFIG env var (JSON string) — set by OpenClaw plugin wrapper
  2. REMEMBER_CONFIG_FILE env var (path to JSON file)
  3. ~/.claude/plugin-config/remember/config.json (user scope)
  4. .claude/plugin-config/remember/config.json (project scope)
  5. ${PLUGIN_ROOT}/config.defaults.json (shipped default)
  6. Hardcoded defaults
"""

import json
import os
from pathlib import Path

_DEFAULTS = {
    "paths": {"data_root": "~/remember"},
    "session": {
        "load_persona": True,
        "brain_dump_keywords": [
            "save this", "remember this", "brain dump", "note to self",
            "capture this", "save to brain", "write to brain", "add to brain",
            "salvează", "notează", "reține"
        ],
    },
    "extract": {
        "max_assistant_text_len": 500,
        "min_session_size": 500,
    },
}

_cached = None


def _deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _load_json_file(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def load_config(*, force_reload: bool = False) -> dict:
    global _cached
    if _cached and not force_reload:
        return _cached

    config = _DEFAULTS.copy()
    plugin_root = Path(__file__).resolve().parent.parent

    # Try sources in reverse priority (lowest first, highest overwrites)
    sources = [
        plugin_root / "config.defaults.json",
        Path(".claude/plugin-config/remember/config.json"),
        Path.home() / ".claude/plugin-config/remember/config.json",
    ]

    # Env var: file path
    env_file = os.environ.get("REMEMBER_CONFIG_FILE")
    if env_file:
        sources.append(Path(env_file))

    for src in sources:
        data = _load_json_file(str(src))
        if data:
            config = _deep_merge(config, data)

    # Env var: inline JSON (highest priority — from OpenClaw)
    env_json = os.environ.get("REMEMBER_CONFIG")
    if env_json:
        try:
            config = _deep_merge(config, json.loads(env_json))
        except json.JSONDecodeError:
            pass

    _cached = config
    return config


def get_brain_root() -> Path:
    config = load_config()
    raw = config.get("paths", {}).get("data_root", "~/remember")
    return Path(os.path.expanduser(raw))


# CLI: print resolved config or specific key
if __name__ == "__main__":
    import sys
    config = load_config()
    if len(sys.argv) > 1:
        # Dot-path access: e.g. "paths.data_root"
        val = config
        for key in sys.argv[1].split("."):
            val = val.get(key, "") if isinstance(val, dict) else ""
        print(val if not isinstance(val, (dict, list)) else json.dumps(val))
    else:
        print(json.dumps(config, indent=2))
