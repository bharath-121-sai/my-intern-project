import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """Extracts all text from a PDF file."""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text("text")
    pdf.close()
    return text
