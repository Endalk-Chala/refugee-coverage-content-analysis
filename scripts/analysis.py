#!/usr/bin/env python3
"""
Asymmetrical Refugee Legitimation: descriptive and inferential analysis.

    pip install openpyxl pandas scipy statsmodels
    python analysis.py ../arl_coding_workbook.xlsx
    python analysis.py ../arl_coding_workbook.xlsx --out ../output

Produces, for each core variable:
  - a case-by-value cross-tabulation with row percentages
  - a chi-square test where expected counts permit one, Fisher's exact for 2x2
  - Cramer's V as the effect size, with the small-sample correction
  - for ordinal variables, a Mann-Whitney U and a rank-biserial correlation

Then two logistic regressions, run only if the events-per-variable rule allows:
  - P(refugee_frame is deserving) ~ case + outlet_category + genre
  - P(official_claim_treatment >= 2) ~ case + outlet_category + genre

The script refuses to fit a model that the sample cannot support, and says so,
rather than producing coefficients that look like findings.
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

ALPHA = 0.05
EPV_MIN = 10          # events per variable, the conventional floor for logistic regression
SMALL_CELL = 5


def load(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)

    def sheet(name):
        ws = wb[name]
        head = [c.value for c in ws[1]]
        rows = [dict(zip(head, r)) for r in ws.iter_rows(min_row=2, values_only=True) if r and r[0]]
        return pd.DataFrame(rows)

    reg, cod = sheet("register"), sheet("coding")
    meta = sheet("variable_meta")
    if reg.empty or cod.empty:
        sys.exit("The register or coding sheet is empty. Nothing to analyse yet.")
    reg = reg[reg["in_sample"].astype(str).str.lower() == "yes"]
    cod = cod[cod.get("coding_round", 1).astype(str).isin(["1", "1.0"])]
    df = cod.merge(reg[["item_id", "outlet", "pub_date", "wire_origin"]],
                   on="item_id", how="inner", suffixes=("", "_reg"))
    return df, meta


def cramers_v(table):
    chi2 = stats.chi2_contingency(table, correction=False)[0]
    n = table.values.sum()
    r, k = table.shape
    phi2 = chi2 / n
    # Bergsma's bias correction, which matters at the sample sizes here
    phi2c = max(0.0, phi2 - (k - 1) * (r - 1) / (n - 1))
    rc = r - (r - 1) ** 2 / (n - 1)
    kc = k - (k - 1) ** 2 / (n - 1)
    denom = min(kc - 1, rc - 1)
    return np.sqrt(phi2c / denom) if denom > 0 else np.nan


def crosstab_block(df, var, lom, out):
    sub = df[["case", var]].dropna()
    if sub.empty or sub[var].nunique() < 2 or sub["case"].nunique() < 2:
        print(f"\n{var}: not enough variation to cross-tabulate.")
        return None
    tab = pd.crosstab(sub["case"], sub[var])
    if lom in ("ordinal", "interval", "ratio"):
        # codes are stored as text, so sort the columns numerically rather than
        # alphabetically, which would print -1 before -2
        try:
            tab = tab[sorted(tab.columns, key=lambda c: float(c))]
        except (TypeError, ValueError):
            pass
    pct = (tab.T / tab.sum(axis=1)).T * 100
    print(f"\n{'=' * 70}\n{var}  ({lom})\n{'=' * 70}")
    print(tab.to_string())
    print("\nrow %:")
    print(pct.round(1).to_string())

    exp = stats.chi2_contingency(tab, correction=False)[3]
    small = (exp < SMALL_CELL).sum()
    if tab.shape == (2, 2):
        odds, p = stats.fisher_exact(tab.values)
        print(f"\nFisher's exact p = {p:.4f}, odds ratio = {odds:.3f}")
    elif small == 0:
        chi2, p, dof, _ = stats.chi2_contingency(tab, correction=False)
        print(f"\nchi2({dof}) = {chi2:.3f}, p = {p:.4f}")
    else:
        chi2, p, dof, _ = stats.chi2_contingency(tab, correction=False)
        print(f"\nchi2({dof}) = {chi2:.3f}, p = {p:.4f}  "
              f"[{small} of {exp.size} expected counts below {SMALL_CELL}: "
              f"treat as descriptive, or collapse categories and say you did]")
    v = cramers_v(tab)
    print(f"Cramer's V (bias-corrected) = {v:.3f}")

    if lom == "ordinal":
        try:
            groups = [pd.to_numeric(g[var], errors="coerce").dropna()
                      for _, g in sub.groupby("case")]
            if len(groups) == 2 and all(len(g) > 0 for g in groups):
                u, p = stats.mannwhitneyu(groups[0], groups[1], alternative="two-sided")
                n1, n2 = len(groups[0]), len(groups[1])
                rbc = 1 - (2 * u) / (n1 * n2)
                print(f"Mann-Whitney U = {u:.1f}, p = {p:.4f}, "
                      f"rank-biserial r = {rbc:.3f}")
                print(f"medians: " + ", ".join(
                    f"{c} = {g.median():.1f}" for (c, _), g in zip(sub.groupby('case'), groups)))
        except Exception as e:
            print(f"  ordinal test skipped: {e}")

    tab.to_csv(os.path.join(out, f"crosstab_{var}.csv"))
    return tab


def logit(df, name, outcome_series, out):
    try:
        import statsmodels.formula.api as smf
    except ImportError:
        print(f"\n{name}: statsmodels is not installed, so no model was fitted.")
        print("  pip install statsmodels, then rerun. The cross-tabulations above stand on")
        print("  their own and are what most of the argument rests on in any case.")
        return

    d = df.copy()
    d["_y"] = outcome_series
    d = d[["_y", "case", "outlet_category", "genre"]].dropna()
    if d.empty or d["_y"].nunique() < 2:
        print(f"\n{name}: outcome has no variation. Not fitted.")
        return
    events = int(min(d["_y"].sum(), len(d) - d["_y"].sum()))
    # parameters = 1 intercept + (levels-1) for each predictor
    k = 1 + sum(max(d[c].nunique() - 1, 0) for c in ("case", "outlet_category", "genre"))
    epv = events / k if k else 0
    print(f"\n{'=' * 70}\n{name}\n{'=' * 70}")
    print(f"n = {len(d)}, minority events = {events}, parameters = {k}, EPV = {epv:.1f}")
    if epv < EPV_MIN:
        print(f"NOT FITTED. Events per variable is below {EPV_MIN}, so the coefficients would be")
        print("unstable and the standard errors optimistic. Report the cross-tabulations instead,")
        print("or collapse outlet_category and genre and rerun. Saying 'the sample did not support")
        print("a model' is a finding; fitting one anyway is not.")
        return
    try:
        m = smf.logit("_y ~ C(case) + C(outlet_category) + C(genre)", data=d).fit(disp=False)
        print(m.summary2().as_text())
        odds = pd.DataFrame({"OR": np.exp(m.params),
                             "2.5%": np.exp(m.conf_int()[0]),
                             "97.5%": np.exp(m.conf_int()[1])})
        print("\nodds ratios:")
        print(odds.round(3).to_string())
        odds.to_csv(os.path.join(out, f"logit_{name.replace(' ', '_')}.csv"))
    except Exception as e:
        print(f"model failed to converge: {e}")
        print("Usually separation: one predictor level perfectly predicts the outcome.")


def main(path, out):
    os.makedirs(out, exist_ok=True)
    df, meta = load(path)
    print(f"ARL analysis\n{'=' * 70}")
    print(f"items analysed: {len(df)}")
    if "case" in df:
        print(df["case"].value_counts().to_string())
    if "outlet_category" in df:
        print("\nby outlet category:")
        print(pd.crosstab(df["outlet_category"], df["case"]).to_string())
    if "genre" in df:
        print("\nby genre:")
        print(pd.crosstab(df["genre"], df["case"]).to_string())

    core = meta[(meta["tier"] == "core") & (meta["variable"].isin(df.columns))]
    for _, row in core.iterrows():
        crosstab_block(df, row["variable"], row["lom"], out)

    if "refugee_frame" in df:
        y = df["refugee_frame"].map(
            lambda v: 1 if v in ("victim_deserving", "contributor_neighbour")
            else (0 if pd.notna(v) and v != "" else np.nan))
        logit(df, "deserving frame", y, out)
    if "official_claim_treatment" in df:
        y = pd.to_numeric(df["official_claim_treatment"], errors="coerce").map(
            lambda v: np.nan if pd.isna(v) else (1 if v >= 2 else 0))
        logit(df, "official claim tested", y, out)

    print(f"\ncross-tabs and model output written to {out}")
    print("\nA reminder before any of this goes in a draft: these are counts of what was")
    print("published, not of what happened. An outlet that ran no story about a family is")
    print("not recorded here as having decided not to, and absence is a large part of the")
    print("argument. Say so where you report the numbers.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "output"
    main(sys.argv[1], o)
