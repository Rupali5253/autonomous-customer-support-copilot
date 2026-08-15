from pathlib import Path
from pypdf import PdfReader


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# PDF knowledge-base folder
PDF_DIR = BASE_DIR / "knowledge_base" / "pdfs"

# Processed text folder
PROCESSED_DIR = BASE_DIR / "knowledge_base" / "processed"


def load_pdf(pdf_path: Path) -> str:
    """Extract text from a single PDF."""

    reader = PdfReader(str(pdf_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def process_all_pdfs():
    """Read all PDFs and save extracted text into processed folder."""

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_path in pdf_files:

        print(f"Processing: {pdf_path.name}")

        text = load_pdf(pdf_path)

        output_file = PROCESSED_DIR / f"{pdf_path.stem}.txt"

        output_file.write_text(
            text,
            encoding="utf-8"
        )

        print(f"Saved: {output_file.name}")

    print("\nPDF processing completed.")


if __name__ == "__main__":
    process_all_pdfs()