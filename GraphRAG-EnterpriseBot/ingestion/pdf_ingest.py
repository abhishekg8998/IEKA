import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    """Extract full text from PDF"""
    doc = fitz.open(pdf_path)

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    return full_text


def chunk_text(text, chunk_size=400):
    """Split text into smaller chunks"""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
