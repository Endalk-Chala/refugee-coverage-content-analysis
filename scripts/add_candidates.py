"""Append search hits to data/output/search_candidates.csv.
stdin: JSON list of {"outlet","query","items":[{"title","url","snippet"|"date"}]}. Decodes DuckDuckGo redirect links."""
import csv, json, sys, pathlib, datetime, urllib.parse, re
batches = json.load(sys.stdin)
p = pathlib.Path("data/output/search_candidates.csv"); new = not p.exists()
seen = set() if new else {r["url"] for r in csv.DictReader(open(p, encoding="utf-8"))}
def clean(u):
    if "duckduckgo.com/l/" in u:
        q = urllib.parse.parse_qs(urllib.parse.urlparse(u).query); u = q.get("uddg", [u])[0]
    u = u.split("?")[0].split("#")[0]
    return re.sub(r"^http://", "https://", u)
with open(p, "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new: w.writerow(["outlet","query","date_raw","title","url","snippet","searched_at","screen"])
    for b in batches:
        added = 0
        for it in b["items"]:
            u = clean(it["url"])
            if u in seen or "duckduckgo.com" in u: continue
            seen.add(u); added += 1
            w.writerow([b["outlet"], b["query"], it.get("date",""), it.get("title",""), u, it.get("snippet",""), datetime.date.today().isoformat(), ""])
        print(f"{b['outlet']:12} | {b['query'][:50]:50} | {len(b['items']):2d} hits, {added:2d} new")
print("total candidates:", len(seen))
