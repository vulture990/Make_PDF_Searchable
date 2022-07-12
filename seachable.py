import pytesseract
import argparse
import os

from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger
from progressbar import ProgressBar


def create_searchable_pdf(images: list, output_path: str):
    """Generate a searchable PDF from document images.
    """

    merger = PdfFileMerger()
    pbar=ProgressBar()
    for page_index, image in enumerate(pbar(images)):
        pdf_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        pdf_page_path = f"/tmp/{page_index}.pdf"        
        with open(pdf_page_path, "wb") as f:
            f.write(pdf_page)
        merger.append(pdf_page_path)
        os.remove(pdf_page_path)

    merger.write(output_path)

    return None


def main(input_path, output_path):
    """Convert PDF to images, OCR and then generate a searchable
    PDF file.
    """
    print(f"Input PDF path: {input_path}")
    # Convert input PDF into list of images.
    print(f"Converting PDF to PNG images...")
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    images= convert_from_path(input_path, poppler_path='C:\\Program Files\\poppler-22.04.0\\Library\\bin')
    # Create searchable PDF using Tesseract.
    print(f"Generating searchable {len(images)}-page PDF...")
    create_searchable_pdf(images, output_path)
    print(f"Output PDF path: {output_path}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a searchable PDF.")
    parser.add_argument("input_path", type=str)
    parser.add_argument("--output_path", type=str, default="output.pdf")
    args = parser.parse_args()
    main(args.input_path, args.output_path)