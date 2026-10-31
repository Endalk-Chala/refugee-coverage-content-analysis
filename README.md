# Refugee Coverage: A Comparative Content Analysis

**How U.S. national, wire, partisan and Minnesota news outlets covered two refugee
policy cases, 2025 to 2026: the Afrikaner resettlement program and Operation PARRIS**

Endalkachew H. Chala, PhD
Community Fellow, Center for an Informed Public, University of Washington

Research infrastructure, version 0.2, 31 October 2026. Work in progress; the corpus is
still being assembled and no results are reported here.

---

## Overview

This repository holds the research infrastructure for a comparative content analysis of
U.S. news coverage of two refugee policy episodes that unfolded within a year of each other:

- **The Afrikaner resettlement program.** In February 2025 an executive order directed the
  United States to prioritise white South Africans of Afrikaner descent for refugee
  admission, while most other refugee admissions remained suspended. The first group arrived
  in May 2025; the program was expanded in the months that followed.
- **Operation PARRIS.** In January 2026 the Department of Homeland Security announced
  Operation PARRIS (Post-Admission Refugee Reverification and Integrity Strengthening), a
  re-examination of roughly 5,600 refugees already admitted to the United States and living in
  Minnesota, accompanied by arrests, detentions and transfers out of state, followed by
  litigation.

The two cases involve the same legal category, refugee status, applied to different
populations under different circumstances. The study asks whether and how news coverage of
the two differed in sourcing, individualisation, attribution of credibility and the framing
of refugee status, and whether those differences vary by outlet tier.

## Design

- **Comparative content analysis** with a single codebook applied to both cases, followed
  by a discourse-analytic reading of a subsample.
- **Four outlet tiers**: national elite press, wire services, partisan outlets on both sides,
  and Minnesota outlets. The Minnesota tier is expected to be thin for the Afrikaner case,
  which was a national story; the imbalance is reported rather than corrected.
- **Sampling windows**, fixed before coding and recorded in `docs/search_protocol.md`:
  1 February to 31 December 2025 for the Afrikaner case, 1 December 2025 to 31 October 2026
  for PARRIS. Both run eleven months and open one month before the anchor event so that the
  run-up to each policy moment is captured on the same terms.
- **Inclusion** is by relevance: an item is included if it is about the group's resettlement
  or the policy acting on it, regardless of where the outlet is based.
- **Analysis** reports cross-tabulations and effect sizes first. A multivariate model is
  fitted only where events per variable permit it; `scripts/analysis.py` enforces that rule.
- **Reliability** is assessed either with a second coder on a subsample or by intra-coder
  stability on a re-coded subsample at least two weeks later; the workbook and
  `scripts/reliability.py` support both designs, and the choice is reported in the methods.

## What is here

```
refugee-coverage-content-analysis/
├── README.md                     this file
├── arl_coding_workbook.xlsx      register, coding sheet, codebook, value lists
├── docs/
│   ├── codebook.md               the coding instrument in readable form
│   ├── search_protocol.md        windows, outlets, search strings, inclusion rules
│   └── retrieval.md              how the corpus was retrieved, and the access limits met
├── scripts/
│   ├── reliability.py            Krippendorff's alpha, self-tested
│   ├── analysis.py               cross-tabulations, effect sizes, logistic models
│   ├── build_workbook.py         regenerates the coding workbook from vars.py
│   ├── add_candidates.py         logs discovery-search hits to search_candidates.csv
│   ├── place_all.py              names and files saved article texts, strips boilerplate
│   ├── build_retrieval_log.py    regenerates retrieval_log.csv from file headers
│   └── fetch_fulltext.py         direct HTTP fetcher for open-access outlets
├── vars.py                       the single source of truth for the instrument
└── data/
    ├── arl_candidate_corpus.xlsx first-pass candidate list with retrieval status
    ├── fulltext/                 retrieved article texts: held locally, not redistributed
    └── output/
        ├── retrieval_log.csv     one row per retrieved item, with confirmed dates and word counts
        └── search_candidates.csv discovery hits by outlet and query, with status
```

The coding workbook is generated from `vars.py`; changes to variables are made there and
the workbook rebuilt with `scripts/build_workbook.py`.

## Corpus status

As of 31 October 2026 the corpus holds 76 full-text items (about 67,700 words), 69 of them
within the recorded windows (36 Afrikaner, 33 PARRIS), from AP, Fox News, MPR News, NPR, MSNBC,
Sahan Journal, Reuters and MinnPost. Items from paywalled outlets (The Washington Post, Star
Tribune, The New York Times) and from outlets that block automated access (CNN, most of Reuters)
are to be retrieved through library databases; the candidate list identifies each by URL. `docs/retrieval.md` records the procedure and every limit encountered, so that the
corpus can be rebuilt and checked against the logged word counts.

Article texts are not distributed in this repository. They are the copyright of their
publishers; the retrieval log identifies every item by URL.

## Reproducing the pipeline

```
pip install openpyxl pandas scipy statsmodels
python scripts/reliability.py --selftest        # confirms the alpha implementation
python scripts/build_workbook.py                # regenerates the workbook from vars.py
python scripts/build_retrieval_log.py           # regenerates the retrieval log from data/fulltext/
```

The coding sequence is: register every retrieved item; decide `in_sample` with a recorded
reason for each exclusion; shuffle by `coding_order`; code; re-code the stability subsample as
round 2; run `reliability.py`; run `analysis.py`; select the discourse subsample last.

## Limits of the design

The corpus records what was published, not what was not. An outlet's decision not to cover
an episode leaves no trace in a content analysis, and such absences are part of what a
comparative study of this kind has to reckon with. The quantitative component can establish
differences in how the two cases were covered; the discourse-analytic component is needed to
show how particular framings are produced in the text. The two are kept distinct in the
analysis and in the reporting.

## Citation

Chala, E. H. (2026). *Refugee coverage: A comparative content analysis* (research
infrastructure, version 0.2) [Data set and code]. GitHub.
https://github.com/Endalk-Chala/refugee-coverage-content-analysis

A paper based on this material is in preparation. Please cite the published article when it
appears; until then, cite this repository.

## Licence

Code (`scripts/`, `vars.py`) is released under the MIT Licence. Documentation, the codebook
and the retrieval logs are released under CC BY 4.0. Article texts are the copyright of their
publishers and are not distributed.

## Contact

Endalkachew H. Chala · [endalk-chala.github.io](https://endalk-chala.github.io) ·
ORCID [0000-0001-6210-6706](https://orcid.org/0000-0001-6210-6706)
