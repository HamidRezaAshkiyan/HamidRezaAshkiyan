#!/usr/bin/env python3
"""Sync latest engineering blog posts from hamidrezaashkiyan.github.io/feed.xml into README.md."""

from __future__ import annotations

import email.utils
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://hamidrezaashkiyan.github.io/feed.xml"
README_PATH = Path(__file__).resolve().parent.parent / "README.md"
MAX_POSTS = 5

START_MARKER = "<!-- BLOG-POST-LIST:START -->"
END_MARKER = "<!-- BLOG-POST-LIST:END -->"


def fetch_posts(feed_url: str, max_posts: int) -> list[tuple[str, str, str]]:
    req = urllib.request.Request(
        feed_url,
        headers={"User-Agent": "HamidRezaAshkiyan-Profile-Sync/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError("Invalid RSS feed: missing <channel> element")

    posts: list[tuple[str, str, str]] = []
    for item in channel.findall("item")[:max_posts]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date_raw = (item.findtext("pubDate") or "").strip()

        date_str = ""
        if pub_date_raw:
            try:
                parsed = email.utils.parsedate_to_datetime(pub_date_raw)
                date_str = parsed.strftime("%Y-%m-%d")
            except (TypeError, ValueError):
                date_str = pub_date_raw

        if title and link:
            posts.append((title, link, date_str))

    return posts


def render_markdown(posts: list[tuple[str, str, str]]) -> str:
    lines = []
    for title, link, date_str in posts:
        if date_str:
            lines.append(f"- [{title}]({link}) — `{date_str}`")
        else:
            lines.append(f"- [{title}]({link})")
    return "\n".join(lines)


def update_readme(readme_path: Path, rendered: str) -> bool:
    content = readme_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"({re.escape(START_MARKER)}).*?({re.escape(END_MARKER)})",
        flags=re.DOTALL,
    )
    if not pattern.search(content):
        raise RuntimeError(
            f"Could not find {START_MARKER} ... {END_MARKER} markers in {readme_path}"
        )

    updated = pattern.sub(rf"\1\n{rendered}\n\2", content, count=1)
    if updated == content:
        return False

    readme_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    posts = fetch_posts(FEED_URL, MAX_POSTS)
    if not posts:
        print("No posts found in RSS feed; leaving README.md unchanged.", file=sys.stderr)
        return 1

    rendered = render_markdown(posts)
    changed = update_readme(README_PATH, rendered)
    print(f"Synced {len(posts)} posts from {FEED_URL} (changed={changed}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
