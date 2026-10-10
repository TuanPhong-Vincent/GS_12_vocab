#!/usr/bin/env python3
"""
Web Test Portal Builder for GS10-12 (build_web_test.py)

Generates:
1. Interactive Online Test Section for `index.html` (Test 01 & Test 02)
   - 50-minute Countdown Timer with visual alerts (<5m warning, <1m danger, auto-submit)
   - 40-question Interactive Answer Sheet with Option Cards
   - Question Palette Grid (1-40) with live status tracking & smooth scrolling
   - Live Progress Tracking (X/40 answered)
   - Automatic Grading according to 2025 THPT Exam Formula (Score / 10.0, 0.25pt/q)
   - Score Result Modal with performance badges, time spent, and analytics
   - Detailed Pedagogical Explanations (knowledge_type, per-option analysis, Vietnamese translations)
   - Direct PDF Download Links for original printable exam papers
2. Standalone `lessons/unit-<N>/test/test_unit<N>.html`
3. Injects seamlessly into workspace `index.html`
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from html import escape

# Configure UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_json(filepath):
    """Safely load JSON file."""
    p = Path(filepath)
    if not p.exists():
        print(f"[Warning] File not found: {filepath}", file=sys.stderr)
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error] Failed to load JSON {filepath}: {e}", file=sys.stderr)
        return None


def format_passage(text):
    """
    Format passage text into clean, accessible HTML:
    - Paragraph splits (\n\n)
    - Highlighted blanks **(N)_________**
    - Underlined target terms <u>...</u>
    - Bold terms **...**
    - Clean line breaks
    """
    if not text:
        return ""

    paragraphs = text.strip().split("\n\n")
    html_paras = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        p_esc = escape(p_clean)

        # Restore <u> and </u> tags for target vocabulary
        p_esc = p_esc.replace("&lt;u&gt;", '<u class="underlined-target">')
        p_esc = p_esc.replace("&lt;/u&gt;", "</u>")

        # Format numbered blanks: **(1)_________**
        p_esc = re.sub(
            r'\*\*\(([0-9]+)\)_________\*\*',
            r'<span class="exam-blank" title="Chỗ trống (\1)">(\1) _________</span>',
            p_esc,
        )

        # Format standard **bold**
        p_esc = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p_esc)

        # Preserve single newlines
        p_esc = p_esc.replace("\n", "<br>")

        html_paras.append(f'<p class="passage-para">{p_esc}</p>')

    return "\n".join(html_paras)


def format_prompt(prompt_text, q_num, passage_id=None):
    """
    Format question prompt:
    - If multi-line (dialogue / letter / arrangement), render dialogue box with badges.
    - If single line, render clean question title.
    - If reading section has a passage, add quick jump link.
    """
    jump_btn = f' <a href="#{passage_id}" class="btn-jump-passage" title="Xem lại đoạn văn đọc hiểu">📖 Bài đọc</a>' if passage_id else ''

    if not prompt_text:
        return f'<div class="q-title-row"><span class="q-num-badge">Câu {q_num}:</span>{jump_btn}</div>'

    lines = [line.strip() for line in prompt_text.strip().split("\n") if line.strip()]

    # If first line contains "Question X:", extract it
    first_line = lines[0] if lines else f"Question {q_num}:"
    rest_lines = lines[1:] if len(lines) > 1 else []

    header_html = f'<div class="q-title-row"><span class="q-num-badge">Câu {q_num}:</span> <span class="q-prompt-text">{escape(first_line)}</span>{jump_btn}</div>'

    if not rest_lines:
        return header_html

    # Format dialogue / letter lines
    dialogue_items = []
    for line in rest_lines:
        # Match lines like "a. Sam: ...", "b. ...", "Dear Lin,", etc.
        m = re.match(r"^([a-e])\.\s*(.*)$", line, re.IGNORECASE)
        if m:
            bullet = m.group(1).lower()
            content = m.group(2)
            # Bold speaker if format "Speaker: ..."
            sp_m = re.match(r"^([^:]+):\s*(.*)$", content)
            if sp_m:
                speaker = escape(sp_m.group(1))
                spoken = escape(sp_m.group(2))
                line_rendered = f'<strong>{speaker}:</strong> {spoken}'
            else:
                line_rendered = escape(content)
            dialogue_items.append(
                f'<div class="dialogue-line"><span class="dialogue-bullet">{bullet}</span><span class="dialogue-text">{line_rendered}</span></div>'
            )
        else:
            dialogue_items.append(f'<div class="dialogue-note">{escape(line)}</div>')

    dialogue_html = f'<div class="dialogue-card">{"".join(dialogue_items)}</div>'
    return header_html + dialogue_html


def clean_analysis_text(text):
    """Clean markdown bold markers from analysis text."""
    if not text:
        return ""
    # Remove leading "**" or trailing "**" often found in key explanations
    text_clean = text.strip()
    if text_clean.endswith("**"):
        text_clean = text_clean[:-2].strip()
    # Format remaining markdown bold
    text_esc = escape(text_clean)
    text_esc = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text_esc)
    return text_esc


def render_question_options(options, test_id, q_num):
    """
    Render 4 radio option cards with dynamic grid layout based on text length.
    Threshold: <= 8 chars -> 4 cols, <= 50 chars -> 2 cols, > 50 chars -> 1 col.
    """
    opt_lengths = [len(str(val)) for val in options.values()]
    max_len = max(opt_lengths) if opt_lengths else 0

    if max_len <= 8:
        layout_class = "opts-grid-4cols"
    elif max_len <= 50:
        layout_class = "opts-grid-2cols"
    else:
        layout_class = "opts-grid-1col"

    html_parts = [f'<div class="exam-options-grid {layout_class}">']

    for opt_key in ["A", "B", "C", "D"]:
        opt_text = options.get(opt_key, "")
        opt_id = f"opt_{test_id}_{q_num}_{opt_key}"

        html_parts.append(f"""
        <label class="exam-option-card" id="card_{opt_id}" for="{opt_id}">
            <input type="radio" name="q_{test_id}_{q_num}" id="{opt_id}" value="{opt_key}"
                   onchange="examSelectOption('{test_id}', {q_num}, '{opt_key}')">
            <span class="opt-letter">{opt_key}</span>
            <span class="opt-text">{escape(opt_text)}</span>
            <span class="opt-icon-badge" id="icon_{opt_id}"></span>
        </label>
        """)

    html_parts.append("</div>")
    return "\n".join(html_parts)


def render_explanation_block(q_data, test_id, q_num):
    """Render collapsible detailed explanation card."""
    exp = q_data.get("explanation", {})
    knowledge_type = exp.get("knowledge_type", "Kiến thức bài thi THPT")
    analysis = exp.get("analysis", {})
    translation = q_data.get("vietnamese_translation", "")
    correct_ans = q_data.get("correct_answer", "")

    html_parts = []
    html_parts.append(f"""
    <div class="exam-explanation-box" id="exp_{test_id}_{q_num}" style="display: none;">
        <div class="exp-top-bar">
            <div class="exp-title-wrap">
                <span class="exp-icon">💡</span>
                <span class="exp-title">Lời Giải Chi Tiết</span>
                <span class="exp-correct-pill">Đáp án đúng: <strong>{correct_ans}</strong></span>
            </div>
            <span class="exp-knowledge-pill">🏷️ {escape(knowledge_type)}</span>
        </div>
        <div class="exp-analysis-list">
    """)

    # Render analysis items
    if isinstance(analysis, dict):
        for k, v in analysis.items():
            if not v:
                continue
            cleaned = clean_analysis_text(v)
            is_correct_opt = (str(k).upper() == correct_ans.upper())
            item_class = "exp-item-correct" if is_correct_opt else "exp-item-normal"
            html_parts.append(f"""
            <div class="exp-analysis-item {item_class}">
                <span class="exp-item-key">{escape(str(k))}.</span>
                <span class="exp-item-text">{cleaned}</span>
            </div>
            """)
    elif isinstance(analysis, str):
        html_parts.append(f'<div class="exp-analysis-text">{clean_analysis_text(analysis)}</div>')

    if translation:
        html_parts.append(f"""
        <div class="exp-translation-wrap">
            <div class="exp-trans-title">🇻🇳 Dịch nghĩa câu &amp; ngữ cảnh:</div>
            <div class="exp-trans-content">{escape(translation)}</div>
        </div>
        """)

    html_parts.append("</div>")  # closes .exp-analysis-list
    html_parts.append("</div>")  # closes .exam-explanation-box
    return "\n".join(html_parts)


def render_single_test_html(test_data, test_id):
    """
    Render all sections and questions for one test (test1 or test2).
    """
    sections = test_data.get("sections", [])
    questions = test_data.get("questions", [])
    q_dict = {q["question_number"]: q for q in questions}

    html = []
    html.append(f'<div class="single-test-body" id="test-body-{test_id}">')

    for sec in sections:
        sec_num = sec.get("section_number", 1)
        sec_title = sec.get("title", f"Section {sec_num}")
        instruction = sec.get("instruction", "")
        passage_title = sec.get("passage_title", "")
        passage_text = sec.get("passage_text", "")
        q_range = sec.get("questions_range", [1, 40])
        start_q, end_q = q_range[0], q_range[1]

        html.append(f"""
        <div class="test-section-card" id="sec_{test_id}_{sec_num}">
            <div class="sec-header-strip">
                <span class="sec-badge">PHẦN {sec_num}</span>
                <span class="sec-title">{escape(sec_title)}</span>
                <span class="sec-range">(Câu {start_q} – {end_q})</span>
            </div>
            <div class="sec-instruction">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                <span><em>{escape(instruction)}</em></span>
            </div>
        """)

        # Passage Box
        passage_id = f"sec_passage_{test_id}_{sec_num}" if passage_text else None
        if passage_text:
            html.append(f'<div class="passage-box" id="{passage_id}">')
            if passage_title:
                html.append(f'<h4 class="passage-title">{escape(passage_title)}</h4>')
            html.append(format_passage(passage_text))
            html.append("</div>")

        # Questions in this section
        html.append('<div class="sec-questions-list">')
        for q_num in range(start_q, end_q + 1):
            if q_num not in q_dict:
                continue
            q_data = q_dict[q_num]

            prompt_html = format_prompt(q_data.get("prompt", ""), q_num, passage_id=passage_id)
            options_html = render_question_options(q_data.get("options", {}), test_id, q_num)
            explanation_html = render_explanation_block(q_data, test_id, q_num)

            html.append(f"""
            <div class="exam-question-item" id="q_{test_id}_{q_num}" data-qnum="{q_num}">
                <div class="q-content-wrap">
                    {prompt_html}
                    {options_html}
                    <div class="q-status-badge" id="badge_{test_id}_{q_num}"></div>
                    {explanation_html}
                </div>
            </div>
            """)

        html.append("</div>")  # .sec-questions-list
        html.append("</div>")  # .test-section-card

    html.append("</div>")  # .single-test-body
    return "\n".join(html)


def render_question_palette(test_id, total_questions=40):
    """
    Render 40-button navigation palette grid.
    """
    buttons = []
    for i in range(1, total_questions + 1):
        buttons.append(
            f'<button type="button" class="palette-q-btn" id="pal_{test_id}_{i}" '
            f'onclick="examScrollToQuestion(\'{test_id}\', {i})" title="Nhảy đến câu {i}">'
            f'{i}</button>'
        )

    return f"""
    <div class="palette-grid-wrapper" id="palette_wrap_{test_id}">
        <div class="palette-header">
            <span class="palette-title">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                Ma Trận 40 Câu Hỏi
            </span>
            <span class="palette-answered-count" id="pal_count_{test_id}">0/40 đã chọn</span>
        </div>
        <div class="palette-grid">
            {"".join(buttons)}
        </div>
        <div class="palette-legend">
            <span class="legend-item"><span class="legend-dot dot-blank"></span> Chưa làm</span>
            <span class="legend-item"><span class="legend-dot dot-answered"></span> Đã chọn</span>
            <span class="legend-item"><span class="legend-dot dot-correct"></span> Đúng</span>
            <span class="legend-item"><span class="legend-dot dot-wrong"></span> Sai</span>
        </div>
    </div>
    """


def render_test_control_toolbar(test_id, duration_minutes=50):
    """
    Render sticky exam control panel:
    - Countdown Timer (with pause/reset)
    - Progress Bar (clickable to open mobile question palette)
    - Submit, Question Palette & Check buttons
    """
    return f"""
    <div class="exam-control-sticky-bar" id="ctrl_bar_{test_id}">
        <div class="ctrl-left">
            <div class="timer-display-box" id="timer_box_{test_id}">
                <div class="timer-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                </div>
                <div class="timer-info">
                    <span class="timer-label">Thời gian</span>
                    <span class="timer-digits" id="timer_val_{test_id}">{duration_minutes:02d}:00</span>
                </div>
            </div>
            <div class="timer-controls">
                <button type="button" class="btn-ctrl-icon" id="btn_timer_toggle_{test_id}" onclick="examToggleTimer('{test_id}')" title="Tạm dừng / Tiếp tục">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
                </button>
                <button type="button" class="btn-ctrl-icon" onclick="examResetTimer('{test_id}')" title="Đặt lại thời gian 50 phút">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
                </button>
            </div>
        </div>

        <div class="ctrl-mid" onclick="toggleMobilePalette('{test_id}')" title="Chạm để mở ma trận 40 câu hỏi">
            <div class="progress-meta">
                <span class="progress-lbl">Tiến độ làm bài</span>
                <span class="progress-stat" id="progress_stat_{test_id}">0 / 40 câu (0%)</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="progress_fill_{test_id}" style="width: 0%;"></div>
            </div>
        </div>

        <div class="ctrl-right">
            <button type="button" class="btn-exam-action btn-submit" id="btn_submit_{test_id}" onclick="examSubmitTest('{test_id}')">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
                <span>Nộp Bài</span>
            </button>
            <button type="button" class="btn-exam-action btn-palette-toggle" onclick="toggleMobilePalette('{test_id}')" title="Mở ma trận 40 câu hỏi">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                <span>Ma Trận</span>
            </button>
            <button type="button" class="btn-exam-action btn-check" id="btn_check_{test_id}" onclick="examCheckAnswers('{test_id}')">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                <span>Đáp Án</span>
            </button>
            <button type="button" class="btn-exam-action btn-reset" onclick="examResetAll('{test_id}')" title="Làm lại đề thi từ đầu">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><polyline points="23 20 23 14 17 14"></polyline><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path></svg>
                <span>Làm Lại</span>
            </button>
        </div>
    </div>
    """


def render_full_test_section(test1_data, test2_data, unit_num=1):
    """
    Render complete Section 4 HTML containing Test 01 & Test 02.
    """
    test1_content = render_single_test_html(test1_data, "test1")
    test2_content = render_single_test_html(test2_data, "test2")

    palette1 = render_question_palette("test1", 40)
    palette2 = render_question_palette("test2", 40)

    toolbar1 = render_test_control_toolbar("test1", 50)
    toolbar2 = render_test_control_toolbar("test2", 50)

    # Embed JSON answer keys for JS scoring engine
    key1_json = json.dumps(test1_data.get("answer_key_summary", {}))
    key2_json = json.dumps(test2_data.get("answer_key_summary", {}))

    return f"""
    <!-- START SECTION 4: ĐỀ THI CHUẨN THPT (TEST 01 & TEST 02) -->
    <section class="section-box tab-content-test" id="section-test" style="margin-top: 30px;">
        <div class="section-headline">
            <div class="headline-left">
                <div class="headline-icon-box" style="background: #f5f3ff; color: #7c3aed;">📝</div>
                <div class="headline-text">
                    <h2 style="color: #4c1d95;">Đề thi Unit {unit_num}</h2>
                </div>
            </div>
            <div class="headline-right-actions">
                <a href="lessons/unit-{unit_num}/test/test1.pdf" target="_blank" class="nav-item btn-standalone-link" style="border: 1.5px solid #ddd6fe; font-size: 12px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 9999px; background: #f5f3ff; color: #6d28d9;" title="Mở file PDF Đề 1">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                    PDF Test 01 ↗
                </a>
                <a href="lessons/unit-{unit_num}/test/test2.pdf" target="_blank" class="nav-item btn-standalone-link" style="border: 1.5px solid #ddd6fe; font-size: 12px; font-weight: 700; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 9999px; background: #f5f3ff; color: #6d28d9;" title="Mở file PDF Đề 2">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                    PDF Test 02 ↗
                </a>
            </div>
        </div>

        <!-- TEST SUB-TABS SELECTOR -->
        <div class="test-switcher-tabs-wrap">
            <div class="test-switcher-tabs">
                <button type="button" class="test-switcher-btn active" id="btnTestTab1" onclick="switchExamTab('test1')">
                    <span class="tab-badge-num">01</span>
                    <span class="tab-info">
                        <strong>TEST 01: Family Life</strong>
                        <small>40 câu • 50 phút • Cơ bản &amp; Nâng cao</small>
                    </span>
                </button>
                <button type="button" class="test-switcher-btn" id="btnTestTab2" onclick="switchExamTab('test2')">
                    <span class="tab-badge-num">02</span>
                    <span class="tab-info">
                        <strong>TEST 02: Family Life</strong>
                        <small>40 câu • 50 phút • Phân hóa &amp; Đọc hiểu sâu</small>
                    </span>
                </button>
            </div>
        </div>

        <!-- TEST 1 CONTAINER -->
        <div class="test-pane-container active" id="pane_test1">
            {toolbar1}
            <div class="test-layout-grid">
                <div class="test-main-column">
                    {test1_content}
                </div>
                <aside class="test-sidebar-column">
                    <div class="sticky-palette-card">
                        {palette1}
                    </div>
                </aside>
            </div>
        </div>

        <!-- TEST 2 CONTAINER -->
        <div class="test-pane-container" id="pane_test2" style="display: none;">
            {toolbar2}
            <div class="test-layout-grid">
                <div class="test-main-column">
                    {test2_content}
                </div>
                <aside class="test-sidebar-column">
                    <div class="sticky-palette-card">
                        {palette2}
                    </div>
                </aside>
            </div>
        </div>

        <!-- EMBEDDED TEST KEYS DATA -->
        <script id="exam_keys_data" type="application/json">
        {{
            "test1": {key1_json},
            "test2": {key2_json}
        }}
        </script>
    </section>

    <!-- EXAM SCORE SUMMARY MODAL (SHARED) -->
    <div class="exam-modal-backdrop" id="examScoreModal" style="display: none;">
        <div class="exam-modal-card">
            <div class="modal-confetti" id="modalConfetti"></div>
            <button type="button" class="modal-close-btn" onclick="closeExamModal()" title="Đóng">✕</button>
            
            <div class="modal-score-header">
                <div class="score-badge-circle" id="modalScoreCircle">
                    <span class="score-large-val" id="modalScoreVal">9.0</span>
                    <span class="score-scale-lbl">/ 10 điểm</span>
                </div>
                <div class="score-rating-banner" id="modalScoreRating">Xuất Sắc! 🎉</div>
                <p class="modal-score-subtitle" id="modalScoreSubtitle">Bạn đã hoàn thành xuất sắc bài thi trắc nghiệm THPT!</p>
            </div>

            <div class="modal-score-stats-grid">
                <div class="modal-stat-box stat-correct">
                    <span class="stat-num" id="modalCorrectCount">36</span>
                    <span class="stat-label">Câu Đúng (x0.25đ)</span>
                </div>
                <div class="modal-stat-box stat-wrong">
                    <span class="stat-num" id="modalWrongCount">4</span>
                    <span class="stat-label">Câu Sai</span>
                </div>
                <div class="modal-stat-box stat-skipped">
                    <span class="stat-num" id="modalSkippedCount">0</span>
                    <span class="stat-label">Bỏ Trống</span>
                </div>
                <div class="modal-stat-box stat-time">
                    <span class="stat-num" id="modalTimeSpent">28:15</span>
                    <span class="stat-label">Thời Gian Làm</span>
                </div>
            </div>

            <div class="modal-action-buttons">
                <button type="button" class="btn-modal-action btn-modal-review" onclick="closeExamModalAndReview()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                    <span>Xem Chi Tiết Lời Giải &amp; Đáp Án</span>
                </button>
                <button type="button" class="btn-modal-action btn-modal-retake" onclick="modalRetakeExam()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 4v6h-6"></path><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
                    <span>Làm Lại Đề Này</span>
                </button>
            </div>
        </div>
    </div>

    <!-- MOBILE QUESTION PALETTE DRAWER (BOTTOM SHEET) -->
    <div class="mobile-palette-drawer-backdrop" id="mobilePaletteDrawerBackdrop" onclick="closeMobilePalette()" style="display: none;">
        <div class="mobile-palette-drawer" onclick="event.stopPropagation()">
            <div class="drawer-drag-bar-wrap" onclick="closeMobilePalette()">
                <div class="drawer-drag-bar"></div>
            </div>
            <div class="mobile-palette-drawer-header">
                <div class="drawer-header-title">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                    <span id="mobileDrawerTitle">Ma Trận 40 Câu Hỏi</span>
                </div>
                <div class="drawer-header-actions">
                    <span class="drawer-answered-pill" id="mobileDrawerCount">0/40 đã chọn</span>
                    <button type="button" class="drawer-close-btn" onclick="closeMobilePalette()" title="Đóng">✕</button>
                </div>
            </div>
            <div class="mobile-palette-body">
                <div class="mobile-palette-instruction">
                    💡 Chạm vào số câu bất kỳ để cuộn ngay đến câu hỏi đó
                </div>
                <div class="palette-grid mobile-drawer-grid" id="mobileDrawerGrid">
                    <!-- Dynamic cloned question buttons -->
                </div>
                <div class="palette-legend drawer-legend">
                    <span class="legend-item"><span class="legend-dot dot-blank"></span> Chưa làm</span>
                    <span class="legend-item"><span class="legend-dot dot-answered"></span> Đã chọn</span>
                    <span class="legend-item"><span class="legend-dot dot-correct"></span> Đúng</span>
                    <span class="legend-item"><span class="legend-dot dot-wrong"></span> Sai</span>
                </div>
            </div>
        </div>
    </div>
    <!-- END SECTION 4: ĐỀ THI CHUẨN THPT -->
    """


def get_test_css():
    """Return CSS styles for the online test portal."""
    return """
    /* ==========================================================================
       ONLINE TEST SYSTEM STYLES (TEST 01 & TEST 02)
       ========================================================================== */

    /* Sub-tabs Switcher */
    .test-switcher-tabs-wrap {
        margin: 20px 0 24px;
    }
    .test-switcher-tabs {
        display: flex;
        gap: 12px;
        background: #f1f5f9;
        padding: 6px;
        border-radius: 16px;
        border: 1px solid var(--border-subtle);
    }
    .test-switcher-btn {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 18px;
        background: transparent;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        text-align: left;
        transition: all 0.25s ease;
        font-family: inherit;
    }
    .test-switcher-btn:hover {
        background: rgba(255, 255, 255, 0.7);
    }
    .test-switcher-btn.active {
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.12);
        border: 1px solid #ddd6fe;
    }
    .tab-badge-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #ede9fe;
        color: #7c3aed;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 15px;
    }
    .test-switcher-btn.active .tab-badge-num {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: #ffffff;
    }
    .tab-info strong {
        display: block;
        font-size: 14px;
        color: var(--text-heading);
    }
    .tab-info small {
        display: block;
        font-size: 11px;
        color: var(--text-muted);
        margin-top: 2px;
    }

    /* Test Pane & Layout Grid */
    .test-pane-container {
        display: block;
    }
    .test-layout-grid {
        display: grid;
        grid-template-columns: 1fr 280px;
        gap: 24px;
        align-items: start;
        margin-top: 20px;
    }
    .test-main-column {
        min-width: 0;
    }
    .test-sidebar-column {
        position: sticky;
        top: 75px;
        z-index: 40;
    }

    /* Sticky Exam Control Toolbar */
    .exam-control-sticky-bar {
        position: sticky;
        top: 60px;
        z-index: 60;
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(14px);
        border: 1.5px solid #e2e8f0;
        border-radius: 16px;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }
    .ctrl-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .timer-display-box {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #f8fafc;
        border: 1.5px solid #cbd5e1;
        padding: 6px 14px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .timer-display-box.timer-warning {
        background: #fffbeb;
        border-color: #f59e0b;
        color: #b45309;
        animation: pulseWarning 1.5s infinite;
    }
    .timer-display-box.timer-danger {
        background: #fef2f2;
        border-color: #ef4444;
        color: #b91c1c;
        animation: pulseDanger 0.8s infinite;
    }
    @keyframes pulseWarning {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    @keyframes pulseDanger {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { transform: scale(1.04); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
    }
    .timer-icon {
        color: #6d28d9;
        display: flex;
        align-items: center;
    }
    .timer-info {
        display: flex;
        flex-direction: column;
    }
    .timer-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-muted);
        font-weight: 700;
        line-height: 1;
    }
    .timer-digits {
        font-family: 'Plus Jakarta Sans', monospace;
        font-weight: 800;
        font-size: 18px;
        color: var(--text-heading);
        line-height: 1.2;
    }
    .timer-controls {
        display: flex;
        gap: 4px;
    }
    .btn-ctrl-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        border: 1px solid var(--border-subtle);
        background: #ffffff;
        color: var(--text-muted);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
    }
    .btn-ctrl-icon:hover {
        background: #ede9fe;
        color: #6d28d9;
        border-color: #c4b5fd;
    }

    .ctrl-mid {
        flex: 1;
        max-width: 320px;
    }
    .progress-meta {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        font-weight: 600;
        color: var(--text-muted);
        margin-bottom: 4px;
    }
    .progress-track {
        height: 8px;
        background: #e2e8f0;
        border-radius: 9999px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        border-radius: 9999px;
        transition: width 0.3s ease;
    }

    .ctrl-right {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .btn-exam-action {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        font-family: inherit;
    }
    .btn-submit {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
    }
    .btn-submit:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
    }
    .btn-check {
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
    }
    .btn-check:hover {
        background: #dbeafe;
    }
    .btn-reset {
        background: #f8fafc;
        color: var(--text-muted);
        border: 1px solid var(--border-subtle);
    }
    .btn-reset:hover {
        background: #f1f5f9;
        color: var(--text-heading);
    }

    /* Question Palette (Ma trận 40 câu) */
    .sticky-palette-card {
        background: #ffffff;
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 16px;
        box-shadow: var(--shadow-default);
    }
    .palette-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 12px;
    }
    .palette-title {
        font-size: 13px;
        font-weight: 800;
        color: var(--text-heading);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .palette-answered-count {
        font-size: 11px;
        font-weight: 700;
        color: #7c3aed;
        background: #f5f3ff;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    .palette-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 6px;
    }
    .palette-q-btn {
        width: 100%;
        aspect-ratio: 1;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background: #ffffff;
        color: var(--text-heading);
        font-weight: 700;
        font-size: 12px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.15s ease;
        font-family: inherit;
    }
    .palette-q-btn:hover {
        border-color: #7c3aed;
        background: #f5f3ff;
        color: #7c3aed;
        transform: scale(1.05);
    }
    .palette-q-btn.pal-answered {
        background: #2563eb;
        color: #ffffff;
        border-color: #1d4ed8;
    }
    .palette-q-btn.pal-correct {
        background: #10b981 !important;
        color: #ffffff !important;
        border-color: #059669 !important;
    }
    .palette-q-btn.pal-wrong {
        background: #ef4444 !important;
        color: #ffffff !important;
        border-color: #dc2626 !important;
    }
    .palette-q-btn.pal-skipped {
        background: #f1f5f9 !important;
        color: #94a3b8 !important;
        border-color: #cbd5e1 !important;
    }

    .palette-legend {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-top: 14px;
        padding-top: 12px;
        border-top: 1px solid var(--border-subtle);
        font-size: 11px;
        color: var(--text-muted);
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 3px;
    }
    .dot-blank { background: #ffffff; border: 1px solid #94a3b8; }
    .dot-answered { background: #2563eb; }
    .dot-correct { background: #10b981; }
    .dot-wrong { background: #ef4444; }

    /* Section Card */
    .test-section-card {
        background: #ffffff;
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .sec-header-strip {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
    }
    .sec-badge {
        background: #7c3aed;
        color: #ffffff;
        font-size: 11px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }
    .sec-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 17px;
        color: var(--primary-navy);
    }
    .sec-range {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-muted);
    }
    .sec-instruction {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 13px;
        color: #475569;
        background: #f8fafc;
        border-left: 3px solid #7c3aed;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 18px;
        line-height: 1.5;
    }
    .sec-instruction svg {
        flex-shrink: 0;
        margin-top: 3px;
        color: #7c3aed;
    }

    /* Passage Box */
    .passage-box {
        background: #fbfcfe;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 24px;
        font-size: 15px;
        line-height: 1.75;
        color: #1e293b;
        scroll-margin-top: 85px;
    }
    .passage-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16px;
        font-weight: 800;
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .passage-para {
        margin-bottom: 14px;
        text-align: justify;
    }
    .passage-para:last-child {
        margin-bottom: 0;
    }
    .exam-blank {
        display: inline-block;
        font-weight: 700;
        color: #2563eb;
        background: #eff6ff;
        padding: 1px 8px;
        border-radius: 4px;
        border-bottom: 2px dashed #3b82f6;
    }
    .underlined-target {
        text-decoration: underline 2px #7c3aed;
        text-underline-offset: 3px;
        font-weight: 700;
        color: #4c1d95;
    }

    .btn-jump-passage {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 700;
        color: #4f46e5;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        padding: 2px 8px;
        border-radius: 9999px;
        text-decoration: none;
        margin-left: 8px;
        vertical-align: middle;
        transition: all 0.2s ease;
    }
    .btn-jump-passage:hover {
        background: #e0e7ff;
        color: #3730a3;
        border-color: #a5b4fc;
        transform: translateY(-1px);
    }

    /* Question Item */
    .exam-question-item {
        background: #ffffff;
        border: 1.5px solid #f1f5f9;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 18px;
        transition: all 0.25s ease;
        overflow: hidden;
        width: 100%;
        box-sizing: border-box;
        scroll-margin-top: 85px;
    }
    .exam-question-item:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }
    .exam-question-item.item-answered {
        border-color: #bfdbfe;
        background: #fbfdff;
    }
    .exam-question-item.highlight-flash {
        animation: questionFlash 1.2s ease;
    }
    @keyframes questionFlash {
        0%, 100% { border-color: #f1f5f9; box-shadow: none; }
        30%, 70% { border-color: #7c3aed; box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.2); }
    }

    .q-title-row {
        font-size: 15px;
        line-height: 1.5;
        margin-bottom: 12px;
        color: var(--text-heading);
    }
    .q-num-badge {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        color: #1e3a8a;
        margin-right: 6px;
    }
    .q-prompt-text {
        font-weight: 600;
    }

    /* Dialogue Card */
    .dialogue-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 14px;
        font-size: 14px;
    }
    .dialogue-line {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 5px 0;
        border-bottom: 1px dashed #f1f5f9;
    }
    .dialogue-line:last-child {
        border-bottom: none;
    }
    .dialogue-bullet {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        border-radius: 6px;
        background: #ede9fe;
        color: #7c3aed;
        font-weight: 800;
        font-size: 12px;
        flex-shrink: 0;
    }
    .dialogue-text {
        color: #334155;
        line-height: 1.5;
    }
    .dialogue-note {
        font-style: italic;
        color: #64748b;
        padding: 4px 0;
    }

    /* Options Grid & Option Card */
    .exam-options-grid {
        display: grid;
        gap: 8px;
        margin-top: 10px;
        width: 100%;
        box-sizing: border-box;
    }
    .opts-grid-4cols {
        grid-template-columns: repeat(4, minmax(0, 1fr));
    }
    .opts-grid-2cols {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .opts-grid-1col {
        grid-template-columns: 1fr;
    }

    .exam-option-card {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        font-size: 14px;
        min-width: 0;
        max-width: 100%;
        box-sizing: border-box;
        overflow: hidden;
    }
    .exam-option-card:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
    }
    .exam-option-card input[type="radio"] {
        position: absolute;
        opacity: 0;
        pointer-events: none;
    }
    .opt-letter {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        border-radius: 8px;
        background: #ffffff;
        border: 1.5px solid #cbd5e1;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 12px;
        color: var(--text-heading);
        flex-shrink: 0;
        transition: all 0.2s;
    }
    .opt-text {
        flex: 1;
        color: #334155;
        line-height: 1.4;
        min-width: 0;
        word-break: break-word;
        overflow-wrap: break-word;
    }
    .opt-icon-badge {
        flex-shrink: 0;
        font-size: 14px;
        font-weight: 800;
    }

    /* Option Selected State */
    .exam-option-card.opt-selected {
        background: #eff6ff;
        border-color: #3b82f6;
    }
    .exam-option-card.opt-selected .opt-letter {
        background: #2563eb;
        color: #ffffff;
        border-color: #2563eb;
    }

    /* Post-Submit Review States */
    .exam-option-card.opt-correct {
        background: #ecfdf5 !important;
        border-color: #10b981 !important;
    }
    .exam-option-card.opt-correct .opt-letter {
        background: #10b981 !important;
        color: #ffffff !important;
        border-color: #10b981 !important;
    }
    .exam-option-card.opt-correct .opt-icon-badge::after {
        content: "✓ Đúng";
        color: #059669;
        font-size: 11px;
        font-weight: 800;
        background: #d1fae5;
        padding: 2px 8px;
        border-radius: 9999px;
    }

    .exam-option-card.opt-wrong {
        background: #fef2f2 !important;
        border-color: #ef4444 !important;
    }
    .exam-option-card.opt-wrong .opt-letter {
        background: #ef4444 !important;
        color: #ffffff !important;
        border-color: #ef4444 !important;
    }
    .exam-option-card.opt-wrong .opt-icon-badge::after {
        content: "✗ Bạn chọn";
        color: #dc2626;
        font-size: 11px;
        font-weight: 800;
        background: #fee2e2;
        padding: 2px 8px;
        border-radius: 9999px;
    }

    .exam-option-card.opt-correct-missed {
        background: #f0fdf4 !important;
        border: 2px dashed #10b981 !important;
    }
    .exam-option-card.opt-correct-missed .opt-letter {
        background: #10b981 !important;
        color: #ffffff !important;
        border-color: #10b981 !important;
    }
    .exam-option-card.opt-correct-missed .opt-icon-badge::after {
        content: "★ Đáp án đúng";
        color: #059669;
        font-size: 11px;
        font-weight: 800;
        background: #d1fae5;
        padding: 2px 8px;
        border-radius: 9999px;
    }

    /* Question Score Badge */
    .q-status-badge {
        margin-top: 10px;
        font-size: 12px;
        font-weight: 700;
    }
    .q-status-badge:empty {
        display: none;
    }
    .badge-scored-correct {
        color: #059669;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
    }
    .badge-scored-wrong {
        color: #dc2626;
        background: #fef2f2;
        border: 1px solid #fecaca;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
    }
    .badge-scored-skipped {
        color: #d97706;
        background: #fffbeb;
        border: 1px solid #fde68a;
        padding: 4px 10px;
        border-radius: 6px;
        display: inline-block;
    }

    /* Explanation Card */
    .exam-explanation-box {
        margin-top: 14px;
        background: #fbfdff;
        border: 1.5px solid #bfdbfe;
        border-radius: 12px;
        padding: 16px;
        animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-4px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .exp-top-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        padding-bottom: 10px;
        border-bottom: 1px solid #dbeafe;
        margin-bottom: 12px;
    }
    .exp-title-wrap {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .exp-icon {
        font-size: 16px;
    }
    .exp-title {
        font-size: 13px;
        font-weight: 800;
        color: #1e40af;
    }
    .exp-correct-pill {
        font-size: 12px;
        background: #dbeafe;
        color: #1e40af;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    .exp-knowledge-pill {
        font-size: 11px;
        font-weight: 700;
        background: #eff6ff;
        color: #2563eb;
        border: 1px solid #bfdbfe;
        padding: 3px 10px;
        border-radius: 9999px;
    }

    .exp-analysis-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .exp-analysis-item {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        font-size: 13px;
        line-height: 1.55;
        padding: 6px 10px;
        border-radius: 8px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
    }
    .exp-analysis-item.exp-item-correct {
        background: #f0fdf4;
        border-color: #bbf7d0;
    }
    .exp-item-key {
        font-weight: 800;
        color: #1e3a8a;
        flex-shrink: 0;
    }
    .exp-item-correct .exp-item-key {
        color: #15803d;
    }
    .exp-item-text {
        color: #334155;
    }
    .exp-analysis-text {
        font-size: 13px;
        line-height: 1.6;
        color: #334155;
        padding: 6px 0;
    }

    .exp-translation-wrap {
        margin-top: 12px;
        padding: 10px 12px;
        background: #f8fafc;
        border-left: 3px solid #3b82f6;
        border-radius: 0 8px 8px 0;
    }
    .exp-trans-title {
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        color: #1e40af;
        margin-bottom: 4px;
    }
    .exp-trans-content {
        font-size: 13px;
        line-height: 1.55;
        color: #1e293b;
        font-style: italic;
    }

    /* Score Summary Modal */
    .exam-modal-backdrop {
        position: fixed;
        inset: 0;
        z-index: 999;
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(6px);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
        animation: modalBackdrop 0.2s ease;
    }
    @keyframes modalBackdrop {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .exam-modal-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 36px 32px;
        max-width: 520px;
        width: 100%;
        position: relative;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        text-align: center;
        animation: modalCardPop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes modalCardPop {
        from { transform: scale(0.9); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    .modal-close-btn {
        position: absolute;
        top: 18px;
        right: 18px;
        width: 32px;
        height: 32px;
        border-radius: 9999px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        color: var(--text-muted);
        font-size: 15px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }
    .modal-close-btn:hover {
        background: #fee2e2;
        color: #ef4444;
        border-color: #fca5a5;
    }

    .modal-score-header {
        margin-bottom: 24px;
    }
    .score-badge-circle {
        width: 120px;
        height: 120px;
        margin: 0 auto 16px;
        border-radius: 9999px;
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        color: #ffffff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.35);
    }
    .score-large-val {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 40px;
        font-weight: 800;
        line-height: 1;
    }
    .score-scale-lbl {
        font-size: 11px;
        opacity: 0.85;
        font-weight: 700;
        margin-top: 2px;
    }
    .score-rating-banner {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 22px;
        font-weight: 800;
        color: #1e1b4b;
        margin-bottom: 6px;
    }
    .modal-score-subtitle {
        font-size: 13px;
        color: var(--text-muted);
    }

    .modal-score-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 24px;
    }
    .modal-stat-box {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .modal-stat-box .stat-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 20px;
        font-weight: 800;
        line-height: 1.1;
    }
    .modal-stat-box .stat-label {
        font-size: 10px;
        color: var(--text-muted);
        font-weight: 600;
        margin-top: 4px;
    }
    .modal-stat-box.stat-correct .stat-num { color: #059669; }
    .modal-stat-box.stat-wrong .stat-num { color: #dc2626; }
    .modal-stat-box.stat-skipped .stat-num { color: #d97706; }
    .modal-stat-box.stat-time .stat-num { color: #4338ca; }

    .modal-action-buttons {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .btn-modal-action {
        width: 100%;
        padding: 12px 20px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.2s ease;
        border: none;
        font-family: inherit;
    }
    .btn-modal-review {
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: #ffffff;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.25);
    }
    .btn-modal-review:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }
    .btn-modal-retake {
        background: #f1f5f9;
        color: var(--text-heading);
    }
    .btn-modal-retake:hover {
        background: #e2e8f0;
    }

    /* Mobile Palette Drawer & Toggle Button */
    .btn-palette-toggle {
        background: #f5f3ff;
        color: #6d28d9;
        border: 1.5px solid #ddd6fe;
    }
    .btn-palette-toggle:hover {
        background: #ede9fe;
        color: #5b21b6;
    }

    .mobile-palette-drawer-backdrop {
        position: fixed;
        inset: 0;
        z-index: 950;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(4px);
        display: flex;
        align-items: flex-end;
        justify-content: center;
        animation: drawerFadeIn 0.2s ease-out;
    }
    @keyframes drawerFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .mobile-palette-drawer {
        background: #ffffff;
        width: 100%;
        max-width: 520px;
        max-height: 82vh;
        border-radius: 24px 24px 0 0;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: drawerSlideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes drawerSlideUp {
        from { transform: translateY(100%); }
        to { transform: translateY(0); }
    }
    .drawer-drag-bar-wrap {
        display: flex;
        justify-content: center;
        padding: 10px 0 4px;
        cursor: pointer;
        width: 100%;
    }
    .drawer-drag-bar {
        width: 40px;
        height: 4px;
        border-radius: 9999px;
        background: #cbd5e1;
    }
    .mobile-palette-drawer-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 18px 12px;
        border-bottom: 1px solid #f1f5f9;
    }
    .drawer-header-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 15px;
        font-weight: 800;
        color: #1e1b4b;
    }
    .drawer-header-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .drawer-answered-pill {
        font-size: 11.5px;
        font-weight: 700;
        color: #7c3aed;
        background: #f5f3ff;
        padding: 3px 10px;
        border-radius: 9999px;
        border: 1px solid #ddd6fe;
    }
    .drawer-close-btn {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        color: #64748b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        cursor: pointer;
    }
    .mobile-palette-body {
        padding: 14px 18px 24px;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
    }
    .mobile-palette-instruction {
        font-size: 12px;
        color: #64748b;
        background: #f8fafc;
        border-radius: 8px;
        padding: 6px 10px;
        margin-bottom: 12px;
        text-align: center;
    }
    .mobile-drawer-grid {
        display: grid !important;
        grid-template-columns: repeat(8, 1fr) !important;
        gap: 8px !important;
    }
    .drawer-legend {
        margin-top: 16px;
    }

    /* Responsive Breakpoints */
    @media (max-width: 1400px) {
        .test-layout-grid {
            grid-template-columns: 1fr 240px;
            gap: 16px;
        }
        .opts-grid-4cols {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    @media (max-width: 1024px) {
        .test-layout-grid {
            grid-template-columns: 1fr;
        }
        .test-sidebar-column {
            position: static;
        }
        .opts-grid-4cols {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    @media (max-width: 768px) {
        .exam-control-sticky-bar {
            top: 76px !important;
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            margin-bottom: 16px;
        }
        .ctrl-left {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            gap: 8px;
        }
        .timer-display-box {
            padding: 4px 10px;
            gap: 6px;
        }
        .timer-digits {
            font-size: 15px;
        }
        .timer-label {
            font-size: 9px;
        }
        .ctrl-right {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: nowrap;
        }
        .btn-exam-action {
            padding: 6px 10px;
            font-size: 12px;
            border-radius: 8px;
            white-space: nowrap;
        }
        .btn-submit {
            font-weight: 800;
            box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
        }
        .ctrl-mid {
            width: 100%;
            max-width: 100%;
            cursor: pointer;
            padding: 2px 0;
        }
        .progress-meta {
            font-size: 10.5px;
            margin-bottom: 3px;
        }
        .progress-track {
            height: 6px;
        }

        /* Reading passage: left alignment on mobile for clean typography */
        .passage-box {
            padding: 14px 12px;
            font-size: 14px;
            line-height: 1.6;
            border-radius: 12px;
            margin-bottom: 16px;
        }
        .passage-para {
            text-align: left !important;
            margin-bottom: 12px;
        }

        /* Question items & options */
        .test-section-card {
            padding: 16px 12px;
            border-radius: 14px;
            margin-bottom: 16px;
        }
        .sec-title {
            font-size: 15px;
        }
        .sec-instruction {
            padding: 8px 10px;
            font-size: 12px;
            margin-bottom: 14px;
        }
        .exam-question-item {
            padding: 14px 12px;
            border-radius: 12px;
            margin-bottom: 14px;
        }
        .q-title-row {
            font-size: 14px;
            margin-bottom: 10px;
        }
        .exam-option-card {
            padding: 10px 12px;
            font-size: 13.5px;
            border-radius: 10px;
            min-height: 44px;
        }
        .opts-grid-4cols, .opts-grid-2cols {
            grid-template-columns: 1fr;
            gap: 8px;
        }
        .test-switcher-tabs {
            flex-direction: column;
            gap: 8px;
        }

        /* Bottom safe area padding to prevent FAB overlap */
        .test-pane-container {
            padding-bottom: 95px;
        }
        .test-sidebar-column {
            padding-bottom: 35px;
        }

        /* Score Modal on Mobile */
        .exam-modal-backdrop {
            padding: 12px;
        }
        .exam-modal-card {
            padding: 22px 14px;
            border-radius: 20px;
            max-height: 88vh;
            overflow-y: auto;
        }
        .score-badge-circle {
            width: 86px;
            height: 86px;
            margin-bottom: 10px;
        }
        .score-large-val {
            font-size: 30px;
        }
        .score-rating-banner {
            font-size: 18px;
        }
        .modal-score-subtitle {
            font-size: 12px;
        }
        .modal-score-stats-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            padding: 10px;
            margin-bottom: 16px;
        }
        .modal-stat-box .stat-num {
            font-size: 17px;
        }
        .btn-modal-action {
            padding: 11px 16px;
            font-size: 13.5px;
            min-height: 44px;
        }
    }
    @media (max-width: 420px) {
        .mobile-drawer-grid {
            grid-template-columns: repeat(5, 1fr) !important;
            gap: 6px !important;
        }
    }
    """


def get_test_js():
    """Return JavaScript logic for state management, timer, scoring, and palettes."""
    return """
    // ==========================================================================
    // INTERACTIVE ONLINE TEST CONTROLLER (TEST 01 & TEST 02)
    // ==========================================================================

    const ExamManager = {
        activeTestId: 'test1',
        tests: {
            test1: {
                totalQuestions: 40,
                durationSeconds: 3000,
                secondsRemaining: 3000,
                timerInterval: null,
                timerRunning: false,
                answers: {},
                isSubmitted: false,
                keys: {}
            },
            test2: {
                totalQuestions: 40,
                durationSeconds: 3000,
                secondsRemaining: 3000,
                timerInterval: null,
                timerRunning: false,
                answers: {},
                isSubmitted: false,
                keys: {}
            }
        },

        init() {
            // Load embedded answer keys
            try {
                const keysElem = document.getElementById('exam_keys_data');
                if (keysElem) {
                    const parsed = JSON.parse(keysElem.textContent);
                    if (parsed.test1) this.tests.test1.keys = parsed.test1;
                    if (parsed.test2) this.tests.test2.keys = parsed.test2;
                }
            } catch (e) {
                console.warn('Failed parsing embedded exam keys:', e);
            }
            this.updateTimerDisplay('test1');
            this.updateTimerDisplay('test2');
            this.updateProgress('test1');
            this.updateProgress('test2');
        },

        switchTest(testId) {
            this.activeTestId = testId;
            const pane1 = document.getElementById('pane_test1');
            const pane2 = document.getElementById('pane_test2');
            const btn1 = document.getElementById('btnTestTab1');
            const btn2 = document.getElementById('btnTestTab2');

            if (testId === 'test2') {
                if (pane1) pane1.style.display = 'none';
                if (pane2) pane2.style.display = 'block';
                if (btn1) btn1.classList.remove('active');
                if (btn2) btn2.classList.add('active');
            } else {
                if (pane1) pane1.style.display = 'block';
                if (pane2) pane2.style.display = 'none';
                if (btn1) btn1.classList.add('active');
                if (btn2) btn2.classList.remove('active');
            }
        },

        selectOption(testId, qNum, optKey) {
            const t = this.tests[testId];
            if (t.isSubmitted) return;

            // Auto-start timer on first selection
            if (!t.timerRunning && t.secondsRemaining > 0) {
                this.startTimer(testId);
            }

            t.answers[qNum] = optKey;

            // Update card styling
            ['A', 'B', 'C', 'D'].forEach(k => {
                const card = document.getElementById(`card_opt_${testId}_${qNum}_${k}`);
                if (card) {
                    if (k === optKey) {
                        card.classList.add('opt-selected');
                    } else {
                        card.classList.remove('opt-selected');
                    }
                }
            });

            // Mark question item as answered
            const qItem = document.getElementById(`q_${testId}_${qNum}`);
            if (qItem) qItem.classList.add('item-answered');

            // Update question palette
            const palBtn = document.getElementById(`pal_${testId}_${qNum}`);
            if (palBtn) palBtn.classList.add('pal-answered');

            const drawerGrid = document.getElementById('mobileDrawerGrid');
            if (drawerGrid && drawerGrid.children[qNum - 1]) {
                drawerGrid.children[qNum - 1].classList.add('pal-answered');
            }

            this.updateProgress(testId);
        },

        updateProgress(testId) {
            const t = this.tests[testId];
            const answered = Object.keys(t.answers).length;
            const total = t.totalQuestions;
            const pct = Math.round((answered / total) * 100);

            const statEl = document.getElementById(`progress_stat_${testId}`);
            const fillEl = document.getElementById(`progress_fill_${testId}`);
            const palCountEl = document.getElementById(`pal_count_${testId}`);
            const drawerCountEl = document.getElementById('mobileDrawerCount');

            if (statEl) statEl.textContent = `${answered} / ${total} câu (${pct}%)`;
            if (fillEl) fillEl.style.width = `${pct}%`;
            if (palCountEl) palCountEl.textContent = `${answered}/${total} đã chọn`;
            if (drawerCountEl) drawerCountEl.textContent = `${answered}/${total} đã chọn`;

            const fabExamPal = document.getElementById('fabExamPalette');
            if (fabExamPal) {
                const span = fabExamPal.querySelector('span');
                if (span) span.textContent = `Ma trận (${answered}/${total})`;
            }
        },

        startTimer(testId) {
            const t = this.tests[testId];
            if (t.timerRunning) return;
            t.timerRunning = true;
            this.updateTimerControls(testId);

            t.timerInterval = setInterval(() => {
                if (t.secondsRemaining > 0) {
                    t.secondsRemaining--;
                    this.updateTimerDisplay(testId);
                } else {
                    clearInterval(t.timerInterval);
                    t.timerRunning = false;
                    this.updateTimerControls(testId);
                    alert(`⏰ Hết giờ làm bài 50 phút cho ${testId.toUpperCase()}! Hệ thống đang tự động nộp bài và chấm điểm.`);
                    this.submitTest(testId);
                }
            }, 1000);
        },

        pauseTimer(testId) {
            const t = this.tests[testId];
            if (!t.timerRunning) return;
            clearInterval(t.timerInterval);
            t.timerRunning = false;
            this.updateTimerControls(testId);
        },

        toggleTimer(testId) {
            const t = this.tests[testId];
            if (t.timerRunning) {
                this.pauseTimer(testId);
            } else {
                this.startTimer(testId);
            }
        },

        resetTimer(testId) {
            const t = this.tests[testId];
            clearInterval(t.timerInterval);
            t.timerRunning = false;
            t.secondsRemaining = t.durationSeconds;
            this.updateTimerDisplay(testId);
            this.updateTimerControls(testId);
        },

        updateTimerDisplay(testId) {
            const t = this.tests[testId];
            const m = Math.floor(t.secondsRemaining / 60);
            const s = t.secondsRemaining % 60;
            const str = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;

            const el = document.getElementById(`timer_val_${testId}`);
            if (el) el.textContent = str;

            const box = document.getElementById(`timer_box_${testId}`);
            if (box) {
                box.classList.remove('timer-warning', 'timer-danger');
                if (t.secondsRemaining <= 60 && t.secondsRemaining > 0) {
                    box.classList.add('timer-danger');
                } else if (t.secondsRemaining <= 300 && t.secondsRemaining > 0) {
                    box.classList.add('timer-warning');
                }
            }
        },

        updateTimerControls(testId) {
            const t = this.tests[testId];
            const btn = document.getElementById(`btn_timer_toggle_${testId}`);
            if (!btn) return;
            if (t.timerRunning) {
                btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>`;
                btn.title = "Tạm dừng";
            } else {
                btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
                btn.title = "Tiếp tục";
            }
        },

        scrollToQuestion(testId, qNum) {
            const el = document.getElementById(`q_${testId}_${qNum}`);
            if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'start' });
                el.classList.add('highlight-flash');
                setTimeout(() => el.classList.remove('highlight-flash'), 1200);
            }
        },

        submitTest(testId, skipConfirm = false) {
            const t = this.tests[testId];
            const answeredCount = Object.keys(t.answers).length;
            const total = t.totalQuestions;

            if (!skipConfirm && answeredCount < total) {
                const unanswered = total - answeredCount;
                const ok = confirm(`Bạn mới làm ${answeredCount}/${total} câu (còn ${unanswered} câu chưa chọn). Bạn có chắc chắn muốn nộp bài ngay bây giờ?`);
                if (!ok) return;
            }

            // Stop Timer
            this.pauseTimer(testId);
            t.isSubmitted = true;

            const timeSpentSeconds = t.durationSeconds - t.secondsRemaining;
            const spentM = Math.floor(timeSpentSeconds / 60);
            const spentS = timeSpentSeconds % 60;
            const spentStr = `${String(spentM).padStart(2, '0')}:${String(spentS).padStart(2, '0')}`;

            let correctCount = 0;
            let wrongCount = 0;
            let skippedCount = 0;

            for (let q = 1; q <= total; q++) {
                const userAns = t.answers[q];
                const correctAns = t.keys[String(q)];
                const statusBadge = document.getElementById(`badge_${testId}_${q}`);
                const palBtn = document.getElementById(`pal_${testId}_${q}`);
                const expBox = document.getElementById(`exp_${testId}_${q}`);

                // Always reveal explanations on submit
                if (expBox) expBox.style.display = 'block';

                if (!userAns) {
                    skippedCount++;
                    if (statusBadge) {
                        statusBadge.innerHTML = `<span class="badge-scored-skipped">⚠️ Chưa trả lời (0đ) • Đáp án đúng: <strong>${correctAns || '---'}</strong></span>`;
                    }
                    if (palBtn) {
                        palBtn.className = 'palette-q-btn pal-skipped';
                        palBtn.innerHTML = `${q}`;
                    }
                    // Highlight correct option as missed
                    const correctCard = document.getElementById(`card_opt_${testId}_${q}_${correctAns}`);
                    if (correctCard) correctCard.classList.add('opt-correct-missed');
                } else if (userAns === correctAns) {
                    correctCount++;
                    if (statusBadge) {
                        statusBadge.innerHTML = `<span class="badge-scored-correct">✓ Đúng (+0.25đ)</span>`;
                    }
                    if (palBtn) {
                        palBtn.className = 'palette-q-btn pal-correct';
                        palBtn.innerHTML = `${q} ✓`;
                    }
                    const optCard = document.getElementById(`card_opt_${testId}_${q}_${userAns}`);
                    if (optCard) optCard.classList.add('opt-correct');
                } else {
                    wrongCount++;
                    if (statusBadge) {
                        statusBadge.innerHTML = `<span class="badge-scored-wrong">✗ Sai (0đ) • Đáp án đúng: <strong>${correctAns}</strong></span>`;
                    }
                    if (palBtn) {
                        palBtn.className = 'palette-q-btn pal-wrong';
                        palBtn.innerHTML = `${q} ✗`;
                    }
                    const userCard = document.getElementById(`card_opt_${testId}_${q}_${userAns}`);
                    if (userCard) userCard.classList.add('opt-wrong');
                    const correctCard = document.getElementById(`card_opt_${testId}_${q}_${correctAns}`);
                    if (correctCard) correctCard.classList.add('opt-correct-missed');
                }
            }

            // Calculate scaled score
            const scaledScore = (correctCount * 0.25).toFixed(2);
            this.showScoreModal(scaledScore, correctCount, wrongCount, skippedCount, spentStr);
        },

        showScoreModal(score, correct, wrong, skipped, timeSpent) {
            const modal = document.getElementById('examScoreModal');
            if (!modal) return;

            document.getElementById('modalScoreVal').textContent = score;
            document.getElementById('modalCorrectCount').textContent = correct;
            document.getElementById('modalWrongCount').textContent = wrong;
            document.getElementById('modalSkippedCount').textContent = skipped;
            document.getElementById('modalTimeSpent').textContent = timeSpent;

            const ratingEl = document.getElementById('modalScoreRating');
            const subEl = document.getElementById('modalScoreSubtitle');
            const sNum = parseFloat(score);

            if (sNum >= 9.0) {
                ratingEl.textContent = "Xuất Sắc! 🎉";
                subEl.textContent = "Thành tích tuyệt vời! Bạn nắm vững 100% ngữ pháp & từ vựng bài thi.";
            } else if (sNum >= 8.0) {
                ratingEl.textContent = "Rất Tốt! 🌟";
                subEl.textContent = "Kết quả rất cao! Đạt chuẩn điểm thi tốt nghiệp THPT xuất sắc.";
            } else if (sNum >= 6.5) {
                ratingEl.textContent = "Khá Tốt! 👍";
                subEl.textContent = "Nắm chắc các dạng bài cơ bản, hãy ôn thêm các câu phân hóa nhé.";
            } else if (sNum >= 5.0) {
                ratingEl.textContent = "Đạt Yêu Cầu! 📖";
                subEl.textContent = "Cần củng cố thêm từ vựng và cấu trúc ngữ pháp trọng tâm.";
            } else {
                ratingEl.textContent = "Cần Nỗ Lực Hơn! 💪";
                subEl.textContent = "Hãy đọc kỹ phần Lời giải chi tiết bên dưới để rút kinh nghiệm nhé.";
            }

            modal.style.display = 'flex';
        },

        checkAnswers(testId) {
            const t = this.tests[testId];
            const total = t.totalQuestions;

            // Reveal all explanations and correct answers without formal scoring
            for (let q = 1; q <= total; q++) {
                const correctAns = t.keys[String(q)];
                const expBox = document.getElementById(`exp_${testId}_${q}`);
                if (expBox) expBox.style.display = 'block';

                const correctCard = document.getElementById(`card_opt_${testId}_${q}_${correctAns}`);
                if (correctCard) correctCard.classList.add('opt-correct-missed');
            }
            alert(`🔍 Đã mở toàn bộ Đáp án & Lời giải chi tiết cho ${testId.toUpperCase()}! Bạn có thể cuộn xem từng câu hỏi.`);
        },

        resetAll(testId) {
            const ok = confirm(`Bạn có muốn làm lại ${testId.toUpperCase()} từ đầu không? Toàn bộ lựa chọn sẽ được đặt lại.`);
            if (!ok) return;

            const t = this.tests[testId];
            this.resetTimer(testId);
            t.answers = {};
            t.isSubmitted = false;

            const total = t.totalQuestions;
            for (let q = 1; q <= total; q++) {
                // Reset radios
                const radios = document.getElementsByName(`q_${testId}_${q}`);
                radios.forEach(r => { r.checked = false; });

                // Reset cards
                ['A', 'B', 'C', 'D'].forEach(k => {
                    const card = document.getElementById(`card_opt_${testId}_${q}_${k}`);
                    if (card) {
                        card.className = 'exam-option-card';
                    }
                });

                // Reset question container
                const qItem = document.getElementById(`q_${testId}_${q}`);
                if (qItem) qItem.className = 'exam-question-item';

                // Reset status badge
                const badge = document.getElementById(`badge_${testId}_${q}`);
                if (badge) badge.innerHTML = '';

                // Hide explanation
                const expBox = document.getElementById(`exp_${testId}_${q}`);
                if (expBox) expBox.style.display = 'none';

                // Reset palette button
                const palBtn = document.getElementById(`pal_${testId}_${q}`);
                if (palBtn) {
                    palBtn.className = 'palette-q-btn';
                    palBtn.textContent = `${q}`;
                }
            }

            this.updateProgress(testId);
        }
    };

    // Global Wrapper Functions for inline handlers
    function switchExamTab(testId) {
        ExamManager.switchTest(testId);
    }
    function examSelectOption(testId, qNum, optKey) {
        ExamManager.selectOption(testId, qNum, optKey);
    }
    function examToggleTimer(testId) {
        ExamManager.toggleTimer(testId);
    }
    function examResetTimer(testId) {
        ExamManager.resetTimer(testId);
    }
    function examScrollToQuestion(testId, qNum) {
        ExamManager.scrollToQuestion(testId, qNum);
    }
    function examSubmitTest(testId) {
        ExamManager.submitTest(testId);
    }
    function examCheckAnswers(testId) {
        ExamManager.checkAnswers(testId);
    }
    function examResetAll(testId) {
        ExamManager.resetAll(testId);
    }
    function closeExamModal() {
        const modal = document.getElementById('examScoreModal');
        if (modal) modal.style.display = 'none';
    }
    function closeExamModalAndReview() {
        closeExamModal();
        const activePane = document.getElementById(`pane_${ExamManager.activeTestId}`);
        if (activePane) activePane.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    function modalRetakeExam() {
        closeExamModal();
        ExamManager.resetAll(ExamManager.activeTestId);
    }

    function toggleMobilePalette(testId) {
        testId = testId || ExamManager.activeTestId;
        const backdrop = document.getElementById('mobilePaletteDrawerBackdrop');
        if (!backdrop) return;
        
        if (backdrop.style.display === 'flex') {
            closeMobilePalette();
            return;
        }
        
        const t = ExamManager.tests[testId];
        const total = t ? t.totalQuestions : 40;
        const answered = t ? Object.keys(t.answers).length : 0;
        
        const titleEl = document.getElementById('mobileDrawerTitle');
        const countEl = document.getElementById('mobileDrawerCount');
        const gridEl = document.getElementById('mobileDrawerGrid');
        
        if (titleEl) {
            titleEl.textContent = `Ma Trận 40 Câu (${testId === 'test2' ? 'Test 02' : 'Test 01'})`;
        }
        if (countEl) {
            countEl.textContent = `${answered}/${total} đã chọn`;
        }
        
        if (gridEl) {
            gridEl.innerHTML = '';
            for (let i = 1; i <= total; i++) {
                const origBtn = document.getElementById(`pal_${testId}_${i}`);
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = origBtn ? origBtn.className : 'palette-q-btn';
                btn.textContent = origBtn ? origBtn.textContent : String(i);
                btn.onclick = () => {
                    examScrollToQuestion(testId, i);
                    closeMobilePalette();
                };
                gridEl.appendChild(btn);
            }
        }
        
        backdrop.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeMobilePalette() {
        const backdrop = document.getElementById('mobilePaletteDrawerBackdrop');
        if (backdrop) backdrop.style.display = 'none';
        document.body.style.overflow = '';
    }

    // Keyboard support: Escape closes mobile drawer & modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeMobilePalette();
            closeExamModal();
        }
    });

    // Auto-init on DOM load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            ExamManager.init();
            if (typeof initDesktopSidebar === 'function') initDesktopSidebar();
        });
    } else {
        ExamManager.init();
        if (typeof initDesktopSidebar === 'function') initDesktopSidebar();
    }
    """


def inject_into_index_html(index_path, test1_data, test2_data, unit_num=1):
    """
    Seamlessly inject the complete Online Test Portal into index.html:
    1. Header nav tab: 'tabTest'
    2. switchMainTab support for 'test'
    3. Sidebar statistics & quick navigation link
    4. #section-test markup before </main>
    5. CSS inside <style>
    6. JS inside <script>
    """
    p = Path(index_path)
    if not p.exists():
        print(f"[Error] index.html not found at: {index_path}", file=sys.stderr)
        return False

    with open(p, "r", encoding="utf-8") as f:
        html = f.read()

    print(f"[Info] Read {len(html)} chars from {index_path}")

    # 1. Update header-nav-tabs
    test_tab_btn = '<button type="button" class="nav-tab-btn" id="tabTest" onclick="switchMainTab(\'test\')">📝 Test (Test01 &amp; Test02)</button>'
    if 'id="tabTest"' not in html:
        # Insert after tabGrammar
        grammar_tab_pat = r'(<button[^>]+id="tabGrammar"[^>]*>.*?</button>)'
        if re.search(grammar_tab_pat, html):
            html = re.sub(grammar_tab_pat, r'\1\n                ' + test_tab_btn, html, count=1)
            print("[Success] Injected #tabTest button into header-nav-tabs")
        else:
            print("[Warning] Could not find #tabGrammar to place #tabTest button", file=sys.stderr)

    # 2. Update switchMainTab in JS
    # Look for function switchMainTab(tab)
    if "const testSec = document.getElementById('section-test');" not in html:
        old_switch_pat = r'function switchMainTab\(tab\)\s*\{([\s\S]*?)const btns = \[(.*?)\];'
        m = re.search(old_switch_pat, html)
        if m:
            inner_decl = m.group(1)
            btns_arr = m.group(2)
            new_decl = inner_decl + "            const testSec = document.getElementById('section-test');\n"
            new_btns = btns_arr if "'tabTest'" in btns_arr else btns_arr.rstrip() + ", 'tabTest'"
            replacement = f"function switchMainTab(tab) {{\n{new_decl}            const btns = [{new_btns}];"
            html = html.replace(m.group(0), replacement, 1)

            # Now handle tab === 'test' inside switchMainTab
            old_grammar_branch = r"(if\s*\(\s*tab\s*===\s*'grammar'\s*\)\s*\{[\s\S]*?const el = document\.getElementById\('tabGrammar'\);[\s\S]*?if \(el\) el\.classList\.add\('active'\);[\s\S]*?\})"
            gm = re.search(old_grammar_branch, html)
            if gm:
                test_branch = """ else if (tab === 'test') {
                if (theorySec) theorySec.style.display = 'none';
                if (exSec) exSec.style.display = 'none';
                if (grammarSec) grammarSec.style.display = 'none';
                if (testSec) testSec.style.display = 'block';
                const el = document.getElementById('tabTest');
                if (el) el.classList.add('active');
            }"""
                html = html.replace(gm.group(0), gm.group(0)[:-1].rstrip() + " " + test_branch, 1)

                # Update theorySec/exSec/grammarSec display handling in other branches
                # For 'theory', 'exercises', 'grammar', ensure testSec is hidden
                html = re.sub(r"(if\s*\(theorySec\)\s*theorySec\.style\.display\s*=\s*'block';\s*if\s*\(exSec\)\s*exSec\.style\.display\s*=\s*'none';\s*if\s*\(grammarSec\)\s*grammarSec\.style\.display\s*=\s*'none';)",
                              r"\1\n                if (testSec) testSec.style.display = 'none';", html)
                html = re.sub(r"(if\s*\(theorySec\)\s*theorySec\.style\.display\s*=\s*'none';\s*if\s*\(exSec\)\s*exSec\.style\.display\s*=\s*'block';\s*if\s*\(grammarSec\)\s*grammarSec\.style\.display\s*=\s*'none';)",
                              r"\1\n                if (testSec) testSec.style.display = 'none';", html)
                html = re.sub(r"(if\s*\(theorySec\)\s*theorySec\.style\.display\s*=\s*'none';\s*if\s*\(exSec\)\s*exSec\.style\.display\s*=\s*'none';\s*if\s*\(grammarSec\)\s*grammarSec\.style\.display\s*=\s*'block';)",
                              r"\1\n                if (testSec) testSec.style.display = 'none';", html)
                # For 'all', ensure testSec is block
                html = re.sub(r"(if\s*\(theorySec\)\s*theorySec\.style\.display\s*=\s*'block';\s*if\s*\(exSec\)\s*exSec\.style\.display\s*=\s*'block';\s*if\s*\(grammarSec\)\s*grammarSec\.style\.display\s*=\s*'block';)",
                              r"\1\n                if (testSec) testSec.style.display = 'block';", html)

                print("[Success] Updated switchMainTab to support 'test' tab")

    # 3. Update Sidebar Stats & Navigation
    if 'id="stat_tests_count"' not in html:
        stats_needle = '<div class="stats-2x2">'
        if stats_needle in html:
            extra_stats = """<div class="stat-item">
                        <div class="stat-val" id="stat_tests_count">2</div>
                        <div class="stat-lbl">Đề thi THPT</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val" id="stat_test_q_count">80</div>
                        <div class="stat-lbl">Câu hỏi Test</div>
                    </div>"""
            html = html.replace(stats_needle, stats_needle + "\n                    " + extra_stats, 1)
            print("[Success] Added Test statistics to sidebar stats card")

    if 'href="#section-test"' not in html:
        sidebar_link_needle = '<li><a href="#g_u1_h"'
        if sidebar_link_needle in html:
            extra_nav_links = """<li style="margin-top: 14px; padding-top: 10px; border-top: 1px dashed #cbd5e1;">
            <a href="#section-test" class="nav-item" onclick="activateNav(this); switchMainTab('test');" style="font-weight: 700; color: #7c3aed;">
                <span>📝 Đề Thi Chuẩn THPT (Test 1 &amp; 2)</span>
                <span class="nav-badge" style="background: #f5f3ff; color: #7c3aed; border: 1px solid #c4b5fd;">2 Đề</span>
            </a>
        </li>
        <li><a href="#pane_test1" class="nav-item" onclick="activateNav(this); switchMainTab('test'); switchExamTab('test1');"><span>📋 Unit 1 – Test 01 (40 câu)</span></a></li>
        <li><a href="#pane_test2" class="nav-item" onclick="activateNav(this); switchMainTab('test'); switchExamTab('test2');"><span>📋 Unit 1 – Test 02 (40 câu)</span></a></li>"""
            # Insert after the list item for g_u1_h
            html = re.sub(r'(<li><a href="#g_u1_h"[^>]*>.*?</a></li>)', r'\1\n        ' + extra_nav_links, html, count=1)
            print("[Success] Added Test links to sidebar navigation list")

    # 4. Generate & Inject Section 4 HTML
    test_section_html = render_full_test_section(test1_data, test2_data, unit_num)

    if 'id="section-test"' in html:
        print("[Info] Replacing existing #section-test in index.html...")
        section_pat = r'(?:<!-- (?:START )?SECTION 4: ĐỀ THI[\s\S]*?<!-- END SECTION 4: ĐỀ THI.*?-->|<section class="section-box tab-content-test" id="section-test"[\s\S]*?(?:<!-- END SECTION 4: ĐỀ THI.*?-->|<!-- EXAM SCORE SUMMARY MODAL[\s\S]*?id="examScoreModal"[\s\S]*?</div>\s*</div>\s*(?:<div class="modal-action-buttons">[\s\S]*?</div>\s*</div>\s*</div>)*))'
        if re.search(section_pat, html):
            html = re.sub(section_pat, test_section_html.strip(), html, count=1)
        else:
            html = re.sub(r'<!-- (?:START )?SECTION 4: ĐỀ THI[\s\S]*?</main>', test_section_html.strip() + "\n\n        </main>", html, count=1)
    else:
        # Insert before </main>
        main_end_needle = '</main>'
        if main_end_needle in html:
            html = html.replace(main_end_needle, "\n" + test_section_html + "\n\n        " + main_end_needle, 1)
            print("[Success] Injected #section-test markup before </main>")
        else:
            print("[Error] Could not find </main> in index.html", file=sys.stderr)
            return False

    # 5. Inject / Update CSS styles
    test_css = get_test_css()
    if 'ONLINE TEST SYSTEM STYLES' in html:
        print("[Info] Updating existing test CSS in index.html...")
        html = re.sub(r'/\* ==========================================================================\s+ONLINE TEST SYSTEM STYLES[\s\S]*?</style>',
                      test_css.strip() + "\n    </style>", html, count=1)
    else:
        style_end_needle = '</style>'
        if style_end_needle in html:
            html = html.replace(style_end_needle, "\n" + test_css + "\n    " + style_end_needle, 1)
            print("[Success] Injected test CSS styles into <style>")

    # 6. Inject / Update JS logic
    test_js = get_test_js()
    if '// INTERACTIVE ONLINE TEST CONTROLLER' in html:
        print("[Info] Updating existing test JS controller in index.html...")
        html = re.sub(r'// ==========================================================================\s+// INTERACTIVE ONLINE TEST CONTROLLER[\s\S]*?</script>',
                      test_js.strip() + "\n    </script>", html, count=1)
    else:
        script_end_needle = '</script>'
        last_script_idx = html.rfind('</script>')
        if last_script_idx != -1:
            html = html[:last_script_idx] + "\n" + test_js + "\n    " + html[last_script_idx:]
            print("[Success] Injected test JS controller into <script>")

    # 7. Add Floating Action Button for Exam Palette
    if 'id="fabExamPalette"' not in html:
        fab_needle = '<div class="mobile-fab-container" id="mobileFabContainer">'
        if fab_needle in html:
            fab_exam_btn = '''        <button type="button" class="fab-btn fab-palette" id="fabExamPalette" onclick="toggleMobilePalette()" title="Mở ma trận 40 câu hỏi" style="display: none; background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #ffffff;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
            <span>Ma trận</span>
        </button>'''
            html = html.replace(fab_needle, fab_needle + "\n" + fab_exam_btn, 1)
            print("[Success] Injected #fabExamPalette into mobile-fab-container")

    # 8. Hook fabExamPalette in switchMainTab
    if "const fabPal = document.getElementById('fabExamPalette');" not in html:
        tab_test_branch = r"(if\s*\(\s*tab\s*===\s*'test'\s*\)\s*\{[\s\S]*?if\s*\(el\)\s*el\.classList\.add\('active'\);)"
        if re.search(tab_test_branch, html):
            enhanced_branch = r'''\1
                const fabPal = document.getElementById('fabExamPalette');
                const fabToc = document.getElementById('fabTOC');
                if (fabPal) fabPal.style.display = 'inline-flex';
                if (fabToc) fabToc.style.display = 'none';'''
            html = re.sub(tab_test_branch, enhanced_branch, html, count=1)
            
            # Hide fabPal when leaving test tab
            html = re.sub(r"(if\s*\(el\)\s*el\.classList\.add\('active'\);(?!\s*const fabPal))",
                          r'''\1
                const fabPal = document.getElementById('fabExamPalette');
                const fabToc = document.getElementById('fabTOC');
                if (fabPal) fabPal.style.display = 'none';
                if (fabToc) fabToc.style.display = '';''',
                          html)
            print("[Success] Enhanced switchMainTab to toggle #fabExamPalette")

    with open(p, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Done] index.html successfully updated! ({len(html)} chars)")
    return True


def generate_standalone_test_page(test1_data, test2_data, unit_num, output_path):
    """
    Generate a standalone, responsive, interactive HTML file for Unit Tests.
    """
    test_section_html = render_full_test_section(test1_data, test2_data, unit_num)
    test_css = get_test_css()
    test_js = get_test_js()

    standalone_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLOBAL SUCCESS 10 • UNIT {unit_num} – ĐỀ THI TỐT NGHIỆP THPT (TEST 01 &amp; TEST 02)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-blue: #2563eb;
            --primary-dark: #1d4ed8;
            --primary-navy: #1e3a8a;
            --primary-light: #eff6ff;
            --surface-white: #ffffff;
            --bg-page: #f8fafc;
            --text-main: #0f172a;
            --text-heading: #1e293b;
            --text-muted: #64748b;
            --border-subtle: #e2e8f0;
            --shadow-default: 0 4px 20px -2px rgba(37, 99, 235, 0.08);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Be Vietnam Pro', sans-serif;
            background: var(--bg-page);
            color: var(--text-main);
            line-height: 1.55;
            padding: 24px 16px 60px;
        }}
        .standalone-container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header-brand-bar {{
            background: #ffffff;
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }}
        .brand-logo-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .brand-badge {{
            background: linear-gradient(135deg, #7c3aed, #4f46e5);
            color: #ffffff;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 13px;
            padding: 6px 14px;
            border-radius: 9999px;
        }}
        .brand-text h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 18px;
            font-weight: 800;
            color: #1e1b4b;
        }}
        .brand-text p {{
            font-size: 12px;
            color: var(--text-muted);
        }}
        .btn-portal-back {{
            text-decoration: none;
            color: #4f46e5;
            font-size: 13px;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 9999px;
            background: #ede9fe;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-portal-back:hover {{
            background: #ddd6fe;
        }}
        .mobile-fab-container {{
            display: none;
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 12px 10px 60px;
            }}
            .header-brand-bar {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
                padding: 14px 16px;
                border-radius: 14px;
            }}
            .brand-text h1 {{
                font-size: 15px;
            }}
            .btn-portal-back {{
                align-self: flex-start;
                font-size: 12px;
                padding: 6px 14px;
            }}
            .mobile-fab-container {{
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                gap: 10px;
                position: fixed;
                bottom: 20px;
                right: 14px;
                z-index: 900;
                pointer-events: none;
            }}
            .fab-btn {{
                pointer-events: auto;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 10px 16px;
                border-radius: 9999px;
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 13px;
                font-weight: 700;
                border: none;
                cursor: pointer;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18), 0 2px 6px rgba(0, 0, 0, 0.08);
                transition: transform 0.2s;
            }}
            .fab-btn:active {{
                transform: scale(0.94);
            }}
            .fab-top {{
                background: #ffffff;
                color: #1e3a8a;
                border: 1.5px solid #bfdbfe;
            }}
        }}
        {test_css}
    </style>
</head>
<body>
    <div class="standalone-container">
        <header class="header-brand-bar">
            <div class="brand-logo-wrap">
                <span class="brand-badge">GS10 • UNIT {unit_num}</span>
                <div class="brand-text">
                    <h1>Hệ Thống Đề Thi Tốt Nghiệp THPT Chuẩn Hóa</h1>
                    <p>Chuẩn format Bộ GD&amp;ĐT 2025 • Test 01 &amp; Test 02 • 40 câu trắc nghiệm • 50 phút</p>
                </div>
            </div>
            <a href="../../../index.html" class="btn-portal-back">
                ← Quay lại Bài học chính
            </a>
        </header>

        <main>
            {test_section_html}
        </main>
    </div>

    <!-- MOBILE FLOATING ACTION BUTTONS -->
    <div class="mobile-fab-container" id="mobileFabContainer">
        <button type="button" class="fab-btn fab-palette" id="fabExamPalette" onclick="toggleMobilePalette()" title="Mở ma trận 40 câu hỏi" style="background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #ffffff;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
            <span>Ma trận</span>
        </button>
        <button type="button" class="fab-btn fab-top" id="fabTop" onclick="window.scrollTo({{top:0, behavior:'smooth'}})" title="Lên đầu trang">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="18 15 12 9 6 15"/>
            </svg>
            <span>Lên đầu</span>
        </button>
    </div>

    <script>
        {test_js}
    </script>
</body>
</html>"""

    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "w", encoding="utf-8") as f:
        f.write(standalone_html)
    print(f"[Done] Standalone test page saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Online Test Portal Builder for GS10")
    parser.add_argument("--unit", type=int, default=1, help="Unit number (default: 1)")
    parser.add_argument("--workspace", type=str, default="d:\\GS10", help="Workspace root path")
    parser.add_argument("--inject-index", action="store_true", default=True, help="Inject into index.html")
    parser.add_argument("--standalone", action="store_true", default=True, help="Generate standalone test page")
    args = parser.parse_args()

    workspace_root = Path(args.workspace)
    test_dir = workspace_root / "lessons" / f"unit-{args.unit}" / "test"
    test1_path = test_dir / "test1.json"
    test2_path = test_dir / "test2.json"

    print(f"[Info] Loading Test 1: {test1_path}")
    test1_data = load_json(test1_path)
    print(f"[Info] Loading Test 2: {test2_path}")
    test2_data = load_json(test2_path)

    if not test1_data or not test2_data:
        print("[Error] Failed to load test JSON data. Exiting.", file=sys.stderr)
        sys.exit(1)

    # 1. Generate standalone test page
    if args.standalone:
        out_standalone = test_dir / f"test_unit{args.unit}.html"
        generate_standalone_test_page(test1_data, test2_data, args.unit, out_standalone)
        # Also copy to root for easy direct URL access if desired
        root_test_standalone = workspace_root / f"test_unit{args.unit}.html"
        generate_standalone_test_page(test1_data, test2_data, args.unit, root_test_standalone)

    # 2. Inject into index.html
    if args.inject_index:
        index_file = workspace_root / "index.html"
        inject_into_index_html(index_file, test1_data, test2_data, args.unit)


if __name__ == "__main__":
    main()
