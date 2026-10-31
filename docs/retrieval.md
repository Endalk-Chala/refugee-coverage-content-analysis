# Corpus retrieval

How the full-text corpus was built, so that it can be rebuilt. Companion to `search_protocol.md`, which sets the
windows, outlets and search strings; this file records what was actually done.

## Windows and scope (decision of 31 October 2026)

| Case | Window | Scope |
|---|---|---|
| Afrikaner | 1 Feb 2025 to 31 Dec 2025 | national; coded wherever it appears in the sampled outlets |
| PARRIS | 1 Dec 2025 to 31 Oct 2026 | Minnesota-anchored; national outlets coded where they cover it |

Both windows are 11 months and open one month before the anchor event. Inclusion is by relevance, not geography.

## Two retrieval routes

1. **Candidate list first.** `data/arl_candidate_corpus.xlsx` (sheet `Candidate_Corpus`) holds the items
   identified in the first search pass, by case, outlet and tier. Columns J to N record retrieval status.
2. **Site-restricted discovery.** Because several outlets' own search pages are recency-sorted and unreliable,
   a second pass ran domain-restricted queries (for example `site:apnews.com Afrikaner refugees`) and logged every
   hit to `data/output/search_candidates.csv` with the query that produced it. Sahan Journal's
   `tags/operation-parris/` archive was enumerated directly.

## Fetching

Articles were opened in a real browser and the article body saved as plain text by a small script that selects the
article container (`article`, `.entry-content`, `.article-body`, `[data-testid="ArticleBody"]`, falling back to
`main`) and keeps paragraphs longer than 30 characters. Page metadata (`article:published_time`, author) is written
into the file header so that recorded dates can be checked against the outlet's own timestamp.

`scripts/place_all.py` then names each saved file `<case>_<outlet>_<date>_<slug>.txt`, matching the URL against the
candidate workbook or the discovery list, prepends the recorded metadata, and strips outlet boilerplate (newsletter
prompts, app promos, video-transcript notices).

`scripts/build_retrieval_log.py` regenerates `data/output/retrieval_log.csv` from the file headers: one row per file
with recorded date, page-confirmed date, word count and window flag. Run it after any change to `data/fulltext/`.

## Access limits encountered

- **CNN** returns "Content Unavailable For Legal Reasons" to the browser used; CNN items must be pulled manually or
  from a licensed database.
- **Washington Post** and **Star Tribune** are paywalled; headlines were logged for completeness and the texts are
  to be pulled through a library database (Nexis Uni or ProQuest).
- **Reuters** blocks automated access after a handful of page loads ("Access is temporarily restricted"), on
  31 October 2026 and again the following morning; two Reuters items were retrieved and the remaining in-window
  items are marked for the library route.
- **MSNBC** URLs now redirect to `ms.now` (the outlet rebranded); both hosts are treated as one outlet.
- **NYT, AP (national-desk pieces not surfaced by search), Reuters remainder**: database route.

## Known deviations worth a line in the methods

- Sahan Journal's 21 January 2026 story changed headline after publication; both are in the file header.
- Two MPR items are short radio write-ups (148 and 258 words); the unit-of-analysis rule should say whether a
  minimum length applies.
- MSNBC's contributions are opinion columns; genre is coded, not filtered.
- National outlets name "Operation PARRIS" rarely even when covering the same arrests; the thinness of that cell
  is a finding about the story's geography, not a retrieval failure.

## Status at last update

Run `python scripts/build_retrieval_log.py` for current counts. At 31 October 2026 (second pass): 76 files, about
67,700 body words, of which 69 are in-window (36 Afrikaner, 33 PARRIS); by outlet, AP 18, Fox News 16, MPR News 12,
NPR 10, MSNBC 8, Sahan Journal 8, Reuters 2, MinnPost 2. Four MSNBC opinion pieces dated 2026 on the Afrikaner
program were retrieved before the window check and are held out of the coded sample. Still to obtain through
library databases: Washington Post (17 candidates), Star Tribune (10), CNN (12), Reuters (5 in-window), and the
New York Times.
