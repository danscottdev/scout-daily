# Scout — daily AI & engineering briefing

Zero-dependency static blog (Python 3 stdlib only).

- `posts/YYYY-MM-DD-slug.html` — one file per post: a `<!-- title/date/order/summary -->` header, then an HTML body fragment.
  `order:` controls ordering within a day (1 = Quick Hits first, 2+ = deep dives).
- `build.py` — renders `site/` (index with newest edition first + archive, post pages, dark-mode CSS, `.nojekyll`).
- `site/` — the deployable output. Never hand-edit it.

## Publish a new edition (every day)
```bash
cd /workspace/scout-blog
# 1. write posts/2026-10-12-quick-hits.html (copy yesterday's as a template), plus 0-3 deep dives
python3 build.py                         # 2. rebuild site/
python3 -m http.server -d site 8000 &    # 3. optional local preview at http://localhost:8000
git add -A && git commit -m "Edition 2026-10-12" && git push origin main   # 4. publish
```

## Hosting (one-time setup, NOT DONE YET — blocked on auth)
Target: GitHub Pages at https://danscottdev.github.io/scout-daily/
1. `gh auth login` on the box (Dan, once), or create the empty public repo `danscottdev/scout-daily` on github.com.
2. `cd /workspace/scout-blog && gh repo create danscottdev/scout-daily --public --source . --push`
   (or `git remote add origin https://github.com/danscottdev/scout-daily.git && git push -u origin main`)
3. Enable Pages with GitHub Actions: the workflow in `.github/workflows/pages.yml` builds and deploys `site/` on every push:
   `gh api -X POST repos/danscottdev/scout-daily/pages -f build_type=workflow`
