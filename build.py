#!/usr/bin/env python3
"""Scout static builder. Posts: posts/YYYY-MM-DD-slug.html with a header block:
<!--
title: ...
date: YYYY-MM-DD
summary: ...
-->
followed by an HTML body fragment. Output goes to site/."""
import os, re, html, shutil
ROOT=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(ROOT,'posts'); S=os.path.join(ROOT,'site')
CSS=""":root{--bg:#fdfdfc;--fg:#1d1d1f;--mu:#6b6b70;--ac:#0b62d6;--bd:#e5e5e5}
@media(prefers-color-scheme:dark){:root{--bg:#111214;--fg:#e8e8ea;--mu:#9a9aa2;--ac:#6ab0ff;--bd:#2a2b2f}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
main,header,footer{max-width:720px;margin:0 auto;padding:0 20px}header{padding-top:32px;border-bottom:1px solid var(--bd)}
header a.brand{font-weight:800;font-size:28px;color:var(--fg);text-decoration:none}header p{color:var(--mu);margin:4px 0 16px}
a{color:var(--ac)}h1{line-height:1.25;margin:32px 0 4px}h2{margin-top:36px}h3{margin:28px 0 4px}.meta{color:var(--mu);font-size:15px}
li{margin:6px 0}.post-list{list-style:none;padding:0}.post-list li{padding:12px 0;border-bottom:1px solid var(--bd)}
.post-list .d{color:var(--mu);font-size:14px;font-family:ui-monospace,monospace;margin-right:10px}.why{color:var(--mu);font-style:italic}
code{font-size:.9em;background:var(--bd);padding:1px 5px;border-radius:4px}footer{color:var(--mu);font-size:14px;padding:40px 20px}"""
def page(title,body,depth=0):
    r='../'*depth
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="stylesheet" href="{r}style.css"></head><body><header><a class="brand" href="{r}index.html">Scout</a><p>Daily AI &amp; engineering briefing for builders. No hype.</p></header><main>{body}</main><footer>Scout &middot; written for Dan Scott</footer></body></html>'
posts=[]
for f in sorted(os.listdir(P)):
    if not f.endswith('.html'): continue
    t=open(os.path.join(P,f)).read(); m=re.match(r'\s*<!--(.*?)-->(.*)',t,re.S)
    meta=dict(l.split(':',1) for l in m.group(1).strip().splitlines() if ':' in l); meta={k.strip():v.strip() for k,v in meta.items()}
    meta['slug']=f[:-5]; meta['body']=m.group(2); posts.append(meta)
posts.sort(key=lambda p:(p['date'],p.get('order','9'),p['slug']),reverse=True)
shutil.rmtree(S,ignore_errors=True); os.makedirs(S+'/posts'); open(S+'/style.css','w').write(CSS); open(S+'/.nojekyll','w').write('')
for p in posts:
    b=f'<article><h1>{html.escape(p["title"])}</h1><p class="meta">{p["date"]}</p>{p["body"]}</article><p><a href="../index.html">&larr; All editions</a></p>'
    open(f'{S}/posts/{p["slug"]}.html','w').write(page(p['title']+' · Scout',b,1))
latest=posts[0]['date'] if posts else ''
li=lambda p:f'<li><span class="d">{p["date"]}</span><a href="posts/{p["slug"]}.html">{html.escape(p["title"])}</a><br><span class="meta">{html.escape(p.get("summary",""))}</span></li>'
body=f'<h2>Latest edition &middot; {latest}</h2><ul class="post-list">'+''.join(li(p) for p in posts if p['date']==latest)+'</ul><h2>Archive</h2><ul class="post-list">'+''.join(li(p) for p in posts if p['date']!=latest)+'</ul>'
open(S+'/index.html','w').write(page('Scout — daily AI & engineering briefing',body))
print(f'built {len(posts)} posts -> {S}')
