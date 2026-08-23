#!/usr/bin/env python3
"""Create a pending persona content stub from a YouTube ID."""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))
YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,}$")
CONTENT_ID_RE = re.compile(r"^C-(\d{3})")


def extract_youtube_id(raw: str) -> str:
    value = raw.strip()
    patterns = [
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]+)",
        r"(?:youtu\.be/)([A-Za-z0-9_-]+)",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            value = match.group(1)
            break
    value = value.split("&", 1)[0].split("?", 1)[0].strip()
    if not YOUTUBE_ID_RE.match(value):
        raise SystemExit(f"invalid YouTube ID: {raw}")
    return value


def next_content_number(contents_dir: Path) -> int:
    max_number = 0
    for path in contents_dir.glob("C-*.md"):
        match = CONTENT_ID_RE.match(path.stem)
        if match:
            max_number = max(max_number, int(match.group(1)))
    return max_number + 1


def main(argv: list[str]) -> int:
    if len(argv) < 2 or len(argv) > 3:
        print("usage: youtube_content_stub.py <youtube-id-or-url> [intent]", file=sys.stderr)
        return 2

    repo = Path(__file__).resolve().parents[2]
    contents_dir = repo / "persona" / "contents"
    if not contents_dir.is_dir():
        raise SystemExit(f"contents dir not found: {contents_dir}")

    youtube_id = extract_youtube_id(argv[1])
    intent = argv[2].strip() if len(argv) == 3 else ""
    number = next_content_number(contents_dir)
    content_id = f"C-{number:03d}"
    today = datetime.now(KST).strftime("%Y.%m.%d")
    path = contents_dir / f"{content_id}-pending.md"
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing file: {path}")

    text = f"""---
type: content
id: {content_id}
date: "{today}"
day: "Day {number:02d}"
title:
  ko: "Pending YouTube Content"
  en: "Pending YouTube Content"
summary:
  ko: "YouTube enrich 대기 중"
  en: "Pending YouTube enrich"
youtubeId: {youtube_id}
status: pending
intent: "{intent}"
---
"""
    path.write_text(text, encoding="utf-8")
    rel = path.relative_to(repo)
    print(f"created: {rel}")
    print(f"id: {content_id}")
    print(f"youtubeId: {youtube_id}")
    print("status: pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
