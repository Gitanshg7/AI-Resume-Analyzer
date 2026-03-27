"""
Resume Parser Module
====================
Handles PDF and DOCX file parsing, text cleaning, and NLP preprocessing.

Pipeline:
    1. parse_file()       → raw text from PDF or DOCX
    2. clean_text()       → lowercase, punctuation-normalized, whitespace-normalized
    3. preprocess_nlp()   → tokenize → stopwords → lemmatize → normalize
    4. extract_email()    → regex email detection
    5. extract_phone()    → regex phone detection
"""

import re
import io
import fitz  # PyMuPDF
from docx import Document as DocxDocument

# Lazy-loaded spaCy model
_nlp = None


def _get_nlp():
    """Load spaCy model lazily."""
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ── File Parsing ─────────────────────────────────────────────────────────


def parse_pdf(file_obj) -> str:
    """
    Extract text from PDF using PyMuPDF.
    OCR is used only if extraction fails or text length is extremely small.
    """

    file_bytes = file_obj.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    text_parts = []
    for page in doc:
        page_text = page.get_text()
        if page_text:
            text_parts.append(page_text)

    text = "\n".join(text_parts)

    # OCR fallback ONLY if extremely little text extracted
    if len(text.strip()) < 200:
        text = _ocr_pdf(doc)

    doc.close()

    return text


def _ocr_pdf(doc) -> str:
    """
    OCR fallback for scanned PDFs.
    Uses Tesseract if available.
    """

    try:
        import pytesseract
        from PIL import Image
        import shutil
        import os

        if not shutil.which("tesseract"):
            tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path

        text_parts = []

        for page in doc:
            mat = fitz.Matrix(300 / 72, 300 / 72)
            pix = page.get_pixmap(matrix=mat)

            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            page_text = pytesseract.image_to_string(img)

            text_parts.append(page_text)

        return "\n".join(text_parts)

    except Exception:
        return ""


def parse_docx(file_obj) -> str:
    """
    Extract text from DOCX files.
    """

    file_bytes = file_obj.read()

    doc = DocxDocument(io.BytesIO(file_bytes))

    text_parts = []

    for para in doc.paragraphs:
        if para.text.strip():
            text_parts.append(para.text)

    return "\n".join(text_parts)


def parse_file(file_obj) -> str:
    """
    Route file to appropriate parser.
    """

    name = file_obj.name.lower()

    if hasattr(file_obj, "seek"):
        file_obj.seek(0)

    if name.endswith(".pdf"):
        return parse_pdf(file_obj)

    elif name.endswith(".docx"):
        return parse_docx(file_obj)

    else:
        raise ValueError(f"Unsupported file type: {name}")


# ── Text Cleaning ───────────────────────────────────────────────────────


def clean_text(text: str) -> str:
    """
    Clean raw text while preserving useful technical tokens.

    Preserves:
        C++
        Node.js
        REST API
    """

    text = text.lower()

    # preserve + and . used in tech names
    text = re.sub(r"[^a-z0-9+.#\s]", " ", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ── NLP Preprocessing ───────────────────────────────────────────────────


def preprocess_nlp(text: str) -> str:
    """
    NLP preprocessing pipeline.

    Steps:
        tokenization
        stopword removal
        lemmatization
    """

    nlp = _get_nlp()

    doc = nlp(text)

    tokens = []

    for token in doc:

        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if token.is_space:
            continue

        lemma = token.lemma_.strip()

        if lemma:
            tokens.append(lemma)

    return " ".join(tokens)


# ── Contact Extraction ──────────────────────────────────────────────────


EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[\s\-]?)?"
    r"(?:\(?\d{2,4}\)?[\s\-]?)?"
    r"\d{3,4}[\s\-]?\d{3,4}"
)


def extract_email(text: str) -> str:
    """Extract email address."""

    match = EMAIL_PATTERN.search(text)

    return match.group() if match else ""


def extract_phone(text: str) -> str:
    """Extract phone number."""

    match = PHONE_PATTERN.search(text)

    return match.group().strip() if match else ""