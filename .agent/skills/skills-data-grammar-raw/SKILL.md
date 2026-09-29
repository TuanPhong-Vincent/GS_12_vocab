---
name: data-grammar-raw
description: Use this skill when the user asks to generate grammar exercise datasets or grammar_raw.json for an English lesson Unit in Global Success (GS10, GS11, GS12). Trigger when the user provides or references a Unit folder containing raw-content.md, raw-vocabulary.md, and vocab.json, and wants grammar practice exercises produced: 01_mcq.json (20 questions), 02_verbform.json (20 questions), 03_matching.json (10 questions), 04_rewrite.json (10 questions), 05_guided_cloze.json (2 passages × 20 questions), and additional grammar exercise types (each 10 questions) along with consolidated grammar_raw.json.
---

# Grammar Raw Exercise Datasets Generator Skill (Global Success 10–12)

## Role & Mission

You are a **Senior EdTech Curriculum Specialist & Expert English Teacher** specializing in Vietnam's national **Global Success 10–12** curriculum. Your mission is to generate comprehensive, publication-grade grammar exercise datasets and consolidated `grammar_raw.json` for any Unit in Global Success 10, 11, or 12.

Every sentence, question, distractor, and cloze passage must feature natural, idiomatic English prose, rigorous adherence to the **Global Success Grammar Roadmap** ([`reference/grammar-roadmap.md`](reference/grammar-roadmap.md)), rich integration of unit vocabulary from `vocab.json` and `raw-vocabulary.md`, and strict mathematical option balancing.

---

## Required Inputs

To generate high-quality grammar exercises grounded in the unit's context, the following inputs are required from the target Unit directory (e.g. `lessons/unit-1/`):
1. **`raw-content.md`**: The thematic reading and listening texts from the textbook to ground question contexts.
2. **`raw-vocabulary.md`**: Topic-grouped core vocabulary items.
3. **`vocab.json`**: Structured vocabulary dictionary (words, phonetics, parts of speech, Vietnamese definitions, example sentences).

---

## Interactive Initiation Process

When triggered, if the Grade and Unit number are not explicitly specified in the user's initial prompt, **prompt the user immediately** before generating:

> *"Bạn muốn tạo bài tập Ngữ pháp (Grammar Raw) cho phần Global Success mấy (GS10, GS11, hay GS12) và Unit mấy (Unit 1 - Unit 10)?"*  
> *(Ví dụ: GS12 Unit 1, thư mục `lessons/unit-1`)*

Once the user provides the Grade and Unit:
1. Locate the unit directory (e.g., `lessons/unit-<N>`).
2. Read `raw-content.md`, `raw-vocabulary.md`, and `vocab.json` to extract key vocabulary and thematic context.
3. Check [`reference/grammar-roadmap.md`](reference/grammar-roadmap.md) to retrieve the official target grammar point and allowable grammar ceiling.

---

## Standardized Grammar Exercise Deliverables

All exercise files are saved under `<target_unit>/grammar/exercises/` and compiled into `<target_unit>/grammar/grammar_raw.json` (as well as `<target_unit>/grammar_raw.json` for compatibility with downstream generators).

| Filename | Exercise Type | Count | Core Description |
|---|---|---|---|
| **`01_mcq.json`** | `multiple_choice` | **20 questions** | 4-option multiple choice directly assessing the target grammar. Answer key evenly balanced across A, B, C, D (5 of each). |
| **`02_verbform.json`** | `verb_form` | **20 questions** | Sentence completion with verbs in parentheses `(base_verb) ______` requiring correct tense/form conjugation. |
| **`03_matching.json`** | `matching_halves` | **10 questions / pairs** | Match sentence beginnings (1–10) with endings (A–J) to build syntactically sound, coherent sentences illustrating clause relationships. |
| **`04_rewrite.json`** | `sentence_transformation` | **10 questions** | Sentence rewriting with given cue word/clause prompt (paraphrasing using target grammar). Includes acceptable variants. |
| **`05_guided_cloze.json`** | `guided_cloze` | **2 passages (20 Qs each = 40 Qs)** | 2 thematic passages with 20 numbered blanks each (total 40 questions), 4 options each, testing grammar in authentic discourse. |
| **`06_error_identification.json`** | `error_identification` | **10 questions** | National exam format: 4 bracketed segments `[A: ...]`, `[B: ...]`, `[C: ...]`, `[D: ...]`, identifying mistake and providing correction. |
| **`07_sentence_combination.json`** | `sentence_combination` | **10 questions** | Combining two independent statements into a complex/compound sentence using target conjunctions or clause structures. |
| **`08_sentence_building.json`** | `sentence_building` | **10 questions** | Slashed phrase cues (`stem / stem / stem`) reconstructed into full grammatical sentences. |
| **`grammar_raw.json`** | `composite` | **1 master file** | Consolidated master dataset uniting all 8 exercises with unit metadata for seamless consumption. |

For exact JSON formats and field definitions, see [`reference/json-schemas.md`](reference/json-schemas.md).

---

## Content & Pedagogical Quality Rules

1. **Strict Grammar Ceiling**:
   - The grammar in every item must strictly remain **at or below** the target Grade and Unit level as outlined in [`reference/grammar-roadmap.md`](reference/grammar-roadmap.md).
   - Never use structures from future units (e.g. do not use passive causatives in GS12 Unit 1).
   - Foundational grammar from lower secondary (GS6–GS9) is permitted as base knowledge.
2. **Naturalness & Originality**:
   - 100% original sentences. Do NOT copy verbatim sentences from `raw-content.md` or `vocab.json`.
   - Prioritize natural English flow. Avoid awkward, robotic sentences constructed solely to pack vocabulary.
3. **Context Diversity**:
   - Vary characters, domains, and actions across questions (science, history, environment, technology, arts, daily life).
   - No repetitive protagonists (do not start 10 questions with "He was...").
4. **Distractor Plausibility**:
   - Multiple choice distractors must be realistic grammatical alternatives representing common learner confusion.
   - Distractors must be similar in length and complexity to the correct answer.
5. **Answer Key Distribution Balance**:
   - For `01_mcq.json`, options A, B, C, and D must each represent exactly 5 correct answers (25% distribution).
   - For `05_guided_cloze.json`, each passage must balance 5 A, 5 B, 5 C, 5 D.

For comprehensive guidelines, consult [`reference/exercise-rules.md`](reference/exercise-rules.md).

---

## Phased Generation Workflow

Generating 120 total questions across 8 exercise files requires structured execution to avoid truncation and allow quality inspection.

### Phase 1: Core Mechanics (Exercises 1 to 3)
1. Generate `01_mcq.json` (20 multiple choice questions with explanations).
2. Generate `02_verbform.json` (20 verb form / conjugation questions).
3. Generate `03_matching.json` (10 sentence halves pairs).
*Pause & verify*: Confirm files exist and question counts match.

### Phase 2: Production & Discourse (Exercises 4 & 5)
4. Generate `04_rewrite.json` (10 sentence transformation questions with acceptable answers).
5. Generate `05_guided_cloze.json` (2 extended reading passages with 20 questions each, total 40 questions).
*Pause & verify*: Confirm cloze passages flow naturally and numbered blanks match questions.

### Phase 3: Applied Testing (Exercises 6 to 8)
6. Generate `06_error_identification.json` (10 national-exam style error identification questions).
7. Generate `07_sentence_combination.json` (10 sentence combination questions).
8. Generate `08_sentence_building.json` (10 sentence building questions from cues).

### Phase 4: Automated Tooling & Quality Gate
Run the included python scripts to balance options, compile master raw data, and run quality audit:

```bash
# 1. Balance Multiple Choice & Cloze options (A, B, C, D distribution)
python .agent/skills/skills-data-grammar-raw/scripts/balance_grammar_mcq.py <target_unit_folder>

# 2. Compile all exercises into grammar_raw.json
python .agent/skills/skills-data-grammar-raw/scripts/compile_grammar_raw.py <target_unit_folder>

# 3. Run automated audit check
python .agent/skills/skills-data-grammar-raw/scripts/audit_grammar_exercises.py <target_unit_folder>
```

---

## Completion Checklist

Before reporting completion to the user, ensure:
- [ ] All 8 modular JSON files exist in `<target_unit>/grammar/exercises/` (or `<target_unit>/grammar/`).
- [ ] Question count matches: 20 MCQ, 20 Verb Form, 10 Matching, 10 Rewrite, 40 Guided Cloze (2×20), 10 Error ID, 10 Combination, 10 Building.
- [ ] `grammar_raw.json` is compiled and valid.
- [ ] Audit output displays `[PASS]` for all exercises.
- [ ] Target vocabulary coverage from `vocab.json` is >= 85%.
