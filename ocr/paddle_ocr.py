from paddleocr import PaddleOCR
import fitz  # PyMuPDF
import os

# Initialize OCR model only once
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image(image_path: str) -> str:
    result = ocr_model.ocr(image_path, cls=True)
    extracted_text = ""

    for line in result:
        for word_info in line:
            word = word_info[1][0]
            extracted_text += word + " "

    return extracted_text.strip()

def extract_text_from_pdf(pdf_path: str) -> str:
    extracted_text = ""
    try:
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                extracted_text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return extracted_text.strip()

