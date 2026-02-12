#!/usr/bin/env python3
"""Resource enrichment — fetch metadata for URLs and create rich notes.

Usage:
    python3 resource_enricher.py "https://example.com/article" --output ~/remember/Resources/articles/
    python3 resource_enricher.py "https://example.com" --dry-run
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import subprocess
import json


def classify_url_type(url: str, content: str = "") -> str:
    """Classify URL type based on domain and content.
    
    Returns: "article", "tool", "video", "book", "documentation"
    """
    domain = urlparse(url).netloc.lower()
    
    # Video platforms
    if any(x in domain for x in ["youtube", "vimeo", "youtu.be"]):
        return "video"
    
    # Documentation sites
    if any(x in domain for x in ["docs.", "documentation", "readthedocs", "github.io"]):
        return "documentation"
    
    # Book/reading platforms
    if any(x in domain for x in ["goodreads", "amazon", "book"]):
        return "book"
    
    # Tool/product pages
    if any(x in content.lower() for x in ["pricing", "features", "get started", "sign up"]):
        return "tool"
    
    # Default: article
    return "article"


def extract_metadata(url: str) -> dict:
    """Fetch URL and extract metadata using web_fetch-like approach.
    
    Returns:
        {
            "title": "Page title",
            "author": "Author name or None",
            "description": "Meta description",
            "content": "First few paragraphs",
            "type": "article|tool|video|etc"
        }
    """
    # This is a placeholder — in real usage, this would call web_fetch
    # or use a library like requests + BeautifulSoup
    # For now, return a template
    
    try:
        # Simulate web_fetch call (in actual use, call the OpenClaw web_fetch tool)
        # result = web_fetch(url)
        # For this template, we'll return basic structure
        
        return {
            "url": url,
            "title": "Extracted Title",  # Would come from <title> or og:title
            "author": None,  # Would come from meta author tag
            "description": "Brief description",  # From meta description
            "content": "Content preview...",  # First 2-3 paragraphs
            "type": "article",  # Classified
            "fetched_at": datetime.now().strftime("%Y-%m-%d"),
        }
    except Exception as e:
        return {
            "url": url,
            "title": urlparse(url).path.split("/")[-1] or "Untitled",
            "author": None,
            "description": None,
            "content": f"Error fetching content: {e}",
            "type": "article",
            "fetched_at": datetime.now().strftime("%Y-%m-%d"),
        }


def slugify(text: str) -> str:
    """Convert text to kebab-case slug."""
    # Remove special chars, convert to lowercase
    text = re.sub(r"[^\w\s-]", "", text.lower())
    # Replace spaces with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # Remove leading/trailing hyphens
    return text.strip("-")


def create_resource_note(metadata: dict, output_dir: Path, session_date: str = None) -> Path:
    """Create a rich resource note from metadata.
    
    Returns: Path to created note
    """
    if not session_date:
        session_date = datetime.now().strftime("%Y-%m-%d")
    
    # Generate filename from title
    filename = slugify(metadata["title"]) + ".md"
    filepath = output_dir / filename
    
    # Prepare frontmatter
    frontmatter = f"""---
source: {metadata["url"]}
author: {metadata.get("author") or "Unknown"}
type: {metadata["type"]}
created: {session_date}
tags: [resource, {metadata["type"]}]
related: []
---
"""
    
    # Prepare content
    content = f"""# {metadata["title"]}

## Summary
{metadata.get("description") or "No description available."}

## Key Takeaways
{metadata.get("content", "")[:500]}...

## Why It Matters
[Add context: why you saved this, how it relates to your work]

## Related
[Links to related Projects/Notes will be added automatically]
"""
    
    # Combine
    note_content = frontmatter + "\n" + content
    
    # Write file
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(note_content, encoding="utf-8")
    
    return filepath


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Enrich URLs with metadata and create resource notes")
    parser.add_argument("url", help="URL to fetch and enrich")
    parser.add_argument("--output", help="Output directory (e.g., ~/remember/Resources/articles/)")
    parser.add_argument("--date", help="Session date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Fetch metadata only, don't create note")
    args = parser.parse_args()
    
    # Fetch metadata
    print(f"Fetching: {args.url}", file=sys.stderr)
    metadata = extract_metadata(args.url)
    
    # Output metadata
    print(json.dumps(metadata, indent=2))
    
    # Create note if not dry-run
    if not args.dry_run and args.output:
        output_dir = Path(args.output).expanduser()
        note_path = create_resource_note(metadata, output_dir, session_date=args.date)
        print(f"\nCreated: {note_path}", file=sys.stderr)
    elif not args.dry_run:
        print("\nUse --output to specify where to create the note", file=sys.stderr)


if __name__ == "__main__":
    main()
