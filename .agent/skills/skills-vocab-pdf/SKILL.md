---
name: vocab_pdf
description: Use this skill when the user asks to generate, display, format, or export vocabulary theory and practice exercises into a publication-grade textbook PDF file (e.g., `unit-<N>.pdf` or `vocab_unit<N>.pdf`). It establishes the strict 11-page publication standard for Global Success (GS10–12): open textbook layout (no heavy card boxes/frames), single font (Plus Jakarta Sans), 3-color scheme (Blue #1d4ed8, Orange #ea580c, Black #000000 on White #ffffff), vertical full-page distribution, right-edge clipping prevention for picture grids, zero Category overlap, and deterministic 11-page budget.
---

# Standard Publication Workbook PDF Skill (`vocab_pdf`)

## Role & Purpose
You are an expert educational publisher and digital curriculum typesetter. Your mission is to compile, lay out, and export a master publication-grade student workbook PDF (`vocab_unit<N>.pdf` / `unit-<N>.pdf`) for any Unit in Global Success (10–12):
1. **Title Header**: `GLOBAL SUCCESS <Grade>` and `Unit <N>: <THEME IN CAPS>` with student identification strip (`Full Name`, `Class`, `Date`).
2. **Part I. Core Vocabulary (Pages 1 & 2)**: All vocabulary words categorized cleanly (first categories on Page 1; remaining categories on Page 2) with large images, British/American IPA, clear Vietnamese definitions, and collocations, spread out to fill ~95% of each page vertically with zero overlap.
3. **Part II. Practice Exercises (Pages 3 to 10)**: All 16 standard practice exercise types formatted in open, uncluttered, ink-saving textbook style without artificial boxes or frames.
4. **Part III. Answer Key & Model Answers (Page 11)**: A compact 4-column master key fitting completely on Page 11 with zero spillover to Page 12.

---

## Strict Publication & Design Standards

### 1. Typography & Ink-Saving Color System
- **Single Font**: Only **`Plus Jakarta Sans`** is permitted across the entire document.
- **Palette**:
  - **Exercise Headers & Section Titles**: Primary Blue (`#1d4ed8`).
  - **Instructions & Directions**: Vibrant Orange (`#ea580c`).
  - **All Body Content & Handwriting Rules**: Black (`#000000`).
  - **Background**: Always pure White (`#ffffff`).
- **No Heavy Card Boxes or Frames**:
  - Do NOT wrap exercises or vocabulary cards in rounded box outlines, dark borders, or solid gray background cards.
  - Apply clean, open typography with thin, subtle dotted row separators (`border-bottom: 1px dotted #000000;`), matching genuine printed educational books.

---

## Page Budget & Section Allocation (Strict 11 Pages)

| Page | Content & Scope | Key Visual & Layout Rules | Target Height Fill |
| :---: | :--- | :--- | :---: |
| **Page 1** | **Title Header + Part I: Categories (First Half)** | • Header: `GLOBAL SUCCESS <Grade>` (18.5pt bold blue), `Unit <N>: <THEME>` (12.5pt bold black), `CORE VOCABULARY & PRACTICE WORKBOOK` (8.2pt orange).<br>• Student info strip: Name, Class, Date on right.<br>• 3-column grid, images `76×66px`, bold word `12pt`, meaning `10.2pt`.<br>• Vertically distributed with subtle dotted row separators. | **~95%** |
| **Page 2** | **Part I: Categories (Second Half)** | • Running header: `GLOBAL SUCCESS <Grade> • UNIT <N>: <THEME>` \| `PART I: CORE VOCABULARY (CONT.)`.<br>• Remaining categories separated by `.cat-separation-gap { height: 6px; clear: both; }`.<br>• **Zero Overlap**: Finishes comfortably on Page 2 with images `70×60px`. | **~95%** |
| **Page 3** | **Part II: Exercises 1 & 2** *(Vocabulary Identification & Completion - 20 items)* | • Running header + `PART II: PRACTICE EXERCISES`.<br>• Exercise 1 (10 items, 2 cols of 5) + Exercise 2 (10 items, 2 cols of 5).<br>• Compact balanced spacing (`.ex1-item, .ex2-item { margin-bottom: 7px !important; font-size: 9.8pt; }`). | **~95%** |
| **Page 4** | **Exercises 3 & 4** *(Everyday Conversations + Picture Vocabulary)* | • Exercise 3: 10 dialogue questions (2 cols of 5, compact `margin-bottom: 2.5px; font-size: 8.6pt; line-height: 1.18`).<br>• Exercise 4: **All 20 pictures** (4 cols × 5 rows) fit completely on Page 4.<br>• **Right-Edge Clipping Prevention**: Grid uses `repeat(4, minmax(0, 1fr)) !important;` with responsive CSS handwriting slot (`.pic-dotted-slot`). Image frame `height: 44px; overflow: hidden;`.<br>• Zero clipping on Column 4. | **~95%** |
| **Page 5** | **Exercises 5, 6, 7 (Part 1)** *(Word Recall, Word Box Sentences, Paragraph Fill Text)* | • Exercise 5: 10 definition recall items (2 cols of 5).<br>• Exercise 6: Word Box + 10 completion sentences (2 cols of 5).<br>• Exercise 7: Word Box + complete narrative reading passage with inline blanks `(1)` to `(10)`. | **~95%** |
| **Page 6** | **Exercises 7 (Part 2), 8, 9** *(Passage Answer Slots, Sentence Ordering, Synonyms)* | • Exercise 7 answer slots: 10 numbered blank lines in 2 rows of 5.<br>• Exercise 8: 5 sentence rearrangement items (2 cols: 3 left, 2 right).<br>• Exercise 9: 5 synonym questions with bold target words (2 cols). | **~90%** |
| **Page 7** | **Exercises 10 & 11** *(Antonyms & Opposite Meaning, Dictionary Skills)* | • Explicit `page-break` before Exercise 10.<br>• Exercise 10: 5 antonym questions in 2 columns.<br>• Exercise 11: 5 authentic dictionary entries (headword, IPA, definition, collocations, 2 practice sentences).<br>• `.dict-open-entry { margin-bottom: 8px; font-size: 9.6pt; line-height: 1.3; }`. | **~92%** |
| **Page 8** | **Exercise 12** *(Real-World Signs & Notices)* | • Explicit `page-break` before Exercise 12.<br>• All 10 real-world notices (Signs 1–5 on left, Signs 6–10 on right).<br>• Sign images `64px` height with `.sign-media-col { width: 74px; }`.<br>• Question stems and choices aligned in parallel right column. | **~92%** |
| **Page 9** | **Exercises 13, 14, 15** *(Word Families Table, Word Form MCQ, Word Formation)* | • Explicit `page-break` before Exercise 13.<br>• Exercise 13: Clean 6-column word families table using `<colgroup>` with percentage widths.<br>• Exercise 14: 10 multiple choice word formation items (2 cols of 5).<br>• Exercise 15: 5 context word formation sentences with root cues `[BASE]`. | **~93%** |
| **Page 10** | **Exercise 16** *(Sentence Translation - Dịch Câu)* | • Explicit `page-break` before Exercise 16.<br>• 10 Vietnamese sentences covering the unit's core vocabulary.<br>• **Full-Width Dotted Writing Rules**: Every sentence has two 100% full-width dotted notebook writing lines (`.trans-write-slot { height: 20px; }`, `.trans-open-row { margin-bottom: 14px; }`). | **~90%** |
| **Page 11** | **Part III: Answer Key & Model Answers** *(Complete Key for All 16 Exercises)* | • Explicit `page-break` before Part III.<br>• Structured in 4 balanced columns (`.ak-4col-grid { gap: 4px 8px; }`).<br>• Compact typography (`.ak-item-open { font-size: 7.6pt; }`, `.ak-stack { font-size: 7.2pt; line-height: 1.12; }`) guaranteeing all 16 exercises fit completely on Page 11.<br>• **Page 12 Spillover Permanently Eliminated**. | **~65%** |

---

## Production Execution Pipeline

### Step 1: Compile the Standard HTML
Run `build_vocab_pdf.py` to generate the master HTML:
```powershell
python ".agent/skills/skills-vocab-pdf copy/scripts/build_vocab_pdf.py" unit-1
```
This produces:
- `lessons/<unit>/vocab/vocab_unit<N>.html`
- `lessons/<unit>/vocab/pdf.html`
- `pdf.html` (at workspace root)

### Step 2: High-Resolution Native JPEG Base64 Encoding & Headless Chrome Export
Execute `export_pdf.py`:
```powershell
python ".agent/skills/skills-vocab-pdf copy/scripts/export_pdf.py" unit-1
```
- Converts local WebP/PNG images into native JPEG Base64 with Pillow (`quality=92, optimize=True`), enabling native PDF DCTDecode.
- Executes Google Chrome Headless:
  ```powershell
  chrome.exe --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf=vocab_unit1.pdf file:///D:/GS12/lessons/unit-1/vocab/temp_selfcontained.html
  ```
- Verifies exact page count with `fitz` (PyMuPDF):
  ```python
  import fitz
  doc = fitz.open("lessons/unit-1/vocab/vocab_unit1.pdf")
  assert len(doc) == 11, f"Expected 11 pages, got {len(doc)}"
  ```

---

## Checklist Before Delivery
1. **Total Page Count**: Must be **EXACTLY 11 pages**. No Page 12.
2. **Page 1 Header**: Title is `GLOBAL SUCCESS 12` and `Unit 1: LIFE STORIES WE ADMIRE`. Student identification strip present.
3. **Page 2 Separation**: All remaining categories are cleanly separated; zero overlap.
4. **Exercise 4**: All 4 columns within printable width; zero right-edge clipping.
5. **Page 8 Signs**: All 10 signs fit on Page 8; images and options clearly readable.
6. **Exercise 16**: Two full-width dotted handwriting lines per translation question.
7. **Clean Workspace**: All intermediate debug scripts (`test_*.py`, `debug_*.html`, `temp_*.html`) removed.
