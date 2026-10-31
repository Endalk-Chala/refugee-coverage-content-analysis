import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

from vars import REGISTER, VARIABLES, ADMIN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/arl_coding_workbook.xlsx"
os.makedirs(ROOT, exist_ok=True)

BASE = Font(name="Arial", size=10)
HEAD = Font(name="Arial", size=10, bold=True, color="FFFFFF")
TITLE = Font(name="Arial", size=14, bold=True)
SUB = Font(name="Arial", size=10, italic=True, color="555555")
HFILL = PatternFill("solid", fgColor="3A3042")
REGFILL = PatternFill("solid", fgColor="5C5470")
BAND = PatternFill("solid", fgColor="F4F2F6")
INPUT = PatternFill("solid", fgColor="FFF9DB")
thin = Side(style="thin", color="D9D9D9")
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()

CORE = [v for v in VARIABLES if v["tier"] == "core"]
EXT = [v for v in VARIABLES if v["tier"] == "extended"]

REG_COLS = [n for n, _ in REGISTER]
VAR_COLS = [v["name"] for v in VARIABLES]
ADMIN_COLS = [n for n, _ in ADMIN]
CODING_COLS = ["item_id", "case", "outlet_category", "genre"] + VAR_COLS + ADMIN_COLS


def style(ws, ncols, nrows, widths=None, fill=HFILL):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = HEAD
        cell.fill = fill
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORD
    for r in range(2, nrows + 2):
        for c in range(1, ncols + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = BASE
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORD
            if r % 2 == 0:
                cell.fill = BAND
    ws.freeze_panes = ws.cell(row=2, column=1)
    ws.auto_filter.ref = f"A1:{get_column_letter(ncols)}{max(nrows + 1, 2)}"
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 34


# ------------------------------------------------------------------ README
ws = wb.active
ws.title = "README"
ws.column_dimensions["A"].width = 26
ws.column_dimensions["B"].width = 104
rows = [
    ("Asymmetrical Refugee Legitimation", None),
    ("Coding workbook, version 0.1. Solo-coded.", None),
    ("Author", "Endalkachew H. Chala, Community Fellow, Center for an Informed Public, University of Washington"),
    ("Built", "23 September 2026"),
    (None, None),
    ("The design in one line",
     "Explanatory sequential mixed methods: a manual content analysis of roughly 100 to 160 news "
     "items establishes the pattern, and a critical discourse analysis of 20 to 30 purposively "
     "selected texts explains how it is produced."),
    ("Order of work",
     "1. Retrieve and register every candidate item in 'register', with an archive capture taken at "
     "retrieval. 2. Decide in_sample there, with a reason for every exclusion. 3. Code in 'coding', "
     "one row per in-sample item. 4. Re-code the stability subsample as round 2. 5. Run "
     "scripts/reliability.py. 6. Run scripts/analysis.py. 7. Select the discourse subsample and mark "
     "it back in 'register'."),
    ("Two sheets, one join",
     "register holds what the item is; coding holds what you judged about it. They join on item_id. "
     "Keeping them apart means a coding decision can be revised without touching the provenance "
     "record, and the provenance record is what makes the corpus reproducible."),
    (None, None),
    ("Reliability without a second coder",
     "The proposal assumed two coders and Krippendorff's alpha between them. Solo, that is not "
     "available, and the substitute has to be chosen rather than defaulted into. Two workable "
     "routes: recruit one coder for the reliability subsample only, which keeps the conventional "
     "standard and costs perhaps six hours of somebody's time; or report intra-coder stability by "
     "re-coding 15 to 20 per cent of the corpus at least two weeks later. The workbook supports "
     "both: 'coder' and 'coding_round' are separate columns and the reliability script computes "
     "alpha across any two passes. Whichever you choose, say so in the methods, and say which "
     "variables it covers."),
    ("Which variables are load-bearing",
     "Seventeen variables are marked core in 'variable_meta' because the research questions need "
     "them. Six are extended. At roughly 15 to 20 minutes an item, the full instrument on 160 items is "
     "something like 45 hours of coding. If that is not available, drop the extended set before "
     "shrinking the corpus: a smaller sample with a complete instrument is defensible; a full "
     "sample coded inconsistently is not."),
    ("Wire services",
     "AP and Reuters copy is coded once, as its own item, and republications are registered with "
     "wire_origin and republication_of and excluded from the analytic sample. Counting a Reuters "
     "story four times because four outlets ran it would turn distribution into agreement."),
    ("The one rule that protects the argument",
     "Code the text, not the case. You already believe the two populations were treated unequally. "
     "That belief is the hypothesis, and the instrument only tests it if each item is coded on what "
     "it says. Code in mixed order rather than case by case; the register has a coding_order column "
     "for the shuffle."),
    (None, None),
    ("Counts", None),
]
r = 1
for a, b in rows:
    if a:
        ws.cell(row=r, column=1, value=a)
    if b:
        ws.cell(row=r, column=2, value=b)
    r += 1
ws["A1"].font = TITLE
ws["A2"].font = SUB
for rr in range(3, r):
    ws.cell(row=rr, column=1).font = Font(name="Arial", size=10, bold=True)
    ws.cell(row=rr, column=1).alignment = Alignment(vertical="top")
    ws.cell(row=rr, column=2).font = BASE
    ws.cell(row=rr, column=2).alignment = Alignment(vertical="top", wrap_text=True)

counts = [
    ("Items registered", "=COUNTA(register!A2:A2000)"),
    ("In sample", '=COUNTIF(register!O2:O2000,"yes")'),
    ("Afrikaner case, in sample", '=COUNTIFS(register!B2:B2000,"afrikaner",register!O2:O2000,"yes")'),
    ("PARRIS case, in sample", '=COUNTIFS(register!B2:B2000,"parris",register!O2:O2000,"yes")'),
    ("Marked for discourse analysis", '=COUNTIF(register!Q2:Q2000,"yes")'),
    ("Rows coded, round 1", '=COUNTIF(coding!%s2:%s2000,1)' % (
        get_column_letter(CODING_COLS.index("coding_round") + 1),
        get_column_letter(CODING_COLS.index("coding_round") + 1))),
    ("Rows coded, round 2", '=COUNTIF(coding!%s2:%s2000,2)' % (
        get_column_letter(CODING_COLS.index("coding_round") + 1),
        get_column_letter(CODING_COLS.index("coding_round") + 1))),
    ("Flagged for adjudication", '=COUNTIF(coding!%s2:%s2000,"yes")' % (
        get_column_letter(CODING_COLS.index("flag_adjudication") + 1),
        get_column_letter(CODING_COLS.index("flag_adjudication") + 1))),
]
for label, f in counts:
    ws.cell(row=r, column=1, value=label).font = BASE
    ws.cell(row=r, column=2, value=f).font = BASE
    r += 1
ws.cell(row=r + 1, column=1,
        value="Live formulas over rows 2 to 2000. They update as you add items.").font = SUB

# ------------------------------------------------------------------ register
ws = wb.create_sheet("register")
ws.append(REG_COLS + ["coding_order", "notes"])
style(ws, len(REG_COLS) + 2, 0, fill=REGFILL,
      widths=[11, 11, 22, 17, 11, 12, 52, 18, 40, 40, 13, 11, 12, 14, 10, 20, 12, 40, 13, 40])
for i, (n, d) in enumerate(REGISTER, start=1):
    if d:
        ws.cell(row=1, column=i).comment = Comment(d, "Codebook")
ws.cell(row=1, column=len(REG_COLS) + 1).comment = Comment(
    "A random number per item. Sort by it before coding so you do not code one case straight "
    "through, which is how a hypothesis becomes a habit.", "Codebook")

# ------------------------------------------------------------------ coding
ws = wb.create_sheet("coding")
ws.append(CODING_COLS)
w = [11, 11, 17, 11] + [17] * len(VAR_COLS) + [9, 9, 12, 9, 13, 44]
style(ws, len(CODING_COLS), 0, widths=w)
for v in VARIABLES:
    idx = CODING_COLS.index(v["name"]) + 1
    note = f"{v['question']}\n\nTier: {v['tier']}. Level: {v['lom']}.\n\n{v['rule']}"
    ws.cell(row=1, column=idx).comment = Comment(note[:2000], "Codebook")
for n, d in ADMIN:
    ws.cell(row=1, column=CODING_COLS.index(n) + 1).comment = Comment(d, "Codebook")

# ------------------------------------------------------------------ value_lists
vl = wb.create_sheet("value_lists")
col = 1
placement = {}
extra = {
    "case": ["afrikaner", "parris"],
    "outlet_category": ["national_elite", "wire", "partisan", "minnesota"],
    "genre": ["news", "analysis", "opinion", "editorial", "letter"],
    "in_sample": ["yes", "no"],
    "exclusion_reason": ["off_topic", "duplicate", "wire_reprint", "paywalled_unobtainable",
                         "not_original_reporting", "outside_window"],
    "cda_subsample": ["yes", "no"],
    "wire_origin": ["ap", "reuters", "none"],
    "coding_round": ["1", "2"],
    "flag_adjudication": ["yes", "no"],
}
lists = {}
for name, vals in extra.items():
    lists[name] = vals
for v in VARIABLES:
    if v["lom"] == "ratio" or not v["values"]:
        continue
    if v["name"] == "secondary_frame":
        vals = [c for c, _ in next(x for x in VARIABLES if x["name"] == "refugee_frame")["values"]] + ["none"]
    else:
        vals = [c for c, _ in v["values"]]
    lists[v["name"]] = vals

for name, vals in lists.items():
    L = get_column_letter(col)
    vl[f"{L}1"] = name
    vl[f"{L}1"].font = HEAD
    vl[f"{L}1"].fill = HFILL
    for i, val in enumerate(vals, start=2):
        c = vl[f"{L}{i}"]
        c.value = val
        c.font = BASE
    vl.column_dimensions[L].width = max(18, len(name) + 4)
    placement[name] = (L, len(vals))
    col += 1

cod = wb["coding"]
reg = wb["register"]
LAST = 2000
for name, (L, n) in placement.items():
    f1 = f"=value_lists!${L}$2:${L}${n + 1}"
    if name in CODING_COLS:
        idx = CODING_COLS.index(name) + 1
        dv = DataValidation(type="list", formula1=f1, allow_blank=True, showDropDown=False)
        cod.add_data_validation(dv)
        dv.add(f"{get_column_letter(idx)}2:{get_column_letter(idx)}{LAST}")
    if name in REG_COLS:
        idx = REG_COLS.index(name) + 1
        dv2 = DataValidation(type="list", formula1=f1, allow_blank=True, showDropDown=False)
        reg.add_data_validation(dv2)
        dv2.add(f"{get_column_letter(idx)}2:{get_column_letter(idx)}{LAST}")

for sheet, ncols in ((reg, len(REG_COLS) + 2), (cod, len(CODING_COLS))):
    for r_ in range(2, 30):
        for c_ in range(1, ncols + 1):
            cell = sheet.cell(row=r_, column=c_)
            cell.fill = INPUT
            cell.border = BORD
            cell.font = BASE

# ------------------------------------------------------------------ codebook
ws = wb.create_sheet("codebook")
ws.append(["variable", "tier", "level", "code", "label", "definition_or_rule"])
n = 0
for v in VARIABLES:
    ws.append([v["name"], v["tier"], v["lom"], "", v["question"], v["rule"]])
    n += 1
    for code, label in v["values"]:
        ws.append(["", "", "", code, label, ""])
        n += 1
style(ws, 6, n, widths=[26, 11, 11, 26, 52, 78])

# ------------------------------------------------------------------ variable_meta
ws = wb.create_sheet("variable_meta")
ws.append(["variable", "tier", "lom", "n_values", "used_in_reliability"])
for v in VARIABLES:
    ws.append([v["name"], v["tier"], v["lom"], len(v["values"]) or "", "yes"])
style(ws, 5, len(VARIABLES), widths=[28, 12, 12, 11, 20])
ws.cell(row=1, column=3).comment = Comment(
    "Level of measurement decides the distance function in Krippendorff's alpha. Getting this wrong "
    "changes the number: an ordinal variable treated as nominal reports a lower alpha than it "
    "deserves, because a one-step disagreement is scored the same as a four-step one.", "Codebook")
ws.cell(row=1, column=5).comment = Comment(
    "Set to no for any variable you decide not to report reliability on, and say why in the methods.",
    "Codebook")

# ------------------------------------------------------------------ reliability_log
ws = wb.create_sheet("reliability_log")
ws.append(["run_date", "subsample_n", "share_of_corpus", "comparison",
           "variables_below_0_667", "variables_below_0_800", "action_taken", "notes"])
style(ws, 8, 0, widths=[12, 14, 16, 30, 28, 28, 40, 60])
ws.cell(row=1, column=4).comment = Comment(
    "For example 'EC round 1 vs EC round 2' for stability, or 'EC vs second coder' if one is added.",
    "Codebook")
ws.cell(row=1, column=7).comment = Comment(
    "What you changed. A failed variable is usually a definition problem, not a coder problem: "
    "rewrite the rule, re-code the subsample, log both runs. Never report only the second run.",
    "Codebook")

wb.save(OUT)
print("saved", OUT)
print("register cols:", len(REG_COLS) + 2, "| coding cols:", len(CODING_COLS),
      "| variables:", len(VARIABLES), f"(core {len(CORE)}, extended {len(EXT)})",
      "| codebook rows:", n)
