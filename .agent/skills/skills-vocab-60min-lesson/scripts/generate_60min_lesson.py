#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 60-Minute Master Vocabulary Lesson Plan Script (Hyper-Detailed Pedagogy Edition)
Aligns strictly with d:/GS10/reference/method.md (Paul Nation, Michael Lewis, Task Involvement Load)
Parses vocab.json and exercises/*.json to produce an ultra-detailed, micro-scripted lesson plan
including Verbatim Teacher Talk, Physical Gestures, Student Actions, Board Layout Blueprint, and CCQs.
"""

import os
import sys
import json
import argparse
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kế Hoạch Bài Dạy 60 Phút Chi Tiết Sư Phạm: {unit_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #1e40af;
            --primary-dark: #1e3a8a;
            --primary-light: #eff6ff;
            --accent: #2563eb;
            --text-dark: #0f172a;
            --text-muted: #475569;
            --bg-light: #f8fafc;
            --border: #cbd5e1;
            --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
            --gold: #d97706;
            --green: #15803d;
            --red: #b91c1c;
            --purple: #7e22ce;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f1f5f9;
            color: var(--text-dark);
            line-height: 1.65;
            padding: 24px;
        }}

        .container {{
            max-width: 1140px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);
            color: #ffffff;
            padding: 44px 40px;
            position: relative;
        }}

        .header-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(10px);
            padding: 6px 16px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            margin-bottom: 14px;
            border: 1px solid rgba(255, 255, 255, 0.35);
        }}

        .header h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 30px;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }}

        .header p {{
            font-size: 15.5px;
            opacity: 0.92;
            max-width: 900px;
        }}

        .meta-bar {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 18px;
            background: #f8fafc;
            padding: 20px 40px;
            border-bottom: 1px solid var(--border);
        }}

        .meta-item strong {{
            color: var(--primary-dark);
            display: block;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }}

        .meta-item span {{
            font-size: 14.5px;
            color: #334155;
            font-weight: 500;
        }}

        .content {{
            padding: 40px;
        }}

        .section-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 21px;
            font-weight: 800;
            color: var(--primary-dark);
            margin: 36px 0 18px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-title:first-child {{
            margin-top: 0;
        }}

        .board-layout-box {{
            background: #0f172a;
            color: #f8fafc;
            border-radius: 12px;
            padding: 24px;
            margin: 20px 0 30px 0;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
            border: 2px solid #334155;
        }}

        .board-layout-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: #38bdf8;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .board-columns {{
            display: grid;
            grid-template-columns: 1fr 1.6fr 1fr;
            gap: 16px;
        }}

        @media (max-width: 860px) {{
            .board-columns {{
                grid-template-columns: 1fr;
            }}
        }}

        .board-col {{
            background: #1e293b;
            border: 1px dashed #475569;
            border-radius: 8px;
            padding: 14px;
            font-size: 13.5px;
            line-height: 1.55;
        }}

        .board-col h5 {{
            color: #facc15;
            font-size: 13.5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
            border-bottom: 1px solid #334155;
            padding-bottom: 4px;
        }}

        .board-col ul {{
            list-style: none;
            padding-left: 0;
        }}

        .board-col ul li {{
            margin-bottom: 6px;
        }}

        .timeline-card {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 14px;
            margin-bottom: 28px;
            box-shadow: var(--card-shadow);
            overflow: hidden;
        }}

        .timeline-header {{
            background: #f8fafc;
            padding: 18px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            flex-wrap: wrap;
            gap: 12px;
        }}

        .timeline-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 700;
            font-size: 17px;
            color: var(--primary-dark);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .time-pill {{
            background: var(--primary-dark);
            color: #ffffff;
            padding: 5px 12px;
            border-radius: 9999px;
            font-size: 13.5px;
            font-weight: 700;
        }}

        .involvement-badge {{
            background: #fef3c7;
            color: #92400e;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 700;
            border: 1px solid #fde68a;
        }}

        .timeline-body {{
            padding: 24px;
        }}

        .objective-box {{
            background: #eff6ff;
            border-left: 4px solid var(--accent);
            padding: 14px 18px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 20px;
            font-size: 14.5px;
        }}

        .objective-box strong {{
            color: var(--primary-dark);
        }}

        .action-step-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            margin-bottom: 18px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }}

        .action-step-header {{
            background: #f1f5f9;
            padding: 12px 18px;
            font-size: 15px;
            font-weight: 700;
            color: #1e293b;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e2e8f0;
        }}

        .action-step-time {{
            color: var(--accent);
            font-size: 13px;
            font-weight: 600;
            background: #ffffff;
            padding: 2px 10px;
            border-radius: 20px;
            border: 1px solid #cbd5e1;
        }}

        .action-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            padding: 16px 18px;
        }}

        @media (max-width: 800px) {{
            .action-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .teacher-side {{
            background: #f0fdf4;
            border-radius: 8px;
            padding: 14px;
            border: 1px solid #bbf7d0;
            font-size: 14px;
        }}

        .student-side {{
            background: #fdf4ff;
            border-radius: 8px;
            padding: 14px;
            border: 1px solid #f5d0fe;
            font-size: 14px;
        }}

        .side-title {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .teacher-side .side-title {{
            color: #15803d;
        }}

        .student-side .side-title {{
            color: #a21caf;
        }}

        .script-quote {{
            background: #ffffff;
            border-left: 3px solid #16a34a;
            padding: 8px 12px;
            margin: 8px 0;
            border-radius: 0 6px 6px 0;
            font-style: italic;
            color: #14532d;
            font-size: 13.5px;
        }}

        .gesture-note {{
            color: #b45309;
            font-size: 13px;
            margin-top: 6px;
            display: flex;
            align-items: flex-start;
            gap: 5px;
            background: #fffbeb;
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid #fef3c7;
        }}

        .student-action-box {{
            background: #ffffff;
            border-left: 3px solid #c026d3;
            padding: 8px 12px;
            margin: 8px 0;
            border-radius: 0 6px 6px 0;
            color: #701a75;
            font-size: 13.5px;
        }}

        .ccq-box {{
            background: #fffbeb;
            border: 1px solid #fde68a;
            border-radius: 8px;
            padding: 12px 16px;
            margin-top: 10px;
            font-size: 13.5px;
            color: #78350f;
        }}

        .ccq-box strong {{
            color: #b45309;
            display: block;
            margin-bottom: 4px;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}

        .vocab-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 14px;
            margin-top: 16px;
        }}

        .vocab-card {{
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            background: #ffffff;
            border-top: 4px solid var(--accent);
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}

        .vocab-word {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--primary-dark);
            margin-bottom: 2px;
        }}

        .vocab-ipa {{
            font-size: 13px;
            color: var(--accent);
            margin-bottom: 6px;
            font-weight: 500;
        }}

        .vocab-meaning {{
            font-size: 14px;
            color: #334155;
            margin-bottom: 8px;
        }}

        .vocab-collocation {{
            font-size: 13px;
            background: #f1f5f9;
            padding: 6px 10px;
            border-radius: 6px;
            color: #475569;
            line-height: 1.4;
        }}

        .rules-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
            font-size: 14px;
        }}

        .rules-table th, .rules-table td {{
            padding: 12px 16px;
            border: 1px solid var(--border);
            text-align: left;
        }}

        .rules-table th {{
            background: var(--bg-light);
            color: var(--primary-dark);
            font-weight: 700;
        }}

        .exit-ticket-card {{
            background: #ffffff;
            border: 2px dashed #94a3b8;
            border-radius: 12px;
            padding: 24px;
            margin-top: 16px;
        }}

        @media print {{
            body {{
                background: #ffffff;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                border: none;
                max-width: 100%;
            }}
            .timeline-card, .board-layout-box {{
                break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-badge">Ultra-Detailed Pedagogical Blueprint • 60-Minute Model</div>
            <h1>KẾ HOẠCH BÀI DẠY TỪ VỰNG CHI TIẾT: {unit_title}</h1>
            <p>Thiết kế sư phạm vi mô (Micro-Scripted): Lời nói nguyên văn, cử chỉ cơ thể, phản ứng của học viên và sơ đồ bảng chuẩn hóa.</p>
        </div>

        <div class="meta-bar">
            <div class="meta-item">
                <strong>Thời Lượng Tiết Học</strong>
                <span>60 Phút (01 tiết tiêu chuẩn BGD&ĐT)</span>
            </div>
            <div class="meta-item">
                <strong>Quy Mô Từ Vựng</strong>
                <span>{target_chunks_count} Target Lexical Chunks (Rule 80/20)</span>
            </div>
            <div class="meta-item">
                <strong>Phương Tiện & Học Liệu</strong>
                <span>cards.html, vocab.json, Bảng con, Exit Ticket</span>
            </div>
            <div class="meta-item">
                <strong>Chỉ Số Tải Trọng (Laufer)</strong>
                <span>Involvement Load: 2 &rarr; 5 (Mức Sản Sinh Sâu)</span>
            </div>
        </div>

        <div class="content">
            <h2 class="section-title">📐 1. Sơ Đồ Thiết Lập Lớp Học & Bố Cục Bảng (Board Layout Blueprint)</h2>
            <div class="board-layout-box">
                <div class="board-layout-title">
                    <span>🖥️ SƠ ĐỒ PHÂN BỔ BẢNG LỚP HỌC (3 CỘT TIÊU CHUẨN SUỐT 60 PHÚT)</span>
                </div>
                <div class="board-columns">
                    <div class="board-col">
                        <h5>CỘT TRÁI (LƯU ĐỘNG & SỬA LỖI)</h5>
                        <ul>
                            <li>• <strong>Odd-One-Out Blitz:</strong> Ghi từ lạc loài (e.g. <em>*do a decision</em> &rarr; <em>make a decision</em>).</li>
                            <li>• <strong>Spelling Traps:</strong> Phụ âm đôi, chữ cái câm (gạch chân mực đỏ: <em>breadwi<u>nn</u>er</em>).</li>
                            <li>• <strong>Delayed Feedback Board:</strong> Nơi GV ghi nhanh các lỗi ngữ điệu/collocation nghe được trong lúc HS nói tự do.</li>
                        </ul>
                    </div>
                    <div class="board-col">
                        <h5>CỘT GIỮA (TRỌNG TÂM DÀI HẠN)</h5>
                        <ul>
                            <li>• <strong>Tiêu đề:</strong> {unit_title_upper} - LEXICAL CHUNKS FOCUS.</li>
                            <li>• <strong>Collocation Grid 5-5-1 (Michael Lewis):</strong>
                                <br>&nbsp;&nbsp;[primary / sole / family] + <strong>BREADWINNER</strong>
                                <br>&nbsp;&nbsp;[do / share / split] + <strong>HOUSEWORK</strong>
                            </li>
                            <li>• <strong>Sentence Frames:</strong>
                                <br>&nbsp;&nbsp;<em>"In my family, [Person] is the primary breadwinner, while I [Action]."</em>
                            </li>
                            <li>• <strong>Word Family Matrix:</strong> Verb &harr; Noun &harr; Adjective.</li>
                        </ul>
                    </div>
                    <div class="board-col">
                        <h5>CỘT PHẢI (QUẢN TRỊ & NHIỆM VỤ)</h5>
                        <ul>
                            <li>• <strong>Timeline 60p:</strong> 5 Giai đoạn & đồng hồ đếm ngược.</li>
                            <li>• <strong>Bảng điểm thi đua nhóm:</strong> Group A / B / C / D (Stars / Points).</li>
                            <li>• <strong>Cascade 3-Part Exchange Model:</strong>
                                <br>&nbsp;&nbsp;1. A: Khởi xướng (Initiator)
                                <br>&nbsp;&nbsp;2. B: Phản hồi hướng mình [I-focus]
                                <br>&nbsp;&nbsp;3. A: Phản hồi hướng bạn [You-focus]
                            </li>
                            <li>• <strong>Exit Ticket Prompt:</strong> 3-2-1 Challenge.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <h2 class="section-title">🎯 2. Danh Sách Target Lexical Chunks Cốt Lõi (80/20 Rule)</h2>
            <p style="font-size: 14.5px; color: var(--text-muted); margin-bottom: 14px;">
                Được tuyển chọn theo tần suất sử dụng cao nhất, loại trừ triệt để hiện tượng nhiễm chéo ngữ nghĩa (Anti-Cross Association).
            </p>
            <div class="vocab-grid">
                {vocab_cards_html}
            </div>

            <h2 class="section-title">⏱️ 3. Kịch Bản Sư Phạm Vi Mô (Micro-Scripted 60-Minute Lesson Delivery)</h2>
            <p style="font-size: 14.5px; color: var(--text-muted); margin-bottom: 16px;">
                Chi tiết từng lời nói nguyên văn của Giáo viên (Teacher Talk), cử chỉ tay/cơ thể (Body Language), hành vi của Học viên và câu hỏi kiểm tra khái niệm (CCQs).
            </p>

            {stages_html}

            <h2 class="section-title">🎟️ 4. Phiếu Đánh Giá Quá Trình (Exit Ticket 3-2-1) & Cam Kết Pimsleur</h2>
            <div class="exit-ticket-card">
                <h4 style="font-size: 16px; font-weight: 700; color: var(--primary-dark); margin-bottom: 10px;">
                    PHIẾU EXIT TICKET 3-2-1 RETRIEVAL (THU 100% TẠI CỬA LỚP)
                </h4>
                <div style="font-size: 14px; color: #334155; line-height: 1.8;">
                    <strong>[Họ và tên học sinh]:</strong> .............................................................. <strong>[Lớp]:</strong> 10......<br>
                    <strong>3 Chunks:</strong> Ghi lại 3 cụm từ (collocations) em nhớ sâu sắc nhất và tự tin phát âm đúng nhất hôm nay:<br>
                    &nbsp;&nbsp;1. .....................................................................................................................................<br>
                    &nbsp;&nbsp;2. .....................................................................................................................................<br>
                    &nbsp;&nbsp;3. .....................................................................................................................................<br>
                    <strong>2 Sentences:</strong> Viết 2 câu hoàn chỉnh nói về sự thật của chính bản thân em có chứa 2 trong số các cụm từ trên:<br>
                    &nbsp;&nbsp;1. .....................................................................................................................................<br>
                    &nbsp;&nbsp;2. .....................................................................................................................................<br>
                    <strong>1 Trap:</strong> Ghi lại 1 bẫy chính tả (phụ âm đôi/chữ câm) hoặc 1 phát âm mà em cần cẩn thận để không mắc lỗi:<br>
                    &nbsp;&nbsp;• .....................................................................................................................................
                </div>
                <div class="teacher-talk" style="margin-top: 16px; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 12px 16px; border-radius: 8px; font-size: 13.5px; color: #166534;">
                    <strong>Hợp đồng lặp lại giãn cách Pimsleur tại nhà (Bắt buộc):</strong><br>
                    • <strong>Sau 24 giờ (Tối mai):</strong> Mở <code>cards.html</code>, dùng tay che cột nghĩa tiếng Việt, nhìn tranh và nghe audio để tự truy hồi mặt chữ và nghĩa (Active Recall).<br>
                    • <strong>Sau 7 ngày (Trước buổi học kế tiếp):</strong> Đăng nhập <code>index.html</code>, chọn chế độ <em>"Practice Mode"</em> để tự kiểm tra trắc nghiệm 10 câu.
                </div>
            </div>

            <h2 class="section-title">⚖️ 5. Tiêu Chí Giám Sát Sư Phạm (Observer's Quality Rubric)</h2>
            <table class="rules-table">
                <thead>
                    <tr>
                        <th>Tiêu Chí</th>
                        <th>Mức Đạt Chuẩn (Standard)</th>
                        <th>Mức Bậc Thầy Sư Phạm (Mastery)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Collocation First</strong></td>
                        <td>Dạy từ có kèm từ loại và nghĩa tiếng Việt.</td>
                        <td>100% từ mới nằm trong sơ đồ Collocation Grid 5-5-1, không có từ trần; học sinh nhận ra từ đối tác.</td>
                    </tr>
                    <tr>
                        <td><strong>Quy Trình 4 Bước & Mumble Drill</strong></td>
                        <td>Đi theo thứ tự Nghĩa &rarr; Âm &rarr; Chữ.</td>
                        <td>Thực hiện chuẩn 3s Mumble Drill; gõ nhịp trọng âm; highlight bẫy chính tả bằng phấn màu; CCQs sắc bén.</td>
                    </tr>
                    <tr>
                        <td><strong>Quản Trị Nhịp Độ (Pacing)</strong></td>
                        <td>Hoàn thành trong khoảng 55-65 phút.</td>
                        <td>Đúng chính xác từng phút theo 5 giai đoạn; chuyển giao hoạt động nhịp nhàng dưới 15 giây.</td>
                    </tr>
                    <tr>
                        <td><strong>Mức Độ Tương Tác (STT vs. TTT)</strong></td>
                        <td>Giáo viên hỏi, học sinh trả lời khi được gọi.</td>
                        <td>STT > 65% thời lượng; học sinh nói theo cặp tự nhiên bằng mắt; Involvement Load đạt Mức 5 ở Giai đoạn 4.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

def load_json_safe(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not read {path}: {e}")
        return None

def extract_target_words(vocab_data, max_words=8):
    all_words = []
    seen_words = set()
    antonyms_to_delay = set()

    for group in vocab_data:
        for w in group.get("words", []):
            eng = w.get("english_word", "").strip().lower()
            if not eng or eng in seen_words:
                continue
            ant = w.get("antonym", "").strip().lower()
            if eng in antonyms_to_delay:
                continue
            if ant:
                antonyms_to_delay.add(ant)
            seen_words.add(eng)
            all_words.append(w)
            if len(all_words) >= max_words:
                break
        if len(all_words) >= max_words:
            break
            
    return all_words

def generate_lesson_plan(unit_dir, output_md_path=None, output_html_path=None):
    unit_path = Path(unit_dir)
    vocab_json_path = unit_path / "vocab.json"
    if not vocab_json_path.exists():
        vocab_json_path = unit_path / "vocab" / "vocab.json"
    
    if not vocab_json_path.exists():
        print(f"Error: vocab.json not found in {unit_dir}")
        sys.exit(1)

    exercises_dir = vocab_json_path.parent / "exercises"
    vocab_data = load_json_safe(vocab_json_path)
    if not vocab_data:
        print("Error: Empty or invalid vocab.json")
        sys.exit(1)

    target_words = extract_target_words(vocab_data, max_words=8)
    
    unit_name = unit_path.name
    if unit_name == "vocab":
        unit_name = unit_path.parent.name
    unit_title = unit_name.replace("-", " ").title()

    # Load select exercises for specific stages
    ex_mcq_sentence = load_json_safe(exercises_dir / "02_multiple_choice_sentence.json") or {}
    ex_conversation = load_json_safe(exercises_dir / "03_multiple_choice_conversation.json") or {}
    ex_fill_blanks = load_json_safe(exercises_dir / "06_fill_in_blanks.json") or {}
    ex_word_families = load_json_safe(exercises_dir / "13_word_families_table.json") or {}
    ex_signs = load_json_safe(exercises_dir / "12_signs_and_notices.json") or {}
    ex_translation = load_json_safe(exercises_dir / "16_translate_sentences.json") or {}

    sample_sentence_q = ex_mcq_sentence.get("questions", [{}])[0] if ex_mcq_sentence.get("questions") else {}
    sample_conv_q = ex_conversation.get("questions", [{}])[0] if ex_conversation.get("questions") else {}
    sample_fill_q = ex_fill_blanks.get("questions", [{}])[0] if ex_fill_blanks.get("questions") else {}
    sample_sign_q = ex_signs.get("questions", [{}])[0] if ex_signs.get("questions") else {}
    sample_trans_q = ex_translation.get("questions", [{}])[0] if ex_translation.get("questions") else {}

    # Sample word for deep teaching
    primary_word_obj = target_words[0] if target_words else {}
    primary_word = primary_word_obj.get("english_word", "breadwinner")
    primary_ipa = primary_word_obj.get("pronunciation_british") or primary_word_obj.get("pronunciation_american") or "/ˈbredwɪnə/"
    primary_colloc = primary_word_obj.get("collocation", "primary breadwinner, sole breadwinner")

    # Build Stages with Micro-Scripted Details
    stages_data = [
        {
            "num": "GIAI ĐOẠN 1",
            "title": "Warm-up & Spaced Retrieval",
            "time": "00:00 - 00:07 (7 Phút)",
            "inv": "Involvement Load: 2 (Need=1, Search=0, Eval=1)",
            "objective": "Kích hoạt mạng lưới ngữ nghĩa (Spreading Activation), truy hồi chủ động (Active Recall) kiến thức cũ theo Pimsleur, tạo tâm thế học tập hứng khởi.",
            "steps": [
                {
                    "title": "Bước 1.1: Khởi Động & Ổn Định Năng Lượng (Energy Reset)",
                    "time": "00:00 - 00:01 (1 phút)",
                    "teacher_speech": "Good morning, class! Pens down, eyes on me. Take a deep breath. Today we have a high-energy mission: unlocking the secret language codes of real family life. Are you ready?",
                    "teacher_gesture": "Đứng ở vị trí trung tâm bục giảng (không đứng sau bàn GV), hai tay mở rộng hướng về cả lớp, mỉm cười tự tin, ánh mắt quét qua cả 4 góc phòng.",
                    "student_action": "100% học sinh đặt bút xuống bàn, ngồi thẳng lưng, hướng ánh mắt lên giáo viên, đồng thanh đáp: 'Yes, teacher! Ready!'",
                    "notes": "Tạo khoảng trống tĩnh lặng 3 giây trước khi phát lệnh để thu hút toàn bộ sự chú ý."
                },
                {
                    "title": "Bước 1.2: Odd-One-Out Collocation Blitz (Thử Thách Bảng Con)",
                    "time": "00:01 - 00:04 (3 phút)",
                    "teacher_speech": "Look at Screen 1! You see 3 groups of collocations. One combination in each row is an impostor. You have 15 seconds to write the non-collocate on your mini-boards. Silent thinking. Go! ... 3, 2, 1 - Boards UP! ... Row 2, Nam, why did you write 'a decision' with DO?",
                    "teacher_gesture": "Bấm clicker chuyển slide. Giơ ngón trỏ lên môi ra hiệu 'im lặng tuyệt đối'. Đi dọc lối đi giữa lớp quan sát. Khi đếm 3-2-1, hai tay hất dứt khoát lên cao. Chỉ lòng bàn tay mở về phía Nam.",
                    "student_action": "Học sinh suy nghĩ cá nhân trong im lặng (15s), viết từ sai lên bảng con bằng bút dạ. Nghe hiệu lệnh, đồng loạt giơ bảng ngang ngực. Học sinh Nam đứng dậy: 'Teacher, we say MAKE a decision, not DO a decision!'",
                    "teacher_speech_feedback": "Bingo! Spot on! 'Do housework', 'do laundry', but 'MAKE a decision'. 1 point for Team 2!",
                    "teacher_gesture_feedback": "Vỗ tay 2 nhịp dứt khoát, dùng phấn ghi nhanh cụm 'make a decision' lên Cột Trái (Delayed Feedback Board).",
                    "notes": "Kiểm tra phản xạ kết hợp từ tự nhiên (Lewis's Collocations), tránh học vẹt."
                },
                {
                    "title": "Bước 1.3: Visual Thematic Hook & Cognitive Priming (Mồi Ngữ Nghĩa)",
                    "time": "00:04 - 00:07 (3 phút)",
                    "teacher_speech": "Now, look at these two photos from our cards portal. Photo A: a father returning home tired with a heavy briefcase. Photo B: a family together in the kitchen washing dishes and laughing. Which life looks happier, and who carries the heavier load?",
                    "teacher_gesture": "Chuyển slide chiếu 2 ảnh từ cards.html. Hai tay đưa ra so sánh tựa như hai bàn cân trái - phải.",
                    "student_action": "Học sinh trao đổi thì thầm với bạn cùng bàn 10 giây. 3 học sinh xung phong giơ tay.",
                    "student_speech_sample": "Lan: 'Photo B is happier because they share the housework, but in Photo A the father is lonely earning money.'",
                    "teacher_speech_wrap": "Brilliant insight, Lan! To talk about the person who earns the family income, what special word do we use in English? Let's open our treasure box today!",
                    "teacher_gesture_wrap": "Cầm bút dạ đen viết tiêu đề lớn lên Cột Giữa trên bảng: UNIT 1: FAMILY LIFE - LEXICAL CHUNKS FOCUS.",
                    "notes": "Dẫn dắt trực tiếp vào nhu cầu giao tiếp (Cognitive Need)."
                }
            ]
        },
        {
            "num": "GIAI ĐOẠN 2",
            "title": "Language-Focused Learning: 4 Bước Khắc Sâu Chunks",
            "time": "00:07 - 00:25 (18 Phút)",
            "inv": "Involvement Load: 3 (Need=1, Search=0, Eval=2)",
            "objective": "Chiếm lĩnh 8 Target Lexical Chunks theo ma trận 9 khía cạnh (Paul Nation). Áp dụng triệt để Mumble Drill, sơ đồ Collocation Grid 5-5-1, loại bỏ Bathtub Effect & Semantic Interference.",
            "steps": [
                {
                    "title": "Bước 2.1: Meaning First & Bộ Câu Hỏi CCQs (Khái Niệm Trước Ký Tự)",
                    "time": "00:07 - 00:11 (4 phút)",
                    "teacher_speech": f"Look at this gentleman on cards.html. He works 10 hours a day. He buys food, pays electricity bills, and supports the whole family. He is the... (pauses). In English, we call this person a BREADWINNER. Let's check our understanding:",
                    "teacher_gesture": "Chỉ vào hình ảnh trực quan trên slide. Tay làm động tác mở ví tiền và che chở. Ánh mắt tò mò khích lệ học sinh đoán.",
                    "ccqs": [
                        {"q": "CCQ 1: Does a breadwinner stay home all day or work to earn money?", "a": "Works to earn money!", "action": "GV nghiêng người lắng nghe, HS đồng thanh đáp dứt khoát."},
                        {"q": "CCQ 2: Can a mother or a wife be the breadwinner of the family?", "a": "Yes, absolutely!", "action": "GV gật đầu khích lệ: 'Exactly, in modern society both can be.'"},
                        {"q": "CCQ 3: If a family has ONLY ONE person earning money, what word do we add?", "a": "Sole breadwinner / Primary breadwinner.", "action": "GV đưa 1 ngón tay lên mô phỏng tính duy nhất."}
                    ],
                    "student_action": "Học sinh nhìn hình, tư duy theo kịch bản tình huống, trả lời nhanh các câu CCQs, không dịch thô từng chữ.",
                    "notes": "Tuyệt đối không đưa mặt chữ tiếng Anh ra trước khi CCQs được thông qua."
                },
                {
                    "title": "Bước 2.2: Spoken Form & Kỹ Thuật Mumble Drill (Đọc Bằng Tai)",
                    "time": "00:11 - 00:16 (5 phút)",
                    "teacher_speech": f"Now, eyes on me, lips closed! Listen to the natural stress rhythm twice: '{primary_ipa}' ... '{primary_ipa}'. Notice where the beat drops: BREAD-win-ner! Now, MUMBLE DRILL! 3 seconds. Do NOT make any sound. Move your lips and feel the stress inside your head. 3... 2... 1...",
                    "teacher_gesture": "Đưa tay lên vành tai ra hiệu lắng nghe. Tay phải vỗ nhẹ nhịp vào đùi ở âm tiết trọng âm /ˈbred/. Khi ra lệnh Mumble, đặt ngón trỏ lên môi làm hiệu im lặng, miệng GV cử động nhẩm chậm rãi làm mẫu.",
                    "student_action": "Cả lớp im lặng tuyệt đối trong 3 giây. Môi và cơ miệng cử động nhẩm theo nhịp trọng âm /ˈbredwɪnər/, cảm nhận âm thanh nội tâm.",
                    "teacher_speech_drill": "Everyone together, with full energy: BREADWINNER!",
                    "teacher_gesture_drill": "Hai tay mở rộng hất lên như nhạc trưởng bắt nhịp đồng thanh (Choral).",
                    "student_action_drill": "100% học sinh đồng thanh: 'BREADWINNER!' (nhấn mạnh trọng âm đầu).",
                    "teacher_speech_individual": "Row 3, Minh, pronounce it please!",
                    "student_speech_individual": "Minh: '/ˈbredwɪnər/'.",
                    "teacher_feedback_technique": "Nếu học sinh phát âm thiếu âm cuối hoặc sai trọng âm, GV dùng kỹ thuật Finger Correction: Giơ 3 ngón tay (tượng trưng 3 âm tiết), chạm vào ngón thứ nhất để nhắc HS tự sửa. Khen: 'Crystal clear! Excellent!'",
                    "notes": "Loại trừ triệt để Bathtub Effect (học sinh hay nuốt âm tiết giữa hoặc mất trọng âm)."
                },
                {
                    "title": "Bước 2.3: Written Form & Cảnh Báo Bẫy Chính Tả (Spelling Traps)",
                    "time": "00:16 - 00:20 (4 phút)",
                    "teacher_speech": "Now look at the board as I write the word. Notice the spelling trap: The vowel sound is /e/, but it is written with 'EA' (like 'bread'). And look at the middle: DOUBLE 'N' (winner)! If you write one 'n', it's a spelling crime! Take your Lexical Notebooks, write the word and underline the double 'n'.",
                    "teacher_gesture": "Cầm bút dạ đen viết nắn nót từ 'breadwinner' lên Cột Giữa. Cầm bút dạ đỏ gạch chân 2 đường dưới cặp chữ 'ea' và khoanh tròn 'nn'. Đi vòng quanh lớp kiểm tra tập vở.",
                    "student_action": "Học sinh mở sổ tay từ vựng, nắn nót viết từ 'breadwinner', dùng bút highlight hoặc bút đỏ đánh dấu bẫy chính tả theo mẫu trên bảng.",
                    "notes": "Hình thành trí nhớ thị giác chuẩn xác (Orthographic Mapping)."
                },
                {
                    "title": "Bước 2.4: Collocation Grid 5-5-1 & Personalised Micro-Sentence",
                    "time": "00:20 - 00:25 (5 phút)",
                    "teacher_speech": "Golden Rule #2: Never learn an isolated word! Look at the Collocation Grid on the board. We combine BREADWINNER with: primary, sole, family. And look at HOUSEWORK: we DO housework, SHARE housework, HELP WITH housework. Now, 60-Second Personal Challenge! Write 1 TRUE sentence about your family using the frame on the board: 'In my family, [Person] is the primary breadwinner, while I usually [Action].' Go!",
                    "teacher_gesture": "Vẽ nhánh sơ đồ 5-5-1 lên bảng. Chỉ tay vào khung câu bán cố định (Sentence Frame). Vỗ tay 1 nhịp, bấm đồng hồ đếm ngược 60 giây. Cúi xuống đọc bài của 2 bạn gần nhất.",
                    "student_action": "Học sinh suy nghĩ và viết câu thật của chính mình vào vở trong 60 giây.",
                    "student_speech_sample": "Hà: 'In my family, my father is the sole breadwinner, while my mother and I share the household chores.'",
                    "teacher_speech_praise": "Marvelous, Hà! 'Sole breadwinner' and 'share household chores' - you used two powerful chunks in one sentence!",
                    "notes": "Đạt độ sâu cảm xúc (Affective Depth) khi gắn từ vựng vào đời thực của người học."
                }
            ]
        },
        {
            "num": "GIAI ĐOẠN 3",
            "title": "Controlled Practice: Thang Bậc Nhận Thức",
            "time": "00:25 - 00:40 (15 Phút)",
            "inv": "Involvement Load: 3-4 (Need=2, Search=0, Eval=1~2)",
            "objective": "Vận hành nhận thức qua 3 tầng bậc: Identifying (Nhận diện) &rarr; Selecting (Lựa chọn) &rarr; Sorting (Phân loại họ từ). Khai thác ngân hàng bài tập 16 dạng.",
            "steps": [
                {
                    "title": "Bước 3.1: Speed Collocation & Clue Underlining (Think-Pair-Share)",
                    "time": "00:25 - 00:31 (6 phút)",
                    "teacher_speech": "Open Handout Page 1 (Exercise 2 & 6). We have 4 questions on screen. Mandatory Rule: You cannot just guess A, B, C, or D! You MUST circle the 'Partner Clue' in the sentence that demands that word. 60 seconds pair discussion with your shoulder partner. Go!",
                    "teacher_gesture": "Chuyển slide chiếu 4 câu hỏi trắc nghiệm ngữ cảnh. Hai tay đan vào nhau mô phỏng làm việc cặp đôi. Di chuyển quanh phòng lắng nghe các cặp trao đổi.",
                    "student_action": "Hai học sinh cùng bàn quay sang nhau, dùng bút chì gạch chân từ khóa đi kèm trong câu đề (ví dụ: gạch chân 'lifting' để chọn 'heavy'; gạch chân 'rubbish' để chọn 'put out').",
                    "student_speech_sample": "Cặp Nam & Đức: 'In Question 1, the clue is \"lifting\", so the collocate must be \"heavy\" &rarr; do the heavy lifting!'",
                    "teacher_speech_confirm": "Exactly right! 'Lifting' demands 'heavy'. That is how native speakers think in chunks!",
                    "notes": "Huấn luyện học sinh kỹ năng dò tìm đối tác kết hợp từ (Collocation Partner)."
                },
                {
                    "title": "Bước 3.2: Morphology & Word Family Matrix (Giảm Tải Nhận Thức)",
                    "time": "00:31 - 00:36 (5 phút)",
                    "teacher_speech": "Look at the Family Tree on the board from Exercise 13. One root word generates 3 members! Fill in the missing boxes in 90 seconds: Verb [support] &rarr; Noun (Person) [?] &rarr; Adjective [?]. Ready, set, write!",
                    "teacher_gesture": "Chỉ vào bảng 3 cột kẻ sẵn trên Cột Giữa. Đưa tay vẽ hình cây gia đình tỏa nhánh.",
                    "student_action": "Học sinh điền nhanh vào bảng: support &rarr; supporter &rarr; supportive; responsible &rarr; responsibility.",
                    "teacher_speech_deconstruct": "Notice the suffixes: '-er' makes a person who does the action, '-ive' creates a character adjective, and '-ility' builds an abstract noun. When you master 1 root, you conquer 3 words at once!",
                    "notes": "Ứng dụng lý thuyết Word Family của Paul Nation giúp giảm learning burden gấp 3 lần."
                },
                {
                    "title": "Bước 3.3: Real-World Pragmatics / Signs & Notices (Ngữ Vực Đời Thực)",
                    "time": "00:36 - 00:40 (4 phút)",
                    "teacher_speech": "Look at Screen 3 (Exercise 12): A notice on an apartment noticeboard: 'PLEASE PUT OUT THE RUBBISH BEFORE 8 P.M. AND SEPARATE RECYCLABLES.' Who wrote this, and where do you see it in real life?",
                    "teacher_gesture": "Đưa tay làm động tác đọc thông báo dán trước cửa thang máy chung cư.",
                    "student_action": "Học sinh suy nghĩ 15s. Học sinh Tuấn giơ tay: 'Teacher, it's from the building management to all residents.'",
                    "teacher_speech_register": "Spot on. The tone is formal and polite. Look at the phrasal verb: 'put out the rubbish' - natural everyday English, not textbook robotic language.",
                    "notes": "Nâng cao nhận thức về văn phong và ngữ vực (Register & Constraints on Use)."
                }
            ]
        },
        {
            "num": "GIAI ĐOẠN 4",
            "title": "Meaning-Focused Output & Communicative Fluency",
            "time": "00:40 - 00:54 (14 Phút)",
            "inv": "Involvement Load: 5 (Need=2, Search=1, Eval=2)",
            "objective": "Đạt đỉnh tháp nhận thức Mức 3 (Involvement Load = 5). Chuyển hóa toàn diện từ vốn từ thụ nhận sang sản sinh tự do, tự động hóa độ lưu loát trong hội thoại.",
            "steps": [
                {
                    "title": "Bước 4.1: Cascade 3-Part Exchange (Khung Hội Thoại 3 Lượt)",
                    "time": "00:40 - 00:46 (6 phút)",
                    "teacher_speech": "Michael Lewis taught us that conversation flows in prefabricated chunks. Look at this Cascade 3-Part Exchange model on Cột Phải: Partner A initiates with a problem; Partner B responds focusing on themself [I-focus]; Partner A follows up focusing on Partner B [You-focus]. Let's demonstrate with Huy!",
                    "teacher_gesture": "Mời học sinh Huy đứng lên trước lớp. GV đóng vai A, nét mặt bận rộn chỉ vào đống đồ tưởng tượng trên bàn: 'The living room is completely cluttered with laundry!' Huy đáp: 'Don't worry, Mom. I'll fold the clothes right now.' GV mỉm cười cảm ơn: 'Thanks a million! Could you also help me do the washing-up later?'",
                    "teacher_speech_command": "Stand up, everyone! Face your partner. Rule: NO reading from paper! Look into each other's eyes. You have 3 minutes to perform 2 exchanges. Swap roles after 90 seconds. Speak with real emotion! Go!",
                    "teacher_gesture_command": "Vỗ tay 2 nhịp dứt khoát. Đi vòng quanh lớp lắng nghe, KHÔNG ngắt lời học sinh. Cầm sổ tay sư phạm ghi nhanh các lỗi phát âm hoặc collocations bị vấp để sửa ở cuối giờ.",
                    "student_action": "100% học sinh đứng dậy, quay mặt vào nhau, ánh mắt biểu cảm, cử chỉ tự nhiên, luân phiên đóng vai A và B thực hành đối thoại theo khung.",
                    "notes": "Rèn luyện phản xạ khối ngữ lưu và ngữ điệu tự nhiên (Interactive Talk)."
                },
                {
                    "title": "Bước 4.2: Communicative Task: '1-Minute Fluency Pitch' (Bảng Phân Công Gia Đình)",
                    "time": "00:46 - 00:54 (8 phút)",
                    "teacher_speech": "Final Communicative Mission! In groups of 3, create a 60-second 'Family Chore Charter' for a modern Vietnamese family. Condition: You MUST use at least 3 target chunks from today (breadwinner, share housework, heavy lifting, do the cooking, laundry). You have 3 minutes to brainstorm and assign roles. Go!",
                    "teacher_gesture": "Chỉ vào đồng hồ đếm ngược 3 phút trên slide. GV lùi về cuối phòng học để nhường không gian làm chủ cho học sinh thảo luận.",
                    "student_action": "Học sinh chụm đầu nhóm 3, thảo luận sôi nổi, ghi nhanh dàn ý các chunks cần sử dụng vào giấy nháp.",
                    "teacher_speech_pitch": "Time is up! Group 2, the stage is yours! 60 seconds on the clock. Action!",
                    "student_speech_pitch": "Đại diện Group 2: 'In our modern family charter, both father and mother are equal breadwinners. Therefore, they share the housework equally. The son is responsible for doing the heavy lifting and putting out the rubbish, while the daughter does the washing-up. Sharing chores makes our family happier and stronger!'",
                    "teacher_feedback_pitch": "Give Group 2 a resounding round of applause! Excellent delivery, seamless chunks, and zero hesitation on 'equal breadwinners'!",
                    "teacher_gesture_pitch": "Vỗ tay nhiệt liệt khích lệ cả lớp vỗ tay theo.",
                    "notes": "Đạt chỉ số Task Involvement Load tối đa = 5 (Need=2, Search=1, Evaluation=2)."
                }
            ]
        },
        {
            "num": "GIAI ĐOẠN 5",
            "title": "Wrap-up, Assessment & Spaced Contract",
            "time": "00:54 - 01:00 (6 Phút)",
            "inv": "Involvement Load: 4 (Need=2, Search=0, Eval=2)",
            "objective": "Đánh giá quá trình cá nhân (Formative Assessment) theo thang VKS; sửa lỗi trì hoãn (Delayed Feedback); thiết lập hợp đồng lặp lại giãn cách Pimsleur.",
            "steps": [
                {
                    "title": "Bước 5.1: Formative Assessment - Exit Ticket 3-2-1 Retrieval Challenge",
                    "time": "00:54 - 00:58 (4 phút)",
                    "teacher_speech": "Pens in hand! Look at your Exit Ticket slips. You have 3 minutes of absolute silence to complete the 3-2-1 Challenge: 3 collocations you remember best today, 2 true sentences about your life, and 1 spelling or pronunciation trap you must avoid. No books, no chatting. Pure active recall. Go!",
                    "teacher_gesture": "Phát phiếu Exit Ticket đến từng dãy bàn (hoặc học sinh lấy phiếu có sẵn). Đứng nghiêm túc quan sát giữ không khí im lặng tuyệt đối (Silent Reflection).",
                    "student_action": "100% học sinh tập trung làm việc độc lập, tự lực truy hồi kiến thức từ bộ nhớ dài hạn, không nhìn tài liệu, điền vào phiếu.",
                    "notes": "Đo lường chính xác tỷ lệ chuyển hóa từ vựng của từng học sinh (VKS Levels 4-5)."
                },
                {
                    "title": "Bước 5.2: Delayed Error Feedback & Spaced Retrieval Contract (Lịch Pimsleur)",
                    "time": "00:58 - 01:00 (2 phút)",
                    "teacher_speech": "Stop writing. Pass your slips to the aisle right now. While I collect them, look at the Left Board! During our fluency pitch, I noticed two tiny slips: someone said 'do a decision' and wrote 'breadwiner with one n'. Let's correct it together: MAKE a decision, and DOUBLE 'N' in breadwinner! Great job catching that!",
                    "teacher_gesture": "Thu các phiếu Exit Ticket. Dùng phấn đỏ gõ nhẹ vào Cột Trái trên bảng, mỉm cười ấm áp khích lệ cả lớp.",
                    "teacher_speech_contract": "Now, our solemn contract with memory science: If you do not review, 80% will vanish in 24 hours. Your mission: Tomorrow evening, open cards.html, cover the Vietnamese with your hand, and test your recall. Before our next lesson, complete the Practice Mode test on index.html. Thank you for your incredible energy today. Class dismissed!",
                    "teacher_gesture_contract": "Cúi đầu chào nhẹ, mỉm cười, đứng ở cửa lớp thu nốt các phiếu Exit Ticket khi học sinh bước ra.",
                    "student_action": "Học sinh thu dọn đồ dùng, nộp phiếu Exit Ticket tận tay giáo viên, đồng thanh: 'Thank you and goodbye, teacher!'",
                    "notes": "Chặn đứng đường cong quên lãng Ebbinghaus bằng cam kết hành động cụ thể."
                }
            ]
        }
    ]

    # Build HTML Content
    vocab_cards_html = []
    for w in target_words:
        word = w.get("english_word", "")
        ipa = w.get("pronunciation_british") or w.get("pronunciation_american") or ""
        meaning = w.get("vietnamese_meaning", "")
        colloc = w.get("collocation", "N/A")
        card = f"""
        <div class="vocab-card">
            <div class="vocab-word">{word}</div>
            <div class="vocab-ipa">{ipa}</div>
            <div class="vocab-meaning">{meaning}</div>
            <div class="vocab-collocation"><strong>Collocation:</strong> {colloc}</div>
        </div>
        """
        vocab_cards_html.append(card)

    stages_html = []
    for s in stages_data:
        steps_html = []
        for step in s["steps"]:
            # Format CCQs if any
            ccqs_markup = ""
            if "ccqs" in step:
                ccq_items = []
                for c in step["ccqs"]:
                    ccq_items.append(f"<li><strong>{c['q']}</strong> &rarr; <em>Đáp án: {c['a']}</em> ({c['action']})</li>")
                ccqs_markup = f"""
                <div class="ccq-box">
                    <strong>Bộ Câu Hỏi Kiểm Tra Khái Niệm (Concept Checking Questions - CCQs):</strong>
                    <ul style="margin-left: 18px; margin-top: 4px;">
                        {"".join(ccq_items)}
                    </ul>
                </div>
                """

            feedback_markup = ""
            if "teacher_speech_feedback" in step:
                feedback_markup = f"""
                <div class="script-quote" style="border-left-color: #0284c7; color: #0369a1; margin-top: 6px;">
                    <strong>GV phản hồi:</strong> "{step['teacher_speech_feedback']}"
                </div>
                <div class="gesture-note">
                    <span>💡</span> <strong>Cử chỉ phản hồi:</strong> {step['teacher_gesture_feedback']}
                </div>
                """

            student_speech_markup = ""
            if "student_speech_sample" in step:
                student_speech_markup = f"""
                <div class="student-action-box" style="margin-top: 6px;">
                    <strong>Lời thoại HV mẫu:</strong> "{step['student_speech_sample']}"
                </div>
                """

            step_card = f"""
            <div class="action-step-card">
                <div class="action-step-header">
                    <span>{step["title"]}</span>
                    <span class="action-step-time">{step["time"]}</span>
                </div>
                <div class="action-grid">
                    <div class="teacher-side">
                        <div class="side-title">👨‍🏫 HOẠT ĐỘNG & LỜI THOẠI GIÁO VIÊN (TEACHER TALK)</div>
                        <div class="script-quote">
                            <strong>GV nói (nguyên văn):</strong> "{step["teacher_speech"]}"
                        </div>
                        <div class="gesture-note">
                            <span>🎭</span> <strong>Cử chỉ & Hành động GV:</strong> {step["teacher_gesture"]}
                        </div>
                        {feedback_markup}
                    </div>
                    <div class="student-side">
                        <div class="side-title">🧑‍🎓 PHẢN ỨNG & HÀNH VI HỌC VIÊN (STUDENT ACTION)</div>
                        <div class="student-action-box">
                            <strong>HV thực hiện:</strong> {step["student_action"]}
                        </div>
                        {student_speech_markup}
                        <div style="font-size: 12.5px; color: #64748b; margin-top: 8px; font-style: italic;">
                            📌 <strong>Mục tiêu vi mô:</strong> {step.get("notes", "")}
                        </div>
                    </div>
                </div>
                {ccqs_markup}
            </div>
            """
            steps_html.append(step_card)

        stage_card = f"""
        <div class="timeline-card">
            <div class="timeline-header">
                <div class="timeline-title">
                    <span class="time-pill">{s["time"]}</span>
                    <span>{s["num"]}: {s["title"]}</span>
                </div>
                <div class="involvement-badge">{s["inv"]}</div>
            </div>
            <div class="timeline-body">
                <div class="objective-box">
                    <strong>Mục tiêu sư phạm trọng tâm:</strong> {s["objective"]}
                </div>
                {"".join(steps_html)}
            </div>
        </div>
        """
        stages_html.append(stage_card)

    html_content = HTML_TEMPLATE.format(
        unit_title=unit_title,
        unit_title_upper=unit_title.upper(),
        target_chunks_count=len(target_words),
        vocab_cards_html="".join(vocab_cards_html),
        stages_html="".join(stages_html)
    )

    # Build Markdown Content
    md_lines = []
    md_lines.append(f"# KẾ HOẠCH BÀI DẠY TỪ VỰNG CHI TIẾT (60 PHÚT): {unit_title.upper()}")
    md_lines.append(f"> **Thiết kế Sư phạm Vi mô (Micro-Scripted):** Lời nói nguyên văn (Teacher Talk), Cử chỉ cơ thể, Phản ứng học viên, Sơ đồ bảng 3 cột.")
    md_lines.append(f"> **Phương pháp luận:** Paul Nation (Four Strands), Michael Lewis (Lexical Approach), Task Involvement Load (Laufer).\n")
    md_lines.append(f"- **Thời lượng:** 60 phút (01 tiết tiêu chuẩn)")
    md_lines.append(f"- **Quy mô từ vựng:** {len(target_words)} Target Lexical Chunks (Rule 80/20)")
    md_lines.append(f"- **Học liệu tích hợp:** `vocab.json`, `cards.html`, `exercises/*.json`, Bảng con, Phiếu Exit Ticket 3-2-1\n")
    md_lines.append("---\n")

    md_lines.append("## 1. SƠ ĐỒ PHÂN BỔ BẢNG LỚP HỌC (BOARD LAYOUT BLUEPRINT)")
    md_lines.append("```")
    md_lines.append("+---------------------------+-----------------------------------+-----------------------------+")
    md_lines.append("| CỘT TRÁI (LƯU ĐỘNG)       | CỘT GIỮA (TRỌNG TÂM DÀI HẠN)      | CỘT PHẢI (NHIỆM VỤ & QUẢN LÝ)|")
    md_lines.append("| - Odd-One-Out Blitz       | UNIT 1: FAMILY LIFE - LEXIS       | - Timeline 60p (5 Stages)   |")
    md_lines.append("| - Spelling Traps:         | 1. Collocation Grid 5-5-1:        | - Bảng điểm thi đua nhóm    |")
    md_lines.append("|   breadwinner (double n)  |    [sole / primary] + BREADWINNER | - Khung Cascade 3 Lượt:     |")
    md_lines.append("| - Delayed Feedback Board: |    [do / share] + HOUSEWORK       |   A: Initiator              |")
    md_lines.append("|   (make a decision)       | 2. Sentence Frame:                |   B: I-focus                |")
    md_lines.append("|                           |    'In my family, ... while ...'  |   A: You-focus              |")
    md_lines.append("|                           | 3. Word Family:                   | - Exit Ticket 3-2-1         |")
    md_lines.append("|                           |    support -> supporter -> ...    | - Hợp đồng Pimsleur 24h & 7d|")
    md_lines.append("+---------------------------+-----------------------------------+-----------------------------+")
    md_lines.append("```\n---\n")

    md_lines.append("## 2. DANH SÁCH TARGET LEXICAL CHUNKS TRỌNG TÂM")
    md_lines.append("| STT | Cụm từ (Lexical Chunk) | Phát âm (IPA) | Nghĩa tiếng Việt | Kết hợp từ tự nhiên (Collocations) |")
    md_lines.append("|---|---|---|---|---|")
    for idx, w in enumerate(target_words, 1):
        word = w.get("english_word", "")
        ipa = w.get("pronunciation_british") or w.get("pronunciation_american") or ""
        meaning = w.get("vietnamese_meaning", "")
        colloc = w.get("collocation", "N/A")
        md_lines.append(f"| {idx} | **{word}** | `{ipa}` | {meaning} | *{colloc}* |")
    md_lines.append("\n---\n")

    md_lines.append("## 3. TIẾN TRÌNH SƯ PHẠM VI MÔ CHI TIẾT (60 PHÚT)\n")
    for s in stages_data:
        md_lines.append(f"### {s['num']}: {s['title']} ({s['time']})")
        md_lines.append(f"- **Mục tiêu nhận thức:** {s['objective']}")
        md_lines.append(f"- **Chỉ số Tác vụ:** {s['inv']}\n")
        for step in s["steps"]:
            md_lines.append(f"#### {step['title']} ({step['time']})")
            md_lines.append(f"- **Lời nói GV (Teacher Talk nguyên văn):** *\"{step['teacher_speech']}\"*")
            md_lines.append(f"- **Cử chỉ & Hành động GV:** {step['teacher_gesture']}")
            md_lines.append(f"- **Hành động của Học viên:** {step['student_action']}")
            if "student_speech_sample" in step:
                md_lines.append(f"- **Lời nói HV mẫu:** *\"{step['student_speech_sample']}\"*")
            if "ccqs" in step:
                md_lines.append("- **Bộ câu hỏi kiểm tra khái niệm (CCQs):**")
                for c in step["ccqs"]:
                    md_lines.append(f"  - *{c['q']}* $\\rightarrow$ **Đáp án:** {c['a']} ({c['action']})")
            if "notes" in step:
                md_lines.append(f"- **Mục tiêu vi mô:** {step['notes']}")
            md_lines.append("")
        md_lines.append("---\n")

    md_lines.append("## 4. PHIẾU ĐÁNH GIÁ QUÁ TRÌNH (EXIT TICKET 3-2-1) & LỊCH PIMSLEUR")
    md_lines.append("1. **3 Chunks:** Ghi lại 3 cụm từ em nhớ sâu sắc nhất và tự tin phát âm đúng nhất hôm nay.")
    md_lines.append("2. **2 Sentences:** Viết 2 câu hoàn chỉnh nói về sự thật của chính bản thân em có chứa 2 cụm từ trên.")
    md_lines.append("3. **1 Trap:** Ghi lại 1 bẫy chính tả (phụ âm đôi/chữ câm) hoặc phát âm mà em cần đặc biệt lưu ý.")
    md_lines.append("\n**Hợp đồng lặp lại giãn cách Pimsleur:**")
    md_lines.append("- **Sau 24 giờ:** Mở `cards.html`, che nghĩa tiếng Việt, nhìn tranh và nghe audio để tự truy hồi mặt chữ.")
    md_lines.append("- **Sau 7 ngày:** Vào `index.html` chọn Practice Mode hoàn thành 10 câu trắc nghiệm.\n")

    md_content = "\n".join(md_lines)

    # Save output files
    if not output_md_path:
        output_md_path = unit_path / "lesson_plan_60min.md"
    if not output_html_path:
        output_html_path = unit_path / "lesson_plan_60min.html"

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Generated Markdown lesson plan: {output_md_path}")

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML lesson plan: {output_html_path}")

    return output_md_path, output_html_path

def main():
    parser = argparse.ArgumentParser(description="Generate Hyper-Detailed 60-Minute Master Vocabulary Lesson Plan")
    parser.add_argument("unit_dir", help="Path to unit directory containing vocab.json and exercises")
    parser.add_argument("--output-md", "-om", help="Custom output Markdown file path")
    parser.add_argument("--output-html", "-oh", help="Custom output HTML file path")

    args = parser.parse_args()
    generate_lesson_plan(args.unit_dir, args.output_md, args.output_html)

if __name__ == "__main__":
    main()
