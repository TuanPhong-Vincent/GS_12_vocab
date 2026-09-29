#!/usr/bin/env python3
"""
Vocabulary & Exercises Index Builder (build_vocab_index.py)

Generates:
1. `index.html`: Publication-grade unified web portal combining Vocabulary Theory
   (styled identically to cards.html) and all 16 Practice Exercises (with uniform
   navy/blue title styling, aligned elements, live search, TTS audio, and dual Review/Practice modes).
2. `cards.html`: Standalone vocabulary flashcards page conforming to the Modern Blue spec.
"""

import os
import sys
import json
import glob
import re
import argparse
from pathlib import Path
from html import escape

# Safe Windows stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_json(file_path):
    """Safely load and parse a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed to read {file_path}: {e}", file=sys.stderr)
        return None


def resolve_unit_paths(input_path):
    """
    Given a path that could be a unit folder (lessons/unit-1)
    or a vocab folder (lessons/unit-1/vocab), normalize and return
    (vocab_dir, unit_name, book_name).
    """
    path_obj = Path(input_path).resolve()
    if path_obj.name.lower() == "vocab":
        vocab_dir = path_obj
        unit_dir = path_obj.parent
    else:
        vocab_dir = path_obj / "vocab" if (path_obj / "vocab").is_dir() else path_obj
        unit_dir = path_obj

    # Detect unit name e.g. "Unit 1"
    unit_name = "Unit 1"
    book_name = "Global Success 12"

    parts = list(unit_dir.parts)
    for p in reversed(parts):
        m = re.match(r"^unit[-_]?(\d+)$", p, re.IGNORECASE)
        if m:
            unit_name = f"Unit {m.group(1)}"
            break

    for p in parts:
        if re.search(r"gs[-_]?12", p, re.IGNORECASE) or "12" in p:
            book_name = "Global Success 12"
            break
        elif re.search(r"gs[-_]?11", p, re.IGNORECASE):
            book_name = "Global Success 11"
            break
        elif re.search(r"gs[-_]?10", p, re.IGNORECASE):
            book_name = "Global Success 10"
            break

    return vocab_dir, unit_dir, book_name, unit_name


def find_workspace_root(start_path):
    """Locate the workspace root by looking for GS12.pdf or .agent."""
    curr = Path(start_path).resolve()
    for p in [curr] + list(curr.parents):
        if (p / ".agent").exists() or (p / "lessons").exists():
            return p
    return curr


def resolve_asset_relpath(asset_path_str, output_html_file, workspace_root):
    """
    Convert an asset path (like /lessons/media/gs12/unit-1/images/childhood.webp)
    into a relative path from the output HTML file location so it loads
    seamlessly in browsers via file:/// or web servers.
    """
    if not asset_path_str:
        return ""
    
    # If it's already an http(s) URL
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


def build_vocab_cards_html_content(vocab_data, unit_title, subtitle, output_file, workspace_root):
    """
    Build standalone cards.html matching the exact user template and design.
    """
    card_items_html = []

    for group in vocab_data:
        g_name = group.get("group", "")
        for word in group.get("words", []):
            en_word = word.get("english_word", "").strip()
            ipa = word.get("pronunciation_british") or word.get("pronunciation_american") or ""
            meaning = word.get("vietnamese_meaning", "").strip()
            img_raw = word.get("image", "")
            img_rel = resolve_asset_relpath(img_raw, output_file, workspace_root)
            alt_text = word.get("alt") or en_word

            # Audio fallback string
            safe_word = en_word.replace("'", "\\'")

            card = f"""
            <!-- Card: {escape(en_word)} -->
            <div class="vocab-card" data-word="{escape(en_word.lower())}" data-group="{escape(g_name.lower())}">
                <div class="image-container">
                    <img src="{escape(img_rel)}" alt="{escape(alt_text)}" loading="lazy" onerror="this.style.opacity='0.4';">
                    <button class="btn-audio" onclick="speak('{safe_word}')" title="Nghe phát âm '{escape(en_word)}'">
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
            card_items_html.append(card)

    cards_body = "\n".join(card_items_html)

    return f"""<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(unit_title)} - Vocabulary Cards</title>
    <!-- Google Fonts: Be Vietnam Pro & Plus Jakarta Sans -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {{
            --primary-blue: #2563eb;
            --primary-dark: #1d4ed8;
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
            padding: 40px 24px 60px;
        }}

        .container {{
            max-width: 1460px;
            margin: 0 auto;
        }}

        .header-bar {{
            text-align: center;
            margin-bottom: 36px;
        }}

        .header-bar h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 30px;
            font-weight: 800;
            color: #1e3a8a;
            letter-spacing: -0.5px;
            display: inline-flex;
            align-items: center;
            gap: 12px;
        }}

        .header-bar p {{
            color: var(--text-muted);
            font-size: 15px;
            margin-top: 8px;
        }}

        /* Live filter toolbar */
        .toolbar {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 30px;
            gap: 14px;
            flex-wrap: wrap;
        }}

        .search-box {{
            position: relative;
            width: 320px;
            max-width: 100%;
        }}

        .search-box input {{
            width: 100%;
            padding: 10px 16px 10px 42px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            background: #ffffff;
            font-size: 14px;
            font-family: inherit;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            outline: none;
            transition: all 0.2s;
        }}

        .search-box input:focus {{
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        .search-box svg {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            width: 18px;
            height: 18px;
            color: var(--text-muted);
        }}

        .btn-portal {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 9999px;
            background: var(--primary-blue);
            color: #ffffff;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }}

        .btn-portal:hover {{
            background: var(--primary-dark);
            transform: translateY(-1px);
        }}

        /* BỐ CỤC GRID: 4 - 5 cards / hàng */
        .vocab-grid {{
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        }}

        @media (min-width: 1320px) {{
            .vocab-grid {{
                grid-template-columns: repeat(5, 1fr);
                /* 5 cards / hàng cho màn hình rộng */
            }}
        }}

        @media (min-width: 1024px) and (max-width: 1319px) {{
            .vocab-grid {{
                grid-template-columns: repeat(4, 1fr);
                /* 4 cards / hàng cho laptop */
            }}
        }}

        /* CARD TỪ VỰNG BO GÓC MỀM MẠI */
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

        /* KHUNG HÌNH ẢNH TO - KHÔNG CROP MẤT HÌNH - KHÔNG PHÓNG TO */
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
            /* Giữ trọn vẹn toàn bộ ảnh, không bị cắt góc */
            border-radius: 12px;
            display: block;
            transition: transform 0.3s ease;
        }}

        .vocab-card:hover .image-container img {{
            transform: scale(1.02);
        }}

        /* NÚT LOA PHÁT ÂM HIỆN ĐẠI */
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

        /* KHỐI NỘI DUNG TỪ VỰNG */
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

        /* TỪ TIẾNG ANH: CHỮ THƯỜNG / TITLE CASE TINH TẾ (KHÔNG DÙNG IN HOA) */
        .word-en {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 21px;
            font-weight: 700;
            color: #1e293b;
            letter-spacing: -0.3px;
            text-transform: none;
            /* Giữ chữ thường, không in hoa */
        }}

        /* PHIÊN ÂM IPA */
        .word-ipa {{
            font-size: 14px;
            color: #3b82f6;
            /* Xanh lam dịu */
            font-weight: 500;
            font-family: 'Be Vietnam Pro', sans-serif;
        }}

        /* ĐƯỜNG PHÂN CÁCH TINH GỌN */
        .divider {{
            height: 1px;
            background: linear-gradient(90deg, #e2e8f0 0%, rgba(226, 232, 240, 0.2) 100%);
        }}

        /* NGHĨA TIẾNG VIỆT */
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
            <h1>📖 {escape(unit_title)} - Lý Thuyết Từ Vựng</h1>
            <p>{escape(subtitle)}</p>
        </div>

        <div class="toolbar">
            <div class="search-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                <input type="text" id="searchInput" placeholder="Tìm kiếm từ vựng, phiên âm, nghĩa..." oninput="filterCards(this.value)">
            </div>
            <a href="index.html" class="btn-portal">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
                Xem Bài Tập & Lý Thuyết (index.html)
            </a>
        </div>

        <!-- GRID HIỂN THỊ HÀNG LOẠT -->
        <div class="vocab-grid" id="vocabGrid">
{cards_body}
        </div>
    </div>

    <script>
        // Phát âm giọng chuẩn Mỹ qua Web Speech API
        function speak(text) {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'en-US';
                utterance.rate = 0.9;
                window.speechSynthesis.speak(utterance);
            }}
        }}

        // Lọc thẻ từ vựng trực tiếp
        function filterCards(query) {{
            const q = query.trim().toLowerCase();
            const cards = document.querySelectorAll('.vocab-card');
            cards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                if (!q || text.includes(q)) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>

</html>
"""


def render_all_exercises_html(exercises_data, output_file, workspace_root):
    """
    Renders all 16 exercise blocks cleanly with uniform titles, consistent colors,
    and proportional alignment of elements.
    """
    rendered_blocks = []

    for ex_idx, ex in enumerate(exercises_data):
        ex_id = ex.get("id", str(ex_idx + 1))
        ex_type = ex.get("type", "")
        ex_title = ex.get("title", f"Exercise {ex_idx+1}")
        ex_desc = ex.get("description", "")
        file_name = ex.get("_filename", "")

        body_html = render_single_exercise_inner(ex, ex_idx, output_file, workspace_root)

        block = f"""
        <!-- Exercise Card {ex_id}: {escape(ex_title)} -->
        <div class="exercise-card" id="exercise-block-{ex_idx}" data-ex-idx="{ex_idx}" data-ex-type="{escape(ex_type)}">
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
                    <span class="score-pill" id="score-pill-{ex_idx}" style="display:none;"></span>
                    <button type="button" class="btn-check" onclick="checkExercise({ex_idx})">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                        Kiểm Tra
                    </button>
                    <button type="button" class="btn-reset" onclick="resetExercise({ex_idx})" title="Làm lại bài này">
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


def highlight_target_word(text):
    """Transforms [word] into an underlined target word highlight."""
    if not text:
        return ""
    return re.sub(r"\[([^\]]+)\]", r"<span class='target-word'>\1</span>", escape(text))


def render_single_exercise_inner(ex, ex_idx, output_file, workspace_root):
    """
    Renders inner content of each exercise cleanly and proportionally.
    """
    ex_type = ex.get("type", "")
    questions = ex.get("questions", [])

    # 1. Multiple Choice (Direct, Sentence, Conversation, Closest, Opposite, Word Family MCQ)
    if ex_type in ["multiple_choice", "word_families_mcq", "sentence_ordering_multiple_choice"]:
        items = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            raw_text = q.get("text", "")
            sentences = q.get("sentences", [])
            options = q.get("options", [])
            correct = q.get("correct_answer", "").strip()

            # Format dialogue if multiline
            if "\n" in raw_text:
                dialogue_lines = raw_text.split("\n")
                formatted_stem = "<div class='dialogue-box'>" + "".join(
                    f"<div class='dialogue-line'>{highlight_target_word(line)}</div>" for line in dialogue_lines if line.strip()
                ) + "</div>"
            elif sentences:
                # Sentence ordering
                s_list = "".join(f"<li class='order-item'>{escape(s)}</li>" for s in sentences)
                formatted_stem = f"<ol class='sentence-order-list'>{s_list}</ol>"
            else:
                formatted_stem = f"<div class='question-stem'>{highlight_target_word(raw_text)}</div>"

            # Render 4 options in clean responsive grid
            option_letters = ["A", "B", "C", "D"]
            opt_htmls = []
            for opt_i, opt in enumerate(options):
                letter = option_letters[opt_i] if opt_i < len(option_letters) else str(opt_i + 1)
                opt_str = str(opt).strip()
                is_correct = (opt_str.lower() == correct.lower())
                
                # Input radio
                radio_name = f"ex_{ex_idx}_q_{q_idx}"
                opt_id = f"opt_{ex_idx}_{q_idx}_{opt_i}"

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
                <div class="q-feedback" id="feedback_{ex_idx}_{q_idx}" style="display:none;"></div>
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
                    <img src="{escape(img_rel)}" alt="Question {q_id}" loading="lazy" onerror="this.style.opacity='0.4';">
                    <span class="pic-tag">#{q_id}</span>
                </div>
                <div class="pic-controls">
                    <input type="text" class="tidy-input pic-input" id="input_{ex_idx}_{q_idx}" placeholder="Nhập từ tiếng Anh..." autocomplete="off">
                    <div class="answer-badge" id="ans_badge_{ex_idx}_{q_idx}" style="display:none;">
                        <span>Đáp án:</span> <strong>{escape(correct)}</strong>
                    </div>
                </div>
            </div>"""
            items.append(card)
        return f"<div class='pic-grid'>{''.join(items)}</div>"

    # 3. Write English Words from Vietnamese (05)
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
                        <input type="text" class="tidy-input write-input" id="input_{ex_idx}_{q_idx}_{p_idx}" placeholder="Viết từ tiếng Anh tương ứng..." autocomplete="off">
                        <span class="sub-ans-reveal" id="sub_ans_{ex_idx}_{q_idx}_{p_idx}" style="display:none;">{escape(correct)}</span>
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

            # Replace blanks ________ with inline input
            input_html = f"<input type='text' class='tidy-input inline-blank' id='input_{ex_idx}_{q_idx}' placeholder='...' autocomplete='off' data-correct='{escape(correct)}'>"
            formatted_sentence = re.sub(r"_{2,}", input_html, escape(raw_text))

            row = f"""
            <div class="question-row blank-row" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="q-header">
                    <span class="q-num">Câu {escape(str(q_id))}</span>
                    <div class="blank-sentence">{formatted_sentence}</div>
                </div>
                <div class="inline-ans-reveal" id="blank_ans_{ex_idx}_{q_idx}" style="display:none;">Đáp án: <strong>{escape(correct)}</strong></div>
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
                    <input type="text" class="tidy-input para-input" id="para_input_{ex_idx}_{blank_counter}" placeholder="..." autocomplete="off">
                    <span class="para-key" id="para_key_{ex_idx}_{blank_counter}" style="display:none;">{escape(b_correct)}</span>
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
                inp = f"<input type='text' class='tidy-input dict-blank' id='dict_inp_{ex_idx}_{e_idx}_{q_idx}' placeholder='...' autocomplete='off' data-correct='{escape(correct)}'>"
                formatted_q = re.sub(r"_{2,}", inp, escape(q_text))

                q_rows.append(f"""
                <div class="dict-question-item" data-correct="{escape(correct)}">
                    <span class="dict-q-num">#{q_id}</span>
                    <div class="dict-q-body">{formatted_q}</div>
                    <div class="dict-ans-reveal" id="dict_ans_{ex_idx}_{e_idx}_{q_idx}" style="display:none;">Đáp án: <strong>{escape(correct)}</strong></div>
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
                radio_name = f"ex_{ex_idx}_sign_{q_idx}"
                opt_id = f"opt_sign_{ex_idx}_{q_idx}_{opt_i}"

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
                <div class="q-feedback" id="feedback_{ex_idx}_{q_idx}" style="display:none;"></div>
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

            input_html = f"<input type='text' class='tidy-input inline-blank' id='wf_input_{ex_idx}_{q_idx}' placeholder='...' autocomplete='off' data-correct='{escape(correct)}'>"
            formatted_sentence = re.sub(r"_{2,}", input_html, escape(raw_text))

            row = f"""
            <div class="question-row wf-item-row" data-q-idx="{q_idx}" data-correct="{escape(correct)}">
                <div class="q-header">
                    <span class="q-num">Câu {escape(str(q_id))}</span>
                    <div class="blank-sentence">{formatted_sentence} <span class="root-badge">[{escape(base)}]</span></div>
                </div>
                <div class="inline-ans-reveal" id="wf_ans_{ex_idx}_{q_idx}" style="display:none;">Đáp án đúng: <strong>{escape(correct)}</strong></div>
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
                    <textarea class="tidy-textarea trans-textarea" id="trans_input_{ex_idx}_{q_idx}" placeholder="Nhập câu dịch tiếng Anh của bạn..." rows="2"></textarea>
                    <div class="trans-reveal-box" id="trans_key_{ex_idx}_{q_idx}" style="display:none;">
                        <span class="trans-key-label">🇬🇧 Đáp án chuẩn:</span>
                        <div class="trans-key-text">{escape(en_correct)}</div>
                    </div>
                </div>
            </div>"""
            items.append(row)
        return "\n".join(items)

    # Fallback generic
    return "<p class='empty-hint'>Định dạng bài tập đang được hiển thị.</p>"


def build_unified_index_html(vocab_data, exercises_data, book_name, unit_name, output_file, workspace_root):
    """
    Generates the complete index.html that unites:
    1. Vocabulary Theory (styled per cards.html)
    2. All 16 Practice Exercises with uniform title colors, aligned elements, live search, TTS.
    """
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

    m_u = re.search(r'\d+', unit_name)
    unit_num = m_u.group(0) if m_u else '1'
    full_title = f"{book_name.upper()} • {unit_name.upper()}"
    subtitle = f"Toàn diện Lý Thuyết Từ Vựng (Flashcards) & Hệ Thống 16 Dạng Bài Tập Thực Hành"

    # 1. Render Vocab Cards (Exact cards.html style)
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
                    <img src="{escape(img_rel)}" alt="{escape(alt_text)}" loading="lazy" onerror="this.style.opacity='0.4';">
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

    all_vocab_theory_html = "\n".join(vocab_cards_html)

    # 2. Render Exercises
    all_exercises_html = render_all_exercises_html(exercises_data, output_file, workspace_root)

    # 3. Sidebar Links
    sidebar_links = []
    sidebar_links.append(f"""
        <li>
            <a href="#section-theory" class="nav-item active" onclick="activateNav(this)">
                <span>📖 Lý Thuyết Từ Vựng</span>
                <span class="nav-badge">{total_words} từ</span>
            </a>
        </li>""")
    for e_idx, ex in enumerate(exercises_data):
        e_id = ex.get("id", str(e_idx + 1))
        e_title = ex.get("title", f"Exercise {e_idx+1}")
        short_title = e_title.split("-")[-1].strip() if "-" in e_title else e_title
        sidebar_links.append(f"""
        <li>
            <a href="#exercise-block-{e_idx}" class="nav-item" onclick="activateNav(this)">
                <span>#{e_id}. {escape(short_title)}</span>
            </a>
        </li>""")

    return f"""<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(full_title)} - Lý Thuyết & Bài Tập Từ Vựng</title>

    <!-- Google Fonts: Plus Jakarta Sans & Be Vietnam Pro -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {{
            /* Unified Palette - Modern Blue / Navy */
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

        /* STICKY APP HEADER */
        header.portal-header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
        }}

        .header-inner {{
            max-width: 1520px;
            margin: 0 auto;
            padding: 12px 24px;
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

        .header-nav-tabs {{
            display: flex;
            background: #f1f5f9;
            padding: 4px;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
        }}

        .nav-tab-btn {{
            padding: 6px 16px;
            border-radius: 9999px;
            border: none;
            background: transparent;
            font-size: 13px;
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

        .header-controls {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}

        .search-field {{
            position: relative;
            width: 250px;
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

        /* APP LAYOUT */
        .portal-layout {{
            max-width: 1520px;
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
            top: 76px;
            max-height: calc(100vh - 90px);
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

        /* MAIN CONTENT AREA */
        main.portal-main {{
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 36px;
        }}

        /* SECTION CONTAINERS */
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

        /* LÝ THUYẾT TỪ VỰNG - THE EXACT CARDS.HTML SPEC */
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
            text-transform: none;
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

        /* BÀI TẬP TỪ VỰNG - UNIFORM TITLE COLORS & PROPORTIONAL ALIGNMENT */
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

        /* UNIFORM EXERCISE HEADER */
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

        /* UNIFORM EXERCISE TITLE COLOR */
        .exercise-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: var(--primary-navy); /* Unified across ALL 16 exercises */
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

        /* QUESTION ROWS & CARDS */
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

        /* OPTIONS GRID - 2 COLUMNS ON DESKTOP, 1 ON MOBILE */
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

        /* RADIO SELECTED STATE */
        .option-label.is-selected {{
            border-color: var(--primary-blue);
            background: var(--primary-light);
        }}

        .option-label.is-selected .option-badge {{
            background: var(--primary-blue);
            color: white;
        }}

        /* REVIEW / CHECK FEEDBACK STATE */
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

        /* TIDY INPUT STYLING */
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

        /* DIALOGUE BUBBLE */
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

        /* SENTENCE ORDERING */
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

        /* PICTURE TO WORD (04) */
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

        /* WRITE PARTS (05) */
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
            font-size: 14px;
            font-weight: 600;
            color: #334155;
            flex: 1;
            min-width: 220px;
        }}

        .part-input-wrap {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .write-input {{
            width: 240px;
        }}

        .sub-ans-reveal {{
            font-size: 12px;
            font-weight: 700;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 4px 8px;
            border-radius: 6px;
        }}

        /* WORD BOX */
        .word-box-container {{
            background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
            border: 1px solid #bfdbfe;
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .word-box-label {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 800;
            color: var(--primary-navy);
            letter-spacing: 0.5px;
        }}

        .word-box-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .word-box-chip {{
            background: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            color: var(--primary-navy);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }}

        .inline-blank {{
            display: inline-block;
            width: 140px;
            margin: 0 4px;
            padding: 4px 8px;
            font-size: 13.5px;
        }}

        .blank-sentence {{
            font-size: 14.5px;
            line-height: 1.7;
        }}

        .inline-ans-reveal {{
            margin-top: 6px;
            font-size: 12px;
            color: var(--success-color);
            background: var(--success-bg);
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
        }}

        /* PARAGRAPH FLOW (07) */
        .paragraph-flow-card {{
            background: #ffffff;
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 24px;
            line-height: 2.2;
            font-size: 15px;
        }}

        .inline-slot {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin: 0 4px;
            vertical-align: middle;
        }}

        .slot-num {{
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-blue);
        }}

        .para-input {{
            width: 120px;
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

        /* OXFORD DICTIONARY CARDS (11) */
        .oxford-dict-card {{
            background: #ffffff;
            border: 1px solid var(--border-subtle);
            border-left: 4px solid var(--primary-blue);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .dict-head {{
            display: flex;
            align-items: baseline;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .dict-word-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 19px;
            font-weight: 800;
            color: var(--primary-navy);
        }}

        .dict-pos-tag {{
            font-style: italic;
            color: var(--text-muted);
            font-size: 13.5px;
            font-weight: 600;
        }}

        .dict-ipa {{
            color: var(--primary-blue);
            font-size: 13.5px;
        }}

        .dict-def {{
            font-size: 14px;
            color: #334155;
            padding-left: 10px;
            border-left: 2px solid var(--border-subtle);
        }}

        .dict-collocs {{
            background: #f8fafc;
            border-radius: 8px;
            padding: 10px 14px;
        }}

        .dict-collocs-title {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }}

        .dict-bullets-list {{
            list-style-type: square;
            padding-left: 18px;
            font-size: 13.5px;
            color: #334155;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .dict-practice-title {{
            font-size: 12px;
            font-weight: 700;
            color: var(--primary-navy);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        .dict-question-item {{
            padding: 8px 12px;
            background: #f8fafc;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 13.5px;
        }}

        .dict-q-num {{
            font-weight: 700;
            color: var(--primary-blue);
            margin-right: 6px;
        }}

        .dict-blank {{
            width: 180px;
            margin: 0 4px;
        }}

        .dict-ans-reveal {{
            font-size: 12px;
            color: var(--success-color);
            margin-top: 4px;
        }}

        /* SIGNS AND NOTICES (12) */
        .sign-layout {{
            display: flex;
            gap: 20px;
            align-items: flex-start;
            flex-wrap: wrap;
        }}

        .sign-board {{
            width: 220px;
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
            flex-shrink: 0;
        }}

        .sign-board.has-image {{
            background: #ffffff;
            padding: 4px;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            display: flex;
            align-items: center;
            justify-content: center;
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
            font-size: 32px;
            margin-bottom: 8px;
        }}

        .sign-desc {{
            font-size: 12px;
            line-height: 1.4;
            opacity: 0.95;
        }}

        .sign-qa {{
            flex: 1;
            min-width: 260px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        /* WORD FAMILIES TABLE (13) */
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
            background: white;
        }}

        .wf-table th {{
            background: #f8fafc;
            padding: 12px 16px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            color: var(--primary-navy);
            border-bottom: 2px solid var(--border-subtle);
            text-transform: uppercase;
            font-size: 11.5px;
            letter-spacing: 0.5px;
        }}

        .wf-table td {{
            padding: 10px 16px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .wf-table tr:hover td {{
            background: #f8fafc;
        }}

        .base-chip {{
            font-weight: 700;
            color: var(--primary-dark);
            background: var(--primary-light);
            padding: 2px 8px;
            border-radius: 6px;
        }}

        .base-type-tag {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .root-badge {{
            font-weight: 700;
            color: var(--primary-blue);
            background: var(--primary-light);
            padding: 2px 8px;
            border-radius: 6px;
            font-size: 12px;
        }}

        /* TRANSLATION (16) */
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
            padding: 10px 14px;
            border-radius: 8px;
        }}

        .trans-key-label {{
            font-size: 11px;
            font-weight: 700;
            color: var(--success-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 2px;
        }}

        .trans-key-text {{
            font-size: 14px;
            color: #065f46;
            font-weight: 600;
        }}

        /* FOOTER */
        footer.portal-footer {{
            background: #ffffff;
            border-top: 1px solid var(--border-subtle);
            padding: 20px 24px;
            text-align: center;
            font-size: 13px;
            color: var(--text-muted);
            margin-top: auto;
        }}

        /* PRINT STYLES */
        @media print {{
            header.portal-header, aside.portal-sidebar, .exercise-actions, .btn-audio {{
                display: none !important;
            }}
            .portal-layout {{
                display: block;
                padding: 0;
            }}
            .section-box, .exercise-card {{
                box-shadow: none;
                border: 1px solid #ccc;
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>

<body class="mode-practice">

    <!-- STICKY APP HEADER -->
    <header class="portal-header">
        <div class="header-inner">
            <div class="brand-meta">
                <div class="brand-badge">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                    </svg>
                    VOCAB MASTER
                </div>
                <div class="brand-titles">
                    <h1>{escape(full_title)}</h1>
                    <p>{total_words} Từ vựng &bull; 16 Dạng bài tập &bull; {total_questions} Câu hỏi</p>
                </div>
            </div>

            <!-- TAB SWITCHER: ALL / THEORY / EXERCISES -->
            <div class="header-nav-tabs">
                <button type="button" class="nav-tab-btn active" id="tabAll" onclick="switchMainTab('all')">📚 Tất Cả</button>
                <button type="button" class="nav-tab-btn" id="tabTheory" onclick="switchMainTab('theory')">💡 Lý Thuyết (Cards)</button>
                <button type="button" class="nav-tab-btn" id="tabExercises" onclick="switchMainTab('exercises')">✍️ Bài Tập (16 Dạng)</button>
            </div>

            <!-- CONTROLS: SEARCH, REVIEW/PRACTICE, PRINT -->
            <div class="header-controls">
                <div class="search-field">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="11" cy="11" r="8"/>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <input type="text" id="globalSearchInput" placeholder="Tìm từ vựng, câu hỏi..." oninput="handleGlobalSearch(this.value)">
                </div>

                <div class="mode-toggle">
                    <button type="button" class="mode-btn" id="btnModeReview" onclick="setMode('review')">👁️ Xem Đáp Án</button>
                    <button type="button" class="mode-btn active" id="btnModePractice" onclick="setMode('practice')">✏️ Làm Bài</button>
                </div>

                <a href="vocab_unit{unit_num}.pdf" target="_blank" class="btn-print" title="Mở &amp; In file PDF sách bài học (Lý thuyết &amp; 16 Dạng bài)" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="6 9 6 2 18 2 18 9"/>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
                        <rect x="6" y="14" width="12" height="8"/>
                    </svg>
                    In PDF
                </a>
            </div>
        </div>
    </header>

    <!-- MAIN PORTAL LAYOUT -->
    <div class="portal-layout">
        <!-- SIDEBAR -->
        <aside class="portal-sidebar">
            <div class="stats-summary-card">
                <h4>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="20" x2="18" y2="10"/>
                        <line x1="12" y1="20" x2="12" y2="4"/>
                        <line x1="6" y1="20" x2="6" y2="14"/>
                    </svg>
                    Tổng Quan Bài Học
                </h4>
                <div class="stats-2x2">
                    <div class="stat-item">
                        <div class="stat-val">{total_words}</div>
                        <div class="stat-lbl">Từ vựng</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val">{total_groups}</div>
                        <div class="stat-lbl">Nhóm chủ đề</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val">{total_exercises}</div>
                        <div class="stat-lbl">Bài tập</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-val">{total_questions}</div>
                        <div class="stat-lbl">Câu hỏi</div>
                    </div>
                </div>
            </div>

            <div class="nav-list-card">
                <div class="nav-list-title">
                    <span>Mục Lục Nhanh</span>
                    <span>{1 + total_exercises} mục</span>
                </div>
                <ul class="sidebar-links-list">
                    {''.join(sidebar_links)}
                </ul>
            </div>
        </aside>

        <!-- MAIN SECTIONS -->
        <main class="portal-main">
            <!-- 1. LÝ THUYẾT TỪ VỰNG (CARDS.HTML COMPLIANT) -->
            <section class="section-box" id="section-theory">
                <div class="section-headline">
                    <div class="headline-left">
                        <div class="headline-icon-box">📖</div>
                        <div class="headline-text">
                            <h2>Lý Thuyết Từ Vựng Trọng Tâm (Flashcards)</h2>
                            <p>{total_words} từ vựng chuẩn ngữ âm, nghĩa tiếng Việt, hình ảnh minh họa và phát âm giọng Mỹ</p>
                        </div>
                    </div>
                    <div>
                        <a href="cards.html" class="nav-item" style="border:1px solid #bfdbfe; font-size:12px; font-weight:700;" title="Mở trang thẻ riêng biệt">
                            Mở Trang cards.html ↗
                        </a>
                    </div>
                </div>
                <div class="theory-body">
                    {all_vocab_theory_html}
                </div>
            </section>

            <!-- 2. BÀI TẬP TỪ VỰNG (16 DẠNG) -->
            <section class="section-box" id="section-exercises">
                <div class="section-headline">
                    <div class="headline-left">
                        <div class="headline-icon-box">✍️</div>
                        <div class="headline-text">
                            <h2>Hệ Thống Bài Tập Thực Hành Từ Vựng</h2>
                            <p>16 dạng bài tập chuẩn format THPT & Quốc Gia &bull; {total_questions} câu hỏi luyện tập trực tiếp</p>
                        </div>
                    </div>
                </div>
                <div class="exercises-container">
                    {all_exercises_html}
                </div>
            </section>
        </main>
    </div>

    <!-- FOOTER -->
    <footer class="portal-footer">
        <p>Hệ thống Học Từ Vựng & Bài Tập Tương Tác &bull; {escape(full_title)} &bull; Google Deepmind Antigravity Skills</p>
    </footer>

    <!-- INTERACTIVE JAVASCRIPT LOGIC -->
    <script>
        // Data models for scoring
        const EXERCISE_DATA = {json.dumps([{
            "idx": i,
            "id": ex.get("id"),
            "type": ex.get("type"),
            "title": ex.get("title")
        } for i, ex in enumerate(exercises_data)], ensure_ascii=False)};

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

        // Tab Switcher
        function switchMainTab(tab) {{
            const theorySec = document.getElementById('section-theory');
            const exSec = document.getElementById('section-exercises');
            const btns = ['tabAll', 'tabTheory', 'tabExercises'];
            btns.forEach(b => document.getElementById(b).classList.remove('active'));

            if (tab === 'theory') {{
                theorySec.style.display = 'block';
                exSec.style.display = 'none';
                document.getElementById('tabTheory').classList.add('active');
            }} else if (tab === 'exercises') {{
                theorySec.style.display = 'none';
                exSec.style.display = 'block';
                document.getElementById('tabExercises').classList.add('active');
            }} else {{
                theorySec.style.display = 'block';
                exSec.style.display = 'block';
                document.getElementById('tabAll').classList.add('active');
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
                btnRev.classList.add('active');
                btnPrac.classList.remove('active');
                revealAllAnswerKeys(true);
            }} else {{
                body.classList.remove('mode-review');
                body.classList.add('mode-practice');
                btnPrac.classList.add('active');
                btnRev.classList.remove('active');
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
        function checkExercise(exIdx) {{
            const block = document.getElementById(`exercise-block-${{exIdx}}`);
            if (!block) return;

            let correctCount = 0;
            let totalCount = 0;

            // 1. Multiple Choice checks
            const qRows = block.querySelectorAll('.question-row[data-correct]');
            qRows.forEach(row => {{
                const targetCorrect = (row.getAttribute('data-correct') || '').trim().toLowerCase();
                const selectedRadio = row.querySelector('input[type="radio"]:checked');
                
                totalCount++;

                // Clear previous result classes
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
                        // Highlight the right one
                        row.querySelectorAll('.option-label[data-is-correct="true"]').forEach(c => c.classList.add('result-correct'));
                    }}
                }} else {{
                    // Highlight correct
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

            // 3. Write English parts (05)
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

            // 4. Inline blanks (06, 15)
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

            // 5. Paragraph slots (07)
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

            // 6. Dictionary blanks (11)
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

            // 7. Translation reveals (16)
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
            const scorePill = document.getElementById(`score-pill-${{exIdx}}`);
            if (scorePill && totalCount > 0) {{
                scorePill.style.display = 'inline-block';
                scorePill.textContent = `${{correctCount}} / ${{totalCount}} Đúng (${{Math.round(correctCount / totalCount * 100)}}%)`;
            }}
        }}

        // Reset an exercise
        function resetExercise(exIdx) {{
            const block = document.getElementById(`exercise-block-${{exIdx}}`);
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

            const scorePill = document.getElementById(`score-pill-${{exIdx}}`);
            if (scorePill) scorePill.style.display = 'none';
        }}

        // Live Search Handler
        function handleGlobalSearch(query) {{
            const q = query.trim().toLowerCase();

            // 1. Filter vocab cards
            const cards = document.querySelectorAll('.vocab-card');
            cards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                card.style.display = (!q || text.includes(q)) ? 'flex' : 'none';
            }});

            // 2. Filter questions in exercises
            const qRows = document.querySelectorAll('.question-row, .pic-word-card, .oxford-dict-card');
            qRows.forEach(row => {{
                const text = row.textContent.toLowerCase();
                row.style.display = (!q || text.includes(q)) ? '' : 'none';
            }});
        }}

        // Sidebar active link update on click
        function activateNav(linkEl) {{
            document.querySelectorAll('.sidebar-links-list .nav-item').forEach(l => l.classList.remove('active'));
            linkEl.classList.add('active');
        }}
    </script>
</body>

</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Build index.html and cards.html for vocabulary theory & exercises.")
    parser.add_argument("vocab_dir", help="Path to unit vocab folder (e.g., lessons/unit-1/vocab or lessons/unit-1)")
    parser.add_argument("--output-index", "-oi", default=None, help="Destination path for index.html")
    parser.add_argument("--output-cards", "-oc", default=None, help="Destination path for cards.html")

    args = parser.parse_args()

    vocab_dir, unit_dir, book_name, unit_name = resolve_unit_paths(args.vocab_dir)
    workspace_root = find_workspace_root(vocab_dir)

    print(f"[*] Processing Unit: {book_name} - {unit_name}")
    print(f"[*] Vocab Directory: {vocab_dir}")
    print(f"[*] Workspace Root:  {workspace_root}")

    # Load vocab.json
    vocab_json_path = vocab_dir / "vocab.json"
    vocab_data = []
    if vocab_json_path.exists():
        vocab_data = load_json(vocab_json_path) or []
        print(f"[+] Loaded vocab.json: {sum(len(g.get('words', [])) for g in vocab_data)} words in {len(vocab_data)} groups")
    else:
        print(f"[!] vocab.json not found in {vocab_dir}", file=sys.stderr)

    # Load exercises
    exercises_dir = vocab_dir / "exercises"
    exercises_data = []
    if exercises_dir.exists() and exercises_dir.is_dir():
        for jf in sorted(exercises_dir.glob("*.json")):
            data = load_json(jf)
            if data and isinstance(data, dict):
                data["_filename"] = jf.name
                exercises_data.append(data)
        print(f"[+] Loaded exercises: {len(exercises_data)} exercise files")
    else:
        print(f"[!] exercises directory not found in {vocab_dir}", file=sys.stderr)

    full_unit_title = f"{book_name} - {unit_name}"

    # Determine output destinations
    # We generate index.html and cards.html in:
    # 1. Workspace root (e.g. d:/GS12/index.html and d:/GS12/cards.html)
    # 2. Inside unit's vocab folder (e.g. lessons/unit-1/vocab/index.html and cards.html)
    root_index_path = workspace_root / "index.html"
    root_cards_path = workspace_root / "cards.html"
    unit_index_path = vocab_dir / "index.html"
    unit_cards_path = vocab_dir / "cards.html"

    if args.output_index:
        target_indices = [Path(args.output_index).resolve()]
    else:
        target_indices = [root_index_path, unit_index_path]

    if args.output_cards:
        target_cards = [Path(args.output_cards).resolve()]
    else:
        target_cards = [root_cards_path, unit_cards_path]

    # Generate cards.html
    for c_path in target_cards:
        c_path.parent.mkdir(parents=True, exist_ok=True)
        cards_html_content = build_vocab_cards_html_content(
            vocab_data=vocab_data,
            unit_title=full_unit_title,
            subtitle="Trực quan • Dễ ghi nhớ • Chuẩn phát âm",
            output_file=c_path,
            workspace_root=workspace_root
        )
        with open(c_path, "w", encoding="utf-8") as f:
            f.write(cards_html_content)
        print(f"[OK] Generated cards.html: {c_path}")

    # Generate index.html
    for i_path in target_indices:
        i_path.parent.mkdir(parents=True, exist_ok=True)
        index_html_content = build_unified_index_html(
            vocab_data=vocab_data,
            exercises_data=exercises_data,
            book_name=book_name,
            unit_name=unit_name,
            output_file=i_path,
            workspace_root=workspace_root
        )
        with open(i_path, "w", encoding="utf-8") as f:
            f.write(index_html_content)
        print(f"[OK] Generated index.html: {i_path}")

    print("\n[Done] Successfully generated all files!")


if __name__ == "__main__":
    main()
