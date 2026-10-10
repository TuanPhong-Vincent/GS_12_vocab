#!/usr/bin/env python3
"""
Export Unit Test JSON to Markdown format (both Teacher GV and Student HS versions).
Usage:
  python export_test_markdown.py <path_to_test.json> [--gv] [--hs] [--out-dir <dir>]
"""

import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def render_test_markdown(test_data, is_gv=True):
    lines = []
    
    title = test_data.get("title", "UNIT TEST")
    u_num = test_data.get("unit_number", 1)
    u_title = test_data.get("unit_title", "Unit")
    t_id = test_data.get("test_id", "test_1").upper()
    role_str = "GIÁO VIÊN (CÓ ĐÁP ÁN & GIẢI THÍCH CHI TIẾT)" if is_gv else "HỌC SINH (ĐỀ BÀI LUYỆN TẬP)"
    
    lines.append(f"# {title} - {'GV' if is_gv else 'HS'}")
    lines.append(f"> **Tài liệu:** {role_str}  ")
    lines.append(f"> **Thời gian làm bài:** {test_data.get('duration_minutes', 50)} phút | **Số lượng:** 40 câu trắc nghiệm  ")
    lines.append(f"> **Định dạng:** Chuẩn cấu trúc Đề thi tốt nghiệp THPT từ năm 2025")
    lines.append("\n---\n")
    
    # Render sections
    sections = test_data.get("sections", [])
    questions = {q["question_number"]: q for q in test_data.get("questions", [])}
    
    for sec in sections:
        q_start, q_end = sec.get("questions_range", [1, 40])
        lines.append(f"\n---\n\n### {sec.get('instruction', '')}\n")
        
        # Passage title & text
        p_title = sec.get("passage_title", "")
        if p_title:
            lines.append(f"**{p_title}**\n")
            
        p_text = sec.get("passage_text", "")
        if p_text:
            lines.append(f"{p_text}\n")
            
        # Questions in this section
        for q_num in range(q_start, q_end + 1):
            if q_num not in questions:
                continue
            q = questions[q_num]
            prompt = q.get("prompt", f"Question {q_num}:")
            options = q.get("options", {})
            ca = q.get("correct_answer", "")
            # Options line
            opts_parts = []
            for lbl in ["A", "B", "C", "D"]:
                if lbl in options:
                    val = options[lbl]
                    if is_gv and lbl == ca:
                        opts_parts.append(f"**{lbl}. {val}**")
                    else:
                        opts_parts.append(f"**{lbl}.** {val}")
                        
            # Check length of options to decide inline vs multiline
            total_opts_len = sum(len(p) for p in opts_parts)

            # Format question line
            if "\n" in prompt:
                p_lines = prompt.split("\n")
                first = p_lines[0]
                rest = p_lines[1:]
                prompt_line = (f"**{first}**" if not first.startswith("**") else first) + "\n\n" + "\n\n".join(rest)
                lines.append(prompt_line)
                if total_opts_len < 80:
                    lines.append("    ".join(opts_parts))
                else:
                    for p in opts_parts:
                        lines.append(p)
            else:
                prompt_line = f"**{prompt}**" if not prompt.startswith("**") else prompt
                if total_opts_len < 80:
                    lines.append(f"{prompt_line}    " + "    ".join(opts_parts))
                else:
                    lines.append(prompt_line)
                    for p in opts_parts:
                        lines.append(p)
                    
            # If GV, include explanation & translation
            if is_gv:
                expl = q.get("explanation", {})
                k_type = expl.get("knowledge_type", "Kiến thức bài thi")
                lines.append(f"\n**Giải Thích:** {k_type}")
                
                analysis = expl.get("analysis", {})
                for k, v in analysis.items():
                    lines.append(f"**{k}.** {v}")
                    
                vi_trans = q.get("vietnamese_translation", "")
                if vi_trans:
                    lines.append(f"**Tạm Dịch:** {vi_trans}")
                    
            lines.append("")
            
    content = "\n\n".join(l for l in lines if l.strip())
    return content

def export_test(json_path, out_dir=None):
    path = Path(json_path)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    out_folder = Path(out_dir) if out_dir else path.parent
    out_folder.mkdir(parents=True, exist_ok=True)
    
    stem = path.stem
    # Export GV
    gv_md = render_test_markdown(data, is_gv=True)
    gv_path = out_folder / f"{stem}_GV.md"
    gv_path.write_text(gv_md, encoding='utf-8')
    print(f"✓ Exported Teacher Markdown: {gv_path} ({len(gv_md):,} chars)")
    
    # Export HS
    hs_md = render_test_markdown(data, is_gv=False)
    hs_path = out_folder / f"{stem}_HS.md"
    hs_path.write_text(hs_md, encoding='utf-8')
    print(f"✓ Exported Student Markdown: {hs_path} ({len(hs_md):,} chars)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_test_markdown.py <path_to_test.json>")
        sys.exit(1)
    export_test(sys.argv[1])
