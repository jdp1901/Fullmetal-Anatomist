"""File upload text extraction — PDF, DOCX, and TXT."""

from pathlib import Path


def extract_text(file_path: Path) -> str:
    """Extract plain text from a file based on its extension."""
    suffix = file_path.suffix.lower()

    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8", errors="replace")

    if suffix == ".pdf":
        return _extract_pdf(file_path)

    if suffix == ".docx":
        return _extract_docx(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")


def _extract_pdf(path: Path) -> str:
    import fitz  # PyMuPDF

    doc = fitz.open(str(path))
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n\n".join(pages)


def _extract_docx(path: Path) -> str:
    from docx import Document

    doc = Document(str(path))
    return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
