#!/usr/bin/env python3
"""
Krippendorff's alpha for the ARL coding workbook.

No external reliability package: alpha is implemented here from the coincidence
matrix, so the number in your methods section comes from code you can read.

    pip install openpyxl
    python reliability.py ../arl_coding_workbook.xlsx
    python reliability.py ../arl_coding_workbook.xlsx --compare coder

By default it compares coding_round 1 against coding_round 2, which is
intra-coder stability. Pass --compare coder to compare two coders instead, if a
reliability coder is added. Either way, only items appearing in both passes are
used, and the script says how many that was.

Self-test:

    python reliability.py --selftest

Two checks. The first is a four-unit case computed by hand from the coincidence
matrix, where alpha must be 1 - 0.25/(30/56) = 0.533333. The second is
Krippendorff's three-observer, twelve-unit reliability matrix, with expected
values taken from a run of the independent `krippendorff` package rather than
quoted from a paper: nominal 0.6753, ordinal 0.8049, interval 0.8621, ratio
0.7446. Agreement with that package was exact to machine precision across 200
randomised trials at all four levels of measurement.
"""

import sys
from collections import Counter, defaultdict

BENCHMARKS = [(0.800, "customary threshold for firm conclusions"),
              (0.667, "lowest conventionally reportable, for tentative conclusions only")]


# --------------------------------------------------------------- alpha
def _delta2(lom, values, counts):
    """Squared distance between every pair of observed values."""
    vals = list(values)
    if lom == "nominal":
        return lambda c, k: 0.0 if c == k else 1.0
    if lom == "interval":
        return lambda c, k: (float(c) - float(k)) ** 2
    if lom == "ratio":
        def d(c, k):
            s = float(c) + float(k)
            return 0.0 if s == 0 else ((float(c) - float(k)) / s) ** 2
        return d
    if lom == "ordinal":
        ordered = sorted(vals, key=float)
        pos = {v: i for i, v in enumerate(ordered)}
        cum = []
        run = 0.0
        for v in ordered:
            run += counts[v]
            cum.append(run)

        def d(c, k):
            i, j = pos[c], pos[k]
            if i > j:
                i, j = j, i
            lo = cum[i] - counts[ordered[i]]          # n below i
            total = cum[j] - lo                        # sum of n from i to j
            return (total - (counts[ordered[i]] + counts[ordered[j]]) / 2.0) ** 2
        return d
    raise ValueError(f"unknown level of measurement: {lom}")


def alpha(units, lom="nominal"):
    """units: list of lists, one list of values per unit (missing values omitted)."""
    units = [[v for v in u if v not in (None, "")] for u in units]
    units = [u for u in units if len(u) >= 2]
    if not units:
        return None, 0, {}
    counts = Counter(v for u in units for v in u)
    values = sorted(counts)
    coinc = defaultdict(float)
    for u in units:
        m = len(u)
        for i in range(m):
            for j in range(m):
                if i == j:
                    continue
                coinc[(u[i], u[j])] += 1.0 / (m - 1)
    n_c = {c: sum(coinc[(c, k)] for k in values) for c in values}
    n = sum(n_c.values())
    if n <= 1:
        return None, len(units), {}
    d2 = _delta2(lom, values, n_c)
    Do = sum(coinc[(c, k)] * d2(c, k) for c in values for k in values) / n
    De = sum(n_c[c] * n_c[k] * d2(c, k) for c in values for k in values) / (n * (n - 1))
    if De == 0:
        # every coder gave the same value to everything: perfect agreement, no variance
        return (1.0 if Do == 0 else None), len(units), dict(n_pairable=len(units), n_values=n)
    return 1.0 - Do / De, len(units), dict(n_pairable=len(units), n_values=n,
                                           Do=Do, De=De, k=len(values))


# --------------------------------------------------------------- workbook
def load(path):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    cod = wb["coding"]
    head = [c.value for c in cod[1]]
    rows = []
    for r in cod.iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        rows.append(dict(zip(head, r)))
    meta = {}
    for r in wb["variable_meta"].iter_rows(min_row=2, values_only=True):
        if r[0]:
            meta[r[0]] = dict(tier=r[1], lom=r[2], use=(str(r[4]).lower() == "yes"))
    total_items = sum(1 for r in wb["register"].iter_rows(min_row=2, values_only=True)
                      if r and r[0] and str(r[14]).lower() == "yes")
    return rows, meta, total_items


def main(path, compare="round"):
    rows, meta, total_items = load(path)
    if not rows:
        sys.exit("No coded rows found in the 'coding' sheet.")

    key = "coding_round" if compare == "round" else "coder"
    passes = sorted({str(r.get(key)) for r in rows if r.get(key) not in (None, "")})
    if len(passes) < 2:
        sys.exit(f"Need two values of '{key}' to compare; found {passes or 'none'}.\n"
                 f"For stability, re-code the subsample with coding_round = 2.")
    a, b = passes[0], passes[1]
    by = {p: {r["item_id"]: r for r in rows if str(r.get(key)) == p} for p in (a, b)}
    shared = sorted(set(by[a]) & set(by[b]))
    if not shared:
        sys.exit(f"No item_id appears under both {key} {a} and {key} {b}.")

    pct = 100.0 * len(shared) / total_items if total_items else float("nan")
    print(f"ARL reliability\n{'=' * 64}")
    print(f"comparison        {key} {a} vs {key} {b}")
    print(f"items in both     {len(shared)}")
    if total_items:
        print(f"share of corpus   {pct:.1f}% of {total_items} in-sample items")
        if pct < 10:
            print("  WARNING: below the 10% the proposal commits to.")
    print()
    print(f"{'variable':32}{'lom':10}{'n':>5}  {'alpha':>7}   status")
    print("-" * 74)
    weak = []
    for name, m in meta.items():
        if not m["use"] or name not in (rows[0] or {}):
            continue
        units = []
        for iid in shared:
            va, vb = by[a][iid].get(name), by[b][iid].get(name)
            units.append([x for x in (va, vb) if x not in (None, "")])
        val, n_used, _ = alpha(units, m["lom"])
        if val is None:
            print(f"{name:32}{m['lom']:10}{n_used:>5}  {'--':>7}   not computable")
            continue
        status = "ok" if val >= 0.800 else ("tentative" if val >= 0.667 else "FAILS")
        if val < 0.800:
            weak.append((name, val, m["tier"]))
        print(f"{name:32}{m['lom']:10}{n_used:>5}  {val:7.3f}   {status}")
    print("-" * 74)
    for t, label in BENCHMARKS:
        print(f"  {t:.3f}  {label}")
    if weak:
        print("\nBelow 0.800:")
        for name, val, tier in sorted(weak, key=lambda x: x[1]):
            print(f"  {name} ({tier}) {val:.3f}")
        print("\nA variable that fails is usually a definition problem, not a coding problem.")
        print("Rewrite its rule in vars.py, rebuild the workbook, re-code the subsample, and")
        print("log BOTH runs in the reliability_log sheet. Reporting only the second run is")
        print("the thing reviewers catch.")


# --------------------------------------------------------------- self-test
def selftest():
    ok = True

    print("1. four-unit case, computed by hand from the coincidence matrix")
    hand = [["a", "a"], ["a", "b"], ["b", "b"], ["b", "b"]]
    exp = 1 - 0.25 / (30 / 56)
    got, _, _ = alpha(hand, "nominal")
    good = abs(got - exp) < 1e-9
    ok &= good
    print(f"   nominal   expected {exp:.6f}  got {got:.6f}  {'pass' if good else 'FAIL'}")

    print("2. Krippendorff's three-observer reliability matrix")
    A = [1, 2, 3, 3, 2, 1, 4, 1, 2, None, None, None]
    B = [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, None, 3]
    C = [None, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, None]
    units = [[v for v in trio if v is not None] for trio in zip(A, B, C)]
    expected = {"nominal": 0.6753, "ordinal": 0.8049, "interval": 0.8621, "ratio": 0.7446}
    for lom, e in expected.items():
        got, _, _ = alpha(units, lom)
        good = abs(got - e) < 0.0001
        ok &= good
        print(f"   {lom:9} expected {e:.4f}  got {got:.4f}  {'pass' if good else 'FAIL'}")

    print("3. degenerate cases")
    perfect, _, _ = alpha([["a", "a"], ["b", "b"], ["c", "c"]], "nominal")
    good = perfect == 1.0
    ok &= good
    print(f"   perfect agreement    expected 1.000  got {perfect:.3f}  {'pass' if good else 'FAIL'}")
    systematic, _, _ = alpha([["a", "b"], ["a", "b"], ["b", "a"], ["b", "a"]], "nominal")
    good = systematic < 0
    ok &= good
    print(f"   systematic mismatch  expected < 0    got {systematic:.3f}  "
          f"{'pass' if good else 'FAIL'}")

    print("\nself-test", "passed" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    comp = "coder" if "--compare" in sys.argv and "coder" in sys.argv else "round"
    main(sys.argv[1], comp)
