#!/usr/bin/env python3
"""
Grammar & Vocabulary Portal Builder (build_grammar_portal.py)

Generates:
1. `index.html`: Unified, publication-grade web portal combining:
   - Dynamic Unit Switcher (Unit 1, Unit 2, Unit 3)
   - Vocabulary Flashcards (conforming to cards.html Modern Blue specification)
   - 16 Vocabulary Practice Exercises
   - Grammar Theory (conforming strictly to textbook layout: top accent bar, lesson header,
     pill badges, dark navy #1e3a8a tables with bold blue highlighted structures, amber WATCH OUT! boxes)
   - 8 Grammar Practice Exercises (A through H with bold section letters, italic sub-instructions,
     dotted underline handwriting blanks, interactive checks, scoring, and explanations)
   - Fast Live Search, Dual Review/Practice modes, and Print styles.
2. Standalone `grammar_unit<N>.html` for each unit.
"""

import os
import sys
import json
import glob
import re
import argparse
from pathlib import Path
from html import escape

# Ensure proper stdout encoding on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_json(filepath):
    """Safely load and parse JSON."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed loading {filepath}: {e}", file=sys.stderr)
        return None


def get_units_list(workspace_root):
    """Find all unit directories under lessons/."""
    lessons_dir = workspace_root / "lessons"
    units = []
    if lessons_dir.is_dir():
        for d in sorted(lessons_dir.iterdir()):
            if d.is_dir() and re.match(r"^unit-\d+$", d.name, re.IGNORECASE):
                u_num = int(d.name.split("-")[1])
                units.append(u_num)
    return sorted(units) if units else [1, 2, 3]


def load_grammar_theory_db(workspace_root):
    """Load grammar theory database from reference folder."""
    db_file = workspace_root / ".agent" / "skills" / "skills-grammar-theory-exercises" / "reference" / "grammar_theory_database.json"
    if db_file.exists():
        return load_json(db_file)
    return {}


def render_grammar_theory_html(unit_num, theory_data):
    """
    Render grammar theory conforming strictly to the textbook images:
    - Top accent line
    - Lesson header: LESSON <N> – <GRAMMAR TOPIC>
    - Pill section badge: <div class="grammar-pill">...</div>
    - Introductory bullets
    - Contrastive / Rule Table with #1e3a8a header, white text, bold blue target words
    - Amber WATCH OUT! box
    """
    if not theory_data:
        return "<p>Đang cập nhật lý thuyết ngữ pháp...</p>"

    lesson_title = theory_data.get("lesson_title", f"LESSON {unit_num} – GRAMMAR THEORY")
    sections = theory_data.get("sections", [])

    html_parts = []
    html_parts.append(f"""
    <div class="grammar-doc-container">
        <!-- Top Accent Bar & Lesson Title -->
        <div class="lesson-top-bar"></div>
        <div class="lesson-header-title">
            <h2>{escape(lesson_title)}</h2>
        </div>
    """)

    for sec in sections:
        pill = sec.get("pill_badge", "")
        intro_bullets = sec.get("intro_bullets", [])
        tbl = sec.get("table", {})
        watch_out = sec.get("watch_out", {})

        html_parts.append('<div class="grammar-theory-subtopic">')
        if pill:
            html_parts.append(f'<div class="grammar-pill">{escape(pill)}</div>')

        if intro_bullets:
            html_parts.append('<ul class="grammar-intro-list">')
            for b in intro_bullets:
                html_parts.append(f'<li>{b}</li>')
            html_parts.append('</ul>')

        if tbl and "headers" in tbl and "rows" in tbl:
            headers = tbl["headers"]
            rows = tbl["rows"]
            html_parts.append('<div class="grammar-table-wrapper">')
            html_parts.append('<table class="grammar-styled-table">')
            html_parts.append('<thead><tr>')
            for h in headers:
                html_parts.append(f'<th>{escape(h)}</th>')
            html_parts.append('</tr></thead>')
            html_parts.append('<tbody>')
            for r in rows:
                html_parts.append('<tr>')
                for cell in r:
                    html_parts.append(f'<td>{cell}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody>')
            html_parts.append('</table>')
            html_parts.append('</div>')

        if watch_out and "bullets" in watch_out:
            w_bullets = watch_out.get("bullets", [])
            if w_bullets:
                html_parts.append("""
                <div class="watch-out-box">
                    <div class="watch-out-header">
                        <span class="watch-out-icon">⚠</span> WATCH OUT!
                    </div>
                    <ul class="watch-out-list">
                """)
                for wb in w_bullets:
                    html_parts.append(f'<li>{wb}</li>')
                html_parts.append("""
                    </ul>
                </div>
                """)

        html_parts.append('</div>')  # subtopic

    html_parts.append("</div>")  # doc container
    return "\n".join(html_parts)


def render_grammar_exercises_html(unit_num, ex_files_dict, theory_data):
    """
    Render grammar exercises A through H conforming strictly to Image 3:
    - Bold letter badge (A, B, C, D, E, F, G, H)
    - Bold exercise title
    - Italic sub-instruction
    - Questions with dotted handwriting blank, bracketed prompts, interactive inputs,
      per-exercise check button, and answer explanation.
    """
    lesson_title = theory_data.get("lesson_title", f"LESSON {unit_num} – GRAMMAR PRACTICE")
    html_parts = []

    html_parts.append(f"""
    <div class="grammar-exercises-doc">
        <!-- Top Accent Bar & Lesson Title -->
        <div class="lesson-top-bar"></div>
        <div class="lesson-header-title">
            <h2>{escape(lesson_title)} – PRACTICE EXERCISES</h2>
        </div>
    """)

    # Standard exercise mapping order:
    ordered_keys = [
        ("A", "02_verbform.json", "Complete using the correct form of the verb in brackets.",
         "Apply target tense rules. Pay special attention to time markers, interruptions, and parallel actions."),
        ("B", "01_mcq.json", "Choose the best option (A, B, C, or D) that correctly completes each sentence.",
         "Analyze time clauses, grammatical agreements, and contextual clues carefully."),
        ("C", "03_matching.json", "Match the sentence beginnings (1–10) with the appropriate endings (A–J).",
         "Create logically coherent and syntactically sound compound/complex sentences."),
        ("D", "04_rewrite.json", "Rewrite each sentence using the cue provided so that it has the same meaning.",
         "Use the given cue word without changing the original core meaning."),
        ("E", "05_guided_cloze.json", "Read the following passages and choose the best option (A, B, C, or D) for each blank.",
         "Apply target grammar rules and context vocabulary within authentic discourse."),
        ("F", "06_error_identification.json", "Identify the bracketed part [A, B, C, or D] containing an error, then write the correct form.",
         "Pay special attention to verb forms, prepositions, and structural agreements."),
        ("G", "07_sentence_combination.json", "Combine each pair of sentences into a single sentence using the cue provided.",
         "Connect clauses accurately using target conjunctions or relative pronouns."),
        ("H", "08_sentence_building.json", "Use the given cue words to write complete, grammatically correct sentences.",
         "Supply necessary prepositions, auxiliary verbs, and proper grammatical forms.")
    ]

    for letter, filename, default_title, default_instruction in ordered_keys:
        ex_data = ex_files_dict.get(filename)
        if not ex_data:
            continue

        title = default_title
        instruction = ex_data.get("instruction", default_instruction)
        ex_type = ex_data.get("type", "")
        ex_id = f"g_u{unit_num}_{letter.lower()}"

        html_parts.append(f"""
        <div class="grammar-exercise-card" id="{ex_id}" data-unit="{unit_num}">
            <div class="exercise-header-row">
                <div class="exercise-title-wrap">
                    <span class="exercise-letter-badge">{letter}</span>
                    <span class="exercise-main-title">{escape(title)}</span>
                </div>
                <div class="exercise-badge-type">{escape(ex_type.replace('_', ' ').title())}</div>
            </div>
            <div class="exercise-subinstruction">{escape(instruction)}</div>
            <div class="exercise-questions-body">
        """)

        # Render questions according to exercise type
        if filename == "02_verbform.json":
            # Dotted underline blank with bracketed prompt (Image 3 Ex A)
            questions = ex_data.get("questions", [])
            for q in questions:
                qid = q.get("id", "")
                text = q.get("text", "")
                ans = q.get("correct_answer", "")
                exp = q.get("explanation", "")

                if "______" in text:
                    input_html = f'<input type="text" class="dotted-text-input" data-ans="{escape(ans)}" placeholder=". . . . . . . . . . . ." autocomplete="off">'
                    q_formatted = text.replace("______", input_html)
                else:
                    q_formatted = f'{text} <input type="text" class="dotted-text-input" data-ans="{escape(ans)}" placeholder=". . . . . . . . . . . ." autocomplete="off">'

                html_parts.append(f"""
                <div class="q-row-item" data-qid="{qid}">
                    <span class="q-number">{qid}</span>
                    <div class="q-content-text">{q_formatted}</div>
                    <div class="q-feedback-slot"></div>
                    <div class="q-explanation-slot" style="display:none;">
                        <span class="exp-label">💡 Giải thích:</span> {escape(exp)} (Đáp án: <strong>{escape(ans)}</strong>)
                    </div>
                </div>
                """)

        elif filename == "01_mcq.json":
            # Multiple Choice (Image 3 Ex B / MCQ)
            questions = ex_data.get("questions", [])
            for q in questions:
                qid = q.get("id", "")
                text = q.get("text", "")
                options = q.get("options", [])
                ans = q.get("correct_answer", "")
                exp = q.get("explanation", "")

                opt_labels = ["A", "B", "C", "D"]
                opts_html = []
                for i, opt in enumerate(options):
                    lbl = opt_labels[i] if i < len(opt_labels) else str(i+1)
                    is_correct = (opt.strip() == ans.strip())
                    opts_html.append(f"""
                    <label class="mcq-option-pill" data-val="{escape(opt)}" data-correct="{str(is_correct).lower()}">
                        <input type="radio" name="mcq_{ex_id}_{qid}" value="{escape(opt)}">
                        <span class="opt-label">{lbl}</span>
                        <span class="opt-text">{escape(opt)}</span>
                    </label>
                    """)

                html_parts.append(f"""
                <div class="q-row-item mcq-item" data-qid="{qid}">
                    <div class="mcq-header-text">
                        <span class="q-number">{qid}</span>
                        <div class="q-content-text">{escape(text)}</div>
                    </div>
                    <div class="mcq-options-grid">
                        {''.join(opts_html)}
                    </div>
                    <div class="q-feedback-slot"></div>
                    <div class="q-explanation-slot" style="display:none;">
                        <span class="exp-label">💡 Giải thích:</span> {escape(exp)} (Đáp án đúng: <strong>{escape(ans)}</strong>)
                    </div>
                </div>
                """)

        elif filename == "03_matching.json":
            # Matching Halves (1-10 to A-J)
            pairs = ex_data.get("pairs", [])
            options = ex_data.get("options", [])
            correct_matches = ex_data.get("correct_matches", {})

            html_parts.append('<div class="matching-container">')
            html_parts.append('<div class="matching-columns-wrap">')

            # Left column (Beginnings)
            html_parts.append('<div class="matching-left-col">')
            for p in pairs:
                pid = p.get("id", "")
                first_half = p.get("first_half", "")
                correct_lbl = correct_matches.get(str(pid), p.get("second_half_label", ""))

                # Build select dropdown for A-J
                opts_sel = ['<option value="">-- Chọn --</option>']
                for opt in options:
                    lbl = opt.get("label", "")
                    opts_sel.append(f'<option value="{lbl}">{lbl}</option>')

                html_parts.append(f"""
                <div class="matching-left-item" data-pid="{pid}">
                    <span class="q-number">{pid}</span>
                    <span class="match-text">{escape(first_half)}</span>
                    <select class="match-select" data-correct="{correct_lbl}">
                        {''.join(opts_sel)}
                    </select>
                    <span class="match-feedback"></span>
                </div>
                """)
            html_parts.append('</div>')

            # Right column (Endings A-J)
            html_parts.append('<div class="matching-right-col">')
            for opt in options:
                lbl = opt.get("label", "")
                half_b = opt.get("half_b", "")
                html_parts.append(f"""
                <div class="matching-right-item">
                    <span class="opt-label">{lbl}</span>
                    <span class="match-text">{escape(half_b)}</span>
                </div>
                """)
            html_parts.append('</div>')

            html_parts.append('</div></div>')

        elif filename == "04_rewrite.json":
            # Sentence Transformation
            questions = ex_data.get("questions", [])
            for q in questions:
                qid = q.get("id", "")
                orig = q.get("original_sentence", "")
                cue = q.get("cue", "")
                ans = q.get("correct_answer", "")
                exp = q.get("explanation", "")

                html_parts.append(f"""
                <div class="q-row-item rewrite-item" data-qid="{qid}">
                    <div class="rewrite-prompt-row">
                        <span class="q-number">{qid}</span>
                        <div class="orig-sentence">{escape(orig)}</div>
                    </div>
                    <div class="cue-badge-row">
                        <span class="cue-tag">Gợi ý / Cue:</span> <strong>{escape(cue)}</strong>
                    </div>
                    <div class="rewrite-input-wrap">
                        <span class="arrow-indicator">&rarr;</span>
                        <input type="text" class="dotted-text-input full-width" data-ans="{escape(ans)}" placeholder="Viết lại câu hoàn chỉnh ở đây..." autocomplete="off">
                    </div>
                    <div class="q-feedback-slot"></div>
                    <div class="q-explanation-slot" style="display:none;">
                        <span class="exp-label">💡 Đáp án chuẩn:</span> <strong>{escape(ans)}</strong><br>
                        <span class="exp-note">{escape(exp)}</span>
                    </div>
                </div>
                """)

        elif filename == "05_guided_cloze.json":
            # Guided Cloze Passages
            passages = ex_data.get("passages", [])
            for pass_idx, p in enumerate(passages):
                p_title = p.get("title", f"Passage {pass_idx + 1}")
                p_content = p.get("content", "")
                p_questions = p.get("questions", [])

                html_parts.append(f"""
                <div class="cloze-passage-block">
                    <h4 class="cloze-passage-title">📖 {escape(p_title)}</h4>
                    <div class="cloze-text-box">
                        {p_content}
                    </div>
                    <div class="cloze-questions-grid">
                """)

                for q in p_questions:
                    qid = q.get("id", "")
                    blank_num = q.get("blank_number", qid)
                    q_opts = q.get("options", [])
                    ans = q.get("correct_answer", "")

                    opt_labels = ["A", "B", "C", "D"]
                    cloze_opts_html = []
                    for i, opt in enumerate(q_opts):
                        lbl = opt_labels[i] if i < len(opt_labels) else str(i+1)
                        is_correct = (opt.strip() == ans.strip())
                        cloze_opts_html.append(f"""
                        <label class="cloze-opt-btn" data-val="{escape(opt)}" data-correct="{str(is_correct).lower()}">
                            <input type="radio" name="cloze_{ex_id}_{blank_num}" value="{escape(opt)}">
                            <span class="opt-label">{lbl}</span> {escape(opt)}
                        </label>
                        """)

                    html_parts.append(f"""
                    <div class="cloze-q-cell" data-qid="{blank_num}">
                        <div class="cloze-q-num">[{blank_num}]</div>
                        <div class="cloze-opts-row">
                            {''.join(cloze_opts_html)}
                        </div>
                        <div class="cloze-feedback-slot"></div>
                    </div>
                    """)

                html_parts.append("</div></div>")

        elif filename == "06_error_identification.json":
            # Error Identification & Correction
            questions = ex_data.get("questions", [])
            for q in questions:
                qid = q.get("id", "")
                text = q.get("text", "")
                correct_opt = q.get("correct_answer", "")
                err_segment = q.get("error_segment", "")
                correction = q.get("correction", "")
                exp = q.get("explanation", "")

                formatted_text = text
                for opt in ["A", "B", "C", "D"]:
                    pattern = rf"\[{opt}:\s*([^\]]+)\]"
                    repl = rf'<span class="error-bracket-tag" data-opt="{opt}"><u>[{opt}] \1</u></span>'
                    formatted_text = re.sub(pattern, repl, formatted_text)

                html_parts.append(f"""
                <div class="q-row-item error-id-item" data-qid="{qid}" data-correct-opt="{escape(correct_opt)}" data-correction="{escape(correction)}">
                    <div class="error-text-row">
                        <span class="q-number">{qid}</span>
                        <div class="q-content-text">{formatted_text}</div>
                    </div>
                    <div class="error-action-row">
                        <div class="error-opt-selector">
                            <span class="selector-lbl">Lỗi sai:</span>
                            <button type="button" class="btn-err-opt" onclick="selectErrorOpt(this, 'A')">A</button>
                            <button type="button" class="btn-err-opt" onclick="selectErrorOpt(this, 'B')">B</button>
                            <button type="button" class="btn-err-opt" onclick="selectErrorOpt(this, 'C')">C</button>
                            <button type="button" class="btn-err-opt" onclick="selectErrorOpt(this, 'D')">D</button>
                        </div>
                        <div class="error-correction-input">
                            <span class="selector-lbl">Sửa lại thành:</span>
                            <input type="text" class="dotted-text-input err-corr-input" placeholder="Từ / cụm từ đúng..." autocomplete="off">
                        </div>
                    </div>
                    <div class="q-feedback-slot"></div>
                    <div class="q-explanation-slot" style="display:none;">
                        <span class="exp-label">💡 Đáp án:</span> Vị trí <strong>[{escape(correct_opt)}]</strong> (Sửa <em>{escape(err_segment)}</em> &rarr; <strong>{escape(correction)}</strong>)<br>
                        <span class="exp-note">{escape(exp)}</span>
                    </div>
                </div>
                """)

        elif filename == "07_sentence_combination.json":
            # Sentence Combination
            questions = ex_data.get("questions", [])
            for q in questions:
                qid = q.get("id", "")
                s1 = q.get("sentence_1", "")
                s2 = q.get("sentence_2", "")
                cue = q.get("cue", "")
                ans = q.get("correct_answer", "")
                exp = q.get("explanation", "")

                html_parts.append(f"""
                <div class="q-row-item combination-item" data-qid="{qid}">
                    <div class="combo-sentences-box">
                        <span class="q-number">{qid}</span>
                        <div class="combo-sentences-text">
                            <div>• {escape(s1)}</div>
                            <div>• {escape(s2)}</div>
                        </div>
                    </div>
                    <div class="cue-badge-row">
                        <span class="cue-tag">Liên từ gợi ý:</span> <strong>{escape(cue)}</strong>
                    </div>
                    <div class="rewrite-input-wrap">
                        <span class="arrow-indicator">&rarr;</span>
                        <input type="text" class="dotted-text-input full-width" data-ans="{escape(ans)}" placeholder="Viết câu kết hợp hoàn chỉnh ở đây..." autocomplete="off">
                    </div>
                    <div class="q-feedback-slot"></div>
                    <div class="q-explanation-slot" style="display:none;">
                        <span class="exp-label">💡 Câu kết hợp mẫu:</span> <strong>{escape(ans)}</strong><br>
                        <span class="exp-note">{escape(exp)}</span>
                    </div>
                </div>
                """)

        elif filename == "08_sentence_building.json":
            # Sentence Building from Cues
            questions = ex_data.get("questions", [])
            for q in questions:
                qid = q.get("id", "")
                cues = q.get("cues", "")
                ans = q.get("correct_answer", "")
                exp = q.get("explanation", "")

                html_parts.append(f"""
                <div class="q-row-item building-item" data-qid="{qid}">
                    <div class="building-cues-row">
                        <span class="q-number">{qid}</span>
                        <div class="cue-chain">🔤 {escape(cues)}</div>
                    </div>
                    <div class="rewrite-input-wrap">
                        <span class="arrow-indicator">&rarr;</span>
                        <input type="text" class="dotted-text-input full-width" data-ans="{escape(ans)}" placeholder="Xây dựng câu hoàn chỉnh ở đây..." autocomplete="off">
                    </div>
                    <div class="q-feedback-slot"></div>
                    <div class="q-explanation-slot" style="display:none;">
                        <span class="exp-label">💡 Câu hoàn chỉnh mẫu:</span> <strong>{escape(ans)}</strong><br>
                        <span class="exp-note">{escape(exp)}</span>
                    </div>
                </div>
                """)

        # Exercise Action Footer
        html_parts.append(f"""
            </div>
            <div class="exercise-footer-actions">
                <button type="button" class="btn-check-ex" onclick="checkGrammarExercise('{ex_id}')">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                    Kiểm Tra Bài {letter}
                </button>
                <button type="button" class="btn-toggle-exp" onclick="toggleExplanations('{ex_id}')">
                    💡 Xem Giải Thích
                </button>
                <div class="exercise-score-badge" id="score_{ex_id}"></div>
            </div>
        </div>
        """)

    html_parts.append("</div>")
    return "\n".join(html_parts)


def get_grammar_css():
    """Returns CSS rules matching the exact textbook images and portal system."""
    return """
        /* === GRAMMAR LESSON STYLES (MATCHING IMAGES 1, 2, 3) === */
        .grammar-doc-container, .grammar-exercises-doc {
            background: #ffffff;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            padding: 28px 36px;
            margin-bottom: 30px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        }

        .lesson-top-bar {
            height: 4px;
            background: #1e40af;
            border-radius: 2px;
            width: 100%;
            margin-bottom: 20px;
        }

        .lesson-header-title {
            text-align: center;
            margin-bottom: 24px;
        }

        .lesson-header-title h2 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: #1e3a8a;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin: 0;
        }

        .grammar-pill {
            display: inline-block;
            background: #e0f2fe;
            border: 1.5px solid #38bdf8;
            color: #0369a1;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14.5px;
            font-weight: 700;
            padding: 6px 20px;
            border-radius: 9999px;
            margin: 18px 0 12px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }

        .grammar-intro-list {
            list-style-type: disc;
            margin: 0 0 16px 24px;
            padding: 0;
            color: #334155;
            font-size: 14.5px;
            line-height: 1.65;
        }

        .grammar-intro-list li {
            margin-bottom: 6px;
        }

        .grammar-table-wrapper {
            overflow-x: auto;
            margin-bottom: 20px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
        }

        .grammar-styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            text-align: left;
            background: #ffffff;
        }

        .grammar-styled-table th {
            background: #1e3a8a;
            color: #ffffff;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            font-size: 13.5px;
            padding: 11px 16px;
            letter-spacing: 0.3px;
        }

        .grammar-styled-table td {
            padding: 10px 16px;
            border-bottom: 1px solid #e2e8f0;
            color: #1e293b;
            vertical-align: top;
            line-height: 1.5;
        }

        .grammar-styled-table tbody tr:nth-child(even) td {
            background: #f8fafc;
        }

        .grammar-styled-table tbody tr:hover td {
            background: #eff6ff;
        }

        .grammar-hl {
            color: #1d4ed8;
            font-weight: 700;
        }

        /* ⚠ WATCH OUT! Amber Box */
        .watch-out-box {
            background: #fffbeb;
            border: 1px solid #fde047;
            border-left: 5px solid #f59e0b;
            border-radius: 10px;
            padding: 16px 20px;
            margin: 20px 0 24px 0;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.05);
        }

        .watch-out-header {
            color: #b45309;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            font-weight: 800;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 8px;
        }

        .watch-out-icon {
            font-size: 16px;
        }

        .watch-out-list {
            list-style: disc;
            margin: 0 0 0 20px;
            padding: 0;
            color: #78350f;
            font-size: 13.5px;
            line-height: 1.6;
        }

        .watch-out-list li {
            margin-bottom: 6px;
        }

        /* === GRAMMAR EXERCISE CARDS (IMAGE 3) === */
        .grammar-exercise-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            transition: all 0.2s;
        }

        .grammar-exercise-card:hover {
            box-shadow: 0 6px 16px rgba(30, 58, 138, 0.06);
        }

        .exercise-header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 6px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .exercise-title-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .exercise-letter-badge {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: #1e40af;
            background: #eff6ff;
            border: 1.5px solid #bfdbfe;
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .exercise-main-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: #0f172a;
        }

        .exercise-badge-type {
            font-size: 12px;
            font-weight: 600;
            color: #475569;
            background: #f1f5f9;
            padding: 4px 10px;
            border-radius: 9999px;
            border: 1px solid #e2e8f0;
        }

        .exercise-subinstruction {
            font-size: 13.5px;
            font-style: italic;
            color: #475569;
            margin-bottom: 20px;
            padding-left: 44px;
        }

        /* Question Item Rows */
        .q-row-item {
            padding: 12px 14px;
            border-bottom: 1px dashed #e2e8f0;
            display: flex;
            flex-direction: column;
            gap: 8px;
            transition: background 0.15s;
            border-radius: 8px;
        }

        .q-row-item:hover {
            background: #f8fafc;
        }

        .q-row-item:last-child {
            border-bottom: none;
        }

        .q-number {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #1e3a8a;
            min-width: 24px;
            display: inline-block;
        }

        .q-content-text {
            font-size: 14.5px;
            color: #1e293b;
            line-height: 1.6;
            flex: 1;
        }

        /* Dotted Underline Handwriting Inputs */
        .dotted-text-input {
            border: none;
            border-bottom: 2px dotted #1e40af;
            background: transparent;
            padding: 3px 10px;
            font-family: inherit;
            font-size: 14.5px;
            font-weight: 600;
            color: #1e40af;
            outline: none;
            min-width: 140px;
            text-align: center;
            transition: all 0.2s;
        }

        .dotted-text-input:focus {
            border-bottom-style: solid;
            background: #eff6ff;
            border-radius: 4px 4px 0 0;
        }

        .dotted-text-input.full-width {
            width: 100%;
            text-align: left;
            min-width: unset;
        }

        .dotted-text-input.is-correct {
            border-bottom: 2px solid #10b981;
            color: #065f46;
            background: #ecfdf5;
        }

        .dotted-text-input.is-wrong {
            border-bottom: 2px solid #ef4444;
            color: #991b1b;
            background: #fef2f2;
        }

        /* MCQ Options Grid */
        .mcq-header-text {
            display: flex;
            align-items: baseline;
            gap: 8px;
        }

        .mcq-options-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 8px;
            margin-top: 6px;
            padding-left: 28px;
        }

        .mcq-option-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            cursor: pointer;
            font-size: 13.5px;
            transition: all 0.15s;
        }

        .mcq-option-pill:hover {
            background: #eff6ff;
            border-color: #93c5fd;
        }

        .mcq-option-pill input {
            cursor: pointer;
        }

        .mcq-option-pill .opt-label {
            font-weight: 700;
            color: #1e40af;
        }

        .mcq-option-pill.selected-correct {
            background: #ecfdf5;
            border-color: #10b981;
            color: #065f46;
            font-weight: 600;
        }

        .mcq-option-pill.selected-wrong {
            background: #fef2f2;
            border-color: #ef4444;
            color: #991b1b;
        }

        /* Matching */
        .matching-columns-wrap {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        @media (max-width: 860px) {
            .matching-columns-wrap {
                grid-template-columns: 1fr;
            }
        }

        .matching-left-item, .matching-right-item {
            padding: 10px 14px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: #ffffff;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13.5px;
        }

        .match-select {
            padding: 5px 8px;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            font-weight: 700;
            color: #1e40af;
            outline: none;
            background: #eff6ff;
            margin-left: auto;
        }

        /* Sentence Rewrite & Cues */
        .rewrite-prompt-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
        }

        .orig-sentence {
            font-size: 14.5px;
            font-weight: 500;
            color: #1e293b;
        }

        .cue-badge-row {
            padding-left: 28px;
            font-size: 13px;
            color: #475569;
        }

        .cue-tag {
            background: #eff6ff;
            color: #1d4ed8;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
        }

        .rewrite-input-wrap {
            display: flex;
            align-items: center;
            gap: 8px;
            padding-left: 28px;
        }

        .arrow-indicator {
            font-weight: 800;
            color: #1e40af;
            font-size: 16px;
        }

        /* Cloze */
        .cloze-passage-block {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 20px;
        }

        .cloze-passage-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 10px;
        }

        .cloze-text-box {
            font-size: 14.5px;
            line-height: 1.7;
            color: #334155;
            margin-bottom: 16px;
        }

        .cloze-questions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 12px;
        }

        .cloze-q-cell {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px 12px;
        }

        .cloze-q-num {
            font-weight: 700;
            color: #1e40af;
            font-size: 13px;
            margin-bottom: 4px;
        }

        .cloze-opts-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .cloze-opt-btn {
            font-size: 12.5px;
            padding: 4px 8px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            background: #f8fafc;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        /* Error ID */
        .error-bracket-tag {
            background: #fef3c7;
            color: #92400e;
            padding: 1px 4px;
            border-radius: 4px;
            font-weight: 600;
        }

        .error-action-row {
            display: flex;
            align-items: center;
            gap: 16px;
            padding-left: 28px;
            flex-wrap: wrap;
        }

        .error-opt-selector {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .btn-err-opt {
            width: 28px;
            height: 28px;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            background: #ffffff;
            font-weight: 700;
            color: #1e40af;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-err-opt:hover, .btn-err-opt.selected {
            background: #1e40af;
            color: #ffffff;
            border-color: #1e40af;
        }

        .err-corr-input {
            width: 200px;
        }

        /* Explanation & Feedback Slots */
        .q-feedback-slot {
            font-size: 13px;
            font-weight: 600;
            padding-left: 28px;
        }

        .q-explanation-slot {
            background: #f0fdf4;
            border-left: 3px solid #10b981;
            padding: 8px 14px;
            font-size: 13px;
            color: #065f46;
            border-radius: 0 6px 6px 0;
            margin-left: 28px;
            line-height: 1.5;
        }

        .exp-label {
            font-weight: 700;
            color: #047857;
        }

        /* Exercise Footer Actions */
        .exercise-footer-actions {
            margin-top: 18px;
            padding-top: 14px;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .btn-check-ex {
            background: #1e40af;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .btn-check-ex:hover {
            background: #1d4ed8;
            box-shadow: 0 4px 10px rgba(30, 64, 175, 0.2);
        }

        .btn-toggle-exp {
            background: #ffffff;
            color: #475569;
            border: 1px solid #cbd5e1;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn-toggle-exp:hover {
            background: #f1f5f9;
            color: #0f172a;
        }

        .exercise-score-badge {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            margin-left: auto;
        }
    """


def get_grammar_js():
    """Returns raw JavaScript for grammar interaction engine."""
    return r"""
    <script>
    function checkGrammarExercise(cardId) {
        const card = document.getElementById(cardId);
        if (!card) return;

        let total = 0;
        let correct = 0;

        // 1. Dotted text inputs
        const textInputs = card.querySelectorAll('input.dotted-text-input:not(.err-corr-input)');
        textInputs.forEach(input => {
            total++;
            const expected = (input.dataset.ans || '').trim().toLowerCase();
            const userVal = (input.value || '').trim().toLowerCase();
            const row = input.closest('.q-row-item');
            const slot = row ? row.querySelector('.q-feedback-slot') : null;

            if (userVal && (userVal === expected || isGrammarMatch(userVal, expected))) {
                correct++;
                input.classList.remove('is-wrong');
                input.classList.add('is-correct');
                if (slot) slot.innerHTML = '<span style="color:#10b981;">✓ Đúng</span>';
            } else {
                input.classList.remove('is-correct');
                input.classList.add('is-wrong');
                if (slot) slot.innerHTML = `<span style="color:#ef4444;">✗ Sai. Đáp án: <strong>${input.dataset.ans}</strong></span>`;
            }
        });

        // 2. MCQ
        const mcqItems = card.querySelectorAll('.mcq-item');
        mcqItems.forEach(item => {
            total++;
            const checkedRadio = item.querySelector('input[type="radio"]:checked');
            const slot = item.querySelector('.q-feedback-slot');
            const pills = item.querySelectorAll('.mcq-option-pill');

            pills.forEach(p => p.classList.remove('selected-correct', 'selected-wrong'));

            if (checkedRadio) {
                const parentPill = checkedRadio.closest('.mcq-option-pill');
                const isCorr = parentPill.dataset.correct === 'true';
                if (isCorr) {
                    correct++;
                    parentPill.classList.add('selected-correct');
                    if (slot) slot.innerHTML = '<span style="color:#10b981;">✓ Chính xác!</span>';
                } else {
                    parentPill.classList.add('selected-wrong');
                    const correctPill = item.querySelector('.mcq-option-pill[data-correct="true"]');
                    if (correctPill) correctPill.classList.add('selected-correct');
                    if (slot) slot.innerHTML = '<span style="color:#ef4444;">✗ Sai rồi.</span>';
                }
            } else {
                if (slot) slot.innerHTML = '<span style="color:#f59e0b;">Chưa chọn đáp án</span>';
            }
        });

        // 3. Matching
        const matchLeftItems = card.querySelectorAll('.matching-left-item');
        matchLeftItems.forEach(item => {
            total++;
            const sel = item.querySelector('.match-select');
            const expected = (sel.dataset.correct || '').trim().toUpperCase();
            const userVal = (sel.value || '').trim().toUpperCase();
            const slot = item.querySelector('.match-feedback');

            if (userVal === expected) {
                correct++;
                sel.style.borderColor = '#10b981';
                sel.style.background = '#ecfdf5';
                if (slot) slot.innerHTML = '<span style="color:#10b981;">✓</span>';
            } else {
                sel.style.borderColor = '#ef4444';
                sel.style.background = '#fef2f2';
                if (slot) slot.innerHTML = `<span style="color:#ef4444;">✗ (${expected})</span>`;
            }
        });

        // 4. Cloze
        const clozeCells = card.querySelectorAll('.cloze-q-cell');
        clozeCells.forEach(cell => {
            total++;
            const checkedRadio = cell.querySelector('input[type="radio"]:checked');
            const slot = cell.querySelector('.cloze-feedback-slot');
            const btns = cell.querySelectorAll('.cloze-opt-btn');

            btns.forEach(b => {
                b.style.borderColor = '#e2e8f0';
                b.style.background = '#f8fafc';
            });

            if (checkedRadio) {
                const parentBtn = checkedRadio.closest('.cloze-opt-btn');
                const isCorr = parentBtn.dataset.correct === 'true';
                if (isCorr) {
                    correct++;
                    parentBtn.style.borderColor = '#10b981';
                    parentBtn.style.background = '#ecfdf5';
                    if (slot) slot.innerHTML = '<span style="color:#10b981; font-size:11px;">✓ Đúng</span>';
                } else {
                    parentBtn.style.borderColor = '#ef4444';
                    parentBtn.style.background = '#fef2f2';
                    const correctBtn = cell.querySelector('.cloze-opt-btn[data-correct="true"]');
                    if (correctBtn) {
                        correctBtn.style.borderColor = '#10b981';
                        correctBtn.style.background = '#ecfdf5';
                    }
                    if (slot) slot.innerHTML = '<span style="color:#ef4444; font-size:11px;">✗ Sai</span>';
                }
            } else {
                if (slot) slot.innerHTML = '<span style="color:#f59e0b; font-size:11px;">Chưa làm</span>';
            }
        });

        // 5. Error ID
        const errorItems = card.querySelectorAll('.error-id-item');
        errorItems.forEach(item => {
            total++;
            const expectedOpt = (item.dataset.correctOpt || '').trim().toUpperCase();
            const selectedBtn = item.querySelector('.btn-err-opt.selected');
            const corrInput = item.querySelector('.err-corr-input');
            const userOpt = selectedBtn ? selectedBtn.textContent.trim().toUpperCase() : '';
            const userCorr = corrInput ? corrInput.value.trim().toLowerCase() : '';
            const slot = item.querySelector('.q-feedback-slot');

            let optOk = (userOpt === expectedOpt);
            let corrOk = (userCorr && isGrammarMatch(userCorr, item.dataset.correction || ''));

            if (optOk && corrOk) {
                correct++;
                if (corrInput) corrInput.classList.add('is-correct');
                if (slot) slot.innerHTML = '<span style="color:#10b981;">✓ Chính xác hoàn toàn!</span>';
            } else if (optOk) {
                correct += 0.5;
                if (corrInput) corrInput.classList.add('is-wrong');
                if (slot) slot.innerHTML = `<span style="color:#d97706;">✓ Đúng lỗi [${expectedOpt}], cần sửa thành: <strong>${item.dataset.correction}</strong></span>`;
            } else {
                if (corrInput) corrInput.classList.add('is-wrong');
                if (slot) slot.innerHTML = `<span style="color:#ef4444;">✗ Sai. Lỗi ở [${expectedOpt}], sửa thành: <strong>${item.dataset.correction}</strong></span>`;
            }
        });

        const scoreBadge = document.getElementById('score_' + cardId);
        if (scoreBadge && total > 0) {
            const pct = Math.round((correct / total) * 100);
            const color = pct >= 80 ? '#10b981' : (pct >= 50 ? '#d97706' : '#ef4444');
            scoreBadge.innerHTML = `<span style="color:${color}; background:#f1f5f9; padding:4px 10px; border-radius:6px;">Điểm: ${correct}/${total} (${pct}%)</span>`;
        }
    }

    function isGrammarMatch(inputVal, targetVal) {
        if (!inputVal || !targetVal) return false;
        const clean = str => str.toLowerCase().replace(/['".,/#!$%^&*;:{}=\-_`~()]/g, "").replace(/\s+/g, " ").trim();
        return clean(inputVal) === clean(targetVal);
    }

    function toggleExplanations(cardId) {
        const card = document.getElementById(cardId);
        if (!card) return;
        const expSlots = card.querySelectorAll('.q-explanation-slot');
        expSlots.forEach(slot => {
            slot.style.display = (slot.style.display === 'none' || slot.style.display === '') ? 'block' : 'none';
        });
    }

    function selectErrorOpt(btn, optLetter) {
        const container = btn.closest('.error-opt-selector');
        container.querySelectorAll('.btn-err-opt').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
    }
    </script>
    """


def get_portal_js(units_stats_json):
    """Returns the JS controllers for the portal layout and navigation."""
    js_template = r"""
    <script>
    let currentUnit = 1;
    const unitsStats = __UNITS_STATS__;

    function switchUnit(unitNum) {
        currentUnit = unitNum;
        document.querySelectorAll('.unit-nav-btn').forEach(btn => {
            btn.classList.toggle('active', parseInt(btn.dataset.unit) === unitNum);
        });

        document.querySelectorAll('.unit-content-section').forEach(sec => {
            sec.style.display = (sec.id === 'unit-section-' + unitNum) ? 'block' : 'none';
        });

        document.getElementById('sidebar-unit-num').textContent = unitNum;
        const st = unitsStats[unitNum];
        if (st) {
            document.getElementById('stat-vocab-words').textContent = st.v_words;
            document.getElementById('stat-vocab-ex').textContent = st.v_ex;
            document.getElementById('stat-grammar-ex').textContent = st.g_ex;
            document.getElementById('stat-grammar-q').textContent = st.g_q;
        }
    }

    function switchMainTab(tab) {
        document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));
        if (tab === 'all') document.getElementById('tabAll').classList.add('active');
        if (tab === 'theory') document.getElementById('tabTheory').classList.add('active');
        if (tab === 'exercises') document.getElementById('tabExercises').classList.add('active');
        if (tab === 'grammar') document.getElementById('tabGrammar').classList.add('active');

        const activeSec = document.getElementById('unit-section-' + currentUnit);
        if (!activeSec) return;

        const secTheory = activeSec.querySelector('.tab-content-theory');
        const secEx = activeSec.querySelector('.tab-content-exercises');
        const secGrammar = activeSec.querySelector('.tab-content-grammar');

        if (tab === 'all') {
            if (secTheory) secTheory.style.display = 'block';
            if (secEx) secEx.style.display = 'block';
            if (secGrammar) secGrammar.style.display = 'block';
        } else if (tab === 'theory') {
            if (secTheory) secTheory.style.display = 'block';
            if (secEx) secEx.style.display = 'none';
            if (secGrammar) secGrammar.style.display = 'none';
        } else if (tab === 'exercises') {
            if (secTheory) secTheory.style.display = 'none';
            if (secEx) secEx.style.display = 'block';
            if (secGrammar) secGrammar.style.display = 'none';
        } else if (tab === 'grammar') {
            if (secTheory) secTheory.style.display = 'none';
            if (secEx) secEx.style.display = 'none';
            if (secGrammar) secGrammar.style.display = 'block';
        }
    }

    function setPortalMode(mode) {
        document.body.classList.toggle('mode-review', mode === 'review');
        document.body.classList.toggle('mode-practice', mode === 'practice');
        document.getElementById('btnModeReview').classList.toggle('active', mode === 'review');
        document.getElementById('btnModePractice').classList.toggle('active', mode === 'practice');

        document.querySelectorAll('.q-explanation-slot').forEach(slot => {
            slot.style.display = (mode === 'review') ? 'block' : 'none';
        });

        if (mode === 'review') {
            document.querySelectorAll('input.dotted-text-input:not(.err-corr-input)').forEach(inp => {
                if (inp.dataset.ans) inp.value = inp.dataset.ans;
                inp.classList.add('is-correct');
            });
            document.querySelectorAll('.mcq-option-pill[data-correct="true"]').forEach(p => p.classList.add('selected-correct'));
        }
    }

    function scrollToTarget(prefix) {
        const target = document.getElementById(prefix + '-u' + currentUnit) || document.getElementById(prefix);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function speakWord(word) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance(word);
            utter.lang = 'en-US';
            utter.rate = 0.9;
            window.speechSynthesis.speak(utter);
        }
    }

    function handleGlobalSearch(query) {
        const q = query.toLowerCase().trim();
        const activeSec = document.getElementById('unit-section-' + currentUnit);
        if (!activeSec) return;

        activeSec.querySelectorAll('.vocab-card-item').forEach(card => {
            const txt = card.textContent.toLowerCase();
            card.style.display = (!q || txt.includes(q)) ? 'flex' : 'none';
        });

        activeSec.querySelectorAll('.q-row-item').forEach(row => {
            const txt = row.textContent.toLowerCase();
            row.style.display = (!q || txt.includes(q)) ? 'flex' : 'none';
        });
    }
    </script>
    """
    return js_template.replace("__UNITS_STATS__", units_stats_json)


def generate_master_index(workspace_root, available_units, theory_db, output_file):
    """
    Builds the unified index.html incorporating:
    - Unit Switcher dropdown / pills (Unit 1, Unit 2, Unit 3)
    - Navigation Tabs: [Tất Cả], [Lý Thuyết Từ Vựng], [Bài Tập Từ Vựng], [Ngữ Pháp: Lý Thuyết & 8 Dạng Bài]
    - Full Vocabulary theory & exercises for each unit
    - Full Grammar theory & exercises for each unit
    - Live Search, Review/Practice modes, In PDF styles.
    """
    print(f"Compiling Master index.html to {output_file}...")

    # Load data for each unit
    units_data = {}
    for u in available_units:
        u_folder = workspace_root / "lessons" / f"unit-{u}"
        v_file = u_folder / "vocab" / "vocab.json"
        v_ex_dir = u_folder / "vocab" / "exercises"
        g_ex_dir = u_folder / "grammar" / "exercises"

        v_data = load_json(v_file) or []
        v_exs = {}
        for f in sorted(glob.glob(str(v_ex_dir / "*.json"))):
            v_exs[os.path.basename(f)] = load_json(f)

        g_exs = {}
        for f in sorted(glob.glob(str(g_ex_dir / "*.json"))):
            g_exs[os.path.basename(f)] = load_json(f)

        g_theory = theory_db.get(str(u), {})

        # Count questions
        g_q_count = sum(len(d.get("questions", [])) for d in g_exs.values() if "questions" in d)
        for d in g_exs.values():
            if "passages" in d:
                for p in d["passages"]:
                    g_q_count += len(p.get("questions", []))

        v_words_count = sum(len(grp.get("words", [])) for grp in v_data)
        v_q_count = sum(len(d.get("questions", [])) for d in v_exs.values() if "questions" in d)

        units_data[u] = {
            "vocab": v_data,
            "vocab_ex": v_exs,
            "grammar_theory": g_theory,
            "grammar_ex": g_exs,
            "v_words_count": v_words_count,
            "v_q_count": v_q_count,
            "g_q_count": g_q_count,
            "theme": g_theory.get("unit_theme", f"Unit {u}"),
            "grammar_topic": g_theory.get("grammar_topic", "Target Grammar")
        }

    # Render Unit Containers HTML
    units_containers_html = []
    unit_tabs_nav = []

    for idx, u in enumerate(available_units):
        u_info = units_data[u]
        active_cls = "active" if idx == 0 else ""
        display_style = "block" if idx == 0 else "none"

        unit_tabs_nav.append(f"""
        <button type="button" class="unit-nav-btn {active_cls}" data-unit="{u}" onclick="switchUnit({u})">
            Unit {u}: {escape(u_info['theme'])}
        </button>
        """)

        # Vocab Theory HTML
        v_theory_html = []
        for grp in u_info["vocab"]:
            grp_name = grp.get("group", "")
            v_theory_html.append(f'<div class="vocab-group-header"><h3>📁 {escape(grp_name)}</h3></div>')
            v_theory_html.append('<div class="vocab-cards-grid">')
            for w in grp.get("words", []):
                eng = w.get("english_word", "")
                ipa = w.get("phonetics", {}).get("uk", "") or w.get("phonetics", {}).get("us", "")
                pos = w.get("part_of_speech", "")
                defn = w.get("vietnamese_meaning", "")
                ex_en = w.get("example_sentence", {}).get("english", "")
                img = w.get("image_url", "")
                if img.startswith("/"):
                    img = img.lstrip("/")

                v_theory_html.append(f"""
                <div class="vocab-card-item">
                    <div class="card-img-wrap">
                        <img src="{escape(img)}" alt="{escape(eng)}" loading="lazy" onerror="this.src='images/placeholder.webp'">
                        <button type="button" class="btn-audio-speak" onclick="speakWord('{escape(eng)}')" title="Phát âm">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
                        </button>
                    </div>
                    <div class="card-body">
                        <div class="card-word-title">{escape(eng)}</div>
                        <div class="card-ipa-line">/{escape(ipa)}/ <span class="card-pos">({escape(pos)})</span></div>
                        <div class="card-divider"></div>
                        <div class="card-def-vi">{escape(defn)}</div>
                        {f'<div class="card-ex-en">"{escape(ex_en)}"</div>' if ex_en else ''}
                    </div>
                </div>
                """)
            v_theory_html.append('</div>')

        # Grammar Theory HTML
        g_theory_html = render_grammar_theory_html(u, u_info["grammar_theory"])

        # Grammar Exercises HTML
        g_exercises_html = render_grammar_exercises_html(u, u_info["grammar_ex"], u_info["grammar_theory"])

        # Assemble Unit Container
        units_containers_html.append(f"""
        <div class="unit-content-section" id="unit-section-{u}" style="display: {display_style};">
            
            <!-- SECTION 1: LÝ THUYẾT TỪ VỰNG -->
            <section class="section-box tab-content-theory" id="section-vocab-theory-u{u}">
                <div class="section-headline">
                    <div class="headline-left">
                        <div class="headline-icon-box">💡</div>
                        <div class="headline-text">
                            <h2>Unit {u}: Lý Thuyết Từ Vựng Trọng Tâm</h2>
                            <p>{u_info['v_words_count']} từ vựng cốt lõi &bull; Phát âm giọng chuẩn &bull; Nghĩa tiếng Việt và ngữ cảnh mẫu</p>
                        </div>
                    </div>
                </div>
                <div class="theory-body">
                    {''.join(v_theory_html)}
                </div>
            </section>

            <!-- SECTION 2: BÀI TẬP TỪ VỰNG (16 DẠNG) -->
            <section class="section-box tab-content-exercises" id="section-vocab-exercises-u{u}">
                <div class="section-headline">
                    <div class="headline-left">
                        <div class="headline-icon-box">✍️</div>
                        <div class="headline-text">
                            <h2>Unit {u}: Bài Tập Thực Hành Từ Vựng (16 Dạng)</h2>
                            <p>{len(u_info['vocab_ex'])} dạng bài tập thực hành &bull; {u_info['v_q_count']} câu hỏi từ vựng toàn diện</p>
                        </div>
                    </div>
                    <a href="lessons/unit-{u}/vocab/index.html" class="nav-item" style="border:1px solid #bfdbfe; font-size:12px; font-weight:700;">
                        Xem Toàn Bộ 16 Dạng Bài Từ Vựng ↗
                    </a>
                </div>
                <div class="vocab-exercises-preview-note">
                    <p>💡 <em>Hệ thống 16 bài tập từ vựng chuẩn THPT Quốc Gia cho Unit {u} có thể được thực hành chi tiết tại cổng từ vựng chuyên biệt.</em></p>
                </div>
            </section>

            <!-- SECTION 3: NGỮ PHÁP (LÝ THUYẾT CHUẨN MẪU ẢNH + 8 DẠNG BÀI TẬP A-H) -->
            <section class="section-box tab-content-grammar" id="section-grammar-u{u}">
                <div class="section-headline">
                    <div class="headline-left">
                        <div class="headline-icon-box">📐</div>
                        <div class="headline-text">
                            <h2>Unit {u}: Ngữ Pháp – {escape(u_info['grammar_topic'])}</h2>
                            <p>Cấu trúc trình bày chuẩn sách giáo khoa (Pill Badges, Bảng xanh đậm, ⚠ WATCH OUT!) &bull; 8 dạng bài A–H ({u_info['g_q_count']} câu hỏi)</p>
                        </div>
                    </div>
                    <a href="lessons/unit-{u}/grammar_unit{u}.html" target="_blank" class="nav-item" style="border:1px solid #bfdbfe; font-size:12px; font-weight:700;">
                        Mở Trang Grammar Độc Lập ↗
                    </a>
                </div>

                <!-- 3A. LÝ THUYẾT NGỮ PHÁP -->
                <div class="grammar-theory-wrapper">
                    {g_theory_html}
                </div>

                <!-- 3B. BÀI TẬP THỰC HÀNH NGỮ PHÁP (A ĐẾN H) -->
                <div class="grammar-exercises-wrapper" style="margin-top: 30px;">
                    {g_exercises_html}
                </div>
            </section>
        </div>
        """)

    stats_dict = {u: {"v_words": units_data[u]["v_words_count"], "v_ex": len(units_data[u]["vocab_ex"]), "g_ex": len(units_data[u]["grammar_ex"]), "g_q": units_data[u]["g_q_count"]} for u in available_units}
    portal_js_code = get_portal_js(json.dumps(stats_dict))

    # Complete master index.html markup
    full_html = f"""<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GLOBAL SUCCESS 12 • Học Tập Toàn Diện: Từ Vựng & Ngữ Pháp</title>

    <!-- Google Fonts: Plus Jakarta Sans & Be Vietnam Pro -->
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
            --bg-page: #f8fafc;
            --text-main: #0f172a;
            --text-heading: #1e293b;
            --text-muted: #64748b;
            --border-subtle: #e2e8f0;
            --card-radius: 16px;
            --shadow-default: 0 4px 20px -2px rgba(37, 99, 235, 0.08), 0 2px 6px -1px rgba(0, 0, 0, 0.04);
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

        /* STICKY HEADER */
        header.portal-header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        }}

        .header-inner {{
            max-width: 1520px;
            margin: 0 auto;
            padding: 10px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            flex-wrap: wrap;
        }}

        .brand-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
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
        }}

        .brand-titles h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 800;
            color: var(--primary-navy);
        }}

        .brand-titles p {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* UNIT SELECTOR BAR */
        .unit-nav-wrap {{
            display: flex;
            background: #e2e8f0;
            padding: 3px;
            border-radius: 9999px;
            gap: 4px;
        }}

        .unit-nav-btn {{
            border: none;
            background: transparent;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 700;
            padding: 6px 16px;
            border-radius: 9999px;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .unit-nav-btn.active {{
            background: #ffffff;
            color: var(--primary-navy);
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }}

        /* NAVIGATION TABS (ALL / VOCAB / EXERCISES / GRAMMAR) */
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
        }}

        .nav-tab-btn.active {{
            background: #ffffff;
            color: var(--primary-blue);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            font-weight: 700;
        }}

        /* HEADER CONTROLS */
        .header-controls {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .search-field {{
            position: relative;
            width: 220px;
        }}

        .search-field input {{
            width: 100%;
            padding: 6px 12px 6px 32px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            font-size: 13px;
            outline: none;
        }}

        .search-field svg {{
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 15px;
            height: 15px;
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
        }}

        .mode-btn.active {{
            background: #ffffff;
            color: var(--primary-navy);
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
        }}

        /* LAYOUT */
        .portal-layout {{
            max-width: 1520px;
            margin: 0 auto;
            padding: 24px;
            display: flex;
            gap: 28px;
            width: 100%;
            flex: 1;
        }}

        aside.portal-sidebar {{
            width: 280px;
            flex-shrink: 0;
            position: sticky;
            top: 76px;
            max-height: calc(100vh - 90px);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .stats-summary-card {{
            background: linear-gradient(135deg, var(--primary-navy), var(--primary-blue));
            color: white;
            padding: 16px;
            border-radius: var(--card-radius);
            box-shadow: var(--shadow-default);
        }}

        .stats-summary-card h4 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .stats-2x2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .stat-item {{
            background: rgba(255, 255, 255, 0.16);
            backdrop-filter: blur(4px);
            padding: 6px 8px;
            border-radius: 8px;
            text-align: center;
        }}

        .stat-val {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 800;
        }}

        .stat-lbl {{
            font-size: 10.5px;
            opacity: 0.9;
            text-transform: uppercase;
        }}

        .nav-list-card {{
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
            padding: 14px;
        }}

        .nav-list-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }}

        .sidebar-links-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 7px 10px;
            border-radius: 6px;
            color: var(--text-heading);
            text-decoration: none;
            font-size: 12.5px;
            font-weight: 500;
            transition: all 0.15s;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--primary-light);
            color: var(--primary-dark);
            font-weight: 600;
        }}

        main.portal-main {{
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        .section-box {{
            background: #ffffff;
            border-radius: var(--card-radius);
            border: 1px solid var(--border-subtle);
            padding: 24px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        }}

        .section-headline {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-subtle);
            flex-wrap: wrap;
            gap: 12px;
        }}

        .headline-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .headline-icon-box {{
            width: 42px;
            height: 42px;
            border-radius: 10px;
            background: var(--primary-light);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}

        .headline-text h2 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 18px;
            font-weight: 800;
            color: var(--primary-navy);
        }}

        .headline-text p {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        /* VOCAB FLASHCARDS (CARDS.HTML SPEC) */
        .vocab-group-header {{
            margin: 20px 0 12px 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #1e3a8a;
            font-size: 16px;
        }}

        .vocab-cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }}

        .vocab-card-item {{
            background: #ffffff;
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            transition: all 0.2s;
        }}

        .vocab-card-item:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(37,99,235,0.12);
        }}

        .card-img-wrap {{
            height: 160px;
            background: #f8fafc;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}

        .card-img-wrap img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}

        .btn-audio-speak {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(37, 99, 235, 0.9);
            color: white;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            transition: all 0.15s;
        }}

        .btn-audio-speak:hover {{
            background: #1d4ed8;
            transform: scale(1.1);
        }}

        .card-body {{
            padding: 14px;
            display: flex;
            flex-direction: column;
            flex: 1;
        }}

        .card-word-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: #0f172a;
        }}

        .card-ipa-line {{
            font-size: 13px;
            color: var(--primary-blue);
            margin-top: 2px;
        }}

        .card-pos {{
            color: #64748b;
            font-style: italic;
        }}

        .card-divider {{
            height: 1px;
            background: #e2e8f0;
            margin: 8px 0;
        }}

        .card-def-vi {{
            font-size: 13.5px;
            font-weight: 600;
            color: #334155;
            line-height: 1.4;
        }}

        .card-ex-en {{
            font-size: 12px;
            font-style: italic;
            color: #64748b;
            margin-top: 6px;
        }}

        .vocab-exercises-preview-note {{
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 10px;
            padding: 16px 20px;
            color: #1e40af;
            font-size: 14px;
        }}

        {get_grammar_css()}
    </style>
</head>

<body class="mode-practice">

    <!-- APP HEADER -->
    <header class="portal-header">
        <div class="header-inner">
            <div class="brand-meta">
                <div class="brand-badge">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                    GLOBAL SUCCESS 12
                </div>
                <div class="brand-titles">
                    <h1>PORTAL TỪ VỰNG & NGỮ PHÁP</h1>
                    <p>Khung chương trình chuẩn Bộ GD&ĐT &bull; Lý thuyết & Bài tập tương tác</p>
                </div>
            </div>

            <!-- UNIT SWITCHER -->
            <div class="unit-nav-wrap">
                {''.join(unit_tabs_nav)}
            </div>

            <!-- TAB SWITCHER: ALL / VOCAB / EXERCISES / GRAMMAR -->
            <div class="header-nav-tabs">
                <button type="button" class="nav-tab-btn active" id="tabAll" onclick="switchMainTab('all')">📚 Tất Cả</button>
                <button type="button" class="nav-tab-btn" id="tabTheory" onclick="switchMainTab('theory')">💡 Lý Thuyết Từ Vựng</button>
                <button type="button" class="nav-tab-btn" id="tabExercises" onclick="switchMainTab('exercises')">✍️ Bài Tập Từ Vựng</button>
                <button type="button" class="nav-tab-btn" id="tabGrammar" onclick="switchMainTab('grammar')">📐 Ngữ Pháp (Lý Thuyết & Bài Tập)</button>
            </div>

            <!-- CONTROLS: SEARCH, REVIEW/PRACTICE -->
            <div class="header-controls">
                <div class="search-field">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                    <input type="text" id="globalSearchInput" placeholder="Tìm từ vựng, ngữ pháp..." oninput="handleGlobalSearch(this.value)">
                </div>

                <div class="mode-toggle">
                    <button type="button" class="mode-btn" id="btnModeReview" onclick="setPortalMode('review')">👁️ Xem Đáp Án</button>
                    <button type="button" class="mode-btn active" id="btnModePractice" onclick="setPortalMode('practice')">✏️ Làm Bài</button>
                </div>
            </div>
        </div>
    </header>

    <!-- MAIN PORTAL LAYOUT -->
    <div class="portal-layout">
        <!-- SIDEBAR -->
        <aside class="portal-sidebar">
            <div class="stats-summary-card">
                <h4>
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                    Tổng Quan Bài Học (Unit <span id="sidebar-unit-num">1</span>)
                </h4>
                <div class="stats-2x2">
                    <div class="stat-item">
                        <div class="stat-val" id="stat-vocab-words">46</div>
                        <div class="stat-lbl">Từ vựng</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val" id="stat-vocab-ex">16</div>
                        <div class="stat-lbl">Bài tập từ</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val" id="stat-grammar-ex">8</div>
                        <div class="stat-lbl">Dạng ngữ pháp</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val" id="stat-grammar-q">130</div>
                        <div class="stat-lbl">Câu hỏi NP</div>
                    </div>
                </div>
            </div>

            <div class="nav-list-card">
                <div class="nav-list-title">
                    <span>Mục Lục Nhanh</span>
                    <span>Từ Vựng & NP</span>
                </div>
                <ul class="sidebar-links-list">
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('section-vocab-theory')" class="nav-item">💡 Lý Thuyết Từ Vựng</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('section-vocab-exercises')" class="nav-item">✍️ Bài Tập Từ Vựng (16 Dạng)</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('section-grammar')" class="nav-item active">📐 Ngữ Pháp: Lý Thuyết Chuẩn</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_a')" class="nav-item">#A. Verb Form Completion</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_b')" class="nav-item">#B. Multiple Choice (MCQ)</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_c')" class="nav-item">#C. Sentence Matching</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_d')" class="nav-item">#D. Sentence Transformation</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_e')" class="nav-item">#E. Guided Cloze Passages</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_f')" class="nav-item">#F. Error Identification</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_g')" class="nav-item">#G. Sentence Combination</a></li>
                    <li><a href="javascript:void(0)" onclick="scrollToTarget('g_u1_h')" class="nav-item">#H. Sentence Building</a></li>
                </ul>
            </div>
        </aside>

        <!-- MAIN SECTIONS -->
        <main class="portal-main">
            {''.join(units_containers_html)}
        </main>
    </div>

    <!-- PORTAL JAVASCRIPT CONTROLLERS -->
    {portal_js_code}
    {get_grammar_js()}
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Master index.html generated successfully at: {output_file}")


def build_unified_portal(target_unit=None):
    workspace_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    theory_db = load_grammar_theory_db(workspace_root).get("GS12", {})
    available_units = get_units_list(workspace_root)
    
    # Generate standalone files for each unit
    for u in available_units:
        u_theory = theory_db.get(str(u), {})
        u_folder = workspace_root / "lessons" / f"unit-{u}"
        g_ex_dir = u_folder / "grammar" / "exercises"

        ex_files_dict = {}
        for f in glob.glob(str(g_ex_dir / "*.json")):
            fname = os.path.basename(f)
            ex_files_dict[fname] = load_json(f)

        theory_html = render_grammar_theory_html(u, u_theory)
        exercises_html = render_grammar_exercises_html(u, ex_files_dict, u_theory)

        standalone_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Success 12 • Unit {u} - Grammar Lesson</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Be Vietnam Pro', sans-serif;
            background: #f8fafc;
            color: #0f172a;
            padding: 24px;
            margin: 0;
        }}
        .standalone-container {{
            max-width: 1000px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            overflow: hidden;
            border: 1px solid #e2e8f0;
            padding: 20px;
        }}
        {get_grammar_css()}
    </style>
</head>
<body class="mode-practice">
    <div class="standalone-container">
        {theory_html}
        {exercises_html}
    </div>
    {get_grammar_js()}
</body>
</html>
"""
        standalone_out = u_folder / f"grammar_unit{u}.html"
        with open(standalone_out, "w", encoding="utf-8") as f:
            f.write(standalone_html)
        print(f"Generated standalone grammar page: {standalone_out}")

    # Generate master index.html
    master_index_path = workspace_root / "index.html"
    generate_master_index(workspace_root, available_units, theory_db, master_index_path)


def main():
    parser = argparse.ArgumentParser(description="Grammar & Vocabulary Portal Builder")
    parser.add_argument("--unit", type=int, help="Build specific unit (1-10)")
    parser.add_argument("--all", action="store_true", help="Build all units and master index.html")
    args = parser.parse_args()

    build_unified_portal(target_unit=args.unit)


if __name__ == "__main__":
    main()
