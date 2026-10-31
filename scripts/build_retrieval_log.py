"""Rebuild data/output/retrieval_log.csv from the headers of data/fulltext/*.txt."""
import csv, pathlib, re
root = pathlib.Path(__file__).resolve().parents[1]
SEP = "-" * 72
rows = []
for f in sorted((root / "data/fulltext").glob("*.txt")):
    t = f.read_text(encoding="utf-8")
    head, _, body = t.partition(SEP)
    h = {}
    for line in head.splitlines():
        if ": " in line or line.endswith(":"):
            k, _, v = line.partition(":"); h[k.strip()] = v.strip()
    rows.append({"file": f.name, "case": h.get("CASE", ""), "outlet": h.get("OUTLET", ""),
                 "byline_recorded": h.get("BYLINE (recorded)", ""), "date_recorded": h.get("DATE (recorded)", ""), "date_used": h.get("DATE (used)", "") or (h.get("PUBLISHED (meta)", "")[:10] if h.get("PUBLISHED (meta)") else h.get("DATE (recorded)", "")),
                 "headline_recorded": h.get("HEADLINE (recorded)", ""), "page_title": h.get("TITLE", ""),
                 "url": h.get("URL", ""), "published_meta": h.get("PUBLISHED (meta)", ""),
                 "modified_meta": h.get("MODIFIED (meta)", ""), "retrieved": h.get("RETRIEVED", ""),
                 "words_body": len(body.split()), "in_window": "", "include": "", "note": h.get("NOTE", "")})
# window flags per search_protocol.md decision of 31 Oct 2026 (Afrikaner 1 Feb–31 Dec 2025; PARRIS 1 Dec 2025–31 Oct 2026)
for r in rows:
    d, c = (r["date_used"] if re.match(r"\d{4}-\d{2}-\d{2}$", r["date_used"]) else r["date_recorded"]), r["case"]
    if "PARRIS" in c: c = "PARRIS"
    if c == "PARRIS": r["in_window"] = "yes" if "2025-12-01" <= d <= "2026-10-31" else "no"
    elif c == "Afrikaner": r["in_window"] = "yes" if "2025-02-01" <= d <= "2025-12-31" else "no"
    else: r["in_window"] = "n/a"
    r["include"] = "yes" if r["in_window"] == "yes" else "no (see note)"
out = root / "data/output/retrieval_log.csv"
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['case'][:10]:10} {r['outlet'][:13]:13} {r['date_used'][:10]:10} {r['in_window']:4} {r['words_body']:5d}w  {r['headline_recorded'][:50]}")
print(f"\n{len(rows)} files, {sum(r['words_body'] for r in rows)} body words -> {out.relative_to(root)}")
