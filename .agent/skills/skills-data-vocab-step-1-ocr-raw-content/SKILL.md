---
name: data-vocab-step-1-ocr-pdf-to-raw-content
description: Use this skill when the user wants to turn specific pages of a textbook PDF into a structured `raw-content.md` for a Unit. Trigger when the user references a PDF file plus page numbers and wants the OCR/vision-extracted markdown saved under a Unit folder (typically `.../unit-N/vocab/raw-content.md`), or when the user is following the lesson-data pipeline and is on "vocab step 1 OCR raw content".
---

# PDF to Raw-Content Markdown

## Role

You are an experienced English teacher reading textbook pages. The markdown you produce must preserve the lesson exactly as printed — no invented sections, no summarized phrasing, and no skipped exercises.

## What this skill does

Given a textbook PDF and a page range, convert the requested pages to PNG images, inspect and extract text from the images directly using the agent's built-in image reading tool (`view_file` with multimodal vision), and write a structured `raw-content.md` that faithfully mirrors the printed lesson (headings, exercises, tables, dialogs, captions). The temporary image folder is deleted at the end so only `raw-content.md` remains in the Unit folder.

## When to use this skill

- The user provides a PDF path and page numbers and asks for `raw-content.md`.
- The user is following the lesson-data pipeline and is on "vocab step 1 OCR raw content".
- A Unit folder is empty and needs its source markdown produced from a textbook scan.

This skill does not cover vocabulary extraction, exercise generation, or any later pipeline step — each of those has its own skill.

## Non-negotiable rules

1. **USE AGENT VISION TOOL ONLY FOR TEXT EXTRACTION**:
   - The agent MUST use its own built-in tool (`view_file`) on each page image to read and extract text using multimodal vision.
   - **STRICTLY PROHIBITED**: DO NOT write or run Python scripts to perform OCR (e.g. Tesseract, pytesseract, easyocr, cv2, ocr_tool.py). The agent directly "sees" and transcribes the images.
2. **Faithful preservation**:
   - Extract every visible text element on the requested pages: section headings, instructions, numbered exercises, tables, dialogs, examples, and captions.
   - Later pipeline steps rely on complete, verbatim markdown.
   - Do not invent, paraphrase, or hallucinate content. If any text is smudged or ambiguous, record it as seen or add a brief inline flag `[unclear: ...]`.
3. **Exact output format**:
   - Output must be a single Markdown file named exactly `raw-content.md` saved in the **Save Location**. No `.txt`, no other filenames.
4. **Python execution**:
   - Python is used ONLY for slicing the PDF into page images via `scripts/pdf2images.py`.
   - Run via `python3` (or `poetry run python3` if a Poetry environment is configured).

## Initial information needed

Ask the user for three things before starting and wait until all three are provided:

1. **Input PDF File** (`file pdf đầu vào`) — the exact path to the PDF.
2. **Pages to Process** (`trang cần xử lý`) — page numbers or page ranges (e.g. `5-10`, or `12`).
3. **Save Location** (`vị trí lưu file`) — the directory where `raw-content.md` should be written (e.g. `.../unit-1/vocab`).

Do not guess any of these. The page numbers in particular matter — textbooks contain many units in a single PDF.

## Workflow

### Step 1 — Convert the requested pages to images

Run `scripts/pdf2images.py` to extract only the requested pages and save them as PNGs under `<Save Location>/pages/`:

```bash
python3 .agent/skills/skills-data-vocab-step-1-ocr-raw-content/scripts/pdf2images.py <pdf_path> --output <save_location> --start <first_page> --end <last_page>
```

*(Note: If working in a poetry-managed project, you may use `poetry run python3 ...`).*
If a single page is requested, set `--start` and `--end` to the same number.

### Step 2 — Read each image with agent tool (`view_file`) & transcribe to Markdown

1. List the generated images in `<Save Location>/pages/` and sort them in natural page order (e.g. `page_7.png`, `page_8.png`, ...).
2. Call `view_file` on each PNG image file individually.
   - The image is loaded directly into your multimodal vision context.
3. Transcribe and structure the content into clean Markdown:
   - **Headings**: Unit titles and main sections become `#`, `##`, `###` headings.
   - **Exercises**: Keep original numbers, options (A, B, C, D), and blanks (`___`).
   - **Dialogs & Conversations**: Preserve speaker labels (e.g., `Phong: ...`, `Hung: ...`).
   - **Tables**: Convert printed tables and matching grids into Markdown tables (`| ... | ... |`).
   - **Vocabulary Boxes & Prompts**: Keep word boxes verbatim in bulleted or blockquote format.
   - **Grammar & "Remember!" Boxes**: Format with Markdown blockquotes (`> **Remember!** ...`).
4. Assemble all pages in page order into one cohesive document.

### Step 3 — Save `raw-content.md`

Use `write_to_file` to write the assembled content directly into `<Save Location>/raw-content.md` (NOT inside `pages/`).

### Step 4 — Clean up temporary images

Remove the temporary `pages/` directory so only `raw-content.md` remains in `<Save Location>`:

```bash
rm -rf <Save Location>/pages
```

### Step 5 — Confirm with the user

Confirm to the user that `raw-content.md` has been created at the Save Location, mention the pages processed, and invite them to review the content before moving on to Step 2 (`data-vocab-step-2-raw-vocabulary`).
