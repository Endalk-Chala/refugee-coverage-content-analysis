"""Log headline+link hits for paywalled/blocked outlets into data/output/search_candidates.csv.
stdin: JSON list of {"outlet","query","case","items":[{"title","url","date"?,"snippet"?,"screen"?}]}.
Each row gets fulltext = "paywalled; headline logged; library route" unless the item sets "fulltext".
Date is taken from the URL (YYYY/MM/DD) when the item gives none. Window screen is applied automatically."""
import csv, json, sys, pathlib, datetime, re, urllib.parse
WIN = {"Afrikaner": ("2025-02-01", "2025-12-31"), "PARRIS": ("2025-12-01", "2026-10-31")}
p = pathlib.Path("data/output/search_candidates.csv")
rows = list(csv.DictReader(open(p, encoding="utf-8")))
cols = list(rows[0].keys()); seen = {r["url"] for r in rows}
def clean(u):
    if "duckduckgo.com/l/" in u:
        u = urllib.parse.parse_qs(urllib.parse.urlparse(u).query).get("uddg", [u])[0]
    return re.sub(r"^http://", "https://", u.split("?")[0].split("#")[0])
out = []
for b in json.load(sys.stdin):
    added = 0
    for it in b["items"]:
        u = clean(it["url"])
        if u in seen: continue
        seen.add(u); added += 1
        d = it.get("date", "")
        if not d:
            m = re.search(r"/(20\d\d)/(\d\d)/(\d\d)/", u); d = f"{m[1]}-{m[2]}-{m[3]}" if m else ""
        screen = it.get("screen", "")
        if not screen and d:
            lo, hi = WIN[b["case"]]
            screen = "in window" if lo <= d <= hi else f"outside {b['case']} window"
        out.append({"outlet": b["outlet"], "query": b["query"], "date_raw": d, "title": it["title"], "url": u,
                    "snippet": it.get("snippet", ""), "searched_at": datetime.date.today().isoformat(),
                    "screen": screen, "fulltext": it.get("fulltext", "paywalled; headline logged; library route")})
    print(f"{b['outlet']:18} | {b['case']:9} | {len(b['items']):2d} hits, {added:2d} new")
with open(p, "a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); [w.writerow(r) for r in out]
print("total candidates:", len(seen))
