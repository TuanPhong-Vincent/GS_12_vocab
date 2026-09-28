---
name: data-vocab-step-3-vocab-json
description: Use this skill when the user asks to generate `vocab.json` for an English lesson Unit from `raw-vocabulary.md` and `raw-content.md`. Trigger when the user references a Unit folder containing those two files and wants the structured vocab output (pronunciation, meanings, example sentences, audio paths, image paths) produced. Also trigger when the user is following the lesson-data pipeline and is on "vocab step 3 vocab json".
---

# Vocabulary JSON Generation

## Role

You are an experienced English teacher. The meanings and example sentences you write should read like natural, accurate prose — no word-usage errors, no grammar mistakes, no awkward phrasing.

## What this skill does

Given a Unit folder containing `raw-vocabulary.md` and `raw-content.md`, generate a structured `vocab.json` file inside the Unit's `vocab/` subfolder. Each word receives British and American IPA, a Vietnamese meaning matched to the lesson context, a newly generated example sentence (aligned with the lesson context but not copied directly from the text) with its Vietnamese translation, and absolute paths to its audio and image files. The vocabulary is built up one group at a time as part files (`vocab-part-1.json`, `vocab-part-2.json`, ...) and merged into a single `vocab.json` at the end.

## When to use this skill

- The user explicitly asks to generate `vocab.json` / the vocabulary JSON for a Unit.
- The user provides a Unit folder path with `raw-vocabulary.md` (and usually `raw-content.md`) and expects `vocab/vocab.json` output.
- The user is following the lesson-data pipeline and is on "vocab step 3 vocab json".

This skill does not cover reading, speaking, writing, listening, pronunciation, grammar, or the later vocab steps (image prompts, audio generation, practice exercises) — each has its own skill.

## Non-negotiable rules

A handful of rules cannot be relaxed because they protect either the dataset's integrity or the audio/image pipeline that runs on top of these paths:

- Output must be **valid JSON only** — no HTML, no Markdown wrappers, no commentary inside the files.
- **No Python scripts are written during generation.** The only script in [`scripts/`](scripts/) is the merge helper, used during post-processing.
- Meanings must **match the lesson context** in `raw-content.md`. If a word has multiple senses, pick the one that fits how the word is used in the lesson, not a generic dictionary gloss. Due to copyright reasons, **do not copy example sentences directly from `raw-content.md`** — write completely new, original example sentences that align with the lesson's context and vocabulary usage.
- Example sentences must **actively apply the target grammar structures** found in the **Grammar** section of `raw-content.md` (e.g., relative clauses referring to a whole sentence, verbs with prepositions/phrasal verbs, specific tenses, passive forms, or conditional clauses taught in that unit). This ensures every example sentence reinforces both the target vocabulary and the unit's focal grammar.
- Media paths are **absolute and consistent**: every `audio_word`, `audio_sentence`, and `image` for the same word must share the same `{book_slug}/{unit_slug}/{word-with-hyphens}` stem, differing only in suffix.

Everything else — exact field shape, path templates, the IPA "no syllable division" rule — is documented in the reference file.

## Initial information needed

Ask the user for one thing before starting:

- **Target Directory** (`thư mục chứa file raw-vocabulary`) — the exact path to the Unit directory containing `raw-vocabulary.md` and `raw-content.md`.

Wait for the user to provide it. Do not guess.

## Workflow

### Step 1 — Read the inputs

1. Read `raw-vocabulary.md` in the Target Directory. If it does not exist, tell the user and stop.
2. Read `raw-content.md` in the Target Directory for lesson context. If it does not exist, tell the user, then proceed without context (meanings and example sentences will be generated independently — note this is the worse path).
3. Count the vocabulary groups in `raw-vocabulary.md` — each `#` header marks one group.
4. Make sure `vocab/` exists as a subfolder of the Target Directory; create it if not.

### Step 2 — Load the reference material

Before generating any file, read the reference document in this skill folder:

- [`reference/vocab-fields.md`](reference/vocab-fields.md) — the per-word field schema, the part-file shape, and the absolute-path templates for audio and image references.

### Step 3 — Generate one part file per group

Process the groups one at a time to stay clear of output-size limits. For each group `N` (1, 2, 3, ...):

1. Extract every word and phrase in the group from `raw-vocabulary.md`.
2. For each word, build the JSON object described in [`reference/vocab-fields.md`](reference/vocab-fields.md), pulling meanings from `raw-content.md` and generating original, non-overlapping example sentences that match the lesson context and actively apply the target grammar structures taught in the Grammar section of `raw-content.md`.
3. Save the group to `vocab/vocab-part-{N}.json` inside the Target Directory.
4. Move on to the next group. Do not start the next group's file until the current one is written.

### Step 4 — Merge the part files

After every group has been written, run the merge script. It sorts the part files numerically, assigns sequential string `id`s (groups numbered 1..G, words numbered 1..W across the whole file), writes `vocab/vocab.json`, and deletes the part files.

```bash
poetry run python3 .agent/skills/skills-data-vocab-step-3-vocab-json/scripts/merge_vocab_parts.py <target_directory>
```

### Step 5 — Confirm with the user

Tell the user that `vocab.json` has been created, and report the total number of groups and words processed.
