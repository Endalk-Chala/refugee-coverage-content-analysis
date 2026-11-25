# Asymmetrical Refugee Legitimation: variable definitions.
# tier: core = required by the research questions; extended = drop first if time runs short.
# lom: level of measurement, which decides the distance function in Krippendorff's alpha.

REGISTER = [
    ("item_id", "ARL-0001 style. Assign once and never reuse."),
    ("case", "afrikaner | parris. The paired contrast."),
    ("outlet", "Exact masthead."),
    ("outlet_category", "national_elite | wire | partisan | minnesota"),
    ("genre", "news | analysis | opinion | editorial | letter. Coded as distinct categories, not pooled."),
    ("pub_date", "ISO date of first publication."),
    ("headline", "As published. Record the web headline if it differs from print, and say which in notes."),
    ("byline", "As published; 'staff' or 'wire' where there is none."),
    ("url", "Live URL."),
    ("archive_url", "Wayback or perma.cc capture. Do this at retrieval, not later."),
    ("retrieval_date", "ISO date you captured it."),
    ("word_count", "Body text only, excluding captions and furniture."),
    ("wire_origin", "ap | reuters | none. Set for wire copy and for republications of it."),
    ("republication_of", "item_id of the wire original, where this item is a reprint."),
    ("in_sample", "yes | no. A no needs an exclusion_reason."),
    ("exclusion_reason", "off_topic | duplicate | wire_reprint | paywalled_unobtainable | not_original_reporting | outside_window"),
    ("cda_subsample", "yes | no. The 20 to 30 texts for discourse analysis."),
    ("cda_rationale", "Why this text was selected: typical case, extreme case, hinge moment, deviant case."),
]

# ---------------------------------------------------------------------------
# Deservingness criteria (CARIN): Control, Attitude, Reciprocity, Identity, Need.
# Added 24 November 2026 (codebook v0.2). The criteria follow van Oorschot (2000, 2006)
# and their use in news content analysis by De Coninck and Steeman (2026, Journalism &
# Mass Communication Quarterly). Three variables per criterion: whether it is present,
# which way it points, and who voices it.
CARIN_NOTE = (
    "Each criterion is a ground on which a group can be judged more or less deserving of "
    "protection. Code the criterion as present when the item says something that bears on "
    "that ground for the refugee population the item is about, whether in the outlet's own "
    "voice or in a quoted source's. A word on its own is not enough: 'legal' in 'legal "
    "challenge' is not a Control judgement. Direction is always coded from the standpoint of "
    "the population's claim to protection: favourable supports the claim, unfavourable "
    "undercuts it. Voice records who makes the judgement, so that an official's accusation "
    "reported by a journalist is not counted as the journalist's own."
)

_CARIN = [
    ("control", "Control",
     "Is the population presented as responsible for its own situation or for a breach of the rules?",
     "Favourable: not to blame, lawfully admitted, already vetted, followed the rules, fled for "
     "reasons outside their control. Unfavourable: fraud, misrepresentation, unlawful presence, "
     "improper admission, a need for re-vetting, criminality."),
    ("attitude", "Attitude",
     "Is the population presented as grateful, compliant and willing to fit in, or the reverse?",
     "Favourable: gratitude, respect for the law, cooperation with authorities, effort to learn "
     "English or to integrate. Unfavourable: ingratitude, refusal, hostility, defiance."),
    ("reciprocity", "Reciprocity",
     "Is the population presented as contributing in return, or as taking without giving?",
     "Favourable: work, skills, farming, business ownership, taxes paid, service to the community. "
     "Unfavourable: cost to taxpayers, reliance on benefits, misuse of public programmes."),
    ("identity", "Identity",
     "Is the population presented as culturally close to, or distant from, the receiving society?",
     "Favourable: shared values, language, faith or way of life; 'neighbours'; belonging to the "
     "community. Unfavourable: cultural distance, incompatibility, foreignness, failure to "
     "assimilate. Naming a group's race, ethnicity or religion as a fact is not by itself a "
     "judgement: code present only when the item uses it to mark closeness or distance."),
    ("need", "Need",
     "Is the population presented as facing persecution, danger or hardship that calls for protection?",
     "Favourable: persecution, violence, vulnerability or hardship treated as real. Unfavourable: "
     "the claim of persecution or danger is questioned, described as unsupported, or denied."),
]

def _carin_variables():
    out = []
    for key, label, question, guide in _CARIN:
        out.append(dict(
            name=f"carin_{key}_present", tier="core", lom="nominal",
            question=f"{label}: {question}",
            rule=guide + " Code yes if any such judgement appears anywhere in the item.",
            values=[("yes", "At least one judgement on this ground."),
                    ("no", "None.")]))
        out.append(dict(
            name=f"carin_{key}_direction", tier="core", lom="nominal",
            question=f"{label}: which way do the judgements point for the population's claim to protection?",
            rule="Leave blank where the criterion is absent. Use mixed only when favourable and "
                 "unfavourable judgements are given comparable weight, not when one is briefly "
                 "acknowledged.",
            values=[("favourable", "Supports the population's claim."),
                    ("unfavourable", "Undercuts the population's claim."),
                    ("mixed", "Both, with comparable weight.")]))
        out.append(dict(
            name=f"carin_{key}_voice", tier="core", lom="nominal",
            question=f"{label}: who makes the judgement?",
            rule="Leave blank where the criterion is absent. Code the voice that carries the "
                 "judgement coded under direction. Journalist means the outlet's own voice, with "
                 "no attribution. Use multiple only when two kinds of voice carry it equally.",
            values=[("official", "Government or law enforcement, at any level."),
                    ("journalist", "The outlet's own voice, unattributed."),
                    ("refugee", "A member of the affected population or their family."),
                    ("advocate_legal", "An advocacy organisation, lawyer or court filing for the population."),
                    ("other_source", "Any other quoted source, including experts and politicians out of office."),
                    ("multiple", "Two kinds of voice carry it equally.")]))
    return out

CARIN_VARIABLES = _carin_variables()

VARIABLES = [
    dict(name="problem_definition", tier="core", lom="nominal",
         question="What does the item present as the problem to be understood or solved?",
         rule="One code, the one the lead and the first three paragraphs establish. If the lead and "
              "the body disagree, code the lead and flag for adjudication.",
         values=[
             ("humanitarian_protection", "People need protection and the question is whether they get it."),
             ("racial_persecution_abroad", "A group is being persecuted in its home country on racial or ethnic grounds."),
             ("immigration_fraud", "Claims or documents may be false and the system was deceived."),
             ("national_security", "Admission creates a security or terrorism risk."),
             ("administrative_integrity", "Vetting or record-keeping failed and must be corrected."),
             ("legal_process", "The dispute is about law, procedure, jurisdiction or rights."),
             ("political_conflict", "The story is a fight between political actors."),
             ("economic_burden", "Cost to taxpayers, services or labour markets."),
             ("community_harm", "Effects on the receiving community, including fear and disruption."),
             ("other", "None of the above; describe in coder_notes."),
         ]),
    dict(name="refugee_frame", tier="core", lom="nominal",
         question="How is the refugee population itself characterised?",
         rule="Code the dominant characterisation across the whole item. Use mixed only when two "
              "frames are given comparable weight, not when one is briefly acknowledged.",
         values=[
             ("victim_deserving", "Persecuted, endangered, owed protection."),
             ("threat_security", "A danger to safety or order."),
             ("fraud_suspect", "Possibly dishonest; status possibly obtained improperly."),
             ("economic_burden", "A cost."),
             ("contributor_neighbour", "Working, contributing, embedded in local life."),
             ("bureaucratic_case", "A file, a number, a caseload; no human characterisation."),
             ("political_symbol", "Invoked to make a point about somebody else's politics."),
             ("mixed", "Two frames carried with comparable weight."),
             ("absent", "The population is not characterised at all."),
         ]),
    dict(name="secondary_frame", tier="extended", lom="nominal",
         question="The next most prominent characterisation, if any.",
         rule="Same value list as refugee_frame. Leave blank where there is only one.",
         values=[("same_list_as_refugee_frame", "See refugee_frame."), ("none", "No second frame.")]),
    dict(name="primary_source_type", tier="core", lom="nominal",
         question="Who is the first substantive source, by position in the text?",
         rule="First source quoted or paraphrased below the lead. Not the reporter, not a document "
              "cited only as background.",
         values=[
             ("federal_official", "Named or unnamed federal agency or administration figure."),
             ("state_local_official", "State or municipal official, including state attorneys general."),
             ("law_enforcement", "Police, sheriff, federal agents speaking as enforcers."),
             ("refugee_or_family", "A member of the affected population or their family."),
             ("advocacy_ngo", "Resettlement agency, civil rights or refugee rights organisation."),
             ("legal_counsel", "Lawyers for either side."),
             ("academic_expert", "Researcher or analyst."),
             ("community_leader", "Faith, ethnic association or business leader in the affected community."),
             ("anonymous_official", "An official who is not named."),
             ("documents", "Court filings, agency records, data releases."),
             ("none", "No sourcing beyond the reporter."),
         ]),
    dict(name="n_sources_total", tier="core", lom="ratio",
         question="How many distinct sources are quoted or paraphrased?",
         rule="Count distinct people and institutions, not mentions. Documents count as one source each.",
         values=[]),
    dict(name="n_sources_official", tier="core", lom="ratio",
         question="Of those, how many are government sources?",
         rule="Federal, state, local and law enforcement combined.", values=[]),
    dict(name="n_sources_refugee", tier="core", lom="ratio",
         question="Of those, how many are members of the affected population or their families?",
         rule="Community leaders count only if they are themselves from the population.", values=[]),
    dict(name="n_sources_advocacy", tier="extended", lom="ratio",
         question="Of those, how many are advocacy organisations or legal counsel for the population?",
         rule="", values=[]),
    dict(name="attribution_mode", tier="core", lom="nominal",
         question="How is the central factual claim attributed?",
         rule="The claim the story turns on, not every claim in it.",
         values=[
             ("named_on_record", "A named person or institution."),
             ("anonymous_official", "An unnamed official."),
             ("document_based", "A filing, record or dataset."),
             ("unattributed_assertion", "Stated by the outlet with no attribution."),
         ]),
    dict(name="individualisation", tier="core", lom="ordinal",
         question="How far is any member of the population presented as a particular person?",
         rule="Code the highest level reached anywhere in the item.",
         values=[("0", "None. The population appears only in aggregate."),
                 ("1", "Named, with no further detail."),
                 ("2", "Named with biography: occupation, history, circumstances."),
                 ("3", "Family narrative: relationships, home, children, daily life.")]),
    dict(name="refugee_voice", tier="core", lom="ordinal",
         question="Does a member of the population speak?",
         rule="An advocate speaking on their behalf is not their voice; code that under sources.",
         values=[("0", "Absent."), ("1", "Paraphrased only."),
                 ("2", "Directly quoted, one or two sentences."),
                 ("3", "Extended testimony shaping the item's structure.")]),
    dict(name="historical_context", tier="core", lom="ordinal",
         question="Is the situation placed in a history that explains it?",
         rule="History of the persecution, the conflict, the admission programme or the policy. "
              "A date alone is not context.",
         values=[("0", "Absent."), ("1", "Passing mention, a clause or a sentence."),
                 ("2", "Substantive: a paragraph or more that changes how the situation reads.")]),
    dict(name="official_claim_treatment", tier="core", lom="ordinal",
         question="How does the item handle the central claim made by officials?",
         rule="Leave blank where the item contains no official claim. This variable is the heart of "
              "the credibility argument, so code it last, after reading the whole item twice.",
         values=[("0", "Repeated without attribution or challenge."),
                 ("1", "Attributed but not tested."),
                 ("2", "Counter-sourced: someone else is given space to dispute it."),
                 ("3", "Independently verified or checked against evidence by the outlet itself.")]),
    dict(name="official_claim_contradicted", tier="extended", lom="nominal",
         question="Does the item state that an official claim is inaccurate?",
         rule="Separate from treatment: an outlet can counter-source without concluding anything.",
         values=[("yes", ""), ("no", ""), ("na", "No official claim present.")]),
    dict(name="population_label_primary", tier="core", lom="nominal",
         question="What noun does the item mainly use for the population?",
         rule="Count uses in headline, lead and subheads first; the body breaks ties.",
         values=[("refugee", ""), ("asylum_seeker", ""), ("migrant", ""), ("immigrant", ""),
                 ("alien", ""), ("beneficiary", ""), ("suspect_or_fraudster", ""),
                 ("national_or_ethnic_label", "Afrikaner, Somali, Hmong, South African and so on."),
                 ("other", "")]),
    dict(name="official_terminology_adopted", tier="core", lom="nominal",
         question="Does the item use the government's own terms as its own?",
         rule="Unquoted, unattributed use of 'Operation PARRIS', 'reverification', 'integrity', "
              "'persecuted minority' and the like in the outlet's own voice.",
         values=[("yes", "Used in the outlet's voice."),
                 ("quoted", "Used but marked as the government's term."),
                 ("no", "Not used, or replaced with the outlet's own wording.")]),
    dict(name="status_conditionality", tier="core", lom="ordinal",
         question="How secure does the item make the population's legal status appear?",
         rule="This is the post-admission question the paper turns on. Code what the text implies, "
              "not what the law says.",
         values=[("0", "Settled. Status is treated as a completed fact."),
                 ("1", "Implicitly conditional: hedged language, 'currently', 'for now'."),
                 ("2", "Explicitly conditional: status is described as subject to review."),
                 ("3", "Revocable: the item is about the possibility of removal or rescission.")]),
    dict(name="racial_language", tier="core", lom="ordinal",
         question="How does explicit racial vocabulary appear?",
         rule="Explicit only. The paper's claim is that race works through the other variables; this "
              "one exists to show how rarely it is named.",
         values=[("0", "Absent."), ("1", "Descriptive: race or ethnicity named as a fact."),
                 ("2", "Contested: someone in the item alleges racial motivation and is quoted."),
                 ("3", "Central: the item's own frame is about racial differential treatment.")]),
    *CARIN_VARIABLES,
    dict(name="tone_refugee", tier="extended", lom="ordinal",
         question="Overall valence toward the refugee population.",
         rule="Toward the people, not the policy. Judge the item as a whole. Moved to the extended "
              "set in v0.2: the five deservingness criteria now carry this judgement in a form that "
              "can be read off the text.",
         values=[("-2", "Strongly negative."), ("-1", "Negative."), ("0", "Neutral or balanced."),
                 ("1", "Positive."), ("2", "Strongly positive.")]),
    dict(name="tone_policy", tier="core", lom="ordinal",
         question="Overall valence toward the government action.",
         rule="Coded separately and deliberately: an item can be warm toward people and warm toward "
              "the policy that reopens their status.",
         values=[("-2", "Strongly negative."), ("-1", "Negative."), ("0", "Neutral or balanced."),
                 ("1", "Positive."), ("2", "Strongly positive.")]),
    dict(name="numeric_claims_present", tier="extended", lom="nominal",
         question="Does the item carry a statistic about the population or the programme?",
         rule="Counts, rates, costs, caseloads.", values=[("yes", ""), ("no", "")]),
    dict(name="numeric_claims_sourced", tier="extended", lom="nominal",
         question="Is that statistic attributed to a nameable source?",
         rule="Leave blank where no numeric claim is present.",
         values=[("yes", ""), ("no", ""), ("mixed", "Some sourced, some not.")]),
    dict(name="legal_process_detail", tier="extended", lom="ordinal",
         question="Is the legal or administrative process explained?",
         rule="What reverification or resettlement actually involves procedurally.",
         values=[("0", "Absent."), ("1", "Mentioned."), ("2", "Explained.")]),
]

ADMIN = [
    ("coder", "Initials. Kept even for solo coding, because a reliability coder may be added."),
    ("coding_round", "1 or 2. Round 2 is the re-code of the stability subsample, at least two weeks later."),
    ("coding_date", "ISO date."),
    ("minutes_spent", "Optional, but it is the only way to know whether the instrument is too long."),
    ("flag_adjudication", "yes | no. Anything you had to decide rather than read off."),
    ("coder_notes", "Free text. The reason for a hard call, in a sentence."),
]

# ---------------------------------------------------------------------------
# Reliability design (v0.2). Printed at the end of the codebook.
RELIABILITY_DESIGN = (
    "Two human coders, each working without sight of the other's codes or of any earlier "
    "coding. Training uses ten items that are not in the reliability sample; the codebook is "
    "revised once after training and then frozen. The reliability sample is a random draw, "
    "stratified by case and outlet category, of 30 per cent of the in-sample items or 50 items, "
    "whichever is larger. Krippendorff's alpha is reported for every variable used in a claim, "
    "at the level of measurement recorded in `variable_meta`, and every run is logged in "
    "`reliability_log`. Disagreements are resolved by discussion after the alpha is computed, "
    "and the resolved codes are the data of record for those items. If an automated or "
    "AI-assisted step is used at any point (relevance screening, a dictionary measure, an "
    "additional coder), the methods section names the tool, its purpose and its agreement with "
    "the human codes, as the AEJMC policy on the ethical use of AI requires."
)
