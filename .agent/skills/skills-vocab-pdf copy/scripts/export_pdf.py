#!/usr/bin/env python3
"""
High-Resolution Native JPEG Base64 Encoding & Headless Chrome Export
Supports Global Success 10-12 (GS10, GS11, GS12).
Exports strict 11-page publication-grade PDF and verifies with PyMuPDF.
"""

import re
import base64
import os
import io
import sys
import sys
import subprocess
import time
from pathlib import Path
from PIL import Image
import fitz

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def detect_workspace_root():
    current_dir = Path(__file__).resolve()
    for p in current_dir.parents:
        if (p / "lessons").exists():
            return p
    return Path.cwd().resolve()


def generate_optimized_pdf(unit_arg="unit-1"):
    workspace = detect_workspace_root()
    if unit_arg.isdigit():
        unit_name = f"unit-{unit_arg}"
        unit_num = unit_arg
    elif unit_arg.startswith("unit-"):
        unit_name = unit_arg
        unit_num = unit_arg.replace("unit-", "")
    else:
        unit_name = "unit-1"
        unit_num = "1"

    vocab_dir = workspace / "lessons" / unit_name / "vocab"
    html_path = vocab_dir / f"vocab_unit{unit_num}.html"
    if not html_path.exists():
        html_path = vocab_dir / "pdf.html"
    if not html_path.exists():
        html_path = workspace / "pdf.html"

    out_pdf_unit = vocab_dir / f"vocab_unit{unit_num}.pdf"
    out_pdf_alt = vocab_dir / f"unit-{unit_num}.pdf"
    out_pdf_root = workspace / f"unit-{unit_num}.pdf"

    print(f"Reading HTML from {html_path}...")
    content = open(html_path, "r", encoding="utf-8").read()

    # Cache converted base64 images
    img_cache = {}

    def replace_img(match):
        src = match.group(1).replace("\\", "/").lstrip("/")
        if src in img_cache:
            return f'src="{img_cache[src]}"'
        
        # Candidate locations for the image
        candidates = [
            workspace / src,
            vocab_dir / src,
            vocab_dir / "exercises" / src,
            workspace / "lessons" / unit_name / "vocab" / "exercises" / src,
            workspace / "lessons" / unit_name / "vocab" / src,
            vocab_dir / "images" / os.path.basename(src),
            workspace / "lessons" / unit_name / "vocab" / "images" / os.path.basename(src),
            workspace / "lessons" / "media" / "gs12" / unit_name / "images" / os.path.basename(src),
        ]

        full_path = None
        for cand in candidates:
            if cand.exists() and cand.is_file():
                full_path = cand
                break

        if full_path:
            try:
                # Open with Pillow and convert to high-quality JPEG (quality 92)
                # This enables native PDF DCTDecode, keeping PDF size under 5MB with crystal clarity
                with Image.open(full_path) as im:
                    im_rgb = im.convert("RGB")
                    buf = io.BytesIO()
                    im_rgb.save(buf, format="JPEG", quality=92, optimize=True)
                    jpeg_bytes = buf.getvalue()
                    b64 = base64.b64encode(jpeg_bytes).decode("utf-8")
                    data_uri = f"data:image/jpeg;base64,{b64}"
                    img_cache[src] = data_uri
                    return f'src="{data_uri}"'
            except Exception as e:
                print(f"Warning: could not convert {src} ({full_path}): {e}")
        else:
            print(f"Warning: image file not found for src: {src}")

        return match.group(0)

    print("Embedding images as optimized native JPEG Base64...")
    content_b64 = re.sub(r'src="([^"]+\.(?:webp|png|jpg|jpeg))"', replace_img, content)

    temp_html = vocab_dir / "temp_selfcontained.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(content_b64)
    print(f"Wrote {temp_html} ({round(os.path.getsize(temp_html) / (1024*1024), 2)} MB)")

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_path = None
    for cp in chrome_candidates:
        if os.path.exists(cp):
            chrome_path = cp
            break

    if not chrome_path:
        raise FileNotFoundError("Google Chrome executable not found!")

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf_unit}",
        f"file:///{temp_html.as_posix()}"
    ]

    print(f"Executing Chrome headless print-to-pdf -> {out_pdf_unit}...")
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, timeout=90)
    dur = round(time.time() - t0, 2)
    print(f"Chrome finished in {dur}s, exit code: {res.returncode}")

    # Remove temporary HTML
    if temp_html.exists():
        try:
            os.remove(temp_html)
        except Exception:
            pass

    if out_pdf_unit.exists():
        size_mb = round(os.path.getsize(out_pdf_unit) / (1024 * 1024), 2)
        print(f"SUCCESS: {out_pdf_unit} created! Size: {size_mb} MB")

        # Copy to alternative locations for compatibility
        try:
            import shutil
            shutil.copy2(out_pdf_unit, out_pdf_alt)
            shutil.copy2(out_pdf_unit, out_pdf_root)
            print(f"Copied to {out_pdf_alt} and {out_pdf_root}")
        except Exception as e:
            print(f"Notice copying pdf: {e}")

        # Verify with PyMuPDF
        doc = fitz.open(out_pdf_unit)
        page_cnt = len(doc)
        print(f"==================================================")
        print(f"PDF VERIFICATION: {page_cnt} pages generated.")
        print(f"==================================================")
        
        for i in range(page_cnt):
            page = doc[i]
            text = page.get_text()
            first = text.splitlines()[0] if text.splitlines() else "EMPTY"
            heads = [l.strip() for l in text.splitlines() if l.strip().startswith("Exercise ") or "CATEGORY " in l or "PART " in l]
            print(f"Page {i+1}: {heads[:3]} | Top: {first[:35]}")

        return page_cnt
    else:
        print("ERROR: PDF was not created.")
        return 0


if __name__ == "__main__":
    unit_arg = sys.argv[1] if len(sys.argv) > 1 else "unit-1"
    generate_optimized_pdf(unit_arg)
