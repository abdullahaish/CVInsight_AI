import fitz
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import docx
from app.utils.logger import logger


def extract_text(file_path, file_type):
    """Extracts text from PDFs and DOCX files."""
    logger.info(f"Starting text extraction for file: {file_path} with type: {file_type}")
    try:
        if file_type == "pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif file_type == "docx":
            extracted_text = extract_text_from_docx(file_path)
        else:
            logger.error(f"Unsupported file type: {file_type}")
            return None

        if not extracted_text.strip():
            logger.warning(f"No text extracted from file: {file_path}")

        logger.info(f"Text extraction successful for file: {file_path}")
        return extracted_text
    except Exception as e:
        logger.exception(f"Error extracting text from {file_path}: {e}")
        return None


def extract_text_from_pdf(pdf_path):
    """Extracts text from PDFs, including OCR for scanned documents."""
    logger.info(f"Extracting text from PDF: {pdf_path}")
    text = ""

    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text")

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    text += "\n".join(["\t".join(row) for row in table if row])

        if not text.strip():
            logger.warning(f"No text detected in PDF, attempting OCR: {pdf_path}")
            text = extract_text_using_ocr(pdf_path)

        logger.info(f"PDF text extraction successful: {pdf_path}")
        return text
    except Exception as e:
        logger.exception(f"Error extracting text from PDF {pdf_path}: {e}")
        return ""


def extract_text_using_ocr(pdf_path):
    """OCR for scanned PDFs."""
    logger.info(f"Starting OCR for scanned PDF: {pdf_path}")
    text = ""
    try:
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)
        logger.info(f"OCR text extraction completed for {pdf_path}")
        return text
    except Exception as e:
        logger.exception(f"Error performing OCR on {pdf_path}: {e}")
        return ""


def extract_text_from_docx(docx_path):
    """Extract text from DOCX files."""
    logger.info(f"Extracting text from DOCX: {docx_path}")
    try:
        doc = docx.Document(docx_path)
        extracted_text = "\n".join([para.text for para in doc.paragraphs])
        logger.info(f"DOCX text extraction successful: {docx_path}")
        return extracted_text
    except Exception as e:
        logger.exception(f"Error extracting text from DOCX {docx_path}: {e}")
        return ""
