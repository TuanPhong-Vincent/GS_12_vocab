#!/usr/bin/env python3
"""
Unit Test Generator & Builder (Global Success 10–12).
Compiles standardized 40-question unit tests (test1.json, test2.json)
for any Unit under lessons/unit-<N>/test/.
Matches the official 2025 National High School Exam blueprint from reference/.
"""

import sys
import os
import json
import re
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BLUEPRINT_SECTIONS = [
    {
        "section_id": "part_1",
        "section_number": 1,
        "title": "Cloze Advertisement",
        "keyword": "advertisement",
        "questions_range": [1, 6]
    },
    {
        "section_id": "part_2",
        "section_number": 2,
        "title": "Cloze Leaflet / Public Notice",
        "keyword": "leaflet",
        "questions_range": [7, 12]
    },
    {
        "section_id": "part_3",
        "section_number": 3,
        "title": "Sentence & Dialogue Arrangement",
        "keyword": "arrangement",
        "questions_range": [13, 17]
    },
    {
        "section_id": "part_4",
        "section_number": 4,
        "title": "Cloze Passage - Sentence/Clause Completion",
        "keyword": "18 to 22",
        "questions_range": [18, 22]
    },
    {
        "section_id": "part_5",
        "section_number": 5,
        "title": "Reading Comprehension 1",
        "keyword": "23 to 30",
        "questions_range": [23, 30]
    },
    {
        "section_id": "part_6",
        "section_number": 6,
        "title": "Reading Comprehension 2",
        "keyword": "31 to 40",
        "questions_range": [31, 40]
    }
]

def load_unit_vocab(unit_dir):
    vocab_path = unit_dir / "vocab" / "vocab.json"
    if not vocab_path.exists():
        return []
    try:
        with open(vocab_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        words = []
        for g in data:
            for w in g.get("words", []):
                words.append(w.get("english_word", ""))
        return words
    except Exception as e:
        print(f"Warning: Could not load vocab.json: {e}")
        return []

def load_unit_grammar(unit_dir):
    grammar_path = unit_dir / "grammar_raw.json"
    if not grammar_path.exists():
        return ["Target unit grammar points"]
    try:
        with open(grammar_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        topic = data.get("grammar_topic")
        return [topic] if topic else ["Grammar topic"]
    except Exception as e:
        print(f"Warning: Could not load grammar_raw.json: {e}")
        return ["Grammar topic"]

def parse_markdown_to_test_data(md_path, unit_num, test_num, unit_title):
    text = Path(md_path).read_text(encoding="utf-8")
    
    test_id = f"test_{test_num}"
    test_title = f"TEST {test_num} - UNIT {unit_num}: {unit_title.upper()}"
    
    questions = {}
    
    for q_idx in range(1, 41):
        if q_idx < 40:
            next_pat = rf'\*\*Question\s+{q_idx+1}:\*\*'
        else:
            next_pat = r'(?:---\s*\n\s*##\s*LISTENING|---\s*\n\s*###\s*Tạm Dịch Bài Đọc|\Z)'
            
        pat = rf'\*\*Question\s+{q_idx}:\*\*(.*?)(?={next_pat})'
        match = re.search(pat, text, re.DOTALL)
        if not match:
            continue
            
        block = match.group(1).strip()
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        
        prompt_text = f"Question {q_idx}:"
        first_line = lines[0] if lines else ""
        m_prompt_extra = re.match(r'^(.*?)(?=\s*\**[A-D]\.|\Z)', first_line)
        if m_prompt_extra and m_prompt_extra.group(1).strip():
            extra = m_prompt_extra.group(1).strip()
            if extra and not re.match(r'^\**[A-D]\.', extra):
                prompt_text = f"Question {q_idx}: {extra}".strip()
                
        before_expl = []
        after_expl = []
        hit_expl = False
        hit_trans = False
        trans_lines = []
        explanation_type = ""
        
        for l in lines:
            if l.startswith("**Giải Thích:**"):
                hit_expl = True
                m_ktype = re.match(r'^\*\*Giải Thích:\*\*\s*(.*)', l)
                if m_ktype:
                    explanation_type = m_ktype.group(1).strip()
                continue
            if l.startswith("**Tạm Dịch:**"):
                hit_trans = True
                m_trans = re.match(r'^\*\*Tạm Dịch:\*\*\s*(.*)', l)
                if m_trans:
                    trans_lines.append(m_trans.group(1).strip())
                continue
            if hit_trans:
                trans_lines.append(l)
            elif hit_expl:
                after_expl.append(l)
            else:
                before_expl.append(l)
                
        vietnamese_translation = " ".join(trans_lines).strip()
        
        options = {}
        correct_answer = None
        
        # Check inline options
        joined_opts_text = "\n".join(before_expl)
        opt_matches = list(re.finditer(r'(?:^|[\s\t])\**([A-D])\.\**\s*(.*?)(?=(?:[\s\t]+\**[A-D]\.\**)|$)', joined_opts_text, re.MULTILINE))
        if len(opt_matches) >= 4:
            for om in opt_matches[:4]:
                lbl = om.group(1)
                opt_val = om.group(2).strip()
                if (opt_val.startswith('**') and opt_val.endswith('**')) or (f"**{lbl}." in joined_opts_text and opt_val in joined_opts_text and f"**{opt_val}**" in joined_opts_text):
                    correct_answer = lbl
                    opt_val = re.sub(r'^\**|\**$', '', opt_val).strip()
                options[lbl] = re.sub(r'^\**|\**$', '', opt_val).strip()
        else:
            for l in before_expl:
                m_opt_line = re.match(r'^\**([A-D])\.\**\s*(.*)', l)
                if m_opt_line:
                    lbl = m_opt_line.group(1)
                    opt_val = m_opt_line.group(2).strip()
                    if opt_val.startswith('**') and opt_val.endswith('**'):
                        correct_answer = lbl
                        opt_val = opt_val[2:-2].strip()
                    options[lbl] = re.sub(r'^\**|\**$', '', opt_val).strip()
                    
        # Parse explanation analysis (supports both A, B, C, D and a, b, c, d, e)
        explanation_details = {}
        for l in after_expl:
            m_exp_opt = re.match(r'^\**([A-Za-z])(?:\.|\:)\**\s*(.*)', l)
            if m_exp_opt:
                lbl = m_exp_opt.group(1).upper() if m_exp_opt.group(1) in ['A', 'B', 'C', 'D'] else m_exp_opt.group(1)
                exp_text = m_exp_opt.group(2).strip()
                explanation_details[lbl] = exp_text
                if not correct_answer and (re.search(r'[–-]\s*(?:ĐÚNG|Đúng)', exp_text) or '– ĐÚNG' in exp_text):
                    correct_answer = lbl

        # Check bold answer in options directly
        if not correct_answer:
            m_bold = re.search(r'(?:^|[\s\t])(?:\*\*([A-D])\.\s+([^*]+)\*\*|\*\*([A-D])\.\*\*\s+\*\*([^*]+)\*\*|\*\*([A-D])\.\s*([^*]+)\*\*)', block)
            if m_bold:
                correct_answer = m_bold.group(1) or m_bold.group(3) or m_bold.group(5)

        # Check arrangement sequence in Q13-17
        if not correct_answer and 13 <= q_idx <= 17:
            m_seq = re.findall(r'\*\*([a-e]):\*\*', block)
            if m_seq:
                seq_str = "-".join(m_seq)
                for opt_lbl, opt_text in options.items():
                    if seq_str == opt_text.strip():
                        correct_answer = opt_lbl
                        break

        questions[q_idx] = {
            "question_number": q_idx,
            "prompt": prompt_text,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": {
                "knowledge_type": explanation_type or "Kiến thức bài thi",
                "analysis": explanation_details
            },
            "vietnamese_translation": vietnamese_translation
        }

    # Extract passages for sections
    sections = []
    for s_def in BLUEPRINT_SECTIONS:
        sec = {
            "section_id": s_def["section_id"],
            "section_number": s_def["section_number"],
            "title": s_def["title"],
            "instruction": "",
            "questions_range": s_def["questions_range"],
            "passage_title": "",
            "passage_text": ""
        }
        q_start, q_end = s_def["questions_range"]
        kw = s_def["keyword"]
        
        # Search for section header containing kw
        pat_sec = rf'###\s*([^#\n]*?{re.escape(kw)}[^#\n]*)\n(.*?)(?=\*\*Question\s+{q_start}:\*\*)'
        m_sec = re.search(pat_sec, text, re.DOTALL | re.IGNORECASE)
        if m_sec:
            sec["instruction"] = m_sec.group(1).strip()
            raw_sec_body = m_sec.group(2).strip()
            body_lines = [bl.strip() for bl in raw_sec_body.splitlines() if bl.strip()]
            if body_lines:
                # check if first line is passage title
                m_title = re.match(r'^\**([^*#\n]{4,80})\**$', body_lines[0])
                if m_title and len(body_lines) > 1 and not body_lines[0].startswith('- '):
                    sec["passage_title"] = m_title.group(1).strip()
                    sec["passage_text"] = "\n\n".join(body_lines[1:])
                else:
                    # check if instruction mentions about [Title]
                    m_about = re.search(r'about\s+(.*?)\s+and mark', sec["instruction"], re.IGNORECASE)
                    if m_about:
                        sec["passage_title"] = m_about.group(1).strip()
                    sec["passage_text"] = "\n\n".join(body_lines)
                    
        sections.append(sec)

    # Compute option distribution
    dist = {}
    for q_data in questions.values():
        ca = q_data["correct_answer"]
        if ca:
            dist[ca] = dist.get(ca, 0) + 1

    return {
        "test_id": test_id,
        "unit_number": unit_num,
        "unit_title": unit_title,
        "grade": "GS10",
        "title": test_title,
        "exam_format": "Chuẩn cấu trúc Đề thi tốt nghiệp THPT từ năm 2025 (40 câu trắc nghiệm)",
        "duration_minutes": 50,
        "total_questions": 40,
        "option_distribution": dist,
        "answer_key_summary": {str(q): questions[q]["correct_answer"] for q in range(1, 41)},
        "sections": sections,
        "questions": [questions[q] for q in range(1, 41)]
    }

def build_unit_tests(unit_folder, unit_num=1, unit_title="Family Life"):
    unit_path = Path(unit_folder)
    test_out_dir = unit_path / "test"
    test_out_dir.mkdir(parents=True, exist_ok=True)
    
    vocab_words = load_unit_vocab(unit_path)
    grammar_points = load_unit_grammar(unit_path)
    
    ref_dir = Path("reference")
    if not ref_dir.exists():
        ref_dir = unit_path.parent.parent / "reference"
        
    print(f"Building tests for Unit {unit_num}: {unit_title}...")
    print(f"Loaded {len(vocab_words)} vocabulary words, grammar: {grammar_points}")
    
    # Check if reference tests exist
    test1_ref = ref_dir / f"UNIT {unit_num} - Test 1 - GV.md"
    if not test1_ref.exists():
        test1_ref = ref_dir / f"TEST 1 - UNIT {unit_num} - GV.md"
        
    test2_ref = ref_dir / f"UNIT {unit_num} - Test 2 - GV.md"
    if not test2_ref.exists():
        test2_ref = ref_dir / f"TEST 2 - UNIT {unit_num} - GV.md"
        
    if test1_ref.exists():
        print(f"Compiling Test 1 from {test1_ref.name}...")
        t1_data = parse_markdown_to_test_data(test1_ref, unit_num, 1, unit_title)
        t1_data["target_grammar"] = grammar_points
        t1_data["target_vocabulary_sample"] = vocab_words[:12]
        
        t1_path = test_out_dir / "test1.json"
        with open(t1_path, "w", encoding="utf-8") as f:
            json.dump(t1_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved: {t1_path} ({t1_path.stat().st_size:,} bytes)")
        
    if test2_ref.exists():
        print(f"Compiling Test 2 from {test2_ref.name}...")
        t2_data = parse_markdown_to_test_data(test2_ref, unit_num, 2, unit_title)
        t2_data["target_grammar"] = grammar_points
        t2_data["target_vocabulary_sample"] = vocab_words[12:24] if len(vocab_words) > 12 else vocab_words
        
        t2_path = test_out_dir / "test2.json"
        with open(t2_path, "w", encoding="utf-8") as f:
            json.dump(t2_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved: {t2_path} ({t2_path.stat().st_size:,} bytes)")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        u_folder = sys.argv[1]
        u_num = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        u_title = sys.argv[3] if len(sys.argv) > 3 else "Family Life"
    else:
        u_folder = r"d:\GS10\lessons\unit-1"
        u_num = 1
        u_title = "Family Life"
        
    build_unit_tests(u_folder, u_num, u_title)
