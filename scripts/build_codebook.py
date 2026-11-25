#!/usr/bin/env python3
"""Write docs/codebook.md from vars.py.

Usage:  python scripts/build_codebook.py [--version "Version 0.2, 24 November 2026."]

vars.py is the source of truth for every variable. Edit there, then run this script and
scripts/build_workbook.py so the readable codebook and the workbook stay in step.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import vars as V  # noqa: E402

DEFAULT_VERSION = "Version 0.2, 24 November 2026."

INTRO = (
    "The unit of analysis is the news item. One row per in-sample item in the `coding` sheet, "
    "one row per retrieved item in `register`.\n\n"
    "A code you cannot apply from the text alone is a code that needs rewriting. Where you had "
    "to decide rather than read off, set `flag_adjudication` to yes and say why in `coder_notes`: "
    "those flags are where the instrument gets improved between the pilot and the full run."
)
RATIO_NOTE = ("Integer count. Leave blank rather than entering zero where the question does "
              "not apply to the item.")
LOM_TEXT = (
    "The `lom` column in `variable_meta` is not documentation, it is an input. Krippendorff's "
    "alpha uses a different distance function at each level, and an ordinal variable scored as "
    "nominal reports a lower alpha than it deserves, because a one-step disagreement between `1` "
    "and `2` is penalised exactly as heavily as a four-step disagreement between `-2` and `2`. On "
    "the tone variables that difference is large. Check the level before you report the number."
)
THRESHOLD_TEXT = (
    "Alpha of 0.800 is the customary threshold for firm conclusions; 0.667 is the lowest "
    "conventionally reportable, and only for tentative ones. A variable below threshold is almost "
    "always a definition problem rather than a coding problem: rewrite the rule, rebuild the "
    "workbook, re-code the subsample, and log both runs in `reliability_log`. Reporting only the "
    "second run is the thing reviewers catch."
)


def table(rows, head):
    out = [f"| {head[0]} | {head[1]} |", "|---|---|"]
    out += [f"| `{a}` | {b} |" for a, b in rows]
    return "\n".join(out)


def variable(v):
    parts = [f"### `{v['name']}`", f"**{v['question']}**",
             f"Level of measurement: {v['lom']}."]
    if v.get("rule"):
        parts.append(v["rule"])
    if v["values"]:
        parts.append(table(v["values"], ("code", "meaning")))
    elif v["lom"] == "ratio":
        parts.append(RATIO_NOTE)
    return "\n\n".join(parts)


def build(version):
    carin = [v for v in V.VARIABLES if v["name"].startswith("carin_")]
    core = [v for v in V.VARIABLES if v["tier"] == "core" and v not in carin]
    ext = [v for v in V.VARIABLES if v["tier"] == "extended"]
    n_core = len(core) + len(carin)
    if carin:
        count = (f"{n_core} core ({len(core)} general and {len(carin)} on the deservingness "
                 f"criteria) and {len(ext)} extended.")
    else:
        count = f"{n_core} core and {len(ext)} extended."
    doc = ["# Codebook", "## Asymmetrical Refugee Legitimation",
           f"{version} Generated from `vars.py`; edit there, not here.", INTRO, "---",
           "## Register fields",
           "Descriptive, not judgements. These establish what the item is and where it came from.",
           table(V.REGISTER, ("field", "meaning")),
           "Two further fields: `coding_order`, a random number used to shuffle the corpus before "
           "coding, and `notes`.",
           "---", "## Coded variables",
           f"{count} Core variables are required by the research questions. If time is short, "
           "drop the extended set before shrinking the corpus.",
           "## Core variables"]
    doc += [variable(v) for v in core]
    if carin:
        doc += ["## Deservingness criteria (CARIN)", V.CARIN_NOTE,
                "Three variables per criterion: present, direction and voice. The criteria follow "
                "van Oorschot (2000, 2006); their application to news content follows De Coninck "
                "and Steeman (2026)."]
        doc += [variable(v) for v in carin]
    doc += ["## Extended variables"]
    doc += [variable(v) for v in ext]
    doc += ["---", "## Administrative fields", table(V.ADMIN, ("field", "meaning")), "---",
            "## Levels of measurement and why they matter", LOM_TEXT,
            "## Thresholds", THRESHOLD_TEXT]
    if hasattr(V, "RELIABILITY_DESIGN"):
        doc += ["## Reliability design", V.RELIABILITY_DESIGN]
    return "\n\n".join(doc) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default=DEFAULT_VERSION)
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "codebook.md"))
    a = ap.parse_args()
    text = build(a.version)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", a.out, "|", len(V.VARIABLES), "variables")
