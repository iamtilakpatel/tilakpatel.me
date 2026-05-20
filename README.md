# tilakpatel.dev — Static Site Generator

Personal website and build log for Tilak Patel.

## Architecture

```
├── build.py              ← Run this to generate the site
├── content/
│   ├── data.json         ← All site text, nav, projects, timeline
│   └── posts/
│       ├── nasa-challenge-submission.md
│       ├── i2c-debugging-hell.md
│       └── capture-first-compress-later.md
├── templates/
│   ├── base.html         ← Master layout (nav + footer)
│   ├── index.html
│   ├── about.html
│   ├── projects.html
│   ├── blog.html
│   └── post.html
├── assets/
│   ├── css/style.css
│   └── js/main.js
└── dist/                 ← Generated output (gitignored)
```

## Workflow

1. **Edit content** → `content/data.json` or drop a new `.md` into `content/posts/`
2. **Run generator** → `python build.py`
3. **Preview** → Open `dist/index.html` in your browser (no server needed)
4. **Deploy** → Push the `dist/` folder to GitHub Pages

## Setup (one time)

```bash
pip install jinja2 markdown
```

## Adding a Blog Post

1. Create `content/posts/my-new-post.md`
2. Add frontmatter at the top:
   ```yaml
   ---
   date: May 2026
   title: My New Post
   tags: [Hardware, ESP32]
   excerpt: One-line summary for the listing page.
   ---
   ```
3. Write your post in Markdown below the `---`
4. Run `python build.py`

## Design Philosophy

- **Content + UI separated**: Edit JSON/Markdown without touching HTML/CSS
- **Zero client-side JS for rendering**: Everything is baked to static HTML
- **Minimal light theme**: Same clean aesthetic as before, now fully static

## License

MIT — Tilak Patel, 2026
