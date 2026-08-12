import fitz
from pathlib import Path


def load_pdf(pdf_path):
    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages


if __name__ == "__main__":
    pdf_path = Path("documents/resume.pdf")

    pages = load_pdf(pdf_path)

    print(f"Loaded {len(pages)} pages")

    for page in pages[:2]:
        print("\n--- Page", page["page"], "---")
        print(page["text"][:1000])