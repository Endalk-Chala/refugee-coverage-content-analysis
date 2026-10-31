# Refugee Coverage: A Comparative Content Analysis

**How U.S. national, wire, partisan and Minnesota news outlets covered two refugee
policy cases, 2025 to 2026: the Afrikaner resettlement program and Operation PARRIS**

Endalkachew H. Chala, PhD
Community Fellow, Center for an Informed Public, University of Washington

Research infrastructure, version 0.2, 31 October 2026.

---

## Research question

The study asks whether, and how, news coverage of the two cases differed in sourcing,
individualisation, attribution of credibility and the framing of refugee status, across
four outlet tiers. The design is comparative: the same codebook is applied to both cases,
coding is blind to the hypotheses where the instrument allows it, and the analysis reports
cross-tabulations and effect sizes before any interpretive claim. The theoretical framing
that motivates the comparison is set out in the paper, not here.

## What is here

```
refugee-coverage-content-analysis/
├── README.md                     this file
├── arl_coding_workbook.xlsx      register, coding sheet, codebook, value lists
├── docs/
│   ├── codebook.md               the instrument in readable form
│   ├── search_protocol.md        windows, outlets, search strings, inclusion rules
│   └── retrieval.md              how the corpus was actually retrieved, and its limits
├── scripts/
│   ├── reliability.py            Krippendorff's alpha, self-tested
│   ├── analysis.py               cross-tabs, effect sizes, logistic models
│   ├── build_workbook.py         regenerates the coding workbook from vars.py
│   ├── add_candidates.py         logs discovery-search hits to search_candidates.csv
│   ├── place_all.py              names and files saved article texts, strips boilerplate
│   ├── build_retrieval_log.py    regenerates retrieval_log.csv from file headers
│   └── fetch_fulltext.py         direct HTTP fetcher (works outside filtered networks)
├── vars.py                       the single source of truth for the instrument
└── data/
    ├── arl_candidate_corpus.xlsx first-pass candidate list with retrieval status
    ├── fulltext/                 retrieved article texts: local only, not redistributed
    └── output/
        ├── retrieval_log.csv     one row per retrieved item, with confirmed dates and word counts
        └── search_candidates.csv discovery hits by outlet and query, with status
```

The workbook is generated, not hand-built. If you change a variable, change it in
`vars.py` and rerun `scripts/build_workbook.py`. Editing the spreadsheet's headers
directly will work until the scripts stop finding the columns they expect.

## Corpus status

As of 31 October 2026 the corpus holds 42 full-text items (about 37,800 words) across MPR News, Sahan Journal,
Fox News, MSNBC, MinnPost, NPR and Reuters, all inside the recorded windows, with 44 further open-access candidates
logged and pending. The article texts are not in this repository; `docs/retrieval.md` explains how to rebuild them
from the logs.

## Getting started

```
pip install openpyxl pandas scipy statsmodels
python scripts/reliability.py --selftest        # confirms the alpha code
python scripts/build_workbook.py                # regenerate if you edit vars.py
```

Then work in this order: register every retrieved item, decide `in_sample` with a
reason for every exclusion, shuffle by `coding_order`, code, re-code the stability
subsample as round 2, run `reliability.py`, run `analysis.py`, and only then
select the discourse subsample.

## Three decisions this infrastructure leaves open

**Reliability.** The original design had two coders and Krippendorff's alpha
between them. Solo, that is gone, and the substitute should be chosen rather than
fallen into. Either recruit one coder for the reliability subsample alone, which
keeps the conventional standard and costs perhaps six hours of a graduate
student's time, or report intra-coder stability by re-coding 15 to 20 per cent of
the corpus at least two weeks later. The workbook supports both: `coder` and
`coding_round` are separate columns, and `reliability.py` compares either pair.
Reviewers at framing journals will ask, so answer it in the methods rather than
in a footnote.

**Instrument length.** Seventeen variables are marked core and six extended. At
15 to 20 minutes an item, the full instrument across 160 items is roughly 45
hours of coding. If that is not available, drop the extended set before shrinking
the corpus. A smaller sample coded consistently is defensible; a full sample
coded in a hurry is not.

**Statistical power.** `analysis.py` refuses to fit a logistic regression when
events per variable fall below ten, and on a realistic corpus of 140 items with
case, outlet category and genre as predictors it will refuse: that specification
needs seven parameters and yields about eight events per variable. This is worth
knowing now rather than in month four. Either collapse outlet category to two
levels and drop genre from the model, or plan to report cross-tabulations with
effect sizes and say plainly that the sample did not support a multivariate
model. The second is perfectly publishable and more honest than the first.

## What the numbers will and will not show

The corpus records what was published. It does not record what was not. An outlet
that never sent a reporter to a PARRIS family's home leaves no trace here, and
absence of that kind is a large part of what the paper is about. The content
analysis can show that Afrikaner coverage individualises and PARRIS coverage
aggregates; only the discourse analysis can show how a story gets written so that
aggregation seems natural. Keep the division of labour explicit, and resist the
pull to make the quantitative section carry the interpretive claim.

## Licence

Code (`scripts/`, `vars.py`) is released under the MIT Licence. Documentation, the codebook and the retrieval logs
are released under CC BY 4.0. Article texts are the copyright of their publishers and are not distributed.

## A note on the byline

The proposal draft carries "Independent Researcher; Community Fellow, Center for
an Informed Public, University of Washington." One affiliation, the Community
Fellow line alone, is what you have settled on elsewhere, and this infrastructure
uses it throughout.
