import chromadb
import ollama


LLM_MODEL = "qwen2.5:3b"
EMBEDDING_MODEL = "all-minilm:latest"


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="documents"
)


def create_embedding(text):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]


def retrieve(question, n_results=3):

    embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    documents = results["documents"][0]

    return documents


def generate_answer(question, documents):

    context = "\n\n".join(documents)

    prompt = f"""
Answer the question directly using the context below.

Rules:
- Do not reason extensively.
- Do not repeat the question.
- Keep the answer concise.
- If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
    model=LLM_MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={
        "num_predict": 150
    }
)

    return response["message"]["content"]


def main():

    question = input("\nAsk a question: ")

    documents = retrieve(question)

    answer = generate_answer(
        question,
        documents
    )

    print("\n====================")
    print("ANSWER")
    print("====================")
    print(answer)


if __name__ == "__main__":
    main()