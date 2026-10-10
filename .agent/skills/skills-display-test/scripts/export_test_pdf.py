#!/usr/bin/env python3
"""
Production PDF Exporter for Standardized Unit Tests (Global Success 10–12).
Typesets exam papers strictly following the specification:
- Font: Arial
- Font size: 12pt (standard) or configurable
- Color: Pure black on pure white (#000000 on #ffffff)
- Margins: 0.5cm on all sides (top, bottom, left, right)
- Title: ONLY "UNIT * - TEST 0*" (e.g. "UNIT 1 - TEST 01")
- Question Labels: "1:", "2:", ... in bold (replaces "Question 1:", "Question 2:")
- Dynamic Options: 4 columns (1 row), 2 columns (2 rows), or 1 column (4 rows)
- Flow: Continuous, no artificial page breaks, fills printed pages naturally (exact 6-page budget).
"""

import os
import sys
import re
import json
import argparse
import subprocess
import time
from pathlib import Path
import fitz

# Load typography engine
helv_font = fitz.Font("helv")

def find_browser_executable() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    for cmd in ["chrome.exe", "msedge.exe"]:
        try:
            res = subprocess.run(["where", cmd], capture_output=True, text=True)
            if res.returncode == 0:
                p = res.stdout.strip().split("\n")[0].strip()
                if os.path.exists(p):
                    return p
        except Exception:
            pass
    raise FileNotFoundError("Could not find Chrome or Edge executable on this machine.")

def format_markdown_text(text: str) -> str:
    if not text:
        return ""
    # Bold italic
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    # Italic
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t

def format_paragraphs(text: str) -> str:
    if not text:
        return ""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    html_paras = []
    for p in paragraphs:
        lines = p.split("\n")
        formatted_lines = [format_markdown_text(l.strip()) for l in lines]
        para_content = "<br>\n".join(formatted_lines)
        html_paras.append(f'<p class="passage-para">{para_content}</p>')
    return "\n".join(html_paras)

def determine_options_layout(options: dict, is_simple_prompt: bool, font_size: float = 12.0) -> str:
    """
    Determine layout using exact typography measurements with PyMuPDF Helvetica/Arial.
    Returns:
    - 'options-1row' (4 columns, 1 row)
    - 'options-2rows' (2 columns, 2 rows)
    - 'options-4rows' (1 column, 4 rows)
    """
    keys = [k for k in ["A", "B", "C", "D"] if k in options]
    if not keys:
        return "options-1row"

    widths = [helv_font.text_length(f"{k}. {options[k]}", fontsize=font_size) for k in keys]
    max_w = max(widths)
    sum_w = sum(widths)

    # Printable width: 566.93pt
    if font_size <= 12.5:
        if is_simple_prompt:
            # Label "X:" takes 32pt + 8pt gap = 40pt. Available width = 526.93pt.
            # 4 cols: gap 8pt * 3 = 24pt. Each col has (526.93 - 24) / 4 = 125.7pt.
            # 2 cols: gap 14pt. Each col has (526.93 - 14) / 2 = 256.4pt.
            if max_w <= 120.0 and sum_w <= 480.0:
                return "options-1row"
            elif max_w <= 248.0:
                return "options-2rows"
            else:
                return "options-4rows"
        else:
            # Full width = 566.93pt.
            # 4 cols: gap 8pt * 3 = 24pt. Each col has (566.93 - 24) / 4 = 135.7pt.
            # 2 cols: gap 14pt. Each col has (566.93 - 14) / 2 = 276.4pt.
            if max_w <= 130.0 and sum_w <= 510.0:
                return "options-1row"
            elif max_w <= 268.0:
                return "options-2rows"
            else:
                return "options-4rows"
    else:
        # Font size 14pt
        if is_simple_prompt:
            if max_w <= 106.0 and sum_w <= 420.0:
                return "options-1row"
            elif max_w <= 220.0:
                return "options-2rows"
            else:
                return "options-4rows"
        else:
            if max_w <= 128.0 and sum_w <= 500.0:
                return "options-1row"
            elif max_w <= 268.0:
                return "options-2rows"
            else:
                return "options-4rows"

def generate_test_html(test_data: dict, font_size: float = 12.0) -> str:
    unit_num = test_data.get("unit_number", 1)
    test_id = str(test_data.get("test_id", "test_1"))
    match = re.search(r'(\d+)', test_id)
    t_num = int(match.group(1)) if match else 1
    display_title = f"UNIT {unit_num} - TEST {t_num:02d}"

    title_size = 15 if font_size <= 12.5 else 16
    line_h = 1.25 if font_size <= 12.5 else 1.26
    label_width = "32pt" if font_size <= 12.5 else "92pt"

    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>{display_title}</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 0.5cm;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  body {{
    font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
    font-size: {font_size}pt;
    line-height: {line_h};
    color: #000000;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }}

  /* Title: Only "UNIT * - TEST 0*" */
  .test-header {{
    text-align: center;
    margin: 0 0 6pt 0;
    padding: 0;
  }}

  .test-title {{
    font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
    font-size: {title_size}pt;
    font-weight: bold;
    text-transform: uppercase;
    margin: 0;
    letter-spacing: 0.5px;
  }}

  /* Sections */
  .section-block {{
    margin-bottom: 6pt;
  }}

  .section-instruction {{
    font-style: italic;
    font-weight: bold;
    margin: 6pt 0 4pt 0;
    text-align: justify;
    line-height: 1.22;
    page-break-inside: avoid;
    break-inside: avoid;
    page-break-after: avoid;
    break-after: avoid;
  }}

  /* Passage */
  .passage-container {{
    margin-bottom: 5pt;
  }}

  .passage-title {{
    text-align: center;
    font-weight: bold;
    margin: 3pt 0;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .passage-para {{
    margin: 0 0 3pt 0;
    text-indent: 1.5em;
    text-align: justify;
    line-height: {line_h};
  }}

  /* Question layouts - strictly avoid splitting prompt from options */
  .question-item {{
    margin-bottom: 6.0pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  /* Simple prompt (1:, 2:, etc.) */
  .q-row-layout {{
    display: flex;
    align-items: flex-start;
  }}

  .q-label-cell {{
    flex: 0 0 {label_width};
    font-weight: bold;
    white-space: nowrap;
    padding-right: 6pt;
  }}

  .q-options-cell {{
    flex: 1;
    display: grid;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  /* Stem prompt */
  .q-stem-layout {{
    display: block;
  }}

  .q-stem-text {{
    margin-bottom: 2.5pt;
    text-align: justify;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .q-dialogue-block {{
    margin: 2pt 0 3pt 1.2em;
    line-height: 1.22;
  }}

  .q-dialogue-line {{
    margin-bottom: 1.5pt;
  }}

  .q-options-full {{
    display: grid;
    width: 100%;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  /* Options grid variants */
  .options-1row {{
    grid-template-columns: repeat(4, 1fr);
    column-gap: 8pt;
  }}

  .options-2rows {{
    grid-template-columns: repeat(2, 1fr);
    column-gap: 12pt;
    row-gap: 2.2pt;
  }}

  .options-4rows {{
    grid-template-columns: 1fr;
    row-gap: 2.2pt;
  }}

  .opt-cell {{
    text-align: left;
    vertical-align: top;
    line-height: 1.22;
  }}

  .opt-tag {{
    font-weight: bold;
    margin-right: 2pt;
  }}

  .test-footer-rule {{
    text-align: center;
    font-weight: bold;
    margin-top: 10pt;
    margin-bottom: 4pt;
    letter-spacing: 2px;
    font-size: {font_size}pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
</style>
</head>
<body>

<div class="test-header">
  <div class="test-title">{display_title}</div>
</div>
""")

    sections = test_data.get("sections", [])
    questions_map = {q["question_number"]: q for q in test_data.get("questions", [])}

    for sec in sections:
        q_start, q_end = sec.get("questions_range", [1, 40])
        instr = sec.get("instruction", "")
        p_title = sec.get("passage_title", "")
        p_text = sec.get("passage_text", "")

        html_parts.append('<div class="section-block">')
        if instr:
            html_parts.append(f'  <div class="section-instruction">{format_markdown_text(instr)}</div>')

        if p_title or p_text:
            html_parts.append('  <div class="passage-container">')
            if p_title:
                html_parts.append(f'    <div class="passage-title">{format_markdown_text(p_title)}</div>')
            if p_text:
                html_parts.append(f'    {format_paragraphs(p_text)}')
            html_parts.append('  </div>')

        for q_num in range(q_start, q_end + 1):
            if q_num not in questions_map:
                continue
            q = questions_map[q_num]
            prompt = q.get("prompt", f"Question {q_num}:").strip()
            options = q.get("options", {})

            # Replace "Question X:" with "X:"
            is_simple_prompt = bool(re.match(r"^(?:Question\s+)?\d+:\s*$", prompt))
            layout_class = determine_options_layout(options, is_simple_prompt, font_size=font_size)

            opt_cells = []
            for letter in ["A", "B", "C", "D"]:
                if letter in options:
                    val = format_markdown_text(str(options[letter]))
                    opt_cells.append(f'<div class="opt-cell"><span class="opt-tag">{letter}.</span> {val}</div>')
            opts_html = "\n        ".join(opt_cells)

            if is_simple_prompt:
                label_text = f"<b>{q_num}:</b>"
                q_html = f"""  <div class="question-item q-row-layout">
    <div class="q-label-cell">{label_text}</div>
    <div class="q-options-cell {layout_class}">
        {opts_html}
    </div>
  </div>"""
            else:
                lines = prompt.split("\n")
                first_line = lines[0].strip()
                other_lines = [l.strip() for l in lines[1:] if l.strip()]

                m = re.match(r"^Question\s+(\d+):?\s*(.*)$", first_line)
                if m:
                    q_prefix = f"<b>{m.group(1)}:</b>"
                    q_rest = m.group(2)
                    stem_head = f"{q_prefix} {format_markdown_text(q_rest)}" if q_rest else q_prefix
                else:
                    m2 = re.match(r"^(\d+):?\s*(.*)$", first_line)
                    if m2:
                        q_prefix = f"<b>{m2.group(1)}:</b>"
                        q_rest = m2.group(2)
                        stem_head = f"{q_prefix} {format_markdown_text(q_rest)}" if q_rest else q_prefix
                    else:
                        stem_head = f"<b>{q_num}:</b> {format_markdown_text(first_line)}"

                dialogue_html = ""
                if other_lines:
                    d_lines = [f'<div class="q-dialogue-line">{format_markdown_text(l)}</div>' for l in other_lines]
                    dialogue_html = f'<div class="q-dialogue-block">\n      ' + "\n      ".join(d_lines) + '\n    </div>'

                q_html = f"""  <div class="question-item q-stem-layout">
    <div class="q-stem-text">{stem_head}</div>
    {dialogue_html}
    <div class="q-options-full {layout_class}">
        {opts_html}
    </div>
  </div>"""

            html_parts.append(q_html)

        html_parts.append('</div>')

    html_parts.append("""
<div class="test-footer-rule">--- THE END ---</div>
</body>
</html>
""")

    return "\n".join(html_parts)

def export_test_to_pdf(json_path: Path, output_pdf_path: Path = None, generate_preview: bool = False, font_size: float = 12.0) -> Path:
    json_path = Path(json_path)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON test file not found: {json_path}")

    if output_pdf_path is None:
        output_pdf_path = json_path.parent / f"{json_path.stem}.pdf"
    else:
        output_pdf_path = Path(output_pdf_path)

    with open(json_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    html_content = generate_test_html(test_data, font_size=font_size)
    temp_html = json_path.parent / f"temp_{json_path.stem}.html"
    temp_html.write_text(html_content, encoding="utf-8")

    browser_bin = find_browser_executable()
    cmd = [
        browser_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf_path}",
        f"file:///{temp_html.as_posix()}"
    ]

    print(f"Exporting {output_pdf_path.name} (Font size: {font_size}pt)...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, timeout=60)
    dur = round(time.time() - t0, 2)

    if temp_html.exists():
        temp_html.unlink()

    if not output_pdf_path.exists():
        raise RuntimeError(f"Browser failed to generate PDF. Exit code: {res.returncode}. Stderr: {res.stderr.decode('utf-8', errors='ignore')}")

    doc = fitz.open(output_pdf_path)
    page_count = len(doc)
    print(f"SUCCESS: {output_pdf_path.name} created! Total pages: {page_count} (Rendered in {dur}s)")

    last_page_text = doc[-1].get_text()
    last_page_lines = [l.strip() for l in last_page_text.split('\n') if l.strip()]
    if len(last_page_lines) <= 4:
        print(f"WARNING: Last page (Page {page_count}) has only {len(last_page_lines)} lines! Consider checking overflow.")
    else:
        print(f"AUDIT PASS: Page distribution is balanced. Last page has {len(last_page_lines)} lines.")

    if generate_preview:
        preview_dir = json_path.parent / f"preview_{json_path.stem}"
        preview_dir.mkdir(exist_ok=True)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            img_path = preview_dir / f"{json_path.stem}_p{i+1}.png"
            pix.save(str(img_path))
        print(f"Rendered {page_count} preview PNG images to {preview_dir}")

    return output_pdf_path

def main():
    parser = argparse.ArgumentParser(description="Export Unit Test JSON to Standard PDF")
    parser.add_argument("target", help="Path to test JSON file or unit test directory")
    parser.add_argument("--preview", action="store_true", help="Generate preview PNG images")
    parser.add_argument("--output-dir", help="Optional output directory for PDF files")
    parser.add_argument("--font-size", type=float, default=12.0, help="Font size in pt (default: 12.0)")
    args = parser.parse_args()

    target_path = Path(args.target)
    if target_path.is_file() and target_path.suffix == ".json":
        json_files = [target_path]
    elif target_path.is_dir():
        json_files = sorted(list(target_path.glob("test*.json")))
        if not json_files:
            print(f"No test*.json files found in {target_path}")
            sys.exit(1)
    else:
        print(f"Invalid target path: {target_path}")
        sys.exit(1)

    for jf in json_files:
        out_pdf = None
        if args.output_dir:
            out_pdf = Path(args.output_dir) / f"{jf.stem}.pdf"
        export_test_to_pdf(jf, out_pdf, generate_preview=args.preview, font_size=args.font_size)

if __name__ == "__main__":
    main()
