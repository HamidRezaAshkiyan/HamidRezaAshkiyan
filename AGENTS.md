# AGENTS.md — HamidRezaAshkiyan (GitHub Profile README)

## Overview
GitHub profile repository for **Hamid Reza Ashkiyan** (`github.com/HamidRezaAshkiyan`). Renders the public profile `README.md` (bio, tech stack, featured open-source projects, and latest engineering blog posts) with an automated daily GitHub Actions workflow that syncs recent blog entries from `https://hamidrezaashkiyan.github.io/feed.xml`.

## Tech Stack & Requirements
- **Content:** GitHub Flavored Markdown + inline HTML badges (`README.md`)
- **Automation:** Python 3.12+ standard library only (`urllib.request`, `xml.etree.ElementTree`, `email.utils`, `re`, `pathlib`) — zero external dependencies
- **CI/CD:** GitHub Actions (`.github/workflows/sync-blog.yml`)

## Repository Structure
```text
.
├── README.md                        # GitHub profile landing page (auto-updated blog section)
├── scripts/
│   └── sync_blog.py                 # Fetches RSS feed and updates README.md between marker comments
└── .github/
    └── workflows/
        └── sync-blog.yml            # Daily cron (06:00 UTC) + workflow_dispatch RSS sync & auto-commit
```

## Architecture & Key Flows
- **RSS Sync (`scripts/sync_blog.py`):** Fetches `https://hamidrezaashkiyan.github.io/feed.xml`, parses up to `MAX_POSTS = 5` `<item>` entries (`title`, `link`, `pubDate` formatted as `YYYY-MM-DD`), and replaces the content between `<!-- BLOG-POST-LIST:START -->` and `<!-- BLOG-POST-LIST:END -->` in `README.md`.
- **Scheduled Workflow (`.github/workflows/sync-blog.yml`):** Runs daily at `06:00 UTC` (or manually via `workflow_dispatch`), executes `python3 scripts/sync_blog.py`, and commits + pushes `README.md` if changed using `github-actions[bot]`.

## Development & Commands
```bash
# Manually sync the latest 5 blog posts from RSS into README.md
python3 scripts/sync_blog.py
```

## Configuration & Environment
No environment variables or secrets are required locally; GitHub Actions uses its default `GITHUB_TOKEN` with `permissions: contents: write`. Constants (`FEED_URL`, `MAX_POSTS`, marker comments) are defined at the top of `scripts/sync_blog.py`.

## Conventions & Gotchas
- **Preserve Sync Markers:** Never remove or rename `<!-- BLOG-POST-LIST:START -->` and `<!-- BLOG-POST-LIST:END -->` in `README.md`; `scripts/sync_blog.py` raises a `RuntimeError` if either marker is missing.
- **Do Not Hand-Edit the Blog List:** Any manual edits inside the blog markers will be overwritten on the next daily `sync-blog.yml` run. Update posts in the `personal-website` repo instead.
- **External Assets:** The banner image (`og-card.png`) and links point to `https://hamidrezaashkiyan.github.io/`; keep URLs aligned with the deployed personal website.
