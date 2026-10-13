#!/usr/bin/env python3
"""
TILAK.DEV Static Site Generator
Usage:   python build.py
Output:  dist/  ← static HTML + assets, ready for GitHub Pages
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    raise SystemExit("❌  pip install jinja2")

try:
    import markdown
except ImportError:
    raise SystemExit("❌  pip install markdown")


# ── paths ──
ROOT = Path(__file__).parent.resolve()
CONTENT = ROOT / "content"
POSTS = CONTENT / "posts"
TEMPLATES = ROOT / "templates"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"


# ── helpers ──
def clean_dist():
    if DIST.exists():
        shutil.rmtree(DIST)

    DIST.mkdir(parents=True)
    (DIST / "assets" / "css").mkdir(parents=True)
    (DIST / "assets" / "js").mkdir(parents=True)

    shutil.copy2(ROOT / "CNAME", DIST / "CNAME")


def load_data():
    with open(CONTENT / "data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def parse_frontmatter(text: str):
    """Parse simple --- yaml --- frontmatter from markdown."""
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    fm_text, body = parts[1].strip(), parts[2].strip()
    fm = {}

    for line in fm_text.splitlines():
        if ":" not in line:
            continue

        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()

        # handle [a, b, c] lists
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            val = [
                v.strip().strip('"')
                for v in inner.split(",")
                if v.strip()
            ]

        fm[key] = val

    return fm, body


def collect_posts():
    posts = []

    if not POSTS.exists():
        return posts

    for md_file in POSTS.glob("*.md"):
        raw = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)

        html_body = markdown.markdown(
            body,
            extensions=["extra", "fenced_code", "tables", "toc"],
        )

        posts.append({
            "slug": md_file.stem,
            "title": fm.get("title", md_file.stem),
            "date": fm.get("date", ""),
            "tags": fm.get("tags", []),
            "excerpt": fm.get("excerpt", ""),
            "body": html_body,
        })

    posts.sort(
        key=lambda p: datetime.strptime(p["date"], "%B %Y"),
        reverse=True,
    )

    return posts


def collect_projects(data):
    """
    Convert the projects object in data.json into a renderable list.

    page_title and page_subtitle are page-level metadata, not projects.
    Page-level settings (index_kicker, index_intro, …) and any non-object
    value are skipped as well, so new page metadata can be added freely.
    Each project can optionally define its own slug. If omitted, the
    data.json key is converted from underscores to hyphens.
    """
    projects_data = data.get("projects", {})
    project_items = []

    for project_id, project in projects_data.items():
        if project_id in ("page_title", "page_subtitle"):
            continue
        if not isinstance(project, dict) or project_id.startswith("index_"):
            continue

        item = dict(project)
        item["id"] = project_id
        item["slug"] = project.get(
            "slug",
            project_id.replace("_", "-"),
        )

        project_items.append(item)

    return project_items


def copy_assets():
    if not ASSETS.exists():
        return

    for src in ASSETS.rglob("*"):
        if src.is_file():
            rel = src.relative_to(ASSETS)
            dst = DIST / "assets" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def guard_private_repo_links(html: str, data: dict) -> str:
    """De-link any anchor that points to a non-public project repository.

    Driven purely by the data schema: a project entry with
    ``"repository_public": false`` has its ``repo_url`` suppressions applied to
    every generated page (including blog-post bodies). Setting the flag back to
    ``true`` (or removing it) restores the links on the next build.
    """
    import re

    private_urls = [
        p["repo_url"]
        for p in (data.get("projects") or {}).values()
        if isinstance(p, dict) and p.get("repo_url") and p.get("repository_public") is False
    ]
    for url in private_urls:
        pattern = r'<a\s+href="' + re.escape(url) + r'"[^>]*>(.*?)</a>'
        html = re.sub(
            pattern,
            lambda m: re.sub(r"\s*(?:→|↗|\u2192|\u2197)\s*$", "", m.group(1).strip()),
            html,
        )
    return html


def render_site(data, posts):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    project_items = collect_projects(data)

    ctx = {
        **data,
        "posts": posts,
        "project_items": project_items,
    }

    # ── standard static pages ──
    for tmpl_name, out_name in [
        ("index.html", "index.html"),
        ("about.html", "about.html"),
        ("blog.html", "blog.html"),
    ]:
        tmpl = env.get_template(tmpl_name)
        html = tmpl.render(
            **ctx,
            page=out_name.replace(".html", ""),
        )

        html = guard_private_repo_links(html, data)
        (DIST / out_name).write_text(html, encoding="utf-8")
        print(f"  ✓ {out_name}")

    # ── projects index ──
    projects_tmpl = env.get_template("projects.html")
    projects_html = projects_tmpl.render(
        **ctx,
        page="projects",
    )

    # Keep the old URL working:
    # /projects.html
    (DIST / "projects.html").write_text(
        guard_private_repo_links(projects_html, data),
        encoding="utf-8",
    )
    print("  ✓ projects.html")

    # Also create the clean projects index:
    # /projects/
    projects_dir = DIST / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)

    (projects_dir / "index.html").write_text(
        guard_private_repo_links(projects_html, data),
        encoding="utf-8",
    )
    print("  ✓ projects/index.html")

    # ── individual project detail pages ──
    # Projects that opt into the approved case-study layout render through
    # templates/casestudy.html (+ its partials); everything else keeps the
    # legacy template unchanged until its own redesign is approved.
    for project in project_items:
        slug = project["slug"]

        output_dir = DIST / "projects" / slug
        output_dir.mkdir(parents=True, exist_ok=True)

        is_case_study = bool(project.get("case_study"))
        tmpl = env.get_template("casestudy.html" if is_case_study else "project.html")
        html = tmpl.render(
            **ctx,
            project=project,
            page="project",
            home_nav=is_case_study,
        )
        html = guard_private_repo_links(html, data)

        (output_dir / "index.html").write_text(
            html,
            encoding="utf-8",
        )

        print(f"  ✓ projects/{slug}/index.html")

    # ── blog posts ──
    post_tmpl = env.get_template("post.html")

    for post in posts:
        html = post_tmpl.render(
            **ctx,
            post=post,
            page="post",
        )

        html = guard_private_repo_links(html, data)
        (DIST / f"{post['slug']}.html").write_text(
            html,
            encoding="utf-8",
        )

        print(f"  ✓ {post['slug']}.html")


# ── main ──
def main():
    print("🔧  Building TILAK.DEV…")

    clean_dist()

    data = load_data()
    posts = collect_posts()
    project_items = collect_projects(data)

    print(f"📄  Found {len(posts)} blog post(s)")
    print(f"🤖  Found {len(project_items)} project(s)")

    render_site(data, posts)
    copy_assets()

    print(f"\n🚀  Done. Output in: {DIST}/")
    print("    →  Deploy the 'dist/' folder to GitHub Pages.")


if __name__ == "__main__":
    main()
