import os
import pytesseract 
from pdf2image import convert_from_path
import re

class OCRPipeline:
    def __init__(self, tesseract_cmd=None):
        """Initialize the OCR pipeline."""
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        elif os.name == 'nt':
            # Default Windows tesseract location
            tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def process_pdf(self, pdf_path):
        """Convert PDF to images and extract text using OCR."""
        print(f"Processing PDF: {pdf_path}")
        try:
            images = convert_from_path(pdf_path)
            full_text = ""
            for i, image in enumerate(images):
                print(f"Running OCR on page {i + 1}...")
                text = pytesseract.image_to_string(image)
                full_text += text + "\n"
            return self.clean_text(full_text)
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return ""

    def process_image(self, image_path):
        """Extract text from a single image using OCR."""
        print(f"Processing Image: {image_path}")
        try:
            text = pytesseract.image_to_string(image_path)
            return self.clean_text(text)
        except Exception as e:
            print(f"Error processing Image: {e}")
            return ""
            
    def clean_text(self, text):
        """Basic text cleaning."""
        # Replace multiple spaces with a single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Remove empty lines
        text = re.sub(r'\n\s*\n', '\n', text)
        return text.strip()

if __name__ == "__main__":
    print("OCR Pipeline Initialized successfully.")
