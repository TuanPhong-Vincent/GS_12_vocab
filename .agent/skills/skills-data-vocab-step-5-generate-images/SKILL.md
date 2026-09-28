---
name: data-vocab-step-5-generate-images
description: Use this skill when the user asks to batch-generate vocabulary images for a Unit. Trigger when the user references a Unit folder containing `vocab/image-prompts.json` and wants the corresponding images produced under `lessons/media/<book>/<unit>/images/`, or when the user is following the lesson-data pipeline and is on "vocab step 5 generate images".
---

# Vocabulary Image Batch Generation

## Role

You are an automated image generation assistant. Your job is to read `vocab/image-prompts.json` for a Unit and batch-generate all vocabulary images using your built-in `generate_image` tool directly.

## What this skill does

Given a Unit folder containing `vocab/image-prompts.json`, read the prompt definitions, call the agent's native `generate_image` tool for each prompt with 16:9 aspect ratio, and place the resulting images into `lessons/media/<book>/<unit>/images/`.

## When to use this skill

- The user explicitly asks to generate images for a Unit's vocabulary.
- The user provides a Unit folder path with `vocab/image-prompts.json` and expects the images written under `lessons/media/<book>/<unit>/images/`.
- The user is following the lesson-data pipeline and is on "vocab step 5 generate images".

This skill does not generate the prompts — that is step 4. It also does not generate audio — that is step 6.

## Non-negotiable rules

- **Use the built-in `generate_image` tool.** Do not call external APIs, web scraping scripts, or external Gemini python scripts.
- **Aspect Ratio**: Always pass `AspectRatio: "16:9"` when calling `generate_image`.
- **Skip Existing Images**: If an image file already exists under `lessons/media/<book>/<unit>/images/` (e.g. `police-officer.webp` or `police-officer.png`), skip generating it unless the user explicitly requests `--overwrite`.
- **Output Placement**: After generating an image artifact using `generate_image`, move or copy it to `lessons/media/<book>/<unit>/images/<filename>`.

## Initial information needed

Ask the user for:

- **Target Directory** (`thư mục chứa file vocab/image-prompts.json`) — the exact path to the Unit directory holding `vocab/image-prompts.json`.

From that path, derive:

- **book_slug** — e.g. `gs9` for `global-success-9`.
- **unit_slug** — e.g. `unit-1`.
- **Media Output Path**: `lessons/media/{book_slug}/{unit_slug}/images/`

## Workflow

### Step 1 — Read `vocab/image-prompts.json`

1. Read `vocab/image-prompts.json` inside the Target Directory.
2. Ensure the output directory `lessons/media/{book_slug}/{unit_slug}/images/` exists (create if necessary).

### Step 2 — Batch Generate Images with `generate_image` Tool

For each item in `vocab/image-prompts.json`:

1. Extract `object`, `prompt`, and `filename` (e.g. `police-officer.webp`).
2. Check if `lessons/media/{book_slug}/{unit_slug}/images/{filename}` already exists.
3. If it does not exist (or overwrite mode is enabled):
   - Invoke `generate_image` with:
     - `Prompt`: `item["prompt"]`
     - `ImageName`: A short 2-3 word identifier derived from `object` (e.g., `vocab_police_officer`).
     - `AspectRatio`: `"16:9"`
   - Once generated, copy or move the image file to `lessons/media/{book_slug}/{unit_slug}/images/{filename}`.

### Step 3 — Confirm and Report

Report completion to the user:
- List of successfully generated images.
- Final output directory path.
