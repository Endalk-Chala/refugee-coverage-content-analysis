# Hypotheses and analysis plan

Version 0.1, 24 November 2026. Draft for the author's revision. Fixed before coding begins;
changes after that date are logged here with a reason.

## Design in one paragraph

Two refugee policy cases are compared with one codebook: the admission of white South Africans
(Afrikaners) under the February 2025 executive order, and Operation PARRIS, the re-examination of
already-admitted refugees in Minnesota announced in January 2026. Both populations hold or sought
the same legal status. The study asks on which grounds each population is judged deserving of
protection, in which direction, and by whom, using the five deservingness criteria (Control,
Attitude, Reciprocity, Identity, Need) set out by van Oorschot (2000, 2006) and applied to news
content by De Coninck and Steeman (2026).

## Where each comparison can be made

| Comparison | Items used | Why |
|---|---|---|
| Between cases | National elite, wire and partisan outlets, both cases | The same outlets covered both stories, so outlet is held constant. |
| Local against national | Operation PARRIS items only | Minnesota outlets barely covered the Afrikaner case, so a pooled comparison would confound outlet type with case. |

The Minnesota tier in the Afrikaner case is reported descriptively and is not used in a test.

## Hypotheses

Between cases (national outlets):

- **H1 (Control).** Control judgements are present in a larger share of PARRIS items than of
  Afrikaner items, and where present are more often unfavourable.
- **H2 (Identity).** Favourable Identity judgements are present in a larger share of Afrikaner
  items than of PARRIS items.
- **H3 (Voice).** In Afrikaner items, favourable judgements are voiced mainly by officials; in
  PARRIS items, unfavourable judgements are voiced mainly by officials.

Local against national (PARRIS items):

- **H4 (Proximity).** Minnesota outlets carry favourable Need and favourable Reciprocity
  judgements in a larger share of items than national outlets do.
- **H5 (Refugee voice).** Minnesota outlets more often give the judgement to a member of the
  affected population (`carin_*_voice` = refugee; `refugee_voice`; `n_sources_refugee`).

H1 and H2 follow from De Coninck and Steeman's finding that coverage of a population presented
as culturally close foregrounded Need and inclusive Identity while Control receded. H3 is this
study's own expectation and is labelled as such in the paper.

## Research questions

- **RQ1.** How is Need treated in each case: affirmed, questioned or both, and by whom?
- **RQ2.** Which criteria co-occur within items in each case?
- **RQ3.** How do the patterns in H1 to H3 differ across national elite, wire and partisan outlets?

## Measures

| Concept | Variables |
|---|---|
| Criterion present | `carin_<criterion>_present` |
| Direction | `carin_<criterion>_direction` |
| Who voices it | `carin_<criterion>_voice` |
| Sourcing | `n_sources_total`, `n_sources_official`, `n_sources_refugee`, `primary_source_type` |
| Individualisation and voice | `individualisation`, `refugee_voice` |
| Treatment of official claims | `official_claim_treatment` |
| Conditionality of status | `status_conditionality` |
| Explicit racial vocabulary | `racial_language` |

Only variables that reach the reliability threshold in the codebook carry a claim.

## Analysis

- Shares with 95 per cent confidence intervals, and odds ratios, for every comparison.
- Fisher's exact test where an expected cell count is below five; chi-square otherwise.
- One logistic model per criterion (present against absent) with case and outlet category as
  predictors, fitted only where events per variable permit, as `scripts/analysis.py` enforces.
- Items from one outlet are not independent. Every test is accompanied by an outlet-by-outlet
  table, and H4 and H5 are reported with and without Sahan Journal, whose relation to the
  affected communities differs in kind from the other outlets'.
- Wire reprints are excluded from tests; opinion and letters are analysed separately from news.
- The dictionary measure in `dictionaries/` is secondary. It is reported only after validation
  against the human codes (precision, recall and F1 per criterion).

## Scope of the claims

Two cases support claims about these two episodes of coverage. They are a test of the
deservingness and proximity arguments in one setting, and do not establish how local and national
news treat refugees in general.

## References

De Coninck, D., & Steeman, L.-L. (2026). Extending the deservingness framework to communication
sciences. *Journalism & Mass Communication Quarterly*. Advance online publication.
https://doi.org/10.1177/10776990261498399

van Oorschot, W. (2000). Who should get what, and why? On deservingness criteria and the
conditionality of solidarity among the public. *Policy & Politics, 28*(1), 33–48.

van Oorschot, W. (2006). Making the difference in social Europe: Deservingness perceptions among
citizens of European welfare states. *Journal of European Social Policy, 16*(1), 23–42.
