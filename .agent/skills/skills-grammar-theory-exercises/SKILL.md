---
name: grammar_theory_exercises
description: Use this skill when the user asks to display, generate, or view grammar theory and practice exercises formatted strictly according to the textbook layout specification (Lesson header with top blue accent line, pill badges for subtopics, dark navy #1e3a8a tables with bold blue highlighted structures, amber ⚠ WATCH OUT! warning boxes, and exercises A–H based on unit grammar exercises with italic instructions and dotted blanks). It generates standalone interactive HTML lessons (grammar_unit<N>.html) and updates index.html to include a dedicated Grammar section for every Unit.
---

# Grammar Theory & Exercises Portal Skill (`grammar_theory_exercises`)

## Role & Purpose
You are an expert digital curriculum engineer, senior English textbook typographer, and educational UI specialist. Your mission is to generate and maintain a publication-grade, interactive Grammar Theory & Exercises presentation system for Vietnam's **Global Success 10–12** curriculum (Units 1–10).

This skill produces:
1. **Lý Thuyết Ngữ Pháp (Grammar Theory)**: Formatted strictly according to the visual design of the official textbook layout:
   - **Header**: Top blue accent line (`border-top: 3px solid #1e40af`) with centered, bold uppercase lesson title (`LESSON <N> – <GRAMMAR TOPIC>`).
   - **Pill Section Badges**: Rounded badge (`border-radius: 9999px`, background `#e0f2fe`, border `1.5px solid #38bdf8`, color `#0369a1`) introducing each grammar subtopic.
   - **Introductory Bullets**: Clear pedagogical bullet points with bold and italicized examples.
   - **Contrastive / Rule Tables**: Deep Navy `#1e3a8a` header background, crisp white text, clean borders, with target grammatical items highlighted in bold blue (`color: #1d4ed8; font-weight: 700;`).
   - **⚠ WATCH OUT! Alert Boxes**: Amber callout box (background `#fffbeb`, border `#fde047`, left accent line `#f59e0b`, bold amber header `⚠ WATCH OUT!`) highlighting exceptions, common pitfalls, and contrastive notes.
2. **Hệ Thống Bài Tập Ngữ Pháp (Practice Exercises A–H)**:
   - Exercises structured with bold blue section letters (**A**, **B**, **C**, **D**, **E**, **F**, **G**, **H**).
   - Bold exercise title followed by an italicized sub-instruction (`*Apply tense backshift rules. Remember exceptions...*`).
   - Questions numbered sequentially (1, 2, 3...).
   - Dotted underline handwriting blanks (`. . . . . . . . . . . . . . . . . . . .`) and bracketed prompts `(not / want)`.
   - Built directly from the unit's 8 exercise files under `lessons/unit-<N>/grammar/exercises/` or `grammar_raw.json`:
     - **Exercise A**: `02_verbform.json` (Verb Form & Sentence Completion)
     - **Exercise B**: `01_mcq.json` (Multiple Choice Questions)
     - **Exercise C**: `03_matching.json` (Match the Sentence Halves)
     - **Exercise D**: `04_rewrite.json` (Sentence Transformation & Rewriting)
     - **Exercise E**: `05_guided_cloze.json` (Guided Cloze Reading Passages)
     - **Exercise F**: `06_error_identification.json` (Error Identification & Correction)
     - **Exercise G**: `07_sentence_combination.json` (Sentence Combination)
     - **Exercise H**: `08_sentence_building.json` (Sentence Building from Cues)
   - Dual modes: **Làm Bài (Practice Mode)** with interactive inputs and instant evaluation ("Kiểm Tra"), and **Xem Đáp Án (Review Mode)** with correct answers and detailed Vietnamese pedagogical explanations.
3. **Tích Hợp `index.html` (Unified Portal Integration)**:
   - Adds a dedicated **Ngữ Pháp (Grammar)** section and navigation tab to `index.html`.
   - Supports seamless Unit switching (Unit 1, Unit 2, Unit 3) across both Vocabulary and Grammar.
   - Generates standalone lesson pages: `lessons/unit-<N>/grammar_unit<N>.html`.

---

## When to Use This Skill
Activate this skill when:
- The user requests: *"Tạo skills hiển thị grammar theo cấu trúc giống như ảnh/phía trên"*, *"bổ sung grammar vào index.html cho từng unit"*, *"hiển thị bài tập grammar"*, or *"tạo trang grammar_unit*.html"*.
- The user provides images of the grammar textbook layout (Blue header line, Pill badges, Navy `#1e3a8a` tables, `⚠ WATCH OUT!` callouts, Exercise sections A-H with dotted blanks).
- The user wants exercises to be grounded in `lessons/unit-*/grammar/exercises/` (`01_mcq.json` to `08_sentence_building.json`).

---

## Target Inputs & Data Structure

### 1. Grammar Theory Database
Located at: `.agent/skills/skills-grammar-theory-exercises/reference/grammar_theory_database.json`
Contains structured sections, pill badge titles, introductory bullet points, contrastive tables with `<span class="grammar-hl">` highlights, and `watch_out` warning boxes for each Unit.

### 2. Grammar Exercise Datasets
Located at: `lessons/unit-<N>/grammar/exercises/`
- `01_mcq.json`: 20 multiple choice questions with options, answer, and explanation.
- `02_verbform.json`: 20 verb conjugation items with bracketed prompts and dotted blanks.
- `03_matching.json`: 10 sentence halves pairs (1–10 to A–J).
- `04_rewrite.json`: 10 sentence transformation questions with cues and acceptable answers.
- `05_guided_cloze.json`: 2 authentic discourse reading passages with 20 numbered blanks each.
- `06_error_identification.json`: 10 national-exam style error identification questions with bracketed segments `[A: ...] [B: ...] [C: ...] [D: ...]`.
- `07_sentence_combination.json`: 10 sentence combination pairs with connector cues.
- `08_sentence_building.json`: 10 cue-chain sentence building questions.

---

## Process & Execution Workflow

### Step 1: Run the Unified Portal & Grammar Generator Script
Execute the Python script in PowerShell:
```powershell
# Generate for all units and update index.html + standalone files:
python .agent/skills/skills-grammar-theory-exercises/scripts/build_grammar_portal.py --all

# Or generate for a specific unit (e.g. Unit 1):
python .agent/skills/skills-grammar-theory-exercises/scripts/build_grammar_portal.py --unit 1
```

### Script CLI Arguments:
- `--all`: Compiles all available units into `index.html` and produces individual `grammar_unit<N>.html` files.
- `--unit <N>`: Specifies target unit (1, 2, 3, etc.).
- `--output <path>`: Specifies custom output path for `index.html` (default: `index.html` at workspace root).

---

## Visual & Pedagogical Standards (Image-Aligned)

### 1. Theory Presentation
| Component | Visual Specification | CSS / Styling Rules |
|---|---|---|
| **Top Accent Line** | Solid blue top border | `border-top: 3px solid #1e40af;` |
| **Lesson Title** | Centered uppercase bold title | `font-family: 'Plus Jakarta Sans'; font-size: 24px; font-weight: 800; color: #1e3a8a; letter-spacing: 0.5px; text-align: center;` |
| **Pill Section Badge** | Rounded badge with light blue background | `border-radius: 9999px; background: #e0f2fe; border: 1.5px solid #38bdf8; color: #0369a1; padding: 6px 18px; font-weight: 700; font-size: 14.5px;` |
| **Intro Bullets** | Clean list with bold/italic examples | `color: #334155; line-height: 1.6; margin: 10px 0 14px 20px;` |
| **Grammar Table** | Deep Navy header, crisp alternating rows | Header `background: #1e3a8a; color: #ffffff; font-weight: 700;`. Alternating row `background: #f8fafc;`. Target words: `<span class="grammar-hl">` (`color: #1d4ed8; font-weight: 700;`). |
| **⚠ WATCH OUT! Box** | Amber callout box with icon | Background `#fffbeb; border: 1px solid #fde047; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 14px 18px;`. Header in bold `#b45309;`. |

### 2. Exercise Presentation
| Component | Visual Specification | CSS / Styling Rules |
|---|---|---|
| **Section Letter** | Bold uppercase letter | Blue `#1e40af`, font-size: 18px, font-weight: 800. |
| **Exercise Title** | Bold title in `#0f172a` | `font-size: 16px; font-weight: 700; margin-left: 8px;` |
| **Sub-instruction** | Italic pedagogical guidance | `color: #475569; font-style: italic; font-size: 13.5px; margin: 4px 0 16px 0;` |
| **Dotted Blanks** | Dotted underline handwriting style | `border: none; border-bottom: 2px dotted #1e40af; background: transparent; padding: 2px 8px; font-weight: 600; color: #1e40af; text-align: center;` |
| **Interactive Controls** | Check Answers, Review, Explanations | Instant score calculation, green checkmarks for correct answers, red highlights with correct model answers for errors, expandable Vietnamese pedagogical explanations. |

---

## Deliverables Checklist
1. `index.html`: Contains the unified portal with dynamic Unit switching, Vocabulary Theory Flashcards, 16 Vocab Exercises, and the new **Grammar Theory & 8 Exercises** section for every unit.
2. `lessons/unit-<N>/grammar_unit<N>.html`: Dedicated standalone, responsive grammar lesson pages.
3. `.agent/skills/skills-grammar-theory-exercises/`: Reusable, modular skill directory containing scripts, references, and documentation.
