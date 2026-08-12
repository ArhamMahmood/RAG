# Local RAG Resume QA

A local Retrieval-Augmented Generation (RAG) project that uses Ollama and ChromaDB to answer questions from a resume PDF.

## Repository structure

- `src/rag2.py` - Main QA script for asking questions and returning answers.
- `src/database.py` - ChromaDB collection and PDF ingestion utilities.
- `src/embeddings.py` - Ollama embedding helper.
- `src/retrieve.py` - Example retrieval script.
- `src/ingest.py` - Ingest the resume PDF into ChromaDB.
- `src/pdf_loader.py` - PDF page extraction helper.
- `chroma_db/` - Local vector database storage.
- `documents/` - Resume and document files used for ingestion.
- `requirments.txt` - Project dependencies.

## Requirements

- Python 3.13 or newer
- Ollama installed and running locally
- Local resume PDF available for ingestion

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirments.txt
```

3. Place the resume PDF at `documents/resume.pdf`.

4. Start Ollama locally and make sure it is accessible before running the project.

## Usage

### Run the QA script

From the project root:

```powershell
python src\rag2.py
```

Then type a question when prompted.

### Rebuild the vector store

If you need to ingest the resume again, use:

```powershell
python src\ingest.py
```

This will create/update the local ChromaDB dataset from the PDF at `documents/resume.pdf`.

## Privacy and version control

- Do not commit `venv/`, `chroma_db/`, or `documents/*.pdf` to Git.
- The resume PDF should remain local and private.
- A `.gitignore` file is included to help keep these files out of VCS.

## Models

- Embeddings: `all-minilm:latest`
- Chat: `qwen2.5:3b`

If you want faster performance, swap the chat or embedding model to a smaller local Ollama model.

## GitHub

This repository is intended for GitHub. To push your code to `https://github.com/ArhamMahmood/RAG.git`:

```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/ArhamMahmood/RAG.git
git branch -M main
git push -u origin main
```

## Notes

- Keep `venv/` and `chroma_db/` out of source control by using `.gitignore`.
- Use the actual `requirments.txt` file name from this repo when installing dependencies.
- Run commands from the repository root rather than a specific drive path.
