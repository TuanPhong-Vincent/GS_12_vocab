#!/usr/bin/env python3
"""
Vocab & Exercises PDF Book Generator (build_vocab_pdf.py)

Generates a publication-grade, textbook-styled PDF file containing:
- Title Header: Unit * [ĐỀ MỤC]
- Section I: Vocabulary (cards with images, IPA, Vietnamese definitions, examples)
- Section II: Exercises (all 16 exercise types formatted as authentic textbook pages)
- Section III: Answer Key & Explanations (compact reference at the end of the unit)

Key Design Features:
- Natural continuous flow with strictly zero awkward page breaks (no sliced cards, no broken questions, no orphan headers)
- Professional textbook color scheme (Deep Navy #1e3a8a, Royal Blue #2563eb, Slate #334155, Crisp Borders #cbd5e1)
- Native running headers and footers with dynamic page numbering (Page X of Y)
- Responsive CSS-ruled handwriting lines (clean vector dotted lines that never wrap or overflow)
- Automatic headless browser PDF conversion (Edge/Chrome)
"""

import os
import sys
import json
import glob
import re
import argparse
import subprocess
from pathlib import Path
from html import escape

# Safe Windows stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


ROADMAP_THEMES = {
    "GS12": {
        1: "Life Stories We Admire",
        2: "A Multicultural World",
        3: "Green Living",
        4: "Urbanisation",
        5: "The World of Work",
        6: "Artificial Intelligence",
        7: "The World of Mass Media",
        8: "Wildlife Conservation",
        9: "Career Paths",
        10: "Lifelong Learning"
    },
    "GS11": {
        1: "A Long and Healthy Life",
        2: "The Generation Gap",
        3: "Cities of the Future",
        4: "ASEAN and Viet Nam",
        5: "Global Warming",
        6: "Preserving Our Heritage",
        7: "Education Options for School-Leavers",
        8: "Becoming Independent",
        9: "Social Issues",
        10: "The Ecosystem"
    },
    "GS10": {
        1: "Family Life",
        2: "Humans and the Environment",
        3: "Music",
        4: "For a Better Community",
        5: "Inventions",
        6: "Gender Equality",
        7: "Viet Nam and International Organisations",
        8: "New Ways to Learn",
        9: "Protecting the Environment",
        10: "Ecotourism"
    }
}


def find_workspace_root(start_path):
    """Locate the workspace root by looking for .agent or lessons."""
    curr = Path(start_path).resolve()
    for p in [curr] + list(curr.parents):
        if (p / ".agent").exists() or (p / "lessons").exists():
            return p
    return curr


def resolve_unit_info(input_path):
    """
    Resolve vocab_dir, unit_dir, book_name, unit_num, and theme_title.
    """
    path_obj = Path(input_path).resolve()
    if path_obj.name.lower() == "vocab":
        vocab_dir = path_obj
        unit_dir = path_obj.parent
    else:
        vocab_dir = path_obj / "vocab" if (path_obj / "vocab").is_dir() else path_obj
        unit_dir = path_obj

    # Extract unit number
    unit_num = 1
    m = re.search(r"unit[-_]?(\d+)", str(unit_dir), re.IGNORECASE)
    if m:
        unit_num = int(m.group(1))

    # Detect Grade / Book
    book_code = "GS12"
    book_name = "Global Success 12"
    path_str = str(unit_dir).lower()
    if "gs11" in path_str or "gs-11" in path_str:
        book_code = "GS11"
        book_name = "Global Success 11"
    elif "gs10" in path_str or "gs-10" in path_str:
        book_code = "GS10"
        book_name = "Global Success 10"

    # Detect Theme Title from raw-content.md or roadmap fallback
    theme_title = ""
    raw_md_candidates = [
        unit_dir / "raw-content.md",
        vocab_dir / "raw-content.md",
        unit_dir / "raw-all-content.md"
    ]
    for rmc in raw_md_candidates:
        if rmc.exists():
            try:
                with open(rmc, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Look for "# Unit X: Theme Title"
                    tm = re.search(r"#\s*Unit\s*\d+\s*:\s*([^\r\n#]+)", content, re.IGNORECASE)
                    if tm:
                        theme_title = tm.group(1).strip()
                        break
            except Exception:
                pass

    if not theme_title:
        theme_title = ROADMAP_THEMES.get(book_code, {}).get(unit_num, f"Unit {unit_num} Vocabulary")

    return vocab_dir, unit_dir, book_name, book_code, unit_num, theme_title


def load_json(file_path):
    """Safely load JSON data."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed to load {file_path}: {e}", file=sys.stderr)
        return None


def to_file_uri(asset_path_str, workspace_root):
    """
    Convert an asset path (like /lessons/media/gs12/unit-1/images/childhood.webp)
    into a valid absolute file:/// URI for the headless browser.
    """
    if not asset_path_str:
        return ""
    if asset_path_str.startswith("http://") or asset_path_str.startswith("https://") or asset_path_str.startswith("data:"):
        return asset_path_str

    clean = asset_path_str.lstrip("/\\")
    full_path = (workspace_root / clean).resolve()
    if not full_path.exists():
        # Try relative to lessons
        full_path = (workspace_root / "lessons" / clean).resolve()
    return full_path.as_uri()


def highlight_target_word(text):
    """Helper to highlight target words with markdown or asterisks/underscores."""
    if not text:
        return ""
    # Bold **word** or <b>word</b>
    formatted = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    # Underline target words wrapped in [word]
    formatted = re.sub(r"\[(.*?)\]", r"<u class='underline-word'><strong>\1</strong></u>", formatted)
    return formatted


# ==========================================
# RENDER SECTION I: VOCABULARY THEORY CARDS
# ==========================================
def render_vocabulary_cards_html(vocab_data, workspace_root):
    """
    Renders Section I: Vocabulary Cards arranged in a textbook-styled 3-column grid.
    Each card contains:
    - High-quality image (contain, proportional height)
    - English word (Bold Deep Navy #1e3a8a)
    - IPA transcription (Soft Blue #2563eb)
    - Vietnamese meaning (Slate #334155)
    - Contextual example sentences with Vietnamese translation
    """
    html_parts = []
    
    for g_idx, group in enumerate(vocab_data):
        g_name = group.get("group", f"Vocabulary Group {g_idx + 1}")
        words = group.get("words", [])
        if not words:
            continue

        # Group header
        html_parts.append(f"""
        <div class="vocab-group-header">
            <span class="group-num-pill">{g_idx + 1}</span>
            <span class="group-title-text">{escape(g_name)}</span>
            <span class="group-count">({len(words)} words)</span>
        </div>
        <div class="vocab-grid-book">
        """)

        for w in words:
            en_word = w.get("english_word", "").strip()
            ipa_br = w.get("pronunciation_british", "")
            ipa_am = w.get("pronunciation_american", "")
            ipa = ipa_am or ipa_br or ""
            vi_meaning = w.get("vietnamese_meaning", "").strip()
            img_raw = w.get("image", "")
            img_uri = to_file_uri(img_raw, workspace_root)
            alt_text = w.get("alt") or en_word

            img_tag = ""
            if img_raw:
                img_tag = f"""
                <div class="card-img-wrap">
                    <img src="{escape(img_uri)}" alt="{escape(alt_text)}" loading="eager" onerror="this.parentElement.style.display='none';">
                    <div class="btn-speaker-mini">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.74 2.5-2.26 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                        </svg>
                    </div>
                </div>"""

            card_html = f"""
            <div class="vocab-book-card">
                {img_tag}
                <div class="card-body">
                    <div class="word-header-row">
                        <div class="word-en">{escape(en_word)}</div>
                        {f'<div class="word-ipa">{escape(ipa)}</div>' if ipa else ''}
                    </div>
                    <div class="card-divider"></div>
                    <div class="word-vi-def">{escape(vi_meaning)}</div>
                </div>
            </div>"""
            html_parts.append(card_html)

        html_parts.append("</div><!-- /vocab-grid-book -->\n")

    return "\n".join(html_parts)


# ==========================================
# RENDER SECTION II: 16 PRACTICE EXERCISES
# ==========================================
def render_mcq_options(options, q_idx, ex_idx):
    """Render 4 MCQ options formatted for textbook printing with automatic column balancing."""
    letters = ["A", "B", "C", "D"]
    opt_tags = []
    
    # Calculate max option length to auto-balance columns
    max_len = max([len(str(o)) for o in options]) if options else 0
    if len(options) == 4 and max_len <= 16:
        col_class = "opts-col-4"
    elif len(options) == 4 and max_len <= 45:
        col_class = "opts-col-2"
    else:
        col_class = "opts-col-1"

    for i, opt in enumerate(options):
        letter = letters[i] if i < len(letters) else f"({i+1})"
        opt_str = str(opt).strip()
        opt_tags.append(f"""
        <div class="book-option-item">
            <span class="opt-letter"><strong>{letter}.</strong></span>
            <span class="opt-body">{escape(opt_str)}</span>
        </div>""")

    return f"<div class='book-options-grid {col_class}'>{''.join(opt_tags)}</div>"


def render_single_exercise(ex, ex_num, workspace_root):
    """
    Renders an individual exercise into publication-grade textbook HTML.
    Supports all 16 exercise formats with natural layout, handwriting lines,
    and strict break-inside avoid rules.
    """
    ex_type = ex.get("type", "")
    title = ex.get("title", f"Exercise {ex_num}")
    instruction = ex.get("instruction", "")
    questions = ex.get("questions", [])

    body_html = ""

    # 1, 2, 9, 10, 14: Standard MCQ Exercises
    if ex_type in ["multiple_choice", "word_families_mcq"]:
        q_items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            options = q.get("options", [])
            formatted_stem = highlight_target_word(raw_text)

            q_card = f"""
            <div class="book-q-item">
                <div class="q-stem-row">
                    <span class="q-badge">{q_id}</span>
                    <div class="q-stem-text">{formatted_stem}</div>
                </div>
                {render_mcq_options(options, q_idx, ex_num)}
            </div>"""
            q_items.append(q_card)
        body_html = "<div class='mcq-list'>" + "\n".join(q_items) + "</div>"

    # 3: Multiple Choice Conversation
    elif ex_type == "multiple_choice_conversation" or (ex_type == "multiple_choice" and any("\n" in q.get("text", "") for q in questions)):
        q_items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            options = q.get("options", [])
            
            # Format dialogue lines
            lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
            dialogue_spans = []
            for l in lines:
                if ":" in l:
                    speaker, speech = l.split(":", 1)
                    dialogue_spans.append(f"<div class='dialogue-line'><strong class='speaker-tag'>{escape(speaker)}:</strong> {highlight_target_word(speech.strip())}</div>")
                else:
                    dialogue_spans.append(f"<div class='dialogue-line'>{highlight_target_word(l)}</div>")

            q_card = f"""
            <div class="book-q-item dialogue-q-item">
                <div class="q-stem-row">
                    <span class="q-badge">{q_id}</span>
                    <div class="dialogue-box">{''.join(dialogue_spans)}</div>
                </div>
                {render_mcq_options(options, q_idx, ex_num)}
            </div>"""
            q_items.append(q_card)
        body_html = "<div class='mcq-list'>" + "\n".join(q_items) + "</div>"

    # 4: Picture to Word (Balanced 4-column grid with responsive CSS dotted line)
    elif ex_type == "pic_to_word":
        cards = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            img_raw = q.get("image", "")
            img_uri = to_file_uri(img_raw, workspace_root)

            card = f"""
            <div class="pic-to-word-card">
                <div class="pic-box">
                    <span class="pic-q-badge">{q_id}</span>
                    <img src="{escape(img_uri)}" alt="Item {q_id}" loading="eager" onerror="this.style.opacity='0.3';">
                </div>
                <div class="pic-write-line">
                    <div class="hw-line"></div>
                </div>
            </div>"""
            cards.append(card)
        body_html = f"<div class='pic-grid-book'>{''.join(cards)}</div>"

    # 5: Write English Words from Vietnamese (Responsive flex dotted lines)
    elif ex_type == "write_english_words":
        rows = []
        item_counter = 1
        for q in questions:
            parts = q.get("parts", [])
            for p in parts:
                vi = p.get("vietnamese", "")
                row = f"""
                <div class="write-word-item">
                    <span class="q-badge">{item_counter}</span>
                    <span class="vi-prompt">{escape(vi)}</span>
                    <div class="hw-line-flex"></div>
                </div>"""
                rows.append(row)
                item_counter += 1
        body_html = f"<div class='write-words-list-book'>{''.join(rows)}</div>"

    # 6: Fill in the Blanks
    elif ex_type == "fill_in_blanks":
        word_box = ex.get("word_box", [])
        box_chips = "".join(f"<span class='wb-chip'>{escape(w)}</span>" for w in word_box)
        box_html = f"""
        <div class="word-box-book">
            <div class="wb-header">📦 WORD BOX (TỪ GỢI Ý):</div>
            <div class="wb-chips">{box_chips}</div>
        </div>"""

        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            # Replace blank underscores with handwriting underline
            blank_stem = re.sub(r"_{2,}", "<span class='inline-hw-blank'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>", escape(raw_text))

            item = f"""
            <div class="book-q-item blank-q-item">
                <span class="q-badge">{q_id}</span>
                <div class="blank-text">{blank_stem}</div>
            </div>"""
            items.append(item)
        body_html = box_html + f"<div class='blanks-list-book'>{''.join(items)}</div>"

    # 7: Paragraph Fill
    elif ex_type == "paragraph_fill":
        word_box = ex.get("word_box", [])
        box_chips = "".join(f"<span class='wb-chip'>{escape(w)}</span>" for w in word_box)
        box_html = f"""
        <div class="word-box-book">
            <div class="wb-header">📦 WORD BOX (TỪ GỢI Ý ĐIỀN ĐOẠN VĂN):</div>
            <div class="wb-chips">{box_chips}</div>
        </div>"""

        parts = ex.get("paragraph_parts", [])
        para_spans = []
        blank_c = 1
        for p in parts:
            if isinstance(p, str):
                para_spans.append(escape(p))
            elif isinstance(p, dict) and p.get("type") == "blank":
                b_id = p.get("id", str(blank_c))
                para_spans.append(f"<span class='para-inline-slot'><strong>({b_id})</strong> <span class='inline-hw-blank'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>")
                blank_c += 1

        passage_html = f"""
        <div class="paragraph-card-book">
            <div class="para-passage-text">{''.join(para_spans)}</div>
        </div>"""
        body_html = box_html + passage_html

    # 8: Sentence Ordering
    elif ex_type == "sentence_ordering_multiple_choice":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            sentences = q.get("sentences", [])
            options = q.get("options", [])

            s_lis = "".join(f"<li class='order-li'><strong>{chr(97 + si)}.</strong> {escape(s)}</li>" for si, s in enumerate(sentences))
            order_list = f"<ul class='sentence-order-ul'>{s_lis}</ul>"

            item = f"""
            <div class="book-q-item order-q-item">
                <div class="q-stem-row">
                    <span class="q-badge">{q_id}</span>
                    <div class="order-content">
                        {order_list}
                    </div>
                </div>
                {render_mcq_options(options, q_idx, ex_num)}
            </div>"""
            items.append(item)
        body_html = f"<div class='order-list-book'>{''.join(items)}</div>"

    # 11: Dictionary Entries
    elif ex_type == "dictionary_entry":
        entries = ex.get("entries", [])
        entry_cards = []
        for e_idx, e in enumerate(entries):
            e_id = e.get("id", str(e_idx + 1))
            word = e.get("word", "")
            pos = e.get("part_of_speech", "")
            pr = e.get("pronunciation", "")
            defn = e.get("definition", "")
            bullets = e.get("bullet_points", [])
            q_list = e.get("questions", [])

            bullet_tags = "".join(f"<li>{highlight_target_word(b)}</li>" for b in bullets)
            q_tags = []
            for qi, q in enumerate(q_list):
                qid = q.get("id", str(qi + 1))
                qtext = q.get("text", "")
                blanked = re.sub(r"_{2,}", "<span class='inline-hw-blank'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>", escape(qtext))
                q_tags.append(f"""
                <div class="dict-sub-q">
                    <span class="sub-q-num">({qid})</span>
                    <span class="sub-q-text">{blanked}</span>
                </div>""")

            card = f"""
            <div class="oxford-book-entry">
                <div class="dict-top-bar">
                    <span class="dict-headword">{escape(word)}</span>
                    <span class="dict-pos-pill">{escape(pos)}</span>
                    <span class="dict-ipa-pill">{escape(pr)}</span>
                </div>
                <div class="dict-definition"><strong>Definition:</strong> {escape(defn)}</div>
                <div class="dict-bullets-wrap">
                    <div class="dict-colloc-label">Examples & Collocations:</div>
                    <ul class="dict-ul">{bullet_tags}</ul>
                </div>
                <div class="dict-practice-wrap">
                    <div class="dict-colloc-label">Practice Questions:</div>
                    {''.join(q_tags)}
                </div>
            </div>"""
            entry_cards.append(card)
        body_html = f"<div class='dict-entries-list'>{''.join(entry_cards)}</div>"

    # 12: Signs and Notices
    elif ex_type == "signs_and_notices":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            sign_text = q.get("sign_text", "")
            q_stem = q.get("question", "What does this sign mean?")
            options = q.get("options", [])

            item = f"""
            <div class="book-q-item sign-q-item">
                <div class="sign-top-row">
                    <span class="q-badge">{q_id}</span>
                    <div class="sign-board-book">
                        <div class="sign-icon">🪧 NOTICE / SIGN</div>
                        <div class="sign-text-content">{escape(sign_text)}</div>
                    </div>
                </div>
                <div class="sign-question-stem"><strong>{escape(q_stem)}</strong></div>
                {render_mcq_options(options, q_idx, ex_num)}
            </div>"""
            items.append(item)
        body_html = f"<div class='signs-list-book'>{''.join(items)}</div>"

    # 13: Word Families Table
    elif ex_type == "word_families_table":
        rows = []
        for q in questions:
            bw = q.get("base_word", "")
            bt = q.get("base_word_type", "")
            verbs = ", ".join(q.get("verb", [])) or "—"
            nouns = ", ".join(q.get("noun", [])) or "—"
            adjs = ", ".join(q.get("adjective", [])) or "—"
            advs = ", ".join(q.get("adverb", [])) or "—"

            row = f"""
            <tr>
                <td class="td-base"><strong>{escape(bw)}</strong> <span class="tag-pos">({escape(bt)})</span></td>
                <td>{escape(verbs)}</td>
                <td>{escape(nouns)}</td>
                <td>{escape(adjs)}</td>
                <td>{escape(advs)}</td>
            </tr>"""
            rows.append(row)

        body_html = f"""
        <div class="table-container-book">
            <table class="wf-table-book">
                <thead>
                    <tr>
                        <th style="width: 22%;">Base Word</th>
                        <th style="width: 19%;">Verb</th>
                        <th style="width: 21%;">Noun</th>
                        <th style="width: 21%;">Adjective</th>
                        <th style="width: 17%;">Adverb</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        </div>"""

    # 15: Word Formation
    elif ex_type == "word_formation":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            base = q.get("base_word", "")
            blanked = re.sub(r"_{2,}", "<span class='inline-hw-blank'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>", escape(raw_text))

            item = f"""
            <div class="book-q-item wf-formation-item">
                <span class="q-badge">{q_id}</span>
                <div class="wf-stem-wrap">
                    <span class="wf-sentence">{blanked}</span>
                    <span class="wf-root-tag">({escape(base)})</span>
                </div>
            </div>"""
            items.append(item)
        body_html = f"<div class='wf-formation-list'>{''.join(items)}</div>"

    # 16: Translation Sentences (Clean vector ruled lines)
    elif ex_type == "translate_sentences":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            vi = q.get("vietnamese", "")

            item = f"""
            <div class="book-q-item trans-q-item">
                <div class="trans-top">
                    <span class="q-badge">{q_id}</span>
                    <span class="trans-vi-text">{escape(vi)}</span>
                </div>
                <div class="trans-hw-lines">
                    <div class="hw-line-full"></div>
                    <div class="hw-line-full"></div>
                </div>
            </div>"""
            items.append(item)
        body_html = f"<div class='trans-list-book'>{''.join(items)}</div>"

    else:
        body_html = f"<p class='generic-hint'>Exercise {ex_num} ({escape(title)})</p>"

    # Wrap complete exercise card
    return f"""
    <section class="book-exercise-section">
        <div class="exercise-header">
            <span class="ex-num-badge">EXERCISE {ex_num}</span>
            <h3 class="ex-title-text">{escape(title.upper())}</h3>
        </div>
        {f'<div class="exercise-instruction">{escape(instruction)}</div>' if instruction else ''}
        <div class="exercise-content-wrap">
            {body_html}
        </div>
    </section>"""


# ==========================================
# RENDER SECTION III: ANSWER KEY
# ==========================================
def render_answer_key_html(exercises_data):
    """
    Renders Section III: Answer Key & Explanations compactly at the end.
    """
    ex_blocks = []
    
    for ex_idx, ex in enumerate(exercises_data):
        ex_num = ex_idx + 1
        title = ex.get("title", f"Exercise {ex_num}")
        ex_type = ex.get("type", "")
        questions = ex.get("questions", [])

        ans_rows = []

        if ex_type in ["multiple_choice", "word_families_mcq", "sentence_ordering_multiple_choice"]:
            # Extract letters A/B/C/D
            for q_idx, q in enumerate(questions):
                qid = q.get("id", str(q_idx + 1))
                options = q.get("options", [])
                correct = q.get("correct_answer", "").strip()
                # Find letter
                letter = ""
                letters = ["A", "B", "C", "D"]
                for oi, opt in enumerate(options):
                    if str(opt).strip().lower() == correct.lower():
                        letter = letters[oi] if oi < len(letters) else str(oi+1)
                        break
                ans_rows.append(f"<span class='key-chip'><strong>{qid}.</strong> {letter or escape(correct)}</span>")

        elif ex_type == "pic_to_word":
            for q_idx, q in enumerate(questions):
                qid = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<span class='key-chip'><strong>{qid}.</strong> {escape(correct)}</span>")

        elif ex_type == "write_english_words":
            c = 1
            for q in questions:
                for p in q.get("parts", []):
                    correct = p.get("correct_answer", "").strip()
                    ans_rows.append(f"<span class='key-chip'><strong>{c}.</strong> {escape(correct)}</span>")
                    c += 1

        elif ex_type == "fill_in_blanks":
            for q_idx, q in enumerate(questions):
                qid = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<span class='key-chip'><strong>{qid}.</strong> {escape(correct)}</span>")

        elif ex_type == "paragraph_fill":
            c = 1
            for p in ex.get("paragraph_parts", []):
                if isinstance(p, dict) and p.get("type") == "blank":
                    bid = p.get("id", str(c))
                    correct = p.get("correct_answer", "").strip()
                    ans_rows.append(f"<span class='key-chip'><strong>({bid})</strong> {escape(correct)}</span>")
                    c += 1

        elif ex_type == "dictionary_entry":
            for e in ex.get("entries", []):
                for q in e.get("questions", []):
                    qid = q.get("id", "")
                    correct = q.get("correct_answer", "").strip()
                    ans_rows.append(f"<span class='key-chip'><strong>#{qid}</strong> {escape(correct)}</span>")

        elif ex_type == "signs_and_notices":
            for q_idx, q in enumerate(questions):
                qid = q.get("id", str(q_idx + 1))
                options = q.get("options", [])
                correct = q.get("correct_answer", "").strip()
                letter = ""
                letters = ["A", "B", "C", "D"]
                for oi, opt in enumerate(options):
                    if str(opt).strip().lower() == correct.lower():
                        letter = letters[oi] if oi < len(letters) else str(oi+1)
                        break
                ans_rows.append(f"<span class='key-chip'><strong>{qid}.</strong> {letter or escape(correct)}</span>")

        elif ex_type == "word_formation":
            for q_idx, q in enumerate(questions):
                qid = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<span class='key-chip'><strong>{qid}.</strong> {escape(correct)}</span>")

        elif ex_type == "translate_sentences":
            for q_idx, q in enumerate(questions):
                qid = q.get("id", str(q_idx + 1))
                correct = q.get("correct_answer", "").strip()
                ans_rows.append(f"<div class='key-line-full'><strong>{qid}.</strong> {escape(correct)}</div>")

        elif ex_type == "word_families_table":
            ans_rows.append("<span class='key-chip'><em>(See Table in Exercise 13)</em></span>")

        if ans_rows:
            is_full = ex_type == "translate_sentences"
            wrap_class = "key-full-wrap" if is_full else "key-grid-chips"
            ex_blocks.append(f"""
            <div class="key-exercise-card">
                <div class="key-ex-title"><strong>EXERCISE {ex_num}:</strong> {escape(title)}</div>
                <div class="{wrap_class}">{''.join(ans_rows)}</div>
            </div>""")

    return f"""
    <section class="book-answer-key-section">
        <div class="section-title-wrap">
            <h2 class="section-title"><span class="sec-num">III.</span> ANSWER KEY &amp; EXPLANATIONS</h2>
            <div class="sec-subtitle">Bảng đáp án và lời giải chi tiết cho 16 dạng bài tập</div>
        </div>
        <div class="key-container-book">
            {''.join(ex_blocks)}
        </div>
    </section>"""


# ==========================================
# MASTER HTML COMPILATION
# ==========================================
def build_book_html(vocab_data, exercises_data, book_name, book_code, unit_num, theme_title, workspace_root, include_answers=True):
    """
    Assembles the complete publication-grade HTML book ready for headless browser PDF conversion.
    """
    theme_upper = theme_title.upper()
    unit_header_str = f"Unit {unit_num} [{theme_upper}]"
    
    # Render sections
    section_1_html = render_vocabulary_cards_html(vocab_data, workspace_root)
    
    exercise_parts = []
    for idx, ex in enumerate(exercises_data):
        exercise_parts.append(render_single_exercise(ex, idx + 1, workspace_root))
    section_2_html = "\n".join(exercise_parts)

    section_3_html = render_answer_key_html(exercises_data) if include_answers else ""

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(book_name)} - Unit {unit_num}: {escape(theme_title)} (PDF Book)</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap" rel="stylesheet">

    <style>
        /* =========================================================
           CSS PAGED MEDIA & TEXTBOOK PRINT STYLES
           ========================================================= */
        @page {{
            size: A4 portrait;
            margin: 14mm 12mm 14mm 12mm;

            @top-left {{
                content: "{escape(book_name).upper()} • UNIT {unit_num}";
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 7.5pt;
                font-weight: 700;
                color: #64748b;
                letter-spacing: 0.5px;
            }}
            @top-right {{
                content: "{escape(theme_upper)}";
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 7.5pt;
                font-weight: 600;
                color: #1e3a8a;
            }}
            @bottom-left {{
                content: "VOCABULARY & PRACTICE EXERCISES";
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 7.5pt;
                color: #94a3b8;
            }}
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 7.5pt;
                font-weight: 600;
                color: #475569;
            }}
        }}

        :root {{
            --primary-navy: #1e3a8a;
            --secondary-blue: #2563eb;
            --accent-blue: #3b82f6;
            --bg-light: #f8fafc;
            --bg-tint: #eff6ff;
            --border-subtle: #cbd5e1;
            --border-divider: #e2e8f0;
            --text-main: #1e293b;
            --text-body: #334155;
            --text-muted: #64748b;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: 'Be Vietnam Pro', system-ui, -apple-system, sans-serif;
            font-size: 9.5pt;
            line-height: 1.45;
            color: var(--text-body);
            background: #ffffff;
        }}

        /* =========================================================
           PAGE BREAK RULES (NO AWKWARD BREAKS)
           ========================================================= */
        .vocab-book-card,
        .book-q-item,
        .dialogue-q-item,
        .oxford-book-entry,
        .table-container-book,
        .word-box-book,
        .paragraph-card-book,
        .pic-to-word-card,
        .write-word-item,
        .key-exercise-card {{
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}

        h1, h2, h3, h4,
        .book-header,
        .section-title-wrap,
        .exercise-header,
        .exercise-instruction,
        .vocab-group-header,
        .wb-header {{
            break-after: avoid !important;
            page-break-after: avoid !important;
        }}

        /* Clean transition for Answer Key */
        .book-answer-key-section {{
            page-break-before: always;
            break-before: always;
        }}

        /* =========================================================
           BOOK COVER / TOP HEADER: Title: Unit * [ĐỀ MỤC]
           ========================================================= */
        .book-header {{
            text-align: center;
            padding-bottom: 12px;
            margin-bottom: 14px;
            border-bottom: 2.5px solid var(--primary-navy);
        }}

        .book-badge {{
            display: inline-block;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 8pt;
            font-weight: 800;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            color: var(--secondary-blue);
            background: var(--bg-tint);
            padding: 3px 12px;
            border-radius: 9999px;
            border: 1px solid #bfdbfe;
            margin-bottom: 6px;
        }}

        .book-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 19pt;
            font-weight: 800;
            color: var(--primary-navy);
            letter-spacing: -0.5px;
            line-height: 1.25;
            margin: 2px 0 4px;
        }}

        .unit-prefix {{
            color: var(--secondary-blue);
            margin-right: 6px;
        }}

        .unit-topic {{
            color: var(--primary-navy);
        }}

        .book-divider {{
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--secondary-blue), transparent);
            margin-top: 6px;
        }}

        /* =========================================================
           SECTION HEADERS: I. Vocabulary & II. Exercises
           ========================================================= */
        .section-title-wrap {{
            margin: 18px 0 10px;
        }}

        .section-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13.5pt;
            font-weight: 800;
            color: var(--primary-navy);
            display: flex;
            align-items: center;
            gap: 8px;
            padding-bottom: 4px;
            border-bottom: 1.5px solid #93c5fd;
        }}

        .sec-num {{
            background: var(--primary-navy);
            color: #ffffff;
            font-size: 9.5pt;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .sec-subtitle {{
            font-size: 8.5pt;
            color: var(--text-muted);
            margin-top: 3px;
        }}

        /* =========================================================
           SECTION I: VOCABULARY CARDS (TEXTBOOK GRID)
           ========================================================= */
        .vocab-group-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 12px 0 8px;
            padding: 4px 8px;
            background: var(--bg-tint);
            border-left: 3.5px solid var(--secondary-blue);
            border-radius: 0 4px 4px 0;
        }}

        .group-num-pill {{
            background: var(--secondary-blue);
            color: #ffffff;
            font-weight: 700;
            font-size: 8pt;
            padding: 1px 6px;
            border-radius: 9999px;
        }}

        .group-title-text {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 9.5pt;
            font-weight: 700;
            color: var(--primary-navy);
        }}

        .group-count {{
            font-size: 8pt;
            color: var(--text-muted);
        }}

        .vocab-grid-book {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 12px;
        }}

        .vocab-book-card {{
            border: 1px solid var(--border-divider);
            border-radius: 14px;
            background: #ffffff;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}

        .card-img-wrap {{
            position: relative;
            width: 100%;
            height: 82px;
            background: var(--bg-light);
            overflow: hidden;
        }}

        .card-img-wrap img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .btn-speaker-mini {{
            position: absolute;
            right: 5px;
            bottom: 5px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #ffffff;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.18);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--secondary-blue);
        }}

        .card-body {{
            padding: 7px 9px 9px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }}

        .word-header-row {{
            display: flex;
            flex-direction: column;
            margin-bottom: 2px;
        }}

        .word-en {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 10pt;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.2;
        }}

        .word-ipa {{
            font-size: 7.8pt;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--secondary-blue);
            font-weight: 600;
            margin-top: 1px;
        }}

        .card-divider {{
            height: 1px;
            background: #f1f5f9;
            margin: 5px 0 4px;
        }}

        .word-vi-def {{
            font-size: 8pt;
            font-weight: 500;
            color: var(--text-body);
            line-height: 1.28;
        }}

        /* =========================================================
           SECTION II: PRACTICE EXERCISES
           ========================================================= */
        .book-exercise-section {{
            margin-top: 14px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
        }}

        .exercise-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }}

        .ex-num-badge {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 8pt;
            font-weight: 800;
            background: var(--primary-navy);
            color: #ffffff;
            padding: 2px 7px;
            border-radius: 3px;
            letter-spacing: 0.5px;
        }}

        .ex-title-text {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 10.5pt;
            font-weight: 700;
            color: var(--primary-navy);
            letter-spacing: -0.2px;
        }}

        .exercise-instruction {{
            font-size: 8.8pt;
            font-style: italic;
            color: var(--text-muted);
            margin-bottom: 8px;
            padding-left: 2px;
        }}

        .exercise-content-wrap {{
            margin-top: 6px;
        }}

        /* Common Question Items */
        .book-q-item {{
            margin-bottom: 7px;
            padding: 4px 6px;
            border-radius: 4px;
            background: #ffffff;
        }}

        .q-stem-row {{
            display: flex;
            align-items: flex-start;
            gap: 6px;
            margin-bottom: 4px;
        }}

        .q-badge {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 7.8pt;
            font-weight: 700;
            color: var(--secondary-blue);
            background: var(--bg-tint);
            border: 1px solid #bfdbfe;
            min-width: 20px;
            height: 18px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 9999px;
            flex-shrink: 0;
            margin-top: 1px;
        }}

        .q-stem-text {{
            font-size: 9.2pt;
            line-height: 1.35;
            color: var(--text-main);
            flex-grow: 1;
        }}

        .underline-word {{
            text-decoration: underline;
            text-underline-offset: 2px;
            color: var(--primary-navy);
        }}

        /* MCQ Options Layout */
        .book-options-grid {{
            display: grid;
            gap: 4px 10px;
            margin-left: 26px;
        }}

        .opts-col-4 {{
            grid-template-columns: repeat(4, 1fr);
        }}

        .opts-col-2 {{
            grid-template-columns: repeat(2, 1fr);
        }}

        .opts-col-1 {{
            grid-template-columns: 1fr;
        }}

        .book-option-item {{
            display: flex;
            align-items: flex-start;
            gap: 5px;
            font-size: 8.8pt;
            line-height: 1.3;
        }}

        .opt-letter {{
            color: var(--primary-navy);
            font-family: 'Plus Jakarta Sans', sans-serif;
            flex-shrink: 0;
        }}

        .opt-body {{
            color: var(--text-body);
        }}

        /* Dialogue Box */
        .dialogue-box {{
            background: var(--bg-light);
            border-left: 3px solid var(--secondary-blue);
            padding: 5px 8px;
            border-radius: 0 4px 4px 0;
            flex-grow: 1;
            margin-bottom: 4px;
        }}

        .dialogue-line {{
            font-size: 8.8pt;
            line-height: 1.35;
            margin-bottom: 2px;
        }}

        .speaker-tag {{
            color: var(--primary-navy);
            margin-right: 4px;
        }}

        /* Responsive Handwriting Lines */
        .hw-line {{
            border-bottom: 1.2px dotted #94a3b8;
            width: 85%;
            margin: 6px auto 2px;
            height: 12px;
        }}

        .hw-line-flex {{
            border-bottom: 1.2px dotted #cbd5e1;
            flex-grow: 1;
            height: 14px;
            margin-left: 8px;
        }}

        .hw-line-full {{
            border-bottom: 1.2px dotted #cbd5e1;
            width: 100%;
            height: 18px;
            margin-top: 2px;
        }}

        .inline-hw-blank {{
            display: inline-block;
            border-bottom: 1.2px dotted var(--primary-navy);
            min-width: 60px;
            height: 14px;
            margin: 0 3px;
            vertical-align: middle;
        }}

        /* Word Box */
        .word-box-book {{
            background: #f0f7ff;
            border: 1px dashed var(--secondary-blue);
            border-radius: 6px;
            padding: 6px 10px;
            margin-bottom: 8px;
        }}

        .wb-header {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 8pt;
            font-weight: 700;
            color: var(--primary-navy);
            margin-bottom: 4px;
        }}

        .wb-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}

        .wb-chip {{
            background: #ffffff;
            border: 1px solid #bfdbfe;
            color: var(--primary-navy);
            font-weight: 600;
            font-size: 8pt;
            padding: 2px 7px;
            border-radius: 4px;
        }}

        /* Picture to Word Grid (Balanced 4-column layout) */
        .pic-grid-book {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 10px;
        }}

        .pic-to-word-card {{
            border: 1px solid var(--border-divider);
            border-radius: 4px;
            padding: 5px;
            text-align: center;
            background: #ffffff;
        }}

        .pic-box {{
            position: relative;
            height: 62px;
            background: var(--bg-light);
            border-radius: 3px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 4px;
        }}

        .pic-box img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}

        .pic-q-badge {{
            position: absolute;
            top: 2px;
            left: 2px;
            background: var(--primary-navy);
            color: #ffffff;
            font-size: 6.8pt;
            font-weight: 700;
            padding: 1px 4px;
            border-radius: 2px;
        }}

        /* Write Words List (2 Balanced Columns) */
        .write-words-list-book {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 6px 16px;
        }}

        .write-word-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 8.8pt;
        }}

        .vi-prompt {{
            color: var(--text-main);
            font-weight: 500;
            flex-shrink: 0;
            max-width: 55%;
        }}

        /* Paragraph Fill */
        .paragraph-card-book {{
            background: #ffffff;
            border: 1px solid var(--border-divider);
            border-radius: 6px;
            padding: 10px 12px;
            line-height: 1.85;
            font-size: 9.2pt;
        }}

        .para-inline-slot {{
            display: inline-block;
            white-space: nowrap;
            margin: 0 2px;
        }}

        /* Sentence Ordering */
        .sentence-order-ul {{
            list-style: none;
            margin-bottom: 4px;
        }}

        .order-li {{
            font-size: 8.8pt;
            line-height: 1.35;
            margin-bottom: 2px;
        }}

        /* Oxford Dictionary Entry */
        .dict-entries-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .oxford-book-entry {{
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 8px 10px;
            background: #ffffff;
        }}

        .dict-top-bar {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
            padding-bottom: 3px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .dict-headword {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11pt;
            font-weight: 800;
            color: var(--primary-navy);
        }}

        .dict-pos-pill {{
            font-size: 7.5pt;
            font-style: italic;
            color: #475569;
            background: #f1f5f9;
            padding: 1px 6px;
            border-radius: 3px;
        }}

        .dict-ipa-pill {{
            font-size: 8pt;
            color: var(--secondary-blue);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .dict-definition {{
            font-size: 8.8pt;
            margin-bottom: 5px;
            color: var(--text-main);
        }}

        .dict-colloc-label {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 7.8pt;
            font-weight: 700;
            color: var(--secondary-blue);
            margin-bottom: 2px;
            text-transform: uppercase;
        }}

        .dict-ul {{
            margin-left: 16px;
            font-size: 8.3pt;
            color: #475569;
            margin-bottom: 6px;
        }}

        .dict-sub-q {{
            display: flex;
            gap: 5px;
            font-size: 8.5pt;
            margin-bottom: 3px;
        }}

        .sub-q-num {{
            font-weight: 700;
            color: var(--secondary-blue);
        }}

        /* Signs & Notices */
        .signs-list-book {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .sign-top-row {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 4px;
        }}

        .sign-board-book {{
            background: #fefce8;
            border: 1.5px solid #eab308;
            border-radius: 4px;
            padding: 5px 8px;
            flex-grow: 1;
        }}

        .sign-icon {{
            font-size: 7.5pt;
            font-weight: 800;
            color: #854d0e;
            margin-bottom: 2px;
            letter-spacing: 0.5px;
        }}

        .sign-text-content {{
            font-size: 8.8pt;
            font-weight: 600;
            color: #713f12;
            line-height: 1.3;
        }}

        .sign-question-stem {{
            font-size: 8.8pt;
            margin-left: 28px;
            margin-bottom: 3px;
            color: var(--text-main);
        }}

        /* Word Families Table */
        .table-container-book {{
            margin: 6px 0 10px;
        }}

        .wf-table-book {{
            width: 100%;
            border-collapse: collapse;
            font-size: 8.5pt;
        }}

        .wf-table-book th {{
            background: var(--primary-navy);
            color: #ffffff;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            text-align: left;
            padding: 4px 8px;
            border: 1px solid var(--primary-navy);
        }}

        .wf-table-book td {{
            padding: 4px 8px;
            border: 1px solid #cbd5e1;
            color: var(--text-body);
        }}

        .wf-table-book tbody tr:nth-child(even) {{
            background: var(--bg-light);
        }}

        .tag-pos {{
            font-size: 7.5pt;
            color: #64748b;
        }}

        /* Word Formation */
        .wf-formation-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .wf-stem-wrap {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            font-size: 9pt;
        }}

        .wf-root-tag {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            color: var(--primary-navy);
            background: var(--bg-tint);
            border: 1px solid #bfdbfe;
            padding: 1px 7px;
            border-radius: 3px;
            font-size: 8pt;
            margin-left: 8px;
            flex-shrink: 0;
        }}

        /* Translation */
        .trans-list-book {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .trans-top {{
            display: flex;
            align-items: flex-start;
            gap: 6px;
            margin-bottom: 3px;
        }}

        .trans-vi-text {{
            font-size: 9pt;
            font-weight: 500;
            color: var(--text-main);
            line-height: 1.35;
        }}

        .trans-hw-lines {{
            margin-left: 26px;
        }}

        /* =========================================================
           SECTION III: ANSWER KEY
           ========================================================= */
        .key-container-book {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }}

        .key-exercise-card {{
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 6px 8px;
            background: #ffffff;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }}

        .key-ex-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 8.5pt;
            color: var(--primary-navy);
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 3px;
            margin-bottom: 5px;
        }}

        .key-grid-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px 6px;
        }}

        .key-chip {{
            background: var(--bg-light);
            border: 1px solid #e2e8f0;
            border-radius: 3px;
            padding: 1px 5px;
            font-size: 7.8pt;
            color: #1e293b;
        }}

        .key-full-wrap {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .key-line-full {{
            font-size: 7.8pt;
            line-height: 1.3;
            color: #334155;
            padding: 2px 4px;
            background: #f8fafc;
            border-radius: 3px;
        }}
    </style>
</head>
<body>

    <!-- BOOK HEADER: Title: Unit * [ĐỀ MỤC] -->
    <header class="book-header">
        <div class="book-badge">{escape(book_name)} • UNIT {unit_num}</div>
        <h1 class="book-title"><span class="unit-prefix">Unit {unit_num}</span> <span class="unit-topic">[{escape(theme_upper)}]</span></h1>
        <div class="book-divider"></div>
    </header>

    <!-- SECTION I: VOCABULARY THEORY CARDS -->
    <section class="book-vocabulary-section">
        <div class="section-title-wrap">
            <h2 class="section-title"><span class="sec-num">I.</span> VOCABULARY</h2>
            <div class="sec-subtitle">Hệ thống từ vựng trọng tâm theo chủ đề kèm phiên âm chuẩn, định nghĩa và ngữ cảnh minh hoạ</div>
        </div>
        <div class="vocab-theory-content">
            {section_1_html}
        </div>
    </section>

    <!-- SECTION II: PRACTICE EXERCISES -->
    <section class="book-exercises-master-section">
        <div class="section-title-wrap">
            <h2 class="section-title"><span class="sec-num">II.</span> EXERCISES</h2>
            <div class="sec-subtitle">Hệ thống 16 dạng bài tập củng cố và phát triển năng lực từ vựng toàn diện</div>
        </div>
        <div class="exercises-master-content">
            {section_2_html}
        </div>
    </section>

    <!-- SECTION III: ANSWER KEY -->
    {section_3_html}

</body>
</html>"""
    return html_content


# ==========================================
# BROWSER DETECTION & PDF COMPILATION
# ==========================================
def find_headless_browser():
    """Locate Chrome or Edge executable on the host system."""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "msedge",
        "google-chrome",
        "chromium",
        "chrome"
    ]
    for c in candidates:
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        else:
            cmd = "where.exe" if os.name == "nt" else "which"
            res = subprocess.run([cmd, c], capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip().splitlines()[0]
    return None


def export_html_to_pdf(html_path, pdf_path, browser_executable=None):
    """Convert HTML to PDF using Chrome/Edge headless."""
    browser = browser_executable or find_headless_browser()
    if not browser:
        print("[Error] No Chrome or Edge executable found to render PDF.", file=sys.stderr)
        return False

    abs_html = Path(html_path).resolve()
    abs_pdf = Path(pdf_path).resolve()
    abs_pdf.parent.mkdir(parents=True, exist_ok=True)

    file_url = abs_html.as_uri()

    flags = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        file_url
    ]

    print(f"Rendering PDF with browser: {browser}...")
    res = subprocess.run(flags, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[Warning] Headless browser returned code {res.returncode}: {res.stderr}", file=sys.stderr)

    if abs_pdf.exists() and abs_pdf.stat().st_size > 0:
        return True
    return False


# ==========================================
# MAIN WORKFLOW
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Generate publication-grade Vocabulary & Exercises PDF Book.")
    parser.add_argument("input_path", nargs="?", default="lessons/unit-1", help="Path to unit folder (e.g., lessons/unit-1) or vocab folder.")
    parser.add_argument("--output-pdf", "-op", help="Custom target PDF file path.")
    parser.add_argument("--output-html", "-oh", help="Custom target HTML file path.")
    parser.add_argument("--no-answers", action="store_true", help="Do not include Answer Key at the end.")
    parser.add_argument("--browser", help="Explicit path to Chrome or Edge executable.")
    args = parser.parse_args()

    vocab_dir, unit_dir, book_name, book_code, unit_num, theme_title = resolve_unit_info(args.input_path)
    workspace_root = find_workspace_root(unit_dir)

    print(f"=== VOCABULARY & EXERCISES PDF BOOK BUILDER ===")
    print(f"Unit Directory   : {unit_dir}")
    print(f"Book & Unit      : {book_name} - Unit {unit_num}")
    print(f"Theme / Đề mục   : {theme_title}")

    # 1. Load vocab.json
    vocab_json_path = vocab_dir / "vocab.json"
    if not vocab_json_path.exists():
        print(f"[Error] Missing vocab.json at {vocab_json_path}", file=sys.stderr)
        sys.exit(1)
    vocab_data = load_json(vocab_json_path) or []

    # 2. Load all 16 exercise JSONs
    ex_dir = vocab_dir / "exercises"
    ex_files = sorted(glob.glob(str(ex_dir / "*.json")))
    exercises_data = []
    for ef in ex_files:
        d = load_json(ef)
        if d:
            exercises_data.append(d)

    print(f"Loaded {len(vocab_data)} vocab groups and {len(exercises_data)} exercise sets.")

    # 3. Compile Master HTML
    html_content = build_book_html(
        vocab_data=vocab_data,
        exercises_data=exercises_data,
        book_name=book_name,
        book_code=book_code,
        unit_num=unit_num,
        theme_title=theme_title,
        workspace_root=workspace_root,
        include_answers=not args.no_answers
    )

    # Output paths: save in vocab/ and also unit root for easy access
    default_html_name = f"vocab_unit{unit_num}.html"
    default_pdf_name = f"vocab_unit{unit_num}.pdf"

    target_html = Path(args.output_html).resolve() if args.output_html else (vocab_dir / default_html_name)
    target_pdf = Path(args.output_pdf).resolve() if args.output_pdf else (vocab_dir / default_pdf_name)

    # Write HTML file
    with open(target_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML Book: {target_html} ({target_html.stat().st_size:,} bytes)")

    # 4. Convert HTML to PDF
    success = export_html_to_pdf(target_html, target_pdf, browser_executable=args.browser)
    if success:
        size_mb = target_pdf.stat().st_size / (1024 * 1024)
        print(f"SUCCESS: Generated PDF Book at: {target_pdf} ({size_mb:.2f} MB)")
        try:
            import fitz
            doc = fitz.open(str(target_pdf))
            print(f"Total Pages in PDF: {len(doc)} pages")
        except Exception:
            pass
    else:
        print(f"[Error] Failed to convert PDF. Please inspect HTML at {target_html}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
