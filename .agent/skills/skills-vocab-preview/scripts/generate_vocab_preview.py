#!/usr/bin/env python3
"""
Vocab Preview Generator
Generates an interactive, standalone HTML preview for vocabulary (vocab.json)
and all exercise types (exercises/*.json) in a lesson Unit's vocab folder.
"""

import os
import sys
import json
import glob
import re
import argparse
from pathlib import Path
from html import escape


def load_json_file(file_path):
    """Safely load and parse a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Warning] Failed to load {file_path}: {e}", file=sys.stderr)
        return None


def extract_unit_info(vocab_dir):
    """Derive book/grade and unit name from path if possible."""
    path_obj = Path(vocab_dir).resolve()
    # Expecting path like .../data/gs-6/unit-7/vocab
    parts = path_obj.parts
    unit = "Unit"
    grade = ""
    for i, part in enumerate(parts):
        if re.match(r"^unit[-_]?\d+$", part, re.IGNORECASE):
            unit = part.replace("-", " ").title()
            if i > 0:
                prev = parts[i - 1]
                if re.match(r"^(gs|grade|tienganh)[-_]?\d+$", prev, re.IGNORECASE):
                    grade = prev.upper().replace("-", " ")
        elif re.match(r"^(gs|grade)[-_]?\d+$", part, re.IGNORECASE):
            grade = part.upper().replace("-", " ")
    
    title = f"{grade} - {unit}".strip(" - ")
    if not title:
        title = path_obj.name.title()
    return title


def build_html_preview(vocab_dir, output_file=None):
    vocab_path = Path(vocab_dir).resolve()
    if not vocab_path.exists() or not vocab_path.is_dir():
        raise ValueError(f"Target directory does not exist: {vocab_dir}")

    if output_file is None:
        output_file = vocab_path / "vocab_preview.html"
    else:
        output_file = Path(output_file).resolve()

    # Load vocab.json
    vocab_json_path = vocab_path / "vocab.json"
    vocab_data = []
    if vocab_json_path.exists():
        vocab_data = load_json_file(vocab_json_path) or []
    else:
        print(f"[Notice] vocab.json not found in {vocab_path}", file=sys.stderr)

    # Load all exercise files
    exercises_dir = vocab_path / "exercises"
    exercise_files = []
    exercises_data = []
    if exercises_dir.exists() and exercises_dir.is_dir():
        # Get sorted json files
        json_files = sorted(exercises_dir.glob("*.json"))
        for jf in json_files:
            data = load_json_file(jf)
            if data and isinstance(data, dict):
                data["_filename"] = jf.name
                exercises_data.append(data)
                exercise_files.append(jf.name)

    # Calculate statistics
    total_words = sum(len(g.get("words", [])) for g in vocab_data)
    total_groups = len(vocab_data)
    total_exercises = len(exercises_data)
    
    total_questions = 0
    for ex in exercises_data:
        q_list = ex.get("questions", [])
        if q_list:
            total_questions += len(q_list)
        elif "entries" in ex:
            # dictionary entries
            for entry in ex["entries"]:
                total_questions += len(entry.get("questions", []))
        elif "paragraph_parts" in ex:
            # paragraph blanks
            blanks = [p for p in ex.get("paragraph_parts", []) if isinstance(p, dict) and p.get("type") == "blank"]
            total_questions += len(blanks)

    unit_title = extract_unit_info(vocab_dir)

    # Serialize data for the interactive frontend
    vocab_json_str = json.dumps(vocab_data, ensure_ascii=False)
    exercises_json_str = json.dumps(exercises_data, ensure_ascii=False)

    html_content = generate_full_html(
        unit_title=unit_title,
        vocab_path_str=str(vocab_path),
        total_words=total_words,
        total_groups=total_groups,
        total_exercises=total_exercises,
        total_questions=total_questions,
        vocab_data=vocab_data,
        exercises_data=exercises_data,
        vocab_json_str=vocab_json_str,
        exercises_json_str=exercises_json_str
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[Success] Generated vocab preview HTML: {output_file}")
    print(f"          Words: {total_words} | Groups: {total_groups} | Exercises: {total_exercises} | Questions: {total_questions}")
    return str(output_file)


def generate_full_html(
    unit_title, vocab_path_str, total_words, total_groups, total_exercises, total_questions,
    vocab_data, exercises_data, vocab_json_str, exercises_json_str
):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(unit_title)} - Vocabulary & Exercises Preview</title>
  <style>
    :root {{
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --primary-light: #e0e7ff;
      --primary-dark: #3730a3;
      --secondary: #0ea5e9;
      --success: #10b981;
      --success-light: #d1fae5;
      --success-dark: #065f46;
      --warning: #f59e0b;
      --warning-light: #fef3c7;
      --danger: #ef4444;
      --danger-light: #fee2e2;
      --bg-main: #f8fafc;
      --bg-card: #ffffff;
      --bg-alt: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-subtle: #94a3b8;
      --border-color: #e2e8f0;
      --border-hover: #cbd5e1;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 16px;
      --radius-full: 9999px;
      --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-family);
      background-color: var(--bg-main);
      color: var(--text-main);
      line-height: 1.5;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }}

    /* Top App Header */
    header.app-header {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
    }}

    .header-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .brand-section {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: white;
      font-weight: 800;
      font-size: 14px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .header-titles h1 {{
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .header-titles p {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }}

    .search-box {{
      position: relative;
      width: 260px;
    }}

    .search-box input {{
      width: 100%;
      padding: 8px 12px 8px 34px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border-color);
      font-size: 13px;
      background: var(--bg-alt);
      transition: all 0.2s;
    }}

    .search-box input:focus {{
      outline: none;
      background: #fff;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-light);
    }}

    .search-box svg {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 16px;
      height: 16px;
      color: var(--text-muted);
    }}

    .mode-toggle-group {{
      display: flex;
      background: var(--bg-alt);
      padding: 3px;
      border-radius: var(--radius-full);
      border: 1px solid var(--border-color);
    }}

    .mode-btn {{
      padding: 6px 14px;
      border-radius: var(--radius-full);
      border: none;
      background: transparent;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .mode-btn.active {{
      background: white;
      color: var(--primary);
      box-shadow: var(--shadow-sm);
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: var(--radius-md);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid var(--border-color);
      background: white;
      color: var(--text-main);
      transition: all 0.2s;
    }}

    .btn:hover {{
      background: var(--bg-alt);
      border-color: var(--border-hover);
    }}

    .btn-primary {{
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }}

    .btn-primary:hover {{
      background: var(--primary-hover);
      border-color: var(--primary-hover);
    }}

    /* Layout Wrapper */
    .app-body {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px;
      display: flex;
      gap: 28px;
      width: 100%;
      flex: 1;
    }}

    /* Sidebar Navigation */
    aside.sidebar {{
      width: 290px;
      flex-shrink: 0;
      position: sticky;
      top: 80px;
      max-height: calc(100vh - 100px);
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding-right: 8px;
    }}

    aside.sidebar::-webkit-scrollbar {{
      width: 5px;
    }}
    aside.sidebar::-webkit-scrollbar-thumb {{
      background: var(--border-color);
      border-radius: 4px;
    }}

    .stats-card {{
      background: linear-gradient(135deg, #4f46e5, #0ea5e9);
      color: white;
      padding: 16px;
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow);
    }}

    .stats-card h3 {{
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }}

    .stat-box {{
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(4px);
      padding: 10px;
      border-radius: var(--radius-md);
      text-align: center;
    }}

    .stat-number {{
      font-size: 20px;
      font-weight: 800;
    }}

    .stat-label {{
      font-size: 11px;
      opacity: 0.9;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .nav-group {{
      background: var(--bg-card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border-color);
      padding: 14px;
      box-shadow: var(--shadow-sm);
    }}

    .nav-group-title {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .nav-links {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .nav-link {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      color: var(--text-main);
      text-decoration: none;
      font-size: 13px;
      font-weight: 500;
      transition: all 0.15s;
    }}

    .nav-link:hover, .nav-link.active {{
      background: var(--primary-light);
      color: var(--primary-dark);
      font-weight: 600;
    }}

    .nav-link .badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: var(--radius-full);
      background: var(--bg-alt);
      color: var(--text-muted);
    }}

    .nav-link.active .badge {{
      background: white;
      color: var(--primary);
    }}

    /* Main Content */
    main.main-content {{
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 36px;
    }}

    /* Section Styles */
    section.preview-section {{
      background: var(--bg-card);
      border-radius: var(--radius-lg);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
    }}

    .section-header {{
      padding: 20px 24px;
      border-bottom: 1px solid var(--border-color);
      background: linear-gradient(to right, #fafafa, #ffffff);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}

    .section-title-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .section-icon {{
      width: 40px;
      height: 40px;
      border-radius: var(--radius-md);
      background: var(--primary-light);
      color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }}

    .section-header h2 {{
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .section-header p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* Vocabulary Group & Card Layout */
    .vocab-groups-container {{
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 32px;
    }}

    .vocab-group-block {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .group-heading {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 16px;
      font-weight: 700;
      color: var(--text-main);
      padding-bottom: 8px;
      border-bottom: 2px solid var(--primary-light);
    }}

    .group-pill {{
      background: var(--primary-light);
      color: var(--primary-dark);
      font-size: 12px;
      padding: 2px 10px;
      border-radius: var(--radius-full);
      font-weight: 600;
    }}

    .vocab-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 18px;
    }}

    .word-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: relative;
    }}

    .word-card:hover {{
      border-color: var(--primary);
      box-shadow: var(--shadow);
      transform: translateY(-2px);
    }}

    .word-card-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 10px;
    }}

    .word-title-wrap {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .word-english {{
      font-size: 17px;
      font-weight: 700;
      color: var(--primary-dark);
    }}

    .phonetics-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: var(--text-muted);
      font-family: 'Courier New', Courier, monospace;
      flex-wrap: wrap;
    }}

    .phonetic-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: var(--bg-alt);
      padding: 2px 6px;
      border-radius: 4px;
    }}

    .audio-btn {{
      background: var(--primary-light);
      border: none;
      color: var(--primary-dark);
      width: 32px;
      height: 32px;
      border-radius: var(--radius-full);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
      flex-shrink: 0;
    }}

    .audio-btn:hover {{
      background: var(--primary);
      color: white;
      transform: scale(1.08);
    }}

    .audio-btn svg {{
      width: 16px;
      height: 16px;
    }}

    .word-meaning {{
      background: #f8fafc;
      border-left: 3px solid var(--secondary);
      padding: 8px 12px;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      font-size: 14px;
      color: #1e293b;
      font-weight: 500;
    }}

    .pos-tag {{
      display: inline-block;
      font-weight: 700;
      color: var(--secondary);
      margin-right: 4px;
    }}

    .word-examples {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 13px;
      padding-top: 4px;
      border-top: 1px dashed var(--border-color);
    }}

    .example-en {{
      color: #334155;
      font-style: italic;
    }}

    .example-vi {{
      color: var(--text-muted);
      font-size: 12px;
    }}

    .word-image-wrap {{
      margin-top: 6px;
      border-radius: var(--radius-sm);
      overflow: hidden;
      max-height: 140px;
      background: var(--bg-alt);
      position: relative;
    }}

    .word-image {{
      width: 100%;
      height: 140px;
      object-fit: cover;
      display: block;
    }}

    .img-placeholder {{
      height: 70px;
      background: #f1f5f9;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      color: var(--text-muted);
      font-size: 12px;
      border-radius: var(--radius-sm);
      border: 1px dashed var(--border-color);
    }}

    /* Exercise Card Styles */
    .exercise-block {{
      padding: 24px;
      border-bottom: 1px solid var(--border-color);
    }}

    .exercise-block:last-child {{
      border-bottom: none;
    }}

    .exercise-header-row {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}

    .exercise-title-meta {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .exercise-badge-row {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .ex-id-badge {{
      background: var(--primary);
      color: white;
      font-weight: 700;
      font-size: 12px;
      padding: 2px 8px;
      border-radius: var(--radius-sm);
    }}

    .ex-type-badge {{
      background: var(--bg-alt);
      color: var(--text-muted);
      font-size: 12px;
      font-family: monospace;
      padding: 2px 8px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-color);
    }}

    .exercise-title-meta h3 {{
      font-size: 17px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .exercise-desc {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    .ex-check-btn {{
      padding: 6px 14px;
      background: var(--primary-light);
      color: var(--primary-dark);
      border: 1px solid var(--primary-light);
      border-radius: var(--radius-md);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}

    .ex-check-btn:hover {{
      background: var(--primary);
      color: white;
    }}

    .score-badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      background: var(--success-light);
      color: var(--success-dark);
    }}

    /* Questions Layout */
    .questions-list {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .question-item {{
      background: var(--bg-main);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      transition: border-color 0.2s;
    }}

    .question-item:hover {{
      border-color: var(--border-hover);
    }}

    .q-stem-row {{
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
    }}

    .q-num {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 24px;
      height: 24px;
      background: white;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-full);
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      flex-shrink: 0;
    }}

    .q-text {{
      flex: 1;
      white-space: pre-line;
    }}

    .target-highlight {{
      color: var(--primary);
      font-weight: 700;
      text-decoration: underline;
      text-underline-offset: 3px;
    }}

    /* Options List */
    .options-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 10px;
      margin-left: 34px;
    }}

    .option-label {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      background: white;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      font-size: 13px;
      cursor: pointer;
      transition: all 0.15s;
      position: relative;
    }}

    .option-label:hover {{
      border-color: var(--primary);
      background: #fafafa;
    }}

    .option-label input[type="radio"] {{
      accent-color: var(--primary);
      width: 16px;
      height: 16px;
    }}

    .option-letter {{
      font-weight: 700;
      color: var(--text-muted);
      font-size: 12px;
      min-width: 16px;
    }}

    .option-text {{
      flex: 1;
    }}

    /* Answer Key Highlights */
    body.mode-review .option-label.is-correct {{
      background: var(--success-light) !important;
      border-color: var(--success) !important;
      color: var(--success-dark) !important;
      font-weight: 600;
    }}

    body.mode-review .option-label.is-correct::after {{
      content: '✓';
      font-weight: 800;
      color: var(--success);
      margin-left: 6px;
    }}

    body.mode-practice .option-label.user-correct {{
      background: var(--success-light) !important;
      border-color: var(--success) !important;
      color: var(--success-dark) !important;
    }}

    body.mode-practice .option-label.user-wrong {{
      background: var(--danger-light) !important;
      border-color: var(--danger) !important;
      color: var(--danger) !important;
    }}

    /* Inputs for Fill In Blanks / Translation */
    .blank-input-wrap {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-left: 34px;
      flex-wrap: wrap;
    }}

    .blank-input {{
      padding: 8px 12px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      font-size: 13px;
      min-width: 220px;
      background: white;
      transition: all 0.2s;
    }}

    .blank-input:focus {{
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px var(--primary-light);
    }}

    .correct-key-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      background: var(--success-light);
      color: var(--success-dark);
      font-size: 13px;
      font-weight: 600;
      border: 1px solid #a7f3d0;
    }}

    body.mode-practice .correct-key-badge {{
      display: none;
    }}

    body.mode-practice .correct-key-badge.revealed {{
      display: inline-flex;
    }}

    /* Word Box Tag Cloud */
    .word-box-container {{
      background: #eff6ff;
      border: 1px dashed #93c5fd;
      border-radius: var(--radius-md);
      padding: 14px;
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .word-box-label {{
      font-size: 11px;
      font-weight: 700;
      color: #1e40af;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .word-box-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .word-chip {{
      background: white;
      border: 1px solid #bfdbfe;
      color: #1e3a8a;
      padding: 4px 10px;
      border-radius: var(--radius-full);
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }}

    /* Paragraph Fill Passage */
    .paragraph-passage {{
      background: white;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 20px;
      font-size: 15px;
      line-height: 2;
      color: var(--text-main);
    }}

    .inline-blank {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      vertical-align: middle;
      margin: 0 4px;
    }}

    .inline-blank-num {{
      font-size: 11px;
      font-weight: 700;
      background: var(--primary-light);
      color: var(--primary-dark);
      padding: 2px 6px;
      border-radius: 4px;
    }}

    .inline-blank-input {{
      padding: 4px 8px;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      font-size: 14px;
      width: 140px;
    }}

    body.mode-review .inline-blank-input {{
      background: var(--success-light);
      border-color: var(--success);
      color: var(--success-dark);
      font-weight: 600;
    }}

    /* Dictionary Entry Oxford Style */
    .dict-entry-card {{
      background: white;
      border: 1px solid var(--border-color);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-md);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .dict-header {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .dict-word {{
      font-size: 20px;
      font-weight: 800;
      color: var(--primary-dark);
    }}

    .dict-pos {{
      font-style: italic;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 600;
    }}

    .dict-phonetic {{
      font-family: monospace;
      color: var(--text-muted);
      font-size: 13px;
    }}

    .dict-def {{
      font-size: 14px;
      color: #1e293b;
      padding-left: 10px;
      border-left: 2px solid var(--border-color);
    }}

    .dict-collocations {{
      background: var(--bg-alt);
      border-radius: var(--radius-sm);
      padding: 12px 16px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .dict-collocations-title {{
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .dict-bullet {{
      font-size: 13px;
      color: #334155;
    }}

    .dict-bullet strong {{
      color: var(--primary);
      background: rgba(79, 70, 229, 0.08);
      padding: 1px 4px;
      border-radius: 3px;
    }}

    .dict-practice-title {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-top: 6px;
    }}

    /* Word Families Table */
    .wf-table-wrap {{
      overflow-x: auto;
      background: white;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
    }}

    table.wf-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: left;
    }}

    table.wf-table th {{
      background: var(--bg-alt);
      padding: 12px 14px;
      font-weight: 700;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border-color);
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.5px;
    }}

    table.wf-table td {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
    }}

    table.wf-table tr:last-child td {{
      border-bottom: none;
    }}

    table.wf-table tr:hover td {{
      background: #f8fafc;
    }}

    .wf-base-chip {{
      font-weight: 700;
      color: var(--primary-dark);
      background: var(--primary-light);
      padding: 2px 8px;
      border-radius: var(--radius-sm);
      display: inline-block;
    }}

    .wf-tag {{
      display: inline-block;
      background: var(--bg-alt);
      padding: 2px 6px;
      border-radius: 4px;
      margin: 2px;
      font-size: 12px;
    }}

    /* Signs and Notices Box */
    .sign-box {{
      background: white;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 16px;
      display: flex;
      align-items: center;
      gap: 16px;
      background: linear-gradient(to right, #fff, #f8fafc);
    }}

    .sign-visual {{
      width: 90px;
      height: 90px;
      border-radius: var(--radius-md);
      background: #fef3c7;
      border: 2px solid #fde68a;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 6px;
      text-align: center;
      flex-shrink: 0;
      color: #92400e;
    }}

    .sign-visual svg {{
      width: 32px;
      height: 32px;
    }}

    .sign-desc-text {{
      font-size: 13px;
      color: #475569;
      font-style: italic;
      line-height: 1.4;
    }}

    /* Sentence Ordering Box */
    .ordering-parts {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-left: 34px;
      margin-bottom: 8px;
    }}

    .order-sentence-pill {{
      background: white;
      border: 1px solid var(--border-color);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      color: #334155;
    }}

    .ordered-preview-text {{
      margin-left: 34px;
      padding: 10px 14px;
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: var(--radius-sm);
      font-size: 13px;
      color: #166534;
      line-height: 1.5;
    }}

    body.mode-practice .ordered-preview-text {{
      display: none;
    }}

    body.mode-practice .ordered-preview-text.revealed {{
      display: block;
    }}

    /* Word Formation root badge */
    .base-root-badge {{
      display: inline-block;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      color: #334155;
      font-family: monospace;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 13px;
      margin-left: 6px;
    }}

    /* Footer */
    footer.app-footer {{
      margin-top: auto;
      border-top: 1px solid var(--border-color);
      background: white;
      padding: 16px 24px;
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
    }}

    /* Print media styles */
    @media print {{
      header.app-header, aside.sidebar, .mode-toggle-group, .btn, .audio-btn, .ex-check-btn, .search-box {{
        display: none !important;
      }}
      body {{
        background: white;
        color: black;
      }}
      .app-body {{
        padding: 0;
        margin: 0;
      }}
      section.preview-section {{
        box-shadow: none;
        border: none;
        margin-bottom: 24px;
        page-break-inside: avoid;
      }}
      .correct-key-badge {{
        border: 1px solid #000;
        background: #eee;
        color: #000;
      }}
    }}

    /* Responsive adjustments */
    @media (max-width: 1024px) {{
      .app-body {{
        flex-direction: column;
      }}
      aside.sidebar {{
        width: 100%;
        position: static;
        max-height: none;
      }}
    }}
  </style>
</head>
<body class="mode-review">

  <!-- Header -->
  <header class="app-header">
    <div class="header-container">
      <div class="brand-section">
        <div class="logo-badge">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          VOCAB PREVIEW
        </div>
        <div class="header-titles">
          <h1>{escape(unit_title)}</h1>
          <p>{escape(vocab_path_str)}</p>
        </div>
      </div>

      <div class="header-actions">
        <!-- Live Search -->
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input type="text" id="liveSearchInput" placeholder="Tìm từ vựng, câu hỏi..." oninput="handleSearch(this.value)">
        </div>

        <!-- Mode Toggle -->
        <div class="mode-toggle-group">
          <button class="mode-btn active" id="btnModeReview" onclick="setMode('review')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            Xem Đáp Án
          </button>
          <button class="mode-btn" id="btnModePractice" onclick="setMode('practice')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 20h9"/>
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
            </svg>
            Làm Bài
          </button>
        </div>

        <!-- Print Button -->
        <button class="btn" onclick="window.print()" title="In hoặc Xuất PDF">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 6 2 18 2 18 9"/>
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/>
            <rect x="6" y="14" width="12" height="8"/>
          </svg>
          In
        </button>
      </div>
    </div>
  </header>

  <!-- Body Layout -->
  <div class="app-body">
    <!-- Sidebar Navigation -->
    <aside class="sidebar">
      <!-- Quick Stats Card -->
      <div class="stats-card">
        <h3>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
          Tổng Quan Bài Học
        </h3>
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-number">{total_words}</div>
            <div class="stat-label">Từ Vựng</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{total_groups}</div>
            <div class="stat-label">Nhóm Từ</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{total_exercises}</div>
            <div class="stat-label">Bài Tập</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{total_questions}</div>
            <div class="stat-label">Câu Hỏi</div>
          </div>
        </div>
      </div>

      <!-- Navigation Links -->
      <div class="nav-group">
        <div class="nav-group-title">
          <span>Nội Dung</span>
          <span class="badge">{1 + total_exercises} mục</span>
        </div>
        <ul class="nav-links">
          <li>
            <a href="#section-vocab" class="nav-link active" onclick="highlightNav(this)">
              <span>📚 Bảng Từ Vựng</span>
              <span class="badge">{total_words} từ</span>
            </a>
          </li>
          {''.join(render_sidebar_links(exercises_data))}
        </ul>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content" id="mainContentArea">
      <!-- Vocabulary Section -->
      <section class="preview-section" id="section-vocab">
        <div class="section-header">
          <div class="section-title-wrap">
            <div class="section-icon">📖</div>
            <div>
              <h2>Danh Sách Từ Vựng Trọng Tâm</h2>
              <p>{total_words} từ vựng thuộc {total_groups} nhóm chủ đề</p>
            </div>
          </div>
        </div>
        <div class="vocab-groups-container">
          {render_vocab_groups(vocab_data)}
        </div>
      </section>

      <!-- Exercises Section -->
      <section class="preview-section" id="section-exercises">
        <div class="section-header">
          <div class="section-title-wrap">
            <div class="section-icon">✍️</div>
            <div>
              <h2>Hệ Thống Bài Tập Thực Hành (Exercises)</h2>
              <p>{total_exercises} dạng bài tập - {total_questions} câu hỏi luyện tập</p>
            </div>
          </div>
        </div>
        <div>
          {render_all_exercises(exercises_data)}
        </div>
      </section>
    </main>
  </div>

  <!-- Footer -->
  <footer class="app-footer">
    <p>Vocab Preview &bull; Antigravity Skills &bull; {escape(unit_title)}</p>
  </footer>

  <!-- Embedded Client Logic -->
  <script>
    // State
    let currentMode = 'review'; // 'review' or 'practice'

    function setMode(mode) {{
      currentMode = mode;
      document.body.className = mode === 'review' ? 'mode-review' : 'mode-practice';
      document.getElementById('btnModeReview').classList.toggle('active', mode === 'review');
      document.getElementById('btnModePractice').classList.toggle('active', mode === 'practice');
    }}

    // Text to Speech
    function speakText(text, lang = 'en-GB') {{
      if (!('speechSynthesis' in window)) {{
        alert('Trình duyệt không hỗ trợ Web Speech API.');
        return;
      }}
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }}

    // Interactive checking per exercise
    function checkExercise(exIndex) {{
      const exBlock = document.getElementById('ex-block-' + exIndex);
      if (!exBlock) return;
      
      let total = 0;
      let correctCount = 0;

      // Check MCQ radio options
      const qItems = exBlock.querySelectorAll('.question-item');
      qItems.forEach(q => {{
        const correctAns = q.getAttribute('data-correct');
        const radios = q.querySelectorAll('input[type="radio"]');
        if (radios.length > 0) {{
          total++;
          let userVal = '';
          radios.forEach(r => {{
            const lbl = r.closest('.option-label');
            lbl.classList.remove('user-correct', 'user-wrong');
            if (r.checked) {{
              userVal = r.value;
            }}
          }});

          radios.forEach(r => {{
            const lbl = r.closest('.option-label');
            if (r.checked) {{
              if (r.value.trim().toLowerCase() === (correctAns || '').trim().toLowerCase()) {{
                lbl.classList.add('user-correct');
                correctCount++;
              }} else {{
                lbl.classList.add('user-wrong');
              }}
            }} else if (r.value.trim().toLowerCase() === (correctAns || '').trim().toLowerCase()) {{
              // Show correct choice
              lbl.classList.add('user-correct');
            }}
          }});
        }}

        // Check text inputs
        const inputs = q.querySelectorAll('input.blank-input');
        inputs.forEach(inp => {{
          total++;
          const target = inp.getAttribute('data-correct') || '';
          const keyBadge = q.querySelector('.correct-key-badge');
          if (keyBadge) keyBadge.classList.add('revealed');
          
          if (inp.value.trim().toLowerCase() === target.trim().toLowerCase()) {{
            inp.style.borderColor = 'var(--success)';
            inp.style.backgroundColor = 'var(--success-light)';
            correctCount++;
          }} else {{
            inp.style.borderColor = 'var(--danger)';
            inp.style.backgroundColor = 'var(--danger-light)';
          }}
        }});

        // Paragraph fill blanks
        const inlineInps = q.querySelectorAll('input.inline-blank-input');
        inlineInps.forEach(inp => {{
          total++;
          const target = inp.getAttribute('data-correct') || '';
          if (inp.value.trim().toLowerCase() === target.trim().toLowerCase()) {{
            inp.style.borderColor = 'var(--success)';
            inp.style.backgroundColor = 'var(--success-light)';
            correctCount++;
          }} else {{
            inp.style.borderColor = 'var(--danger)';
            inp.style.backgroundColor = 'var(--danger-light)';
          }}
        }});

        // Sentence ordering preview reveal
        const ordPreview = q.querySelector('.ordered-preview-text');
        if (ordPreview) ordPreview.classList.add('revealed');
      }});

      // Update score display
      const scoreBadge = document.getElementById('score-badge-' + exIndex);
      if (scoreBadge) {{
        scoreBadge.style.display = 'inline-flex';
        scoreBadge.textContent = 'Kết quả: ' + correctCount + ' / ' + total;
      }}
    }}

    // Real-time search filter
    function handleSearch(query) {{
      const q = query.trim().toLowerCase();
      // Search in words
      const wordCards = document.querySelectorAll('.word-card');
      wordCards.forEach(card => {{
        const text = card.textContent.toLowerCase();
        card.style.display = (!q || text.includes(q)) ? '' : 'none';
      }});

      // Search in questions
      const qItems = document.querySelectorAll('.question-item');
      qItems.forEach(item => {{
        const text = item.textContent.toLowerCase();
        item.style.display = (!q || text.includes(q)) ? '' : 'none';
      }});
    }}

    function highlightNav(el) {{
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      el.classList.add('active');
    }}
  </script>
</body>
</html>
"""


def render_sidebar_links(exercises_data):
    links = []
    for idx, ex in enumerate(exercises_data):
        fn = ex.get("_filename", f"ex_{idx+1}")
        num_prefix = fn.split("_")[0]
        title = ex.get("title", f"Exercise {idx+1}")
        # Shorten title if too long
        short_title = title if len(title) <= 24 else title[:22] + "..."
        
        q_count = 0
        if "questions" in ex:
            q_count = len(ex["questions"])
        elif "entries" in ex:
            for entry in ex["entries"]:
                q_count += len(entry.get("questions", []))
        elif "paragraph_parts" in ex:
            q_count = len([p for p in ex.get("paragraph_parts", []) if isinstance(p, dict) and p.get("type") == "blank"])

        link_html = f"""
          <li>
            <a href="#ex-block-{idx}" class="nav-link" onclick="highlightNav(this)">
              <span>{escape(num_prefix)}. {escape(short_title)}</span>
              <span class="badge">{q_count}</span>
            </a>
          </li>"""
        links.append(link_html)
    return links


def render_vocab_groups(vocab_data):
    if not vocab_data:
        return "<p class='text-muted'>Không tìm thấy dữ liệu từ vựng trong vocab.json.</p>"

    blocks = []
    for g_idx, group in enumerate(vocab_data):
        group_name = group.get("group", f"Nhóm {g_idx+1}")
        words = group.get("words", [])
        
        card_htmls = []
        for word in words:
            en_word = word.get("english_word", "")
            pr_uk = word.get("pronunciation_british", "")
            pr_us = word.get("pronunciation_american", "")
            meaning = word.get("vietnamese_meaning", "")
            ex_en = word.get("example_sentence_en", "")
            ex_vi = word.get("example_sentence_vi", "")
            img_path = word.get("image", "")

            # Format POS tag if present e.g. (n), (v), (adj)
            pos_match = re.match(r"^\s*(\([a-zA-Z,.\s]+\))\s*:\s*(.*)$", meaning)
            if pos_match:
                formatted_meaning = f"<span class='pos-tag'>{escape(pos_match.group(1))}</span> {escape(pos_match.group(2))}"
            else:
                formatted_meaning = escape(meaning)

            # Phonics row
            phonics_parts = []
            if pr_uk:
                phonics_parts.append(f"<span class='phonetic-badge'>🇬🇧 {escape(pr_uk)}</span>")
            if pr_us:
                phonics_parts.append(f"<span class='phonetic-badge'>🇺🇸 {escape(pr_us)}</span>")
            phonics_html = "".join(phonics_parts)

            # Safe string for js speech
            safe_speak_word = en_word.replace("'", "\\'")
            safe_speak_sentence = ex_en.replace("'", "\\'")

            # Image section
            img_html = ""
            if img_path:
                img_html = f"""
                <div class="word-image-wrap">
                  <img src="{escape(img_path)}" alt="{escape(en_word)}" class="word-image"
                       onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
                  <div class="img-placeholder" style="display:none;">
                    <span>🖼️ {escape(en_word)}</span>
                  </div>
                </div>"""

            card = f"""
            <div class="word-card">
              <div class="word-card-top">
                <div class="word-title-wrap">
                  <div class="word-english">{escape(en_word)}</div>
                  <div class="phonetics-row">{phonics_html}</div>
                </div>
                <button class="audio-btn" onclick="speakText('{safe_speak_word}', 'en-GB')" title="Nghe phát âm từ">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
                    <path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/>
                  </svg>
                </button>
              </div>

              <div class="word-meaning">
                {formatted_meaning}
              </div>

              <div class="word-examples">
                <div class="example-en">
                  "{escape(ex_en)}"
                  <button style="background:none; border:none; cursor:pointer; color:var(--primary); margin-left:4px;" 
                          onclick="speakText('{safe_speak_sentence}', 'en-GB')" title="Nghe câu ví dụ">🔊</button>
                </div>
                <div class="example-vi">{escape(ex_vi)}</div>
              </div>

              {img_html}
            </div>"""
            card_htmls.append(card)

        block = f"""
        <div class="vocab-group-block">
          <div class="group-heading">
            <span>{escape(group_name)}</span>
            <span class="group-pill">{len(words)} từ</span>
          </div>
          <div class="vocab-grid">
            {''.join(card_htmls)}
          </div>
        </div>"""
        blocks.append(block)

    return "".join(blocks)


def render_all_exercises(exercises_data):
    if not exercises_data:
        return "<p class='text-muted' style='padding:24px;'>Chưa có file bài tập nào trong thư mục exercises/.</p>"

    rendered = []
    for idx, ex in enumerate(exercises_data):
        fn = ex.get("_filename", "")
        ex_id = ex.get("id", str(idx + 1))
        ex_type = ex.get("type", "")
        ex_title = ex.get("title", f"Exercise {idx+1}")
        ex_desc = ex.get("description", "")

        body_html = render_single_exercise_body(ex, idx)

        block = f"""
        <div class="exercise-block" id="ex-block-{idx}">
          <div class="exercise-header-row">
            <div class="exercise-title-meta">
              <div class="exercise-badge-row">
                <span class="ex-id-badge">#{escape(str(ex_id))}</span>
                <span class="ex-type-badge">{escape(ex_type)}</span>
                <span style="font-size:11px; color:var(--text-muted); font-family:monospace;">{escape(fn)}</span>
              </div>
              <h3>{escape(ex_title)}</h3>
              <p class="exercise-desc">{escape(ex_desc)}</p>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="score-badge" id="score-badge-{idx}" style="display:none;"></span>
              <button class="ex-check-btn" onclick="checkExercise({idx})">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Kiểm Tra Đáp Án
              </button>
            </div>
          </div>
          {body_html}
        </div>"""
        rendered.append(block)

    return "".join(rendered)


def format_underlined_target(text):
    """Replace [target] with span styled as underline highlight."""
    if not text:
        return ""
    # Safe escape first, but preserve brackets for regex
    escaped = escape(text)
    return re.sub(r"\[(.*?)\]", r"<span class='target-highlight'>\1</span>", escaped)


def render_single_exercise_body(ex, ex_index):
    ex_type = ex.get("type", "")

    # 1. Multiple Choice (Direct, Sentence, Conversation, Closest, Opposite, Signs, etc.)
    if ex_type in ("multiple_choice", "sentence_ordering_multiple_choice", "word_families_mcq"):
        return render_multiple_choice_body(ex, ex_index)

    # 2. Signs and Notices
    elif ex_type == "signs_and_notices":
        return render_signs_and_notices_body(ex, ex_index)

    # 3. Pic to Word
    elif ex_type == "pic_to_word":
        return render_pic_to_word_body(ex, ex_index)

    # 4. Write English Words
    elif ex_type == "write_english_words":
        return render_write_english_words_body(ex, ex_index)

    # 5. Fill in Blanks
    elif ex_type == "fill_in_blanks":
        return render_fill_in_blanks_body(ex, ex_index)

    # 6. Paragraph Fill
    elif ex_type == "paragraph_fill":
        return render_paragraph_fill_body(ex, ex_index)

    # 7. Dictionary Entry
    elif ex_type == "dictionary_entry":
        return render_dictionary_entry_body(ex, ex_index)

    # 8. Word Families Table
    elif ex_type == "word_families_table":
        return render_word_families_table_body(ex, ex_index)

    # 9. Word Formation
    elif ex_type == "word_formation":
        return render_word_formation_body(ex, ex_index)

    # 10. Translation
    elif ex_type == "translate_sentences":
        return render_translate_sentences_body(ex, ex_index)

    else:
        # Fallback generic renderer
        return render_generic_questions_body(ex, ex_index)


def render_multiple_choice_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        text = q.get("text", "")
        correct_answer = q.get("correct_answer", "")
        options = q.get("options", [])
        sentences = q.get("sentences", []) # for sentence ordering

        # If sentence ordering
        ordering_block = ""
        ordered_passage_text = ""
        if sentences:
            p_items = "".join(f"<div class='order-sentence-pill'>{escape(s)}</div>" for s in sentences)
            ordering_block = f"<div class='ordering-parts'>{p_items}</div>"
            
            # Form reconstructed passage from correct_answer e.g. "b-c-a-d"
            letter_order = correct_answer.split("-")
            sentence_map = {}
            for s in sentences:
                m = re.match(r"^([a-d])\.\s*(.*)$", s.strip(), re.IGNORECASE)
                if m:
                    sentence_map[m.group(1).lower()] = m.group(2)
            ordered_pieces = [sentence_map.get(letter.lower(), "") for letter in letter_order if letter.lower() in sentence_map]
            if ordered_pieces:
                ordered_passage_text = f"<div class='ordered-preview-text'><strong>Đoạn văn hoàn chỉnh:</strong> {' '.join(ordered_pieces)}</div>"

        # Options HTML
        opt_htmls = []
        letters = ["A", "B", "C", "D", "E"]
        for opt_idx, opt in enumerate(options):
            letter = letters[opt_idx] if opt_idx < len(letters) else str(opt_idx + 1)
            is_correct = (opt.strip().lower() == correct_answer.strip().lower())
            correct_class = "is-correct" if is_correct else ""

            opt_markup = f"""
            <label class="option-label {correct_class}">
              <input type="radio" name="q_{ex_index}_{q_idx}" value="{escape(opt)}" />
              <span class="option-letter">{letter}.</span>
              <span class="option-text">{escape(opt)}</span>
            </label>"""
            opt_htmls.append(opt_markup)

        stem_content = format_underlined_target(text) if text else "Sắp xếp các câu sau thành đoạn văn logic:"

        q_item = f"""
        <div class="question-item" data-correct="{escape(correct_answer)}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">{stem_content}</div>
          </div>
          {ordering_block}
          <div class="options-grid">
            {''.join(opt_htmls)}
          </div>
          {ordered_passage_text}
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_signs_and_notices_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        sign_type = q.get("sign_type", "")
        sign_text = q.get("sign_text", "")
        question_stem = q.get("question", "What does the sign say?")
        options = q.get("options", [])
        correct_answer = q.get("correct_answer", "")

        # Options HTML
        opt_htmls = []
        letters = ["A", "B", "C", "D"]
        for opt_idx, opt in enumerate(options):
            letter = letters[opt_idx] if opt_idx < len(letters) else str(opt_idx + 1)
            is_correct = (opt.strip().lower() == correct_answer.strip().lower())
            correct_class = "is-correct" if is_correct else ""

            opt_markup = f"""
            <label class="option-label {correct_class}">
              <input type="radio" name="sign_q_{ex_index}_{q_idx}" value="{escape(opt)}" />
              <span class="option-letter">{letter}.</span>
              <span class="option-text">{escape(opt)}</span>
            </label>"""
            opt_htmls.append(opt_markup)

        q_item = f"""
        <div class="question-item" data-correct="{escape(correct_answer)}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">
              <strong>{escape(question_stem)}</strong>
            </div>
          </div>
          <div class="sign-box">
            <div class="sign-visual">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <span style="font-size:10px; font-weight:700; text-transform:uppercase; margin-top:2px;">SIGN</span>
            </div>
            <div class="sign-desc-text">
              <strong>Mô tả biển báo:</strong> "{escape(sign_text)}"
            </div>
          </div>
          <div class="options-grid">
            {''.join(opt_htmls)}
          </div>
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_pic_to_word_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        img_path = q.get("image", "")
        correct_answer = q.get("correct_answer", "")

        q_item = f"""
        <div class="question-item" data-correct="{escape(correct_answer)}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">Nhìn hình và viết từ tiếng Anh tương ứng:</div>
          </div>
          <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap; margin-left:34px;">
            <div style="width:120px; height:90px; background:#f1f5f9; border-radius:6px; overflow:hidden; border:1px solid var(--border-color); display:flex; align-items:center; justify-content:center;">
              <img src="{escape(img_path)}" alt="Pic" style="width:100%; height:100%; object-fit:cover;"
                   onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
              <div style="display:none; flex-direction:column; align-items:center; font-size:11px; color:var(--text-muted);">
                <span>🖼️ Image</span>
              </div>
            </div>
            <div class="blank-input-wrap" style="margin-left:0;">
              <input type="text" class="blank-input" placeholder="Type word here..." data-correct="{escape(correct_answer)}" />
              <span class="correct-key-badge">✓ Đáp án: <strong>{escape(correct_answer)}</strong></span>
            </div>
          </div>
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_write_english_words_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        parts = q.get("parts", [])

        parts_html = []
        for p_idx, part in enumerate(parts):
            vi = part.get("vietnamese", "")
            correct_answer = part.get("correct_answer", "")
            p_markup = f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px; flex-wrap:wrap;">
              <span style="font-weight:600; min-width:180px; color:#334155;">{p_idx+1}. {escape(vi)}:</span>
              <input type="text" class="blank-input" placeholder="Từ tiếng Anh..." data-correct="{escape(correct_answer)}" />
              <span class="correct-key-badge">✓ <strong>{escape(correct_answer)}</strong></span>
            </div>"""
            parts_html.append(p_markup)

        q_item = f"""
        <div class="question-item">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">Viết từ tiếng Anh tương ứng với nghĩa tiếng Việt:</div>
          </div>
          <div style="margin-left:34px;">
            {''.join(parts_html)}
          </div>
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_fill_in_blanks_body(ex, ex_index):
    word_box = ex.get("word_box", [])
    questions = ex.get("questions", [])

    # Word box chips
    word_box_html = ""
    if word_box:
        chips = "".join(f"<span class='word-chip'>{escape(w)}</span>" for w in word_box)
        word_box_html = f"""
        <div class="word-box-container">
          <div class="word-box-label">📦 Hộp từ vựng gợi ý (Word Box)</div>
          <div class="word-box-chips">{chips}</div>
        </div>"""

    q_htmls = []
    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        text = q.get("text", "")
        correct_answer = q.get("correct_answer", "")

        # Highlight blanks
        display_text = re.sub(r"_{3,}", "__________", text)

        q_item = f"""
        <div class="question-item" data-correct="{escape(correct_answer)}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">{escape(display_text)}</div>
          </div>
          <div class="blank-input-wrap">
            <input type="text" class="blank-input" placeholder="Điền từ..." data-correct="{escape(correct_answer)}" />
            <span class="correct-key-badge">✓ Đáp án: <strong>{escape(correct_answer)}</strong></span>
          </div>
        </div>"""
        q_htmls.append(q_item)

    return f"{word_box_html}<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_paragraph_fill_body(ex, ex_index):
    word_box = ex.get("word_box", [])
    parts = ex.get("paragraph_parts", [])

    # Word box
    word_box_html = ""
    if word_box:
        chips = "".join(f"<span class='word-chip'>{escape(w)}</span>" for w in word_box)
        word_box_html = f"""
        <div class="word-box-container">
          <div class="word-box-label">📦 Hộp từ vựng gợi ý (Word Box)</div>
          <div class="word-box-chips">{chips}</div>
        </div>"""

    # Assemble passage
    passage_pieces = []
    for part in parts:
        if isinstance(part, str):
            passage_pieces.append(escape(part))
        elif isinstance(part, dict) and part.get("type") == "blank":
            b_id = part.get("id", "")
            c_ans = part.get("correct_answer", "")
            blank_markup = f"""
            <span class="inline-blank">
              <span class="inline-blank-num">({b_id})</span>
              <input type="text" class="inline-blank-input" value="{escape(c_ans)}" data-correct="{escape(c_ans)}" />
            </span>"""
            passage_pieces.append(blank_markup)

    passage_html = f"""
    <div class="paragraph-passage">
      {''.join(passage_pieces)}
    </div>"""

    return f"{word_box_html}{passage_html}"


def render_dictionary_entry_body(ex, ex_index):
    entries = ex.get("entries", [])
    entry_htmls = []

    for entry_idx, entry in enumerate(entries):
        word = entry.get("word", "")
        pos = entry.get("part_of_speech", "")
        pron = entry.get("pronunciation", "")
        definition = entry.get("definition", "")
        bullet_points = entry.get("bullet_points", [])
        questions = entry.get("questions", [])

        # Bullet points
        bp_htmls = []
        for bp in bullet_points:
            # Highlight bracketed collocations
            formatted_bp = re.sub(r"\[(.*?)\]", r"<strong>\1</strong>", escape(bp))
            bp_htmls.append(f"<div class='dict-bullet'>&bull; {formatted_bp}</div>")

        # Questions
        q_htmls = []
        for q_idx, q in enumerate(questions):
            q_id = q.get("id", str(q_idx + 1))
            text = q.get("text", "")
            correct_answer = q.get("correct_answer", "")

            q_markup = f"""
            <div style="margin-top:8px; display:flex; flex-direction:column; gap:6px;">
              <div style="font-size:13px; font-weight:600; color:#334155;">
                <span class="q-num" style="display:inline-flex; width:20px; height:20px; font-size:11px;">{q_id}</span>
                {escape(text)}
              </div>
              <div class="blank-input-wrap">
                <input type="text" class="blank-input" placeholder="Điền cụm từ phù hợp..." data-correct="{escape(correct_answer)}" />
                <span class="correct-key-badge">✓ Cụm từ: <strong>{escape(correct_answer)}</strong></span>
              </div>
            </div>"""
            q_htmls.append(q_markup)

        entry_card = f"""
        <div class="dict-entry-card">
          <div class="dict-header">
            <span class="dict-word">{escape(word)}</span>
            <span class="dict-pos">({escape(pos)})</span>
            <span class="dict-phonetic">{escape(pron)}</span>
          </div>
          <div class="dict-def">{escape(definition)}</div>
          
          <div class="dict-collocations">
            <div class="dict-collocations-title">📖 Cụm từ thông dụng & ví dụ ngữ cảnh (Collocations):</div>
            {''.join(bp_htmls)}
          </div>

          <div class="dict-practice-title">✏️ Bài tập vận dụng:</div>
          {''.join(q_htmls)}
        </div>"""
        entry_htmls.append(entry_card)

    return f"<div style='display:flex; flex-direction:column; gap:20px;'>{''.join(entry_htmls)}</div>"


def render_word_families_table_body(ex, ex_index):
    questions = ex.get("questions", [])
    row_htmls = []

    for q in questions:
        base_word = q.get("base_word", "")
        base_type = q.get("base_word_type", "")
        verbs = q.get("verb", [])
        nouns = q.get("noun", [])
        adjs = q.get("adjective", [])
        advs = q.get("adverb", [])

        def render_chips(items):
            if not items:
                return "<span style='color:var(--text-subtle);'>—</span>"
            return "".join(f"<span class='wf-tag'>{escape(it)}</span>" for it in items)

        row = f"""
        <tr>
          <td><span class="wf-base-chip">{escape(base_word)}</span></td>
          <td><span style="font-style:italic; color:var(--text-muted); font-size:12px;">{escape(base_type)}</span></td>
          <td>{render_chips(verbs)}</td>
          <td>{render_chips(nouns)}</td>
          <td>{render_chips(adjs)}</td>
          <td>{render_chips(advs)}</td>
        </tr>"""
        row_htmls.append(row)

    table_html = f"""
    <div class="wf-table-wrap">
      <table class="wf-table">
        <thead>
          <tr>
            <th>Từ gốc (Base)</th>
            <th>Từ loại gốc</th>
            <th>Động từ (Verb)</th>
            <th>Danh từ (Noun)</th>
            <th>Tính từ (Adjective)</th>
            <th>Trạng từ (Adverb)</th>
          </tr>
        </thead>
        <tbody>
          {''.join(row_htmls)}
        </tbody>
      </table>
    </div>"""
    return table_html


def render_word_formation_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        text = q.get("text", "")
        correct_answer = q.get("correct_answer", "")
        base_word = q.get("base_word", "")

        q_item = f"""
        <div class="question-item" data-correct="{escape(correct_answer)}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">
              {escape(text)}
              <span class="base-root-badge">[{escape(base_word)}]</span>
            </div>
          </div>
          <div class="blank-input-wrap">
            <input type="text" class="blank-input" placeholder="Dạng từ đúng..." data-correct="{escape(correct_answer)}" />
            <span class="correct-key-badge">✓ Đáp án: <strong>{escape(correct_answer)}</strong></span>
          </div>
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_translate_sentences_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        vi = q.get("vietnamese", "")
        correct_answer = q.get("correct_answer", "")

        q_item = f"""
        <div class="question-item" data-correct="{escape(correct_answer)}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">
              <strong>Tiếng Việt:</strong> "{escape(vi)}"
            </div>
          </div>
          <div class="blank-input-wrap" style="flex-direction:column; align-items:flex-start; gap:8px;">
            <input type="text" class="blank-input" style="width:100%; max-width:600px;" placeholder="Nhập câu dịch tiếng Anh..." data-correct="{escape(correct_answer)}" />
            <span class="correct-key-badge">✓ Bản dịch mẫu: <strong>{escape(correct_answer)}</strong></span>
          </div>
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def render_generic_questions_body(ex, ex_index):
    questions = ex.get("questions", [])
    q_htmls = []

    for q_idx, q in enumerate(questions):
        q_id = q.get("id", str(q_idx + 1))
        text = q.get("text", str(q))
        correct_answer = q.get("correct_answer", "")

        q_item = f"""
        <div class="question-item" data-correct="{escape(str(correct_answer))}">
          <div class="q-stem-row">
            <span class="q-num">{q_id}</span>
            <div class="q-text">{escape(str(text))}</div>
          </div>
          {f'<div class="correct-key-badge" style="margin-left:34px;">✓ Đáp án: <strong>{escape(str(correct_answer))}</strong></div>' if correct_answer else ''}
        </div>"""
        q_htmls.append(q_item)

    return f"<div class='questions-list'>{''.join(q_htmls)}</div>"


def main():
    parser = argparse.ArgumentParser(description="Generate interactive HTML preview for Unit vocabulary and exercises.")
    parser.add_argument("vocab_dir", help="Path to the Unit vocab folder (e.g. data/gs-6/unit-7/vocab)")
    parser.add_argument("--output", "-o", help="Output HTML file path (default: <vocab_dir>/vocab_preview.html)")

    args = parser.parse_args()
    build_html_preview(args.vocab_dir, args.output)


if __name__ == "__main__":
    main()
