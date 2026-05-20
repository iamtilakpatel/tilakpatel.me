#!/usr/bin/env python3
"""
TILAK.DEV Static Site Generator
Usage:   python build.py
Output:  dist/  ← flat HTML + assets, ready for GitHub Pages
"""
import json, shutil
from pathlib import Path

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
POSTS   = CONTENT / "posts"
TEMPLATES = ROOT / "templates"
ASSETS  = ROOT / "assets"
DIST    = ROOT / "dist"

# ── helpers ──
def clean_dist():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "assets" / "css").mkdir(parents=True)
    (DIST / "assets" / "js").mkdir(parents=True)

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
            val = [v.strip().strip('"') for v in inner.split(",") if v.strip()]
        fm[key] = val
    return fm, body

def collect_posts():
    posts = []
    if not POSTS.exists():
        return posts
    for md_file in sorted(POSTS.glob("*.md")):
        raw = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)
        html_body = markdown.markdown(
            body,
            extensions=["extra", "fenced_code", "tables", "toc"]
        )
        posts.append({
            "slug": md_file.stem,
            "title": fm.get("title", md_file.stem),
            "date": fm.get("date", ""),
            "tags": fm.get("tags", []),
            "excerpt": fm.get("excerpt", ""),
            "body": html_body,
        })
    posts.reverse()          # newest first (alphabetical / date order)
    return posts

def copy_assets():
    if not ASSETS.exists():
        return
    for src in ASSETS.rglob("*"):
        if src.is_file():
            rel = src.relative_to(ASSETS)
            dst = DIST / "assets" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

def render_site(data, posts):
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        trim_blocks=True,
        lstrip_blocks=True
    )
    ctx = {**data, "posts": posts}

    # static pages
    for tmpl_name, out_name in [
        ("index.html", "index.html"),
        ("about.html", "about.html"),
        ("projects.html", "projects.html"),
        ("blog.html", "blog.html"),
    ]:
        tmpl = env.get_template(tmpl_name)
        html = tmpl.render(**ctx, page=out_name.replace(".html", ""))
        (DIST / out_name).write_text(html, encoding="utf-8")
        print(f"  ✓ {out_name}")

    # blog posts
    post_tmpl = env.get_template("post.html")
    for post in posts:
        html = post_tmpl.render(**ctx, post=post, page="post")
        (DIST / f"{post['slug']}.html").write_text(html, encoding="utf-8")
        print(f"  ✓ {post['slug']}.html")

# ── main ──
def main():
    print("🔧  Building TILAK.DEV…")
    clean_dist()
    data = load_data()
    posts = collect_posts()
    print(f"📄  Found {len(posts)} blog post(s)")
    render_site(data, posts)
    copy_assets()
    print(f"\n🚀  Done. Output in: {DIST}/")
    print("    →  Deploy the 'dist/' folder to GitHub Pages.")

if __name__ == "__main__":
    main()
