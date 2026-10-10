"""Convert GS12.pdf pages to PNG images for multimodal vision transcription.
Supports:
1. Unit mode: Automatically extracts pages for GS12.pdf for a specified Unit (1-10).
2. Manual mode: Converts specified page range of GS12.pdf or any PDF.
"""

import sys
import os
import argparse
from typing import List

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from page_mapping import get_unit_mapping
except ImportError:
    from .page_mapping import get_unit_mapping

def extract_pdf_pages_to_images(pdf_path: str, output_dir: str, start_page: int, end_page: int, prefix: str = "page", dpi: int = 150) -> List[str]:
    """Convert specified page range of a PDF into PNG images."""
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []

    try:
        import fitz
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        start_idx = max(1, min(start_page, total_pages))
        end_idx = max(start_idx, min(end_page, total_pages))

        for pno in range(start_idx - 1, end_idx):
            page = doc.load_page(pno)
            pix = page.get_pixmap(dpi=dpi)
            image_filename = f"{prefix}_{pno + 1}.png"
            image_path = os.path.join(output_dir, image_filename)
            pix.save(image_path)
            image_paths.append(image_path)
        doc.close()
        return image_paths
    except ImportError:
        pass

    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page, dpi=dpi)
        for i, page in enumerate(images):
            image_filename = f"{prefix}_{start_page + i}.png"
            image_path = os.path.join(output_dir, image_filename)
            page.save(image_path, 'PNG')
            image_paths.append(image_path)
        return image_paths
    except ImportError:
        print("Error: PyMuPDF (fitz) or pdf2image is required.", file=sys.stderr)
        sys.exit(1)

def extract_unit_gs12(unit_num: int, output_base: str, workspace_root: str = ".", dpi: int = 150):
    """Extract scanned pages for a GS12 unit from GS12.pdf."""
    mapping = get_unit_mapping(unit_num)
    if not mapping:
        print(f"Error: No mapping found for Unit {unit_num}", file=sys.stderr)
        return {}

    gs12_pdf = os.path.join(workspace_root, "GS12.pdf")
    if not os.path.exists(gs12_pdf):
        print(f"Error: GS12.pdf not found at {gs12_pdf}", file=sys.stderr)
        return {}

    sb_info = mapping["sb"]
    sb_dir = os.path.join(output_base, f"unit_{unit_num}_sb_pages")
    print(f"[*] Extracting GS12 Unit {unit_num} ({mapping['title']}): pages {sb_info['start']} to {sb_info['end']}...")
    sb_imgs = extract_pdf_pages_to_images(gs12_pdf, sb_dir, sb_info["start"], sb_info["end"], prefix=f"gs12_u{unit_num}_p", dpi=dpi)
    print(f"[✓] Rendered {len(sb_imgs)} pages to {sb_dir}")
    return {"sb": sb_imgs}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract GS12 PDF pages to images for vision transcription")
    parser.add_argument("--unit", type=int, help="GS12 Unit number (1-10)")
    parser.add_argument("--pdf", type=str, default="GS12.pdf", help="Path to PDF file")
    parser.add_argument("--out", type=str, default="temp_pages", help="Output directory for images")
    parser.add_argument("--start", type=int, help="Start page (1-based)")
    parser.add_argument("--end", type=int, help="End page (1-based)")
    parser.add_argument("--prefix", type=str, default="page", help="Filename prefix")
    parser.add_argument("--dpi", type=int, default=150, help="Image resolution DPI")
    parser.add_argument("--workspace", type=str, default=".", help="Workspace root directory")

    args = parser.parse_args()

    if args.unit:
        extract_unit_gs12(args.unit, args.out, workspace_root=args.workspace, dpi=args.dpi)
    elif args.start and args.end:
        extract_pdf_pages_to_images(args.pdf, args.out, args.start, args.end, prefix=args.prefix, dpi=args.dpi)
    else:
        parser.print_help()
