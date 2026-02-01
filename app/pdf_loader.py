import fitz  # PyMuPDF


def load_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page in doc:
        text = page.get_text()
        if text.strip():
            pages.append(text)

    return "\n".join(pages)
