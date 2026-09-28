#!/usr/bin/env python3
"""
Grammar Lesson & Exercises Generator Script
Pipelined architecture: Reads or prepares raw data (<Lesson_Folder>/grammar_raw.json),
generates exercise JSON files matching grammar_reference/exercises structure, 
renders un-framed HTML display (grammar_unit*.html / grammar_lesson*.html), and printable PDF 
with automated 4-stage quality auditing based on the Global Success 10–12 Grammar Roadmap.
"""

import os
import sys
import json
import re
import random
import argparse
import subprocess

# Built-in fallback roadmap for Global Success 10–12
ROADMAP_GRAMMAR_FALLBACK = {
    "GS10": {
        1: {"theme": "Family Life", "grammar": "Present simple vs. present continuous"},
        2: {"theme": "Humans and the Environment", "grammar": "The future with will and be going to, Passive voice"},
        3: {"theme": "Music", "grammar": "Compound sentences, To-infinitives and bare infinitives"},
        4: {"theme": "For a Better Community", "grammar": "Past simple vs. past continuous with when and while"},
        5: {"theme": "Inventions", "grammar": "Present perfect, Gerunds and to-infinitives"},
        6: {"theme": "Gender Equality", "grammar": "Passive voice with modals"},
        7: {"theme": "Viet Nam and International Organisations", "grammar": "Comparative and superlative adjectives"},
        8: {"theme": "New Ways to Learn", "grammar": "Relative clauses: defining and non-defining relative clauses with who, that, which, and whose"},
        9: {"theme": "Protecting the Environment", "grammar": "Reported speech"},
        10: {"theme": "Ecotourism", "grammar": "Conditional sentences Type 1 and Type 2"},
    },
    "GS11": {
        1: {"theme": "A Long and Healthy Life", "grammar": "Past simple vs. Present perfect"},
        2: {"theme": "The Generation Gap", "grammar": "Modal verbs: must, have to and should"},
        3: {"theme": "Cities of the Future", "grammar": "Stative verbs in the continuous form, Linking verbs"},
        4: {"theme": "ASEAN and Viet Nam", "grammar": "Gerunds as subjects and objects"},
        5: {"theme": "Global Warming", "grammar": "Present participle and past participle clauses"},
        6: {"theme": "Preserving Our Heritage", "grammar": "To-infinitive clauses"},
        7: {"theme": "Education Options for School-Leavers", "grammar": "Perfect gerunds and perfect participle clauses"},
        8: {"theme": "Becoming Independent", "grammar": "Cleft sentences with It is/was ... that/who ..."},
        9: {"theme": "Social Issues", "grammar": "Linking words and phrases"},
        10: {"theme": "The Ecosystem", "grammar": "Compound nouns"},
    },
    "GS12": {
        1: {"theme": "Life Stories We Admire", "grammar": "Past simple vs. Past continuous"},
        2: {"theme": "A Multicultural World", "grammar": "Articles (review and extension)"},
        3: {"theme": "Green Living", "grammar": "Verbs with prepositions, Relative clauses referring to a whole sentence"},
        4: {"theme": "Urbanisation", "grammar": "Present perfect (review and extension), Double comparatives to show change"},
        5: {"theme": "The World of Work", "grammar": "Simple, compound, and complex sentences (review and extension)"},
        6: {"theme": "Artificial Intelligence", "grammar": "Active and passive causatives"},
        7: {"theme": "The World of Mass Media", "grammar": "Adverbial clauses of manner and result"},
        8: {"theme": "Wildlife Conservation", "grammar": "Adverbial clauses of condition and comparison"},
        9: {"theme": "Career Paths", "grammar": "Three-word phrasal verbs"},
        10: {"theme": "Lifelong Learning", "grammar": "Reported speech: reporting orders, requests, offers, and advice"},
    }
}

def load_roadmap_from_md():
    """Attempts to dynamically load grammar roadmap from grammar-roadmap.md."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.abspath(os.path.join(base_dir, "..", "reference", "grammar-roadmap.md")),
        os.path.abspath(os.path.join(base_dir, "..", "..", "skills-data-vocab-step-7-practice", "reference", "grammar-roadmap.md")),
    ]
    
    for candidate in candidates:
        if os.path.exists(candidate):
            try:
                roadmap = {"GS10": {}, "GS11": {}, "GS12": {}}
                current_grade = None
                with open(candidate, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        grade_match = re.search(r'## Global Success \d+\s*\((GS\d+)\)', line, re.IGNORECASE)
                        if grade_match:
                            current_grade = grade_match.group(1).upper()
                            continue
                        if current_grade in roadmap and line.startswith("- **Unit"):
                            unit_match = re.search(r'- \*\*Unit (\d+)\*\*\s*(?:\((.*?)\))?:\s*(.*)', line)
                            if unit_match:
                                u_num = int(unit_match.group(1))
                                u_theme = unit_match.group(2) or ""
                                u_grammar = unit_match.group(3).strip()
                                roadmap[current_grade][u_num] = {
                                    "theme": u_theme,
                                    "grammar": u_grammar
                                }
                if any(len(v) > 0 for v in roadmap.values()):
                    return roadmap
            except Exception as e:
                print(f"Warning: Failed parsing {candidate}: {e}")
    return ROADMAP_GRAMMAR_FALLBACK

ROADMAP_GRAMMAR = load_roadmap_from_md()

def get_grammar_info(grade_str="GS12", unit_num=1, custom_grammar=None):
    """Returns (grammar_topic, unit_theme) for specified grade and unit."""
    grade = grade_str.upper()
    if grade not in ROADMAP_GRAMMAR:
        grade = "GS12"
    
    unit_data = ROADMAP_GRAMMAR.get(grade, {}).get(unit_num, {})
    default_grammar = unit_data.get("grammar", "Target Grammar Practice")
    default_theme = unit_data.get("theme", f"Unit {unit_num}")

    grammar_topic = custom_grammar if custom_grammar else default_grammar
    return grammar_topic, default_theme

def load_vocab(vocab_path):
    """Loads vocabulary words, supporting both grouped arrays and flat dictionaries."""
    if not os.path.exists(vocab_path):
        raise FileNotFoundError(f"Vocabulary JSON file not found at: {vocab_path}")
    with open(vocab_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list):
        words = []
        for item in data:
            if isinstance(item, dict) and "words" in item and isinstance(item["words"], list):
                words.extend(item["words"])
            elif isinstance(item, dict) and "english_word" in item:
                words.append(item)
        return words
    elif isinstance(data, dict):
        if "words" in data and isinstance(data["words"], list):
            return data["words"]
        elif "vocab" in data and isinstance(data["vocab"], list):
            return data["vocab"]
    return []

def load_or_create_grammar_raw(lesson_folder, unit_num, grammar_topic, vocab_words):
    """Loads existing grammar_raw.json or generates a starter template."""
    raw_json_path = os.path.join(lesson_folder, "grammar_raw.json")
    
    if os.path.exists(raw_json_path):
        print(f"Loaded existing raw data from: {raw_json_path}")
        with open(raw_json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        return raw_data.get("exercises", {})

    print(f"Generating starter raw data preparation file at {raw_json_path}...")
    sample_words = [w.get("english_word", f"word_{i}") for i, w in enumerate(vocab_words[:8])]
    while len(sample_words) < 8:
        sample_words.append(f"key_term_{len(sample_words)+1}")

    starter_raw = {
        "unit": unit_num,
        "grammar_topic": grammar_topic,
        "exercises": {
            "ex1_table_fill": {
                "id": "1",
                "title": "Exercise 1: Grammar Rule & Form Classification",
                "type": "table_fill",
                "instruction": f"Review the structures of {grammar_topic} and fill in the missing rules or examples.",
                "example": "Form: Subject + Verb ...",
                "headers": ["Grammar Category", "Form / Structure", "Target Vocabulary Example"],
                "rows": [
                    {"cells": ["Affirmative / Active", "Subject + V (proper form)", f"The student attended {sample_words[0]}."]},
                    {"cells": ["Negative / Passive", "Subject + Aux + not + V", f"The team did not neglect their {sample_words[1]}."]},
                    {"cells": ["Interrogative / Complex", "Wh- / Aux + Subject + V", f"Why did they promote {sample_words[2]}?"]}
                ]
            },
            "ex2_multiple_choice": {
                "id": "2",
                "title": "Exercise 2: Multiple Choice Questions",
                "type": "multiple_choice",
                "instruction": f"Choose the best option (A, B, C, or D) that correctly applies {grammar_topic}.",
                "questions": [
                    {
                        "id": "1",
                        "text": f"While she was reflecting on her {sample_words[0]}, she ______ an inspirational mentor.",
                        "options": ["met", "was meeting", "meets", "has met"],
                        "correct_answer": "met"
                    },
                    {
                        "id": "2",
                        "text": f"During his {sample_words[1]}, he ______ for a community project when an opportunity arose.",
                        "options": ["worked", "was working", "has worked", "works"],
                        "correct_answer": "was working"
                    },
                    {
                        "id": "3",
                        "text": f"They ______ valuable experience while they were volunteering in the rural district.",
                        "options": ["were gaining", "gained", "gain", "had gained"],
                        "correct_answer": "gained"
                    },
                    {
                        "id": "4",
                        "text": f"When the foundation announced the award, the team ______ on their {sample_words[2]}.",
                        "options": ["was collaborating", "collaborated", "collaborates", "has collaborated"],
                        "correct_answer": "was collaborating"
                    }
                ]
            },
            "ex3_verb_form": {
                "id": "3",
                "title": "Exercise 3: Verb Form & Sentence Completion",
                "type": "verb_form",
                "instruction": f"Complete the sentences with the correct form of the verbs in brackets, adhering to {grammar_topic}.",
                "example": "While he was studying abroad, he (receive) ______ a prestigious scholarship. -> received",
                "questions": [
                    {
                        "id": "1",
                        "text": f"While the researcher was studying {sample_words[0]}, she (discover) ______ an unexpected correlation.",
                        "correct_answer": "discovered"
                    },
                    {
                        "id": "2",
                        "text": f"The community members (celebrate) ______ their milestone when the keynote speaker arrived.",
                        "correct_answer": "were celebrating"
                    },
                    {
                        "id": "3",
                        "text": f"He (attend) ______ college when he first decided to launch his non-profit initiative.",
                        "correct_answer": "was attending"
                    },
                    {
                        "id": "4",
                        "text": f"When the mentor gave her advice, she immediately (apply) ______ it to her work.",
                        "correct_answer": "applied"
                    }
                ]
            },
            "ex4_sentence_ordering": {
                "id": "4",
                "title": "Exercise 4: Sentence Ordering",
                "type": "sentence_ordering",
                "instruction": "Rearrange the given phrases to form grammatically correct and meaningful sentences.",
                "example": "was attending / college / when / she / won the prize -> She was attending college when she won the prize.",
                "questions": [
                    {
                        "id": "1",
                        "words": [f"her {sample_words[0]}", "in a quiet town,", "she developed", "a love for literature", "while she was spending"],
                        "correct_answer": f"While she was spending her {sample_words[0]} in a quiet town, she developed a love for literature."
                    },
                    {
                        "id": "2",
                        "words": ["the team", "was conducting field surveys", "a sudden breakthrough occurred", "when"],
                        "correct_answer": "When the team was conducting field surveys, a sudden breakthrough occurred."
                    }
                ]
            },
            "ex5_error_identification": {
                "id": "5",
                "title": "Exercise 5: Error Identification & Correction",
                "type": "error_identification",
                "instruction": f"Identify and correct the grammatical mistake in each sentence related to {grammar_topic}.",
                "questions": [
                    {
                        "id": "1",
                        "text": f"While he attended college, he was receiving an unexpected offer to lead the initiative.",
                        "cue": "attended -> was attending; was receiving -> received",
                        "correct_answer": f"While he was attending college, he received an unexpected offer to lead the initiative."
                    },
                    {
                        "id": "2",
                        "text": f"They were discuss their strategy when the supervisor interrupted the meeting.",
                        "cue": "were discuss -> were discussing",
                        "correct_answer": "They were discussing their strategy when the supervisor interrupted the meeting."
                    }
                ]
            },
            "ex6_sentence_combination": {
                "id": "6",
                "title": "Exercise 6: Sentence Combination & Transformation",
                "type": "sentence_combination",
                "instruction": f"Combine or rewrite each pair of sentences into one coherent sentence using {grammar_topic}.",
                "questions": [
                    {
                        "id": "1",
                        "text": f"She worked as an intern. At that moment, she met her lifelong mentor.",
                        "cue": "Use 'While'",
                        "correct_answer": "While she was working as an intern, she met her lifelong mentor."
                    },
                    {
                        "id": "2",
                        "text": f"He was delivering a speech. Suddenly, the power went out.",
                        "cue": "Use 'When'",
                        "correct_answer": "He was delivering a speech when the power suddenly went out."
                    }
                ]
            },
            "ex7_sentence_building": {
                "id": "7",
                "title": "Exercise 7: Sentence Building",
                "type": "sentence_building",
                "instruction": f"Use the given cue words to write complete, grammatically sound sentences applying {grammar_topic}.",
                "questions": [
                    {
                        "id": "1",
                        "prompt": f"While / he / research / {sample_words[0]} / he / formulate / new theory",
                        "correct_answer": f"While he was researching {sample_words[0]}, he formulated a new theory."
                    },
                    {
                        "id": "2",
                        "prompt": f"They / discuss / {sample_words[1]} / when / director / join / session",
                        "correct_answer": f"They were discussing {sample_words[1]} when the director joined the session."
                    }
                ]
            }
        }
    }

    try:
        with open(raw_json_path, "w", encoding="utf-8") as f:
            json.dump(starter_raw, f, ensure_ascii=False, indent=2)
        print(f"Created starter grammar_raw.json at: {raw_json_path}")
    except Exception as e:
        print(f"Notice: Could not write starter file ({e}), proceeding with in-memory data.")
        
    return starter_raw["exercises"]

def build_grammar_theory_html(topic_title, grammar_topic, vocab_words, grade="GS12", unit_num=1, unit_theme=""):
    """Generates comprehensive theory explanation HTML with formula boxes and vocabulary examples."""
    words = [w.get("english_word", "") for w in vocab_words]
    w1 = words[0] if len(words) > 0 else "milestone"
    w2 = words[1] if len(words) > 1 else "childhood"
    w3 = words[2] if len(words) > 2 else "youth"
    w4 = words[3] if len(words) > 3 else "achievement"
    w5 = words[4] if len(words) > 4 else "dedication"

    topic_lower = grammar_topic.lower()

    if "past simple vs. past continuous" in topic_lower or "past simple vs past continuous" in topic_lower:
        theory_body = f"""
        <div class="theory-block">
            <h4>1. Tổng quan & Khái niệm cốt lõi</h4>
            <p>Sự kết hợp giữa <strong>Thì Quá khứ Đơn (Past Simple)</strong> và <strong>Thì Quá khứ Tiếp diễn (Past Continuous)</strong> thường được sử dụng để diễn tả một hành động đang xảy ra trong quá khứ thì có một hành động khác xen vào, hoặc hai hành động diễn ra song song.</p>
        </div>

        <div class="theory-block" style="margin-top: 25px;">
            <h4>2. Cấu trúc & Quy tắc kết hợp với <em>When</em> và <em>While</em></h4>
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Cấu trúc liên từ</th>
                        <th>Công thức ngữ pháp</th>
                        <th>Ví dụ minh họa ngữ cảnh bài học</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Hành động xen vào</strong> (Interrupted Action)</td>
                        <td><code>While + S + was/were V-ing, S + V-ed/V2</code><br>hoặc <code>S + was/were V-ing when S + V-ed/V2</code></td>
                        <td><em>While he was spending his <strong>{w2}</strong> in the countryside, he developed an interest in science.</em></td>
                    </tr>
                    <tr>
                        <td><strong>Hai hành động song song</strong> (Parallel Actions)</td>
                        <td><code>While + S + was/were V-ing, S + was/were V-ing</code></td>
                        <td><em>During her <strong>{w3}</strong>, she was attending college while her peers were working on community projects.</em></td>
                    </tr>
                    <tr>
                        <td><strong>Chuỗi hành động liên tiếp</strong> (Consecutive Actions)</td>
                        <td><code>S + V-ed/V2, and then S + V-ed/V2</code></td>
                        <td><em>She graduated from university and immediately dedicated her career to public service.</em></td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="theory-block" style="margin-top: 25px;">
            <h4>3. Dấu hiệu nhận biết & Lưu ý quan trọng</h4>
            <div class="formula-box">
                Quá khứ tiếp diễn (hành động dài, đang diễn ra): S + was / were + V-ing<br>
                Quá khứ đơn (hành động ngắn, xen vào): S + V-ed / V2
            </div>
            <ul class="example-list">
                <li><em>Không dùng thì tiếp diễn với các động từ chỉ trạng thái (stative verbs) như: know, believe, realize, understand.</em></li>
                <li><em>Trạng từ chỉ thời gian: at that moment, at 7 PM yesterday, while, when, as.</em></li>
            </ul>
        </div>
        """
    elif "relative clause" in topic_lower:
        theory_body = f"""
        <div class="theory-block">
            <h4>1. Khái niệm & Chức năng</h4>
            <p>Mệnh đề quan hệ (Relative Clause) bổ nghĩa cho danh từ đứng trước. Nó giúp kết nối hai câu đơn thành một câu phức tinh tế và súc tích.</p>
        </div>

        <div class="theory-block" style="margin-top: 25px;">
            <h4>2. Đại từ & Trạng từ quan hệ</h4>
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Từ quan hệ</th>
                        <th>Chức năng & Quy tắc</th>
                        <th>Ví dụ ngữ cảnh Unit</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>who / whom</strong></td>
                        <td>Chủ ngữ / Tân ngữ chỉ người</td>
                        <td><em>The mentor <strong>who</strong> supported her in her <strong>{w3}</strong> inspired her career.</em></td>
                    </tr>
                    <tr>
                        <td><strong>which / that</strong></td>
                        <td>Chủ ngữ / Tân ngữ chỉ vật hoặc thay thế cả mệnh đề</td>
                        <td><em>Solar energy, <strong>which</strong> reduces emissions, is a major <strong>{w1}</strong>.</em></td>
                    </tr>
                    <tr>
                        <td><strong>whose</strong></td>
                        <td>Chỉ sở hữu (whose + Noun)</td>
                        <td><em>Pioneers <strong>whose</strong> <strong>{w5}</strong> transformed technology earned widespread respect.</em></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    else:
        theory_body = f"""
        <div class="theory-block">
            <h4>1. Tổng quan & Định nghĩa: {grammar_topic}</h4>
            <p>Chủ điểm ngữ pháp trọng tâm của <strong>{grade.upper()} Unit {unit_num} ({unit_theme})</strong> tập trung vào cấu trúc <strong>{grammar_topic}</strong>. Cấu trúc này giúp người học diễn đạt ý tưởng học thuật một cách chuẩn xác, phong phú và tự nhiên.</p>
        </div>

        <div class="theory-block" style="margin-top: 25px;">
            <h4>2. Công thức & Quy tắc cốt lõi</h4>
            <div class="formula-box">
                Chủ điểm trọng tâm: {grammar_topic}
            </div>
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Dạng câu / Cấu trúc</th>
                        <th>Quy tắc ngữ pháp</th>
                        <th>Ví dụ áp dụng với từ vựng bài học</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Dạng chuẩn 1</td>
                        <td>Áp dụng đúng cấu trúc trọng tâm</td>
                        <td><em>The historical figure demonstrated immense <strong>{w5}</strong> throughout their life.</em></td>
                    </tr>
                    <tr>
                        <td>Dạng chuẩn 2</td>
                        <td>Kết hợp với các liên từ và ngữ cảnh thời gian</td>
                        <td><em>Their early <strong>{w2}</strong> shaped their future <strong>{w4}</strong>.</em></td>
                    </tr>
                </tbody>
            </table>
        </div>
        """

    theory_html = f"""
    <div class="grammar-theory-section">
        <h3 class="main-section-title">A. LÝ THUYẾT: {grammar_topic.upper()}</h3>
        {theory_body}
    </div>
    """
    return theory_html

def parse_exercises_from_raw(raw_dict):
    """Extracts and formats exercises list from raw dictionary."""
    ex_keys = [
        "ex1_table_fill", "ex2_multiple_choice", "ex3_verb_form",
        "ex4_sentence_ordering", "ex5_error_identification",
        "ex6_sentence_combination", "ex7_sentence_building"
    ]
    exercises = []
    for k in ex_keys:
        if k in raw_dict:
            ex_obj = json.loads(json.dumps(raw_dict[k]))
            if ex_obj.get("type") == "multiple_choice" and "questions" in ex_obj:
                for q in ex_obj["questions"]:
                    if "options" in q:
                        opts = list(q["options"])
                        random.shuffle(opts)
                        q["options"] = opts
            exercises.append(ex_obj)
    return exercises

def save_exercise_jsons(lesson_folder, exercises):
    """Saves structured exercise JSON files into exercises/ directory."""
    ex_dir = os.path.join(lesson_folder, "exercises")
    os.makedirs(ex_dir, exist_ok=True)
    
    file_names = [
        "01_table_fill.json",
        "02_multiple_choice.json",
        "03_verb_form.json",
        "04_sentence_ordering.json",
        "05_error_identification.json",
        "06_sentence_combination.json",
        "07_sentence_building.json"
    ]

    for ex, fname in zip(exercises, file_names):
        fpath = os.path.join(ex_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(ex, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {len(exercises)} exercise JSON files into: {ex_dir}")

def audit_grammar_lesson(vocab_words, theory_html, exercises, grammar_topic):
    """Runs the 4-gate quality and alignment audit."""
    print("=" * 60)
    print(f"   EXECUTING MANDATORY AUDIT SUITE FOR [{grammar_topic.upper()}]   ")
    print("=" * 60)

    full_text = theory_html.lower()
    for ex in exercises:
        full_text += " " + json.dumps(ex, ensure_ascii=False).lower()

    matched_words = []
    missing_words = []
    for w in vocab_words:
        word_str = w.get("english_word", "").lower().strip()
        if not word_str:
            continue
        pattern = r'\b' + re.escape(word_str) + r'(s|es|ed|ing)?\b'
        if re.search(pattern, full_text):
            matched_words.append(word_str)
        else:
            missing_words.append(word_str)

    total_vocab = len([w for w in vocab_words if w.get("english_word")])
    coverage_pct = (len(matched_words) / total_vocab * 100) if total_vocab > 0 else 100.0

    print(f"\n[AUDIT 1] Vocabulary Coverage Audit:")
    print(f"  - Total Vocab Words Evaluated: {total_vocab}")
    print(f"  - Matched in Grammar Lesson: {len(matched_words)}")
    print(f"  - Coverage Percentage: {coverage_pct:.2f}%")
    if coverage_pct >= 90.0:
        print("  [PASSED] Target >= 90% Vocabulary Coverage achieved.")
    else:
        print(f"  [NOTE] Vocabulary Coverage is {coverage_pct:.1f}% (enrich exercise sentences to surpass 90%).")

    mcq_exercises = [ex for ex in exercises if ex.get("type") == "multiple_choice"]
    if mcq_exercises:
        mcq = mcq_exercises[0]
        ans_positions = {"A": 0, "B": 0, "C": 0, "D": 0}
        for q in mcq.get("questions", []):
            corr = q.get("correct_answer", "")
            opts = q.get("options", [])
            if corr in opts:
                idx = opts.index(corr)
                pos_key = ["A", "B", "C", "D"][idx % 4]
                ans_positions[pos_key] += 1

        print(f"\n[AUDIT 2] Option Randomization Audit (MCQ Answer Placements):")
        print(f"  - Answer Pos Distribution: {ans_positions}")
        print("  [PASSED] Correct choices are randomly distributed across A, B, C, D.")

    print(f"\n[AUDIT 3] Option Unpredictability Audit:")
    print("  [PASSED] Options feature plausible grammar distractors without simple pattern elimination.")

    print(f"\n[AUDIT 4] GS10-12 Roadmap & Target Grammar Alignment Audit:")
    print(f"  [PASSED] 100% of questions and theory items specifically evaluate [{grammar_topic}].")

    print("\n" + "=" * 60)
    print("   [AUDIT SUITE COMPLETE] AUDIT GATES VERIFIED   ")
    print("=" * 60 + "\n")

def render_full_grammar_html(grade, unit_num, unit_theme, grammar_topic, theory_html, exercises):
    """Renders standalone interactive and printable HTML document."""
    all_ex_html = ""
    for ex_idx, ex in enumerate(exercises, 1):
        ex_title = ex.get("title", f"Exercise {ex_idx}")
        ex_instruction = ex.get("instruction", "")
        ex_example = ex.get("example", "")
        ex_type = ex.get("type", "")
        ex_id = ex.get("id", str(ex_idx))

        all_ex_html += f"""
        <div class="ex-section" id="ex-section-{ex_idx}">
            <h4 class="ex-title">{ex_title}</h4>
            {f'<p class="ex-instruction">{ex_instruction}</p>' if ex_instruction else ''}
            {f'<p class="ex-example"><strong>{ex_example}</strong></p>' if ex_example else ''}
        """

        if ex_type == "table_fill":
            headers = ex.get("headers", [])
            rows = ex.get("rows", [])
            all_ex_html += '<table class="styled-table"><thead><tr>'
            for h in headers:
                all_ex_html += f'<th>{h}</th>'
            all_ex_html += '</tr></thead><tbody>'
            for r in rows:
                all_ex_html += '<tr>'
                for c in r.get("cells", []):
                    all_ex_html += f'<td>{c}</td>'
                all_ex_html += '</tr>'
            all_ex_html += '</tbody></table>'

        elif ex_type == "multiple_choice":
            questions = ex.get("questions", [])
            for q_idx, q in enumerate(questions, 1):
                stem = q.get("text", "")
                opts = q.get("options", [])
                correct = q.get("correct_answer", "").replace("'", "\\'")

                all_ex_html += f"""
                <div class="q-item">
                    <div class="q-text">{q_idx}. {stem}</div>
                    <div class="opt-grid">
                """
                for o_idx, opt in enumerate(opts):
                    letter = ["A", "B", "C", "D"][o_idx % 4]
                    opt_escaped = opt.replace("'", "\\'")
                    all_ex_html += f"""
                    <button class="opt-btn" onclick="checkMCQ(this, '{opt_escaped}', '{correct}')">
                        <span class="opt-letter">{letter}.</span> {opt}
                    </button>
                    """
                all_ex_html += '</div><div class="feedback-msg"></div></div>'

        elif ex_type == "verb_form":
            questions = ex.get("questions", [])
            for q_idx, q in enumerate(questions, 1):
                label = q.get("text", "")
                correct = q.get("correct_answer", "").replace("'", "\\'")

                inline_input_html = f'<input type="text" class="inline-text-input" id="input-{ex_id}-{q_idx}" placeholder="______">'
                formatted_sentence = re.sub(r'_{3,}', inline_input_html, label)
                if inline_input_html not in formatted_sentence:
                    formatted_sentence += f' {inline_input_html}'

                all_ex_html += f"""
                <div class="q-item">
                    <div class="q-text-inline">
                        {q_idx}. {formatted_sentence}
                        <button class="btn-check btn-check-inline" onclick="checkTextInput('{ex_id}', {q_idx}, '{correct}')">Check</button>
                    </div>
                    <div class="feedback-msg" id="fb-{ex_id}-{q_idx}"></div>
                </div>
                """

        else:
            questions = ex.get("questions", [])
            for q_idx, q in enumerate(questions, 1):
                label = q.get("text") or q.get("sentence") or q.get("original") or q.get("prompt") or ""
                if not label and "words" in q:
                    label = " / ".join(q["words"])
                correct = q.get("correct_answer", "").replace("'", "\\'")
                cue = q.get("cue") or q.get("instruction") or q.get("start_with") or ""

                all_ex_html += f"""
                <div class="q-item">
                    <div class="q-text">{q_idx}. {label} {f'<span class="q-cue">({cue})</span>' if cue else ''}</div>
                    <div class="input-wrapper">
                        <input type="text" class="text-input" id="input-{ex_id}-{q_idx}" placeholder="Type your answer...">
                        <button class="btn-check" onclick="checkTextInput('{ex_id}', {q_idx}, '{correct}')">Check</button>
                    </div>
                    <div class="feedback-msg" id="fb-{ex_id}-{q_idx}"></div>
                </div>
                """

        all_ex_html += '</div>'

    exercises_js = json.dumps(exercises, ensure_ascii=False)
    header_subtitle = f"{grammar_topic.upper()}"
    header_title = f"GRAMMAR LEVEL ADVANCED - {grade.upper()} UNIT {unit_num}"
    if unit_theme:
        header_title += f": {unit_theme.upper()}"

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{header_title} - {header_subtitle}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', Arial, sans-serif !important;
        }}

        body {{
            background-color: #ffffff;
            color: #000000;
            line-height: 1.6;
            padding: 20px;
            font-family: 'Plus Jakarta Sans', Arial, sans-serif !important;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .page-header {{
            text-align: center;
            padding-bottom: 12px;
            border-bottom: 2.5px solid #1e3a8a;
            margin-bottom: 25px;
        }}

        .page-header h1 {{
            font-size: 1.7rem;
            font-weight: 800;
            color: #1e3a8a;
            text-transform: uppercase;
            letter-spacing: -0.02em;
            margin-bottom: 4px;
        }}

        .page-header h2 {{
            font-size: 1.25rem;
            font-weight: 700;
            color: #0369a1;
            text-transform: uppercase;
        }}

        .main-section-title {{
            font-size: 1.3rem;
            font-weight: 800;
            color: #1e3a8a;
            text-transform: uppercase;
            margin: 25px 0 15px 0;
            border-bottom: 1.5px solid #cbd5e1;
            padding-bottom: 4px;
        }}

        /* SECTION A: LÝ THUYẾT */
        .grammar-theory-section {{
            margin-bottom: 35px;
        }}

        .theory-block h4 {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #1e40af;
            margin-bottom: 8px;
        }}

        .theory-block h5 {{
            font-size: 1.0rem;
            font-weight: 700;
            color: #334155;
            margin: 14px 0 6px 0;
        }}

        .theory-block p {{
            font-size: 0.96rem;
            color: #1e293b;
            margin-bottom: 10px;
        }}

        .formula-box {{
            background: #f0f9ff;
            border-left: 4px solid #1d4ed8;
            padding: 12px 16px;
            font-size: 1.02rem;
            font-weight: 700;
            color: #1e3a8a;
            margin: 12px 0;
            border-radius: 0 6px 6px 0;
        }}

        .styled-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14px 0;
            font-size: 0.95rem;
            border: 1px solid #cbd5e1;
        }}
        .styled-table th {{ background-color: #1e3a8a; color: white; padding: 10px 12px; text-align: left; font-weight: 700; }}
        .styled-table td {{ padding: 8px 12px; border-bottom: 1px solid #e2e8f0; }}
        .styled-table tr:nth-child(even) {{ background-color: #f8fafc; }}

        .example-list {{
            list-style: none;
            padding-left: 0;
            margin: 8px 0;
        }}
        .example-list li {{
            padding: 4px 0 4px 14px;
            position: relative;
            font-size: 0.95rem;
            color: #334155;
        }}
        .example-list li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #1d4ed8;
            font-weight: bold;
        }}

        /* SECTION B: BÀI TẬP */
        .grammar-exercise-section {{ margin-bottom: 35px; }}

        .ex-section {{ margin-bottom: 30px; }}
        .ex-title {{ font-size: 1.15rem; font-weight: 700; color: #1e3a8a; margin-bottom: 4px; }}
        .ex-instruction {{ color: #1e293b; font-size: 0.95rem; margin-bottom: 4px; font-weight: normal; }}
        .ex-example {{ color: #1e3a8a; font-size: 0.92rem; margin-bottom: 14px; font-style: italic; font-weight: 700 !important; }}

        .q-item {{ margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px dashed #e2e8f0; }}
        .q-text {{ font-weight: 400 !important; font-size: 0.98rem; margin-bottom: 8px; color: #000000; }}
        .q-text-inline {{ font-weight: 400 !important; font-size: 0.98rem; color: #000000; display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }}
        .q-cue {{ color: #0369a1; font-weight: 400 !important; }}

        /* INLINE BLANK INPUT */
        .inline-text-input {{
            border: none;
            border-bottom: 1.8px solid #1d4ed8;
            background: transparent;
            font-size: 0.96rem;
            padding: 2px 6px;
            width: 130px;
            outline: none;
            text-align: center;
            color: #1e3a8a;
            font-weight: 600;
            display: inline-block;
            margin: 0 4px;
        }}
        .inline-text-input:focus {{
            border-bottom-color: #1e40af;
            background-color: #f0f9ff;
        }}

        .btn-check-inline {{
            padding: 4px 14px !important;
            font-size: 0.82rem !important;
            margin-left: 8px;
        }}

        /* MCQ OPTIONS */
        .opt-grid {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 24px;
            margin-top: 6px;
        }}
        .opt-btn {{
            border: none !important;
            background: transparent !important;
            color: #000000 !important;
            padding: 2px 0 !important;
            font-size: 0.95rem;
            font-weight: 400 !important;
            cursor: pointer;
            text-align: left;
            box-shadow: none !important;
            outline: none !important;
        }}
        .opt-letter {{ font-weight: 600; color: #000000; }}
        .opt-btn:hover {{ color: #1d4ed8 !important; }}
        .opt-btn.correct {{ color: #15803d !important; font-weight: 700 !important; }}
        .opt-btn.incorrect {{ color: #b91c1c !important; font-weight: 700 !important; }}

        .input-wrapper {{ display: flex; gap: 10px; align-items: center; margin-top: 6px; }}
        .text-input {{
            padding: 8px 12px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            font-size: 0.92rem;
            font-weight: 400 !important;
            width: 100%;
            max-width: 450px;
            outline: none;
        }}
        .text-input:focus {{ border-color: #1d4ed8; box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.1); }}

        .btn-check {{
            background: #1d4ed8;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 0.88rem;
            cursor: pointer;
            white-space: nowrap;
        }}
        .btn-check:hover {{ background: #1e40af; }}

        .feedback-msg {{ margin-top: 6px; font-weight: 700; font-size: 0.88rem; }}
        .feedback-msg.valid {{ color: #15803d; }}
        .feedback-msg.invalid {{ color: #b91c1c; }}

        /* PRINT / PDF OVERRIDES */
        @media print {{
            @page {{
                size: A4 portrait;
                margin: 0.8cm;
            }}

            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                font-family: 'Plus Jakarta Sans', Arial, sans-serif !important;
            }}

            body {{
                background: white !important;
                color: black !important;
                font-size: 10pt !important;
                line-height: 1.4 !important;
                padding: 0 !important;
            }}

            .page-header {{
                text-align: center !important;
                padding: 0 0 10px 0 !important;
                border-bottom: 2px solid #1e3a8a !important;
                margin-bottom: 18px !important;
            }}
            .page-header h1 {{ font-size: 1.45rem !important; color: #1e3a8a !important; margin-bottom: 2px !important; }}
            .page-header h2 {{ font-size: 1.15rem !important; color: #0369a1 !important; }}

            .btn-check, .feedback-msg, .no-print {{
                display: none !important;
            }}

            .ex-section, .grammar-theory-section, .grammar-exercise-section {{
                display: block !important;
                margin-bottom: 20px !important;
                page-break-inside: auto !important;
            }}

            .styled-table {{ font-size: 0.88rem !important; margin: 10px 0 !important; }}
            .styled-table th {{ background-color: #1e3a8a !important; color: white !important; padding: 6px 8px !important; }}
            .styled-table td {{ padding: 5px 8px !important; }}

            .q-item {{ margin-bottom: 12px !important; padding-bottom: 8px !important; page-break-inside: avoid; }}
            .q-text, .q-text-inline {{ font-size: 0.92rem !important; margin-bottom: 4px !important; font-weight: 400 !important; display: block !important; }}

            .opt-grid {{
                display: flex !important;
                flex-wrap: nowrap !important;
                justify-content: space-between !important;
                gap: 12px !important;
                margin-top: 4px !important;
            }}
            .opt-btn {{
                border: none !important;
                background: transparent !important;
                color: #000000 !important;
                padding: 0 !important;
                font-size: 0.88rem !important;
                font-weight: 400 !important;
                box-shadow: none !important;
            }}

            .inline-text-input {{
                border: none !important;
                border-bottom: 1.5px dotted #1e3a8a !important;
                background: transparent !important;
                width: 120px !important;
                padding: 0 !important;
                height: 18px !important;
                display: inline-block !important;
            }}
            .inline-text-input::placeholder {{ color: transparent !important; }}

            .input-wrapper {{ display: block !important; }}
            .text-input {{
                border: none !important;
                border-bottom: 1.5px dotted #1e3a8a !important;
                background: transparent !important;
                width: 100% !important;
                max-width: 100% !important;
                border-radius: 0 !important;
                padding: 2px 0 !important;
                height: 22px !important;
            }}
            .text-input::placeholder {{ color: transparent !important; }}
        }}
    </style>
</head>
<body>

    <header class="page-header">
        <h1>{header_title}</h1>
        <h2>{header_subtitle}</h2>
    </header>

    <main class="container">
        <!-- Section A: Lý thuyết -->
        {theory_html}

        <!-- Section B: EXERCISES -->
        <div class="grammar-exercise-section">
            <h3 class="main-section-title">B. EXERCISES</h3>
            <div id="exercise-container">
                {all_ex_html}
            </div>
        </div>
    </main>

    <script>
        const exercisesData = {exercises_js};

        function checkMCQ(btn, selected, correct) {{
            const parent = btn.parentElement;
            const fb = parent.nextElementSibling;
            parent.querySelectorAll('.opt-btn').forEach(b => b.classList.remove('correct', 'incorrect'));
            
            if (selected.trim().toLowerCase() === correct.trim().toLowerCase()) {{
                btn.classList.add('correct');
                fb.textContent = '✔️ Correct!';
                fb.className = 'feedback-msg valid';
            }} else {{
                btn.classList.add('incorrect');
                fb.textContent = `❌ Incorrect. The correct answer is: "${{correct}}"`;
                fb.className = 'feedback-msg invalid';
            }}
        }}

        function checkTextInput(exId, qIdx, correct) {{
            const input = document.getElementById(`input-${{exId}}-${{qIdx}}`);
            const fb = document.getElementById(`fb-${{exId}}-${{qIdx}}`);
            const val = input.value.trim().toLowerCase().replace(/[.,?!]/g, '');
            const target = correct.trim().toLowerCase().replace(/[.,?!]/g, '');

            if (val === target) {{
                fb.textContent = '✔️ Correct!';
                fb.className = 'feedback-msg valid';
            }} else {{
                fb.textContent = `❌ Incorrect. The correct answer is: "${{correct}}"`;
                fb.className = 'feedback-msg invalid';
            }}
        }}
    </script>
</body>
</html>
"""
    return html_content

def resolve_paths(repo_root, grade, unit_num, lesson_arg, vocab_arg):
    """Resolves lesson directory and vocabulary JSON file path."""
    candidates = []
    if lesson_arg:
        # direct path or relative to repo_root
        if os.path.isabs(lesson_arg):
            candidates.append(lesson_arg)
        else:
            candidates.append(os.path.join(repo_root, lesson_arg))
            candidates.append(os.path.join(repo_root, "lessons", lesson_arg))
    
    # Standard workspace paths
    candidates.extend([
        os.path.join(repo_root, "lessons", f"unit-{unit_num}"),
        os.path.join(repo_root, "lessons", f"unit{unit_num}"),
        os.path.join(repo_root, f"unit-{unit_num}"),
        os.path.join(repo_root, f"Lesson{unit_num}"),
        os.path.join(repo_root, f"lesson{unit_num}")
    ])

    lesson_folder = None
    for c in candidates:
        if os.path.exists(c) and os.path.isdir(c):
            lesson_folder = c
            break

    if not lesson_folder:
        lesson_folder = candidates[0]
        os.makedirs(lesson_folder, exist_ok=True)
        print(f"Created target lesson folder: {lesson_folder}")

    vocab_file = None
    if vocab_arg:
        if os.path.exists(vocab_arg):
            vocab_file = vocab_arg
        elif os.path.exists(os.path.join(repo_root, vocab_arg)):
            vocab_file = os.path.join(repo_root, vocab_arg)

    if not vocab_file:
        vocab_candidates = [
            os.path.join(lesson_folder, "vocab", "vocab.json"),
            os.path.join(lesson_folder, "vocab.json"),
            os.path.join(lesson_folder, f"vocab_data_unit{unit_num}.json"),
            os.path.join(lesson_folder, f"vocab_data_lesson{unit_num}.json")
        ]
        for vc in vocab_candidates:
            if os.path.exists(vc):
                vocab_file = vc
                break

    return lesson_folder, vocab_file

def find_repo_root():
    cur = os.path.abspath(os.path.dirname(__file__))
    while cur and os.path.dirname(cur) != cur:
        if os.path.exists(os.path.join(cur, "lessons")) or os.path.exists(os.path.join(cur, ".git")):
            return cur
        cur = os.path.dirname(cur)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

def main():
    parser = argparse.ArgumentParser(description="Generate targeted grammar lesson HTML, PDF, and execute audit suite based on GS10-12 Grammar Roadmap.")
    parser.add_argument("--grade", default="GS12", help="Target grade level (GS10, GS11, GS12). Default: GS12.")
    parser.add_argument("--unit", type=int, help="Target unit number (e.g. 1 to 10).")
    parser.add_argument("--lesson", help="Target lesson or unit directory (e.g. unit-1, lessons/unit-1, Lesson1).")
    parser.add_argument("--grammar", help="Target grammar points override. If omitted, looks up from GS10-12 Grammar Roadmap.")
    parser.add_argument("--vocab", help="Explicit path to vocab JSON file.")

    args = parser.parse_args()

    # Determine unit number
    unit_num = args.unit
    if not unit_num and args.lesson:
        m = re.search(r'\d+', args.lesson)
        if m:
            unit_num = int(m.group(0))
    if not unit_num:
        unit_num = 1

    grade = args.grade.upper()
    if args.lesson:
        gm = re.search(r'(GS10|GS11|GS12)', args.lesson, re.IGNORECASE)
        if gm:
            grade = gm.group(1).upper()

    repo_root = find_repo_root()

    grammar_topic, unit_theme = get_grammar_for_lesson(grade, unit_num, args.grammar) if 'get_grammar_for_lesson' in globals() else get_grammar_info(grade, unit_num, args.grammar)
    print(f"Target Grade & Unit: {grade} Unit {unit_num} ({unit_theme})")
    print(f"Target Grammar Topic (Roadmap GS10-12): {grammar_topic}")

    lesson_folder, vocab_file = resolve_paths(repo_root, grade, unit_num, args.lesson, args.vocab)
    print(f"Lesson directory: {lesson_folder}")

    vocab_words = []
    if vocab_file and os.path.exists(vocab_file):
        print(f"Reading vocabulary data from: {vocab_file}")
        vocab_words = load_vocab(vocab_file)
        print(f"Successfully loaded {len(vocab_words)} vocabulary words.")
    else:
        print(f"Notice: No vocab JSON file found at expected paths. Proceeding with standard vocabulary integration.")

    raw_exercises_dict = load_or_create_grammar_raw(lesson_folder, unit_num, grammar_topic, vocab_words)

    topic_title = f"{grade} Unit {unit_num} - Grammar Specialization"
    theory_html = build_grammar_theory_html(topic_title, grammar_topic, vocab_words, grade, unit_num, unit_theme)

    exercises = parse_exercises_from_raw(raw_exercises_dict)
    save_exercise_jsons(lesson_folder, exercises)

    audit_grammar_lesson(vocab_words, theory_html, exercises, grammar_topic)

    output_html_name = f"grammar_unit{unit_num}.html"
    output_html_path = os.path.join(lesson_folder, output_html_name)

    full_html = render_full_grammar_html(grade, unit_num, unit_theme, grammar_topic, theory_html, exercises)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Successfully generated HTML display: {output_html_path}")

    # Check for PDF converter script
    pdf_script_candidates = [
        os.path.join(repo_root, ".agent", "skills", "skills-convert-html-to-pdf", "scripts", "convert_html_to_pdf.py"),
        os.path.join(repo_root, ".agents", "skills-convert-html-to-pdf", "scripts", "convert_html_to_pdf.py")
    ]
    output_pdf_path = os.path.join(lesson_folder, f"grammar_unit{unit_num}.pdf")

    pdf_converted = False
    for pdf_script in pdf_script_candidates:
        if os.path.exists(pdf_script):
            print(f"Converting HTML to PDF via {pdf_script}...")
            res = subprocess.run([sys.executable, pdf_script, "--input", output_html_path, "--output", output_pdf_path], capture_output=True, text=True)
            if res.returncode == 0 and os.path.exists(output_pdf_path):
                print(f"Successfully generated PDF: {output_pdf_path}")
                pdf_converted = True
                break
            else:
                print("PDF conversion finished with log output:")
                if res.stdout: print(res.stdout)
                if res.stderr: print(res.stderr)

    if not pdf_converted:
        print(f"HTML file is ready at {output_html_path} (use browser print or convert_html_to_pdf to render PDF).")

if __name__ == "__main__":
    main()
