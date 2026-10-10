#!/usr/bin/env python3
"""
Textbook-Grade Print-Optimized PDF HTML Builder for Global Success (Master Publication Edition)
Strict 11-page publication standard for Global Success:
- Page 1: Top Header + Part I: Categories 1 & 2 (22 words)
- Page 2: Part I: Categories 3, 4, 5, 6 (24 words)
- Page 3: Part II: Exercises 1 & 2 (20 items in 2 columns)
- Page 4: Exercises 3 & 4 (10 dialogues in 2 cols + 20 pictures in 4 cols x 5 rows)
- Page 5: Exercises 5, 6, 7 (Part 1 - Passage Text)
- Page 6: Exercises 7 (Part 2 - Answer Slots), 8, 9
- Page 7: Exercises 10 & 11 (Antonyms + Dictionary Entries)
- Page 8: Exercise 12 (Real-World Signs & Notices - All 10 signs)
- Page 9: Exercises 13, 14, 15 (Word Families Table + Word Form MCQ + Word Formation)
- Page 10: Exercise 16 (Sentence Translation - 10 Vietnamese sentences, 2 dotted rules each)
- Page 11: Part III: Master Answer Key (4 balanced columns)
"""

import os
import sys
import json
import glob
import re
from pathlib import Path
from html import escape

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def highlight_target_word(text):
    if not text:
        return ""
    return re.sub(r"\[([^\]]+)\]", r"<u><b>\1</b></u>", escape(text))


def resolve_image_path(raw_path, base_output_dir, workspace_root, unit_name):
    if not raw_path:
        return ""
    clean = raw_path.lstrip("/\\")
    
    # 1. Check in lessons/<unit>/vocab/exercises/images/
    if clean.startswith("images/") and not (workspace_root / clean).exists():
        potential = workspace_root / "lessons" / unit_name / "vocab" / "exercises" / clean
        if potential.exists():
            return os.path.relpath(potential, base_output_dir).replace("\\", "/")
        potential2 = workspace_root / "lessons" / unit_name / "vocab" / clean
        if potential2.exists():
            return os.path.relpath(potential2, base_output_dir).replace("\\", "/")

    # 2. Check direct relative from workspace
    target = workspace_root / clean
    if target.exists():
        return os.path.relpath(target, base_output_dir).replace("\\", "/")

    # 3. Check directly in unit images
    potential3 = workspace_root / "lessons" / unit_name / "vocab" / "images" / os.path.basename(clean)
    if potential3.exists():
        return os.path.relpath(potential3, base_output_dir).replace("\\", "/")

    return raw_path


BOOK_EXERCISE_TITLES = {
    "1": "Vocabulary Identification",
    "2": "Sentence Completion",
    "3": "Everyday Conversations",
    "4": "Picture Vocabulary",
    "5": "Word Recall & Definitions",
    "6": "Word Box Sentences",
    "7": "Passage Completion",
    "8": "Sentence Ordering",
    "9": "Synonyms & Closest Meaning",
    "10": "Antonyms & Opposite Meaning",
    "11": "Dictionary Skills & In-Context Usage",
    "12": "Real-World Signs & Notices",
    "13": "Word Families Chart",
    "14": "Word Form Choice",
    "15": "Word Formation Practice",
    "16": "Sentence Translation",
}

BOOK_EXERCISE_GUIDES = {
    "1": "Choose the best answer (A, B, C, or D) to complete each definition or question:",
    "2": "Choose the most appropriate word or phrase to complete each sentence:",
    "3": "Complete each daily conversation with the most suitable response:",
    "4": "Look at the pictures and write the correct English word under each image:",
    "5": "Write the English words that match the Vietnamese definitions below:",
    "6": "Fill in each blank with an appropriate word from the box:",
    "7": "Read the passage carefully and fill in each blank with a suitable word from the box:",
    "8": "Put the sentences in the correct order to form a logical conversation or paragraph:",
    "9": "Choose the word or phrase that is CLOSEST in meaning to the underlined word:",
    "10": "Choose the word or phrase that is OPPOSITE in meaning to the underlined word:",
    "11": "Study the dictionary entries and complete the practice sentences:",
    "12": "Look at each sign or notice and choose the best explanation (A, B, C, or D):",
    "13": "Study the word families chart and complete the missing forms:",
    "14": "Choose the correct form of the word to complete each sentence:",
    "15": "Supply the correct form of the word in brackets to complete each sentence:",
    "16": "Translate the following Vietnamese sentences into natural English:",
}


def render_vocab_card_html(w, base_output_dir, workspace_root, unit_name, is_page1=False):
    word_en = w.get("english_word", "").strip()
    ipa_uk = w.get("pronunciation_british", "").strip()
    ipa_us = w.get("pronunciation_american", "").strip()
    ipa = ipa_us or ipa_uk
    meaning_raw = w.get("vietnamese_meaning", "").strip()

    pos = ""
    m_pos = re.match(r"^\(([a-zA-Z\s,./]+)\)\s*:?\s*(.*)$", meaning_raw)
    if m_pos:
        pos = f"({m_pos.group(1).strip()})"
        meaning = m_pos.group(2).strip()
    else:
        meaning = meaning_raw

    colloc = w.get("collocation", "").strip()
    if "," in colloc:
        colloc_parts = [c.strip() for c in colloc.split(",") if c.strip()]
        colloc_short = ", ".join(colloc_parts[:2])
    else:
        colloc_short = colloc

    img_raw = w.get("image", "")
    img_rel = resolve_image_path(img_raw, base_output_dir, workspace_root, unit_name)

    colloc_span = f"<span class='v-colloc'>• {escape(colloc_short)}</span>" if colloc_short else ""
    extra_cls = "p1-cell" if is_page1 else "p2-cell"

    return f"""
    <div class="vocab-grid-cell {extra_cls}">
        <div class="v-img-frame">
            <img src="{escape(img_rel)}" alt="{escape(word_en)}" onerror="this.style.opacity='0.2';">
        </div>
        <div class="v-content-block">
            <div class="v-word-line">
                <span class="v-word-text">{escape(word_en)}</span>
                <span class="v-pos-text">{escape(pos)}</span>
            </div>
            <div class="v-ipa-text">{escape(ipa)}</div>
            <div class="v-mean-text">{escape(meaning)}</div>
            {colloc_span}
        </div>
    </div>"""


def render_vocab_pages_dynamic(vocab_data, base_output_dir, workspace_root, book_title, unit_heading, unit_name):
    """
    Renders all vocabulary words grouped into authentic categories on Page 1 & Page 2:
    - Page 1: Top Header + Part I: Categories 1 & 2 (22 words)
    - Page 2: Running Header + Part I: Categories 3, 4, 5, 6 (24 words)
    """
    total_groups = len(vocab_data)
    total_words = sum(len(g.get("words", [])) for g in vocab_data)
    
    if total_groups == 3:
        p1_groups = [vocab_data[0]]
        p2_groups = vocab_data[1:]
    elif total_groups >= 4:
        p1_groups = []
        p2_groups = []
        cum_words = 0
        for g in vocab_data:
            w_cnt = len(g.get("words", []))
            if cum_words + w_cnt <= (total_words * 0.52) and len(p1_groups) < total_groups - 1:
                p1_groups.append(g)
                cum_words += w_cnt
            else:
                p2_groups.append(g)
    else:
        p1_groups = vocab_data[:1]
        p2_groups = vocab_data[1:]

    # Build Page 1 Categories
    p1_cats_html = []
    cat_counter = 1
    for g in p1_groups:
        grp_name = g.get("group", f"Group {cat_counter}").upper()
        words = g.get("words", [])
        cards = [render_vocab_card_html(w, base_output_dir, workspace_root, unit_name, is_page1=True) for w in words]
        block = f"""
        <div class="category-header-wrap">
            <h3 class="category-title-blue">CATEGORY {cat_counter}: {escape(grp_name)} ({len(words)} words)</h3>
        </div>
        <div class="vocab-3col-grid page1-grid">
            {''.join(cards)}
        </div>"""
        p1_cats_html.append(block)
        cat_counter += 1

    page1_html = f"""
    <!-- TRANG 1: HEADER & CORE VOCABULARY -->
    <div class="textbook-sheet page-1-vocab" id="page-1">
        <header class="sheet-top-header">
            <div class="header-titles">
                <h1 class="unit-main-heading">{escape(book_title)}</h1>
                <div class="unit-sub-heading">{escape(unit_heading)}</div>
                <div class="unit-topic-tag">CORE VOCABULARY & PRACTICE WORKBOOK</div>
            </div>
            <div class="student-info-strip">
                <div class="si-item"><b>Full Name:</b> ............................................................</div>
                <div class="si-item"><b>Class:</b> .................. &nbsp;&nbsp; <b>Date:</b> ....................</div>
            </div>
        </header>

        <div class="section-title-wrap">
            <h2 class="section-heading-blue">PART I: CORE VOCABULARY</h2>
            <div class="section-instruction-orange">Study the core words, pronunciations, meanings, and collocations:</div>
        </div>

        {''.join(p1_cats_html)}
    </div>
    """

    # Build Page 2 Categories
    p2_cats_html = []
    for g_idx, g in enumerate(p2_groups):
        grp_name = g.get("group", f"Group {cat_counter}").upper()
        words = g.get("words", [])
        cards = [render_vocab_card_html(w, base_output_dir, workspace_root, unit_name, is_page1=False) for w in words]
        sep_gap = "<div class='cat-separation-gap'></div>" if g_idx > 0 else ""
        block = f"""
        {sep_gap}
        <div class="category-header-wrap" style="margin-top: 4px;">
            <h3 class="category-title-blue">CATEGORY {cat_counter}: {escape(grp_name)} ({len(words)} words)</h3>
        </div>
        <div class="vocab-3col-grid page2-grid-cat">
            {''.join(cards)}
        </div>"""
        p2_cats_html.append(block)
        cat_counter += 1

    page2_html = f"""
    <!-- TRANG 2: CÁC CATEGORIES TIẾP THEO -->
    <div class="textbook-sheet page-2-vocab page-break" id="page-2">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART I: CORE VOCABULARY (CONT.)</span>
        </header>

        {''.join(p2_cats_html)}
    </div>
    """

    return page1_html + "\n" + page2_html


def render_exercises_continuous_stream(exercises_list, base_output_dir, workspace_root, book_title, unit_heading, unit_name):
    """
    Renders all 16 exercises with strict 11-page allocation:
    - Page 3: Ex 1 & Ex 2 (starts with page-break)
    - Page 4: Ex 3 & Ex 4 (Ex 3 has page-break)
    - Page 5: Ex 5, Ex 6, Ex 7 (Part 1 - Text) (Ex 5 has page-break)
    - Page 6: Ex 7 (Part 2 - Slots), Ex 8, Ex 9 (Page 6 anchor has page-break)
    - Page 7: Ex 10 & Ex 11 (Ex 10 has page-break)
    - Page 8: Ex 12 (Ex 12 has page-break)
    - Page 9: Ex 13, 14, 15 (Ex 13 has page-break)
    - Page 10: Ex 16 (Ex 16 has page-break)
    """
    html_chunks = []

    # Map exercise files by number
    ex_dict = {}
    for ex in exercises_list:
        # Detect number from filename or id
        t = ex.get("type", "")
        ex_dict[t] = ex

    # Find each exercise by expected type
    def get_ex(num, fallback_idx):
        type_map = {
            1: "multiple_choice",
            2: "multiple_choice",
            3: "multiple_choice",
            4: "pic_to_word",
            5: "write_english_words",
            6: "fill_in_blanks",
            7: "paragraph_fill",
            8: "sentence_ordering_multiple_choice",
            9: "multiple_choice",
            10: "multiple_choice",
            11: "dictionary_entry",
            12: "signs_and_notices",
            13: "word_families_table",
            14: "word_families_mcq",
            15: "word_formation",
            16: "translate_sentences"
        }
        if fallback_idx < len(exercises_list):
            return exercises_list[fallback_idx]
        return {}

    # === PAGE 3: EXERCISES 1 & 2 ===
    ex1 = get_ex(1, 0)
    ex2 = get_ex(2, 1)
    body_ex1 = render_single_exercise_open(ex1, 1, ex1.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex2 = render_single_exercise_open(ex2, 2, ex2.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 3: BÀI TẬP 1 & 2 -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-3-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES</span>
        </header>

        <div class="section-title-wrap" style="margin-top: 6px; margin-bottom: 4px;">
            <h2 class="section-heading-blue">PART II: PRACTICE EXERCISES</h2>
            <div class="section-instruction-orange">Complete all 16 exercises based on Unit core vocabulary:</div>
        </div>

        <div class="exercise-open-section" id="ex-1">
            <h3 class="ex-heading-blue">Exercise 1: {escape(BOOK_EXERCISE_TITLES.get('1',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('1',''))}</div>
            <div class="ex-open-content">{body_ex1}</div>
        </div>

        <div class="exercise-open-section" id="ex-2">
            <h3 class="ex-heading-blue">Exercise 2: {escape(BOOK_EXERCISE_TITLES.get('2',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('2',''))}</div>
            <div class="ex-open-content">{body_ex2}</div>
        </div>
    </div>
    """)

    # === PAGE 4: EXERCISES 3 & 4 ===
    ex3 = get_ex(3, 2)
    ex4 = get_ex(4, 3)
    body_ex3 = render_single_exercise_open(ex3, 3, ex3.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex4 = render_single_exercise_open(ex4, 4, ex4.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 4: BÀI TẬP 3 & 4 -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-4-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-3">
            <h3 class="ex-heading-blue" style="margin-top: 4px;">Exercise 3: {escape(BOOK_EXERCISE_TITLES.get('3',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('3',''))}</div>
            <div class="ex-open-content">{body_ex3}</div>
        </div>

        <div class="exercise-open-section" id="ex-4">
            <h3 class="ex-heading-blue">Exercise 4: {escape(BOOK_EXERCISE_TITLES.get('4',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('4',''))}</div>
            <div class="ex-open-content">{body_ex4}</div>
        </div>
    </div>
    """)

    # === PAGE 5: EXERCISES 5, 6, 7 (PART 1 - TEXT) ===
    ex5 = get_ex(5, 4)
    ex6 = get_ex(6, 5)
    ex7 = get_ex(7, 6)
    body_ex5 = render_single_exercise_open(ex5, 5, ex5.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex6 = render_single_exercise_open(ex6, 6, ex6.get("type",""), base_output_dir, workspace_root, unit_name)
    
    # Ex 7 Part 1: Word Box + Passage Text
    ex7_word_box = ex7.get("word_box", [])
    ex7_chips = " &nbsp;•&nbsp; ".join(f"<b>{escape(w)}</b>" for w in ex7_word_box)
    ex7_parts = ex7.get("paragraph_parts", [])
    ex7_flow_spans = []
    ex7_slots = []
    b_cnt = 0
    for part in ex7_parts:
        if isinstance(part, str):
            ex7_flow_spans.append(f"<span>{escape(part)}</span>")
        elif isinstance(part, dict) and part.get("type") == "blank":
            b_id = part.get("id", str(b_cnt + 1))
            b_correct = part.get("correct_answer", "").strip()
            ex7_flow_spans.append(
                f"<span class='para-slot-inline'><b>({b_id})</b> .....................<span class='teacher-key-line'>[<b>{escape(b_correct)}</b>]</span></span>"
            )
            ex7_slots.append(
                f"<div class='slot-cell'><b>({b_id})</b> <span class='open-dotted-line'>..........................</span><span class='teacher-key-line'> ➔ <b>{escape(b_correct)}</b></span></div>"
            )
            b_cnt += 1

    html_chunks.append(f"""
    <!-- TRANG 5: BÀI TẬP 5, 6 & 7 (PART 1 - ĐOẠN VĂN) -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-5-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-5">
            <h3 class="ex-heading-blue" style="margin-top: 4px;">Exercise 5: {escape(BOOK_EXERCISE_TITLES.get('5',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('5',''))}</div>
            <div class="ex-open-content">{body_ex5}</div>
        </div>

        <div class="exercise-open-section" id="ex-6">
            <h3 class="ex-heading-blue">Exercise 6: {escape(BOOK_EXERCISE_TITLES.get('6',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('6',''))}</div>
            <div class="ex-open-content">{body_ex6}</div>
        </div>

        <div class="exercise-open-section" id="ex-7-part1">
            <h3 class="ex-heading-blue">Exercise 7: {escape(BOOK_EXERCISE_TITLES.get('7',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('7',''))}</div>
            <div class="ex-open-content">
                <div class="open-word-box">
                    <b>WORD BOX:</b> &nbsp; {ex7_chips}
                </div>
                <div class="open-passage-block" style="margin-bottom: 0;">
                    <div class="passage-body-text">
                        {''.join(ex7_flow_spans)}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)

    # === PAGE 6: EXERCISES 7 (PART 2 - SLOTS), 8, 9 ===
    ex8 = get_ex(8, 7)
    ex9 = get_ex(9, 8)
    body_ex8 = render_single_exercise_open(ex8, 8, ex8.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex9 = render_single_exercise_open(ex9, 9, ex9.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 6: BÀI TẬP 7 (PART 2 - ANSWER SLOTS), 8, 9 -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-6-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-7-part2" style="margin-bottom: 12px;">
            <div class="ex-sub-heading-blue" style="font-weight: 800; font-size: 11pt; color: var(--c-blue); margin-top: 4px; margin-bottom: 4px;">Exercise 7 (Continued) — Write Your Answers Below:</div>
            <div class="passage-answer-grid-5">
                {''.join(ex7_slots)}
            </div>
        </div>

        <div class="exercise-open-section" id="ex-8">
            <h3 class="ex-heading-blue">Exercise 8: {escape(BOOK_EXERCISE_TITLES.get('8',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('8',''))}</div>
            <div class="ex-open-content">{body_ex8}</div>
        </div>

        <div class="exercise-open-section" id="ex-9">
            <h3 class="ex-heading-blue">Exercise 9: {escape(BOOK_EXERCISE_TITLES.get('9',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('9',''))}</div>
            <div class="ex-open-content">{body_ex9}</div>
        </div>
    </div>
    """)

    # === PAGE 7: EXERCISES 10 & 11 ===
    ex10 = get_ex(10, 9)
    ex11 = get_ex(11, 10)
    body_ex10 = render_single_exercise_open(ex10, 10, ex10.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex11 = render_single_exercise_open(ex11, 11, ex11.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 7: BÀI TẬP 10 & 11 -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-7-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-10">
            <h3 class="ex-heading-blue" style="margin-top: 4px;">Exercise 10: {escape(BOOK_EXERCISE_TITLES.get('10',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('10',''))}</div>
            <div class="ex-open-content">{body_ex10}</div>
        </div>

        <div class="exercise-open-section" id="ex-11">
            <h3 class="ex-heading-blue">Exercise 11: {escape(BOOK_EXERCISE_TITLES.get('11',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('11',''))}</div>
            <div class="ex-open-content">{body_ex11}</div>
        </div>
    </div>
    """)

    # === PAGE 8: EXERCISE 12 ===
    ex12 = get_ex(12, 11)
    body_ex12 = render_single_exercise_open(ex12, 12, ex12.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 8: BÀI TẬP 12 (BIỂN BÁO TOÀN TRANG) -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-8-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-12">
            <h3 class="ex-heading-blue" style="margin-top: 4px;">Exercise 12: {escape(BOOK_EXERCISE_TITLES.get('12',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('12',''))}</div>
            <div class="ex-open-content">{body_ex12}</div>
        </div>
    </div>
    """)

    # === PAGE 9: EXERCISES 13, 14, 15 ===
    ex13 = get_ex(13, 12)
    ex14 = get_ex(14, 13)
    ex15 = get_ex(15, 14)
    body_ex13 = render_single_exercise_open(ex13, 13, ex13.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex14 = render_single_exercise_open(ex14, 14, ex14.get("type",""), base_output_dir, workspace_root, unit_name)
    body_ex15 = render_single_exercise_open(ex15, 15, ex15.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 9: BÀI TẬP 13, 14, 15 -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-9-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-13">
            <h3 class="ex-heading-blue" style="margin-top: 4px;">Exercise 13: {escape(BOOK_EXERCISE_TITLES.get('13',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('13',''))}</div>
            <div class="ex-open-content">{body_ex13}</div>
        </div>

        <div class="exercise-open-section" id="ex-14">
            <h3 class="ex-heading-blue">Exercise 14: {escape(BOOK_EXERCISE_TITLES.get('14',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('14',''))}</div>
            <div class="ex-open-content">{body_ex14}</div>
        </div>

        <div class="exercise-open-section" id="ex-15">
            <h3 class="ex-heading-blue">Exercise 15: {escape(BOOK_EXERCISE_TITLES.get('15',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('15',''))}</div>
            <div class="ex-open-content">{body_ex15}</div>
        </div>
    </div>
    """)

    # === PAGE 10: EXERCISE 16 ===
    ex16 = get_ex(16, 15)
    body_ex16 = render_single_exercise_open(ex16, 16, ex16.get("type",""), base_output_dir, workspace_root, unit_name)

    html_chunks.append(f"""
    <!-- TRANG 10: BÀI TẬP 16 (DỊCH CÂU TOÀN TRANG) -->
    <div class="textbook-sheet exercises-sheet page-break" id="page-10-exercises">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART II: PRACTICE EXERCISES (CONT.)</span>
        </header>

        <div class="exercise-open-section" id="ex-16">
            <h3 class="ex-heading-blue" style="margin-top: 4px;">Exercise 16: {escape(BOOK_EXERCISE_TITLES.get('16',''))}</h3>
            <div class="ex-guide-orange">{escape(BOOK_EXERCISE_GUIDES.get('16',''))}</div>
            <div class="ex-open-content">{body_ex16}</div>
        </div>
    </div>
    """)

    return "\n".join(html_chunks)


def render_single_exercise_open(ex, ex_num, ex_type, base_output_dir, workspace_root, unit_name):
    questions = ex.get("questions", [])

    # 1, 2, 3, 9, 10, 14: Multiple Choice
    if ex_type in ["multiple_choice", "word_families_mcq"]:
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            options = q.get("options", [])
            correct = q.get("correct_answer", "").strip()

            if "\n" in raw_text:
                dialogue_lines = raw_text.split("\n")
                formatted_stem = "<div class='open-dialogue'>" + "".join(
                    f"<div>{highlight_target_word(line)}</div>" for line in dialogue_lines if line.strip()
                ) + "</div>"
            else:
                formatted_stem = f"<span class='stem-text'>{highlight_target_word(raw_text)}</span>"

            option_letters = ["A", "B", "C", "D"]
            opt_spans = []
            for opt_i, opt in enumerate(options):
                letter = option_letters[opt_i] if opt_i < len(option_letters) else str(opt_i + 1)
                opt_str = str(opt).strip()
                is_correct = (opt_str.lower() == correct.lower())
                correct_cls = "key-correct-target" if is_correct else ""
                check_icon = "<span class='key-check-mark'>✓</span>" if is_correct else ""

                opt_spans.append(
                    f"<span class='opt-choice {correct_cls}'><b>{letter}.</b> {escape(opt_str)}{check_icon}</span>"
                )

            item = f"""
            <div class="q-open-item avoid-break ex{ex_num}-item">
                <div class="q-line-stem">
                    <span class="q-seq-num"><b>{q_id}.</b></span>
                    <span class="q-stem-body">{formatted_stem}</span>
                </div>
                <div class="q-choices-grid">
                    {''.join(opt_spans)}
                </div>
                <div class="teacher-key-line">Key: <b>{escape(correct)}</b></div>
            </div>"""
            items.append(item)

        return f"<div class='open-2col-flow'>{''.join(items)}</div>"

    # 4. Picture to Word (04) - BIG IMAGES, NO BOXES
    elif ex_type == "pic_to_word":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            img_raw = q.get("image", "")
            img_rel = resolve_image_path(img_raw, base_output_dir, workspace_root, unit_name)
            correct = q.get("correct_answer", "").strip()

            card = f"""
            <div class="pic-open-item avoid-break">
                <div class="pic-big-frame">
                    <img src="{escape(img_rel)}" alt="Picture {q_id}" onerror="this.style.opacity='0.2';">
                </div>
                <div class="pic-label-row">
                    <span class="pic-q-num"><b>{q_id}.</b></span>
                    <span class="pic-dotted-slot"></span>
                </div>
                <div class="teacher-key-line"><b>{escape(correct)}</b></div>
            </div>"""
            items.append(card)

        return f"<div class='pic-4col-grid'>{''.join(items)}</div>"

    # 5. Write English Words (05)
    elif ex_type == "write_english_words":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            parts = q.get("parts", [])
            sub_rows = []
            for p_idx, part in enumerate(parts):
                vi = part.get("vietnamese", "").strip()
                correct = part.get("correct_answer", "").strip()
                sub = f"""
                <div class="write-sub-item">
                    <b>({chr(97 + p_idx)})</b> {escape(vi)}: <span class="open-dotted-line">................................................</span>
                    <span class="teacher-key-line">➔ <b>{escape(correct)}</b></span>
                </div>"""
                sub_rows.append(sub)

            card = f"""
            <div class="q-open-item avoid-break ex5-item">
                <div class="q-seq-num"><b>{q_id}.</b></div>
                <div class="sub-parts-wrap">
                    {''.join(sub_rows)}
                </div>
            </div>"""
            items.append(card)

        return f"<div class='open-2col-flow'>{''.join(items)}</div>"

    # 6. Fill in the Blanks (06)
    elif ex_type == "fill_in_blanks":
        word_box = ex.get("word_box", [])
        box_chips = " &nbsp;•&nbsp; ".join(f"<b>{escape(w)}</b>" for w in word_box)
        box_html = f"""
        <div class="open-word-box">
            <b>WORD BOX:</b> &nbsp; {box_chips}
        </div>"""

        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            correct = q.get("correct_answer", "").strip()

            blank_sentence = re.sub(
                r"_{2,}",
                f"<span class='blank-open-slot'>({q_id}) .........................</span><span class='teacher-key-line'> [<b>{escape(correct)}</b>]</span>",
                escape(raw_text)
            )

            item = f"""
            <div class="q-open-item avoid-break ex6-item">
                <span class="q-seq-num"><b>{q_id}.</b></span>
                <span class="q-stem-body">{blank_sentence}</span>
            </div>"""
            items.append(item)

        return box_html + f"<div class='open-2col-flow' style='margin-top: 6px;'>{''.join(items)}</div>"

    # 8. Sentence Ordering (08)
    elif ex_type == "sentence_ordering_multiple_choice":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            sentences = q.get("sentences", [])
            options = q.get("options", [])
            correct = q.get("correct_answer", "").strip()

            order_letters = ["a", "b", "c", "d", "e"]
            s_rows = []
            for s_i, s_text in enumerate(sentences):
                s_letter = order_letters[s_i] if s_i < len(order_letters) else f"{s_i+1}"
                s_rows.append(f"<div><b>({s_letter})</b> {escape(s_text)}</div>")

            option_letters = ["A", "B", "C", "D"]
            opt_spans = []
            for opt_i, opt in enumerate(options):
                letter = option_letters[opt_i] if opt_i < len(option_letters) else str(opt_i + 1)
                opt_str = str(opt).strip()
                is_correct = (opt_str.lower() == correct.lower())
                correct_cls = "key-correct-target" if is_correct else ""
                check_icon = "<span class='key-check-mark'>✓</span>" if is_correct else ""
                opt_spans.append(
                    f"<span class='opt-choice {correct_cls}'><b>{letter}.</b> {escape(opt_str)}{check_icon}</span>"
                )

            item = f"""
            <div class="q-open-item avoid-break so-item">
                <div class="so-lead"><b>{q_id}.</b> Rearrange the sentences:</div>
                <div class="so-sub-lines">{''.join(s_rows)}</div>
                <div class="so-choices-row">{''.join(opt_spans)}</div>
                <div class="teacher-key-line">Key: <b>{escape(correct)}</b></div>
            </div>"""
            items.append(item)

        return f"<div class='open-2col-flow'>{''.join(items)}</div>"

    # 11. Dictionary Entries (11)
    elif ex_type == "dictionary_entry":
        entries = ex.get("entries", [])
        cards = []
        for e_idx, entry in enumerate(entries):
            e_id = entry.get("id", str(e_idx + 1))
            word = entry.get("word", "")
            pos = entry.get("part_of_speech", "")
            pr = entry.get("pronunciation", "")
            definition = entry.get("definition", "")
            bullets = entry.get("bullet_points", [])
            q_list = entry.get("questions", [])

            short_bullets = bullets[:2] if len(bullets) > 2 else bullets
            bullet_items = "".join(f"<li>{highlight_target_word(b)}</li>" for b in short_bullets)

            q_rows = []
            for q_idx, q in enumerate(q_list):
                q_id = q.get("id", str(q_idx + 1))
                q_text = q.get("text", "")
                correct = q.get("correct_answer", "").strip()

                formatted_q = re.sub(
                    r"_{2,}",
                    f"<span class='blank-open-slot'>( {q_id} ) ............................</span><span class='teacher-key-line'> [<b>{escape(correct)}</b>]</span>",
                    escape(q_text)
                )
                q_rows.append(f"<div><b>{q_id}.</b> {formatted_q}</div>")

            card = f"""
            <div class="dict-open-entry avoid-break">
                <div class="dict-head-text">
                    <b>{escape(word)}</b> <i>({escape(pos)})</i> <span class="ipa-faded">{escape(pr)}</span>
                </div>
                <div class="dict-def-line"><b>Def:</b> {escape(definition)}</div>
                <ul class="dict-bullets-inline">{bullet_items}</ul>
                <div class="dict-sentences-box">
                    {''.join(q_rows)}
                </div>
            </div>"""
            cards.append(card)

        return f"<div class='open-2col-flow'>{''.join(cards)}</div>"

    # 12. Signs and Notices (12)
    elif ex_type == "signs_and_notices":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            sign_img_raw = q.get("sign_image", "")
            sign_img_rel = resolve_image_path(sign_img_raw, base_output_dir, workspace_root, unit_name)
            sign_text = q.get("sign_text", "")
            q_stem = q.get("question", "What does this sign mean?")
            options = q.get("options", [])
            correct = q.get("correct_answer", "").strip()

            if sign_img_rel:
                sign_visual = f"<img src='{escape(sign_img_rel)}' alt='Sign #{q_id}' class='sign-large-img' loading='lazy' onerror=\"this.style.opacity='0.2';\">"
            else:
                sign_visual = f"<div class='sign-open-text'><b>{escape(sign_text)}</b></div>"

            option_letters = ["A", "B", "C", "D"]
            opt_spans = []
            for opt_i, opt in enumerate(options):
                letter = option_letters[opt_i] if opt_i < len(option_letters) else str(opt_i + 1)
                opt_str = str(opt).strip()
                is_correct = (opt_str.lower() == correct.lower())
                correct_cls = "key-correct-target" if is_correct else ""
                check_icon = "<span class='key-check-mark'>✓</span>" if is_correct else ""
                opt_spans.append(
                    f"<div class='sign-opt-row {correct_cls}'><b>{letter}.</b> {escape(opt_str)}{check_icon}</div>"
                )

            item = f"""
            <div class="sign-open-item avoid-break">
                <div class="sign-media-col">
                    <span class="sign-tag-title">Sign {q_id}</span>
                    {sign_visual}
                </div>
                <div class="sign-desc-col">
                    <div class="sign-stem-txt"><b>{q_id}. {escape(q_stem)}</b></div>
                    <div class="sign-options-stack">
                        {''.join(opt_spans)}
                    </div>
                    <div class="teacher-key-line">Key: <b>{escape(correct)}</b></div>
                </div>
            </div>"""
            items.append(item)

        return f"<div class='open-2col-flow'>{''.join(items)}</div>"

    # 13. Word Families Table (13)
    elif ex_type == "word_families_table":
        rows = []
        for q_idx, q in enumerate(questions):
            base_word = q.get("base_word", "")
            base_type = q.get("base_word_type", "")
            verbs = ", ".join(q.get("verb", [])) or "—"
            nouns = ", ".join(q.get("noun", [])) or "—"
            adjs = ", ".join(q.get("adjective", [])) or "—"
            advs = ", ".join(q.get("adverb", [])) or "—"

            tr = f"""
            <tr class="avoid-break">
                <td style="text-align: center;">{q_idx + 1}</td>
                <td><b>{escape(base_word)}</b> <i>({escape(base_type)})</i></td>
                <td>{escape(verbs)}</td>
                <td>{escape(nouns)}</td>
                <td>{escape(adjs)}</td>
                <td>{escape(advs)}</td>
            </tr>"""
            rows.append(tr)

        table_html = f"""
        <table class="clean-open-table avoid-break">
            <colgroup>
                <col style="width: 6%;">
                <col style="width: 24%;">
                <col style="width: 17%;">
                <col style="width: 18%;">
                <col style="width: 18%;">
                <col style="width: 17%;">
            </colgroup>
            <thead>
                <tr>
                    <th>No.</th>
                    <th>Base Word</th>
                    <th>Verb</th>
                    <th>Noun</th>
                    <th>Adjective</th>
                    <th>Adverb</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>"""
        return table_html

    # 15. Word Formation (15)
    elif ex_type == "word_formation":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            base = q.get("base_word", "")
            correct = q.get("correct_answer", "").strip()

            blank_stem = re.sub(
                r"_{2,}",
                f"<span class='blank-open-slot'>...........................................</span><span class='teacher-key-line'> [<b>{escape(correct)}</b>]</span>",
                escape(raw_text)
            )

            item = f"""
            <div class="q-open-item avoid-break ex15-item">
                <span class="q-seq-num"><b>{q_id}.</b></span>
                <span class="q-stem-body">{blank_stem} <b>[{escape(base)}]</b></span>
            </div>"""
            items.append(item)

        return f"<div class='open-2col-flow'>{''.join(items)}</div>"

    # 16. Translation (16)
    elif ex_type == "translate_sentences":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            vi = q.get("vietnamese", "")
            en_correct = q.get("correct_answer", "").strip()

            item = f"""
            <div class="trans-open-row avoid-break">
                <div class="trans-vi-text"><b>{q_id}.</b> {escape(vi)}</div>
                <div class="trans-write-slot"><span class="trans-arrow">➔</span><span class="trans-dotted-rule"></span></div>
                <div class="trans-write-slot"><span class="trans-indent"></span><span class="trans-dotted-rule"></span></div>
                <div class="teacher-key-line">Key: <b>{escape(en_correct)}</b></div>
            </div>"""
            items.append(item)

        return f"<div class='trans-1col-stack'>{''.join(items)}</div>"

    return "<p>Content displayed.</p>"


def render_answer_key_sheet(exercises_list, book_title, unit_heading):
    html_chunks = []
    html_chunks.append(f"""
    <div class="textbook-sheet answer-key-sheet page-break" id="page-answer-key">
        <header class="running-header-bar">
            <span class="rh-left">{escape(book_title)} • {escape(unit_heading.upper())}</span>
            <span class="rh-right">PART III: ANSWER KEY & MODEL ANSWERS</span>
        </header>

        <div class="section-title-wrap" style="margin-top: 4px;">
            <h2 class="section-heading-blue">PART III: ANSWER KEY & MODEL ANSWERS</h2>
            <div class="section-instruction-orange">Official answer key for teacher verification and student reference:</div>
        </div>
        <div class="ak-4col-grid">
    """)

    for ex_idx, ex in enumerate(exercises_list):
        ex_num = ex_idx + 1
        num_str = str(ex_num)
        ex_title = BOOK_EXERCISE_TITLES.get(num_str, f"Exercise {ex_num}")
        ex_type = ex.get("type", "")
        questions = ex.get("questions", [])

        ans_rows = []

        if ex_type in ["multiple_choice", "word_families_mcq", "sentence_ordering_multiple_choice"]:
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                options = q.get("options", [])
                correct = q.get("correct_answer", "").strip()
                letter = ""
                option_letters = ["A", "B", "C", "D"]
                for oi, opt in enumerate(options):
                    if str(opt).strip().lower() == correct.lower():
                        letter = option_letters[oi] if oi < len(option_letters) else ""
                        break
                ans_str = f"<b>{letter}</b> ({escape(correct)})" if letter else f"<b>{escape(correct)}</b>"
                ans_rows.append(f"<span class='ak-chip'><b>{q_id}.</b> {ans_str}</span>")
            ans_body = f"<div class='ak-flow'>{''.join(ans_rows)}</div>"

        elif ex_type == "pic_to_word":
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<span class='ak-chip'><b>{q_id}.</b> {escape(correct)}</span>")
            ans_body = f"<div class='ak-flow'>{''.join(ans_rows)}</div>"

        elif ex_type == "write_english_words":
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                parts = q.get("parts", [])
                part_strs = [f"({chr(97+pi)}) {escape(p.get('correct_answer',''))}" for pi, p in enumerate(parts)]
                ans_rows.append(f"<div><b>Q{q_id}:</b> {' | '.join(part_strs)}</div>")
            ans_body = f"<div class='ak-stack'>{''.join(ans_rows)}</div>"

        elif ex_type == "fill_in_blanks":
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<span class='ak-chip'><b>{q_id}.</b> {escape(correct)}</span>")
            ans_body = f"<div class='ak-flow'>{''.join(ans_rows)}</div>"

        elif ex_type == "paragraph_fill":
            parts = ex.get("paragraph_parts", [])
            b_cnt = 0
            for part in parts:
                if isinstance(part, dict) and part.get("type") == "blank":
                    b_id = part.get("id", str(b_cnt + 1))
                    b_cor = part.get("correct_answer", "").strip()
                    ans_rows.append(f"<span class='ak-chip'><b>({b_id})</b> {escape(b_cor)}</span>")
                    b_cnt += 1
            ans_body = f"<div class='ak-flow'>{''.join(ans_rows)}</div>"

        elif ex_type == "dictionary_entry":
            entries = ex.get("entries", [])
            for e_idx, entry in enumerate(entries):
                e_id = entry.get("id", str(e_idx + 1))
                word = entry.get("word", "")
                q_list = entry.get("questions", [])
                q_strs = [f"#{q.get('id', qi+1)}: {escape(q.get('correct_answer',''))}" for qi, q in enumerate(q_list)]
                ans_rows.append(f"<div><b>Entry {e_id} ({escape(word)}):</b> {', '.join(q_strs)}</div>")
            ans_body = f"<div class='ak-stack'>{''.join(ans_rows)}</div>"

        elif ex_type == "signs_and_notices":
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                options = q.get("options", [])
                correct = q.get("correct_answer", "").strip()
                letter = ""
                option_letters = ["A", "B", "C", "D"]
                for oi, opt in enumerate(options):
                    if str(opt).strip().lower() == correct.lower():
                        letter = option_letters[oi] if oi < len(option_letters) else ""
                        break
                ans_str = f"<b>{letter}</b>" if letter else f"{escape(correct[:24])}"
                ans_rows.append(f"<span class='ak-chip'><b>{q_id}.</b> {ans_str}</span>")
            ans_body = f"<div class='ak-flow'>{''.join(ans_rows)}</div>"

        elif ex_type == "word_families_table":
            ans_body = "<div><i>(Refer to Exercise 13 table)</i></div>"

        elif ex_type == "word_formation":
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<span class='ak-chip'><b>{q_id}.</b> {escape(correct)}</span>")
            ans_body = f"<div class='ak-flow'>{''.join(ans_rows)}</div>"

        elif ex_type == "translate_sentences":
            for q_idx, q in enumerate(questions):
                q_id = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<div><b>{q_id}.</b> {escape(correct)}</div>")
            ans_body = f"<div class='ak-stack'>{''.join(ans_rows)}</div>"

        else:
            ans_body = "<div>—</div>"

        card = f"""
        <div class="ak-item-open avoid-break">
            <div class="ak-item-title"><b>Ex {ex_num}:</b> {escape(ex_title)}</div>
            <div class="ak-item-body">
                {ans_body}
            </div>
        </div>"""
        html_chunks.append(card)

    html_chunks.append("</div></div>")
    return "\n".join(html_chunks)


def build_full_open_textbook_html(vocab_data, exercises_list, base_output_dir, workspace_root, book_title, unit_heading, unit_name):
    vocab_html = render_vocab_pages_dynamic(vocab_data, base_output_dir, workspace_root, book_title, unit_heading, unit_name)
    exercises_html = render_exercises_continuous_stream(exercises_list, base_output_dir, workspace_root, book_title, unit_heading, unit_name)
    answer_key_html = render_answer_key_sheet(exercises_list, book_title, unit_heading)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(book_title)} • {escape(unit_heading)} - Student Workbook</title>
    
    <!-- DUY NHẤT 1 FONT CHỮ: PLUS JAKARTA SANS -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">

    <style>
        :root {{
            --c-blue: #1d4ed8;       /* Header bài tập & Section headers */
            --c-orange: #ea580c;     /* Hướng dẫn làm bài */
            --c-black: #000000;      /* Mọi văn bản còn lại */
            --c-white: #ffffff;      /* Background luôn trắng */
            --font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}

        *, *::before, *::after {{
            box-sizing: border-box;
            font-family: var(--font-family) !important;
            margin: 0;
            padding: 0;
            background-color: transparent;
            border-color: var(--c-black);
        }}

        html, body {{
            background: var(--c-white) !important;
            color: var(--c-black) !important;
            font-size: 10.5pt;
            line-height: 1.38;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        @page {{
            size: A4 portrait;
            margin: 7mm 9mm 7mm 9mm;
        }}

        @media screen {{
            body {{
                background: #f1f5f9 !important;
                padding: 16px 0 60px 0;
            }}
            .floating-action-bar {{
                max-width: 210mm !important;
            }}
            .document-full-wrap {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 20px;
            }}
            .textbook-sheet {{
                width: 210mm;
                min-height: 297mm;
                margin: 0 auto;
                background: var(--c-white) !important;
                padding: 7mm 9mm 7mm 9mm;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                box-sizing: border-box;
            }}
        }}

        @media print {{
            body {{
                background: var(--c-white) !important;
                font-size: 10.5pt !important;
                line-height: 1.38 !important;
                margin: 0 !important;
                padding: 0 !important;
                width: 100% !important;
            }}
            .no-print {{
                display: none !important;
            }}
            .page-break {{
                page-break-before: always !important;
                break-before: page !important;
            }}
            .avoid-break {{
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                -webkit-column-break-inside: avoid !important;
                display: inline-block !important;
                width: 100% !important;
            }}
            .document-full-wrap {{
                width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            .textbook-sheet {{
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                box-sizing: border-box;
            }}
        }}

        /* THANH CÔNG CỤ */
        .floating-action-bar {{
            position: sticky;
            top: 10px;
            z-index: 1000;
            max-width: 1180px;
            margin: 10px auto;
            background: #ffffff !important;
            border: 2px solid var(--c-blue);
            border-radius: 8px;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        }}

        .btn-act {{
            padding: 6px 16px;
            border-radius: 6px;
            font-size: 10.5pt;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid var(--c-black);
            background: #ffffff;
            color: var(--c-black);
        }}

        .btn-act-primary {{
            background: var(--c-blue) !important;
            color: #ffffff !important;
            border-color: var(--c-blue);
        }}

        .btn-act-key {{
            background: #ffffff !important;
            color: var(--c-orange) !important;
            border-color: var(--c-orange);
        }}

        /* SHEET HEADERS */
        .sheet-top-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid var(--c-black);
            padding-bottom: 5px;
            margin-bottom: 8px;
        }}

        .unit-main-heading {{
            font-size: 18.5pt;
            font-weight: 800;
            color: var(--c-blue) !important;
            margin: 0;
            line-height: 1.1;
            letter-spacing: 0.5px;
        }}

        .unit-sub-heading {{
            font-size: 12.5pt;
            color: var(--c-black);
            font-weight: 700;
            margin-top: 1px;
            line-height: 1.2;
        }}

        .unit-topic-tag {{
            font-size: 8.2pt;
            font-weight: 700;
            color: var(--c-orange);
            letter-spacing: 0.8px;
            margin-top: 2px;
        }}

        .student-info-strip {{
            display: flex;
            flex-direction: column;
            gap: 3px;
            font-size: 9.5pt;
            color: var(--c-black);
            text-align: right;
        }}

        .running-header-bar {{
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid var(--c-black);
            padding-bottom: 4px;
            margin-bottom: 8px;
            font-size: 9.2pt;
            font-weight: 700;
            color: var(--c-black);
        }}

        .section-title-wrap {{
            margin-bottom: 6px;
        }}

        .section-heading-blue {{
            font-size: 13pt;
            font-weight: 800;
            color: var(--c-blue) !important;
            text-transform: uppercase;
            letter-spacing: 0.2px;
        }}

        .section-instruction-orange {{
            font-size: 10pt;
            color: var(--c-orange) !important;
            font-style: italic;
            font-weight: 600;
            margin-top: 1px;
        }}

        .category-header-wrap {{
            margin-top: 8px;
            margin-bottom: 6px;
            border-left: 4px solid var(--c-blue);
            padding-left: 10px;
        }}

        .category-title-blue {{
            font-size: 12pt;
            font-weight: 800;
            color: var(--c-blue) !important;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        .ex-heading-blue {{
            font-size: 12.8pt;
            font-weight: 800;
            color: var(--c-blue) !important;
            margin-top: 12px;
            margin-bottom: 3px;
            border-bottom: 1.5px solid var(--c-blue);
            padding-bottom: 2px;
            page-break-after: avoid !important;
            break-after: avoid !important;
        }}

        .ex-guide-orange {{
            font-size: 10.4pt;
            color: var(--c-orange) !important;
            font-style: italic;
            font-weight: 600;
            margin-bottom: 7px;
            page-break-after: avoid !important;
            break-after: avoid !important;
        }}

        /* PHẦN I: TỪ VỰNG */
        .vocab-3col-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            column-gap: 14px;
            width: 100%;
        }}

        .page1-grid {{
            row-gap: 36px;
            margin-top: 8px;
            margin-bottom: 14px;
        }}

        .page2-grid-cat {{
            row-gap: 28px;
            margin-top: 6px;
            margin-bottom: 12px;
        }}

        .cat-separation-gap {{
            height: 20px;
            width: 100%;
            clear: both;
        }}

        .vocab-grid-cell {{
            display: flex;
            align-items: center;
            border-bottom: 1px dotted #000000;
            break-inside: avoid;
            page-break-inside: avoid;
            box-sizing: border-box;
        }}

        .p1-cell {{
            gap: 14px;
            padding: 16px 0;
        }}

        .p2-cell {{
            gap: 12px;
            padding: 13px 0;
        }}

        .p1-cell .v-img-frame {{
            width: 96px;
            height: 90px;
            min-width: 96px;
        }}

        .p2-cell .v-img-frame {{
            width: 88px;
            height: 82px;
            min-width: 88px;
        }}

        .v-img-frame {{
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .v-img-frame img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            display: block;
        }}

        .v-content-block {{
            flex-grow: 1;
            line-height: 1.28;
            color: var(--c-black);
            min-width: 0;
        }}

        .p1-cell .v-word-text {{
            font-size: 14.5pt;
        }}
        .p2-cell .v-word-text {{
            font-size: 13.6pt;
        }}

        .v-word-text {{
            font-weight: 800;
            color: var(--c-black);
            white-space: nowrap;
        }}

        .v-word-line {{
            display: flex;
            align-items: baseline;
            gap: 4px;
            margin-bottom: 2px;
            flex-wrap: wrap;
        }}

        .p1-cell .v-pos-text {{
            font-size: 10pt;
        }}
        .p2-cell .v-pos-text {{
            font-size: 9.5pt;
        }}

        .v-pos-text {{
            font-weight: 700;
            color: var(--c-black);
        }}

        .p1-cell .v-ipa-text {{
            font-size: 9.6pt;
        }}
        .p2-cell .v-ipa-text {{
            font-size: 9.2pt;
        }}

        .v-ipa-text {{
            color: var(--c-black);
            font-style: italic;
            margin-bottom: 2px;
        }}

        .p1-cell .v-mean-text {{
            font-size: 12pt;
            line-height: 1.4;
        }}
        .p2-cell .v-mean-text {{
            font-size: 11.5pt;
            line-height: 1.36;
        }}

        .v-mean-text {{
            font-weight: 600;
            color: var(--c-black);
            margin-bottom: 2px;
        }}

        .p1-cell .v-colloc {{
            font-size: 9.2pt;
        }}
        .p2-cell .v-colloc {{
            font-size: 8.8pt;
        }}

        .v-colloc {{
            color: var(--c-black);
            display: block;
        }}

        /* PHẦN II: BÀI TẬP */
        .open-2col-flow {{
            column-count: 2;
            column-gap: 22px;
            width: 100%;
        }}

        .exercise-open-section {{
            margin-bottom: 10px;
            width: 100%;
        }}

        .q-open-item {{
            display: inline-block;
            width: 100%;
            margin-bottom: 8px;
            font-size: 10.5pt;
            line-height: 1.4;
            color: var(--c-black);
            break-inside: avoid !important;
            page-break-inside: avoid !important;
            -webkit-column-break-inside: avoid !important;
        }}

        .q-line-stem {{
            display: flex;
            align-items: baseline;
            gap: 5px;
            margin-bottom: 2px;
        }}

        .q-seq-num {{
            font-weight: 800;
            color: var(--c-black);
            min-width: 22px;
            font-size: 10.8pt;
        }}

        .q-stem-body {{
            color: var(--c-black);
            font-weight: 500;
            font-size: 10.8pt;
        }}

        .q-choices-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            column-gap: 10px;
            row-gap: 3px;
            padding-left: 22px;
            font-size: 10.2pt;
        }}

        .opt-choice {{
            color: var(--c-black);
        }}

        /* TEACHER KEY */
        .teacher-key-line {{
            display: none;
            color: var(--c-orange);
            font-size: 9.5pt;
            font-weight: 700;
            margin-left: 22px;
            margin-top: 1px;
        }}

        .show-teacher-key-active .teacher-key-line {{
            display: block !important;
        }}

        .key-check-mark {{
            display: none;
            color: var(--c-orange);
            font-weight: 800;
            font-size: 9.5pt;
            margin-left: 3px;
        }}

        .show-teacher-key-active .key-correct-target .key-check-mark {{
            display: inline !important;
        }}
        .show-teacher-key-active .key-correct-target {{
            font-weight: 700;
            color: var(--c-orange) !important;
        }}

        /* BÀI 1 & 2 (TRANG 3) */
        .ex1-item, .ex2-item {{
            margin-bottom: 26px !important;
            font-size: 11.4pt !important;
            line-height: 1.5 !important;
        }}
        .ex1-item .q-seq-num, .ex2-item .q-seq-num {{
            font-size: 11.4pt !important;
            min-width: 24px !important;
        }}
        .ex1-item .q-stem-body, .ex2-item .q-stem-body {{
            font-size: 11.4pt !important;
        }}
        .ex1-item .q-choices-grid, .ex2-item .q-choices-grid {{
            row-gap: 6px !important;
            font-size: 11pt !important;
            padding-left: 24px !important;
        }}

        /* BÀI 3: HỘI THOẠI (TRANG 4) */
        .ex3-item {{
            margin-bottom: 10px !important;
            font-size: 10.2pt !important;
            line-height: 1.35 !important;
        }}
        .ex3-item .open-dialogue {{
            border-left: 2.5px solid var(--c-black);
            padding-left: 8px;
            margin-bottom: 4px;
            font-size: 10.2pt;
            line-height: 1.32;
        }}
        .ex3-item .q-choices-grid {{
            row-gap: 3.5px !important;
            column-gap: 8px !important;
            font-size: 9.8pt !important;
            line-height: 1.25 !important;
        }}

        /* BÀI 4: TRANH ẢNH (TRANG 4) */
        .pic-4col-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
            gap: 8px 12px;
            width: 100% !important;
            box-sizing: border-box !important;
        }}

        .pic-open-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            width: 100%;
            box-sizing: border-box;
            break-inside: avoid;
            page-break-inside: avoid;
        }}

        .pic-big-frame {{
            width: 100%;
            height: 68px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 4px;
            overflow: hidden;
        }}

        .pic-big-frame img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 3px;
        }}

        .pic-label-row {{
            display: flex;
            align-items: center;
            gap: 6px;
            width: 100%;
            box-sizing: border-box;
            padding: 0 4px;
        }}

        .pic-q-num {{
            font-size: 10.2pt;
            font-weight: 700;
            color: var(--c-black);
            flex-shrink: 0;
        }}

        .pic-dotted-slot {{
            flex-grow: 1;
            border-bottom: 1.4px dotted #000000;
            height: 18px;
            display: block;
        }}

        .open-dotted-line {{
            color: var(--c-black);
            letter-spacing: -1px;
            font-family: monospace !important;
        }}

        /* BÀI 5: TỪ THEO NGHĨA (TRANG 5) */
        .ex5-item {{
            margin-bottom: 16px !important;
            font-size: 11.2pt !important;
            line-height: 1.5 !important;
        }}
        .ex5-item .q-seq-num {{
            font-size: 11.2pt !important;
        }}
        .sub-parts-wrap {{
            flex-grow: 1;
        }}
        .write-sub-item {{
            margin-bottom: 3px;
        }}

        /* BÀI 6: WORD BOX (TRANG 5) */
        .ex6-item {{
            margin-bottom: 16px !important;
            font-size: 11.2pt !important;
            line-height: 1.5 !important;
        }}
        .ex6-item .q-seq-num {{
            font-size: 11.2pt !important;
        }}
        .open-word-box {{
            border-top: 1.5px solid var(--c-black);
            border-bottom: 1.5px solid var(--c-black);
            padding: 7px 0;
            margin-bottom: 12px;
            font-size: 11.4pt;
            color: var(--c-black);
            page-break-after: avoid !important;
            break-after: avoid !important;
        }}

        .blank-open-slot {{
            font-weight: 600;
            color: var(--c-black);
        }}

        /* BÀI 7: ĐOẠN VĂN (TRANG 5 & TRANG 6) */
        .open-passage-block {{
            margin-bottom: 8px;
        }}

        .passage-body-text {{
            font-size: 11.8pt;
            line-height: 1.76;
            color: var(--c-black);
            margin-bottom: 12px;
        }}

        .para-slot-inline {{
            display: inline-block;
            margin: 0 2px;
        }}

        .passage-answer-grid-5 {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px 14px;
            font-size: 10.8pt;
            border-top: 1.4px dotted var(--c-black);
            border-bottom: 1.4px dotted var(--c-black);
            padding: 10px 0;
            margin-bottom: 18px;
        }}

        /* BÀI 8: SẮP XẾP CÂU (TRANG 6) */
        .so-item {{
            margin-bottom: 22px !important;
            font-size: 11pt !important;
        }}
        .so-lead {{
            font-weight: 700;
            color: var(--c-black);
            margin-bottom: 5px;
            font-size: 11.5pt;
        }}
        .so-sub-lines {{
            margin-left: 16px;
            margin-bottom: 8px;
            font-size: 11pt;
            line-height: 1.52;
        }}
        .so-choices-row {{
            display: flex;
            gap: 24px;
            font-size: 11pt;
            margin-top: 5px;
        }}

        /* BÀI 9 & 10 (TRANG 6 & TRANG 7) */
        .ex9-item {{
            margin-bottom: 22px !important;
            font-size: 11.4pt !important;
            line-height: 1.5 !important;
        }}
        .ex9-item .q-seq-num {{
            font-size: 11.4pt !important;
            min-width: 24px !important;
        }}
        .ex9-item .q-choices-grid {{
            row-gap: 6px !important;
            font-size: 11pt !important;
            padding-left: 24px !important;
        }}
        .ex10-item {{
            margin-bottom: 26px !important;
            font-size: 11.4pt !important;
            line-height: 1.5 !important;
        }}
        .ex10-item .q-seq-num {{
            font-size: 11.4pt !important;
            min-width: 24px !important;
        }}
        .ex10-item .q-choices-grid {{
            row-gap: 5.5px !important;
            font-size: 11pt !important;
            padding-left: 24px !important;
        }}

        /* BÀI 11: TỪ ĐIỂN MỞ (TRANG 7) */
        .dict-open-entry {{
            display: inline-block;
            width: 100%;
            margin-bottom: 28px;
            font-size: 10.8pt;
            line-height: 1.45;
            border-bottom: 1.2px dotted #000000;
            padding-bottom: 14px;
            break-inside: avoid;
        }}
        .dict-head-text {{
            font-size: 12.5pt;
            font-weight: 800;
            color: var(--c-black);
            margin-bottom: 4px;
        }}
        .ipa-faded {{
            font-style: italic;
        }}
        .dict-def-line {{
            font-size: 11pt;
            margin-bottom: 5px;
            line-height: 1.42;
        }}
        .dict-bullets-inline {{
            padding-left: 18px;
            margin-bottom: 6px;
            font-size: 10.5pt;
            line-height: 1.4;
        }}
        .dict-sentences-box {{
            font-size: 10.8pt;
            line-height: 1.48;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        /* BÀI 12: BIỂN BÁO (TRANG 8) */
        .sign-open-item {{
            display: inline-flex;
            width: 100%;
            gap: 14px;
            margin-bottom: 22px;
            align-items: flex-start;
            break-inside: avoid;
        }}

        .sign-media-col {{
            width: 105px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
            flex-shrink: 0;
        }}

        .sign-tag-title {{
            font-size: 10.6pt;
            font-weight: 800;
            color: var(--c-black);
        }}

        .sign-large-img {{
            max-width: 100%;
            height: 96px;
            max-height: 96px;
            object-fit: contain;
        }}

        .sign-desc-col {{
            flex-grow: 1;
            font-size: 10.2pt;
        }}

        .sign-stem-txt {{
            color: var(--c-black);
            font-size: 11.2pt;
            font-weight: 700;
            line-height: 1.36;
            margin-bottom: 5px;
        }}

        .sign-options-stack {{
            display: flex;
            flex-direction: column;
            gap: 4.5px;
            font-size: 10.2pt;
            line-height: 1.32;
        }}

        /* BÀI 13: BẢNG TỪ LOẠI (TRANG 9) */
        .clean-open-table {{
            width: 100%;
            table-layout: fixed;
            border-collapse: collapse;
            font-size: 11pt;
            margin-bottom: 18px;
        }}

        .clean-open-table th {{
            border-top: 1.5px solid var(--c-black);
            border-bottom: 1.5px solid var(--c-black);
            padding: 8px 8px;
            color: var(--c-black);
            font-weight: 800;
            font-size: 11.2pt;
            text-align: left;
        }}

        .clean-open-table td {{
            border-bottom: 1px dotted #000000;
            padding: 8px 8px;
            color: var(--c-black);
            font-size: 11pt;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* BÀI 14 & 15 (TRANG 9) */
        .ex14-item, .ex15-item {{
            margin-bottom: 22px !important;
            font-size: 11.2pt !important;
            line-height: 1.45 !important;
        }}
        .ex14-item .q-seq-num, .ex15-item .q-seq-num {{
            font-size: 11.2pt !important;
            min-width: 24px !important;
        }}
        .ex14-item .q-stem-body, .ex15-item .q-stem-body {{
            font-size: 11.2pt !important;
        }}
        .ex14-item .q-choices-grid {{
            row-gap: 5px !important;
            font-size: 10.8pt !important;
            padding-left: 24px !important;
        }}

        /* BÀI 16: DỊCH CÂU (TRANG 10) */
        .trans-1col-stack {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 100%;
        }}
        .trans-open-row {{
            margin-bottom: 34px;
            font-size: 12.5pt;
            line-height: 1.55;
        }}
        .trans-vi-text {{
            font-weight: 700;
            color: var(--c-black);
            margin-bottom: 8px;
            font-size: 12.5pt;
        }}
        .trans-write-slot {{
            display: flex;
            align-items: flex-end;
            gap: 8px;
            height: 27px;
            margin-top: 8px;
            width: 100%;
        }}
        .trans-arrow {{
            font-weight: bold;
            color: var(--c-black);
            flex-shrink: 0;
            font-size: 12.5pt;
            line-height: 1;
        }}
        .trans-indent {{
            width: 14px;
            flex-shrink: 0;
        }}
        .trans-dotted-rule {{
            flex-grow: 1;
            border-bottom: 1.4px dotted var(--c-black);
            height: 100%;
        }}

        /* BẢNG ĐÁP ÁN (TRANG 11) */
        .answer-key-sheet {{
            padding-top: 0 !important;
        }}

        .ak-4col-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px 14px;
            margin-top: 10px;
        }}

        .ak-item-open {{
            font-size: 9.4pt;
            border-top: 1.3px solid var(--c-black);
            padding-top: 6px;
        }}

        .ak-item-title {{
            font-size: 10.2pt;
            font-weight: 800;
            color: var(--c-blue) !important;
            margin-bottom: 4px;
        }}

        .ak-flow {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px 8px;
            font-size: 9pt;
            line-height: 1.32;
        }}

        .ak-stack {{
            font-size: 8.6pt;
            line-height: 1.28;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .ak-chip {{
            white-space: nowrap;
        }}

        .hide-key-mode #page-answer-key {{
            display: none !important;
        }}
    </style>
</head>
<body>

    <!-- THANH ĐIỀU KHIỂN NỔI -->
    <div class="floating-action-bar no-print">
        <div style="display: flex; align-items: center; gap: 10px;">
            <button class="btn-act btn-act-primary" onclick="window.print()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="vertical-align: middle; margin-right: 5px;"><path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
                In Sách / Xuất PDF (Ctrl + P)
            </button>
            <button class="btn-act btn-act-key" id="btnToggleKey" onclick="toggleTeacherKey()">
                👁️ Bật Đáp Án Nhanh
            </button>
        </div>
        <div>
            <button class="btn-act" id="btnToggleAk" onclick="toggleAnswerKey()">
                📋 In Kèm Bảng Đáp Án: BẬT
            </button>
        </div>
    </div>

    <!-- TỔNG THỂ TOÀN TẬP TÀI LIỆU -->
    <div class="document-full-wrap" id="docRoot">
        {vocab_html}
        {exercises_html}
        {answer_key_html}
    </div>

    <script>
        function toggleTeacherKey() {{
            const root = document.getElementById('docRoot');
            const btn = document.getElementById('btnToggleKey');
            root.classList.toggle('show-teacher-key-active');
            if (root.classList.contains('show-teacher-key-active')) {{
                btn.innerHTML = '🙈 Ẩn Đáp Án';
                btn.style.background = '#ea580c';
                btn.style.color = '#ffffff';
            }} else {{
                btn.innerHTML = '👁️ Bật Đáp Án Nhanh';
                btn.style.background = '#ffffff';
                btn.style.color = '#ea580c';
            }}
        }}

        function toggleAnswerKey() {{
            const root = document.getElementById('docRoot');
            const btn = document.getElementById('btnToggleAk');
            root.classList.toggle('hide-key-mode');
            if (root.classList.contains('hide-key-mode')) {{
                btn.innerHTML = '📋 In Kèm Bảng Đáp Án: TẮT';
                btn.style.color = '#dc2626';
            }} else {{
                btn.innerHTML = '📋 In Kèm Bảng Đáp Án: BẬT';
                btn.style.color = 'var(--c-black)';
            }}
        }}
    </script>
</body>
</html>
"""


def detect_workspace_root():
    current_dir = Path(__file__).resolve()
    for p in current_dir.parents:
        if (p / "lessons").exists():
            return p
    return Path.cwd().resolve()


def main():
    workspace_root = detect_workspace_root()
    unit_arg = sys.argv[1] if len(sys.argv) > 1 else "unit-1"
    if unit_arg.isdigit():
        unit_name = f"unit-{unit_arg}"
    elif unit_arg.startswith("unit-"):
        unit_name = unit_arg
    else:
        unit_name = "unit-1"

    # Detect grade
    ws_name = workspace_root.name
    grade = "12"
    m_grade = re.search(r"(\d+)", ws_name)
    if m_grade:
        grade = m_grade.group(1)
    book_title = f"GLOBAL SUCCESS {grade}"

    unit_num = unit_name.replace("unit-", "")
    unit_heading = f"Unit {unit_num}"

    vocab_dir = workspace_root / "lessons" / unit_name / "vocab"
    vocab_json_file = vocab_dir / "vocab.json"
    exercises_dir = vocab_dir / "exercises"
    raw_content_file = vocab_dir / "raw-content.md"

    # Detect unit title from raw-content.md
    if raw_content_file.exists():
        try:
            content = open(raw_content_file, "r", encoding="utf-8").read()
            m = re.search(r"#\s*Unit\s*(\d+)[:\s]+([^\n\r]+)", content, re.IGNORECASE)
            if m:
                theme = m.group(2).strip()
                unit_heading = f"Unit {unit_num}: {theme.upper()}"
        except Exception:
            pass

    print(f"Workspace: {workspace_root}")
    print(f"Book Title: {book_title}")
    print(f"Unit: {unit_heading}")
    print(f"Loading vocabulary from {vocab_json_file}...")
    vocab_data = load_json(vocab_json_file)

    print(f"Loading exercises from {exercises_dir}...")
    ex_files = sorted(glob.glob(str(exercises_dir / "*.json")))
    exercises_list = []
    for f in ex_files:
        d = load_json(f)
        if d:
            exercises_list.append(d)

    print(f"Loaded {len(exercises_list)} exercise files.")

    # Generate vocab_unit<N>.html inside unit folder
    unit_html_file = vocab_dir / f"vocab_unit{unit_num}.html"
    print(f"Generating unit HTML at {unit_html_file}...")
    unit_html_content = build_full_open_textbook_html(
        vocab_data, exercises_list, vocab_dir, workspace_root, book_title, unit_heading, unit_name
    )
    with open(unit_html_file, "w", encoding="utf-8") as f:
        f.write(unit_html_content)
    print(f"Successfully generated {unit_html_file} ({len(unit_html_content)} bytes)")

    vocab_pdf_html = vocab_dir / "pdf.html"
    with open(vocab_pdf_html, "w", encoding="utf-8") as f:
        f.write(unit_html_content)

    root_pdf_html = workspace_root / "pdf.html"
    root_html_content = build_full_open_textbook_html(
        vocab_data, exercises_list, workspace_root, workspace_root, book_title, unit_heading, unit_name
    )
    with open(root_pdf_html, "w", encoding="utf-8") as f:
        f.write(root_html_content)
    print(f"Also wrote {vocab_pdf_html} and {root_pdf_html}")


if __name__ == "__main__":
    main()
