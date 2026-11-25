#!/usr/bin/env python3
"""Apply the CARIN dictionary to the article texts and write one row per item.

Usage:
    python scripts/carin_dictionary.py                       # reads data/fulltext/*.txt
    python scripts/carin_dictionary.py --texts some/folder --out data/output/carin_dictionary.csv
    python scripts/carin_dictionary.py --validate human_codes.csv

This is a secondary measure. The human codes in the workbook are the data of record. The
dictionary is reported only after --validate shows acceptable precision, recall and F1 against
those codes. It uses the Python standard library only and no AI system.

Header handling: if a file opens with "key: value" lines followed by a blank line, that block
is treated as the item header and is not searched.
"""
import argparse
import csv
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRITERIA = ["control", "attitude", "reciprocity", "identity", "need"]


def compile_term(term):
    """'fraud*' -> word-initial match with any ending; phrases allow any whitespace."""
    words = term.strip().split()
    parts = []
    for w in words:
        if w.endswith("*"):
            parts.append(re.escape(w[:-1]) + r"[\w'-]*")
        else:
            parts.append(re.escape(w))
    return re.compile(r"(?<![\w-])" + r"\s+".join(parts) + r"(?![\w-])", re.IGNORECASE)


def load_dictionary(path):
    raw = json.load(open(path, encoding="utf-8"))
    return {c: {k: [(t, compile_term(t)) for t in v] for k, v in raw[c].items()} for c in CRITERIA}


def body_of(text):
    lines = text.splitlines()
    i = 0
    while i < len(lines) and re.match(r"^[A-Za-z][A-Za-z _/-]{0,40}:\s", lines[i]):
        i += 1
    if 0 < i < len(lines) and lines[i].strip() == "":
        return "\n".join(lines[i + 1:])
    return text


def score(text, dic):
    row = {}
    for c in CRITERIA:
        counts, hits = {}, []
        for kind, terms in dic[c].items():
            n = 0
            for term, rx in terms:
                k = len(rx.findall(text))
                if k:
                    n += k
                    hits.append(f"{term}={k}")
            counts[kind] = n
        fav, unf = counts.get("favourable", 0), counts.get("unfavourable", 0)
        row[f"{c}_present"] = "yes" if sum(counts.values()) > 0 else "no"
        row[f"{c}_favourable_n"] = fav
        row[f"{c}_unfavourable_n"] = unf
        if "markers" in counts:
            row[f"{c}_markers_n"] = counts["markers"]
        row[f"{c}_direction"] = ("" if fav + unf == 0 else "favourable" if fav > unf
                                 else "unfavourable" if unf > fav else "mixed")
        row[f"{c}_terms"] = "; ".join(hits)
    return row


def validate(dict_rows, human_csv):
    """human_csv needs a 'file' or 'item_id' column and carin_<criterion>_present columns."""
    human = list(csv.DictReader(open(human_csv, encoding="utf-8-sig")))
    key = "file" if "file" in human[0] else "item_id"
    auto = {r[key if key in r else "file"]: r for r in dict_rows}
    print(f"{'criterion':12} {'n':>4} {'precision':>9} {'recall':>7} {'F1':>5}")
    for c in CRITERIA:
        tp = fp = fn = n = 0
        for h in human:
            a = auto.get(h[key])
            hv = h.get(f"carin_{c}_present", "").strip().lower()
            if a is None or hv not in ("yes", "no"):
                continue
            n += 1
            av = a[f"{c}_present"]
            tp += av == "yes" and hv == "yes"
            fp += av == "yes" and hv == "no"
            fn += av == "no" and hv == "yes"
        p = tp / (tp + fp) if tp + fp else float("nan")
        r = tp / (tp + fn) if tp + fn else float("nan")
        f1 = 2 * p * r / (p + r) if p + r else float("nan")
        print(f"{c:12} {n:>4} {p:>9.2f} {r:>7.2f} {f1:>5.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--texts", default=os.path.join(ROOT, "data", "fulltext"))
    ap.add_argument("--dictionary", default=os.path.join(ROOT, "dictionaries", "carin_en_us.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "output", "carin_dictionary.csv"))
    ap.add_argument("--validate", help="CSV of human codes to compare against")
    a = ap.parse_args()

    dic = load_dictionary(a.dictionary)
    rows = []
    for path in sorted(glob.glob(os.path.join(a.texts, "*.txt"))):
        text = body_of(open(path, encoding="utf-8", errors="replace").read())
        row = {"file": os.path.basename(path), "words_searched": len(text.split())}
        row.update(score(text, dic))
        rows.append(row)
    if not rows:
        raise SystemExit(f"no .txt files found in {a.texts}")
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {a.out}: {len(rows)} items")
    if a.validate:
        validate(rows, a.validate)
