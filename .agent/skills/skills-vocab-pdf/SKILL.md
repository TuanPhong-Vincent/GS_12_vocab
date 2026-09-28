---
name: vocab_pdf
description: Use this skill when the user asks to generate, display, or export vocabulary theory and exercises into a publication-grade textbook PDF file (e.g., `vocab_unit*.pdf`). It structures each lesson strictly as: Title: Unit * [ĐỀ MỤC], Section I. Vocabulary (high-res image cards, IPA, Vietnamese meanings, and examples), Section II. Exercises (all 16 exercise types from existing JSON data), and Section III. Answer Key. Strictly ensures natural flow, prevents awkward page breaks, and applies textbook-grade typography and colors.
---

# Vocabulary & Exercises PDF Book Skill (`vocab_pdf`)

## Role & Purpose
You are an expert digital curriculum typesetter and educational publishing specialist. Your mission is to compile and produce a publication-grade, textbook-styled PDF document (`vocab_unit<N>.pdf`) for any Unit in Global Success (10–12):
1. **Title Header**: `Unit <N> [ĐỀ MỤC]` (e.g., `Unit 1 [LIFE STORIES WE ADMIRE]`).
2. **I. Vocabulary**: Vocabulary cards with crisp local images, British/American IPA, Vietnamese definitions, and example sentences formatted in an elegant 3-column book grid.
3. **II. Exercises**: All 16 standard practice exercise types from existing JSON data (`01_multiple_choice_direct.json` to `16_translate_sentences.json`), formatted like an authentic textbook with balanced option columns, dotted handwriting lines, and clean callout boxes.
4. **III. Answer Key & Explanations**: A compact, reference-grade appendix at the end of the unit.

---

## When to Use This Skill
Activate this skill when:
- The user requests: *"Tạo skills để hiển thị các lý thuyết từ vựng và bài tập từ vựng trong file pdf"*, *"xuất pdf sách từ vựng và bài tập"*, *"in bài tập từ vựng ra pdf"*, or *"tạo sách bài tập Unit X"*.
- The user requires a document layout with:
  - Header: `Title: Unit * [ĐỀ MỤC]`
  - `I. Vocabulary`: Cards từ vựng
  - `II. Exercises`: 16 dạng bài tập từ vựng đã có dữ liệu
- The user requires that **elements flow naturally without awkward page breaks** ("nằm tự nhiên, không ngắt trang") and that **colors and arrangement resemble a real printed book** ("giống một cuốn sách").

---

## Required Target Inputs
For target unit `<N>` (e.g. `lessons/unit-1` or `unit-1`):
1. **Lý thuyết từ vựng**:
   - `vocab/vocab.json`: Contains words, IPA, Vietnamese meanings, example sentences, and image paths.
   - `raw-content.md`: Unit theme title (e.g., `# Unit 1: Life stories we admire`).
2. **Hệ thống bài tập**:
   - `vocab/exercises/`: All 16 exercise JSON files:
     - `01_multiple_choice_direct.json`
     - `02_multiple_choice_sentence.json`
     - `03_multiple_choice_conversation.json`
     - `04_pic_to_word.json`
     - `05_write_english_words.json`
     - `06_fill_in_blanks.json`
     - `07_paragraph_fill.json`
     - `08_sentence_ordering.json`
     - `09_multiple_choice_closest.json`
     - `10_multiple_choice_opposite.json`
     - `11_dictionary_entry.json`
     - `12_signs_and_notices.json`
     - `13_word_families_table.json`
     - `14_word_families_mcq.json`
     - `15_word_formation.json`
     - `16_translate_sentences.json`

---

## Process & Execution Workflow

### Step 1: Run the Vocab PDF Builder Script
Execute the bundled Python script in PowerShell or terminal:

```powershell
python .agent/skills/skills-vocab-pdf/scripts/build_vocab_pdf.py <path_to_unit_or_vocab_folder>
```

#### Examples:
```powershell
# For Unit 1:
python .agent/skills/skills-vocab-pdf/scripts/build_vocab_pdf.py lessons/unit-1

# For Unit 2:
python .agent/skills/skills-vocab-pdf/scripts/build_vocab_pdf.py lessons/unit-2

# For Unit 3:
python .agent/skills/skills-vocab-pdf/scripts/build_vocab_pdf.py lessons/unit-3
```

#### Optional CLI Arguments:
- `--output-pdf` or `-op`: Custom path for target `.pdf` file.
- `--output-html` or `-oh`: Custom path for target `.html` file.
- `--no-answers`: Generate pure student workbook without Answer Key appendix.
- `--browser`: Explicit path to Chrome or Edge executable (auto-detected if omitted).

---

## Publication & Layout Standards

### 1. Document Structure & Header Standards
- **Header Title**:
  - Badge: `GLOBAL SUCCESS 12 • UNIT <N>`
  - Main Title: `Unit <N> [<ĐỀ MỤC IN HOA>]` (e.g. `Unit 1 [LIFE STORIES WE ADMIRE]`)
  - Accent Divider: Linear gradient navy rule.
- **Section I**:
  - Title: `I. VOCABULARY`
  - Subtitle: *Hệ thống từ vựng trọng tâm theo chủ đề kèm phiên âm chuẩn, định nghĩa và ngữ cảnh minh hoạ*
- **Section II**:
  - Title: `II. EXERCISES`
  - Subtitle: *Hệ thống 16 dạng bài tập củng cố và phát triển năng lực từ vựng toàn diện*
- **Section III**:
  - Title: `III. ANSWER KEY & EXPLANATIONS`
  - Subtitle: *Bảng đáp án và lời giải chi tiết cho 16 dạng bài tập*

### 2. Strictly Zero Awkward Page Breaks ("Không Ngắt Trang Bừa Bãi")
- **`break-inside: avoid !important; page-break-inside: avoid !important;`** applied to:
  - Every vocabulary card (`.vocab-book-card`).
  - Every multiple choice question item (`.book-q-item`).
  - Every dialogue box (`.dialogue-q-item`).
  - Every picture card (`.pic-to-word-card`).
  - Every dictionary entry (`.oxford-book-entry`).
  - Every sign & notice card (`.sign-q-item`).
  - Every table and word box (`.table-container-book`, `.word-box-book`).
  - Every paragraph passage (`.paragraph-card-book`).
- **`break-after: avoid !important;`** applied to:
  - Headers (`h1`, `h2`, `h3`, `h4`, `.book-header`, `.exercise-header`, `.vocab-group-header`).
  - Prevents orphan headers appearing alone at the bottom of a page without content.
- **Continuous Natural Flow**:
  - Content flows naturally from section to section without unnecessary forced page breaks.
  - Only the Answer Key section begins cleanly on a fresh page (`page-break-before: always;`).

### 3. Textbook Colors & Typography ("Màu Sắc Giống Cuốn Sách")
- **Palette**:
  - Primary Navy: `#1e3a8a` (Unit titles, section titles, headers, badge borders)
  - Secondary Royal Blue: `#2563eb` (Exercise badges, question numbers, IPA, link accents)
  - Body Slate: `#1e293b` (primary question text) and `#334155` (descriptions, definitions)
  - Subtle Callouts: `#f8fafc` and `#eff6ff` (card containers, word boxes)
  - Crisp Borders: `#cbd5e1` and `#e2e8f0` (clean, thin, ink-friendly vector lines)
- **Typography**:
  - Headers: `Plus Jakarta Sans`, 700 / 800 bold.
  - Body: `Be Vietnam Pro`, 400 / 500 / 600 with full Vietnamese diacritics support.
- **Running Headers & Footers**:
  - Top Left: `GLOBAL SUCCESS 12 • UNIT <N>`
  - Top Right: `[THEME NAME]`
  - Bottom Left: `VOCABULARY & PRACTICE EXERCISES`
  - Bottom Right: Dynamic page numbering `Page X of Y` via CSS Paged Media `@page`.

### 4. Elements Formatting for 16 Exercise Types
- **Multiple Choice (01, 02, 09, 10, 14)**:
  - Options dynamically balance into 4 columns (short words), 2 columns (phrases), or 1 column (long sentences).
  - Target words in synonym/antonym exercises are bold and underlined.
- **Dialogue MCQ (03)**:
  - Clean dialogue callout box with navy speaker tags (`Speaker A:`, `Speaker B:`).
- **Picture to Word (04)**:
  - 4-column balanced grid with responsive CSS dotted handwriting lines (`.hw-line`).
- **Write English Words (05)**:
  - 2 balanced columns with flex handwriting lines extending to the margins.
- **Word Boxes (06, 07)**:
  - Soft light blue dashed callout containers with rounded word chips.
- **Sentence Ordering (08)**:
  - Numbered list `a.`, `b.`, `c.`, `d.`, `e.` with 4-column option letters.
- **Dictionary Entries (11)**:
  - Oxford/Cambridge dictionary styled box: headword, POS pill, IPA pill, bold definition, collocations, and practice questions.
- **Signs & Notices (12)**:
  - Bordered sign board card with sign text description, accompanied by question stem and choices.
- **Word Families Table (13)**:
  - Navy header, clean borders, zebra-striped rows for Base Word, Verb, Noun, Adjective, Adverb.
- **Word Formation (15)**:
  - Sentences with underlined handwriting gaps and base words in bold capital tags `(ADMIRE)`.
- **Translation (16)**:
  - Vietnamese prompt accompanied by 2 full-width vector ruled dotted handwriting lines.

---

## Output Deliverables
Running the skill produces:
1. `lessons/unit-<N>/vocab/vocab_unit<N>.html`: The styled HTML book.
2. `lessons/unit-<N>/vocab/vocab_unit<N>.pdf`: The publication-grade PDF ready for printing or digital distribution.
