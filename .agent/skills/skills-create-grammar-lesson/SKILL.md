---
name: create-grammar-lesson
description: Use this skill when the user wants to generate a complete grammar lesson (theory explanation, vocabulary-integrated exercises, interactive HTML, printable PDF, and audit checks) for any Unit in Global Success 10–12 (GS10, GS11, GS12 Units 1–10) based on grammar-roadmap.md, vocab.json, and grammar templates. Trigger when the user requests to create grammar exercises, build grammar lessons, or produce grammar_unit*.html and grammar_unit*.pdf.
---

# Grammar Lesson & Exercises Generator Skill (Global Success 10–12)

## Role

You are a Senior EdTech Curriculum Specialist & Technical Content Developer. You specialize in designing comprehensive English grammar lessons aligned strictly with the official **Global Success 10–12 Grammar Roadmap** ([`reference/grammar-roadmap.md`](reference/grammar-roadmap.md)), combining detailed grammar theory, standardized grammar exercise formats, vocabulary integration from the Unit's `vocab.json`, interactive HTML display pages (`grammar_unit<N>.html`), and printable PDF documents (`grammar_unit<N>.pdf`) with automated quality auditing.

---

## Required Inputs & Roadmap Reference

Before proceeding, check if the user has specified the Grade (GS10, GS11, GS12) and Unit number (1 to 10). If not specified, **prompt the user by presenting the target units and grammar points from the Global Success 10–12 roadmap**:

*Prompt the user*: `"Bạn muốn tạo bài học ngữ pháp cho Grade nào (GS10, GS11, GS12) và Unit mấy (Unit 1 - Unit 10)?"` (Trong repository này, mặc định là GS12).

---

### Global Success 10 (GS10) Roadmap

| Unit | Unit Theme | Target Grammar Point |
|---|---|---|
| **Unit 1** | Family Life | Present simple vs. present continuous |
| **Unit 2** | Humans and the Environment | The future with will and be going to, Passive voice |
| **Unit 3** | Music | Compound sentences, To-infinitives and bare infinitives |
| **Unit 4** | For a Better Community | Past simple vs. past continuous with when and while |
| **Unit 5** | Inventions | Present perfect, Gerunds and to-infinitives |
| **Unit 6** | Gender Equality | Passive voice with modals |
| **Unit 7** | Viet Nam and International Organisations | Comparative and superlative adjectives |
| **Unit 8** | New Ways to Learn | Relative clauses: defining and non-defining relative clauses with who, that, which, and whose |
| **Unit 9** | Protecting the Environment | Reported speech |
| **Unit 10** | Ecotourism | Conditional sentences Type 1 and Type 2 |

---

### Global Success 11 (GS11) Roadmap

| Unit | Unit Theme | Target Grammar Point |
|---|---|---|
| **Unit 1** | A Long and Healthy Life | Past simple vs. Present perfect |
| **Unit 2** | The Generation Gap | Modal verbs: must, have to and should |
| **Unit 3** | Cities of the Future | Stative verbs in the continuous form, Linking verbs |
| **Unit 4** | ASEAN and Viet Nam | Gerunds as subjects and objects |
| **Unit 5** | Global Warming | Present participle and past participle clauses |
| **Unit 6** | Preserving Our Heritage | To-infinitive clauses |
| **Unit 7** | Education Options for School-Leavers | Perfect gerunds and perfect participle clauses |
| **Unit 8** | Becoming Independent | Cleft sentences with It is/was ... that/who ... |
| **Unit 9** | Social Issues | Linking words and phrases |
| **Unit 10** | The Ecosystem | Compound nouns |

---

### Global Success 12 (GS12) Roadmap

| Unit | Unit Theme | Target Grammar Point |
|---|---|---|
| **Unit 1** | Life Stories We Admire | Past simple vs. Past continuous |
| **Unit 2** | A Multicultural World | Articles (review and extension) |
| **Unit 3** | Green Living | Verbs with prepositions, Relative clauses referring to a whole sentence |
| **Unit 4** | Urbanisation | Present perfect (review and extension), Double comparatives to show change |
| **Unit 5** | The World of Work | Simple, compound, and complex sentences (review and extension) |
| **Unit 6** | Artificial Intelligence | Active and passive causatives |
| **Unit 7** | The World of Mass Media | Adverbial clauses of manner and result |
| **Unit 8** | Wildlife Conservation | Adverbial clauses of condition and comparison |
| **Unit 9** | Career Paths | Three-word phrasal verbs |
| **Unit 10** | Lifelong Learning | Reported speech: reporting orders, requests, offers, and advice |

---

### Grammar Ceiling & Prior Knowledge Rules

1. **Strict Grammar Ceiling**: The grammar in every generated sentence, question, option, and example must strictly stay **at or below** the target Grade and Unit's level. **Do NOT borrow structures from higher units or grades** (students have not studied them yet).
2. **Prior Foundation Knowledge (Grades 6–9)**: All core grammar structures taught in lower secondary (GS6–GS9) — basic tenses, basic modal verbs, comparative/superlative forms, simple/compound sentences, basic relative clauses, and basic conditionals — are considered mastered foundational knowledge.
3. **Naturalness First**: If a current-unit structure would make a sentence feel forced or awkward, prioritize natural English phrasing.

---

## Output Deliverables

For target Unit `<N>` (e.g. `lessons/unit-1`):
1. **Interactive HTML Display Page**: `<Target_Unit_Folder>/grammar_unit<N>.html`
2. **Printable PDF Document**: `<Target_Unit_Folder>/grammar_unit<N>.pdf`
3. **JSON Exercises Dataset**: `<Target_Unit_Folder>/exercises/01_*.json` to `07_*.json`

---

## Standardized Grammar Exercise Formats

A complete grammar unit comprises detailed theory (Section A) and 7 standardized exercise formats (Section B):

- **Exercise 1: Table Fill / Rule Classification (`01_table_fill.json`)**: Categorize grammatical forms, rules, or fill in structures/tenses based on grammar formulas.
- **Exercise 2: Multiple Choice Questions (`02_multiple_choice.json`)**: 10 questions (A, B, C, D) testing target grammar with evenly balanced distractor positions (~25% each).
- **Exercise 3: Verb Form & Inline Blank Completion (`03_verb_form.json`)**: Sentences with inline handwriting blanks (`inline-text-input`) to conjugate verbs or fill in key target structures.
- **Exercise 4: Sentence Ordering (`04_sentence_ordering.json`)**: Scrambled phrases to reassemble into grammatically coherent sentences.
- **Exercise 5: Error Identification & Correction (`05_error_identification.json`)**: Sentences containing common learner errors in the target grammar to identify and fix.
- **Exercise 6: Sentence Combination & Transformation (`06_sentence_combination.json`)**: Combine or rewrite sentences using target conjunctions, relative clauses, causatives, or inversions.
- **Exercise 7: Sentence Building (`07_sentence_building.json`)**: Construct complete sentences from cue words/phrases using the target grammar.

---

## Grammar Lesson PDF Layout & Display Standards

When rendering `grammar_unit<N>.pdf` from `grammar_unit<N>.html`:

1. **Page Header**:
   - `<h1>GRAMMAR LEVEL ADVANCED - [GRADE] UNIT <N>: [THEME]</h1>` (Bold `#1e3a8a`, uppercase, centered).
   - `<h2><GRAMMAR TOPIC NAME></h2>` (Bold `#0369a1`, uppercase, centered).
   - Bottom accent divider: `2.5px solid #1e3a8a`.

2. **Theory Section Presentation**:
   - Sub-headings: `h4` in `#1e40af`, `h5` in `#334155`.
   - Highlight formula boxes: `#f0f9ff` background with `border-left: 4px solid #1d4ed8`.
   - Contrastive tables: `#1e3a8a` header background, white text, alternating row background (`#f8fafc`).
   - Bulleted examples integrating unit vocabulary words.

3. **Practice Exercises Presentation**:
   - **Section Headers**: Title in bold `#1e3a8a`, instructions in `#1e293b`, bold italic examples.
   - **MCQ Questions**: Options (A, B, C, D) arranged horizontally on 1 single row (`display: flex; flex-wrap: nowrap; justify-content: space-between`).
   - **Verb Forms / Inline Blanks**: Dotted underline handwriting space (`border-bottom: 1.5px dotted #1e3a8a`, width `120px`), placeholder strings hidden.
   - **Sentence Ordering / Error ID / Combination**: Full-width dotted handwriting line (`border-bottom: 1.5px dotted #1e3a8a`, width `100%`), placeholder text transparent.
   - **Strip Interactive Elements**: Automatically hide check buttons (`.btn-check`, `.btn-check-inline`), feedback messages (`.feedback-msg`), and non-print controls (`@media print`).
   - **Page Margin**: Standard `0.8cm` on all 4 sides with page-break protection on individual questions (`page-break-inside: avoid`).

---

## Quality & Audit Gate Checklist (Mandatory)

Before concluding, every generated grammar lesson MUST pass 4 mandatory quality audits:

1. **Audit Check 1 — Vocabulary Coverage (>= 90%)**:
   - Total unique words from `vocab.json` (or `vocab_data_*.json`) used across theory examples and exercise items.
   - **Requirement**: Target coverage must be at least **90%**. If below 90%, enrich exercise sentences with remaining vocabulary items.
2. **Audit Check 2 — Answer Option Logic & Randomization**:
   - Multiple choice options (A, B, C, D) must contain realistic, plausible distractors.
   - Correct answer positions (A, B, C, D) must be **randomly and evenly distributed** (~25% distribution each).
3. **Audit Check 3 — Option Unpredictability**:
   - Answers must NOT be easily guessed by simple process of elimination or visual patterns.
4. **Audit Check 4 — GS10–12 Roadmap & Grammar Ceiling Alignment**:
   - Verify that 100% of theory sections and exercises strictly focus on the target grammar point specified in [`reference/grammar-roadmap.md`](reference/grammar-roadmap.md) without exceeding the grammar ceiling.

---

## Workflow & Execution Guide

### Step 1 — Verify Inputs & Grammar Target
- Identify the target Grade (`GS10`, `GS11`, `GS12`) and Unit number.
- Read `vocab.json` from `lessons/unit-<N>/vocab/vocab.json`.
- Read `raw-content.md` from `lessons/unit-<N>/raw-content.md` for thematic grounding.

### Step 2 — Run the Grammar Generator Script
Execute the Python generator script located in `scripts/generate_grammar_lesson.py`:

```bash
# Example for GS12 Unit 1:
python .agent/skills/skills-create-grammar-lesson/scripts/generate_grammar_lesson.py --grade GS12 --unit 1

# Or specifying the unit folder directly:
python .agent/skills/skills-create-grammar-lesson/scripts/generate_grammar_lesson.py --lesson "lessons/unit-1"
```

*Arguments*:
- `--grade`: Grade level (`GS10`, `GS11`, `GS12`). Defaults to `GS12`.
- `--unit`: Unit number (`1` to `10`).
- `--lesson`: Folder path (e.g. `lessons/unit-1`, `unit-1`, `Lesson1`).
- `--grammar`: (Optional) Custom grammar point description override. If omitted, automatically resolves from the GS10–12 roadmap.
- `--vocab`: (Optional) Explicit path to `vocab.json`. Defaults to `<lesson_folder>/vocab/vocab.json`.

---

## Final Verification Checklist

1. Confirm `grammar_unit<N>.html` exists and is interactive in the browser.
2. Confirm `grammar_unit<N>.pdf` exists and is formatted for printing.
3. Review audit output to confirm `[AUDIT PASSED]` with vocabulary coverage >= 90%.
4. Inform the user with a summary of the generated files and audit results.
