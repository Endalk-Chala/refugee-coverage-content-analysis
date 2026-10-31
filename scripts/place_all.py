"""File every browser download (*.tmp in Downloads) into data/fulltext/, named from the candidate workbook by URL match."""
import re, pathlib, shutil, sys
import openpyxl
HOME = pathlib.Path.home()
DL = HOME / "mnt/Downloads"; ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / "data/fulltext"; DEST.mkdir(exist_ok=True)
TRASH = DL / "_to_delete"; TRASH.mkdir(exist_ok=True)
SEP = "-" * 72
BOILER = re.compile(r"^(Create an account or log in to save stories\.|Thanks for liking this story!.*|Save|SHARE|Listen|Dear reader,|When our communities are navigating uncertainty.*|At MPR News, we.re committed.*|Do you want to receive the Minnesota Today newsletter.*|Getting these updates in your inbox.*|Get the Minnesota Today Newsletter.*|Providing Support for MPR.*|CLICK HERE TO GET THE FOX NEWS APP|CLICK HERE TO DOWNLOAD THE FOX NEWS APP|Fox News. .*contributed to this report\.|.*is a (politics )?(writer|reporter) (for|at) Fox News Digital.*|Story tips can be sent to.*|Get the .* newsletter.*|Sign up for .*|Follow .* on X|Correction:.*)$")
def norm(u):
    u = re.sub(r"^https?://(www\.|us\.)?", "", u.strip()).rstrip("/").split("?")[0].replace("/index.html", "")
    return re.sub(r"^(msnbc\.com|ms\.now)/", "msnbc/", u)
wb = openpyxl.load_workbook(ROOT / "data/arl_candidate_corpus.xlsx", read_only=True)
meta = {}
for i, row in enumerate(wb["Candidate_Corpus"].iter_rows(values_only=True)):
    if i == 0 or not row[5]: continue
    case, outlet, cat, date, head, url, genre, win, notes = row[:9]
    meta[norm(url)] = dict(case=case, outlet=outlet, category=cat, date=str(date or ""), headline=head or "", genre=genre or "", in_window=win or "", notes=notes or "")
# second source of metadata: discovery hits in search_candidates.csv
import csv as _csv
cand = pathlib.Path(ROOT / "data/output/search_candidates.csv")
if cand.exists():
    for r in _csv.DictReader(open(cand, encoding="utf-8")):
        k = norm(r["url"])
        if k in meta: continue
        t = (r["title"] + " " + r["url"]).lower()
        case = "Afrikaner" if ("afrikaner" in t or "south africa" in t or "white south" in t) else ("Operation PARRIS" if ("parris" in t or "minnesota" in t or "refugee" in t) else "Screen")
        meta[k] = dict(case=case, outlet=r["outlet"].replace(" (ms.now)", ""), category="", date=r["date_raw"], headline=r["title"], genre="", in_window="", notes="discovered via site-restricted search " + r["searched_at"] + "; query: " + r["query"])
done = 0
for tmp in sorted(DL.glob("*.tmp"), key=lambda p: p.stat().st_mtime):
    txt = tmp.read_text(encoding="utf-8", errors="replace")
    head, _, body = txt.partition(SEP)
    url = next((l.split(":",1)[1].strip() for l in head.splitlines() if l.startswith("URL:")), "")
    m = meta.get(norm(url))
    if not m:
        print("NO MATCH:", url); continue
    pub = next((l.split(":",1)[1].strip() for l in head.splitlines() if l.startswith("PUBLISHED (meta):")), "")
    date = m["date"] if re.match(r"\d{4}-\d{2}-\d{2}$", m["date"]) else (pub[:10] if pub else "undated")
    case = "parris" if "PARRIS" in m["case"] else m["case"].lower()
    outlet = re.sub(r"[^a-z]", "", m["outlet"].lower().split()[0])
    slug = re.sub(r"[^a-z0-9]+", "-", m["headline"].lower()).strip("-")[:60]
    name = f"{case}_{outlet}_{date}_{slug}.txt"
    lines = [l for l in body.splitlines() if not BOILER.match(l.strip()) and not l.strip().startswith("This transcript was produced")]
    header = (f"CASE: {m['case']}\nOUTLET: {m['outlet']}\nCATEGORY: {m['category']}\nDATE (recorded): {m['date']}\n"
              f"DATE (used): {date}\nHEADLINE (recorded): {m['headline']}\nGENRE (guess): {m['genre']}\nIN WINDOW (recorded): {m['in_window']}\n"
              f"NOTE: {m['notes']}\n")
    (DEST / name).write_text(header + head + SEP + "\n".join(lines), encoding="utf-8")
    shutil.move(str(tmp), TRASH / tmp.name)
    print(f"{len(' '.join(lines).split()):5d}w  {name}"); done += 1
print(f"filed {done}")
