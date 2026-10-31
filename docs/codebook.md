# Codebook

## Asymmetrical Refugee Legitimation

Version 0.1, 23 September 2026. Generated from `vars.py`; edit there, not here.

The unit of analysis is the news item. One row per in-sample item in the `coding` sheet, one row per retrieved item in `register`.

A code you cannot apply from the text alone is a code that needs rewriting. Where you had to decide rather than read off, set `flag_adjudication` to yes and say why in `coder_notes`: those flags are where the instrument gets improved between the pilot and the full run.

---

## Register fields

Descriptive, not judgements. These establish what the item is and where it came from.

| field | meaning |
|---|---|
| `item_id` | ARL-0001 style. Assign once and never reuse. |
| `case` | afrikaner | parris. The paired contrast. |
| `outlet` | Exact masthead. |
| `outlet_category` | national_elite | wire | partisan | minnesota |
| `genre` | news | analysis | opinion | editorial | letter. Coded as distinct categories, not pooled. |
| `pub_date` | ISO date of first publication. |
| `headline` | As published. Record the web headline if it differs from print, and say which in notes. |
| `byline` | As published; 'staff' or 'wire' where there is none. |
| `url` | Live URL. |
| `archive_url` | Wayback or perma.cc capture. Do this at retrieval, not later. |
| `retrieval_date` | ISO date you captured it. |
| `word_count` | Body text only, excluding captions and furniture. |
| `wire_origin` | ap | reuters | none. Set for wire copy and for republications of it. |
| `republication_of` | item_id of the wire original, where this item is a reprint. |
| `in_sample` | yes | no. A no needs an exclusion_reason. |
| `exclusion_reason` | off_topic | duplicate | wire_reprint | paywalled_unobtainable | not_original_reporting | outside_window |
| `cda_subsample` | yes | no. The 20 to 30 texts for discourse analysis. |
| `cda_rationale` | Why this text was selected: typical case, extreme case, hinge moment, deviant case. |

Two further fields: `coding_order`, a random number used to shuffle the corpus before coding, and `notes`.

---

## Coded variables

17 core and 6 extended. Core variables are required by the research questions. If time is short, drop the extended set before shrinking the corpus.

## Core variables

### `problem_definition`

**What does the item present as the problem to be understood or solved?**

Level of measurement: nominal.

One code, the one the lead and the first three paragraphs establish. If the lead and the body disagree, code the lead and flag for adjudication.

| code | meaning |
|---|---|
| `humanitarian_protection` | People need protection and the question is whether they get it. |
| `racial_persecution_abroad` | A group is being persecuted in its home country on racial or ethnic grounds. |
| `immigration_fraud` | Claims or documents may be false and the system was deceived. |
| `national_security` | Admission creates a security or terrorism risk. |
| `administrative_integrity` | Vetting or record-keeping failed and must be corrected. |
| `legal_process` | The dispute is about law, procedure, jurisdiction or rights. |
| `political_conflict` | The story is a fight between political actors. |
| `economic_burden` | Cost to taxpayers, services or labour markets. |
| `community_harm` | Effects on the receiving community, including fear and disruption. |
| `other` | None of the above; describe in coder_notes. |

### `refugee_frame`

**How is the refugee population itself characterised?**

Level of measurement: nominal.

Code the dominant characterisation across the whole item. Use mixed only when two frames are given comparable weight, not when one is briefly acknowledged.

| code | meaning |
|---|---|
| `victim_deserving` | Persecuted, endangered, owed protection. |
| `threat_security` | A danger to safety or order. |
| `fraud_suspect` | Possibly dishonest; status possibly obtained improperly. |
| `economic_burden` | A cost. |
| `contributor_neighbour` | Working, contributing, embedded in local life. |
| `bureaucratic_case` | A file, a number, a caseload; no human characterisation. |
| `political_symbol` | Invoked to make a point about somebody else's politics. |
| `mixed` | Two frames carried with comparable weight. |
| `absent` | The population is not characterised at all. |

### `primary_source_type`

**Who is the first substantive source, by position in the text?**

Level of measurement: nominal.

First source quoted or paraphrased below the lead. Not the reporter, not a document cited only as background.

| code | meaning |
|---|---|
| `federal_official` | Named or unnamed federal agency or administration figure. |
| `state_local_official` | State or municipal official, including state attorneys general. |
| `law_enforcement` | Police, sheriff, federal agents speaking as enforcers. |
| `refugee_or_family` | A member of the affected population or their family. |
| `advocacy_ngo` | Resettlement agency, civil rights or refugee rights organisation. |
| `legal_counsel` | Lawyers for either side. |
| `academic_expert` | Researcher or analyst. |
| `community_leader` | Faith, ethnic association or business leader in the affected community. |
| `anonymous_official` | An official who is not named. |
| `documents` | Court filings, agency records, data releases. |
| `none` | No sourcing beyond the reporter. |

### `n_sources_total`

**How many distinct sources are quoted or paraphrased?**

Level of measurement: ratio.

Count distinct people and institutions, not mentions. Documents count as one source each.

Integer count. Leave blank rather than entering zero where the question does not apply to the item.

### `n_sources_official`

**Of those, how many are government sources?**

Level of measurement: ratio.

Federal, state, local and law enforcement combined.

Integer count. Leave blank rather than entering zero where the question does not apply to the item.

### `n_sources_refugee`

**Of those, how many are members of the affected population or their families?**

Level of measurement: ratio.

Community leaders count only if they are themselves from the population.

Integer count. Leave blank rather than entering zero where the question does not apply to the item.

### `attribution_mode`

**How is the central factual claim attributed?**

Level of measurement: nominal.

The claim the story turns on, not every claim in it.

| code | meaning |
|---|---|
| `named_on_record` | A named person or institution. |
| `anonymous_official` | An unnamed official. |
| `document_based` | A filing, record or dataset. |
| `unattributed_assertion` | Stated by the outlet with no attribution. |

### `individualisation`

**How far is any member of the population presented as a particular person?**

Level of measurement: ordinal.

Code the highest level reached anywhere in the item.

| code | meaning |
|---|---|
| `0` | None. The population appears only in aggregate. |
| `1` | Named, with no further detail. |
| `2` | Named with biography: occupation, history, circumstances. |
| `3` | Family narrative: relationships, home, children, daily life. |

### `refugee_voice`

**Does a member of the population speak?**

Level of measurement: ordinal.

An advocate speaking on their behalf is not their voice; code that under sources.

| code | meaning |
|---|---|
| `0` | Absent. |
| `1` | Paraphrased only. |
| `2` | Directly quoted, one or two sentences. |
| `3` | Extended testimony shaping the item's structure. |

### `historical_context`

**Is the situation placed in a history that explains it?**

Level of measurement: ordinal.

History of the persecution, the conflict, the admission programme or the policy. A date alone is not context.

| code | meaning |
|---|---|
| `0` | Absent. |
| `1` | Passing mention, a clause or a sentence. |
| `2` | Substantive: a paragraph or more that changes how the situation reads. |

### `official_claim_treatment`

**How does the item handle the central claim made by officials?**

Level of measurement: ordinal.

Leave blank where the item contains no official claim. This variable is the heart of the credibility argument, so code it last, after reading the whole item twice.

| code | meaning |
|---|---|
| `0` | Repeated without attribution or challenge. |
| `1` | Attributed but not tested. |
| `2` | Counter-sourced: someone else is given space to dispute it. |
| `3` | Independently verified or checked against evidence by the outlet itself. |

### `population_label_primary`

**What noun does the item mainly use for the population?**

Level of measurement: nominal.

Count uses in headline, lead and subheads first; the body breaks ties.

| code | meaning |
|---|---|
| `refugee` |  |
| `asylum_seeker` |  |
| `migrant` |  |
| `immigrant` |  |
| `alien` |  |
| `beneficiary` |  |
| `suspect_or_fraudster` |  |
| `national_or_ethnic_label` | Afrikaner, Somali, Hmong, South African and so on. |
| `other` |  |

### `official_terminology_adopted`

**Does the item use the government's own terms as its own?**

Level of measurement: nominal.

Unquoted, unattributed use of 'Operation PARRIS', 'reverification', 'integrity', 'persecuted minority' and the like in the outlet's own voice.

| code | meaning |
|---|---|
| `yes` | Used in the outlet's voice. |
| `quoted` | Used but marked as the government's term. |
| `no` | Not used, or replaced with the outlet's own wording. |

### `status_conditionality`

**How secure does the item make the population's legal status appear?**

Level of measurement: ordinal.

This is the post-admission question the paper turns on. Code what the text implies, not what the law says.

| code | meaning |
|---|---|
| `0` | Settled. Status is treated as a completed fact. |
| `1` | Implicitly conditional: hedged language, 'currently', 'for now'. |
| `2` | Explicitly conditional: status is described as subject to review. |
| `3` | Revocable: the item is about the possibility of removal or rescission. |

### `racial_language`

**How does explicit racial vocabulary appear?**

Level of measurement: ordinal.

Explicit only. The paper's claim is that race works through the other variables; this one exists to show how rarely it is named.

| code | meaning |
|---|---|
| `0` | Absent. |
| `1` | Descriptive: race or ethnicity named as a fact. |
| `2` | Contested: someone in the item alleges racial motivation and is quoted. |
| `3` | Central: the item's own frame is about racial differential treatment. |

### `tone_refugee`

**Overall valence toward the refugee population.**

Level of measurement: ordinal.

Toward the people, not the policy. Judge the item as a whole.

| code | meaning |
|---|---|
| `-2` | Strongly negative. |
| `-1` | Negative. |
| `0` | Neutral or balanced. |
| `1` | Positive. |
| `2` | Strongly positive. |

### `tone_policy`

**Overall valence toward the government action.**

Level of measurement: ordinal.

Coded separately and deliberately: an item can be warm toward people and warm toward the policy that reopens their status.

| code | meaning |
|---|---|
| `-2` | Strongly negative. |
| `-1` | Negative. |
| `0` | Neutral or balanced. |
| `1` | Positive. |
| `2` | Strongly positive. |

## Extended variables

### `secondary_frame`

**The next most prominent characterisation, if any.**

Level of measurement: nominal.

Same value list as refugee_frame. Leave blank where there is only one.

| code | meaning |
|---|---|
| `same_list_as_refugee_frame` | See refugee_frame. |
| `none` | No second frame. |

### `n_sources_advocacy`

**Of those, how many are advocacy organisations or legal counsel for the population?**

Level of measurement: ratio.

Integer count. Leave blank rather than entering zero where the question does not apply to the item.

### `official_claim_contradicted`

**Does the item state that an official claim is inaccurate?**

Level of measurement: nominal.

Separate from treatment: an outlet can counter-source without concluding anything.

| code | meaning |
|---|---|
| `yes` |  |
| `no` |  |
| `na` | No official claim present. |

### `numeric_claims_present`

**Does the item carry a statistic about the population or the programme?**

Level of measurement: nominal.

Counts, rates, costs, caseloads.

| code | meaning |
|---|---|
| `yes` |  |
| `no` |  |

### `numeric_claims_sourced`

**Is that statistic attributed to a nameable source?**

Level of measurement: nominal.

Leave blank where no numeric claim is present.

| code | meaning |
|---|---|
| `yes` |  |
| `no` |  |
| `mixed` | Some sourced, some not. |

### `legal_process_detail`

**Is the legal or administrative process explained?**

Level of measurement: ordinal.

What reverification or resettlement actually involves procedurally.

| code | meaning |
|---|---|
| `0` | Absent. |
| `1` | Mentioned. |
| `2` | Explained. |

---

## Administrative fields

| field | meaning |
|---|---|
| `coder` | Initials. Kept even for solo coding, because a reliability coder may be added. |
| `coding_round` | 1 or 2. Round 2 is the re-code of the stability subsample, at least two weeks later. |
| `coding_date` | ISO date. |
| `minutes_spent` | Optional, but it is the only way to know whether the instrument is too long. |
| `flag_adjudication` | yes | no. Anything you had to decide rather than read off. |
| `coder_notes` | Free text. The reason for a hard call, in a sentence. |

---

## Levels of measurement and why they matter

The `lom` column in `variable_meta` is not documentation, it is an input. Krippendorff's alpha uses a different distance function at each level, and an ordinal variable scored as nominal reports a lower alpha than it deserves, because a one-step disagreement between `1` and `2` is penalised exactly as heavily as a four-step disagreement between `-2` and `2`. On the tone variables that difference is large. Check the level before you report the number.

## Thresholds

Alpha of 0.800 is the customary threshold for firm conclusions; 0.667 is the lowest conventionally reportable, and only for tentative ones. A variable below threshold is almost always a definition problem rather than a coding problem: rewrite the rule, rebuild the workbook, re-code the subsample, and log both runs in `reliability_log`. Reporting only the second run is the thing reviewers catch.
