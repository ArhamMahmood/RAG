from pathlib import Path

import chromadb
import ollama
import fitz


EMBEDDING_MODEL = "all-minilm:latest"

PDF_PATH = Path("documents/resume.pdf")


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def extract_pdf(pdf_path):

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


def chunk_text(text, chunk_size=500, overlap=100):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_embedding(text):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]


def ingest():

    pages = extract_pdf(PDF_PATH)

    print(f"Loaded {len(pages)} pages")

    chunk_id = 0

    for page in pages:

        chunks = chunk_text(page["text"])

        for chunk in chunks:

            embedding = create_embedding(chunk)

            collection.add(
                ids=[str(chunk_id)],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "source": PDF_PATH.name,
                    "page": page["page"]
                }]
            )

            chunk_id += 1

            print(f"Added chunk {chunk_id}")

    print("\nIngestion complete!")
    print("Total chunks:", collection.count())


if __name__ == "__main__":
    ingest()