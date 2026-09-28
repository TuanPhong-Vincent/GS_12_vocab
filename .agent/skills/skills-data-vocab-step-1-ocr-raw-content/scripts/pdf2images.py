import sys
import os
import glob
import argparse
def pdf_to_images(pdf_path, output_folder, first_page=None, last_page=None):
    pages_folder = os.path.join(output_folder, "pages")
    os.makedirs(pages_folder, exist_ok=True)
    image_paths = []

    # Priority 1: PyMuPDF (fitz) - fast, self-contained, no poppler binary needed
    try:
        import fitz
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        start_idx = first_page if first_page else 1
        end_idx = last_page if last_page else total_pages

        start_idx = max(1, min(start_idx, total_pages))
        end_idx = max(start_idx, min(end_idx, total_pages))

        for pno in range(start_idx - 1, end_idx):
            page = doc.load_page(pno)
            pix = page.get_pixmap(dpi=150)
            image_filename = f"page_{pno + 1}.png"
            image_path = os.path.join(pages_folder, image_filename)
            pix.save(image_path)
            image_paths.append(image_path)
        doc.close()
        return image_paths
    except ImportError:
        pass

    # Priority 2: pdf2image
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, first_page=first_page, last_page=last_page)
        start_idx = first_page if first_page else 1
        for i, page in enumerate(images):
            image_filename = f"page_{start_idx + i}.png"
            image_path = os.path.join(pages_folder, image_filename)
            page.save(image_path, 'PNG')
            image_paths.append(image_path)
        return image_paths
    except ImportError:
        print("Error: Neither PyMuPDF (fitz) nor pdf2image is installed. Run: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to images")
    parser.add_argument("pdf_path", nargs="?", help="Path to PDF file")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--start", type=int, help="First page to convert (1-indexed)")
    parser.add_argument("--end", type=int, help="Last page to convert (1-indexed)")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    output_folder = args.output

    if not pdf_path:
        # Find the first PDF file in the raw directory
        pdf_files = glob.glob(os.path.join("book-raw", "*.pdf"))
        if not pdf_files:
            print("Error: No PDF files found in 'book-raw' directory.")
            sys.exit(1)
        pdf_path = pdf_files[0]
        if not output_folder:
            output_folder = "book-raw"

    if not output_folder:
        output_folder = os.path.dirname(pdf_path)
        if not output_folder:
            output_folder = "."

    if not os.path.isfile(pdf_path):
        print(f"Error: {pdf_path} does not exist or is not a file.")
        sys.exit(1)

    image_paths = pdf_to_images(pdf_path, output_folder, args.start, args.end)
    print(f"Converted {len(image_paths)} pages to images in '{os.path.join(output_folder, 'pages')}' from '{pdf_path}'")
