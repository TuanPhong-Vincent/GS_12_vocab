---
name: vocab_theory_exercises
description: Use this skill when the user asks to display or generate vocabulary theory and practice exercises into a unified index.html and cards.html. It formats vocabulary theory per the modern cards.html specification (Modern Blue grid, audio button, contain images, IPA, and meanings) and neatly organizes all 16 exercise types from unit-*/vocab/exercises into a clean, publication-grade page with uniform title colors, relative element alignment, live search, and dual Review/Practice modes.
---

# Vocabulary Theory & Exercises Portal Skill (`vocab_theory_exercises`)

## Role & Purpose
You are an expert digital curriculum engineer and educational UI specialist. Your mission is to generate a state-of-the-art, responsive, unified HTML web portal (`index.html`) and standalone flashcards (`cards.html`) for any Unit in Global Success (10–12):
1. **Lý thuyết từ vựng (Vocabulary Theory)**: Formatted strictly according to the modern card design in `cards.html` (Google Fonts: *Plus Jakarta Sans* & *Be Vietnam Pro*, Modern Blue palette `#2563eb`, 4–5 cards per row grid, contain image frame, floating audio button, IPA, and Vietnamese definitions).
2. **Bài tập từ vựng (Practice Exercises)**: Formats all 16 exercise JSON files from `unit-*/vocab/exercises` into neat, orderly cards with **uniform title colors** (`#1e3a8a` / `#2563eb`), aligned elements, interactive answer checks, scoring, and live search.

---

## When to Use This Skill
Activate this skill when:
- The user requests: *"Tạo skills hiển thị lý thuyết từ vựng và bài tập từ vựng"*, *"tạo index.html chứa lý thuyết và bài tập"*, or *"hiển thị bài tập và cards.html"*.
- The user provides `cards.html` as the design standard for vocabulary theory and exercise JSONs under `unit-*/vocab/exercises` or `lessons/unit-*/vocab/exercises`.
- The user wants a clean, publication-grade web page with consistent title styling and proportionally aligned elements.

---

## Target Inputs
1. **Lý thuyết từ vựng**:
   - `vocab.json` (under `unit-*/vocab/` or `lessons/unit-*/vocab/`): Contains words, British/American IPA, Vietnamese definitions, example sentences, and image paths.
   - `cards.html`: The UI card system and design standard (Modern Blue gradient, soft radius, audio button, typography).
2. **Hệ thống bài tập**:
   - `unit-*/vocab/exercises/` (or `lessons/unit-*/vocab/exercises/`): All 16 exercise files (`01_multiple_choice_direct.json` through `16_translate_sentences.json`).

---

## Process & Execution Workflow

### Step 1: Run the Unified Index Builder Script
Execute the bundled Python script in PowerShell:
```powershell
python .agent/skills/skills-vocab-theory-exercises/scripts/build_vocab_index.py <path_to_unit_or_vocab_folder>
```

#### Example Usage:
```powershell
# For Unit 1:
python .agent/skills/skills-vocab-theory-exercises/scripts/build_vocab_index.py lessons/unit-1/vocab

# For Unit 2:
python .agent/skills/skills-vocab-theory-exercises/scripts/build_vocab_index.py lessons/unit-2/vocab
```

#### Custom Destination Options:
- `--output-index` or `-oi`: Custom path for `index.html`.
- `--output-cards` or `-oc`: Custom path for `cards.html`.

By default, the script generates both in the **workspace root** (e.g., `d:/GS12/index.html` & `d:/GS12/cards.html`) and inside the unit's vocab folder (`lessons/unit-X/vocab/index.html` & `cards.html`).

---

## Key Features & UI Standards

### 1. Lý Thuyết Từ Vựng (Strict `cards.html` Spec)
- **Grid Layout**: 5 cards/row on wide screens (>=1320px), 4 cards/row on laptops (1024px–1319px), responsive auto-fill on mobile.
- **Image Container**: Height 200px, background `#f8fafc`, `object-fit: contain` (no clipping, no distorted zooming), border-radius 12px.
- **Audio Speaker**: Circular floating button at bottom-right of image with SVG speaker; speaks clear American English pronunciation via Web Speech API.
- **Typography & Meta**:
  - English word: `Plus Jakarta Sans`, 21px, bold, title case/lowercase (no harsh uppercase).
  - IPA transcription: 14px in soft blue `#3b82f6`.
  - Divider: 1px subtle linear gradient.
  - Vietnamese definition: 15px, semi-bold `#334155`.

### 2. Bài Tập Từ Vựng (Neat & Harmonious)
- **Màu Sắc Đồng Nhất (Uniform Title Colors)**:
  - All 16 exercise titles share the exact same Deep Navy `#1e3a8a` heading color and `Plus Jakarta Sans` font.
  - Number badges share a soft blue pill style (`#eff6ff` background, `#2563eb` border/text).
  - Exercise type pills use consistent `#f1f5f9` backgrounds with `#475569` text.
- **Sắp Xếp Elements Tương Đối (Balanced Alignment)**:
  - **Multiple Choice**: Options are aligned in a 2-column balanced grid on desktop, 1-column on mobile.
  - **Inputs & Blanks**: Uniform heights (`38px`), rounded corners (`8px`), and gentle focus rings.
  - **Word Boxes**: Cohesive blue gradient container with rounded word chips.
  - **Tables**: Responsive zebra-striped table for Word Families with base word chips.
  - **Signs & Notices**: Clean sign board card with balanced choice buttons.

### 3. Dual Modes & Controls
- **Tab Switcher**: Quick toggle between `[📚 Tất Cả]`, `[💡 Lý Thuyết (Cards)]`, and `[✍️ Bài Tập (16 Dạng)]`.
- **Review Mode (Xem Đáp Án)**: Highlights correct choices in green checkmarks, displays standard answers.
- **Practice Mode (Làm Bài)**: Allows learners to interact, fill blanks, select radios, and click **"Kiểm Tra"** on each exercise or globally for instant percentage scores.
- **Live Search**: Instant real-time filter across both vocabulary cards and exercise questions.
- **Print / PDF Friendly**: Clean print media styles hiding interactive controls for physical handouts.

---

## Output Files
- `index.html`: Unified portal containing both Vocabulary Theory (cards) and all 16 Practice Exercises.
- `cards.html`: Dedicated, standalone vocabulary flashcards page.
