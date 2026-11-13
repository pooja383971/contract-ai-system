from pypdf import PdfReader

def extract_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    if not text.strip():
        raise ValueError("No selectable text was found in this PDF. It may be scanned; OCR is not included in this version.")
    return text
