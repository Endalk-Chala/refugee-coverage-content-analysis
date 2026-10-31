# Search and sampling protocol

## Asymmetrical Refugee Legitimation

Version 0.1, 23 September 2026. Solo-coded.

The purpose of this document is that someone else could rebuild the corpus from
it and get the same items. Write down every decision at the moment you make it,
including the ones that felt obvious, because they will not be obvious in six
months when a reviewer asks why an item is missing.

---

## 1. Cases and windows

| Case | Anchor event | Window opens | Window closes |
|---|---|---|---|
| Afrikaner | Executive order designating White South African Afrikaners for humanitarian relief | 7 February 2025 | 31 December 2025 |
| PARRIS | DHS and USCIS announce Operation PARRIS, roughly 5,600 already-admitted refugees in Minnesota | 9 January 2026 | 31 July 2026 |

The proposal describes the PARRIS window as extendable pending legal
developments, and it should now be extended, for two reasons. The litigation is
the story: the Minnesota Attorney General backed a class action on 6 February
2026 and IRAP has been releasing records through FOIA, so a window that closes
in July captures the announcement and the arrests but not the contest over them.
And an asymmetry in window length between the two cases is a confound the paper
would have to defend.

Two defensible options. Match the lengths: run PARRIS 9 January to 30 September
2026, giving both cases just under nine months from their anchor event. Or run
both to a fixed census date and report it. Whichever you choose, fix it before
retrieval and do not revisit it once coding starts. Extending a window after
seeing results is the sort of thing that is invisible in a paper and fatal in a
replication.

**Decision recorded (31 October 2026):** Both windows run 11 months and open one month before the anchor event, so that the discursive run-up to each policy moment is captured on the same terms.

| Case | Window (final) |
|---|---|
| Afrikaner | 1 February 2025 to 31 December 2025 |
| PARRIS | 1 December 2025 to 31 October 2026 |

Rationale: the February 2025 week before the executive order carries the aid-freeze threats and the first "Afrikaner refugee" framing; December 2025 carries the Minnesota fraud-scandal coverage that supplied PARRIS's vetting-and-fraud framing (including the 31 December denaturalization story) and the 6 to 7 January launch reports that precede the formal 9 January announcement. The closing dates are fixed census dates: year-end for the Afrikaner case, 31 October 2026 for PARRIS, which takes in the status-termination phase reported in October. These windows are not to be revisited after coding begins.

**Scope rule recorded (31 October 2026):** The Afrikaner case is not Minnesota-bound. Afrikaner-case items are coded wherever they appear in the sampled outlets; the Minnesota tier is expected to be thin for that case, and the imbalance is reported rather than corrected. Inclusion for both cases is by relevance (the item is about the group's resettlement or the policy acting on it), not by geography.


---

## 2. Outlet categories

| Category | Outlets |
|---|---|
| National elite | The New York Times, The Washington Post, plus one more (the proposal leaves this open; CNN gives you a broadcast-origin digital outlet, the Wall Street Journal gives you an ideological contrast inside the elite tier) |
| Wire | Associated Press, Reuters |
| Partisan | Fox News, plus one contrasting outlet (MSNBC for broadcast symmetry, The Nation or Mother Jones for print) |
| Minnesota | Minnesota Public Radio, Star Tribune, Sahan Journal, MinnPost |

Two notes on the design. The Minnesota tier is only strictly parallel for the
PARRIS case, since the Afrikaner story has no Minnesota locus. Either accept the
asymmetry and say so, coding Minnesota coverage of the Afrikaner case wherever
it exists and reporting the thin cell honestly, or add a comparison local tier
for the Afrikaner case, which would be wherever Afrikaner arrivals were resettled
in numbers. The first is simpler and the imbalance is itself informative.

Sahan Journal is both a source and, arguably, a subject: it serves the East
African communities PARRIS targeted. That is a strength, since it gives you an
outlet embedded in the affected population, but it needs a sentence in the
methods acknowledging that its position differs in kind from the others'.

---

## 3. Search strings

Run these in a full-text database (Nexis Uni, ProQuest or Factiva through a
library) and again in each outlet's own site search, because database coverage
of digital-only outlets like Sahan Journal and MinnPost is unreliable. Record
both result counts in the retrieval log.

### Afrikaner case

```
(Afrikaner OR "South African" OR "white South African")
AND (refugee OR resettle* OR asylum OR "humanitarian relief" OR admission)
AND NOT (sport* OR cricket OR rugby OR wine)
```

Date limit 2025-02-07 to 2025-12-31.

### PARRIS case

```
("Operation PARRIS" OR PARRIS OR "reverification" OR "re-verification"
 OR "revetting" OR "re-vetting")
AND (refugee OR Minnesota OR USCIS OR "Homeland Security")
```

Date limit 2026-01-09 to your chosen close date. Run a second, broader string to
catch coverage that never names the operation:

```
(refugee OR refugees) AND (Minnesota OR Minneapolis OR "St. Paul" OR "Twin Cities")
AND (fraud OR investigat* OR arrest* OR detain* OR deport* OR "status review")
```

The second string will return a great deal of noise. That is expected, and the
exclusion counts it produces are part of what you report.

---

## 4. Inclusion and exclusion

**Include** an item when all four hold: it is original journalistic content from
a listed outlet; it is substantially about one of the two cases, meaning the case
is the subject rather than a passing reference; it falls inside the window; and
it is in English.

**Exclude**, with the reason recorded in the register:

| Reason | Meaning |
|---|---|
| `off_topic` | The case appears only in passing, below roughly three sentences or 10 per cent of the item. |
| `duplicate` | The same item retrieved twice, including print and web versions of one story. Keep the web version and note the duplicate. |
| `wire_reprint` | A republication of AP or Reuters copy. Register it, set `wire_origin` and `republication_of`, set `in_sample` to no. |
| `paywalled_unobtainable` | You could not obtain the full text. Record it, because the count of these belongs in the limitations. |
| `not_original_reporting` | Aggregation, a link roundup, a transcript with no reporting, a syndicated column. |
| `outside_window` | Returned by the search but outside the date limits. |

Letters to the editor are registered and coded as genre `letter` rather than
excluded, but decide now whether they enter the analytic sample. They are cheap
to code and they carry some of the sharpest legitimation language, but they are
not journalism and pooling them with news would muddy every outlet-level
comparison. The recommendation is to include and analyse separately.

---

## 5. Wire services

The proposal is right that wire copy needs separate treatment, and the reason is
worth stating precisely in the methods. If the Associated Press writes one story
about PARRIS and eleven outlets run it, coding all twelve would record eleven
independent editorial judgements that never happened. The distribution of a
single frame would appear as agreement about it.

So: code the wire original once, in the `wire` category. Register every
republication with `wire_origin` and `republication_of` pointing at the original,
and leave it out of the analytic sample. Then report the republication counts
separately, because how far a wire frame travelled is its own finding, and
arguably a more interesting one than any single outlet's choices.

Watch for the common case where an outlet runs wire copy with local reporting
added. That is original content: code it, and note in `coder_notes` that it has a
wire spine.

---

## 6. Retrieval log

Record these numbers as you go. They are what lets you report the corpus honestly
and they cannot be reconstructed afterwards.

| Step | Afrikaner | PARRIS |
|---|---|---|
| Database hits, string 1 | | |
| Database hits, string 2 | | |
| Site-search hits not in the database | | |
| Total unique items retrieved | | |
| Excluded: off topic | | |
| Excluded: duplicate | | |
| Excluded: wire reprint | | |
| Excluded: unobtainable | | |
| Excluded: not original reporting | | |
| **In analytic sample** | | |

If the in-sample total lands far outside the 100 to 160 the proposal anticipates,
that is information rather than a problem. A much smaller PARRIS corpus than
Afrikaner corpus, or the reverse, is a finding about attention, and it should be
reported before any of the framing results.

---

## 7. Archiving

Capture every retrieved item at the moment of retrieval, to the Wayback Machine
or perma.cc, and put the capture URL in `archive_url`. Items disappear, headlines
get rewritten silently, and a coding decision about a headline is unverifiable
once the headline has changed. This costs a few seconds per item and it is the
difference between a corpus that can be audited and one that cannot.

Keep the full text as well, as PDF or plain text, in `data/fulltext/` under the
`item_id`. Do not redistribute it: it is copyrighted. The archive URLs and the
codebook are what you publish.

---

## 8. Coding order

Assign each registered item a random number in `coding_order` and sort by it
before coding. Do not code the Afrikaner case first and the PARRIS case second.

You already believe the two populations were treated unequally, and coding case
by case would let that belief settle into a rhythm: by item forty of the PARRIS
block, `fraud_suspect` starts to feel like the default. Shuffling does not remove
the expectation, but it stops it from becoming a habit, and it makes the claim
that you coded the text rather than the case something you can actually defend.

For the same reason, code `official_claim_treatment` last within each item, after
reading the item twice. It is the most interpretive variable in the instrument
and the one carrying the most argumentative weight.

---

## 9. The discourse subsample

Select 20 to 30 texts after the content analysis, not before, and record the
rationale for each in `cda_rationale`. Four selection logics, used together:

- **Typical cases**: items sitting at the modal frame for their case and outlet
  tier, which show how the pattern is ordinarily produced.
- **Extreme cases**: the most strongly deserving-framed Afrikaner item and the
  most strongly suspicion-framed PARRIS item, which show the mechanism at full
  strength.
- **Hinge moments**: first coverage of each anchor event, and the first coverage
  after the litigation began, where terminology is still unsettled and you can
  watch official language become journalistic common sense.
- **Deviant cases**: items that run against their tier's pattern. These matter
  most. A Fox News item that individualises a PARRIS family, or a Times item that
  repeats an official fraud claim unchallenged, tells you what the pattern is
  made of by showing where it breaks.

Aim for rough balance across cases and tiers, but do not force it. Report the
selection logic in the methods, including how many of each type.
