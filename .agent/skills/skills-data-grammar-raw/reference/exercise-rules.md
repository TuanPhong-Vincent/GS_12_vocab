# Content & Pedagogical Quality Rules for Grammar Exercises

This document establishes the editorial, pedagogical, and technical standards for generating grammar exercises in Global Success 10–12.

---

## 1. Strict Grammar Ceiling Rule

1. **Upper Bound Constraint**: Sentences, distractors, cues, and guided cloze passages must **never** introduce grammar structures taught in higher units or higher grades.
   - *Example*: In GS10 Unit 1 (Present Simple vs. Present Continuous), do **not** use passive voice, perfect participle clauses, or inverted conditionals.
2. **Prior Foundation Knowledge (GS6–GS9)**: Structures taught in lower secondary (basic tenses, simple modals, basic comparatives, basic relative pronouns, simple/compound sentences) are permitted as natural building blocks.
3. **Focus on the Target Grammar Point**: 80%+ of test items must directly assess the target grammar rule of the unit (e.g. differentiating between Past Simple and Past Continuous, choosing correct articles, active vs. passive causatives, etc.).

---

## 2. Vocabulary Utilization & Enrichment

1. **Deep Lexical Integration**: Sentences should naturally incorporate vocabulary words from `vocab.json` and `raw-vocabulary.md`.
2. **Naturalness Over Stuffing**: Never force 3 or 4 difficult vocabulary words into a single sentence if it makes the sentence sound stiff, robotic, or artificial. One or two well-placed target vocabulary items per question is optimal.
3. **Contextual Fidelity**: Vocabulary should be used in accurate thematic contexts aligned with the unit's overarching theme (e.g. Life Stories, Multicultural World, Green Living, Urbanisation).

---

## 3. Context Diversity & Realism

1. **Avoid Repetitive Protagonists**: Do not repeat the same person's name or scenario across multiple questions. Use diverse subjects:
   - Scientists, historians, artists, environmentalists, volunteers, young innovators, community leaders.
2. **Rich, Meaningful Scenarios**: Every question should tell a micro-story or convey an authentic real-world observation:
   - Historical breakthroughs, community initiatives, technological advancements, cultural festivals, wildlife conservation missions.
3. **No Duplicate Stems**: Ensure each question within an exercise tests a distinct sentence pattern (e.g., in past simple vs. continuous: initial *While*, medial *when*, parallel actions with *while*, state verbs vs. dynamic verbs, negative forms, interrogative forms).

---

## 4. Distractor Design & Plausibility

For Multiple Choice (`01_mcq.json`), Guided Cloze (`05_guided_cloze.json`), and Error Identification (`06_error_identification.json`):

1. **Plausible Distractors**: Distractors must represent common learner misconceptions, typical tense confusions, or near-miss morphological errors.
   - *Bad Distractor*: Obvious nonsense words or impossible English forms (e.g., *"was did"* or *"goed"*).
   - *Good Distractor*: An authentic confusion between Past Simple and Past Continuous (e.g., *"was working"* vs. *"worked"* vs. *"has worked"* vs. *"works"*).
2. **Length & Complexity Balance**: Distractors must be of comparable length and grammatical complexity to the correct answer. The correct answer must never stand out simply because it is noticeably longer or more detailed.
3. **Single Unambiguous Key**: Ensure there is strictly **one** grammatically and contextually correct option. Avoid ambiguous contexts where multiple tenses could be argued as correct.

---

## 5. Option Key Distribution Balancing

1. **Equal Probability across Positions**:
   - For 20 multiple choice questions (`01_mcq.json`), the correct answer positions (A, B, C, D) must be distributed evenly:
     - 5 questions with correct answer **A**
     - 5 questions with correct answer **B**
     - 5 questions with correct answer **C**
     - 5 questions with correct answer **D**
   - For Guided Cloze (`05_guided_cloze.json`), each 20-blank passage must maintain a 5/5/5/5 distribution across A, B, C, D.
2. **Run Post-Processing Script**:
   - Always run `python scripts/balance_grammar_mcq.py <json_path>` after generating multiple choice exercises to mathematically enforce equal distribution while keeping answers correct.

---

## 6. Question Count & Deliverables Checklist

| Exercise | Target Count | Verification Criteria |
|---|---|---|
| `01_mcq.json` | 20 questions | 4 options each, balanced A/B/C/D keys, explanation included |
| `02_verbform.json` | 20 questions | Clear `(verb)` cue, inline blank `______`, explanation included |
| `03_matching.json` | 10 pairs | 10 beginnings (1-10) and 10 endings (A-J), complete meaning |
| `04_rewrite.json` | 10 questions | Authentic prompt, cue word, correct answer + acceptable answers |
| `05_guided_cloze.json` | 2 passages (40 Qs) | Passage 1: Q1-Q20; Passage 2: Q21-Q40, 4 options each |
| `06_error_identification.json` | 10 questions | 4 bracketed sections [A: ...], correction and explanation |
| `07_sentence_combination.json` | 10 questions | 2 source sentences, conjunction cue, combined sentence |
| `08_sentence_building.json` | 10 questions | Slash-delimited cues, grammatically complete target sentence |
| `grammar_raw.json` | 1 composite file | Contains all 8 exercise objects under `exercises` dictionary |
