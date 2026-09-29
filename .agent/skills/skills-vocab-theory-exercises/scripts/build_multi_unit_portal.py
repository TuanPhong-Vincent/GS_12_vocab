#!/usr/bin/env python3
"""
Multi-Unit Vocabulary & Exercises Master Portal Builder (build_multi_unit_portal.py)

Generates:
1. `d:/GS12/index.html`: Unified Master Portal combining all 3 units in lessons:
   - Unit 1: Life Stories We Admire
   - Unit 2: A Multicultural World
   - Unit 3: Green Living
   With:
   - Top Unit Switcher (Unit 1 | Unit 2 | Unit 3 | Tất Cả 3 Units)
   - Tab filter (Tất Cả | Lý Thuyết Cards | Bài Tập 16 Dạng)
   - Interactive Review vs Practice modes
   - Real-time Live Search
   - Web Speech API US voice pronunciation
   - Per-unit sidebar navigation & statistics
   - Exact cards.html visual specifications
   - Uniform exercise title colors (#1e3a8a) & aligned form controls
   - Direct links to each unit's standalone index.html and cards.html
2. `d:/GS12/cards.html`: Master Vocabulary Flashcards page for all 3 units.
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


FALLBACK_SVG = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='1.5'><rect x='3' y='3' width='18' height='18' rx='2'/><circle cx='8.5' cy='8.5' r='1.5'/><path d='M21 15l-5-5L5 21'/></svg>"


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed to read {file_path}: {e}", file=sys.stderr)
        return None


def resolve_asset_relpath(asset_path_str, output_html_file, workspace_root):
    if not asset_path_str:
        return ""
    if asset_path_str.startswith("http://") or asset_path_str.startswith("https://"):
        return asset_path_str

    clean_path = asset_path_str.lstrip("/\\")
    abs_target = workspace_root / clean_path
    out_dir = Path(output_html_file).resolve().parent
    try:
        rel = os.path.relpath(abs_target, out_dir).replace("\\", "/")
        return rel
    except Exception:
        return clean_path.replace("\\", "/")


def highlight_target_word(text):
    if not text:
        return ""
    return re.sub(r"\[([^\]]+)\]", r"<span class='target-word'>\1</span>", escape(text))


def render_single_exercise_inner(ex, ex_idx, u_prefix, output_file, workspace_root):
    ex_type = ex.get("type", "")
    questions = ex.get("questions", [])

    # 1. Multiple Choice
    if ex_type in ["multiple_choice", "word_families_mcq", "sentence_ordering_multiple_choice"]:
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            sentences = q.get("sentences", [])
            options = q.get("options", [])
            correct = q.get("correct_answer", "").strip()

            if "\n" in raw_text:
                dialogue_lines = raw_text.split("\n")
                formatted_stem = "<div class='dialogue-box'>" + "".join(
                    f"<div class='dialogue-line'>{highlight_target_word(line)}</div>" for line in dialogue_lines if line.strip()
                ) + "</div>"
            elif sentences:
                s_list = "".join(f"<li class='order-item'>{escape(s)}</li>" for s in sentences)
                formatted_stem = f"<ol class='sentence-order-list'>{s_list}</ol>"
            else:
                formatted_stem = f"<div class='question-stem'>{highlight_target_word(raw_text)}</div>"

            option_letters = ["A", "B", "C", "D"]
            opt_htmls = []
            for opt_i, opt in enumerate(options):
                letter = option_letters[opt_i] if opt_i < len(option_letters) else str(opt_i + 1)
                opt_str = str(opt).strip()
                is_correct = (opt_str.lower() == correct.lower())
                radio_name = f"{u_prefix}_ex_{ex_idx}_q_{q_idx}"
                opt_id = f"opt_{u_prefix}_{ex_idx}_{q_idx}_{opt_i}"

                opt_card = f"""
                <label class="option-label" for="{opt_id}" data-is-correct="{'true' if is_correct else 'false'}">
                    <input type="radio" name="{radio_name}" id="{opt_id}" value="{escape(opt_str)}" onchange="markSelected(this)">
                    <span class="option-badge">{letter}</span>
                    <span class="option-text">{escape(opt_str)}</span>
                    <span class="check-icon">✓</span>
                </label>"""
                opt_htmls.append(opt_card)

            item_html = f"""
            <div class="question-row" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="q-header">
                    <span class="q-num">Câu {escape(str(q_id))}</span>
                    <div class="q-content">{formatted_stem}</div>
                </div>
                <div class="options-grid">
                    {''.join(opt_htmls)}
                </div>
                <div class="q-feedback" id="feedback_{u_prefix}_{ex_idx}_{q_idx}" style="display:none;"></div>
            </div>"""
            items.append(item_html)
        return "\n".join(items)

    # 2. Picture to Word (04)
    elif ex_type == "pic_to_word":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            img_raw = q.get("image", "")
            img_rel = resolve_asset_relpath(img_raw, output_file, workspace_root)
            correct = q.get("correct_answer", "").strip()

            card = f"""
            <div class="pic-word-card" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="pic-wrapper">
                    <img src="{escape(img_rel)}" alt="Question {q_id}" loading="lazy" onerror="this.onerror=null; this.src='{FALLBACK_SVG}'; this.style.padding='30px';">
                    <span class="pic-tag">#{q_id}</span>
                </div>
                <div class="pic-controls">
                    <input type="text" class="tidy-input pic-input" id="input_{u_prefix}_{ex_idx}_{q_idx}" placeholder="Nhập từ tiếng Anh..." autocomplete="off">
                    <div class="answer-badge" id="ans_badge_{u_prefix}_{ex_idx}_{q_idx}" style="display:none;">
                        <span>Đáp án:</span> <strong>{escape(correct)}</strong>
                    </div>
                </div>
            </div>"""
            items.append(card)
        return f"<div class='pic-grid'>{''.join(items)}</div>"

    # 3. Write English Words (05)
    elif ex_type == "write_english_words":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            parts = q.get("parts", [])
            sub_items = []
            for p_idx, part in enumerate(parts):
                vi = part.get("vietnamese", "")
                correct = part.get("correct_answer", "").strip()
                sub = f"""
                <div class="write-part-row" data-sub-idx="{p_idx}" data-correct="{escape(correct)}">
                    <div class="part-vi">🇻🇳 {escape(vi)}</div>
                    <div class="part-input-wrap">
                        <input type="text" class="tidy-input write-input" id="input_{u_prefix}_{ex_idx}_{q_idx}_{p_idx}" placeholder="Viết từ tiếng Anh tương ứng..." autocomplete="off">
                        <span class="sub-ans-reveal" id="sub_ans_{u_prefix}_{ex_idx}_{q_idx}_{p_idx}" style="display:none;">{escape(correct)}</span>
                    </div>
                </div>"""
                sub_items.append(sub)

            card = f"""
            <div class="question-row write-group" data-q-idx="{q_idx}">
                <div class="q-header">
                    <span class="q-num">Mục {escape(str(q_id))}</span>
                </div>
                <div class="parts-wrap">
                    {''.join(sub_items)}
                </div>
            </div>"""
            items.append(card)
        return "\n".join(items)

    # 4. Fill in the Blanks (06)
    elif ex_type == "fill_in_blanks":
        word_box = ex.get("word_box", [])
        box_pills = "".join(f"<span class='word-box-chip'>{escape(w)}</span>" for w in word_box)
        box_html = f"""
        <div class="word-box-container">
            <div class="word-box-label">📦 TỪ GỢI Ý (WORD BOX):</div>
            <div class="word-box-chips">{box_pills}</div>
        </div>"""

        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            correct = q.get("correct_answer", "").strip()

            input_html = f"<input type='text' class='tidy-input inline-blank' id='input_{u_prefix}_{ex_idx}_{q_idx}' placeholder='...' autocomplete='off' data-correct='{escape(correct)}'>"
            formatted_sentence = re.sub(r"_{2,}", input_html, escape(raw_text))

            row = f"""
            <div class="question-row blank-row" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="q-header">
                    <span class="q-num">Câu {escape(str(q_id))}</span>
                    <div class="blank-sentence">{formatted_sentence}</div>
                </div>
                <div class="inline-ans-reveal" id="blank_ans_{u_prefix}_{ex_idx}_{q_idx}" style="display:none;">Đáp án: <strong>{escape(correct)}</strong></div>
            </div>"""
            items.append(row)

        return box_html + "\n<div class='blanks-list'>" + "\n".join(items) + "</div>"

    # 5. Paragraph Fill (07)
    elif ex_type == "paragraph_fill":
        word_box = ex.get("word_box", [])
        box_pills = "".join(f"<span class='word-box-chip'>{escape(w)}</span>" for w in word_box)
        box_html = f"""
        <div class="word-box-container">
            <div class="word-box-label">📦 TỪ GỢI Ý ĐIỀN ĐOẠN VĂN:</div>
            <div class="word-box-chips">{box_pills}</div>
        </div>"""

        parts = ex.get("paragraph_parts", [])
        flow_spans = []
        blank_counter = 0

        for part in parts:
            if isinstance(part, str):
                flow_spans.append(f"<span>{escape(part)}</span>")
            elif isinstance(part, dict) and part.get("type") == "blank":
                b_id = part.get("id", str(blank_counter + 1))
                b_correct = part.get("correct_answer", "").strip()
                inp = f"""<span class="inline-slot" data-blank-id="{b_id}" data-correct="{escape(b_correct)}">
                    <span class="slot-num">({b_id})</span>
                    <input type="text" class="tidy-input para-input" id="para_input_{u_prefix}_{ex_idx}_{blank_counter}" placeholder="..." autocomplete="off">
                    <span class="para-key" id="para_key_{u_prefix}_{ex_idx}_{blank_counter}" style="display:none;">{escape(b_correct)}</span>
                </span>"""
                flow_spans.append(inp)
                blank_counter += 1

        passage_html = f"""
        <div class="paragraph-flow-card">
            <div class="passage-text">
                {''.join(flow_spans)}
            </div>
        </div>"""
        return box_html + passage_html

    # 6. Dictionary Entries (11)
    elif ex_type == "dictionary_entry":
        entries = ex.get("entries", [])
        entry_cards = []
        for e_idx, entry in enumerate(entries):
            e_id = entry.get("id", str(e_idx + 1))
            word = entry.get("word", "")
            pos = entry.get("part_of_speech", "")
            pr = entry.get("pronunciation", "")
            definition = entry.get("definition", "")
            bullets = entry.get("bullet_points", [])
            q_list = entry.get("questions", [])

            bullet_lis = "".join(f"<li>{highlight_target_word(b)}</li>" for b in bullets)

            q_rows = []
            for q_idx, q in enumerate(q_list):
                q_id = q.get("id", str(q_idx + 1))
                q_text = q.get("text", "")
                correct = q.get("correct_answer", "").strip()
                inp = f"<input type='text' class='tidy-input dict-blank' id='dict_inp_{u_prefix}_{ex_idx}_{e_idx}_{q_idx}' placeholder='...' autocomplete='off' data-correct='{escape(correct)}'>"
                formatted_q = re.sub(r"_{2,}", inp, escape(q_text))

                q_rows.append(f"""
                <div class="dict-question-item" data-correct="{escape(correct)}">
                    <span class="dict-q-num">#{q_id}</span>
                    <div class="dict-q-body">{formatted_q}</div>
                    <div class="dict-ans-reveal" id="dict_ans_{u_prefix}_{ex_idx}_{e_idx}_{q_idx}" style="display:none;">Đáp án: <strong>{escape(correct)}</strong></div>
                </div>""")

            card = f"""
            <div class="oxford-dict-card">
                <div class="dict-head">
                    <div class="dict-word-title">{escape(word)}</div>
                    <span class="dict-pos-tag">{escape(pos)}</span>
                    <span class="dict-ipa">{escape(pr)}</span>
                </div>
                <div class="dict-def">{escape(definition)}</div>
                <div class="dict-collocs">
                    <div class="dict-collocs-title">Collocations & Contextual Usages:</div>
                    <ul class="dict-bullets-list">{bullet_lis}</ul>
                </div>
                <div class="dict-practice-section">
                    <div class="dict-practice-title">📝 Practice Sentences:</div>
                    {''.join(q_rows)}
                </div>
            </div>"""
            entry_cards.append(card)

        return "\n".join(entry_cards)

    # 7. Signs and Notices (12)
    elif ex_type == "signs_and_notices":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            sign_text = q.get("sign_text", "")
            sign_img_raw = q.get("sign_image", "")
            question_stem = q.get("question", "What does this sign mean?")
            options = q.get("options", [])
            correct = q.get("correct_answer", "").strip()

            sign_img_rel = resolve_asset_relpath(sign_img_raw, output_file, workspace_root)

            # Visual sign simulation box or actual sign image
            target_sign_path = (workspace_root / sign_img_raw.lstrip("/\\")) if sign_img_raw else None
            if sign_img_rel and target_sign_path and target_sign_path.exists():
                sign_preview = f"""
            <div class="sign-board has-image">
                <img src="{escape(sign_img_rel)}" alt="Sign #{escape(str(q_id))}" class="sign-img-view" loading="lazy">
            </div>"""
            else:
                sign_preview = f"""
            <div class="sign-board">
                <div class="sign-icon-circle">🪧</div>
                <div class="sign-desc">{escape(sign_text)}</div>
            </div>"""

            option_letters = ["A", "B", "C", "D"]
            opt_htmls = []
            for opt_i, opt in enumerate(options):
                letter = option_letters[opt_i] if opt_i < len(option_letters) else str(opt_i + 1)
                opt_str = str(opt).strip()
                is_correct = (opt_str.lower() == correct.lower())
                radio_name = f"{u_prefix}_ex_{ex_idx}_sign_{q_idx}"
                opt_id = f"opt_sign_{u_prefix}_{ex_idx}_{q_idx}_{opt_i}"

                opt_card = f"""
                <label class="option-label" for="{opt_id}" data-is-correct="{'true' if is_correct else 'false'}">
                    <input type="radio" name="{radio_name}" id="{opt_id}" value="{escape(opt_str)}" onchange="markSelected(this)">
                    <span class="option-badge">{letter}</span>
                    <span class="option-text">{escape(opt_str)}</span>
                    <span class="check-icon">✓</span>
                </label>"""
                opt_htmls.append(opt_card)

            row = f"""
            <div class="question-row sign-row" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="q-header">
                    <span class="q-num">Biển báo #{escape(str(q_id))}</span>
                </div>
                <div class="sign-layout">
                    {sign_preview}
                    <div class="sign-qa">
                        <div class="question-stem"><strong>{escape(question_stem)}</strong></div>
                        <div class="options-grid">
                            {''.join(opt_htmls)}
                        </div>
                    </div>
                </div>
                <div class="q-feedback" id="feedback_{u_prefix}_{ex_idx}_{q_idx}" style="display:none;"></div>
            </div>"""
            items.append(row)
        return "\n".join(items)

    # 8. Word Families Table (13)
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
            <tr>
                <td><span class="base-chip">{escape(base_word)}</span> <span class="base-type-tag">({escape(base_type)})</span></td>
                <td><span class="wf-val">{escape(verbs)}</span></td>
                <td><span class="wf-val">{escape(nouns)}</span></td>
                <td><span class="wf-val">{escape(adjs)}</span></td>
                <td><span class="wf-val">{escape(advs)}</span></td>
            </tr>"""
            rows.append(tr)

        table_html = f"""
        <div class="table-responsive">
            <table class="wf-table">
                <thead>
                    <tr>
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
            </table>
        </div>"""
        return table_html

    # 9. Word Formation (15)
    elif ex_type == "word_formation":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            base = q.get("base_word", "")
            correct = q.get("correct_answer", "").strip()

            input_html = f"<input type='text' class='tidy-input inline-blank' id='wf_input_{u_prefix}_{ex_idx}_{q_idx}' placeholder='...' autocomplete='off' data-correct='{escape(correct)}'>"
            formatted_sentence = re.sub(r"_{2,}", input_html, escape(raw_text))

            row = f"""
            <div class="question-row wf-item-row" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="q-header">
                    <span class="q-num">Câu {escape(str(q_id))}</span>
                    <div class="blank-sentence">{formatted_sentence} <span class="root-badge">[{escape(base)}]</span></div>
                </div>
                <div class="inline-ans-reveal" id="wf_ans_{u_prefix}_{ex_idx}_{q_idx}" style="display:none;">Đáp án đúng: <strong>{escape(correct)}</strong></div>
            </div>"""
            items.append(row)
        return "\n".join(items)

    # 10. Sentence Translation (16)
    elif ex_type == "translate_sentences":
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            vi = q.get("vietnamese", "")
            en_correct = q.get("correct_answer", "").strip()

            row = f"""
            <div class="question-row trans-row" data-q-idx="{q_idx}" data-correct="{escape(en_correct)}">
                <div class="q-header">
                    <span class="q-num">Câu {escape(str(q_id))}</span>
                    <div class="trans-vi-prompt">🇻🇳 {escape(vi)}</div>
                </div>
                <div class="trans-input-box">
                    <textarea class="tidy-textarea trans-textarea" id="trans_input_{u_prefix}_{ex_idx}_{q_idx}" placeholder="Nhập câu dịch tiếng Anh của bạn..." rows="2"></textarea>
                    <div class="trans-reveal-box" id="trans_key_{u_prefix}_{ex_idx}_{q_idx}" style="display:none;">
                        <span class="trans-key-label">🇬🇧 Đáp án chuẩn:</span>
                        <div class="trans-key-text">{escape(en_correct)}</div>
                    </div>
                </div>
            </div>"""
            items.append(row)
        return "\n".join(items)

    return "<p class='empty-hint'>Định dạng bài tập đang được hoàn thiện.</p>"


def render_all_exercises_html(exercises_data, u_prefix, output_file, workspace_root):
    rendered_blocks = []
    for ex_idx, ex in enumerate(exercises_data):
        ex_id = ex.get("id", str(ex_idx + 1))
        ex_type = ex.get("type", "")
        ex_title = ex.get("title", f"Exercise {ex_idx+1}")
        ex_desc = ex.get("description", "")
        file_name = ex.get("_filename", "")

        body_html = render_single_exercise_inner(ex, ex_idx, u_prefix, output_file, workspace_root)

        block = f"""
        <!-- Exercise Card {u_prefix}-{ex_id}: {escape(ex_title)} -->
        <div class="exercise-card" id="exercise-block-{u_prefix}-{ex_idx}" data-u-prefix="{u_prefix}" data-ex-idx="{ex_idx}" data-ex-type="{escape(ex_type)}">
            <div class="exercise-header">
                <div class="exercise-title-group">
                    <div class="badge-row">
                        <span class="ex-num-badge">Bài #{escape(str(ex_id))}</span>
                        <span class="ex-type-pill">{escape(ex_type.replace('_', ' ').upper())}</span>
                        <span class="ex-file-tag">{escape(file_name)}</span>
                    </div>
                    <h3 class="exercise-title">{escape(ex_title)}</h3>
                    <p class="exercise-description">{escape(ex_desc)}</p>
                </div>
                <div class="exercise-actions">
                    <span class="score-pill" id="score-pill-{u_prefix}-{ex_idx}" style="display:none;"></span>
                    <button type="button" class="btn-check" onclick="checkExercise('{u_prefix}', {ex_idx})">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                        Kiểm Tra
                    </button>
                    <button type="button" class="btn-reset" onclick="resetExercise('{u_prefix}', {ex_idx})" title="Làm lại bài này">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                            <path d="M3 3v5h5"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="exercise-body">
                {body_html}
            </div>
        </div>"""
        rendered_blocks.append(block)

    return "\n".join(rendered_blocks)


def render_unit_vocab_cards_html(vocab_data, u_prefix, output_file, workspace_root):
    vocab_cards_html = []
    for g_idx, group in enumerate(vocab_data):
        g_name = group.get("group", f"Nhóm {g_idx+1}")
        words = group.get("words", [])

        cards_in_group = []
        for word in words:
            en_word = word.get("english_word", "").strip()
            ipa = word.get("pronunciation_british") or word.get("pronunciation_american") or ""
            meaning = word.get("vietnamese_meaning", "").strip()
            img_raw = word.get("image", "")
            img_rel = resolve_asset_relpath(img_raw, output_file, workspace_root)
            alt_text = word.get("alt") or en_word
            safe_word = en_word.replace("'", "\\'")

            card = f"""
            <div class="vocab-card" data-word="{escape(en_word.lower())}" data-group="{escape(g_name.lower())}">
                <div class="image-container">
                    <img src="{escape(img_rel)}" alt="{escape(alt_text)}" loading="lazy" onerror="this.onerror=null; this.src='{FALLBACK_SVG}'; this.style.padding='30px';">
                    <button type="button" class="btn-audio" onclick="speak('{safe_word}')" title="Phát âm '{escape(en_word)}'">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.74 2.5-2.26 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                        </svg>
                    </button>
                </div>
                <div class="card-body">
                    <div class="vocab-meta">
                        <div class="word-en">{escape(en_word)}</div>
                        <div class="word-ipa">{escape(ipa)}</div>
                    </div>
                    <div class="divider"></div>
                    <div class="word-vi">{escape(meaning)}</div>
                </div>
            </div>"""
            cards_in_group.append(card)

        group_section = f"""
        <div class="theory-group-block">
            <div class="theory-group-title">
                <span class="group-folder-icon">📁</span>
                <span>{escape(g_name)}</span>
                <span class="group-count-pill">{len(words)} từ</span>
            </div>
            <div class="vocab-grid">
                {''.join(cards_in_group)}
            </div>
        </div>"""
        vocab_cards_html.append(group_section)

    return "\n".join(vocab_cards_html)


def build_master_index_html(units_info, output_file, workspace_root):
    total_all_words = sum(u["total_words"] for u in units_info)
    total_all_exercises = sum(u["total_exercises"] for u in units_info)

    # 1. Render Unit Nav Tabs
    unit_tabs_html = []
    for idx, u in enumerate(units_info):
        is_active = (idx == 0)
        unit_tabs_html.append(f"""
        <button type="button" class="unit-tab-btn {'active' if is_active else ''}" data-unit="{u['id']}" onclick="switchUnit('{u['id']}')">
            <span class="unit-tab-icon">{u['icon']}</span>
            <span class="unit-tab-name">{u['short_name']}: {escape(u['topic'])}</span>
            <span class="unit-tab-badge">{u['total_words']} từ • {u['total_exercises']} bài</span>
        </button>""")

    unit_tabs_html.append(f"""
        <button type="button" class="unit-tab-btn" data-unit="all" onclick="switchUnit('all')">
            <span class="unit-tab-icon">📚</span>
            <span class="unit-tab-name">Tất Cả 3 Units</span>
            <span class="unit-tab-badge">{total_all_words} từ • {total_all_exercises} bài</span>
        </button>""")

    # VOCAB CHALLENGE (SRS GAME & PRACTICE APP)
    unit_tabs_html.append(f"""
        <a href="vocab_challenge/index.html" class="unit-tab-btn vocab-challenge-btn" style="background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #ffffff; border-color: transparent; text-decoration: none;" title="Mở ứng dụng ôn tập từ vựng Spaced Repetition (SRS)">
            <span class="unit-tab-icon">⚡</span>
            <span class="unit-tab-name">Vocab Challenge (SRS)</span>
            <span class="unit-tab-badge" style="background: rgba(255, 255, 255, 0.25); color: #ffffff;">Game & Luyện Thi ↗</span>
        </a>""")

    # 2. Render each Unit's Section
    unit_sections_html = []
    for idx, u in enumerate(units_info):
        u_id = u["id"]
        u_prefix = u["prefix"]
        u_title = u["full_name"]
        u_desc = u["description"]
        vocab_cards_html = render_unit_vocab_cards_html(u["vocab_data"], u_prefix, output_file, workspace_root)
        exercises_html = render_all_exercises_html(u["exercises_data"], u_prefix, output_file, workspace_root)

        sidebar_exercise_links = []
        sidebar_exercise_links.append(f"""
            <li>
                <a href="#section-theory-{u_prefix}" class="nav-item active" onclick="activateNav(this)">
                    <span>📖 Lý Thuyết Từ Vựng</span>
                    <span class="nav-badge">{u['total_words']} từ</span>
                </a>
            </li>""")
        for e_idx, ex in enumerate(u["exercises_data"]):
            e_id = ex.get("id", str(e_idx + 1))
            e_title = ex.get("title", f"Exercise {e_idx+1}")
            short_t = e_title.split("-")[-1].strip() if "-" in e_title else e_title
            sidebar_exercise_links.append(f"""
            <li>
                <a href="#exercise-block-{u_prefix}-{e_idx}" class="nav-item" onclick="activateNav(this)">
                    <span>#{e_id}. {escape(short_t)}</span>
                </a>
            </li>""")

        is_first = (idx == 0)
        display_style = "display: block;" if is_first else "display: none;"

        unit_section = f"""
        <!-- ================= UNIT SECTION: {escape(u_title)} ================= -->
        <div class="unit-content-section" data-unit="{u_id}" id="unit-section-{u_id}" style="{display_style}">
            
            <!-- UNIT INTRO HERO BANNER -->
            <div class="unit-hero-banner">
                <div class="unit-hero-left">
                    <span class="unit-hero-pill">{u['icon']} {escape(u['short_name']).upper()}</span>
                    <h2 class="unit-hero-title">{escape(u_title)}</h2>
                    <p class="unit-hero-desc">{escape(u_desc)}</p>
                </div>
                <div class="unit-hero-links">
                    <a href="lessons/{u_id}/vocab/index.html" class="hero-link-btn" title="Mở index.html riêng của unit này">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                            <polyline points="15 3 21 3 21 9"/>
                            <line x1="10" y1="14" x2="21" y2="3"/>
                        </svg>
                        Mở {escape(u['short_name'])} index.html ↗
                    </a>
                    <a href="lessons/{u_id}/vocab/cards.html" class="hero-link-btn outline" title="Mở flashcards riêng của unit này">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>
                            <line x1="7" y1="2" x2="7" y2="22"/>
                            <line x1="17" y1="2" x2="17" y2="22"/>
                            <line x1="2" y1="12" x2="22" y2="12"/>
                        </svg>
                        Mở Cards ↗
                    </a>
                </div>
            </div>

            <!-- UNIT TWO-COLUMN PORTAL LAYOUT -->
            <div class="portal-layout">
                <!-- SIDEBAR -->
                <aside class="portal-sidebar">
                    <div class="stats-summary-card">
                        <h4>📊 {u['icon']} {escape(u['short_name'])} Overview</h4>
                        <div class="stats-2x2">
                            <div class="stat-item">
                                <div class="stat-val">{u['total_words']}</div>
                                <div class="stat-lbl">Từ Vựng</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-val">{u['total_groups']}</div>
                                <div class="stat-lbl">Nhóm Chủ Đề</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-val">{u['total_exercises']}</div>
                                <div class="stat-lbl">Dạng Bài</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-val">{u['total_questions']}</div>
                                <div class="stat-lbl">Câu Hỏi</div>
                            </div>
                        </div>
                    </div>

                    <div class="nav-list-card">
                        <div class="nav-list-title">
                            <span>Danh Sách 16 Bài Tập</span>
                            <span>{escape(u['short_name'])}</span>
                        </div>
                        <ul class="sidebar-links-list">
                            {''.join(sidebar_exercise_links)}
                        </ul>
                    </div>

                    <div class="quick-file-card">
                        <div class="quick-file-title">📁 File Trực Tiếp Trong Lessons:</div>
                        <a href="lessons/{u_id}/vocab/index.html" class="quick-file-link">
                            <span>📄 index.html</span>
                            <span class="file-arrow">↗</span>
                        </a>
                        <a href="lessons/{u_id}/vocab/cards.html" class="quick-file-link">
                            <span>🗂️ cards.html</span>
                            <span class="file-arrow">↗</span>
                        </a>
                        <a href="lessons/{u_id}/vocab/vocab.json" class="quick-file-link">
                            <span>📦 vocab.json</span>
                            <span class="file-arrow">↗</span>
                        </a>
                        <a href="vocab_challenge/index.html" class="quick-file-link" style="border-color: #c4b5fd; background: #faf5ff;">
                            <span>⚡ vocab_challenge</span>
                            <span class="file-arrow" style="color: #7c3aed;">↗</span>
                        </a>
                    </div>
                </aside>

                <!-- MAIN CONTENT -->
                <main class="portal-main">
                    <!-- 1. LÝ THUYẾT TỪ VỰNG -->
                    <section class="section-box section-theory" id="section-theory-{u_prefix}">
                        <div class="section-headline">
                            <div class="headline-left">
                                <div class="headline-icon-box">💡</div>
                                <div class="headline-text">
                                    <h2>Lý Thuyết Từ Vựng Trọng Tâm &bull; {escape(u['short_name'])}</h2>
                                    <p>{u['total_words']} từ vựng chuẩn IPA Anh/Mỹ, ảnh minh họa trực quan, phát âm giọng chuẩn và nghĩa tiếng Việt</p>
                                </div>
                            </div>
                            <div>
                                <a href="lessons/{u_id}/vocab/cards.html" class="nav-item" style="border:1px solid #bfdbfe; font-size:12px; font-weight:700;" title="Mở trang flashcards riêng">
                                    Mở Flashcards ({escape(u['short_name'])}) ↗
                                </a>
                            </div>
                        </div>
                        <div class="theory-body">
                            {vocab_cards_html}
                        </div>
                    </section>

                    <!-- 2. BÀI TẬP TỪ VỰNG -->
                    <section class="section-box section-exercises" id="section-exercises-{u_prefix}">
                        <div class="section-headline">
                            <div class="headline-left">
                                <div class="headline-icon-box">✍️</div>
                                <div class="headline-text">
                                    <h2>Hệ Thống 16 Dạng Bài Tập &bull; {escape(u['short_name'])}</h2>
                                    <p>Bộ 16 dạng bài tập trắc nghiệm, điền khuyết, đoạn văn, ngữ cảnh từ điển &bull; {u['total_questions']} câu hỏi luyện tập</p>
                                </div>
                            </div>
                        </div>
                        <div class="exercises-container">
                            {exercises_html}
                        </div>
                    </section>
                </main>
            </div>
        </div>"""
        unit_sections_html.append(unit_section)

    all_sections_rendered = "\n".join(unit_sections_html)

    # Return Full HTML Template
    return f"""<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLOBAL SUCCESS 12 • HỌC TỪ VỰNG & BÀI TẬP TOÀN DIỆN (Units 1 - 3)</title>

    <!-- Google Fonts: Plus Jakarta Sans & Be Vietnam Pro -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {{
            /* Unified Palette - Modern Blue / Deep Navy */
            --primary-blue: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-navy: #1e3a8a;
            --primary-light: #eff6ff;
            --accent-blue: #60a5fa;
            --surface-white: #ffffff;
            --bg-page: #f8fafc;
            --bg-gradient: linear-gradient(180deg, #f0f7ff 0%, #f8fafc 100%);
            --text-main: #0f172a;
            --text-heading: #1e293b;
            --text-muted: #64748b;
            --border-subtle: #e2e8f0;
            --border-highlight: #bfdbfe;
            --card-radius: 20px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --shadow-default: 0 4px 20px -2px rgba(37, 99, 235, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
            --shadow-hover: 0 16px 32px -4px rgba(37, 99, 235, 0.15), 0 4px 12px -2px rgba(0, 0, 0, 0.05);
            --success-color: #10b981;
            --success-bg: #ecfdf5;
            --error-color: #ef4444;
            --error-bg: #fef2f2;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Be Vietnam Pro', sans-serif;
            background: var(--bg-page);
            color: var(--text-main);
            line-height: 1.55;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        /* STICKY MASTER PORTAL HEADER */
        header.portal-header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid var(--border-subtle);
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        }}

        .header-top-row {{
            max-width: 1560px;
            margin: 0 auto;
            padding: 12px 24px 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .brand-meta {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .brand-badge {{
            background: linear-gradient(135deg, var(--primary-navy), var(--primary-blue));
            color: white;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 13px;
            padding: 6px 14px;
            border-radius: 9999px;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
        }}

        .brand-titles h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 800;
            color: var(--primary-navy);
            letter-spacing: -0.3px;
        }}

        .brand-titles p {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .header-controls {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .header-nav-tabs {{
            display: flex;
            background: #f1f5f9;
            padding: 3px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
        }}

        .nav-tab-btn {{
            padding: 6px 14px;
            border-radius: 9999px;
            border: none;
            background: transparent;
            font-size: 12.5px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Be Vietnam Pro', sans-serif;
        }}

        .nav-tab-btn.active {{
            background: #ffffff;
            color: var(--primary-blue);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        }}

        .search-field {{
            position: relative;
            width: 240px;
        }}

        .search-field input {{
            width: 100%;
            padding: 7px 12px 7px 34px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            background: #ffffff;
            font-size: 13px;
            font-family: inherit;
            outline: none;
            transition: all 0.2s;
        }}

        .search-field input:focus {{
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }}

        .search-field svg {{
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            color: var(--text-muted);
        }}

        .mode-toggle {{
            display: flex;
            background: #f1f5f9;
            padding: 3px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
        }}

        .mode-btn {{
            padding: 5px 12px;
            border-radius: 9999px;
            border: none;
            background: transparent;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
        }}

        .mode-btn.active {{
            background: #ffffff;
            color: var(--primary-navy);
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
        }}

        .btn-print {{
            padding: 7px 14px;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
            background: white;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-heading);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}

        .btn-print:hover {{
            background: #f1f5f9;
        }}

        /* UNIT SWITCHER NAVIGATION BAR */
        .header-unit-switcher-bar {{
            background: #f8fafc;
            border-top: 1px solid var(--border-subtle);
            padding: 8px 24px;
        }}

        .switcher-inner {{
            max-width: 1560px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .unit-switcher-label {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .unit-nav-buttons {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .unit-tab-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            background: #ffffff;
            color: var(--text-heading);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .unit-tab-btn:hover {{
            border-color: #93c5fd;
            background: #f0f7ff;
            color: var(--primary-blue);
        }}

        .unit-tab-btn.active {{
            background: linear-gradient(135deg, var(--primary-navy), var(--primary-blue));
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
        }}

        .unit-tab-badge {{
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 9999px;
            background: #eff6ff;
            color: var(--primary-blue);
            font-weight: 700;
        }}

        .unit-tab-btn.active .unit-tab-badge {{
            background: rgba(255, 255, 255, 0.22);
            color: #ffffff;
        }}

        /* UNIT HERO BANNER */
        .unit-hero-banner {{
            max-width: 1560px;
            margin: 20px auto 0;
            padding: 22px 28px;
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            border-radius: var(--card-radius);
            color: white;
            box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }}

        .unit-hero-pill {{
            display: inline-block;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11.5px;
            font-weight: 800;
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(4px);
            padding: 4px 12px;
            border-radius: 9999px;
            letter-spacing: 0.6px;
            margin-bottom: 8px;
        }}

        .unit-hero-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.4px;
            line-height: 1.25;
            margin-bottom: 6px;
        }}

        .unit-hero-desc {{
            font-size: 14px;
            opacity: 0.92;
            max-width: 820px;
        }}

        .unit-hero-links {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .hero-link-btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 9px 16px;
            border-radius: 10px;
            background: white;
            color: var(--primary-navy);
            text-decoration: none;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 700;
            transition: all 0.2s;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}

        .hero-link-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }}

        .hero-link-btn.outline {{
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.4);
        }}

        .hero-link-btn.outline:hover {{
            background: rgba(255, 255, 255, 0.28);
        }}

        /* APP LAYOUT */
        .portal-layout {{
            max-width: 1560px;
            margin: 0 auto;
            padding: 24px;
            display: flex;
            gap: 28px;
            width: 100%;
            flex: 1;
        }}

        /* SIDEBAR */
        aside.portal-sidebar {{
            width: 290px;
            flex-shrink: 0;
            position: sticky;
            top: 130px;
            max-height: calc(100vh - 150px);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 18px;
            padding-right: 6px;
        }}

        aside.portal-sidebar::-webkit-scrollbar {{
            width: 4px;
        }}
        aside.portal-sidebar::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}

        .stats-summary-card {{
            background: linear-gradient(135deg, var(--primary-navy), var(--primary-blue));
            color: white;
            padding: 18px;
            border-radius: var(--card-radius);
            box-shadow: var(--shadow-default);
        }}

        .stats-summary-card h4 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stats-2x2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .stat-item {{
            background: rgba(255, 255, 255, 0.16);
            backdrop-filter: blur(4px);
            padding: 8px 10px;
            border-radius: 10px;
            text-align: center;
        }}

        .stat-val {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 18px;
            font-weight: 800;
        }}

        .stat-lbl {{
            font-size: 11px;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .nav-list-card {{
            background: #ffffff;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-subtle);
            padding: 14px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
        }}

        .nav-list-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
        }}

        .sidebar-links-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            color: var(--text-heading);
            text-decoration: none;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.15s;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--primary-light);
            color: var(--primary-dark);
            font-weight: 600;
        }}

        .nav-badge {{
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 9999px;
            background: #f1f5f9;
            color: var(--text-muted);
        }}

        .quick-file-card {{
            background: #f8fafc;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-subtle);
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .quick-file-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .quick-file-link {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 7px 10px;
            background: white;
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 600;
            color: var(--primary-navy);
            text-decoration: none;
            transition: all 0.15s;
        }}

        .quick-file-link:hover {{
            background: var(--primary-light);
            border-color: #bfdbfe;
        }}

        .file-arrow {{
            color: var(--primary-blue);
            font-weight: bold;
        }}

        /* MAIN CONTENT AREA */
        main.portal-main {{
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 36px;
        }}

        /* SECTION BOXES */
        .section-box {{
            background: #ffffff;
            border-radius: var(--card-radius);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-default);
            overflow: hidden;
        }}

        .section-headline {{
            padding: 22px 28px;
            border-bottom: 1px solid var(--border-subtle);
            background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .headline-left {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .headline-icon-box {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: var(--primary-light);
            color: var(--primary-blue);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
        }}

        .headline-text h2 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--primary-navy);
            letter-spacing: -0.4px;
        }}

        .headline-text p {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        /* LÝ THUYẾT TỪ VỰNG - EXACT CARDS SPEC */
        .theory-body {{
            padding: 28px;
            display: flex;
            flex-direction: column;
            gap: 36px;
            background: var(--bg-gradient);
        }}

        .theory-group-block {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .theory-group-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: var(--primary-navy);
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 8px;
            border-bottom: 2px solid #bfdbfe;
        }}

        .group-count-pill {{
            font-size: 12px;
            padding: 2px 10px;
            border-radius: 9999px;
            background: var(--primary-light);
            color: var(--primary-blue);
            font-weight: 600;
        }}

        .vocab-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        }}

        @media (min-width: 1320px) {{
            .vocab-grid {{
                grid-template-columns: repeat(5, 1fr);
            }}
        }}

        @media (min-width: 1024px) and (max-width: 1319px) {{
            .vocab-grid {{
                grid-template-columns: repeat(4, 1fr);
            }}
        }}

        .vocab-card {{
            background: var(--surface-white);
            border-radius: var(--card-radius);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-default);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
        }}

        .vocab-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
            border-color: #bfdbfe;
        }}

        .image-container {{
            width: 100%;
            height: 200px;
            background: #f8fafc;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid #f1f5f9;
            padding: 8px;
        }}

        .image-container img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 12px;
            display: block;
            transition: transform 0.3s ease;
        }}

        .vocab-card:hover .image-container img {{
            transform: scale(1.02);
        }}

        .btn-audio {{
            position: absolute;
            bottom: 14px;
            right: 14px;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(226, 232, 240, 0.8);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-blue);
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.15);
            transition: all 0.2s ease;
            z-index: 2;
        }}

        .btn-audio:hover {{
            transform: scale(1.08);
            background: var(--primary-blue);
            color: #ffffff;
            box-shadow: 0 6px 14px rgba(37, 99, 235, 0.3);
        }}

        .card-body {{
            padding: 18px 20px 20px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            justify-content: space-between;
            gap: 14px;
        }}

        .vocab-meta {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .word-en {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 21px;
            font-weight: 700;
            color: #1e293b;
            letter-spacing: -0.3px;
        }}

        .word-ipa {{
            font-size: 14px;
            color: #3b82f6;
            font-weight: 500;
            font-family: 'Be Vietnam Pro', sans-serif;
        }}

        .divider {{
            height: 1px;
            background: linear-gradient(90deg, #e2e8f0 0%, rgba(226, 232, 240, 0.2) 100%);
        }}

        .word-vi {{
            font-size: 15px;
            font-weight: 600;
            color: #334155;
            line-height: 1.4;
        }}

        /* BÀI TẬP TỪ VỰNG - UNIFORM TITLE COLORS */
        .exercises-container {{
            padding: 28px;
            display: flex;
            flex-direction: column;
            gap: 28px;
        }}

        .exercise-card {{
            background: #ffffff;
            border-radius: 16px;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
            overflow: hidden;
            transition: all 0.2s;
        }}

        .exercise-card:hover {{
            border-color: #cbd5e1;
        }}

        .exercise-header {{
            padding: 18px 22px;
            border-bottom: 1px solid var(--border-subtle);
            background: linear-gradient(90deg, #f8fafc 0%, #ffffff 100%);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .exercise-title-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .badge-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .ex-num-badge {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-blue);
            background: var(--primary-light);
            padding: 2px 10px;
            border-radius: 9999px;
            border: 1px solid #bfdbfe;
        }}

        .ex-type-pill {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            background: #f1f5f9;
            padding: 2px 8px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }}

        .ex-file-tag {{
            font-family: monospace;
            font-size: 11px;
            color: #94a3b8;
        }}

        .exercise-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: var(--primary-navy);
            letter-spacing: -0.2px;
        }}

        .exercise-description {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        .exercise-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .btn-check {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 8px;
            background: var(--primary-blue);
            color: white;
            border: none;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}

        .btn-check:hover {{
            background: var(--primary-dark);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        }}

        .btn-reset {{
            padding: 8px;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
            background: white;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .btn-reset:hover {{
            background: #f1f5f9;
            color: var(--text-main);
        }}

        .score-pill {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
            background: var(--success-bg);
            color: var(--success-color);
            border: 1px solid #a7f3d0;
        }}

        .exercise-body {{
            padding: 22px;
        }}

        /* QUESTION ROWS */
        .question-row {{
            background: #ffffff;
            border: 1px solid #f1f5f9;
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 14px;
            transition: all 0.2s;
        }}

        .question-row:last-child {{
            margin-bottom: 0;
        }}

        .question-row:hover {{
            border-color: #cbd5e1;
        }}

        .q-header {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .q-num {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            background: var(--primary-light);
            color: var(--primary-blue);
            padding: 3px 8px;
            border-radius: 6px;
            flex-shrink: 0;
            border: 1px solid #bfdbfe;
        }}

        .q-content {{
            flex: 1;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-main);
            line-height: 1.5;
        }}

        .target-word {{
            font-weight: 700;
            color: var(--primary-dark);
            text-decoration: underline;
            text-underline-offset: 3px;
            background: var(--primary-light);
            padding: 0 4px;
            border-radius: 4px;
        }}

        /* OPTIONS GRID - 2 COLUMNS BALANCED */
        .options-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}

        @media (max-width: 820px) {{
            .options-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .option-label {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 14px;
            border-radius: 10px;
            border: 1.5px solid var(--border-subtle);
            background: #ffffff;
            cursor: pointer;
            transition: all 0.15s ease;
            position: relative;
        }}

        .option-label:hover {{
            background: #f8fafc;
            border-color: #93c5fd;
        }}

        .option-label input[type="radio"] {{
            position: absolute;
            opacity: 0;
            pointer-events: none;
        }}

        .option-badge {{
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background: #f1f5f9;
            color: #475569;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            font-family: 'Plus Jakarta Sans', sans-serif;
            flex-shrink: 0;
            transition: all 0.2s;
        }}

        .option-text {{
            font-size: 13.5px;
            color: var(--text-heading);
            flex: 1;
        }}

        .check-icon {{
            display: none;
            font-weight: bold;
            font-size: 14px;
        }}

        .option-label.is-selected {{
            border-color: var(--primary-blue);
            background: var(--primary-light);
        }}

        .option-label.is-selected .option-badge {{
            background: var(--primary-blue);
            color: white;
        }}

        body.mode-review .option-label[data-is-correct="true"],
        .option-label.result-correct {{
            background: var(--success-bg) !important;
            border-color: var(--success-color) !important;
        }}

        body.mode-review .option-label[data-is-correct="true"] .option-badge,
        .option-label.result-correct .option-badge {{
            background: var(--success-color) !important;
            color: white !important;
        }}

        body.mode-review .option-label[data-is-correct="true"] .check-icon,
        .option-label.result-correct .check-icon {{
            display: inline-block;
            color: var(--success-color);
        }}

        .option-label.result-incorrect {{
            background: var(--error-bg) !important;
            border-color: var(--error-color) !important;
        }}

        .option-label.result-incorrect .option-badge {{
            background: var(--error-color) !important;
            color: white !important;
        }}

        /* FORM INPUTS */
        .tidy-input {{
            padding: 8px 14px;
            border-radius: 8px;
            border: 1.5px solid var(--border-subtle);
            font-size: 14px;
            font-family: 'Be Vietnam Pro', sans-serif;
            outline: none;
            transition: all 0.2s;
            background: #ffffff;
        }}

        .tidy-input:focus {{
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }}

        .tidy-input.correct-field {{
            background: var(--success-bg);
            border-color: var(--success-color);
            color: #065f46;
            font-weight: 600;
        }}

        .tidy-input.incorrect-field {{
            background: var(--error-bg);
            border-color: var(--error-color);
            color: #991b1b;
        }}

        .tidy-textarea {{
            width: 100%;
            padding: 10px 14px;
            border-radius: 8px;
            border: 1.5px solid var(--border-subtle);
            font-size: 14px;
            font-family: inherit;
            outline: none;
            transition: all 0.2s;
            resize: vertical;
        }}

        .tidy-textarea:focus {{
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
        }}

        /* DIALOGUE & SENTENCE LISTS */
        .dialogue-box {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding: 10px 14px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid var(--primary-blue);
        }}

        .dialogue-line {{
            font-size: 14px;
        }}

        .sentence-order-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 8px;
        }}

        .order-item {{
            background: #f8fafc;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13.5px;
            border-left: 3px solid #94a3b8;
        }}

        /* PIC TO WORD */
        .pic-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
        }}

        .pic-word-card {{
            background: #ffffff;
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .pic-wrapper {{
            height: 150px;
            background: #f8fafc;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 6px;
        }}

        .pic-wrapper img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 8px;
        }}

        .pic-tag {{
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(0, 0, 0, 0.6);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
        }}

        .pic-controls {{
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .pic-input {{
            width: 100%;
            text-align: center;
        }}

        .answer-badge {{
            font-size: 12px;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 4px 8px;
            border-radius: 6px;
            text-align: center;
        }}

        /* WRITE ENGLISH */
        .parts-wrap {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .write-part-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 10px 14px;
            background: #f8fafc;
            border-radius: 8px;
            flex-wrap: wrap;
        }}

        .part-vi {{
            font-size: 13.5px;
            font-weight: 600;
            color: #334155;
            flex: 1;
        }}

        .part-input-wrap {{
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 260px;
        }}

        .write-input {{
            flex: 1;
        }}

        .sub-ans-reveal {{
            font-size: 12.5px;
            font-weight: 700;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 4px 10px;
            border-radius: 6px;
        }}

        /* WORD BOX CONTAINER */
        .word-box-container {{
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #bfdbfe;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 20px;
        }}

        .word-box-label {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-navy);
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}

        .word-box-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .word-box-chip {{
            background: #ffffff;
            color: var(--primary-blue);
            font-size: 13px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 9999px;
            border: 1px solid #bfdbfe;
            box-shadow: 0 1px 3px rgba(37, 99, 235, 0.08);
        }}

        .inline-blank {{
            width: 140px;
            display: inline-block;
            margin: 0 6px;
            text-align: center;
            vertical-align: middle;
        }}

        .blank-sentence {{
            line-height: 2.2;
            font-size: 14px;
        }}

        .inline-ans-reveal {{
            margin-top: 8px;
            font-size: 12.5px;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
        }}

        /* PARAGRAPH FILL */
        .paragraph-flow-card {{
            background: #f8fafc;
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 22px 24px;
            line-height: 2.3;
            font-size: 15px;
            color: #1e293b;
        }}

        .inline-slot {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin: 0 4px;
            vertical-align: middle;
        }}

        .slot-num {{
            font-weight: 700;
            color: var(--primary-blue);
            font-size: 12px;
        }}

        .para-input {{
            width: 125px;
            text-align: center;
            padding: 4px 8px;
            font-size: 13.5px;
        }}

        .para-key {{
            font-size: 12px;
            font-weight: 700;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 2px 6px;
            border-radius: 4px;
        }}

        /* OXFORD DICTIONARY CARDS */
        .oxford-dict-card {{
            background: #ffffff;
            border: 1.5px solid #bfdbfe;
            border-radius: 14px;
            padding: 20px 22px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.05);
        }}

        .oxford-dict-card:last-child {{
            margin-bottom: 0;
        }}

        .dict-head {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
            flex-wrap: wrap;
        }}

        .dict-word-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--primary-navy);
        }}

        .dict-pos-tag {{
            font-size: 12px;
            font-style: italic;
            color: #64748b;
            background: #f1f5f9;
            padding: 2px 8px;
            border-radius: 6px;
        }}

        .dict-ipa {{
            font-size: 13.5px;
            color: var(--primary-blue);
            font-family: 'Be Vietnam Pro', sans-serif;
        }}

        .dict-def {{
            font-size: 14.5px;
            color: #334155;
            line-height: 1.5;
            margin-bottom: 14px;
        }}

        .dict-collocs {{
            background: #f8fafc;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
        }}

        .dict-collocs-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-blue);
            margin-bottom: 6px;
        }}

        .dict-bullets-list {{
            list-style: square inside;
            font-size: 13.5px;
            color: #475569;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .dict-practice-section {{
            border-top: 1px dashed var(--border-subtle);
            padding-top: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .dict-practice-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: #475569;
        }}

        .dict-question-item {{
            font-size: 14px;
            line-height: 2.1;
        }}

        .dict-q-num {{
            font-weight: 700;
            color: var(--primary-blue);
            font-size: 12px;
            margin-right: 6px;
        }}

        .dict-blank {{
            width: 140px;
            display: inline-block;
            margin: 0 4px;
            text-align: center;
        }}

        .dict-ans-reveal {{
            font-size: 12px;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            margin-top: 4px;
        }}

        /* SIGNS AND NOTICES */
        .sign-layout {{
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 20px;
            align-items: center;
        }}

        @media (max-width: 700px) {{
            .sign-layout {{
                grid-template-columns: 1fr;
            }}
        }}

        .sign-board {{
            background: #fefce8;
            border: 2px solid #facc15;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 120px;
            box-shadow: 0 4px 10px rgba(234, 179, 8, 0.12);
        }}

        .sign-board.has-image {{
            background: #ffffff;
            padding: 4px;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: auto;
        }}

        .sign-img-view {{
            width: 100%;
            height: auto;
            aspect-ratio: 1 / 1;
            object-fit: contain;
            display: block;
            border-radius: 8px;
        }}

        .sign-icon-circle {{
            font-size: 28px;
            margin-bottom: 6px;
        }}

        .sign-desc {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 13px;
            color: #713f12;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .sign-qa {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        /* WORD FAMILIES TABLE */
        .table-responsive {{
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
        }}

        .wf-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13.5px;
            text-align: left;
        }}

        .wf-table th {{
            background: #f8fafc;
            color: var(--primary-navy);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            padding: 12px 16px;
            border-bottom: 2px solid var(--border-subtle);
        }}

        .wf-table td {{
            padding: 12px 16px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .wf-table tbody tr:hover {{
            background: #f8fafc;
        }}

        .base-chip {{
            font-weight: 700;
            color: var(--primary-blue);
        }}

        .base-type-tag {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .wf-val {{
            color: #334155;
            font-weight: 500;
        }}

        /* WORD FORMATION */
        .root-badge {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-navy);
            background: #dbeafe;
            padding: 2px 8px;
            border-radius: 4px;
            margin-left: 6px;
        }}

        /* TRANSLATION */
        .trans-vi-prompt {{
            font-size: 14.5px;
            font-weight: 600;
            color: #1e293b;
        }}

        .trans-input-box {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 8px;
        }}

        .trans-reveal-box {{
            background: var(--success-bg);
            border: 1px solid #a7f3d0;
            border-radius: 8px;
            padding: 10px 14px;
        }}

        .trans-key-label {{
            font-size: 12px;
            font-weight: 700;
            color: var(--success-color);
        }}

        .trans-key-text {{
            font-size: 13.5px;
            color: #065f46;
            font-weight: 600;
            margin-top: 2px;
        }}

        /* FOOTER */
        footer.portal-footer {{
            margin-top: auto;
            background: #ffffff;
            border-top: 1px solid var(--border-subtle);
            padding: 24px;
            text-align: center;
            font-size: 13px;
            color: var(--text-muted);
        }}

        /* PRINT STYLES */
        @media print {{
            header.portal-header,
            aside.portal-sidebar,
            .exercise-actions,
            .btn-audio,
            .unit-hero-links {{
                display: none !important;
            }}
            .portal-layout {{
                padding: 0;
            }}
            .unit-hero-banner {{
                margin: 0 0 20px 0;
                box-shadow: none;
                background: #f1f5f9 !important;
                color: #000000 !important;
            }}
            .unit-hero-pill {{
                background: #e2e8f0 !important;
                color: #000000 !important;
            }}
            .unit-hero-title {{
                color: #000000 !important;
            }}
            .section-box, .exercise-card {{
                box-shadow: none !important;
                border: 1px solid #cbd5e1 !important;
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>

<body>

    <!-- STICKY APP HEADER -->
    <header class="portal-header">
        <div class="header-top-row">
            <div class="brand-meta">
                <span class="brand-badge">GS12 PORTAL</span>
                <div class="brand-titles">
                    <h1>GLOBAL SUCCESS 12 • HỌC TỪ VỰNG & BÀI TẬP TOÀN DIỆN</h1>
                    <p>Khám phá toàn bộ Unit 1 &bull; Unit 2 &bull; Unit 3 &bull; Lý thuyết trực quan & 16 Dạng bài tập chuẩn BGD</p>
                </div>
            </div>

            <div class="header-controls">
                <!-- VIEW TABS -->
                <div class="header-nav-tabs">
                    <button type="button" class="nav-tab-btn active" id="tabAll" onclick="switchMainTab('all')">📚 Tất Cả</button>
                    <button type="button" class="nav-tab-btn" id="tabTheory" onclick="switchMainTab('theory')">💡 Lý Thuyết (Cards)</button>
                    <button type="button" class="nav-tab-btn" id="tabExercises" onclick="switchMainTab('exercises')">✍️ Bài Tập (16 Dạng)</button>
                </div>

                <!-- LIVE SEARCH -->
                <div class="search-field">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <input type="text" id="masterSearchInput" placeholder="Tìm từ, IPA, câu hỏi..." oninput="handleGlobalSearch(this.value)">
                </div>

                <!-- REVIEW / PRACTICE MODE TOGGLE -->
                <div class="mode-toggle">
                    <button type="button" class="mode-btn active" id="btnModeReview" onclick="setMode('review')">👁️ Xem Đáp Án</button>
                    <button type="button" class="mode-btn" id="btnModePractice" onclick="setMode('practice')">✍️ Làm Bài</button>
                </div>

                <!-- PRINT BUTTON: Opens PDF of active Unit -->
                <button type="button" class="btn-print" onclick="openActiveUnitPdf()" title="Mở &amp; In file PDF sách bài học theo Unit đang xem">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 6 2 18 2 18 9"/>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                        <rect x="6" y="14" width="12" height="8"/>
                    </svg>
                    In PDF
                </button>
            </div>
        </div>

        <!-- UNIT SWITCHER NAVIGATION BAR -->
        <div class="header-unit-switcher-bar">
            <div class="switcher-inner">
                <div class="unit-switcher-label">
                    <span>⚡ Chọn Bài Học (Units):</span>
                </div>
                <div class="unit-nav-buttons" role="tablist">
                    {''.join(unit_tabs_html)}
                </div>
            </div>
        </div>
    </header>

    <!-- MAIN WRAPPER CONTAINER WITH ALL 3 UNITS -->
    <div id="masterPortalContent">
        {all_sections_rendered}
    </div>

    <!-- FOOTER -->
    <footer class="portal-footer">
        <p>Hệ thống Học Từ Vựng & Bài Tập Tương Tác Global Success 12 &bull; 3 Units Hoàn Chỉnh &bull; Google Deepmind Antigravity Skills</p>
    </footer>

    <!-- INTERACTIVE JAVASCRIPT LOGIC -->
    <script>
        let currentUnit = 'unit-1';
        let currentTab = 'all';

        // Web Speech API Voice synthesis
        function speak(text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }}
        }}

        // Switch Unit Handler
        function switchUnit(unitId) {{
            currentUnit = unitId;

            // 1. Update unit nav buttons
            document.querySelectorAll('.unit-tab-btn').forEach(btn => {{
                if (btn.getAttribute('data-unit') === unitId) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});

            // 2. Show / hide unit content sections
            document.querySelectorAll('.unit-content-section').forEach(sec => {{
                const u = sec.getAttribute('data-unit');
                if (unitId === 'all') {{
                    sec.style.display = 'block';
                }} else if (u === unitId) {{
                    sec.style.display = 'block';
                }} else {{
                    sec.style.display = 'none';
                }}
            }});

            // 3. Update URL hash without jumping page
            if (history.replaceState) {{
                history.replaceState(null, null, '#' + unitId);
            }}

            // 4. Re-apply current tab filter (all / theory / exercises)
            switchMainTab(currentTab);
        }}

        // Open publication-grade PDF for active unit
        function openActiveUnitPdf() {{
            let uNum = '1';
            if (currentUnitId && currentUnitId !== 'all') {{
                const m = currentUnitId.match(/\d+/);
                if (m) uNum = m[0];
            }}
            const pdfUrl = `lessons/unit-${{uNum}}/vocab/vocab_unit${{uNum}}.pdf`;
            window.open(pdfUrl, '_blank');
        }}

        // Tab Switcher (Tất Cả / Lý Thuyết / Bài Tập)
        function switchMainTab(tab) {{
            currentTab = tab;
            const btns = ['tabAll', 'tabTheory', 'tabExercises'];
            btns.forEach(b => {{
                const el = document.getElementById(b);
                if (el) el.classList.remove('active');
            }});

            const activeBtn = document.getElementById(tab === 'theory' ? 'tabTheory' : (tab === 'exercises' ? 'tabExercises' : 'tabAll'));
            if (activeBtn) activeBtn.classList.add('active');

            const theorySecs = document.querySelectorAll('.section-theory');
            const exSecs = document.querySelectorAll('.section-exercises');

            if (tab === 'theory') {{
                theorySecs.forEach(s => s.style.display = 'block');
                exSecs.forEach(s => s.style.display = 'none');
            }} else if (tab === 'exercises') {{
                theorySecs.forEach(s => s.style.display = 'none');
                exSecs.forEach(s => s.style.display = 'block');
            }} else {{
                theorySecs.forEach(s => s.style.display = 'block');
                exSecs.forEach(s => s.style.display = 'block');
            }}
        }}

        // Review vs Practice Mode Toggle
        function setMode(mode) {{
            const body = document.body;
            const btnRev = document.getElementById('btnModeReview');
            const btnPrac = document.getElementById('btnModePractice');

            if (mode === 'review') {{
                body.classList.remove('mode-practice');
                body.classList.add('mode-review');
                if (btnRev) btnRev.classList.add('active');
                if (btnPrac) btnPrac.classList.remove('active');
                revealAllAnswerKeys(true);
            }} else {{
                body.classList.remove('mode-review');
                body.classList.add('mode-practice');
                if (btnPrac) btnPrac.classList.add('active');
                if (btnRev) btnRev.classList.remove('active');
                revealAllAnswerKeys(false);
            }}
        }}

        // Reveal or Hide Answer Keys
        function revealAllAnswerKeys(show) {{
            const reveals = document.querySelectorAll(
                '.answer-badge, .sub-ans-reveal, .inline-ans-reveal, .para-key, .dict-ans-reveal, .trans-reveal-box'
            );
            reveals.forEach(el => {{
                el.style.display = show ? 'inline-block' : 'none';
                if (el.classList.contains('trans-reveal-box')) {{
                    el.style.display = show ? 'block' : 'none';
                }}
            }});
        }}

        // Mark radio selection
        function markSelected(radio) {{
            const container = radio.closest('.options-grid');
            if (container) {{
                container.querySelectorAll('.option-label').forEach(lbl => {{
                    lbl.classList.remove('is-selected');
                }});
            }}
            const label = radio.closest('.option-label');
            if (label && radio.checked) {{
                label.classList.add('is-selected');
            }}
        }}

        // Check a single exercise
        function checkExercise(uPrefix, exIdx) {{
            const block = document.getElementById(`exercise-block-${{uPrefix}}-${{exIdx}}`);
            if (!block) return;

            let correctCount = 0;
            let totalCount = 0;

            // 1. Multiple Choice checks
            const qRows = block.querySelectorAll('.question-row[data-correct]');
            qRows.forEach(row => {{
                const targetCorrect = (row.getAttribute('data-correct') || '').trim().toLowerCase();
                const selectedRadio = row.querySelector('input[type="radio"]:checked');
                
                totalCount++;

                row.querySelectorAll('.option-label').forEach(lbl => {{
                    lbl.classList.remove('result-correct', 'result-incorrect');
                }});

                if (selectedRadio) {{
                    const val = selectedRadio.value.trim().toLowerCase();
                    const lbl = selectedRadio.closest('.option-label');
                    if (val === targetCorrect) {{
                        correctCount++;
                        if (lbl) lbl.classList.add('result-correct');
                    }} else {{
                        if (lbl) lbl.classList.add('result-incorrect');
                        row.querySelectorAll('.option-label[data-is-correct="true"]').forEach(c => c.classList.add('result-correct'));
                    }}
                }} else {{
                    row.querySelectorAll('.option-label[data-is-correct="true"]').forEach(c => c.classList.add('result-correct'));
                }}
            }});

            // 2. Picture input checks
            const picCards = block.querySelectorAll('.pic-word-card[data-correct]');
            picCards.forEach(card => {{
                totalCount++;
                const target = card.getAttribute('data-correct').trim().toLowerCase();
                const inp = card.querySelector('.pic-input');
                const badge = card.querySelector('.answer-badge');
                if (badge) badge.style.display = 'block';

                if (inp) {{
                    if (inp.value.trim().toLowerCase() === target) {{
                        correctCount++;
                        inp.classList.add('correct-field');
                        inp.classList.remove('incorrect-field');
                    }} else {{
                        inp.classList.add('incorrect-field');
                        inp.classList.remove('correct-field');
                    }}
                }}
            }});

            // 3. Write English parts
            const writeParts = block.querySelectorAll('.write-part-row[data-correct]');
            writeParts.forEach(part => {{
                totalCount++;
                const target = part.getAttribute('data-correct').trim().toLowerCase();
                const inp = part.querySelector('.write-input');
                const reveal = part.querySelector('.sub-ans-reveal');
                if (reveal) reveal.style.display = 'inline-block';

                if (inp) {{
                    if (inp.value.trim().toLowerCase() === target) {{
                        correctCount++;
                        inp.classList.add('correct-field');
                        inp.classList.remove('incorrect-field');
                    }} else {{
                        inp.classList.add('incorrect-field');
                        inp.classList.remove('correct-field');
                    }}
                }}
            }});

            // 4. Inline blanks
            const blankRows = block.querySelectorAll('.blank-row, .wf-item-row');
            blankRows.forEach(row => {{
                totalCount++;
                const target = (row.getAttribute('data-correct') || '').trim().toLowerCase();
                const inp = row.querySelector('.tidy-input');
                const reveal = row.querySelector('.inline-ans-reveal');
                if (reveal) reveal.style.display = 'inline-block';

                if (inp) {{
                    if (inp.value.trim().toLowerCase() === target) {{
                        correctCount++;
                        inp.classList.add('correct-field');
                        inp.classList.remove('incorrect-field');
                    }} else {{
                        inp.classList.add('incorrect-field');
                        inp.classList.remove('correct-field');
                    }}
                }}
            }});

            // 5. Paragraph slots
            const paraSlots = block.querySelectorAll('.inline-slot[data-correct]');
            paraSlots.forEach(slot => {{
                totalCount++;
                const target = (slot.getAttribute('data-correct') || '').trim().toLowerCase();
                const inp = slot.querySelector('.para-input');
                const key = slot.querySelector('.para-key');
                if (key) key.style.display = 'inline-block';

                if (inp) {{
                    if (inp.value.trim().toLowerCase() === target) {{
                        correctCount++;
                        inp.classList.add('correct-field');
                        inp.classList.remove('incorrect-field');
                    }} else {{
                        inp.classList.add('incorrect-field');
                        inp.classList.remove('correct-field');
                    }}
                }}
            }});

            // 6. Dictionary blanks
            const dictItems = block.querySelectorAll('.dict-question-item[data-correct]');
            dictItems.forEach(item => {{
                totalCount++;
                const target = (item.getAttribute('data-correct') || '').trim().toLowerCase();
                const inp = item.querySelector('.dict-blank');
                const reveal = item.querySelector('.dict-ans-reveal');
                if (reveal) reveal.style.display = 'block';

                if (inp) {{
                    if (inp.value.trim().toLowerCase() === target) {{
                        correctCount++;
                        inp.classList.add('correct-field');
                        inp.classList.remove('incorrect-field');
                    }} else {{
                        inp.classList.add('incorrect-field');
                        inp.classList.remove('correct-field');
                    }}
                }}
            }});

            // 7. Translation reveals
            const transRows = block.querySelectorAll('.trans-row');
            transRows.forEach(row => {{
                totalCount++;
                const inp = row.querySelector('.trans-textarea');
                const reveal = row.querySelector('.trans-reveal-box');
                if (reveal) reveal.style.display = 'block';
                if (inp && inp.value.trim().length > 5) {{
                    correctCount++;
                }}
            }});

            // Update Score Pill
            const scorePill = document.getElementById(`score-pill-${{uPrefix}}-${{exIdx}}`);
            if (scorePill && totalCount > 0) {{
                scorePill.style.display = 'inline-block';
                scorePill.textContent = `${{correctCount}} / ${{totalCount}} Đúng (${{Math.round(correctCount / totalCount * 100)}}%)`;
            }}
        }}

        // Reset an exercise
        function resetExercise(uPrefix, exIdx) {{
            const block = document.getElementById(`exercise-block-${{uPrefix}}-${{exIdx}}`);
            if (!block) return;

            block.querySelectorAll('input[type="radio"]').forEach(r => {{
                r.checked = false;
            }});
            block.querySelectorAll('.option-label').forEach(lbl => {{
                lbl.classList.remove('is-selected', 'result-correct', 'result-incorrect');
            }});
            block.querySelectorAll('input[type="text"], textarea').forEach(inp => {{
                inp.value = '';
                inp.classList.remove('correct-field', 'incorrect-field');
            }});
            block.querySelectorAll(
                '.answer-badge, .sub-ans-reveal, .inline-ans-reveal, .para-key, .dict-ans-reveal, .trans-reveal-box'
            ).forEach(el => {{
                el.style.display = 'none';
            }});

            const scorePill = document.getElementById(`score-pill-${{uPrefix}}-${{exIdx}}`);
            if (scorePill) scorePill.style.display = 'none';
        }}

        // Live Search Handler
        function handleGlobalSearch(query) {{
            const q = query.trim().toLowerCase();
            
            const activeSection = (currentUnit === 'all') 
                ? document 
                : document.querySelector(`.unit-content-section[data-unit="${{currentUnit}}"]`);
            
            if (!activeSection) return;

            const cards = activeSection.querySelectorAll('.vocab-card');
            cards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                card.style.display = (!q || text.includes(q)) ? 'flex' : 'none';
            }});

            const qRows = activeSection.querySelectorAll('.question-row, .pic-word-card, .oxford-dict-card');
            qRows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = (!q || text.includes(q)) ? '' : 'none';
            }});
        }}

        // Sidebar active link update
        function activateNav(linkEl) {{
            const sidebar = linkEl.closest('.portal-sidebar');
            if (sidebar) {{
                sidebar.querySelectorAll('.sidebar-links-list .nav-item').forEach(l => l.classList.remove('active'));
            }}
            linkEl.classList.add('active');
        }}

        // Hash Navigation on Load
        window.addEventListener('DOMContentLoaded', () => {{
            const hash = window.location.hash.replace('#', '').trim();
            if (hash && ['unit-1', 'unit-2', 'unit-3', 'all'].includes(hash)) {{
                switchUnit(hash);
            }} else if (hash.startsWith('exercise-block-u1-') || hash.includes('-u1-')) {{
                switchUnit('unit-1');
                setTimeout(() => {{
                    document.getElementById(hash)?.scrollIntoView({{ behavior: 'smooth' }});
                }}, 150);
            }} else if (hash.startsWith('exercise-block-u2-') || hash.includes('-u2-')) {{
                switchUnit('unit-2');
                setTimeout(() => {{
                    document.getElementById(hash)?.scrollIntoView({{ behavior: 'smooth' }});
                }}, 150);
            }} else if (hash.startsWith('exercise-block-u3-') || hash.includes('-u3-')) {{
                switchUnit('unit-3');
                setTimeout(() => {{
                    document.getElementById(hash)?.scrollIntoView({{ behavior: 'smooth' }});
                }}, 150);
            }} else {{
                switchUnit('unit-1');
            }}
        }});
    </script>
</body>

</html>
"""


def build_master_cards_html(units_info, output_file, workspace_root):
    """
    Builds the master cards.html containing flashcards from all units with unit switcher.
    """
    unit_tabs = []
    unit_card_blocks = []

    for idx, u in enumerate(units_info):
        is_first = (idx == 0)
        unit_tabs.append(f"""
        <button type="button" class="unit-tab-btn {'active' if is_first else ''}" data-unit="{u['id']}" onclick="filterCardsByUnit('{u['id']}')">
            <span>{u['icon']} {u['short_name']}</span>
            <span class="unit-tab-badge">{u['total_words']} từ</span>
        </button>""")

        cards_html = render_unit_vocab_cards_html(u["vocab_data"], u["prefix"], output_file, workspace_root)
        block = f"""
        <div class="cards-unit-wrapper" data-unit="{u['id']}" id="cards-unit-{u['id']}" style="{'display:block;' if is_first else 'display:none;'}">
            <div class="unit-section-title">
                <h2>{u['icon']} {escape(u['full_name'])}</h2>
                <p>{escape(u['description'])} &bull; {u['total_words']} từ vựng</p>
            </div>
            {cards_html}
        </div>"""
        unit_card_blocks.append(block)

    unit_tabs.append(f"""
        <button type="button" class="unit-tab-btn" data-unit="all" onclick="filterCardsByUnit('all')">
            <span>📚 Tất Cả 3 Units</span>
            <span class="unit-tab-badge">{sum(u['total_words'] for u in units_info)} từ</span>
        </button>""")

    unit_tabs.append(f"""
        <a href="vocab_challenge/index.html" class="unit-tab-btn vocab-challenge-link" style="background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #ffffff; border-color: transparent; text-decoration: none;" title="Mở ứng dụng ôn tập từ vựng Spaced Repetition (SRS)">
            <span>⚡ Vocab Challenge</span>
            <span class="unit-tab-badge" style="background: rgba(255,255,255,0.25); color: #fff;">SRS App ↗</span>
        </a>""")

    return f"""<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLOBAL SUCCESS 12 • FLASHCARDS TỪ VỰNG TOÀN DIỆN (Units 1 - 3)</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {{
            --primary-blue: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-navy: #1e3a8a;
            --primary-light: #eff6ff;
            --accent-blue: #60a5fa;
            --surface-white: #ffffff;
            --bg-gradient: linear-gradient(180deg, #f0f7ff 0%, #f8fafc 100%);
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border-subtle: #e2e8f0;
            --card-radius: 20px;
            --shadow-default: 0 4px 20px -2px rgba(37, 99, 235, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
            --shadow-hover: 0 16px 32px -4px rgba(37, 99, 235, 0.15), 0 4px 12px -2px rgba(0, 0, 0, 0.05);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Be Vietnam Pro', sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px 24px 60px;
        }}

        .container {{
            max-width: 1560px;
            margin: 0 auto;
        }}

        .header-bar {{
            text-align: center;
            margin-bottom: 28px;
        }}

        .header-bar h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 30px;
            font-weight: 800;
            color: var(--primary-navy);
            letter-spacing: -0.5px;
            display: inline-flex;
            align-items: center;
            gap: 12px;
        }}

        .header-bar p {{
            color: var(--text-muted);
            font-size: 15px;
            margin-top: 6px;
        }}

        /* Toolbar */
        .toolbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            gap: 14px;
            flex-wrap: wrap;
            background: #ffffff;
            padding: 12px 20px;
            border-radius: 16px;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        }}

        .unit-nav-buttons {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .unit-tab-btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 16px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            background: #ffffff;
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .unit-tab-btn:hover {{
            background: var(--primary-light);
            border-color: #bfdbfe;
        }}

        .unit-tab-btn.active {{
            background: linear-gradient(135deg, var(--primary-navy), var(--primary-blue));
            color: #ffffff;
            border-color: transparent;
        }}

        .unit-tab-badge {{
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 9999px;
            background: #eff6ff;
            color: var(--primary-blue);
            font-weight: 700;
        }}

        .unit-tab-btn.active .unit-tab-badge {{
            background: rgba(255, 255, 255, 0.25);
            color: #ffffff;
        }}

        .search-box {{
            position: relative;
            width: 300px;
            max-width: 100%;
        }}

        .search-box input {{
            width: 100%;
            padding: 9px 14px 9px 38px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            background: #ffffff;
            font-size: 13.5px;
            font-family: inherit;
            outline: none;
            transition: all 0.2s;
        }}

        .search-box input:focus {{
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        .search-box svg {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            width: 16px;
            height: 16px;
            color: var(--text-muted);
        }}

        .btn-portal {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 18px;
            border-radius: 9999px;
            background: var(--primary-blue);
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            font-size: 13.5px;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }}

        .btn-portal:hover {{
            background: var(--primary-dark);
            transform: translateY(-1px);
        }}

        .unit-section-title {{
            margin: 24px 0 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--border-subtle);
        }}

        .unit-section-title h2 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 22px;
            font-weight: 800;
            color: var(--primary-navy);
        }}

        .unit-section-title p {{
            font-size: 13.5px;
            color: var(--text-muted);
        }}

        /* Flashcard Grid Spec */
        .theory-group-block {{
            margin-bottom: 30px;
        }}

        .theory-group-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: var(--primary-navy);
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
        }}

        .group-count-pill {{
            font-size: 12px;
            padding: 2px 10px;
            border-radius: 9999px;
            background: var(--primary-light);
            color: var(--primary-blue);
            font-weight: 600;
        }}

        .vocab-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        }}

        @media (min-width: 1320px) {{
            .vocab-grid {{
                grid-template-columns: repeat(5, 1fr);
            }}
        }}

        @media (min-width: 1024px) and (max-width: 1319px) {{
            .vocab-grid {{
                grid-template-columns: repeat(4, 1fr);
            }}
        }}

        .vocab-card {{
            background: var(--surface-white);
            border-radius: var(--card-radius);
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-default);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
        }}

        .vocab-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
            border-color: #bfdbfe;
        }}

        .image-container {{
            width: 100%;
            height: 200px;
            background: #f8fafc;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid #f1f5f9;
            padding: 8px;
        }}

        .image-container img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 12px;
            display: block;
            transition: transform 0.3s ease;
        }}

        .vocab-card:hover .image-container img {{
            transform: scale(1.02);
        }}

        .btn-audio {{
            position: absolute;
            bottom: 14px;
            right: 14px;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(226, 232, 240, 0.8);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-blue);
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.15);
            transition: all 0.2s ease;
            z-index: 2;
        }}

        .btn-audio:hover {{
            transform: scale(1.08);
            background: var(--primary-blue);
            color: #ffffff;
            box-shadow: 0 6px 14px rgba(37, 99, 235, 0.3);
        }}

        .card-body {{
            padding: 18px 20px 20px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            justify-content: space-between;
            gap: 14px;
        }}

        .vocab-meta {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .word-en {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 21px;
            font-weight: 700;
            color: #1e293b;
            letter-spacing: -0.3px;
        }}

        .word-ipa {{
            font-size: 14px;
            color: #3b82f6;
            font-weight: 500;
            font-family: 'Be Vietnam Pro', sans-serif;
        }}

        .divider {{
            height: 1px;
            background: linear-gradient(90deg, #e2e8f0 0%, rgba(226, 232, 240, 0.2) 100%);
        }}

        .word-vi {{
            font-size: 15px;
            font-weight: 600;
            color: #334155;
            line-height: 1.4;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="header-bar">
            <h1>📖 Global Success 12 • Flashcards Toàn Diện</h1>
            <p>Hệ thống Thẻ Từ Vựng Thông Minh &bull; Chuẩn IPA &bull; Phát Âm Bản Ngữ &bull; Hình Ảnh Trực Quan</p>
        </div>

        <div class="toolbar">
            <div class="unit-nav-buttons">
                {''.join(unit_tabs)}
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
                <div class="search-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <input type="text" id="cardsSearchInput" placeholder="Tìm kiếm từ vựng, phiên âm, nghĩa..." oninput="filterCards(this.value)">
                </div>
                <a href="index.html" class="btn-portal">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                    </svg>
                    Xem Bài Tập (index.html)
                </a>
            </div>
        </div>

        <!-- ALL CARDS CONTAINER -->
        <div id="allCardsContainer">
            {''.join(unit_card_blocks)}
        </div>
    </div>

    <script>
        let currentCardUnit = 'unit-1';

        function speak(text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }}
        }}

        function filterCardsByUnit(unitId) {{
            currentCardUnit = unitId;
            document.querySelectorAll('.unit-tab-btn').forEach(btn => {{
                if (btn.getAttribute('data-unit') === unitId) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});

            document.querySelectorAll('.cards-unit-wrapper').forEach(w => {{
                const u = w.getAttribute('data-unit');
                if (unitId === 'all') {{
                    w.style.display = 'block';
                }} else if (u === unitId) {{
                    w.style.display = 'block';
                }} else {{
                    w.style.display = 'none';
                }}
            }});
        }}

        function filterCards(query) {{
            const q = query.trim().toLowerCase();
            const activeWrappers = (currentCardUnit === 'all')
                ? document.querySelectorAll('.cards-unit-wrapper')
                : [document.getElementById(`cards-unit-${{currentCardUnit}}`)];

            activeWrappers.forEach(wrap => {{
                if (!wrap) return;
                const cards = wrap.querySelectorAll('.vocab-card');
                cards.forEach(card => {{
                    const text = card.textContent.toLowerCase();
                    card.style.display = (!q || text.includes(q)) ? 'flex' : 'none';
                }});
            }});
        }}
    </script>
</body>

</html>
"""


def main():
    workspace_root = Path("d:/GS12").resolve()
    lessons_dir = workspace_root / "lessons"

    unit_configs = [
        {
            "id": "unit-1",
            "prefix": "u1",
            "short_name": "Unit 1",
            "topic": "Life Stories",
            "icon": "🌟",
            "full_name": "Unit 1: Life Stories We Admire",
            "description": "Tiểu sử các danh nhân, cống hiến cuộc đời, dấu mốc lịch sử và bài học truyền cảm hứng.",
            "dir": lessons_dir / "unit-1" / "vocab"
        },
        {
            "id": "unit-2",
            "prefix": "u2",
            "short_name": "Unit 2",
            "topic": "A Multicultural World",
            "icon": "🌍",
            "full_name": "Unit 2: A Multicultural World",
            "description": "Sự đa dạng văn hóa, toàn cầu hóa, lễ hội quốc tế, ẩm thực thế giới và hội nhập.",
            "dir": lessons_dir / "unit-2" / "vocab"
        },
        {
            "id": "unit-3",
            "prefix": "u3",
            "short_name": "Unit 3",
            "topic": "Green Living",
            "icon": "🌱",
            "full_name": "Unit 3: Green Living",
            "description": "Lối sống xanh, tái chế rác thải, bảo vệ môi trường, giảm thiểu rác thải nhựa và năng lượng bền vững.",
            "dir": lessons_dir / "unit-3" / "vocab"
        }
    ]

    units_data = []
    for cfg in unit_configs:
        v_dir = cfg["dir"]
        v_json = v_dir / "vocab.json"
        vocab_data = load_json(v_json) or []

        ex_dir = v_dir / "exercises"
        exercises_data = []
        if ex_dir.exists():
            for jf in sorted(ex_dir.glob("*.json")):
                d = load_json(jf)
                if d:
                    d["_filename"] = jf.name
                    exercises_data.append(d)

        total_words = sum(len(g.get("words", [])) for g in vocab_data)
        total_groups = len(vocab_data)
        total_exercises = len(exercises_data)
        total_questions = 0
        for ex in exercises_data:
            if "questions" in ex:
                total_questions += len(ex["questions"])
            elif "entries" in ex:
                for entry in ex["entries"]:
                    total_questions += len(entry.get("questions", []))
            elif "paragraph_parts" in ex:
                total_questions += len([p for p in ex.get("paragraph_parts", []) if isinstance(p, dict) and p.get("type") == "blank"])

        cfg["vocab_data"] = vocab_data
        cfg["exercises_data"] = exercises_data
        cfg["total_words"] = total_words
        cfg["total_groups"] = total_groups
        cfg["total_exercises"] = total_exercises
        cfg["total_questions"] = total_questions

        units_data.append(cfg)
        print(f"[+] Loaded {cfg['short_name']}: {total_words} words, {total_exercises} exercises, {total_questions} questions")

    # Generate master index.html at root d:\GS12\index.html
    root_index_path = workspace_root / "index.html"
    master_html = build_master_index_html(units_data, root_index_path, workspace_root)
    with open(root_index_path, "w", encoding="utf-8") as f:
        f.write(master_html)
    print(f"[OK] Successfully built Master Portal: {root_index_path} ({len(master_html):,} bytes)")

    # Generate master cards.html at root d:\GS12\cards.html
    root_cards_path = workspace_root / "cards.html"
    master_cards_html = build_master_cards_html(units_data, root_cards_path, workspace_root)
    with open(root_cards_path, "w", encoding="utf-8") as f:
        f.write(master_cards_html)
    print(f"[OK] Successfully built Master Cards:  {root_cards_path} ({len(master_cards_html):,} bytes)")


if __name__ == "__main__":
    main()
