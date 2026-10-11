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

## Hosting (live)
- Live: https://danscottdev.github.io/scout-daily/  (repo: github.com/danscottdev/scout-daily, Pages source = GitHub Actions)
- Every push to `main` runs `.github/workflows/pages.yml` (build.py -> deploy `site/`). Watch it with:
  `gh run list -R danscottdev/scout-daily --limit 1` / `gh run watch <id> -R danscottdev/scout-daily --exit-status`
- Auth: fine-grained token in env var `GH_TOKEN` (never print it). The repo-local git credential helper reads it at push time,
  so no token is stored in .git/config. Requires `$GH_TOKEN` to be set in the shell running `git push`.
  If the remote/helper is ever missing (fresh clone), restore it:
  ```bash
  git remote add origin https://github.com/danscottdev/scout-daily.git
  git config credential.https://github.com.helper '!f(){ echo username=x-access-token; echo "password=$GH_TOKEN"; }; f'
  ```
- The token cannot run `gh workflow run` (403 on workflow dispatch). To redeploy without changing content, push an empty commit:
  `git commit --allow-empty -m redeploy && git push`
- Verify: `curl -s -o /dev/null -w "%{http_code}" https://danscottdev.github.io/scout-daily/posts/<slug>.html`
