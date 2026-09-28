---
name: data-vocab-step-7-practice
description: Use this skill when the user asks to generate vocabulary practice exercises for an English lesson Unit. Trigger when the user references a Unit folder containing `vocab.json` (and `raw-content.md` or `raw-all-content.md`) and wants the 16 `vocab/exercises/` files produced — multiple choice, fill-in-blanks, paragraph fill, sentence ordering, dictionary entries, signs and notices, word families, word formation, translation — together with coverage checking and option balancing. Also trigger when the user is following the lesson-data pipeline and is on "vocab step 7 practice".
---

# Vocabulary Practice Exercises JSON Generation

## Role

You are an experienced English teacher. The sentences and questions you write should read like natural, accurate prose — no word-usage errors, no grammar mistakes, no awkward phrasing.

## What this skill does

Given a Unit folder containing `vocab.json` and `raw-content.md`, generate 16 vocabulary practice exercises as separate JSON files inside a `vocab/exercises/` subfolder. The exercise types span recognition (multiple choice, pic-to-word), production (write English words, fill in blanks, translation), organization (sentence ordering, word families), and applied reading (dictionary entries, signs and notices) — together they give a Unit's vocabulary a full practice cycle.

The full list of 16 files and their schemas lives in [`reference/json-schemas.md`](reference/json-schemas.md).

## When to use this skill

- The user explicitly asks to generate the vocabulary practice / vocab exercises for a Unit.
- The user provides a Unit folder path with `vocab.json` and expects `vocab/exercises/` output.
- The user is following the lesson-data pipeline and is on "vocab step 7 practice".

This skill does not cover reading, speaking, writing, listening, pronunciation, or grammar exercises — each has its own skill.

## Non-negotiable rules

A handful of rules cannot be relaxed because they protect either the dataset's integrity or the student's experience:

- Output must be **valid JSON only** — no HTML, no Markdown wrappers, no commentary in the file.
- **No Python scripts** are written during generation. The five scripts in [`scripts/`](scripts/) are the only tooling, and they only run during post-processing.
- Sentences and example phrases must be **100% original in both ideas and prose**. Do not use any ideas, contexts, names, or entities from `raw-content.md` or `example_sentence_en` from `vocab.json`. Students need fresh contexts, not a paraphrasing of the lesson.
- The grammar in every generated sentence strictly follows [`reference/grammar-roadmap.md`](reference/grammar-roadmap.md) for the target Grade and Unit. Grammar structures must stay **at or below the target Unit's level** — do NOT use grammar structures from higher units or higher grades (students haven't learned them yet).
- **Diverse contexts with topic focus & rich vocabulary (Đa dạng ngữ cảnh, bám sát chủ đề & tối ưu từ vựng)**: Exercises must feature a wide variety of engaging, realistic contexts across questions while staying anchored to the Unit's core theme or closely related domains. Maximize the utilization of the Unit's vocabulary set. Controlled, natural expansion of related contexts is encouraged, but it must strictly maintain the target grade's English proficiency level without using obscure, unstudied words.

Everything else — question counts, per-exercise structure, option-length balance, ID conventions, word-box overlap — is documented in the reference files.

## Initial information needed

Ask the user for one thing before starting:

- **Target Directory** (`thư mục chứa bài học`) — the exact path to the Unit directory containing `vocab.json` and `raw-content.md`.

Wait for the user to provide it. Do not guess.

## Workflow

The generation happens in three phases, each ending with a pause so the user can review before you continue. The phases exist for two reasons: they keep the output well within token limits, and they let the user catch direction issues early instead of after 16 files of work.

### Step 1 — Read the inputs

1. Read `vocab.json` in the Target Directory to internalize the vocabulary list (groups, words, Vietnamese meanings, example sentences, image paths).
2. Read `raw-content.md` (or `raw-all-content.md` if the Unit uses that name) to understand the topic, characters, and context.
3. Check whether `vocab/exercises/` exists. Create it if not.

### Step 2 — Load the reference material

Before generating any file, read the four reference documents in this skill folder:

- [`reference/grammar-roadmap.md`](reference/grammar-roadmap.md) — the grammar roadmap (Global Success 10–12) defining the exact grammar ceiling allowed for the target Grade and Unit.
- [`reference/json-schemas.md`](reference/json-schemas.md) — the exact JSON schema and an example for each of the 16 file types.
- [`reference/exercise-rules.md`](reference/exercise-rules.md) — cross-cutting content rules (originality, uniqueness, grammar alignment, IDs, word-box overlap) plus per-exercise instructions.
- [`reference/quality-checks.md`](reference/quality-checks.md) — what the coverage check enforces and how to read the final-review checklist.

### Step 3 — Generate the 16 JSON files in three phases

Each phase ends with a pause: write all the files for the phase, then stop and ask the user whether to continue. The 16 files are named exactly as listed in [`reference/json-schemas.md`](reference/json-schemas.md).

**Phase 1 — exercises 1 to 6.** Direct multiple choice, sentence completion, conversation completion, pic-to-word, write English words, fill in the blanks. When all six files are written, ask: *"I have completed Phase 1. Are you ready for Phase 2?"*

**Phase 2 — exercises 7 to 11.** Paragraph fill, sentence ordering, closest in meaning, opposite in meaning, dictionary entry. When all five files are written, ask: *"I have completed Phase 2. Are you ready for Phase 3?"*

**Phase 3 — exercises 12 to 16.** Signs and notices, word families table, word families MCQ, word formation, translate sentences. After Phase 3, proceed directly to Step 4 — no further pause.

For exercise 12 (signs and notices), the JSON files reference image paths like `images/sign_1.png` and the `sign_text` field is the description used as the image-generation prompt. **Do NOT generate images during exercise creation.** Write `12_signs_and_notices.json` with clear, descriptive `sign_text` prompts and unit-themed questions, but skip calling `generate_image`. The user will review the questions first and explicitly request image generation later.

### Step 4 — Post-process with the provided scripts

After all 16 files are written, run the post-processing scripts. They're idempotent — re-running is safe.

1. **Balance MCQ option positions** — spreads correct answers evenly across A/B/C/D. Run on every file with 4-option multiple-choice questions (exercises 1, 2, 3, 8, 9, 10, 12, 14):
   ```bash
   poetry run python3 .agent/skills/skills-data-vocab-step-7-practice/scripts/balance_mcq_options.py <path_to_exercise_json>
   ```

2. **Shuffle word boxes** — randomizes word order in `word_box` arrays. Run on the two files that have a word_box (exercises 6 and 7):
   ```bash
   poetry run python3 .agent/skills/skills-data-vocab-step-7-practice/scripts/shuffle_word_box.py <path_to_exercise_json>
   ```

3. **Shuffle dictionary entries** — randomizes bullet points and questions order within each entry in `11_dictionary_entry.json`:
   ```bash
   poetry run python3 .agent/skills/skills-data-vocab-step-7-practice/scripts/shuffle_dictionary_entry.py <path_to_exercise_json_or_exercises_directory>
   ```

4. **Reorder exercise IDs** — sets the top-level `id` on each file based on its `type` and `title` so the frontend displays the exercises in the canonical order. Run once on the exercises directory:
   ```bash
   poetry run python3 .agent/skills/skills-data-vocab-step-7-practice/scripts/reorder_vocab_ids.py <path_to_vocab_exercises_directory>
   ```

### Step 5 — Coverage check

Run the coverage script against the exercises directory:

```bash
poetry run python3 .agent/skills/skills-data-vocab-step-7-practice/scripts/vocab_coverage_checker.py <path_to_vocab.json> <path_to_exercises_directory>
```

The target is **≥ 95%**. If coverage falls short, follow the fix-it loop documented in [`reference/quality-checks.md`](reference/quality-checks.md) — reduce overused words, add unused words to exercises 2 and 3 in increments of 5 questions, re-run until the script reports ≥ 95%.

### Step 6 — Final review and confirm

Walk through the final-review checklist in [`reference/quality-checks.md`](reference/quality-checks.md), then let the user know all 16 vocabulary exercises have been generated, post-processed, and coverage-verified.
