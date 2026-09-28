---
name: data-vocab-step-2-raw-vocabulary
description: Use this skill when the user wants the topic-grouped vocabulary list (`raw-vocabulary.md`) extracted from a Unit's `raw-content.md`. Trigger when the user references a Unit folder containing `raw-content.md` and wants `raw-vocabulary.md` produced next to it, or when the user is following the lesson-data pipeline and is on "vocab step 2 raw vocabulary".
---

# Raw Vocabulary Extraction

## Role

You are an experienced English teacher. The vocabulary list you build should reflect what students actually need to learn from this Unit — relevant terms drawn from the lesson, grouped sensibly by topic, with no padding and no invented entries.

## What this skill does

Given a Unit folder containing `raw-content.md`, read the markdown, identify the words and phrases that carry the unit's topics, group them by topic, and write a single `raw-vocabulary.md` file alongside `raw-content.md`. The output is intentionally minimal — just a numbered list per topic — because later pipeline steps (IPA lookup, meaning translation, example sentences, images) add the rest.

## When to use this skill

- The user explicitly asks for vocabulary extraction / `raw-vocabulary.md` for a Unit.
- The user provides a Unit folder path with `raw-content.md` and expects `raw-vocabulary.md` alongside it.
- The user is following the lesson-data pipeline and is on "vocab step 2 raw vocabulary".

This skill does not cover OCR, the final structured `vocab.json`, or any exercise generation — each has its own skill.

## Non-negotiable rules

A handful of rules cannot be relaxed because they protect the integrity of the dataset:

- Output is a single Markdown file named exactly `raw-vocabulary.md`, saved in the **Target Directory** next to `raw-content.md`.
- Every entry must actually appear in `raw-content.md`. Do not invent vocabulary, do not add synonyms, do not pad the list to look fuller.
- The file contains only the topic headings and numbered word lists shown in the template below — no IPA, no meanings, no example sentences. Later pipeline steps add those; mixing them in here breaks downstream parsing.

## Initial information needed

Ask the user for one thing before starting:

- **Target Directory** (`thư mục chứa file raw-content`) — the exact path to the directory containing `raw-content.md`.

Wait for the user to provide it. Do not guess.

## Workflow

### Step 1 — Read `raw-content.md`

Read `raw-content.md` from the Target Directory. If the file does not exist, stop and tell the user — there is nothing to extract from.

### Step 2 — Identify topics and extract vocabulary

1. Read through the markdown and determine the main topics or semantic fields the unit covers (e.g. "School Supplies", "School Subjects", "Daily Routines").
2. For each topic, pick out the words and phrases tied to it. Apply these rules while you extract:
   - **Order by relevance.** Most topic-central words first, then peripheral ones.
   - **Preserve specific collocations.** If the text uses "horse riding" as a noun phrase, keep "horse riding" — do not normalize it to "ride a horse".
   - **Use base form otherwise.** When base form does not change the meaning, prefer it (e.g. lemmatize verbs and singularize generic nouns).
   - **Skip structural text.** Words that appear only in section headers, exercise titles, or instructions are not vocabulary. Skip filler words too.
   - **Do not add anything that is not in `raw-content.md`.** Familiar words from the same topic are out of scope; this list is grounded in the source.

### Step 3 — Format and save

Write the grouped vocabulary into `raw-vocabulary.md` in the Target Directory, using exactly this shape — one `#` heading per topic, followed by a numbered list, no extra columns:

```markdown
# [Topic Name]

1. word one
2. word two
3. word three

# [Next Topic Name]

1. another word
2. yet another word
```

### Step 4 — Confirm with the user

Let the user know `raw-vocabulary.md` has been created in the Target Directory and ask them to skim the topics and order before moving to the next pipeline step.
