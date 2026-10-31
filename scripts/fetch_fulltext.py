"""Fetch full text of candidate articles into data/fulltext/ and log retrieval."""
import csv, re, time, pathlib, datetime, sys
import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "fulltext"; OUT.mkdir(parents=True, exist_ok=True)
LOG = ROOT / "data" / "output" / "retrieval_log.csv"; LOG.parent.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}

# case, outlet, byline(as recorded), date, headline, url, note
ITEMS = [
("PARRIS","MPR News","Sarah Thamer","2026-01-13","Resettlement agency head says new Homeland Security operation 'terrifying' refugee families","https://www.mprnews.org/story/2026/01/13/operation-parris-dhs-terrifying-refugee-families",""),
("PARRIS","MPR News","Sarah Thamer (Regina Medina contributed)","2026-01-21","'ICE is here!' Refugee family with legal status unsettled by early morning arrest","https://www.mprnews.org/story/2026/01/21/ice-is-here-refugee-family-with-legal-status-unsettled-by-early-morning-arrest",""),
("PARRIS","MPR News","Emily Bright and Aleesa Kuznetsov","2026-01-29","Lawyer: DHS not complying with order to release detained refugees from Minnesota","https://www.mprnews.org/story/2026/01/29/lawyer-dhs-not-complying-with-order-to-release-detained-refugees-from-minnesota",""),
("PARRIS","MPR News","Sarah Thamer","2026-01-29","Trapped inside: A Minnesota refugee family's life on hold amid ICE arrests","https://www.mprnews.org/story/2026/01/29/trapped-inside-a-minnesota-refugee-familys-life-on-hold-amid-ice-arrests",""),
("PARRIS","MPR News","Jon Collins","2026-02-20","Immigration advocates challenge federal refugee policy in court","https://www.mprnews.org/story/2026/02/20/immigration-advocates-challenge-federal-refugee-policy-in-court",""),
("PARRIS","MPR News","MPR News Staff","2026-02-28","Judge stops DHS from detaining lawful refugees in Minnesota","https://www.mprnews.org/story/2026/02/28/judge-stops-dhs-from-detaining-lawful-refugees-in-minnesota",""),
("Afrikaner","MPR News (NPR wire)","Kate Bartlett (NPR)","2025-05-12","White South African Afrikaner refugees arrive in U.S. on a government-chartered plane","https://www.mprnews.org/story/2025/05/12/npr-first-group-afrikaner-refugees-arrive","NPR wire carried by MPR; decide whether it counts as Minnesota-tier or wire-tier"),
("PARRIS","Sahan Journal","Katelyn Vue and Mohamud Farah","2026-01-21","New federal operation targets Minnesota refugees with legal status","https://sahanjournal.com/immigration/minnesota-refugees-immigration-operation-parris/",""),
("PARRIS","Sahan Journal","Nicolas Scibelli and Anshu Patel","2026-02-06","Refugees' futures uncertain as Operation PARRIS legal fight proceeds","https://sahanjournal.com/immigration/operation-parris-minneapolis-woman-arrested-detained-immigration/",""),
("PARRIS","Sahan Journal","Nicolas Scibelli and Anshu Patel","2026-03-03","Judge extends reprieve for refugees targeted by Operation PARRIS","https://sahanjournal.com/immigration/minnesota-refugees-operation-parris-judge-extends-temporary-protection/",""),
("PARRIS","Sahan Journal","Shubhanjana Das","2026-04-30","Canceled Operation PARRIS interviews leave refugees in limbo","https://sahanjournal.com/immigration/operation-parris-minnesota-refugees-interviews-canceled/",""),
("PARRIS","Sahan Journal","Nicolas Scibelli","2026-10-16","Feds target Minnesota in effort to terminate refugee status","https://sahanjournal.com/immigration/refugee-status-termination-operation-parris-minnesota/","OUTSIDE 31 Jul 2026 window; include only if window extended"),
("Afrikaner","Sahan Journal","Katelyn Vue","2025-01-31","Thousands of refugees destined for Minnesota in limbo under Trump","https://sahanjournal.com/immigration/minnesota-immigration-stalled-president-donald-trump-orders/","Does not mention Afrikaners; before window opens (7 Feb 2025); background only, EXCLUDE from coded corpus"),
]

def extract(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script","style","noscript","figure","aside","nav","footer","header","form","iframe"]): t.decompose()
    # candidate containers, most specific first
    for sel in ["article .entry-content", "div.entry-content", "article .body", "div.article-body", ".story-body", "article", "main"]:
        node = soup.select_one(sel)
        if node:
            paras = [p.get_text(" ", strip=True) for p in node.find_all("p")]
            paras = [p for p in paras if len(p) > 30]
            if len(" ".join(paras)) > 800:
                return "\n\n".join(paras)
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    return "\n\n".join(p for p in paras if len(p) > 30)

def meta(soup_html, prop):
    m = re.search(r'<meta[^>]+(?:property|name)="%s"[^>]+content="([^"]*)"' % re.escape(prop), soup_html)
    return m.group(1) if m else ""

rows = []
for i, (case, outlet, byline, date, headline, url, note) in enumerate(ITEMS, 1):
    status, words, path, pub, auth = "", 0, "", "", ""
    try:
        r = requests.get(url, headers=UA, timeout=30)
        status = str(r.status_code)
        if r.ok:
            text = extract(r.text)
            pub = meta(r.text, "article:published_time") or meta(r.text, "datePublished")
            auth = meta(r.text, "author") or meta(r.text, "article:author")
            words = len(text.split())
            slug = re.sub(r"[^a-z0-9]+", "-", headline.lower()).strip("-")[:60]
            fname = f"{case.lower()}_{outlet.split()[0].lower()}_{date}_{slug}.txt"
            path = str(OUT / fname)
            header = (f"CASE: {case}\nOUTLET: {outlet}\nBYLINE (recorded): {byline}\nBYLINE (page meta): {auth}\n"
                      f"DATE (recorded): {date}\nDATE (page meta): {pub}\nHEADLINE: {headline}\nURL: {url}\n"
                      f"RETRIEVED: {datetime.datetime.now().isoformat(timespec='seconds')}\nNOTE: {note}\nWORDS: {words}\n"
                      + "-"*72 + "\n\n")
            pathlib.Path(path).write_text(header + text, encoding="utf-8")
    except Exception as e:
        status = f"ERROR {e}"
    rows.append([i, case, outlet, byline, date, headline, url, status, words, pathlib.Path(path).name if path else "", pub, note])
    print(f"{i:2d} {status:>4} {words:5d}w  {outlet} | {headline[:60]}")
    time.sleep(2.5)

with open(LOG, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id","case","outlet","byline","date","headline","url","http_status","words","fulltext_file","page_published_meta","note"]); w.writerows(rows)
print("log:", LOG)
